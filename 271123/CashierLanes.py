from Lane import Lanes
import json
import random
import time


class CashierLane(Lanes):
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

    def ExtractCashierLanes(self):
        with open("StoringData/CashierLane.json", "r") as f:
            CashierLanes = json.load(f)
        return CashierLanes

    # Base function to show the customers in the self-checkout.
    def SortIntoSelfCheckout(self):
        ordered_data = self.extract_ordered_customers()
        # print(ordered_data)

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

    # Creates the file
    def CreateCashierFile(self):
        result = self.SortIntoSelfCheckout()
        with open("StoringData/Cashier.json", "w") as f:
            f.write(json.dumps(result, indent=2))

    def UpdateCashierFile(self, data):
        with open("StoringData/Cashier.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    def UpdateCashierLaneFile(self,data):
        with open("StoringData/CashierLane.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    def IncrementCashierLane(self, laneNumber):
        CashierLane = self.ExtractCashierLanes()
        CustomersInLane = CashierLane[laneNumber]["CustomersInLane"]
        try:
            CashierLane[laneNumber].update({
                "CustomersInLane": CustomersInLane + 1
            })
            self.UpdateCashierLaneFile(CashierLane)

        except KeyError:
            print("Lane Number was not found")

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
            self.UpdateCashierFile(Customers)
        except KeyError:
            print("Customer ID not found.")

    def FindBestLane(self):
        CashierLanes = self.ExtractCashierLanes()
        Best_Lane = None
        least_customers = float("inf")

        for laneNumber, customers in CashierLanes.items():
            if customers["CustomersInLane"] < least_customers:
                least_customers = customers["CustomersInLane"]
                Best_Lane = laneNumber

        return Best_Lane

    def AddCustomerToLane(self):
        Status = self.CashierLaneFull()
        Customers = self.ExtractCustomerData()
        #Increment the CustomersInLane key by 1.
        for customer, lane in Customers.items():
            if "Cashier Lane Number" not in lane:
                best_lane = self.FindBestLane()
                self.AddLaneNumberToCustomer(customer, best_lane)
                self.IncrementCashierLane(best_lane)


C1 = CashierLane()
C1.AddCustomerToLane()
# C1.AddLaneNumberToCustomer("Customer 2", 3)
# C1.FindBestLane()
# C1.FindBestLane()
# C1.IncrementCashierLane()