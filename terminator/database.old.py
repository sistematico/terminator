import sqlite3
from config import DB_FILE, SQL_FILE


class Database(object):
    # def __init__(self):
    #     self.connection = sqlite3.connect(DB_FILE, check_same_thread=False)
    #     # self.connection.set_trace_callback(print) # DEBUG
    #     self.cursor = self.connection.cursor()

    # # def __enter__(self):
    # #     return self

    # # def __exit__(self):
    # #     return

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()

    def fetchone(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        self.close()

        if row:
            return row
        else:
            return False

    def fetchall(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.close()

        if rows:
            return rows
        else:
            return False

    def create_table(self):
        with open(SQL_FILE, 'r') as sql_file:
            self.connection.executescript(sql_file.read())

    def insert(self, payload, params):
        return


    def insert_or_replace(self, payload, params, table='usuarios'):
        sql="INSERT OR REPLACE INTO " + table

        params=params.split(',')

        for param in params:
            p=(*param, sep=',')
            p=param + ","
            b=f"{param}"

        # s4=" ".join([s1,s2])

        return

    def execute(self, payload, params):
        self.connection.close()

        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()

        self.cursor.execute(payload, params)

        self.connection.commit()

        self.connection.close()

    def executemany(self, payload):
        # self.connection.close()

        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()

        for s in payload:
            print(s['query'], s['params'])
            self.cursor.executemany(s['query'], s['params'])

        self.connection.commit()

        self.connection.close()

    # def executemany(self, payload, params):
    #     self.cursor.executemany(payload, params)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
        self.cursor.close()
