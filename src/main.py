#!/bin/env python3.10
import logging
import datetime

from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# local imports
import config
import mongo_ops


LOGGER = logging.getLogger(__name__)


IMPORTANT_INFO_TEXT = "Важная инфомрация!"
CAMP_RULES_TEXT = "Правила лагеря!"

LANDSCAPE_OBJECTS_DICT = {
    'text_camp': 'лагерь',
    'text_grosery': "гастрономия",
    'text_main_stage': 'main stage',
    'text_amphitheater': 'амфитеатр',
    'text_backstage': 'закулисье',
    }

PROGRAM_LOCATION_DICT = {
    'program_main_stage': 'main stage',
    'program_amphitheater': 'амфитеатр',
    'program_backstage': 'закулисье'
    }


MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="карта"), KeyboardButton(text="что происходит")],
        [KeyboardButton(text="программа"), KeyboardButton(text="музыка")],
        [
            KeyboardButton(text="правила лагеря"),
            KeyboardButton(text="ландшафтные объекты"),
        ],
        [KeyboardButton(text="важное"), KeyboardButton(text="трансфер")],
    ],
    resize_keyboard=True,
    is_persistent=True,
    one_time_keyboard=False,
)

PROGRAM_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("main stage", callback_data="program_main_stage")],
        [InlineKeyboardButton("амфитеатр", callback_data="program_amphitheater")],
        [InlineKeyboardButton("закулисье", callback_data="program_backstage")],
    ])

LANDSCAPE_KEYBOARD = InlineKeyboardMarkup([
        [InlineKeyboardButton("лагерь", callback_data="text_camp")],
        [InlineKeyboardButton("гастрономия", callback_data="text_grosery")],
        [InlineKeyboardButton("main stage", callback_data="text_main_stage")],
        [InlineKeyboardButton("амфитеатр", callback_data="text_amphitheater")],
        [InlineKeyboardButton("закулисье", callback_data="text_backstage")],
    ])


async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="choose an option",
        reply_markup=MAIN_KEYBOARD,
    )


async def get_map(update, context):
    photo_map_jpg = mongo_ops.get_file_by_name("map.jpg")
    photo_map_pdf = mongo_ops.get_file_by_name("map.pdf")

    if not all([photo_map_jpg, photo_map_pdf]):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Не могу загрузить карту."
        )

    if photo_map_jpg is not None:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo_map_jpg
        )

    if photo_map_pdf is not None:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=photo_map_pdf,
            filename="camp map.pdf",
        )


async def get_current_events(update, context):
    user_time = datetime.datetime.now()
    current_events = mongo_ops.get_events_by_user_time(user_time)
    if current_events is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="не могу загрузить текущие события."
        )
        return

    if len(current_events) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Сейчас ничего не происходит: your time: {user_time}",
        )

    for event in current_events:
        event_name = event.get("name")
        if event_name is not None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"{event['name']}"
            )


async def get_programm(update, context):
    photo_program_jpg = mongo_ops.get_file_by_name("program.jpg")
    photo_program_pdf = mongo_ops.get_file_by_name("program.pdf")

    if not all([photo_program_pdf, photo_program_jpg]):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="не могу прислать программу."
        )
    if photo_program_jpg is not None:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo_program_jpg
        )

    if photo_program_pdf is not None:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=photo_program_pdf,
            filename="program.pdf",
        )
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Подробная информация по каждой площадке:",
        reply_markup=PROGRAM_KEYBOARD
    )


async def get_music(update, context):
    photo_music_jpg = mongo_ops.get_file_by_name("music.jpg")
    photo_music_pdf = mongo_ops.get_file_by_name("music.pdf")

    if not all([photo_music_jpg, photo_music_pdf]):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Не могу загрузить музыку."
        )

    if photo_music_jpg is not None:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo_music_jpg
        )

    if photo_music_pdf is not None:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=photo_music_pdf,
            filename="music.pdf",
        )


async def get_camp_rules(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=CAMP_RULES_TEXT
    )


async def get_landscape_objects(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="sent you your landscape objects",
        reply_markup=LANDSCAPE_KEYBOARD,
    )


async def inline_button(update, context):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data in LANDSCAPE_OBJECTS_DICT:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"landscape {data}")
    
    elif data in PROGRAM_LOCATION_DICT:
        events = mongo_ops.get_events_by_location(PROGRAM_LOCATION_DICT.get(data))
        if events is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'не могу загрузить программу для: {data}')
            return

        for event in events:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{event.get("name")}')

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"other {data}")


async def get_important_info(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=IMPORTANT_INFO_TEXT
    )


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
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^что происходит$"), get_current_events
        )
    )
    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^программа$"), get_programm)
    )
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^музыка$"), get_music))
    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^правила лагеря$"), get_camp_rules)
    )
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^ландшафтные объекты$"), get_landscape_objects
        )
    )
    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^важное$"), get_important_info)
    )
    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^трансфер$"), get_transer_info)
    )

    app.add_handler(CallbackQueryHandler(inline_button))

    # start
    app.run_polling()


if __name__ == "__main__":
    main()
