from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from containers import Container
from user.application.user_service import UserService

"""
파이단틱은 데이터 유효성 검사와 직렬화/역직렬화를 위해 FastAPI가 기본으로 사용하는 라이브러리 Jackson 같은거인듯
파이썬의 타입힌트를 이용해 유효성을 검증함
"""
router = APIRouter(prefix="/users", tags=["users"])

class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str

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

class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None

@router.put("/{user_id}")
@inject
def update_user(
        user_id: str,
        user: UpdateUser,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.update_user(
        user_id=user_id,
        name=user.name,
        password=user.password,
    )