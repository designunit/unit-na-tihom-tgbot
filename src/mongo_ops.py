from pymongo import MongoClient
import logging

from config import mongo_config

LOGGER = logging.getLogger(__name__)


def connect():
    try:
        params = mongo_config()

        conn = MongoClient(**params)
        if conn is not None:
            return conn
        
    except Exception as e:
        LOGGER.critical(e)
        exit(1)

