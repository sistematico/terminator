#!/usr/bin/env python

import os
try:
    from terminator.credentials import BOT_TOKEN, BOT_URL
except ModuleNotFoundError:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    BOT_URL = os.environ.get('WEBHOOK_URL', 'https://terminator.fly.dev/')

BOT_PORT = int(os.environ.get('PORT', '8443'))
BOT_MODE = os.environ.get('ENV', 'production')

DB_FILE = 'data/database.db'
SQL_FILE = 'sql/database.sql'
