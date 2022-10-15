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

if os.path.exists(db_file):
    os.remove(db_file)
else:
    print(f"O arquivo {db_file} não existe.")


def create_tables(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grupos (id integer PRIMARY KEY, group_id integer, nome text, flags integer);
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
           id integer PRIMARY KEY,
           user_id integer,
           apelido text,
           nome text,
           warnings integer,
           likes integer,
           gid integer,
           FOREIGN KEY(gid) REFERENCES grupos (id)
        );
    """)

    connection.close()


create_tables(db_file)

# Enable logging
# CRITICAL ERROR WARNING INFO DEBUG NOTSET
# loglevel = 'logging.WARNING' if bot_mode == 'production' else 'logging.DEBUG'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Olá {user.mention_markdown_v2()}\!', reply_markup=ForceReply(selective=True), )


def add_warn(user, chat):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, warnings, gid FROM usuarios WHERE user_id = ? AND gid = ?", (user.id, chat.id,))


    # cursor.execute("""
    #     INSERT INTO usuarios (user_id, apelido, nome)
    #     VALUES (?,?,?)
    # """, (1, fr'@{user.username}', user.first_name))

    # cursor.execute(f"""
    #     INSERT OR REPLACE INTO usuarios (warnings)
    #     values (SELECT * FROM usuarios WHERE user_id = {user.id} AND warnings = warnings + 1)
    #     RETURNING *;
    # """)

    # cursor.execute("""
    # INSERT INTO usuarios (userID, errorMsg, sessionStartTimestamp)
    # VALUES(?, ?, ?)
    # ON CONFLICT(userID, sessionStartTimestamp)
    # DO UPDATE SET errorMsg = 'An error occured'
    # WHERE errorMsg IS NOT NULL
    # RETURNING *;
    # """, ())

    # sql = r"INSERT OR REPLACE INTO usuarios(user_id, warnings) VALUES ((SELECT user_id FROM usuarios WHERE user_id = %i), %i, ifnull((SELECT user_id, warnings FROM usuarios WHERE user_id = %i), 0 ) + 1) RETURNING *;"
    sql = r"INSERT OR REPLACE INTO usuarios(user_id, warnings) VALUES ((SELECT user_id FROM usuarios WHERE user_id = %i), %i, ifnull((SELECT warnings FROM usuarios WHERE user_id = %i), 0 ) + 1)"

    ret = cursor.execute(fr"INSERT OR REPLACE INTO usuarios(user_id, warnings) VALUES ((SELECT warnings FROM usuarios WHERE user_id = {user.id}), {user.id}, ifnull((SELECT user_id FROM usuarios WHERE user_id = {user.id}), 0 ) + 1)")

    return ret




    # cursor.execute("""
    #     INSERT OR REPLACE INTO usuarios (user_id, warnings) values (?, ?);
    # """, (user.id, 20,))

    # connection.commit()
    connection.close()

    # warnings = cursor.fetchone()

    # if warnings:
    #     return warnings[0].warnings
    # else:
    return 20


#
# UPDATE product SET price = price + 50


def get_warnings(user, chat) -> int:
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, warnings, gid FROM usuarios WHERE user_id = ? AND gid = ?", (user.id, chat.id,))
    rows = cursor.fetchone()
    connection.close()

    if rows:
        return rows[0].warnings
    else:
        return 0


def warn2(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        chat = update.message.chat
        user = update.message.reply_to_message.from_user

        #user = update.effective_user
        #chat = update.effective_chat

        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO grupos (group_id, nome, flags) VALUES (?, ?, ?)
        """, (chat.id, chat.username, 111))

        # inserindo dados na tabela
        cursor.execute("""
            INSERT INTO usuarios (user_id, apelido, nome)
            VALUES (?,?,?)
        """, (1, fr'@{user.username}', user.first_name))

        connection.commit()
        connection.close()

        context.bot.send_message(update.message.chat_id, fr'O usuário @{user.username} agora tem 1 warning!')


def warn(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        chat = update.message.chat
        user = update.message.reply_to_message.from_user
        warnings = add_warn(user, chat)

        context.bot.send_message(update.message.chat_id, fr'O usuário @{user.username} agora tem {warnings} warnings!')


def warns(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    chat = update.effective_chat

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user.id,))
    rows = cursor.fetchone()

    if rows:
        context.bot.send_message(update.message.chat_id, str(rows[0]))
    else:
        context.bot.send_message(update.message.chat_id, "Nenhum warn.")


    # connection.close()


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
