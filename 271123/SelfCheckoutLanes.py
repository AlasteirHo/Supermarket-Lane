from Lane import Lanes
import json
import time

class SelfCheckout(Lanes):
    def __init__(self):
        super().__init__()
        self.self_checkout_customers = {}

    def sort_into_self_checkout_lanes(self):
        ordered_data = self.extract_ordered_customers()

        for keys in ordered_data:
            if ordered_data[keys]["basket_size"] < 10:
                self.self_checkout_customers.update({
                    keys: {
                        "customer_id": ordered_data[keys]["customer_id"],
                        "items_in_basket": ordered_data[keys]["basket_size"],
                        "lane_type": "SelfCheckout",
                        "process_time": ordered_data[keys]["time_at_self_service"]
                    }
                })
        return self.self_checkout_customers

    def create_self_checkout_file(self):
        result = self.sort_into_self_checkout_lanes()
        with open("StoringData/SelfCheckoutData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(result, indent=2))

    @staticmethod
    def extract_customer_data():
        with open("StoringData/SelfCheckoutData/SelfCheckout.json", "r") as f:
            customers_in_self_checkout = json.load(f)
        return customers_in_self_checkout

    @staticmethod
    def extract_lane_data():
        with open("StoringData/SelfCheckoutData/SelfCheckoutLane.json", "r") as f:
            self_checkout_lane_data = json.load(f)
        return self_checkout_lane_data

    @staticmethod
    def write_self_checkout_lanes(data):
        with open("StoringData/SelfCheckoutData/SelfCheckoutLane.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    @staticmethod
    def write_self_checkout_customer(data):
        with open("StoringData/SelfCheckoutData/SelfCheckout.json", "w") as f:
            f.write(json.dumps(data, indent=2))

    def find_best_lane(self):
        data = self.extract_lane_data()
        for lanes, customers in data.items():
            if customers["customers_in_self_checkout_lane"] == 0:
                return lanes

    def remove_customer_from_self_checkout(self, customer_id):
        customers = self.extract_customer_data()

        if customer_id in customers:
            del customers[customer_id]
            print(f"The key {customer_id} has been deleted")
            with open("StoringData/SelfCheckoutData/SelfCheckout.json", "w") as f:
                f.write(json.dumps(customers, indent=2))
        else:
            print("Customer was not found")

    def open_self_checkout_lanes(self, lane_number):
        data = self.extract_lane_data()
        try:
            data[lane_number]["customers_in_self_checkout_lane"] = 1
            data[lane_number]["lane_open"] = "Open"
            self.write_self_checkout_lanes(data)
        except KeyError:
            print("Lane was not found.")

    def decrease_self_checkout_lanes(self, lane_number):
        data = self.extract_lane_data()
        self_checkout_lane = f"SelfCheckoutTill {lane_number}"
        try:
            data[self_checkout_lane]["customers_in_self_checkout_lane"] = 0
            data[self_checkout_lane]["lane_open"] = "Closed"
            self.write_self_checkout_lanes(data)
        except KeyError:
            print("Lane was not found.")

    def process_items(self):
        customers_in_self_checkout_lane = self.extract_customer_data()
        for keys in customers_in_self_checkout_lane:
            updated_customer_dict = self.extract_customer_data()
            delays = updated_customer_dict[keys]["process_time"]
            customer_lane_number = updated_customer_dict[keys]["self_checkout_lane_number"]
            time.sleep(5)
            self.decrease_self_checkout_lanes(customer_lane_number)
            self.remove_customer_from_self_checkout(keys)

    def add_self_checkout_lane_to_customer(self, customer_id, lane_number):
        customers = self.extract_customer_data()
        try:
            lane_number = int(lane_number.split()[-1])
            customers[customer_id].update({
                "self_checkout_lane_number":lane_number
            })
            self.write_self_checkout_customer(customers)
        except KeyError:
            print("Customer ID not found.")

    def display_lane_status(self):
        lanes = self.extract_lane_data()
        total_customers = 0
        for lane_name, lane_details in lanes.items():
            if lane_details['lane_open'] == 'Open':
                total_customers += lane_details['customers_in_lane']

        return total_customers

    def main(self):
        customers = self.extract_customer_data()
        for customer, lane in customers.items():
            lane = self.find_best_lane()
            self.add_self_checkout_lane_to_customer(customer, lane)
            self.open_self_checkout_lanes(lane)

        # self.process_items()

# Remember to include if all the lanes are full to return lane saturation

t = SelfCheckout()
# t.create_self_checkout_file()
# t.main()
# t.display_lane_status()
# t.decrease_self_checkout_lanes("SelfCheckoutTill 1")
# t.create_self_checkout_file()
# t.process_items()
