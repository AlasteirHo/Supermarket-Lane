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
        with open("StoringData/CashierData/CashierLane.json", "w") as f:
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
        with open("StoringData/SelfCheckoutData/SelfCheckoutLane.json", "w") as f:
            f.write(json.dumps(self.SelfCheckout, indent=2))


    # Extracts the cashier lanes.
    @staticmethod
    def ExtractCashierLanes():
        with open("StoringData/CashierData/CashierLane.json", "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def extract_ordered_customers():
        with open("StoringData/OrderedCustomers.json", "r") as f:
            data = json.load(f)
        return data

    def ExtractSelfCheckOutData(self): #Extracts the current customers in the Cashier.json file.
        with open("StoringData/CashierData/Cashier.json", "r") as f:
            CustomersInCashier = json.load(f)
        return CustomersInCashier

    #Will add up all the customers across all lanes.
    def CashierCustomerTotal(self):
        TotalCustomers = 0
        data = self.ExtractCashierLanes()
        for lane_number, lane_data in data.items():
            TotalCustomers += lane_data["CustomersInLane"]
        if TotalCustomers == 25:
            return "Lane Saturation"
        else:
            return TotalCustomers

    def SelfCheckoutCustomerTotal(self):
        TotalCustomers = 0
        data = self.ExtractSelfCheckOutData()
        for lane_number, lane_data in data.items():
            TotalCustomers += lane_data["CustomersInSelfCheckoutLane"]
        if TotalCustomers == 15:
            return "Lane Saturation"
        else:
            return TotalCustomers

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

    def getTime(self):
        Timestamp = datetime.now()
        hour = Timestamp.hour
        minute = Timestamp.minute
        CurrentTime = f"{hour}:{minute}"
        return CurrentTime


# Create new OrderedCustomers.json file
Checkout1 = Lanes()
# Checkout1.ExtractCustomerData()
Checkout1.SortCustomer()

# Checkout1.CreateCashierLane(1)
# # Checkout1.CreateSelfCheckoutLane()
# Checkout1.CashierLaneFull("LaneNumber 1")
# Checkout1.CashierCustomerTotal()
