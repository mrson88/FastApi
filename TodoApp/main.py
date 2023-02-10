from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, xsmb, payment
from TodoApp.check_data.schedule_task import task_daily, task_two_minute, task_new_day
import asyncio

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(xsmb.router)
app.include_router(payment.router)


@app.on_event('startup')
def start_up():
    asyncio.create_task(task_two_minute())
    asyncio.create_task(task_daily())
    asyncio.create_task(task_new_day())
