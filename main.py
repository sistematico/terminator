#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from terminator.config import BOT_MODE, BOT_PORT, BOT_URL, BOT_TOKEN
from terminator.decorators import restricted, get_me, group, not_group
from terminator.warn import awarn, rwarn, cwarn
from terminator.admin import flush, drop, install

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 👍

@group
@restricted
def admin(update: Update, context: CallbackContext) -> None:
    if "getme" in update.message.text:
        print(context.bot.get_me().id)

    if "install" in update.message.text:
        install(update, context)

    if "flush" in update.message.text:
        flush(update, context)

    if "drop" in update.message.text:
        drop(update, context)

@get_me
@group
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
