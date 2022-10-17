#!/usr/bin/env python
# pylint: disable=C0116,W0613

import os
import logging
import sqlite3
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
try:
    from credentials import bot_token, bot_url
except ModuleNotFoundError:
    bot_token = os.environ.get('BOT_TOKEN')
    bot_url = os.environ.get('WEBHOOK_URL', 'https://terminator.fly.dev/')

bot_port = int(os.environ.get('PORT', '8443'))
bot_mode = os.environ.get('ENV', 'production')
db_file = r'data/database.db'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)
logger = logging.getLogger(__name__)

connection = sqlite3.connect(db_file)
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS grupos 
    (id integer PRIMARY KEY, gid integer UNIQUE, nome text, flags integer DEFAULT 111)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id integer PRIMARY KEY,
        uid integer UNIQUE,
        gid integer,
        apelido text,
        nome text,
        warnings integer NOT NULL DEFAULT 0,
        likes integer NOT NULL DEFAULT 0,
        FOREIGN KEY(gid) REFERENCES grupos (gid)
    )
""")

connection.close()

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Olá {user.mention_markdown_v2()}\!', reply_markup=ForceReply(selective=True), )

def get_warnings(user, chat) -> int:
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("SELECT uid, gid, warnings FROM usuarios WHERE uid = ? AND gid = ? LIMIT 1", (abs(user.id), abs(chat.id)))

    rows = cursor.fetchone()
    connection.close()

    if rows:
        return rows[2]
    else:
        return 0

def add_warn(user, chat):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("INSERT OR IGNORE INTO grupos (gid, nome) VALUES (?, ?)", (abs(chat.id), chat.title))
    
    # query = cursor.execute("""
    #     insert or replace into usuarios (uid, gid, warnings) values (
    #     (SELECT uid FROM usuarios WHERE uid = :user_id),
    #     (SELECT gid FROM usuarios WHERE gid = :group_id),
    #     (SELECT warnings FROM usuarios WHERE uid = :user_id AND gid = :group_id) + 1)
    #     RETURNING warnings;""", 
    #     { "user_id": abs(user.id), "group_id": abs(chat.id) }
    # )

    cursor.execute("""
        INSERT INTO usuarios (uid, gid, warnings)
        VALUES (
            :uid, 
            :gid, 
            :idade
        )
        ON CONFLICT(uid) 
        DO UPDATE SET warnings = warnings + 1
        RETURNING warnings;""", 
        {"nome": "Lucas", "email": "sistematico@gmail.com", "idade": 39}
    )

# (select warnings from usuarios where uid = :user_id) + 1) 
    

#     insert or replace into Book (ID, Name, TypeID, Level, Seen) values (
#    (select ID from Book where Name = "SearchName"),
#    "SearchName",
#     5,
#     6,
#     (select Seen from Book where Name = "SearchName"));


    warnings = query.fetchone()
    connection.commit()
    connection.close()

    print(warnings[0])

    if warnings:
        return warnings[0]
    else:
        return 1   


def warn(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        chat = update.message.chat
        warnings = add_warn(user, chat)
        context.bot.send_message(update.message.chat_id, fr'O usuário @{user.username} agora tem {warnings} warnings!')


def warns(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.message.chat

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE uid = ? AND gid = ?", (int(user.id), int(chat.id)))
    rows = cursor.fetchone()

    if rows:
        context.bot.send_message(update.message.chat_id, str(rows))
    else:
        context.bot.send_message(update.message.chat_id, "Nenhum warn.")

    connection.close()


def main() -> None:
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("warn", warn))
    dispatcher.add_handler(CommandHandler("warns", warns))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, bio))

    if bot_mode == 'development' or bot_mode == 'dev':
        updater.start_polling()

    if bot_mode == 'production':
        updater.start_webhook(listen="0.0.0.0",
                              port=bot_port,
                              url_path=bot_token,
                              webhook_url=bot_url + bot_token)

    updater.idle()


if __name__ == '__main__':
    main()
