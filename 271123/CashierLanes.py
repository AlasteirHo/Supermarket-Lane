from CheckoutClass import Checkout
import json
import random

#A random number between 1 and 10 customers need to join the Cashier lane at the beginning of the simulation. (This can be done in the simulation class)
#self.LaneMax = 25
#for self service theres 1 lane of 8 tills = 7 people can be queuing at one time if all 8 tills are open and has customers
# Customers made -> Lane1 -> Is Lane1 Full? -> Open new lane ELSE Put customer in Lane1 -> Process Customer -> Output lane status? -> Remove Customer from lane
class Lane(Checkout):
    def __init__(self):
        self.laneNumber = 1
        self.ServiceLane = 1 #This can hold 8 different lanes
        self.Queue = []
        super().__init__()

    def extract_ordered_customers(self):
        with open("StoringData/OrderedCustomers.json", "r") as f:
            data = json.load(f)
        return data

    #Base function to show the customers in the selfcheckout.
    def SortIntoSelfCheckout(self):
        ordered_data = self.extract_ordered_customers()
        print(ordered_data)

        for keys in ordered_data:
            if ordered_data[keys]["Items"] >= 10:
                self.CashierCheckoutCustomers.update({
                    keys: {
                        "Items In Basket": ordered_data[keys]["Items"],
                        "Lane Type": "Cashier"
                    }
                })
        return self.CashierCheckoutCustomers

    #Creates the file
    def CreateSelfCheckoutFile(self):
        result = self.SortIntoSelfCheckout()
        with open("StoringData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(result,indent=2))

    def ProcessItems(self):
        #Using time, delay the operation by however long the processtime is.

    def RemoveCustomer(self):
        #This function will be called by ProcessItems at the end once the customer has finished.

    def LaneStatus(self):
        #Will check if the lane needs to be opened or closed.

    def OpenNewLane(self):
        #Will open a new lane if LaneStatus returns Open.

    def CloseLane(self):
        #Will close the lane if LaneStatus returns Close.



b = Lane()
b.CreateSelfCheckoutFile()






