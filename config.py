import os
from dotenv import load_dotenv
import pymongo


class ConfigGGG:
    db = None

    def __init__(self):
        load_dotenv()
        dbclient = pymongo.MongoClient(
            "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(
                os.getenv("MONGO_USERNAME"),
                os.getenv("MONGO_PASSWORD"),
                os.getenv("MONGO_URL"),
                os.getenv("MONGO_PORT"),
                os.getenv("MONGO_DB"),
            )
        )
        self.db = dbclient[os.getenv("MONGO_DB")]

    def getDB(self):
        return self.db
