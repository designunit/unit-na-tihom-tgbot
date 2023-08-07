#!/bin/env python3.10
import telegram
import logging

from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from telegram import ForceReply, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

# local imports
import config


LOGGER = logging.getLogger(__name__)


COMMAND_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
         [KeyboardButton(text='карта'),KeyboardButton(text='что происходит')],
         [KeyboardButton(text='программа'), KeyboardButton(text='музыка')],
         [KeyboardButton(text='правила лагеря'),KeyboardButton(text='ландшафтные объекты')],
         [KeyboardButton(text='важное'), KeyboardButton(text='трансфер')]
         ],
    resize_keyboard=True,
    is_persistent=True,
)


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="choose an option", reply_markup=COMMAND_KEYBOARD)


async def get_map(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you your map!")


async def get_current_events(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you current events")


async def get_programm(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you your programm")


async def get_music(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you your music")


async def get_camp_rules(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you the camp rules")


async def get_landscape_objects(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you thr")


async def get_important_info(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="important info!")


async def get_transer_info(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="transer!")


async def help_command(update, context):
    await update.message.reply_text("Help!")


def main():
    try:
        app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    except Exception as e:
        LOGGER.critical(f"{e}")
        exit(1)

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^карта$"), get_map))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^что происходит$"), get_current_events))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^программа$"), get_programm))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^музыка$"), get_music))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^правила лагеря$"), get_camp_rules))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^ландшафтные объекты$"), get_landscape_objects))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^важное$"), get_important_info))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^трансфер"), get_transer_info))

    # start
    app.run_polling()


if __name__ == "__main__":
    main()
