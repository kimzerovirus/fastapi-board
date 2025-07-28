from abc import ABCMeta, abstractmethod
from user.domain.user import User

# 파이썬에서 제공하는 객체지향 인터페이스를 위한 ABCMeta
class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError # 인터페이스 함수의 구현부는 이 에러를 통해 구현이 필요함을 기술한다.

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        """
        이메일로 유저를 검색한다.
        검색한 유저가 없을 경우 422 에러를 발생한다.
        :param email:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError