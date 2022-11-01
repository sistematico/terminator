import os

try:
    from terminator.credentials import BOT_TOKEN, BOT_URL, BOT_PORT
except ModuleNotFoundError:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    BOT_URL = os.environ.get('BOT_URL', 'https://terminator.fly.dev/')

BOT_PORT = int(os.environ.get('BOT_PORT', 8443))
BOT_MODE = os.environ.get('ENV', 'production')

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
IMAGES_DIR = os.path.join(ROOT_DIR, 'data', 'img')

DB_FILE = os.path.join(ROOT_DIR, 'data', 'database.db')
SQL_FILE = os.path.join(ROOT_DIR, 'data', 'install.sql')

sqldict = {
  "create": "CREATE TABLE IF NOT EXISTS {} ({})",
  "drop": "DROP TABLE IF EXISTS {}",
  "select": "SELECT ({}) FROM {}",
  "select_all": "SELECT * FROM {}",
  "insert": "INSERT OR IGNORE INTO {}",
  "update": "UPDATE {} SET {} WHERE {}",
  "delete": "DELETE FROM {} WHERE {}",
  "delete_all": "DELETE FROM {}",
  "search": "SELECT * FROM {} WHERE {}"
}