from CustomerClass import Customer
import json
import time
from datetime import datetime
import random

# Generate a lane:
# Create a data structure which holds the status "Open" or "Closed"
# Timestamp of when it was created.
# The customers in that line.
# If all lanes are full report lane saturation.
# Self-checkout lane has 8 tills.

# Lanes: {
#   Lane 1: {
#     TimeStampCreated: "xxxx",
#     LaneOpen: True,
#     CustomersInLane: 5,
#    Lane 2: {
#     TimeStampCreated: "xxxx",
#     LaneOpen: False,
#     CustomersInLane: 0,
#   }
# }


class Checkout:
    def __init__(self):
        self.LaneStatus = "Open"
        self.LaneFull = False
        self.TimeStamp = "00:00"
        self.Lane = {}
        self.NewLane = {}
        self.CustomersInLane = 0
        self.LaneMax = 25
        self.MaxLane = 5


    def createLane(self):
        for i in range(5):
            TestVal = random.randint(1,6)
            LaneNumber = i
            self.NewLane = {
                "TimeStamp": self.getTime(),
                "LaneOpen": self.LaneStatus,
                "CustomersInLane": TestVal
            }
            self.Lane[LaneNumber] = self.NewLane
            self.WriteLaneDict()

    def getTime(self):
        Timestamp = datetime.now()
        hour = Timestamp.hour
        minute = Timestamp.minute
        CurrentTime = (f"{hour}:{minute}")
        return CurrentTime


    def WriteLaneDict(self):
        with open("Lanes.txt", "w") as f:
            f.write(json.dumps(self.Lane,indent=2))


Checkout1 = Checkout()
Checkout1.createLane()








