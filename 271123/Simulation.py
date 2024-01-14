import random
import time
from datetime import datetime, timedelta
from CustomerItemProcessor import Customer, ItemProcessing
from SelfCheckoutLanes import SelfCheckout
from Lane import Lanes
from CashierLanes import CashierLanes


class Simulation(Customer):
    def __init__(self, basket_size):
        super().__init__(basket_size)
        self.simulation_time = None
        self.opening_time = datetime.strptime('07:00:00', '%H:%M:%S')
        self.closing_time = datetime.strptime('23:00:00', '%H:%M:%S')

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
        print(f"Simulation started at {self.simulation_time.strftime('%H:%M')}")
        self.initialize_customers()
        self.simulation_time += timedelta(minutes=30)

    def main_loop(self):
        simulation_interval = 5
        end_simulation = False

        while self.simulation_time.time() < self.closing_time.time() and not end_simulation:
            user_input = input("Enter anything to end the simulation or press enter to continue to next interval: ")
            if user_input:
                end_simulation = True
            else:
                simulation_time = self.simulation_time
                print(f"Current Time: {simulation_time.strftime('%H:%M')}")

            # Generate a random number of customers (up to 10) every 30 seconds
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
            self.simulation_time += timedelta(minutes=30)

            # Simulate real-time passage (sleep for 30 seconds)
            time.sleep(simulation_interval)

        # Display the final state of the customer dictionary
        # Customer.display_customer_dict()


if __name__ == "__main__":
    simulation = Simulation(0)
    simulation.initialize_simulation()
    simulation.main_loop()
