from Lane import Lanes
import json
import time


class CashierLanes(Lanes):
    def __init__(self):
        self.CashierCheckoutCustomers = {}
        self.laneNumber = 1
        self.ServiceLane = 1
        super().__init__()


    def ExtractCustomerData(self): #Extracts the current customers in the Cashier.json file.
        with open("StoringData/CashierData/Cashier.json", "r") as f:
            CustomersInCashier = json.load(f)
        return CustomersInCashier

    @staticmethod
    def WriteCashierFile(data): #Used to write data into the Cashier.json file.
        with open("StoringData/CashierData/Cashier.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    # Updates the Cashier Lane file
    @staticmethod
    def WriteCashierLaneFile(data): #Used to write data into the CashierLane.json file.
        with open("StoringData/CashierData/CashierLane.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    def CreateCashierFile(self): #Creates the cashier file.
        result = self.SortIntoCashierLanes()
        with open("StoringData/CashierData/Cashier.json", "w") as f:
            f.write(json.dumps(result, indent=2))

    def UpdateCashierFile(self,data): #Used to update the cashier file with new data.
        current_content = self.ExtractCashierLanes()
        current_content.update(data)
        with open("StoringData/CashierData/CashierLane.json", "w") as f:
            f.write(json.dumps(current_content, indent=2))

    def SortIntoCashierLanes(self): #Used to check if customers meet the requirements to be in the Cashier Lane.
        ordered_data = self.extract_ordered_customers()

        for keys in ordered_data:
            if ordered_data[keys]["Basket Size"] >= 10: #Checks if their basket size is over or equal to 10.
                self.CashierCheckoutCustomers.update({ #If so we update the Customer carrying over their values and updating their lane type.
                    keys: {
                        "CustomerID": ordered_data[keys]["CustomerID"],
                        "Items In Basket": ordered_data[keys]["Basket Size"],
                        "Lane Type": "Cashier",
                        "Process Time": ordered_data[keys]["Time at Cashier"]
                    }
                })
        return self.CashierCheckoutCustomers


    def AddNewCashierLanes(self, NewLaneNumber): #Used to create a new lane and assign its values.
        NewLaneDetails = {
            "TimeStamp": self.getTime(),
            "LaneOpen": self.LaneStatus,
            "CustomersInLane": 0,
        }
        NewLane = f"LaneNumber {NewLaneNumber}"
        self.CashierLane[NewLane] = NewLaneDetails
        self.UpdateCashierFile(self.CashierLane)



    def UpdateAndDeleteCustomerFile(self,customerID): #Used to remove customers from the lane and update the Cashier.json file to show the removal.
        current_content = self.ExtractCustomerData()

        if customerID in current_content:
            del current_content[customerID]
            with open("StoringData/CashierData/Cashier.json", "w") as f:
                f.write(json.dumps(current_content, indent=2))
        else:
            print("Customer cannot be found.")


    def IncrementCashierLane(self, laneNumber): #Used to increment the customerinlane value by 1.
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
        data = self.ExtractCashierLanes()

        for LaneNumber, Customers in data.items():
            if Customers["CustomersInLane"] == 5:
                NewLaneNumber = int(LaneNumber.split(" ")[1]) + 1
                self.AddNewCashierLanes(NewLaneNumber)
            else:
                print("No need to open new lane.")


    def CloseNewLane(self):
        data = self.ExtractCashierLanes()
        EmptyLanes = []


        for LaneNumber, Customers in data.items():
            if Customers["CustomersInLane"] == 0:
                EmptyLanes.append(LaneNumber)

        if len(EmptyLanes) != 0:
            for lanes in EmptyLanes:
                del data[lanes]

        self.WriteCashierLaneFile(data)

    def ProcessItems(self):
        Customers_In_Cashier = self.ExtractCustomerData()
        for keys in Customers_In_Cashier:
            UpdatedCustomersDict = self.ExtractCustomerData()
            Delays = (UpdatedCustomersDict[keys]["Process Time"]) #Calculated using the formula given.
            CustomerLaneNumber = (UpdatedCustomersDict[keys]["Cashier Lane Number"])
            time.sleep(Delays)
            self.DecreaseLaneNumber(CustomerLaneNumber)
            self.UpdateAndDeleteCustomerFile(keys)

    def DisplayLaneStatus(self):
        lanes = self.ExtractCashierLanes()
        for lane_name, lane_details in lanes.items():
            if lane_details['LaneOpen'] == 'Open':
                print(f"{lane_name} (Cashier): {'*' * lane_details['CustomersInLane']}")
        pass

    def DecreaseLaneNumber(self, Number):
        data = self.ExtractCashierLanes()
        laneNumber = f"LaneNumber {Number}"
        CustomersInLane = data[laneNumber]["CustomersInLane"]
        try:
            data[laneNumber].update({
                "CustomersInLane": CustomersInLane - 1
            })
            self.WriteCashierLaneFile(data)

        except KeyError:
            print("Lane Number was not found")

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
        Customers = self.ExtractCustomerData()

        for customer, lane in Customers.items():
            self.CloseNewLane()
            if "Cashier Lane Number" not in lane:
                self.OpenNewLane()
                best_lane = self.FindBestLane()
                self.AddLaneNumberToCustomer(customer, best_lane)
                self.IncrementCashierLane(best_lane)


C1 = CashierLanes()
# C1.AddCustomerToLane() #This will add customers and increment the lanes.
#Functions that need to be used for later:
C1.DisplayLaneStatus()
# C1.ProcessItems()