#!/bin/env python3.10
import telegram

from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    ConversationHandler,
)


async def map_start_conversation(context, update):
    return None


async def map_stop_conversation(context, update):
    return None


def main():
    try:
        app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    except Exception as e:
        LOGGER.critical(f"{e}")
        exit(1)

    app.add_handler(CommandHandler("start", help))

    revert_hander = ConversationHandler(
        entry_points=[CommandHandler("revert", revert)],
        states={
            USER_KEYBOARD_INPUT: [
                MessageHandler(
                    filters.Regex("^(Yes|No)$"),
                    confirm_revert
                )
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(insert_record_handler)
    app.add_handler(revert_hander)

    app.add_handler(MessageHandler(filters.TEXT, help))

    app.add_error_handler(error)

    # start
    app.run_polling()


if __name__ == '__main__':
    main()

