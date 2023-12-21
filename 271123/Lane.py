import json
import time
from datetime import datetime
import random


# MAX Cashier Lane = 5

class Lanes:
    def __init__(self):
        self.TotalCustomer = 0
        self.LaneStatus = "Open"
        self.CashierLane = {}
        self.SelfCheckout = {}
        self.ordered_dict_items = {}

    # Functions that deal with the creation of lanes:
    def CreateCashierLane(self, LaneNumber):
        self.NewLane = {
            "TimeStamp": self.getTime(),
            "LaneOpen": self.LaneStatus,
            "CustomersInLane": 0,
        }
        self.CashierLane[f"LaneNumber {LaneNumber}"] = self.NewLane
        self.WriteCashierLane()

    def WriteCashierLane(self):
        with open("StoringData/CashierLane.json", "w") as f:
            f.write(json.dumps(self.CashierLane, indent=2))

    def CreateSelfCheckoutLane(self):
        self.SelfCheckout.update({
            f"SelfCheckoutTill {i}": {
                "LaneOpen": "Open",
                "CustomersInSelfCheckoutLane": 0,
            } for i in range(1, 9)
        })
        self.WriteSelfCheckoutLane()

    def WriteSelfCheckoutLane(self):
        with open("StoringData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(self.SelfCheckout, indent=2))

########################################################################################################################

    # Extracts the cashier lanes.
    def ExtractCashierLanes(self):
        with open("StoringData/CashierLane.json", "r") as f:
            data = json.load(f)
        return data

    #Will add up all the customers across all lanes.
    def CashierCustomerTotal(self):
        TotalCustomers = 0
        data = self.ExtractCashierLanes()
        for lane_number, lane_data in data.items():
            TotalCustomers += lane_data["CustomersInLane"]

        return TotalCustomers

    #Will conduct the basic checks on the current lanes.
    def CashierLaneFull(self, LaneNumber=None):
        self.TotalCustomer = 0
        data = self.ExtractCashierLanes()
        Total = self.CashierCustomerTotal()

        if len(data) == 5:  # This will check if the maximum number of lanes has been met.
            if Total == 25:
                return True #Change this to whatever the spec wants.
            else:
                return False

        if LaneNumber is not None:  # Will check if the lane specified is full or not.
            if data[LaneNumber]["CustomersInLane"] == 5:
                print("Full")
                return True
            else:
                print("Not full")
                return False

    #To do today:
    #Create a function that will remove the customer once the process is done in CashierLanes.py
    #Create a function that will output the status of the lanes.

    def ExtractCustomerData(self):
        with open("StoringData/customer_data.json", "r") as f:  # Change this to the new file
            data = json.load(f)
        return data

    def SetCustomerData(self):
        with open("StoringData/OrderedCustomers.json", "w") as f:
            f.write(json.dumps(self.ordered_dict_items, indent=2))

    def SortCustomer(self):
        customer_data = self.ExtractCustomerData()
        self.ordered_dict_items = dict(sorted(customer_data.items(), key=lambda item: item[1]['Basket Size']))
        self.SetCustomerData()
        return self.ordered_dict_items

    def DisplayLaneStatus(self):
        # This will output the lane status.
        pass

    def getTime(self):
        Timestamp = datetime.now()
        hour = Timestamp.hour
        minute = Timestamp.minute
        CurrentTime = f"{hour}:{minute}"
        return CurrentTime


# Create new OrderedCustomers.json file
Checkout1 = Lanes()
# Checkout1.ExtractCustomerData()
# Checkout1.SortCustomer()

# Checkout1.CreateCashierLane(1)
# # Checkout1.CreateSelfCheckoutLane()
Checkout1.CashierLaneFull("LaneNumber 1")
# Checkout1.CashierCustomerTotal()
