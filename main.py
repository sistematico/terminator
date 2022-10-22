#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

from terminator.config import BOT_MODE, BOT_PORT, BOT_URL, BOT_TOKEN
from terminator.decorators import is_group, is_restricted
from terminator.warn import awarn, rwarn, cwarn

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@is_group
@is_restricted
def warn(update: Update, context: CallbackContext) -> None:
    awarn(update, context)


@is_group
def warns(update: Update, context: CallbackContext) -> None:
    cwarn(update, context)


def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("warn", warn))
    dispatcher.add_handler(CommandHandler("warns", warns))
    dispatcher.add_handler(CallbackQueryHandler(rwarn))

    if BOT_MODE.startswith('dev'):
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0", port=BOT_PORT, url_path=BOT_TOKEN, webhook_url=BOT_URL + BOT_TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
