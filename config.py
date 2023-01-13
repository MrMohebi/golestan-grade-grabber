import os
from dotenv import load_dotenv
import pymongo
from sshProxy import SSHProxyController


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

        sshPFUrl = os.getenv("IRAN_SSH_TUNNELING_URL")
        if sshPFUrl is not None and len(sshPFUrl) > 0:
            sshPFUsername = os.getenv("IRAN_SSH_TUNNELING_USERNAME")
            sshPFPassword = os.getenv("IRAN_SSH_TUNNELING_PASSWORD")
            sshPFPort = os.getenv("IRAN_SSH_TUNNELING_PORT")
            controlssh = SSHProxyController(sshPFUrl, sshPFUsername, sshPFPassword, 1080, sshPFPort)
            controlssh.start()
            self.IranProxy = "socks5://127.0.0.1:1080"

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
