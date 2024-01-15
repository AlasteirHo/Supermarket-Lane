import json
# import time
from datetime import datetime
import random

MAX_CASHIER_LANE = 5
MAX_SELF_CHECKOUT_LANE = 8

class Lanes:
    def __init__(self):
        self.total_customer = 0
        self.lane_status = "Open"
        self.cashier_lane = {}
        self.self_checkout = {}
        self.ordered_dict_items = {}

    def create_lane(self, lane_type, lane_number=None):
        if lane_type == "cashier":
            lane_dict = {
                f"LaneNumber {lane_number}": {
                    "time_stamp": self.get_time(),
                    "lane_open": self.lane_status,
                    "customers_in_lane": 0,
                }
            }
            self.cashier_lane.update(lane_dict)
            self.write_lane("cashier",self.cashier_lane)
        elif lane_type == "self_checkout":
            lane_dict = {
                f"SelfCheckoutTill {lane_number}": {
                    "lane_open": "Closed",
                    "customers_in_self_checkout_lane": 0,
                } for lane_number in range(1, MAX_SELF_CHECKOUT_LANE + 1)
            }
            self.self_checkout.update(lane_dict)
            self.write_lane("self_checkout",self.self_checkout)

    def write_lane(self, lane_type,data):
        if lane_type == "cashier":
            with open("StoringData/CashierData/CashierLane.json", "w") as f:
                json.dump(data, f, indent=2)
        elif lane_type == "self_checkout":
            with open("StoringData/SelfCheckoutData/SelfCheckoutLane.json", "w") as f:
                json.dump(self.self_checkout, f, indent=2)

    @staticmethod
    def extract_lanes(lane_type):
        if lane_type == "cashier":
            with open("StoringData/CashierData/CashierLane.json", "r") as f:
                data = json.load(f)
        elif lane_type == "self_checkout":
            with open("StoringData/SelfCheckoutData/SelfCheckoutLane.json", "r") as f:
                data = json.load(f)
        return data

    @staticmethod
    def extract_ordered_customers():
        with open("StoringData/OrderedCustomers.json", "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def extract_customers():
        with open("customer_data.json", "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def extract_customer_data(customer_type):
        if customer_type == "cashier":
            with open("StoringData/CashierData/Cashier.json", "r") as f:  # Change this to the new file
                data = json.load(f)
        elif customer_type == "self_checkout":
            with open("StoringData/SelfCheckoutData/SelfCheckout.json", "r") as f:  # Change this to the new file
                data = json.load(f)
        return data

    def set_customer_data(self):
        with open("StoringData/OrderedCustomers.json", "w") as f:
            json.dump(self.ordered_dict_items, f, indent=2)

    def sort_customer(self):
        customer_data = self.extract_customers()
        self.ordered_dict_items = dict(sorted(customer_data.items(), key=lambda item: item[1]['basket_size']))
        self.set_customer_data()
        return self.ordered_dict_items

    @staticmethod
    def get_time():
        timestamp = datetime.now()
        hour = timestamp.hour
        minute = timestamp.minute
        current_time = f"{hour}:{minute}"
        return current_time

    def cashier_customer_total(self):
        total_customers = 0
        data = self.extract_lanes("cashier")
        for lane_number, lane_data in data.items():
            total_customers += lane_data["customers_in_lane"]
        if total_customers == MAX_CASHIER_LANE * 5:
            return "Lane Saturation"
        else:
            return total_customers

    def self_checkout_customer_total(self):
        total_customers = 0
        data = self.extract_lanes("self_checkout")
        for lane_number, lane_data in data.items():
            total_customers += lane_data["customers_in_self_checkout_lane"]
        if total_customers == MAX_SELF_CHECKOUT_LANE:
            return "Lane Saturation"
        else:
            return total_customers

Checkout1 = Lanes()
# Checkout1.create_lane("self_checkout")
# Checkout1.extract_customer_data()