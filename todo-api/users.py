from sqlalchemy import Column, Integer, String
from database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True)
    hashed_password = Column(String(200))

def hash_password(password: str) -> str:
    return pwd_context.hash(password)  # şifreyi hashle

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)  # şifreyi kontrol et