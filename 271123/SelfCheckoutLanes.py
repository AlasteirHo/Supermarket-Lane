from Lane import Lanes
import json
import time

class SelfCheckout(Lanes):
    def __init__(self):
        super().__init__()
        self.SelfCheckoutCustomers = {}



    def SortIntoSelfCheckoutLanes(self):
        ordered_data = self.extract_ordered_customers()

        for keys in ordered_data:
            if ordered_data[keys]["Basket Size"] < 10:
                self.SelfCheckoutCustomers.update({
                    keys: {
                        "CustomerID": ordered_data[keys]["CustomerID"],
                        "Items In Basket": ordered_data[keys]["Basket Size"],
                        "Lane Type": "SelfCheckout",
                        "Process Time": ordered_data[keys]["Time at Cashier"]
                    }
                })
        return self.SelfCheckoutCustomers

    def CreateSelfCheckoutFile(self):
        result = self.SortIntoSelfCheckoutLanes()
        with open("StoringData/SelfCheckoutData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(result, indent=2))


    def ExtractCustomerData(self):
        with open("StoringData/SelfCheckoutData/SelfCheckout.json", "r") as f:
            CustomersInSelfCheckout = json.load(f)
        return CustomersInSelfCheckout

    @staticmethod
    def ExtractLaneData():
        with open("StoringData/SelfCheckoutData/SelfCheckoutLane.json", "r") as f:
            SelfCheckoutLaneData = json.load(f)
        return SelfCheckoutLaneData
    @staticmethod
    def WriteSelfCheckoutLanes(data):
        with open("StoringData/SelfCheckoutData/SelfCheckoutLane.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    @staticmethod
    def WriteSelfCheckoutCustomer(data):
        with open("StoringData/SelfCheckoutData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    def FindBestLane(self):
        data = self.ExtractLaneData()
        for lanes, customers in data.items():
            if customers["CustomersInSelfCheckoutLane"] == 0:
                return lanes

    def RemoveCustomerFromSelfCheckout(self, customerID):
        Customers = self.ExtractCustomerData()

        if customerID in Customers:
            del Customers[customerID]
            print(f"The key {customerID} has been deleted")
            with open("StoringData/SelfCheckoutData/SelfCheckout.json", "w") as f:
                f.write(json.dumps(Customers, indent=2))
        else:
            print("Customer was not found")

    def OpenSelfCheckoutLanes(self,lane_number):
        data = self.ExtractLaneData()
        CustomersInLane = data[lane_number]["CustomersInSelfCheckoutLane"]
        print(CustomersInLane)
        try:
            data[lane_number]["CustomersInSelfCheckoutLane"] = 1
            data[lane_number]["LaneOpen"] = "Open"
            self.WriteSelfCheckoutLanes(data)
        except KeyError:
            print("Lane was not found.")

    def DecreaseSelfCheckoutLanes(self, lane_number):
        data = self.ExtractLaneData()
        SelfCheckoutLane = f"SelfCheckoutTill {lane_number}"
        try:
            data[SelfCheckoutLane]["CustomersInSelfCheckoutLane"] = 0
            data[SelfCheckoutLane]["LaneOpen"] = "Closed"
            self.WriteSelfCheckoutLanes(data)
        except KeyError:
            print("Lane was not found.")


    def ProcessItems(self):
        CustomersInSelfCheckoutLane = self.ExtractCustomerData()
        for keys in CustomersInSelfCheckoutLane:
            UpdatedCustomerDict = self.ExtractCustomerData()
            Delays = (UpdatedCustomerDict[keys]["Process Time"])
            CustomerLaneNumber = (UpdatedCustomerDict[keys]["SelfCheckoutLane Number"])
            print(CustomerLaneNumber)
            time.sleep(Delays)
            self.DecreaseSelfCheckoutLanes(CustomerLaneNumber)
            self.RemoveCustomerFromSelfCheckout(keys)


    def AddSelfCheckoutLaneToCustomer(self, CustomerID, LaneNumber):
        Customers = self.ExtractCustomerData()
        try:
            LaneNumber = int(LaneNumber.split()[-1])
            Customers[CustomerID].update({
                "SelfCheckoutLane Number": LaneNumber
            })
            self.WriteSelfCheckoutCustomer(Customers)
        except KeyError:
            print("Customer ID not found.")

    def DisplayLaneStatus(self):
        lanes = self.ExtractLaneData()
        total_customers = 0
        for lane_name, lane_details in lanes.items():
            if lane_details['LaneOpen'] == 'Open':
                total_customers += lane_details['CustomersInSelfCheckoutLane']

        return total_customers

    def main(self):
        Customers = self.ExtractCustomerData()
        for customer, lane in Customers.items():
            lane = self.FindBestLane()
            self.AddSelfCheckoutLaneToCustomer(customer, lane)
            self.OpenSelfCheckoutLanes(lane)

        self.ProcessItems()

#Remember to include if all the lanes are full to return lane saturation

T = SelfCheckout()
# T.main()
T.DisplayLaneStatus()
# T.DecreaseSelfCheckoutLanes("SelfCheckoutTill 1")
# T.CreateSelfCheckoutFile()
# T.ProcessItems()