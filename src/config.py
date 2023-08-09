import logging
import os
import configparser

from dotenv import load_dotenv


if os.path.isfile(".env"):
    load_dotenv()
else:
    raise Exception("No .env file found")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("/tmp/tg_bot.log"), logging.StreamHandler()],
)

logging.getLogger("httpx").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
if not all([BOT_TOKEN, DB_NAME, COLLECTION_NAME]):
    raise Exception("Not all env variables are present")


def mongo_config(filename="database.ini", section="mongo"):
    parser = configparser.ConfigParser()

    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    # try:
    #     db_config['port'] = int(db_config['port'])
    # except Exception as e:
    #     raise Exception(e)

    return db_config
