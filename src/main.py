#!/bin/env python3.10
import logging

from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
)

from telegram import ReplyKeyboardMarkup, KeyboardButton

# local imports
import config
import mongo_ops


LOGGER = logging.getLogger(__name__)

IMPORTANT_INFO_TEXT = "Важная инфомрация!"
CAMP_RULES_TEXT = "Правила лагеря!"


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
    photo_map_jpg = mongo_ops.get_file_by_name('map.jpg')
    photo_map_pdf = mongo_ops.get_file_by_name('map.pdf')
    
    if not all([photo_map_jpg, photo_map_pdf]):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Не могу загрузить карту.")

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_map_jpg)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=photo_map_pdf, filename='camp map.pdf')


async def get_current_events(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you current events")


async def get_programm(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you your programm")


async def get_music(update, context):
    photo_music_jpg = mongo_ops.get_file_by_name('music.jpg')
    photo_music_pdf = mongo_ops.get_file_by_name('music.pdf')
    
    if not all([photo_music_jpg, photo_music_pdf]):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Не могу загрузить музыку.")

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_music_jpg)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=photo_music_pdf, filename='music.pdf')


async def get_camp_rules(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=CAMP_RULES_TEXT)


async def get_landscape_objects(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="sent you your landscape objects")


async def get_important_info(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=IMPORTANT_INFO_TEXT)


async def get_transer_info(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="transer!")


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
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^трансфер$"), get_transer_info))

    # start
    app.run_polling()


if __name__ == "__main__":
    main()
