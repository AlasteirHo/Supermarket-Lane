from CheckoutClass import Checkout
import json
import random
import time


# A random number between 1 and 10 customers need to join the Cashier lane at the beginning of the simulation. (This can be done in the simulation class)
# self.LaneMax = 25
# for self-service theres 1 lane of 8 tills = 7 people can be queuing at one time if all 8 tills are open and has customers
#  made -> Lane1 -> Is Lane1 Full? -> Open new lane ELSE Put customer in Lane1 -> Process Customer -> Output lane status? -> Remove Customer from lane
class Lane(Checkout):
    def __init__(self):
        self.CashierCheckoutCustomers = {}
        self.laneNumber = 1
        self.ServiceLane = 1  # This can hold 8 different lanes
        self.Queue = []
        super().__init__()

    def extract_ordered_customers(self):
        with open("StoringData/OrderedCustomers.json", "r") as f:
            data = json.load(f)
        return data

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
    def CreateSelfCheckoutFile(self):
        result = self.SortIntoSelfCheckout()
        with open("StoringData/Cashier.json", "w") as f:
            f.write(json.dumps(result, indent=2))

    def ExtractCustomerData(self):
        with open("StoringData/Cashier.json", "r") as f:
            CustomersInLane = json.load(f)
        return CustomersInLane

    def ProcessItems(self):
        Customers_In_Cashier = self.ExtractCustomerData()
        for keys in Customers_In_Cashier:
            delays = (Customers_In_Cashier[keys]["Process Time"])
            time.sleep(delays)
            print(f"Customer {Customers_In_Cashier[keys]["CustomerID"]} time has been completed.")


    def RemoveCustomer(self):
        # This function will be called by ProcessItems at the end once the customer has finished.
        pass

    def LaneStatus(self):
        # Will check if the lane needs to be opened or closed.
        pass

    def OpenNewLane(self):
        # Will open a new lane if LaneStatus returns Open.
        pass

    def CloseLane(self):
        # Will close the lane if LaneStatus returns Close.
        pass


b = Lane()
b.SortIntoSelfCheckout()
b.CreateSelfCheckoutFile()
b.ProcessItems()