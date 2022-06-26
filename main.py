from config import ConfigGGG
from golestanGradeGrabber import GolestanGradeGrabber

if __name__ == '__main__':
    configs = ConfigGGG()
    ggg = GolestanGradeGrabber(configs.getLoginURL())

