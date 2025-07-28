from fastapi import APIRouter
from pydantic import BaseModel

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
def create_user(user: CreateUserBody):
    user_service = UserService()
    return user_service.create_user(
        name=user.name,
        email=user.email,
        password=user.password
    )