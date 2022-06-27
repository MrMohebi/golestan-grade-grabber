from config import ConfigGGG
from golestanGradeGrabber import GolestanGradeGrabber
from telegramBot import TelegramBotGGG


if __name__ == '__main__':
    configs = ConfigGGG()
    ggg = GolestanGradeGrabber(configs.getLoginURL())
    telBot = TelegramBotGGG(configs.getTelBotToken(), configs.getDB())


    telBot.lessenAll()
    telBot.getTelBot().infinity_polling()