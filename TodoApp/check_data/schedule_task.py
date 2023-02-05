import asyncio
import time
from TodoApp.crawl_data.crawl_data import crawl_data, create_data_five_minute
from TodoApp.check_data.save_data_to_database import PostgresNoDuplicates
from TodoApp.check_data.check_data_daily import CheckDataDaily

is_check_5_minute = False


async def task_daily():
    # async with httpx.AsyncClient() as client:
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(10)
        if int(local_time.tm_hour) == 18 and int(local_time.tm_min) == 50 and int(local_time.tm_sec) < 20:
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
    save_data.process_item_five_minute(create_data_five_minute())
    owner_id_list = CheckDataDaily().check_all_id()
    for i in range(len(owner_id_list)):
        # CheckDataDaily().check_data_daily(owner_id_list[i])
        CheckDataDaily().check_data_five_minute(owner_id_list[i])
    save_data.close_database()


async def task_five_minute():
    # async with httpx.AsyncClient() as client:
    global is_check_5_minute
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(1)
        if int(local_time.tm_min) % 2 == 0 and (int(local_time.tm_sec) in [0, 5]):
            is_check_5_minute = False
            if not is_check_5_minute:
                # print("time: ", local_time.tm_sec)
                save_data = PostgresNoDuplicates()
                finish_1 = time.time() - seconds
                # print('finish_1=', finish_1)
                save_data.process_item_five_minute(create_data_five_minute())
                finish_2 = time.time() - seconds
                # print('finish_2=', finish_2)
                owner_id_list = CheckDataDaily().check_all_id()
                finish_3 = time.time() - seconds
                # print('finish_3=', finish_3)
                for i in range(len(owner_id_list)):
                    # for j in ['x2', 'x3', 'x4', 'L2', 'L3', 'L4', 'D2', 'D3', 'D4']:
                    CheckDataDaily().check_data_five_minute(owner_id_list[i])
                finish_4 = time.time() - seconds
                print('finish_4=', finish_4)
                save_data.close_database()
                is_check_5_minute = True


async def task_new_day():
    # async with httpx.AsyncClient() as client:
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(2)
        if int(local_time.tm_hour) == 0 and int(local_time.tm_min) == 0 and int(local_time.tm_sec) < 30:
            owner_id_list = CheckDataDaily().check_all_id()
            for i in range(len(owner_id_list)):
                CheckDataDaily().set_data_new_day(owner_id_list[i])
