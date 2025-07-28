from datetime import datetime

from fastapi import HTTPException
from ulid import ULID

from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User
from utils.crpyto import Crypto


class UserService:
    def __init__(
        self,
        user_repo: IUserRepository,
        # user_repo: IUserRepository = Depends(
        #     Provide[Container.user_repository]
        # ), # annotated를 사용하라고 fastapi에서는 권장하지만 지금은 에러나나봄
     ):
        self.user_repo = user_repo
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(
            self,
            name: str,
            email: str,
            password: str,
            memo: str | None = None,
    ) -> User:
        _user = None
        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        if _user:
            raise HTTPException(status_code=422) # 이미 가입한 유저의 경우 422 에러

        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            memo=memo,
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)
        return user

    def update_user(
            self,
            user_id: str,
            name: str | None = None,
            password: str | None = None,
    ):
        user = self.user_repo.find_by_id(user_id)

        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password)

        user.updated_at = datetime.now()

    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        users = self.user_repo.get_users(page, items_per_page)

        return users

    def delete_user(self, user_id: str):
        self.user_repo.delete(user_id)