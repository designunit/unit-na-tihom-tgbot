import logging
import os

from dotenv import load_dotenv
from configparser import ConfigParser


if os.path.isfile(".env"):
    load_dotenv()
else:
    raise Exception("No .env file found")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("/tmp/tg_bot.log"), logging.StreamHandler()],
)

LOGGER = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not found in .env file")


def mongo_config(filename='database.ini', section='mongo'):
    parser = ConfigParser()

    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")
    
    return db_config
