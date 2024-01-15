import random
import time
from datetime import datetime, timedelta

from CustomerItemProcessor import Customer, ItemProcessing
# from SelfCheckoutLanes import SelfCheckout
# from Lane import Lanes
# from CashierLanes import CashierLanes


class Simulation(Customer):
    def __init__(self):
        super().__init__()
        self.simulation_time = None
        self.opening_time = datetime.strptime('07:00:00', '%H:%M:%S')
        self.closing_time = datetime.strptime('23:00:00', '%H:%M:%S')
        self.simulation_interval = 5
    @staticmethod
    def initialize_customers():
        initial_customers = []
        for i in range(random.randint(1, 10)):
            first_customers = Customer.create_customer()
            initial_customers.append(first_customers)

            processing_time_cashier, processing_time_self_checkout = ItemProcessing.calculate_processing_time(
                first_customers.basket_size)
            first_customers.processing_time_cashier = processing_time_cashier
            first_customers.processing_time_self_checkout = processing_time_self_checkout
            lottery_status = ItemProcessing.award_lottery(first_customers)
            ItemProcessing.display_customer_details(first_customers, lottery_status)

    def initialize_simulation(self):
        self.simulation_time = self.opening_time
        print(f"Simulation started at {self.simulation_time.strftime('%H:%M:%S')}")
        self.initialize_customers()
        self.simulation_time += timedelta(seconds=30)

        time.sleep(self.simulation_interval)
    def main_loop(self):

        while self.simulation_time.time() < self.closing_time.time():
            simulation_time = self.simulation_time
            print(f"Current Time: {simulation_time.strftime('%H:%M:%S')}")

            num_customers = random.randint(1, 10)
            for i in range(num_customers):
                customer_spawn = Customer.create_customer()
                processing_time_cashier, processing_time_self_checkout = ItemProcessing.calculate_processing_time(
                    customer_spawn.basket_size)

                customer_spawn.processing_time_cashier = processing_time_cashier
                customer_spawn.processing_time_self_checkout = processing_time_self_checkout

                lottery_status = ItemProcessing.award_lottery(customer_spawn)
                ItemProcessing.display_customer_details(customer_spawn, lottery_status)

                Customer.save_customer_dict_to_json()

            # Move time forward in the simulation
            self.simulation_time += timedelta(seconds=30)

            # Simulate real-time passage (sleep for 30 seconds)
            time.sleep(self.simulation_interval)


if __name__ == "__main__":
    simulation = Simulation()
    simulation.initialize_simulation()
    simulation.main_loop()
