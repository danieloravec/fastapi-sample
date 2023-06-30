from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas


# TODO hide, use .env
SECRET_KEY = "73286341d5ef72d2aba7ae0a9fc6457442dc7e20f4d4f21e4641e02ef680d481"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    db_user = models.User(email=user.email, password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
