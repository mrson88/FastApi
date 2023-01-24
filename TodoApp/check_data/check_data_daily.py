import psycopg2

from TodoApp.check_time.check_time_data import time_minute, time_hour, before_x_day, time_today, date_today_strf


class CheckDataDaily:
    def __init__(self):
        # Connection Details
        hostname = 'localhost'
        # hostname = '14.225.36.120'
        username = 'postgres'
        password = 'daovanson88'  # your password
        database = 'mrsondb'

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

    def checkdata(self, id_owner):
        xien = [100, 200, 300]

        if int(time_hour()) > 18 and int(time_minute()) > 30:
            self.cur.execute("select result from result_daily where day = %s", (date_today_strf(),))
        else:
            self.cur.execute("select result from result_daily where day = %s", (before_x_day(2),))
        result = self.cur.fetchone()
        # print(type(result[0]))
        if result:
            result_calculate = []
            for i in range(len(result[0])):
                result_calculate.append(result[0][i][-2:])
            # print(result_calculate)

            for i in range(2, 5):
                self.cur.execute(
                    "select data from xsmb where date = %s and data_type = %s and owner_id = %s and active = %s",
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
                self.cur.execute(f"update payment set data_money=data_money+{x}*%s where owner_id = %s",
                                 (xien[i - 2], id_owner,))
                self.connection.commit()

                # print(len(result_data))
                self.cur.execute("update xsmb set active=true where date = %s and data_type = %s and owner_id = %s",
                                 (date_today_strf(), f'x{i}', id_owner))
                self.connection.commit()

    def check_data_five_minute(self, id_owner):
        xien_5p = 100

        self.cur.execute("select result from result_five_minute where day = %s",
                         (date_today_strf(),))
        result = self.cur.fetchone()
        # print('result_five_minute=', result)

        self.cur.execute("select data from xsmb where date = %s and data_type = %s and owner_id = %s and active = %s",
                         (date_today_strf(), 'xs_5p', id_owner, False))
        result_data = self.cur.fetchall()
        # print('result_data_five_minute=', result_data)

        if result:
            result_calculate = []
            for i in range(len(result[0])):
                result_calculate.append(result[0][i])
            # print(result_calculate)

            # print(len(result_data))
            # print((result_data))
            for j in range(len(result_data)):
                x = 0
                aa = result_data[j][0]
                # print((aa))
                for k in range(len(aa)):
                    bb = aa[k]
                    # if set(bb).issubset(result_calculate):
                    if bb in result_calculate:
                        x += 1
                        print('bb=', bb)
                # print('x=', x)
                if x > 0:
                    self.cur.execute(f"update payment set data_money=data_money+{x}*%s where owner_id = %s",
                                     (xien_5p, id_owner,))
                    self.connection.commit()

                # print(len(result_data))

            self.cur.execute("update xsmb set active=true where date = %s and data_type = %s and owner_id = %s",
                             (date_today_strf(), 'xs_5p', id_owner))
            self.connection.commit()
