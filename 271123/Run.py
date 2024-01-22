import time
import random
from CustomerItemProcessor import Customer


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


if __name__ == "__main__":
    S1 = Simulation()
    S1.initialize_simulation()
    max_time = time.time() + 60 * 10  # Runs for 10 minutes
    while time.time() < max_time and S1.is_running:
        interval = random.randint(1, 5)
        S1.main_loop()
        S1.display_cus_details()
        time.sleep(interval)
