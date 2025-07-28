from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.auth import settings

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./"
    f"{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # autocommit True이면 데이터베이스 롤백이 안된다

Base = declarative_base()