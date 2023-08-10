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

ADMIN_IDS = [136858809, 777855967]
IMPORTANT_INFO_TEXT = ["Объявления еще нет!"]
CAMP_RULES_TEXT = """
Дорогой гость! Наша резиденция располагается на невероятно красивой частной территории. Наша главная цель - отдохнуть и при этом не причинить вреда лесу, себе и друг другу 🫶

Вот несколько важных пунктов:
 1. В целях нашей общей безопасности не разводить костров, даже в мангалах! 
 2. Помнить, что на площадке есть дети!
 3. Соблюдать правила раздельного сбора мусора действующие на территории всей резиденции. Вас с радостью проконсультируют наши волонтеры.
 4. Если что-то случилось или у вас появились вопросы - обращаться к любому сотруднику инфоцентра, расположенного напротив фудкорта.
 5. Медпункт всегда вам поможет! не паниковать и при необходимости общаться к ним.
 6. Уважать друг друга, заботиться об окружающих людях и пространстве ❤️
"""

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

TRANSFER_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("туда", callback_data="forward_trip_jpg"), InlineKeyboardButton("обратно", callback_data="back_trip_jpg")]
])


async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="choose an option",
        reply_markup=MAIN_KEYBOARD,
    )


async def get_map(update, context):
    photo_data_jpg = mongo_ops.get_file_by_name("map_jpg")
    photo_data_pdf = mongo_ops.get_file_by_name("map_pdf")

    if not all([photo_data_jpg, photo_data_pdf]):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Не могу загрузить карту."
        )

    if photo_data_jpg is not None:
        photo_map = photo_data_jpg[1]
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo_map
        )

    if photo_data_pdf is not None:
        file_name, photo_map = photo_data_pdf
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=photo_map,
            filename=file_name,
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
        return

    buttons = []
    for event in current_events:
        event_name = event.get("name")
        if event_name is not None:
            buttons.append([InlineKeyboardButton(text=event_name, callback_data=event_name)])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Сейчас происходит:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def get_programm(update, context):
    photo_data_jpg = mongo_ops.get_file_by_name("program_jpg")
    photo_data_pdf = mongo_ops.get_file_by_name("program_pdf")

    if not all([photo_data_pdf, photo_data_jpg]):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="не могу прислать программу."
        )

    if photo_data_jpg is not None:
        photo_program = photo_data_jpg[1]
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo_program
        )

    if photo_data_pdf is not None:
        file_name, photo_program = photo_data_pdf
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=photo_program,
            filename=file_name,
        )
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Подробная информация по каждой площадке:",
        reply_markup=PROGRAM_KEYBOARD
    )


async def get_music(update, context):
    photo_data_jpg = mongo_ops.get_file_by_name("music_jpg")
    photo_data_pdf = mongo_ops.get_file_by_name("music_pdf")

    if not all([photo_data_jpg, photo_data_pdf]):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Не могу загрузить музыку."
        )

    if photo_data_jpg is not None:
        photo_jpg = photo_data_jpg[1]
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo_jpg
        )

    if photo_data_pdf is not None:
        file_name, photo_music = photo_data_pdf
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=photo_music,
            filename=file_name,
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


async def get_important_info(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=IMPORTANT_INFO_TEXT[-1]
    )


async def get_transer_info(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="трансфер:",
        reply_markup=TRANSFER_KEYBOARD
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
        buttons = []
        for event in events:
            event_name = event.get("name")
            event_id = event.get("_id")

            if event_name is not None:
                buttons.append([InlineKeyboardButton(text=f'{event_name}', callback_data=str(event_id) + 'Bot_program_event!')])
        
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Программа для: {data}",
                                       reply_markup=InlineKeyboardMarkup(buttons)
                                        )
            
        # for event in events:
        #     name = event.get("name")
        #     lectors = event.get("speakers")
        #     description = event.get("description")
        #     time_start = event.get("start_time")
        #     time_end = event.get("end_time")

        #     print([name, lectors, time_start, time_end, description])
        #     if all([name, lectors, time_start, time_end, description]):
        #         output_text = f'Название: {name}\nЛектор: {lectors}\nОписание: {description}\nВремя: {time_start} - {time_end}'
        #         await context.bot.send_message(chat_id=update.effective_chat.id, text=output_text)

    elif 'Bot_program_event' in data:
        query = update.callback_query
        data = query.data
        await query.answer()


        await context.bot.send_message(chat_id=update.effective_chat.id, text=data) 

    else:
        file_data = mongo_ops.get_file_by_name(data.lower())
        if file_data is not None:
            file_name, presentation = file_data
            await context.bot.send_document(chat_id=update.effective_chat.id,
                                            document=presentation,
                                            filename=file_name,
        )


async def announcement(update, context):
    if not update.effective_chat.id in ADMIN_IDS:
        return 

    admin_announcement = update.message.text

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Сообщение: '{admin_announcement}' было добавлено в объявления")
    IMPORTANT_INFO_TEXT.append(admin_announcement)


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

    app.add_handler(MessageHandler(filters.TEXT, announcement))

    # start
    app.run_polling()


if __name__ == "__main__":
    main()
