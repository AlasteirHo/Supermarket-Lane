from Lane import Lanes
import json
import random
import time


class CashierLanes(Lanes):
    def __init__(self):
        self.CashierCheckoutCustomers = {}
        self.laneNumber = 1
        self.ServiceLane = 1
        self.Queue = []
        super().__init__()

    def extract_ordered_customers(self):
        with open("StoringData/OrderedCustomers.json", "r") as f:
            data = json.load(f)
        return data

    def ExtractCustomerData(self):
        with open("StoringData/Cashier.json", "r") as f:
            CustomersInCashier = json.load(f)
        return CustomersInCashier

    def SortIntoCashierLanes(self):
        ordered_data = self.extract_ordered_customers()

        for keys in ordered_data:
            if ordered_data[keys]["Basket Size"] >= 10:
                self.CashierCheckoutCustomers.update({
                    keys: {
                        "CustomerID": ordered_data[keys]["CustomerID"],
                        "Items In Basket": ordered_data[keys]["Basket Size"],
                        "Lane Type": "Cashier",
                        "Process Time": ordered_data[keys]["Time at Cashier"]
                    }
                })
        return self.CashierCheckoutCustomers


    def AddNewCashierLanes(self, NewLaneNumber):
        NewLaneDetails = {
            "TimeStamp": self.getTime(),
            "LaneOpen": self.LaneStatus,
            "CustomersInLane": 0,
        }
        NewLane = f"LaneNumber {NewLaneNumber}"
        self.CashierLane[NewLane] = NewLaneDetails
        self.UpdateCashierFile(self.CashierLane)

    # Creates the file
    def CreateCashierFile(self):
        result = self.SortIntoCashierLanes()
        with open("StoringData/Cashier.json", "w") as f:
            f.write(json.dumps(result, indent=2))

    def UpdateCashierFile(self,data):
        current_content = self.ExtractCashierLanes()
        current_content.update(data)

        with open("StoringData/CashierLane.json", "w") as f:
            f.write(json.dumps(current_content, indent=2))


    @staticmethod
    def WriteCashierFile(data):
        with open("StoringData/Cashier.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    # Updates the Cashier Lane file
    @staticmethod
    def WriteCashierLaneFile(data):
        with open("StoringData/CashierLane.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    # Increments the cashier customerinlane key by 1
    def IncrementCashierLane(self, laneNumber):
        data = self.ExtractCashierLanes()
        CustomersInLane = data[laneNumber]["CustomersInLane"]
        try:
            data[laneNumber].update({
                "CustomersInLane": CustomersInLane + 1
            })
            self.WriteCashierLaneFile(data)

        except KeyError:
            print("Lane Number was not found")

    def OpenNewLane(self):
        # Open a new lane if the current lane open has 5 customersinlane.
        data = self.ExtractCashierLanes()

        for LaneNumber, Customers in data.items():
            if Customers["CustomersInLane"] == 5:
                NewLaneNumber = int(LaneNumber.split(" ")[1]) + 1
                print(NewLaneNumber)
                self.AddNewCashierLanes(NewLaneNumber)
            else:
                print("No need to open new lane.")

    def ProcessItems(self):
        Customers_In_Cashier = self.ExtractCustomerData()
        for keys in Customers_In_Cashier:
            delays = (Customers_In_Cashier[keys]["Process Time"]) #Calculated using the formula given.
            time.sleep(delays)
            print(f"Customer {Customers_In_Cashier[keys]["CustomerID"]} time has been completed.")

    def AddLaneNumberToCustomer(self, CustomerID, LaneNumber):
        Customers = self.ExtractCustomerData()
        try:
            LaneNumber = int(LaneNumber.split()[-1])
            Customers[CustomerID].update({
                "Cashier Lane Number": LaneNumber
            })
            self.WriteCashierFile(Customers)
        except KeyError:
            print("Customer ID not found.")

    def FindBestLane(self):
        data = self.ExtractCashierLanes()
        Best_Lane = None
        least_customers = float("inf")

        for laneNumber, customers in data.items():
            if customers["CustomersInLane"] < least_customers:
                least_customers = customers["CustomersInLane"]
                Best_Lane = laneNumber

        return Best_Lane

    def AddCustomerToLane(self):
        Status = self.CashierLaneFull()
        Customers = self.ExtractCustomerData()

        for customer, lane in Customers.items():
            if "Cashier Lane Number" not in lane:
                self.OpenNewLane()
                best_lane = self.FindBestLane()
                self.AddLaneNumberToCustomer(customer, best_lane)
                self.IncrementCashierLane(best_lane)


C1 = CashierLanes()
# C1.AddCustomerToLane()
# C1.AddLaneNumberToCustomer("Customer 2", 3)
# C1.FindBestLane()
C1.AddCustomerToLane()
# C1.IncrementCashierLane()