import logging
import os

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

LOGGER = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not found in .env file")
