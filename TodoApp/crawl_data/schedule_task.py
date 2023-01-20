import asyncio
import time
from .crawl_data import crawl_data
from .save_data_to_database import PostgresNoDuplicates
from .check_data_daily import CheckDataDaily


async def task():
    # async with httpx.AsyncClient() as client:
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(10)
        if int(local_time.tm_hour) == 18 and int(local_time.tm_min) == 40:
            print("time: ", local_time.tm_sec)
            save_data = PostgresNoDuplicates()
            save_data.process_item(crawl_data())
            owner_id_list = CheckDataDaily().check_all_id()
            for i in range(len(owner_id_list)):
                CheckDataDaily().checkdata(owner_id_list[i])
            save_data.close_database()


async def task_check():
    # async with httpx.AsyncClient() as client:
    # while True:
    seconds = time.time()
    local_time = time.localtime(seconds)
    print("time: ", local_time.tm_sec)
    save_data = PostgresNoDuplicates()
    save_data.process_item(crawl_data())
    owner_id_list = CheckDataDaily().check_all_id()
    for i in range(len(owner_id_list)):
        CheckDataDaily().checkdata(owner_id_list[i])
    save_data.close_database()

    # await asyncio.sleep(10)
    # if int(local_time.tm_hour) == 11 and int(local_time.tm_min) == 32:
    #     print("time: ", local_time.tm_sec)
    #     save_data = PostgresNoDuplicates()
    #     save_data.process_item(crawl_data())
    #     CheckDataDaily().checkdata()
    #     save_data.close_database()
