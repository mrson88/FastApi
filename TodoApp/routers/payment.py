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


class PaymentHistory(BaseModel):
    date: Optional[str]
    time: Optional[str]
    data_money: Optional[float]
    data_type: Optional[str]


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


@router.post("/create_payment")
async def create_payment(payment: Payment,
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

    return successful_response(200)


@router.put("/minus_money/{payment_id}")
async def minus_payment(payment_id: int,
                        payment: Payment,
                        # payment_his: PaymentHistory,
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
    payment_model.data_money -= payment.data_money * 23000
    payment_model.active = payment.active

    if float(payment_model.data_money) >= 0:
        db.add(payment_model)
        # db.add(payment_his_model)
        db.commit()

        return successful_response(200)
    else:
        return http_exception()


@router.put("/add_money/{payment_id}")
async def add_payment(payment_id: int,
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


@router.put("/status_payment/{payment_id}")
async def status_payment(payment_id: int,
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
    payment_model.data_money = payment.data_money + 1000000
    payment_model.active = payment.active
    if not payment_model.active:
        payment_model.active = True
        db.add(payment_model)
        db.commit()
        return successful_response(200)
    else:
        return http_exception()


@router.get("/payment_history")
async def read_payment_history_by_user(user: dict = Depends(get_current_user),
                                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    list_payment_id = db.query(models.PaymentHistory) \
        .filter(models.PaymentHistory.owner_id == user.get("id")) \
        .order_by(models.PaymentHistory.id.desc()).limit(50) \
        .all()

    return list_payment_id


@router.post("/payment_history")
async def create_payment_history(payment_his: PaymentHistory,
                                 user: dict = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    payment_his_model = models.PaymentHistory()
    payment_his_model.date = payment_his.date
    payment_his_model.time = payment_his.time
    payment_his_model.data_money = payment_his.data_money * 23000
    payment_his_model.data_type = payment_his.data_type
    payment_his_model.owner_id = user.get("id")
    db.add(payment_his_model)
    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
