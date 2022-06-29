from config import ConfigGGG
from golestan import Golestan
from telegramBot import TelegramBotGGG


class GolestanGradeGrabber:
    DB = None
    Configs = None
    TelBot = None

    def __init__(self):
        self.Configs = ConfigGGG()
        self.DB = self.Configs.getDB()
        self.TelBot = TelegramBotGGG(self.Configs.getTelBotToken(), self.DB)
        self.TelBot.lessenAll()

    def compereScores(self, previousScores, newScores, username):
        freshScores = []
        for eNewLessen in newScores:
            newFlag = True
            for ePL in previousScores:
                if eNewLessen["name"] == ePL["name"] and eNewLessen["score"] == ePL["score"]:
                    newFlag = False
            if newFlag:
                eNewLessen['username'] = username
                freshScores.append(eNewLessen)

        self.saveFreshScoresToDB(freshScores, username)

        return freshScores

    def saveFreshScoresToDB(self, freshScores, username):
        for eNewScore in freshScores:
            self.DB["lessens"].update_one(
                {"name": eNewScore["name"], "username": username},
                {"$set": eNewScore},
                upsert=True
            )

    def checkScores(self):
        for eGroup in self.Configs.getGroups():
            users = eGroup['users']
            for eUser in users:
                try:
                    ggg = Golestan(self.Configs.getLoginURL(), eUser['username'], eUser['password'], True, self.Configs.getIranProxy())
                    scores = ggg.getUserScores()
                    previousUserLessens = list(self.Configs.getDB()["lessens"].find({"username": eUser['username']}))
                    diffs = self.compereScores(previousUserLessens, scores, eUser['username'])
                    if len(diffs) > 0:
                        self.TelBot.sendNewScores(eGroup["chatId"], diffs)
                except:
                    pass
