from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from common.auth import CurrentUser, get_current_user, get_admin_user
from containers import Container
from user.application.user_service import UserService

"""
파이단틱은 데이터 유효성 검사와 직렬화/역직렬화를 위해 FastAPI가 기본으로 사용하는 라이브러리 Jackson 같은거인듯
파이썬의 타입힌트를 이용해 유효성을 검증함
"""
router = APIRouter(prefix="/users", tags=["users"])

class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

@router.post("", status_code=201)
@inject
def create_user(
    user: CreateUserBody,
    user_service: UserService = Depends(Provide[Container.user_service]), # dependency-injector 이용
    # user_service = Annotated[UserService, Depends(UserService)] # 단순 Depends 이용
):
    return user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )

class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)

@router.put("", response_model=UserResponse)
@inject
def update_user(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        body: UpdateUserBody,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.update_user(
        user_id=current_user.id,
        name=body.name,
        password=body.password,
    )

class GetUsersResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]


@router.get("")
@inject
def get_users(
    current_user: Annotated[CurrentUser, Depends(get_admin_user)],
    page: int = 1,
    items_per_page: int = 10,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> GetUsersResponse:
    total_count, users = user_service.get_users(page, items_per_page)

    return GetUsersResponse(
        total_count=total_count,
        page=page,
        users=[UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at
        ) for user in users]
    )


@router.delete("", status_code=204)
@inject
def delete_user(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(current_user.id)

@router.post("/login")
@inject
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    access_token = user_service.login(
        email=form_data.username,
        password=form_data.password,
    )

    return {"access_token": access_token, "token_type": "bearer"}