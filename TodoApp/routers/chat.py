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
from fastapi import FastAPI
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/messages")
def read_messages():
    return {"messages": []}


@router.post("/messages")
def create_message(message: str):
    data = JSONResponse(content={"message": message})
    print(data)
    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
