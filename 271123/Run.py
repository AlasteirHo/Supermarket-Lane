import time
import random
from CustomerItemProcessor import Customer
from Lane import Lanes
from CashierLanes import CashierLanes
from SelfCheckoutLanes import SelfCheckout

lane = Lanes()
cashier_lanes = CashierLanes()
self_checkout = SelfCheckout()

class Simulation:
    def __init__(self):
        self.is_running = False
        self.start_time = 0

    def initialize_simulation(self):
        start_time = time.time()  # Save the start time
        start_time_str = time.strftime("%H:%M:%S", time.localtime(start_time))
        print(f"Simulation started at: {start_time_str}")

        initial_customer = random.randint(1, 10)
        for i in range(initial_customer):
            C1 = Customer()
            C1.create_customer()
        self.is_running = True

    def initalize_lanes(self):
        lane.create_lane("cashier")
        lane.create_lane("self_checkout")
        self_checkout.create_self_checkout_file()
        cashier_lanes.create_cashier_file()

    def update_lane(self):
        self.is_running = True
        if self.is_running:
            print("Starting Lane Simulation...")
            self.initalize_lanes()
            print("Files have been created.")
            self_checkout_total = lane.self_checkout_customer_total()
            cashier_total = lane.cashier_customer_total()
            total_customers = self_checkout_total + cashier_total #Will check if all lanes are full or not.
            if total_customers == 40:
                print("Lane saturation") #Will print Lane saturation and avoid the next iterations.
            else:
                self_checkout.main()
                cashier_lanes.main()

    def main_loop(self):
        self.customer_creator()

    @staticmethod
    def customer_creator():
        customer = Customer()
        customer.create_customer()

    @staticmethod
    def display_cus_details():
        # Call the static method to display customer details
        print("--------------------------------------------")
        Customer.display_customer_details(Customer.customer_dict)

    def stop_simulation(self):
        self.is_running = False

# S1 = Simulation()
# S1.initialize_simulation()
# max_time = time.time() + 60 * 10    # Runs for 10 minutes
# while time.time() < max_time and S1.is_running:
# S1.main_loop()
# S1.display_cus_details()
