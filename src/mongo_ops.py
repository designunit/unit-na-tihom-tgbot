from pymongo import MongoClient
import logging
import gridfs

from config import mongo_config


LOGGER = logging.getLogger(__name__)
DB_NAME = "tixiy_bot_db"
COLLECTION_NAME = "events"


def connect():
    try:
        params = mongo_config()

        conn = MongoClient(**params)
        if conn is not None:
            return conn

    except Exception as e:
        LOGGER.critical(e)
        exit(1)


def insert_event(event):
    try:
        conn = connect()
        collection = conn[DB_NAME][COLLECTION_NAME]
        event_id = collection.insert_one(event).inserted_id
        if event_id is not None:
            return True

        return False

    except Exception as e:
        LOGGER.error(f"Error occured when you tried to insert new event: {e}")
        return False


def get_events_by_user_time(user_time):
    # user time must be datetime object
    try:
        conn = connect()
        collection = conn[DB_NAME][COLLECTION_NAME]
        events = collection.find(
            {"time_start": {"$lte": user_time}, "time_end": {"$gte": user_time}}
        )
        if events is None:
            return None
        
        return [event for event in events]

    except Exception as e:
        LOGGER.error(f"Error occured when you tried to get events by user time: {e}")
        return None


def get_file_by_name(filename):
    try:
        conn = connect()
        db = conn[DB_NAME]
        fs = gridfs.GridFS(db)
        data = db.fs.files.find_one({"filename": filename})
        if data is None:
            return None

        id = data.get("_id")
        if id is None:
            return None

        return fs.get(id).read()

    except Exception as e:
        LOGGER.error(f"Error occured when you tried to get {filename} file: {e}")
        return None


def get_events_by_location(location):
    try:
        conn = connect()
        collection = conn[DB_NAME][COLLECTION_NAME]
        events = collection.find({"location": location})

        if events is None:
            return None
        
        return [event for event in events]

    except Exception as e:
        LOGGER.error(f"Error occured when you trid to get event by {location} place: {e}")
        return None
