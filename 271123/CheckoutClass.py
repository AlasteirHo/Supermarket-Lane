import json
import time
from datetime import datetime
import random


class Checkout:
    def __init__(self):
        self.LaneStatus = "Open"
        self.Lane = {}
        self.ordered_dict_items = {}


    def CreateCashierLane(self):
    #     for i in range(1,6):
            TestVal = random.randint(1,6)
            # LaneNumber = f"Manned Tills {i}"
            self.NewLane = {
                "TimeStamp": self.getTime(),
                "LaneOpen": self.LaneStatus,
                "CustomersInLane": TestVal
            }
            self.Lane["1"] = self.NewLane
            self.WriteLaneDict()


    def CreateSelfCheckoutLane(self):
        self.Lane.update({
            f"SelfCheckoutTill {i}": {
                "LaneOpen": "Open",
                "CustomersInSelfCheckoutLane": 0,
            } for i in range(1,9)
        })
        self.WriteLaneDict()


    def WriteLaneDict(self):
        with open("StoringData/Lanes.json", "w") as f:
            f.write(json.dumps(self.Lane,indent=2))

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


    def CreateSelfCheckoutFile(self):
        result = self.SortIntoSelfCheckout()[1]
        with open ("StoringData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(result,indent=2))

    def CreateCashierCheckoutFile(self):
        result = self.SortIntoSelfCheckout()[0]
        with open ("StoringData/Cashier.json", "w") as f:
            f.write(json.dumps(result,indent=2))

    def DisplayLaneStatus(self):
        #This will output the lane status.
        pass



#Create new OrderedCustomers.json file
Checkout1 = Checkout()
Checkout1.ExtractCustomerData()
Checkout1.SortCustomer()





