#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from terminator.config import BOT_MODE, BOT_PORT, BOT_URL, BOT_TOKEN
from terminator.decorators import restricted
from terminator.warn import awarn, rwarn, cwarn
from terminator.admin import flush, drop

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 👍

@restricted
def admin(update: Update, context: CallbackContext) -> None:
    if "flush" in update.message.text:
        flush(update, context)

    if "drop" in update.message.text:
        drop(update, context)

@restricted
def warn(update: Update, context: CallbackContext) -> None:
    awarn(update, context)

def warns(update: Update, context: CallbackContext) -> None:
    cwarn(update, context)

def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("warn", warn))
    dispatcher.add_handler(CommandHandler("warns", warns))
    dispatcher.add_handler(CallbackQueryHandler(rwarn))
    dispatcher.add_handler(MessageHandler(Filters.text, admin))

    if BOT_MODE.startswith('dev'):
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0", port=BOT_PORT, url_path=BOT_TOKEN, webhook_url=BOT_URL + BOT_TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
