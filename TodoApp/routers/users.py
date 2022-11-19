from fastapi import Depends, HTTPException, status, APIRouter
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import sys
from pydantic import BaseModel
from typing import Optional

sys.path.append("..")
from .auth import get_current_user, get_user_exception, verify_password, get_password_hash

from TodoApp.routers.todos import http_exception

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={401: {'user': 'Not Authorized'}}

)


def get_db():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/")
async def get_all_user(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/user/")
async def user_by_query(user_id: int,
                        db: Session = Depends(get_db)):
    user_model = db.query(models.Users) \
        .filter(models.Users.id == user_id) \
        .first()
    if user_model is not None:
        return user_model
    return 'Invalid user_id'


@router.get("/{user_id}")
async def get_user(user_id: int,
                   db: Session = Depends(get_db)):
    user_model = db.query(models.Users) \
        .filter(models.Users.id == user_id) \
        .first()
    if user_model is not None:
        return user_model
    return 'Invalid user_id'


@router.put('/user/password/')
async def user_password_change(user_verification: UserVerification, user: dict = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(user_verification.password,
                                                                                 user_model.hashed_password):
            user_model.hashe_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return 'Succesfull'
    return 'Invalid user or request'


@router.delete("/user")
async def delete_user(user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users) \
        .filter(models.Users.id == user.get("id")) \
        .first()

    if user_model is None:
        return 'Invalid user'

    db.query(models.Users) \
        .filter(models.Users.id == user.get('id')) \
        .delete()

    db.commit()

    return 'Delete Successfull'
