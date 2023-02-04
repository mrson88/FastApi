import sys

sys.path.append("..")

from typing import Optional, List
from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/xsmb",
    tags=["xsmb"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Xsmb(BaseModel):
    date: Optional[str]
    time: Optional[str]
    data: List[Optional[str]]
    data_type: Optional[str]
    data_cost: Optional[str]
    xs_type: Optional[str]
    is_check: bool


# class ResultDaily(BaseModel):
#     day: str
#     result: List[str]


class ResultFiveMinute(BaseModel):
    day: Optional[str]
    time: Optional[str]
    result: List[str]
    ischeck: bool


class ResultDaily(BaseModel):
    day: Optional[str]
    result: List[str]


@router.post("/add_loto")
async def create_xsmb(xsmb: Xsmb,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    xsmb_model = models.Xsmb()
    xsmb_model.date = xsmb.date
    xsmb_model.time = xsmb.time
    xsmb_model.data = xsmb.data
    xsmb_model.xs_type = xsmb.xs_type
    xsmb_model.data_type = xsmb.data_type
    print(xsmb.data)
    print(xsmb.data_type)
    print(xsmb.xs_type)
    if float(xsmb.data_cost) > 0:
        if xsmb.data_type in ['x2', 'x3', 'x4', ]:
            xsmb_model.data_cost = str(float(xsmb.data_cost) * 10000)
        if xsmb.data_type in ['L2']:
            xsmb_model.data_cost = str(float(xsmb.data_cost) * 27000)
        if xsmb.data_type in ['L3', 'L4']:
            xsmb_model.data_cost = str(float(xsmb.data_cost) * 20000)
        if xsmb.data_type in ['D2', 'D3', 'D4']:
            xsmb_model.data_cost = str(float(xsmb.data_cost) * 1000)
    else:
        raise http_exception()
    xsmb_model.is_check = xsmb.is_check
    xsmb_model.owner_id = user.get("id")
    db.add(xsmb_model)
    db.commit()

    return successful_response(201)


@router.get("/kq-xs5p/{day}")
async def read_kqxs5p_day(day: str,
                          db: Session = Depends(get_db)):
    xs5p_model = db.query(models.ResultFiveMinute.result) \
        .filter(models.ResultFiveMinute.day == day) \
        .order_by(models.ResultFiveMinute.id.desc()).first()
    if xs5p_model is not None:
        return xs5p_model
    raise http_exception()


@router.get("/kq-xs5p-number/{number}")
async def read_kqxs5p_number(number: str,
                             db: Session = Depends(get_db)):
    xs5p_model = db.query(models.ResultFiveMinute) \
        .order_by(models.ResultFiveMinute.id.desc()).limit(int(number)).all()
    if xs5p_model is not None:
        return xs5p_model
    raise http_exception()


@router.get("/xsmb-dayly-number/{number}")
async def read_kqxsmb_number(number: str,
                             db: Session = Depends(get_db)):
    kq_xsmb_dayly_model = db.query(models.ResultDaily) \
        .order_by(models.ResultDaily.id.desc()).limit(int(number)).all()
    if kq_xsmb_dayly_model is not None:
        return kq_xsmb_dayly_model
    raise http_exception()


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
