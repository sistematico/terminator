#!/usr/bin/env python
# pylint: disable=C0116,W0613

import os
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

try:
    from credentials import bot_token, bot_url
except ModuleNotFoundError:
    bot_token = os.environ.get('BOT_TOKEN')
    bot_url = os.environ.get('WEBHOOK_URL', 'https://terminator.fly.dev')

bot_port = int(os.environ.get('PORT', '8443'))
bot_mode = os.environ.get('ENV', 'production')

# Enable logging
# CRITICAL ERROR WARNING INFO DEBUG NOTSET
loglevel = 'logging.WARNING' if bot_mode == 'production' else 'logging.DEBUG'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(fr'Olá {user.mention_markdown_v2()}\!', reply_markup=ForceReply(selective=True),)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def main() -> None:
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

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
