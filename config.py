import os
from dotenv import load_dotenv
import pymongo


class ConfigGGG:
    DB = None
    LoginURL = None
    TelToken = None
    IranProxy = None

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
        self.DB = dbclient[os.getenv("MONGO_DB")]

        self.TelToken = os.getenv("TEL_BOT_TOKEN")
        self.LoginURL = os.getenv("LOGIN_URL")
        self.IranProxy = os.getenv("IRAN_HTTP_PROXY")

    def getDB(self):
        return self.DB

    def getTelBotToken(self):
        return self.TelToken

    def getLoginURL(self):
        return self.LoginURL

    def getGroups(self):
        return list(self.DB['groups'].find({}))

    def getIranProxy(self):
        return self.IranProxy
