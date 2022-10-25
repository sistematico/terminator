#!/usr/bin/env python

import sqlite3
from terminator.config import *


class Database:
    def __init__(self):
        try:
            self.connection = sqlite3.connect(
                DB_FILE, check_same_thread=False, isolation_level=None)  # Auto-Commit
            self.cursor = self.connection.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database!")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None

    def execute(self, payload, data):
        self.cursor.execute(payload, data)
        row = self.cursor.fetchone()
        return row[0]

    def fetchone(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row[0] if row else 'Nenhum resultado.'

    def create_table(self):
        if self.connection:
            with open(SQL_FILE, 'r') as sql_file:
                self.connection.executescript(sql_file.read())
