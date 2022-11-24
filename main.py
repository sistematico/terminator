#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from config.definitions import BOT_MODE, BOT_PORT, BOT_URL, BOT_TOKEN
from terminator.decorators import restricted, group
from terminator.warn import awarn, rwarn, cwarn
from terminator.admin import flush, drop, install, uninstall
from terminator.config import status, get_flags, set_flags
from terminator.utils import hora_certa

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_text(update: Update, context: CallbackContext) -> None:
    if "hora certa" in update.message.text.lower():
        horacerta(update, context)

def horacerta(update: Update, context: CallbackContext) -> None:
    hora = hora_certa()
    context.bot.send_message(update.message.chat_id, f'Agora em brasília são: {hora}')

def pong(update: Update, context: CallbackContext) -> None:
    context.bot.delete_message(update.message.chat_id, update.message.message_id)
    context.bot.delete_message(update.message.chat_id, update.message.reply_to_message.message_id)

@group
@restricted
def admin(update: Update, context: CallbackContext) -> None:
    if update.message.text.startswith("install"):
        install(update, context)
    elif "uninstall" in update.message.text:
        uninstall(update, context)
    elif "flush" in update.message.text:
        flush(update, context)
    elif "drop" in update.message.text:
        drop(update, context)
    else:
        return

@group
@restricted
def c_status(update: Update, context: CallbackContext) -> None:
    status(update, context)

@group
@restricted
def get_c_flags(update: Update, context: CallbackContext) -> None:
    if update.message.text.partition(' ')[2]:
        flags = update.message.text.partition(' ')[2]
        get_flags(update, context, flags)
    else:
        get_flags(update, context)


@group
@restricted
def set_c_flags(update: Update, context: CallbackContext) -> None:
    if update.message.text.partition(' ')[2]:
        set_flags(update, update.message.text.partition(' ')[2])

# Warn System
@group
@restricted
def warn(update: Update, context: CallbackContext) -> None:
    awarn(update, context)

def warns(update: Update, context: CallbackContext) -> None:
    cwarn(update, context)

def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("ping", pong))
    dispatcher.add_handler(CommandHandler("status", c_status))
    dispatcher.add_handler(CommandHandler("get", get_c_flags))
    dispatcher.add_handler(CommandHandler("set", set_c_flags))
    dispatcher.add_handler(CommandHandler("warn", warn))
    dispatcher.add_handler(CommandHandler("warns", warns))
    dispatcher.add_handler(CallbackQueryHandler(rwarn))
    dispatcher.add_handler(MessageHandler(Filters.text , admin))
    dispatcher.add_handler(MessageHandler(Filters.text , parse_text))

    # Message is text and contains a link
    # handler = MessageHandler(Filters.text & (Filters.entity(MessageEntity.URL) | Filters.entity(MessageEntity.TEXT_LINK)), callback)

    # Photo & Not Forwarded
    # handler = MessageHandler(Filters.photo & (~ Filters.forwarded), callback)

    if BOT_MODE.startswith('dev'):
        print("Running via long polling...")
        updater.start_polling()
    else:
        print(" Running via webhooks... ")
        updater.start_webhook(listen="0.0.0.0", port=BOT_PORT, url_path=BOT_TOKEN, webhook_url=BOT_URL + BOT_TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
