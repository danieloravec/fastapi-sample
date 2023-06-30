from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine
from db.tokens import create_access_token

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/login")
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.Token:
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if not crud.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"user_id": db_user.id})
    return schemas.Token(access_token=token, token_type="Bearer")
