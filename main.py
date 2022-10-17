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

if os.path.exists(db_file):
    os.remove(db_file)
else:
    print(f"O arquivo {db_file} não existe.")

def create_tables(banco):
    connection = sqlite3.connect(banco)
    #print(connection.total_changes)

    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grupos 
        (id integer PRIMARY KEY, gid integer, nome text, flags integer DEFAULT 111)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
           id integer PRIMARY KEY,
           uid integer,
           gid integer,
           apelido text,
           nome text,
           warnings integer,
           likes integer,
           FOREIGN KEY(gid) REFERENCES grupos (gid)
        )
    """)

    connection.close()


create_tables(db_file)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Olá {user.mention_markdown_v2()}\!', reply_markup=ForceReply(selective=True), )

def get_warnings(user, chat) -> int:
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # cursor.execute("""
    #     SELECT user_id, warnings, gid 
    #     FROM usuarios 
    #     WHERE user_id = :user_id AND gid = :chat_id""", 
    #     { "user_id": user.id, "chat_id":  chat.id }
    # )

    cursor.execute("""
        SELECT uid, warnings, gid 
        FROM usuarios 
        WHERE uid = :user_id AND gid = :chat_id""", 
        { "user_id": user.id, "chat_id":  chat.id }
    )

    print(rows)

    rows = cursor.fetchone()
    connection.close()

    if rows:
        return rows[0].warnings
    else:
        return 0

def add_warn(user, chat):
    warnings = get_warnings(user, chat) + 1
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    #cursor.execute("SELECT user_id, warnings, gid FROM usuarios WHERE user_id = ? AND gid = ?", (user.id, chat.id,))
    cursor.execute("INSERT INTO grupos (gid, nome) VALUES (?, ?)", (abs(chat.id), chat.title))
    cursor.execute("INSERT INTO usuarios (uid, warnings) VALUES (?, ?)", (user.id, warnings))
    
    connection.close()

    return warnings

def warn(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        chat = update.message.chat
        user = update.message.reply_to_message.from_user
        warnings = add_warn(user, chat)

        print("++++++++++++++++++++++++++++++++++++++")
        print("User Object")
        print(user)

        context.bot.send_message(update.message.chat_id, fr'O usuário @{user.username} agora tem {warnings} warnings!')


def warns(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat = update.message.chat

    print("----------------------------------")
    print("User Object")
    print(user)

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE user_id = :user_id", { "user_id": int(user.id) })
    rows = cursor.fetchone()

    if rows:
        context.bot.send_message(update.message.chat_id, str(rows[0]))
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

    if bot_mode == 'development':
        updater.start_polling()

    if bot_mode == 'production':
        updater.start_webhook(listen="0.0.0.0",
                              port=bot_port,
                              url_path=bot_token,
                              webhook_url=bot_url + bot_token)

    updater.idle()


if __name__ == '__main__':
    main()
