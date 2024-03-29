import sys
from datetime import datetime, timedelta

sys.path.append("..")
from sqlalchemy import create_engine, Column, Integer, Date, func, text
from typing import Optional, List
from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception
from TodoApp.check_data.schedule_task import task_check
import asyncio
from TodoApp.check_time.check_time_data import date_today_strf, time_today, time_today_second, before_x_day, \
    time_minute, time_hour

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
    data_type: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class PaymentHistory(BaseModel):
    date: Optional[str]
    time: Optional[str]
    data_money: Optional[float]
    data_type: Optional[str]
    result_his: List[List[str]]


class Users(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]


class DataInput(BaseModel):
    data_column: str
    value_column: int


class DataOutput(BaseModel):
    data_column: str
    value_sum: int


@router.post('/check')
async def f():
    asyncio.create_task(task_check())
    return successful_response(200)


@router.get("/user")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    list_user_id = db.query(models.Payment) \
        .filter(models.Payment.owner_id == user.get("id")) \
        .all()
    return list_user_id


@router.get("/name_user")
async def read_username(user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    list_user_name = db.query(models.Users.first_name, models.Users.last_name) \
        .filter(models.Users.id == user.get("id")) \
        .first()
    return list_user_name


@router.get("/top_user")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    list_top_user = db.query(models.Payment) \
        .order_by(models.Payment.data_money.desc()).limit(10) \
        .all()
    return list_top_user


@router.post("/create_payment")
async def create_payment(payment: Payment,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    payment_model = models.Payment()
    payment_model.date = date_today_strf()
    payment_model.time = time_today_second()
    if payment.data_money < 100000001:
        payment_model.data_money = payment.data_money
    else:
        raise http_exception()
    payment_model.first_name = payment.first_name
    payment_model.last_name = payment.last_name
    payment_model.owner_id = user.get("id")
    payment_model.active = True
    payment_model.daily_pay = True
    payment_model.time_pay = 0
    db.add(payment_model)
    db.commit()
    db.close()
    return successful_response(200)


@router.put("/minus_money/{payment_id}")
async def minus_payment(payment_id: int,
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

    payment_model.date = date_today_strf()
    payment_model.time = time_today_second()
    payment_model.data_type = payment.data_type
    if float(payment.data_money) > 0:
        if payment.data_type in ['x2', 'x3', 'x4']:
            payment_model.data_money -= float(payment.data_money) * 10000
        elif payment.data_type in ['L2']:
            payment_model.data_money -= float(payment.data_money) * 27000
        elif payment.data_type in ['L3', 'L4']:
            payment_model.data_money -= float(payment.data_money) * 20000
        elif payment.data_type in ['D2', 'D3', 'D4']:
            payment_model.data_money -= float(payment.data_money) * 1000
        else:
            payment_model.data_money -= 0
        if float(payment_model.data_money) >= 0:
            db.add(payment_model)
            db.commit()
            db.close()
            return successful_response(200)
        else:
            raise http_exception()
    else:
        raise http_exception()


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

    payment_model.date = date_today_strf()
    payment_model.time = time_today_second()
    payment_model.data_type = payment.data_type
    if payment_model.time_pay < 6:
        payment_model.time_pay += 1
    else:
        raise http_exception()
    if float(payment.data_money) > 0 and payment_model.active:

        if payment.data_money < 10000001:
            payment_model.data_money += payment.data_money
        else:
            raise http_exception()
        db.add(payment_model)
        db.commit()
        db.close()
        return successful_response(200)
    else:
        raise http_exception()


@router.get("/payment_history")
async def read_payment_history_by_user(user: dict = Depends(get_current_user),
                                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    list_payment_id = db.query(models.PaymentHistory) \
        .filter(models.PaymentHistory.owner_id == user.get("id")) \
        .order_by(models.PaymentHistory.id.desc()).limit(100) \
        .all()

    return list_payment_id


@router.get("/payment_history_all/{day}")
async def read_payment_history_all(day: str, db: Session = Depends(get_db)):
    data_type_list = ['x2', 'x3', 'x4', 'L2', 'L3', 'L4', 'D2', 'D3', 'D4']
    data_type_win_list = [('win_' + str(i)) for i in data_type_list]
    list_user_id = db.query(models.Payment.owner_id, models.Payment.first_name, models.Payment.last_name).limit(10) \
        .all()
    list_day = [str((datetime.now().date() - timedelta(days=i)).strftime("%d-%m-%Y")) for i in range(int(day))]
    all_data = []
    for k in list_user_id:
        list_payment_all = 0
        list_win_all = 0
        lis_cost_all = 0
        final_payment = 0

        for i in list_day:
            # print(i)
            list_payment = db.query(func.sum(models.PaymentHistory.data_money)).filter(
                models.PaymentHistory.date == str(i), models.PaymentHistory.owner_id == k[0],
                models.PaymentHistory.data_money < 0
            ).scalar()
            list_win = db.query(func.sum(models.PaymentHistory.data_money)).filter(
                models.PaymentHistory.date == str(i), models.PaymentHistory.owner_id == k[0],
                models.PaymentHistory.data_money > 0
            ).scalar()
            if list_payment is not None:
                list_payment_all += list_payment
            if list_win is not None:
                list_win_all += list_win
            final_payment += float(list_payment_all) + float(list_win_all)
        all_data.append([k[0], str(final_payment), f"{str(k[1])} {str(k[2])}"])
    all_data_final = sorted(all_data, key=lambda alldata: float(alldata[1]), reverse=True)
    return all_data_final


@router.post("/payment_history")
async def create_payment_history(payment_his: PaymentHistory,
                                 user: dict = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    payment_his_model = models.PaymentHistory()
    payment_his_model.date = date_today_strf()
    payment_his_model.time = time_today_second()
    payment_his_model.data_type = payment_his.data_type
    payment_his_model.result_his = payment_his.result_his
    payment_his_model.owner_id = user.get("id")
    if payment_his.data_type in ['x2', 'x3', 'x4']:
        payment_his_model.data_money = payment_his.data_money * 10000
    elif payment_his.data_type in ['L2']:
        payment_his_model.data_money = payment_his.data_money * 27000
    elif payment_his.data_type in ['L3', 'L4']:
        payment_his_model.data_money = payment_his.data_money * 20000
    elif payment_his.data_type in ['D2', 'D3', 'D4']:
        payment_his_model.data_money = payment_his.data_money * 1000
    else:
        raise http_exception()

    db.add(payment_his_model)
    db.commit()
    db.close()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
