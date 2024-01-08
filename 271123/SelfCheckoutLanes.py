from Lane import Lanes
import json

class SelfCheckout(Lanes):
    def __init__(self):
        super().__init__()
        self.SelfCheckoutCustomers = {}
        self.MaxCustomer = 1


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

    def UpdateSelfCheckoutLanes(self,lane_number):
        data = self.ExtractLaneData()
        CustomersInLane = data[lane_number]["CustomersInSelfCheckoutLane"]
        print(CustomersInLane)
        try:
            data[lane_number]["CustomersInSelfCheckoutLane"] = CustomersInLane + 1
            data[lane_number]["LaneOpen"] = "Open"
            self.WriteSelfCheckoutLanes(data)
        except KeyError:
            print("Lane was not found.")

    def CloseSelfCheckoutLanes(self):
        data = self.ExtractLaneData()
        for lanes, keys in data.items():
            if data[lanes]["LaneOpen"] == "Open" and data[lanes]["CustomersInSelfCheckoutLane"] == 0:
                print(lanes)

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

    def main(self):
        Customers = self.ExtractCustomerData()
        for customer, lane in Customers.items():
            lane = self.FindBestLane()
            self.AddSelfCheckoutLaneToCustomer(customer, lane)
            self.UpdateSelfCheckoutLanes(lane)



T = SelfCheckout()
# T.main()
T.CloseSelfCheckoutLanes()
# T.CreateSelfCheckoutFile()