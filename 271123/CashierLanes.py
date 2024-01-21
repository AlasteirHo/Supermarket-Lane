from Lane import Lanes
import json
import time


class CashierLanes(Lanes):
    def __init__(self):
        super().__init__()
        self.cashier_checkout_customers = {}
        self.lane_number = None

    @staticmethod
    def write_cashier_file(data):
        # Write cashier customer data to a JSON file.
        with open("StoringData/CashierData/Cashier.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    @staticmethod
    def write_cashier_lane_file(data):
        # Write cashier lane data to a JSON file.
        with open("StoringData/CashierData/CashierLane.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    def create_cashier_file(self):
        # Create a JSON file with sorted cashier customers.
        result = self.sort_into_cashier_lanes()
        with open("StoringData/CashierData/Cashier.json", "w") as f:
            f.write(json.dumps(result, indent=2))

    def update_cashier_file(self, data):
        # Update cashier lane file with new data.
        current_content = self.extract_lanes("cashier")
        current_content.update(data)
        with open("StoringData/CashierData/CashierLane.json", "w") as f:
            f.write(json.dumps(current_content, indent=2))

    def sort_into_cashier_lanes(self):
        # Sort customers into cashier lanes based on basket size.
        ordered_data = self.extract_ordered_customers()

        for keys in ordered_data:
            if ordered_data[keys]["basket_size"] >= 10:
                self.cashier_checkout_customers.update({
                    keys: {
                        "customer_id": ordered_data[keys]["customer_id"],
                        "basket_size": ordered_data[keys]["basket_size"],
                        "lane_type": "Cashier",
                        "process_time": ordered_data[keys]["time_at_cashier"]
                    }
                })
        return self.cashier_checkout_customers

    def add_new_cashier_lanes(self, new_lane_number):
        # Add a new cashier lane.
        new_lane_details = {
            "time_stamp": self.get_time(),
            "lane_open": self.lane_status,
            "customers_in_lane": 0,
        }
        new_lane = f"LaneNumber {new_lane_number}"
        self.cashier_lane[new_lane] = new_lane_details
        self.update_cashier_file(self.cashier_lane)

    def update_and_delete_customer_file(self, customer_id):
        # Update and delete customer data file.
        current_content = self.extract_customer_data("cashier")

        if customer_id in current_content:
            del current_content[customer_id]
            with open("StoringData/CashierData/Cashier.json", "w") as f:
                f.write(json.dumps(current_content, indent=2))
        else:
            print("Customer cannot be found.")

    def increment_cashier_lane(self, lane_number):
        # Increment the customer count in a cashier lane.
        lanes = self.extract_lanes("cashier")
        customers_in_lane = lanes[lane_number]["customers_in_lane"]

        try:
            lanes[lane_number].update({
                "customers_in_lane": customers_in_lane + 1
            })
            self.write_cashier_lane_file(lanes)
        except KeyError:
            print(f"Lane Number {lane_number} was not found")

    def open_new_lane(self, best_lane):
        # Open a new cashier lane if the current lane is full.
        data = self.extract_lanes("cashier")
        customers_in_lane = data[best_lane]["customers_in_lane"]

        # Check if the current lane is full (maximum customers is 5).
        if customers_in_lane == 5:
            # Determine the number for the new lane.
            new_lane_number = int(best_lane.split()[-1]) + 1

            # Add a new cashier lane with the next available lane number.
            self.add_new_cashier_lanes(new_lane_number)

    def close_lane(self):
        # Close empty cashier lanes.
        data = self.extract_lanes("cashier")
        empty_lanes = []

        # Iterate over cashier lanes and identify empty or negatively impacted lanes.
        for lane_number, customers in data.items():
            if customers["customers_in_lane"] == 0:
                empty_lanes.append(lane_number)
            elif customers["customers_in_lane"] < 0:  # Avoid negative customer counts impacting future lanes.
                empty_lanes.append(lane_number)

        # Check if there are empty lanes to be closed.
        if len(empty_lanes) != 0:
            # Remove empty lanes from the data.
            for lanes in empty_lanes:
                del data[lanes]

            # Write the updated cashier lane data to the file.
            self.write_cashier_lane_file(data)

        self.write_cashier_lane_file(data)

    def process_items(self):
        # Process items for customers in cashier lanes.
        customers_in_cashier = self.extract_customer_data("cashier")
        for keys in customers_in_cashier:  # Loops through the number of customers in cashier lanes.
            updated_customers_dict = self.extract_customer_data("cashier")
            delays = (updated_customers_dict[keys]["process_time"])  # Calculated using the formula given.
            customer_lane_number = (updated_customers_dict[keys]["cashier_lane_number"])
            time.sleep(2)
            self.decrease_lane_number(customer_lane_number)  # Decreases the lane number after removal.
            self.update_and_delete_customer_file(keys)  # Shows the deletion in the files.

    def decrease_lane_number(self, number):
        # Decrease the customer count in a cashier lane.
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
        # Add cashier lane information to the customer data.
        customers = self.extract_customer_data("cashier")
        try:
            lane_number = int(lane_number.split()[-1])
            customers[customer_id].update({
                "cashier_lane_number": lane_number
            })
            self.write_cashier_file(customers)
        except KeyError:
            print("Customer ID not found.")

    def find_best_lane(self):
        # Find the cashier lane with the fewest customers.
        data = self.extract_lanes("cashier")
        best_lane = None
        least_customers = float("inf")

        for lane_number, customers in data.items():
            if customers["customers_in_lane"] < least_customers:
                least_customers = customers["customers_in_lane"]
                best_lane = lane_number

        return best_lane

    def main(self):
        # Main simulation function for cashier lanes.
        customers = self.extract_customer_data("cashier")
        for customer, lane in customers.items():
            best_lane = self.find_best_lane()
            self.add_lane_number_to_customer(customer, best_lane)
            self.open_new_lane(best_lane)
            self.increment_cashier_lane(best_lane)
            # self.display_lane_status()
        self.process_items()
        self.close_lane()


# Uncommented code for creating an instance of CashierLanes and running the simulation.
# C1.increment_cashier_lane()
# print(C1.find_best_lane())

# This will add customers and increment the lanes.
# C1.open_new_lane(C1.find_best_lane())
# Functions that need to be used for later:
# C1.create_cashier_file()
#
