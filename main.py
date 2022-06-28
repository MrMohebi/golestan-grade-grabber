from setInterval import SetInterval
from GolestanGradeGrabber import GolestanGradeGrabber


if __name__ == '__main__':
    ggg = GolestanGradeGrabber()
    print("started...")
    inter = SetInterval(3600, ggg.checkScores)

