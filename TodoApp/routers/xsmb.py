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
    data: List[str]
    data_type: Optional[str]
    data_cost: Optional[str]
    active: bool


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
    xsmb_model.data_type = xsmb.data_type
    xsmb_model.data_cost = str(float(xsmb.data_cost) * 23000)
    xsmb_model.active = xsmb.active
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
    kq_xsmb_dayly_model = db.query(models.Xsmb) \
        .order_by(models.Xsmb.id.desc()).limit(int(number)).all()
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
