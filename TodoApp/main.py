from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, todos, xsmb, payment
from company import companyapis, dependencies
from crawl_data.schedule_task import task
import asyncio

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(xsmb.router)
app.include_router(payment.router)


# app.include_router(
#     companyapis.router,
#     prefix="/companyapis",
#     tags=["companysapis"],
#     dependencies=[Depends(dependencies.get_token_header)],
#     responses={418: {"description": "Internal Use Only"}}
# )

@app.on_event('startup')
def start_up():
    asyncio.create_task(task())
