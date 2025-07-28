from http.client import HTTPException
from ulid import ULID
from datetime import datetime
from user.domain.user import User
from user.domain.repository.user_repo import IUserRepository
from user.infra.repository.user_repo import UserRepository
from utils.crpyto import Crypto


class UserService:
    def __init__(self):
        self.user_repo: IUserRepository = UserRepository()
        self.ulid = ULID()
        self.crypto = Crypto()

    def create_user(self, name: str, email: str, password: str) -> User:
        _user = None
        try:
            _user = self.user_repo.find_by_email(email)
        except HTTPException as e:
            if e.status_code != 422:
                raise e

        if _user:
            raise HTTPException(statsu_code=422) # 이미 가입한 유저의 경우 422 에러

        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            created_at=now,
            updated_at=now,
        )
        self.user_repo.save(user)
        return user