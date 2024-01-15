from Lane import Lanes
import json
import time


class CashierLanes(Lanes):
    def __init__(self):
        super().__init__()
        self.CashierCheckoutCustomers = {}
        self.laneNumber = 1
        self.ServiceLane = 1

    @staticmethod
    def write_cashier_file(data):  # Used to write data into the Cashier.json file.
        with open("StoringData/CashierData/Cashier.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    @staticmethod
    def write_cashier_lane_file(data):  # Used to write data into the CashierLane.json file.
        with open("StoringData/CashierData/CashierLane.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    def create_cashier_file(self):  # Creates the cashier file.
        result = self.sort_into_cashier_lanes()
        with open("StoringData/CashierData/Cashier.json", "w") as f:
            f.write(json.dumps(result, indent=2))

    def update_cashier_file(self, data):  # Used to update the cashier file with new data.
        current_content = self.extract_lanes("cashier")
        current_content.update(data)
        with open("StoringData/CashierData/CashierLane.json", "w") as f:
            f.write(json.dumps(current_content, indent=2))

    def sort_into_cashier_lanes(self):  # Used to check if customers meet the requirements to be in the Cashier Lane.
        ordered_data = self.extract_ordered_customers()

        for keys in ordered_data:
            if ordered_data[keys]["basket_size"] >= 10:  # Checks if their basket size is over or equal to 10.
                self.CashierCheckoutCustomers.update({  # If so, we update the Customer carrying over their values and updating their lane type.
                    keys: {
                        "customer_id": ordered_data[keys]["customer_id"],
                        "basket_size": ordered_data[keys]["basket_size"],
                        "lane_type": "Cashier",
                        "process_time": ordered_data[keys]["time_at_cashier"]
                    }
                })
        return self.CashierCheckoutCustomers

    def add_new_cashier_lanes(self, new_lane_number):  # Used to create a new lane and assign its values.
        new_lane_details = {
            "time_stamp": self.get_time(),
            "lane_open": self.lane_status,
            "customers_in_lane": 0,
        }
        new_lane = f"LaneNumber {new_lane_number}"
        self.cashier_lane[new_lane] = new_lane_details
        self.update_cashier_file(self.cashier_lane)

    def update_and_delete_customer_file(self, customer_id):  # Used to remove customers from the lane and update the Cashier.json file to show the removal.
        current_content = self.extract_customer_data("cashier")

        if customer_id in current_content:
            del current_content[customer_id]
            with open("StoringData/CashierData/Cashier.json", "w") as f:
                f.write(json.dumps(current_content, indent=2))
        else:
            print("Customer cannot be found.")


    def increment_cashier_lane(self, lane_number):  # Used to increment the customerinlane value by 1.
        customers = self.extract_lanes("cashier")
        customers_in_lane = customers[lane_number]["customers_in_lane"]
        try:
            customers[lane_number].update({
                "customers_in_lane": customers_in_lane + 1
            })
            self.write_cashier_lane_file(customers)

        except KeyError:
            print(f"Lane Number {lane_number} was not found")

    def open_new_lane(self):
        data = self.extract_lanes("cashier")

        for lane_number, customers in data.items():
            if customers["customers_in_lane"] == 5:
                new_lane_number = int(lane_number.split(" ")[1]) + 1
                self.add_new_cashier_lanes(new_lane_number)
            else:
                pass

    def close_new_lane(self):
        data = self.extract_lanes("cashier")
        empty_lanes = []

        for lane_number, customers in data.items():
            if customers["customers_in_lane"] == 0:
                empty_lanes.append(lane_number)

        if len(empty_lanes) != 0:
            for lanes in empty_lanes:
                del data[lanes]

        self.write_cashier_lane_file(data)

    def process_items(self):
        customers_in_cashier = self.extract_customer_data("cashier")
        for keys in customers_in_cashier:
            updated_customers_dict = self.extract_customer_data("cashier")
            delays = (updated_customers_dict[keys]["process_time"])  # Calculated using the formula given.
            customer_lane_number = (updated_customers_dict[keys]["cashier_lane_number"])
            time.sleep(2)
            self.decrease_lane_number(customer_lane_number)
            self.update_and_delete_customer_file(keys)

    def display_lane_status(self):
        lanes = self.extract_lanes("cashier")
        for lane_name, lane_details in lanes.items():
            if lane_details['LaneOpen'] == 'Open' and lane_details["customers_in_lane"] != 0:
                print(f"{lane_name} (Cashier): {'*' * lane_details['customers_in_lane']}")
        pass

    def decrease_lane_number(self, number):
        data = self.extract_lanes("cashier")
        lane_number = f"LaneNumber {number}"
        customers_in_lane = data[lane_number]["customers_in_lane"]
        try:
            data[lane_number].update({
                "customers_in_lane": customers_in_lane - 1
            })
            self.write_cashier_lane_file(data)

        except KeyError:
            print("Lane Number was not found")

    def add_lane_number_to_customer(self, customer_id, lane_number):
        customers = self.extract_customer_data("cashier")
        try:
            lane_number = int(lane_number.split()[-1])
            print(lane_number)
            customers[customer_id].update({
                "cashier_lane_number": lane_number
            })
            self.write_cashier_file(customers)
        except KeyError:
            print("Customer ID not found.")

    def find_best_lane(self):
        data = self.extract_lanes("cashier")
        best_lane = None
        least_customers = float("inf")

        for lane_number, customers in data.items():
            if customers["customers_in_lane"] < least_customers:
                least_customers = customers["customers_in_lane"]
                best_lane = lane_number

        return best_lane

    def add_customer_to_lane(self):
        customers = self.extract_customer_data("cashier")
        iteration = 0
        for customer, lane in customers.items():
            if "cashier_lane_number" not in lane:
                if iteration != 0:
                    self.close_new_lane()
                self.open_new_lane()
                best_lane = self.find_best_lane()
                self.increment_cashier_lane(best_lane)
                self.add_lane_number_to_customer(customer, best_lane)
                iteration += 1
                # self.process_items()





C1 = CashierLanes()
C1.add_customer_to_lane()
# This will add customers and increment the lanes.
# Functions that need to be used for later:
# C1.display_lane_status()
# C1.create_cashier_file()
#
