import psycopg2
from sqlalchemy.sql import text
from TodoApp.check_time.check_time_data import time_minute, time_hour, before_x_day, time_today, date_today_strf
import os

# os.environ['PASS_DATABASE'] = ''//password

pass_database = os.environ.get("PASS_DATABASE")
database_name = os.environ.get("DATABASE")


class CheckDataDaily:
    def __init__(self):
        # Connection Details
        hostname = 'localhost'
        # hostname = '14.225.36.120'
        username = 'postgres'
        password = pass_database  # your password
        database = 'mrsondb'
        self.eff_money = 23000

        # Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        # ## Create quotes table if none exists
        # self.cur.execute("""
        # CREATE TABLE IF NOT EXISTS result_daily(
        #     id serial PRIMARY KEY,
        #     day varchar(10),
        #     result varchar(255)
        #     )
        # """)

    def check_all_id(self):
        self.cur.execute("select owner_id from payment")
        result_id = self.cur.fetchall()
        # print(result_id)
        return result_id

    def check_data_daily(self, id_owner):

        xien = [99, 99 / 27, 17, 74, 251]

        if int(time_hour()) > 18 and int(time_minute()) > 30:
            self.cur.execute("select result from result_daily where day = %s", (date_today_strf(),))
        else:
            self.cur.execute("select result from result_daily where day = %s", (before_x_day(1),))
        result = self.cur.fetchone()
        # print(type(result[0]))
        if result:
            result_calculate = []
            for i in range(len(result[0])):
                result_calculate.append(result[0][i][-2:])
            # print(result_calculate)

            for i in range(5):
                self.cur.execute(
                    "select data from xsmb where date = %s and data_type = %s and owner_id = %s and is_check = %s",
                    (date_today_strf(), f'x{i}', id_owner, False))
                result_data = self.cur.fetchall()

                x = 0
                for j in range(len(result_data)):

                    aa = list(result_data[j][0])
                    # print(len(aa))
                    for k in range(len(aa)):
                        bb = str(result_data[j][0][k]).split()
                        if set(bb).issubset(result_calculate):
                            x += 1
                            # print('bb=', bb)
                # print('x=', x)
                self.cur.execute(
                    f"update payment set data_money=data_money+{x}*%s where owner_id = %s",
                    (xien[i], id_owner,))
                self.connection.commit()

                # print(len(result_data))
                self.cur.execute("update xsmb set is_check=true where date = %s and data_type = %s and owner_id = %s",
                                 (date_today_strf(), f'x{i}', id_owner))
                self.connection.commit()
                self.cur.close()
                self.connection.close()

    def check_data_five_minute(self, id_owner):
        win_factor = {
            'x2': 17,
            'x3': 74,
            'x4': 251,
            'L2': 99,
            'L3': 97.23 / 2,
            'L4': 450,
            'D2': 99,
            'D3': 972.3,
            'D4': 9000
        }
        data_type_list = ['x2', 'x3', 'x4', 'L2', 'L3', 'L4', 'D2', 'D3', 'D4']
        # print('check data')
        self.cur.execute("select result from result_five_minute where day = %s order by id desc limit 1",
                         (date_today_strf(),))
        result = self.cur.fetchone()
        # print('result=', result)

        self.cur.execute(
            "select data,data_cost,data_type from xsmb where date = %s  and owner_id = %s and is_check = %s",
            (date_today_strf(), id_owner, False))
        result_data = self.cur.fetchall()

        if result and result_data:
            print('result_data_five_minute=', result_data)

            result_calculate = []
            for i in range(len(result[0])):
                result_calculate.append(result[0][i][-2:])
            print('result_calculate=', result_calculate)

            print(len(result_data))
            print('result_data=', result_data)

            for j in range(len(result_data)):
                data_type = result_data[j][2]
                # price = result_data[j][1]
                # print('price=', price)
                x = 0
                result_his = []
                aa = result_data[j][0][0]
                print('aa=', aa)
                for k in range(len(aa)):
                    bb = aa[k]
                    for l in range(len(result_calculate)):
                        if bb == result_calculate[l]:
                            x += 1
                            print('bb=', bb)
                            result_his.append(bb)
                    print('x=', x)
                if x > 0:
                    self.cur.execute(
                        f"update payment set data_money=data_money+{x * 1000}*%s where owner_id = %s",
                        (win_factor[data_type], id_owner,))
                    # self.connection.commit()
                    # print('x=', x)
                    query = "insert into payment_history(date,time,data_money,data_type,owner_id,result_his) values (" \
                            "%s,%s,%s,%s,%s,%s); "
                    self.cur.execute(query,
                                     (
                                         date_today_strf(), time_today(),
                                         f'+{float(round((win_factor[data_type] * x * 1000), 0))}',
                                         data_type,
                                         id_owner, result_his))
                    self.connection.commit()

                print(len(result_data))

            self.cur.execute("update xsmb set is_check=true where date = %s  and owner_id = %s",
                             (date_today_strf(), id_owner))
            self.connection.commit()
            self.cur.close()
            self.connection.close()

    def set_data_new_day(self, id_owner):
        self.cur.execute("update payment set daily_pay=false where owner_id = %s",
                         (id_owner))
        self.connection.commit()
        self.cur.close()
        self.connection.close()
