from config import ConfigGGG
from golestanGradeGrabber import GolestanGradeGrabber

if __name__ == '__main__':
    configs = ConfigGGG()

    for eGroup in configs.getGroups():
        users = eGroup['users']
        for eUser in users:
            try:
                ggg = GolestanGradeGrabber(configs.getLoginURL(), eUser['username'], eUser['password'])
                scores = ggg.getUserScores()
                previousUserLessens = list(configs.getDB()["lessens"].find({"username": eUser['username']}))
                newScores = []
                for eNewLessen in scores:
                    newFlag = True
                    for ePL in previousUserLessens:
                        if eNewLessen["name"] == ePL["name"] and eNewLessen["score"] == ePL["score"]:
                            newFlag = False
                    if newFlag:
                        eNewLessen['username'] = eUser['username']
                        newScores.append(eNewLessen)

                for eNewScore in newScores:
                    configs.getDB()["lessens"].update_one(
                        {"name": eNewScore["name"], "username": eUser['username']},
                        {"$set": eNewScore},
                        upsert=True
                    )
                print(newScores)

            except:pass

