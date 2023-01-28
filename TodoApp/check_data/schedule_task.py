import asyncio
import time
from TodoApp.crawl_data.crawl_data import crawl_data, create_data_five_minute
from TodoApp.check_data.save_data_to_database import PostgresNoDuplicates
from TodoApp.check_data.check_data_daily import CheckDataDaily


async def task():
    # async with httpx.AsyncClient() as client:
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(10)
        if int(local_time.tm_hour) == 18 and int(local_time.tm_min) == 35 and int(local_time.tm_sec) < 20:
            # print("time: ", local_time.tm_sec)
            save_data = PostgresNoDuplicates()
            save_data.process_item(crawl_data())
            owner_id_list = CheckDataDaily().check_all_id()
            for i in range(len(owner_id_list)):
                CheckDataDaily().check_data_daily(owner_id_list[i])
            save_data.close_database()


async def task_check():
    seconds = time.time()
    local_time = time.localtime(seconds)
    # print("time: ", local_time.tm_sec)
    save_data = PostgresNoDuplicates()
    save_data.process_item(crawl_data())
    owner_id_list = CheckDataDaily().check_all_id()
    for i in range(len(owner_id_list)):
        CheckDataDaily().check_data_daily(owner_id_list[i])
        CheckDataDaily().check_data_five_minute(owner_id_list[i])
    save_data.close_database()


async def task_five_minute():
    # async with httpx.AsyncClient() as client:
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(10)
        if int(local_time.tm_min) % 5 == 0 and int(local_time.tm_sec) < 10:
            # print("time: ", local_time.tm_sec)
            save_data = PostgresNoDuplicates()
            save_data.process_item_five_minute(create_data_five_minute())
            owner_id_list = CheckDataDaily().check_all_id()
            for i in range(len(owner_id_list)):
                CheckDataDaily().check_data_five_minute(owner_id_list[i])
            save_data.close_database()
