from passlib.context import CryptContext

class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, secret: str) -> str:
        return self.pwd_context.hash(secret)

    def decrypt(self, secret: str, hash: str) -> bool:
        return self.pwd_context.verify(secret, hash)
