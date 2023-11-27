from CustomerClass import Customer
import json
import time
from datetime import datetime
import random


class Checkout:
    def __init__(self):
        self.LaneStatus = "Open"
        self.LaneFull = False
        self.TimeStamp = "00:00"
        self.Lane = {}
        self.NewLane = {}
        self.NewSelfLane = {}
        self.data = {}
        self.CheckoutCustomers = {}
        self.SelfCheckoutCustomers = {}
        self.CashierCheckoutCustomers = {}
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

    def getTime(self):
        Timestamp = datetime.now()
        hour = Timestamp.hour
        minute = Timestamp.minute
        CurrentTime = (f"{hour}:{minute}")
        return CurrentTime

    def WriteLaneDict(self):
        with open("StoringData/Lanes.json", "w") as f:
            f.write(json.dumps(self.Lane,indent=2))

    def ExtractCustomerData(self):
        with open("StoringData/Customers.json") as f:
            data = json.load(f)
        return data

    def SetCustomerData(self):
        with open ("StoringData/OrderedCustomers.json", "w") as f:
            f.write(json.dumps(self.ordered_dict_items,indent=2))

    def SortCustomer(self):
        customer_data = self.ExtractCustomerData()
        self.ordered_dict_items = dict(sorted(customer_data.items(), key=lambda item: item[1]['Items']))
        self.SetCustomerData()
        return self.ordered_dict_items


    def SortIntoSelfCheckout(self):
        ordered_data = self.SortCustomer()
        print(ordered_data)

        for keys in ordered_data:
            if ordered_data[keys]["Items"] >= 10:
                # print(f"{keys}: {ordered_data[keys]['Items']}")
                self.CashierCheckoutCustomers.update({
                    keys: {
                        "Item In Basket": ordered_data[keys]["Items"],
                        "Lane Type": "Cashier"
                    }
                })

            else:
                # print(f"{keys}: {ordered_data[keys]['Items']}")
                self.SelfCheckoutCustomers.update({
                    keys: {
                        "Item In Basket": ordered_data[keys]["Items"],
                        "Lane Type": "Self Checkout"
                    }
                })

        return self.CashierCheckoutCustomers, self.SelfCheckoutCustomers

    def CreateSelfCheckoutFile(self):
        result = self.SortIntoSelfCheckout()[1]
        with open ("StoringData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(result,indent=2))

    def CreateCashierCheckoutFile(self):
        result = self.SortIntoSelfCheckout()[0]
        with open ("StoringData/Cashier.json", "w") as f:
            f.write(json.dumps(result,indent=2))





# Checkout1 = Checkout()
# Checkout1.CreateCashierLane()
# Checkout1.CreateSelfCheckoutLane()
# # Checkout1.SortIntoSelfCheckout()
# Checkout1.CreateSelfCheckoutFile()
# Checkout1.CreateCashierCheckoutFile()

# Customer1 = Customer()
# Customer1.createCustomerDict()
# Checkout1.SortCustomer()
# Checkout1.SortIntoSelfCheckout()
# Checkout1.CreateSelfCheckoutFile()
# Checkout1.CreateCashierCheckoutFile()







