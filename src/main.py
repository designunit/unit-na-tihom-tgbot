#!/bin/env python3.10
import telegram
import logging

from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    ConversationHandler,
)

# local imports
import config


LOGGER = logging.getLogger(__name__)


async def start(update, context):
    return None


async def help(update, context):
    await update.send_message("hehe")


async def map_start_conversation(update, context):
    return None


async def map_stop_conversation(update, context):
    return None


async def revert(update, context):
    return None


def main():
    try:
        app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    except Exception as e:
        LOGGER.critical(f"{e}")
        exit(1)

    app.add_handler(CommandHandler("start", help))

    app.add_handler(insert_record_handler)
    app.add_handler(revert_hander)

    app.add_handler(MessageHandler(filters.TEXT, help))

    app.add_error_handler(error)

    # start
    app.run_polling()


if __name__ == "__main__":
    main()
