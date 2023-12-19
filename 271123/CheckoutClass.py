import json
import time
from datetime import datetime
import random

#MAX Cashier Lane = 5

class Checkout:
    def __init__(self):
        self.LaneStatus = "Open"
        self.CashierLane = {}
        self.SelfCheckout = {}
        self.ordered_dict_items = {}

    #Functions that deal with the creation of lanes:
    def CreateCashierLane(self,LaneNumber):
            self.NewLane = {
                "TimeStamp": self.getTime(),
                "LaneOpen": self.LaneStatus,
                "CustomersInLane": 0,
            }
            self.CashierLane[LaneNumber] = self.NewLane
            self.WriteCashierLane()

    def WriteCashierLane(self):
        with open("StoringData/CashierLane.json", "w") as f:
            f.write(json.dumps(self.CashierLane,indent=2))

    def CreateSelfCheckoutLane(self):
        self.SelfCheckout.update({
            f"SelfCheckoutTill {i}": {
                "LaneOpen": "Open",
                "CustomersInSelfCheckoutLane": 0,
            } for i in range(1,9)
        })
        self.WriteSelfCheckoutLane()

    def WriteSelfCheckoutLane(self):
        with open("StoringData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(self.SelfCheckout,indent=2))

#########################################################################################################################

    #Extracts the cashier lanes.
    def ExtractCashierLanes(self):
        with open("StoringData/CashierLane.json", "r") as f:
            data = json.load(f)
        return data

    # if ordered_data[keys]["Basket Size"] >= 10:
    def CheckCashierLane(self):
    #Needs to check if the current lane open/given to the function is full or not.
        data = self.ExtractCashierLanes()
        if len(data) != 5:
            for items in data:
                if data[items]["LaneOpen"] == True and data[items]["CustomerInLane"] == 0: #Complete this

    def ExtractCustomerData(self):
        with open("StoringData/customer_data.json", "r") as f: #Change this to the new file
            data = json.load(f)
        return data

    def SetCustomerData(self):
        with open ("StoringData/OrderedCustomers.json", "w") as f:
            f.write(json.dumps(self.ordered_dict_items,indent=2))

    def SortCustomer(self):
        customer_data = self.ExtractCustomerData()
        self.ordered_dict_items = dict(sorted(customer_data.items(), key=lambda item: item[1]['Basket Size']))
        self.SetCustomerData()
        return self.ordered_dict_items


    def DisplayLaneStatus(self):
        #This will output the lane status.
        pass

    def getTime(self):
        Timestamp = datetime.now()
        hour = Timestamp.hour
        minute = Timestamp.minute
        CurrentTime = f"{hour}:{minute}"
        return CurrentTime

#Create new OrderedCustomers.json file
Checkout1 = Checkout()
# Checkout1.ExtractCustomerData()
# Checkout1.SortCustomer()

Checkout1.CreateCashierLane(1)
Checkout1.CreateSelfCheckoutLane()
Checkout1.CheckCashierLane()







