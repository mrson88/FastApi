import asyncio
import time
from TodoApp.crawl_data.crawl_data import crawl_data, create_data_two_minute
from TodoApp.check_data.save_data_to_database import PostgresNoDuplicates
from TodoApp.check_data.check_data_daily import CheckDataDaily

is_check_2_minute = False


async def task_daily():
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(60)
        if int(local_time.tm_hour) == 18 and 31 < int(local_time.tm_min) < 50:
            print("time: ", local_time.tm_sec)
            save_data = PostgresNoDuplicates()
            if save_data.process_item(crawl_data()):
                owner_id_list = CheckDataDaily().check_all_id()
                for i in range(len(owner_id_list)):
                    CheckDataDaily().check_data(owner_id_list[i], 'xs_mb')
                save_data.close_database()


async def task_check():
    seconds = time.time()
    local_time = time.localtime(seconds)
    # print("time: ", local_time.tm_sec)
    save_data = PostgresNoDuplicates()
    save_data.process_item(crawl_data())
    save_data.process_item_two_minute(create_data_two_minute())
    owner_id_list = CheckDataDaily().check_all_id()
    for i in range(len(owner_id_list)):
        # CheckDataDaily().check_data_daily(owner_id_list[i])
        CheckDataDaily().check_data(owner_id_list[i], 'xs_2p')
    save_data.close_database()


async def task_two_minute():
    global is_check_2_minute
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(1)
        if int(local_time.tm_min) % 2 == 0 and (int(local_time.tm_sec) in [0, 5]):
            is_check_2_minute = False
            if not is_check_2_minute:
                save_data = PostgresNoDuplicates()
                save_data.process_item_two_minute(create_data_two_minute())
                owner_id_list = CheckDataDaily().check_all_id()
                for i in range(len(owner_id_list)):
                    CheckDataDaily().check_data(owner_id_list[i], 'xs_2p')
                # finish_4 = time.time() - seconds
                # print('finish_4=', finish_4)
                save_data.close_database()
                is_check_2_minute = True


async def task_new_day():
    while True:
        seconds = time.time()
        local_time = time.localtime(seconds)

        await asyncio.sleep(2)
        if int(local_time.tm_hour) == 0 and int(local_time.tm_min) == 0 and int(local_time.tm_sec) < 30:
            owner_id_list = CheckDataDaily().check_all_id()
            for i in range(len(owner_id_list)):
                CheckDataDaily().set_data_new_day(owner_id_list[i])
