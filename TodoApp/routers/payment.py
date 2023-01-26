import sys

sys.path.append("..")

from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception
from TodoApp.check_data.schedule_task import task_check
import asyncio

router = APIRouter(
    prefix="/payment",
    tags=["payment"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Payment(BaseModel):
    date: Optional[str]
    time: Optional[str]
    data_money: Optional[float]
    active: bool


@router.post('/check')
async def f():
    # seconds = time.time()
    # local_time = time.localtime(seconds)
    asyncio.create_task(task_check())

    return successful_response(200)

    # task()
    # print("time: ", local_time.tm_min)


@router.get("/user")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    list_user_id = db.query(models.Payment) \
        .filter(models.Payment.owner_id == user.get("id")) \
        .all()
    # print(list_user_id)
    return list_user_id


@router.post("/add_money")
async def create_xsmb(payment: Payment,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    payment_model = models.Payment()
    payment_model.date = payment.date
    payment_model.time = payment.time
    payment_model.data_money = payment.data_money
    payment_model.active = payment.active
    payment_model.owner_id = user.get("id")
    db.add(payment_model)
    db.commit()

    return successful_response(201)


@router.put("/minus_money/{payment_id}")
async def update_todo(payment_id: int,
                      payment: Payment,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    payment_model = db.query(models.Payment) \
        .filter(models.Payment.id == payment_id) \
        .filter(models.Payment.owner_id == user.get("id")) \
        .first()

    if payment_model is None:
        raise http_exception()

    payment_model.date = payment.date
    payment_model.time = payment.time
    payment_model.data_money -= payment.data_money
    payment_model.active = payment.active
    if float(payment_model.data_money) >= 0:
        db.add(payment_model)
        db.commit()

        return successful_response(200)
    else:
        return http_exception()


@router.put("/add_money/{payment_id}")
async def update_todo(payment_id: int,
                      payment: Payment,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    payment_model = db.query(models.Payment) \
        .filter(models.Payment.id == payment_id) \
        .filter(models.Payment.owner_id == user.get("id")) \
        .first()

    if payment_model is None:
        raise http_exception()

    payment_model.date = payment.date
    payment_model.time = payment.time
    payment_model.data_money += payment.data_money
    payment_model.active = payment.active
    db.add(payment_model)
    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
