#!/usr/bin/env python

import sqlite3
from terminator.config import *


class Database:
    def __init__(self):
        self.open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        if self.connection:
            try:
                self.connection = sqlite3.connect(DB_FILE, check_same_thread=False, isolation_level=None)  # Auto-Commit
                self.cursor = self.connection.cursor()

            except sqlite3.Error as e:
                print("Error connecting to database: " + e.args[0])

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None

    def install(self):
        self.create_table()

    def execute(self, payload, data):
        self.cursor.execute(payload, data)
        row = self.cursor.fetchone()
        return row[0] if row else False

    def insert(self, payload, data):
        return self.cursor.execute(payload, data)

    def insert_and_return(self, payload, data):
        self.cursor.execute(payload, data)
        row = self.cursor.fetchone()
        return row[0] if row else False

    def get(self, query, data):
        self.cursor.execute(query, data)
        row = self.cursor.fetchone()
        return row[0] if row else False

    def all(self, query, data):
        self.cursor.execute(query, data)
        row = self.cursor.fetchall()
        return row if row else False

    def flush(self, tabela):
        return self.cursor.execute(f"DELETE FROM {tabela}")

    def drop(self, tabela):
        return self.cursor.execute(f"DROP TABLE IF EXISTS {tabela}")

    def create_table(self):
        if self.connection:
            with open(SQL_FILE, 'r') as sql_file:
                self.connection.executescript(sql_file.read())

    def build(self, table, action, data = None, where = None, update = None):
        query = sqldict[action]
        placeholder = ''
        fields = ''

        if data:
            for key in data:
                placeholder = f'{placeholder} :{key}'
                fields = f'{fields} {key},'

            fields = ''.join(fields[0:-1]).strip()
        
        match action:
            case 'create':
                query = query.format(table, fields)
            case 'drop':
                query = query.format(table)
            case 'search':
                query = query.format(table, where)
            case 'update':
                query = query.format(table, update, where)
            case _:
                query = query.format(fields, table)
                query = f'{query} {table}'
                query = f'{query} ({fields}) VALUES ({placeholder.strip()})'

        return query
