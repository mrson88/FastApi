import time
import datetime
import psycopg2


class CheckDataDaily:
    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'daovanson88'  # your password
        database = 'mrsondb'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        ## Create cursor, used to execute commands
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
        print(result_id)
        return result_id

    def checkdata(self, id_owner):
        xien = [100, 200, 300]

        # named_tuple = time.localtime()  # get struct_time
        # time_string = time.strftime("%d/%m/%Y", named_tuple)

        date_today = datetime.date.today()
        no_of_days = datetime.timedelta(days=1)
        before_one_days = (date_today - no_of_days).strftime("%d/%m/%Y")
        date_today_strftime = date_today.strftime("%d/%m/%Y")
        time_today_strtime_hour = time.strftime('%H')
        time_today_strtime_minute = time.strftime('%M')
        print(before_one_days)
        # print(time_today_strtime_hour)
        # print(time_today_strtime_minute)
        if int(time_today_strtime_hour) > 18 and int(time_today_strtime_minute) > 30:
            self.cur.execute("select result from result_daily where day = %s", (date_today_strftime,))
        else:
            self.cur.execute("select result from result_daily where day = %s", (before_one_days,))
        result = self.cur.fetchone()
        # print(result[0])
        result_calculate = []
        for i in range(len(result[0])):
            result_calculate.append(result[0][i][-2:])
        # print(result_calculate)

        for i in range(2, 5):
            self.cur.execute("select data from xsmb where date = %s and data_type = %s and active = %s",
                             (date_today_strftime, f'x{i}', False))
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
            self.cur.execute(f"update payment set data_money=data_money+{x}*%s where owner_id = %s",
                             (xien[i - 2], id_owner,))
            self.connection.commit()

            # print(len(result_data))
            self.cur.execute("update xsmb set active=true where date = %s and data_type = %s",
                             (date_today_strftime, f'x{i}'))
            self.connection.commit()
