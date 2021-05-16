



import time


class cTimeBand:

    def __init__(self):
        self.mTimeList = []


    def addTimePoint(self):
        self.mTimeList.append(time.process_time())
        return self

    def getTimeBand(self):
        return self.mTimeList