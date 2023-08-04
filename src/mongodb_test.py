import pymongo
import urllib.parse


username = urllib.parse.quote_plus('tixiy_bot_user')
password = urllib.parse.quote_plus('sample')


db_client = pymongo.MongoClient('mongodb://%s:%s@localhost:27017/' % (username, password))

current_db = db_client["tixiy_bot_db"]

collection = current_db["test"]


test_doc = {"test": 123321}
ins_result = collection.insert_one(test_doc)