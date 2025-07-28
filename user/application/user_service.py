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
            memo: str,
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