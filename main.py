from setInterval import SetInterval
from GolestanGradeGrabber import GolestanGradeGrabber


if __name__ == '__main__':
    ggg = GolestanGradeGrabber()

    inter = SetInterval(20, ggg.checkScores)

