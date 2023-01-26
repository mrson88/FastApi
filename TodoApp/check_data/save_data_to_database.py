import psycopg2


class PostgresNoDuplicates:

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

    def process_item(self, item):
        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS result_daily(
            id serial PRIMARY KEY,
            day varchar(10),
            result varchar(400)
            )
        """)
        # Check to see if text is already in database

        self.cur.execute("select * from result_daily where day = %s", (str(item[0]).replace('/', '-'),))

        result = self.cur.fetchone()
        # print(str(item))

        # If it is in DB, create log message
        if result:
            return
            # print("Item already in database: %s" % str(item[0]))

        # If text isn't in the DB, insert data
        else:
            # Define insert statement
            self.cur.execute(""" insert into result_daily (day, result) values (%s,%s)""",
                             (str(item[0]).replace('/', '-'),
                              item[1],
                              ))

            # print('save data ok')

            # Execute insert of data into database
            self.connection.commit()

    def process_item_five_minute(self, item):
        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS result_five_minute(
            id serial PRIMARY KEY,
            day varchar(10),
            time varchar(10),
            result varchar(400),
            ischeck bool default false
            )
        """)
        # Check to see if text is already in database

        self.cur.execute("select * from result_five_minute where day = %s and time = %s", (item[0], item[1],))

        result = self.cur.fetchone()
        # print(str(item))

        # If it is in DB, create log message
        if result:
            # print("Item already in database: %s" % str(item[1]))
            return

        # If text isn't in the DB, insert data
        else:

            # Define insert statement
            self.cur.execute(""" insert into result_five_minute (day, time, result) values (%s,%s,%s)""",
                             (str(item[0]), str(item[1]), item[2],))

            # print('save data ok')

            # Execute insert of data into database
            self.connection.commit()

    def close_database(self):
        # Close cursor & connection to database
        self.cur.close()
        self.connection.close()
