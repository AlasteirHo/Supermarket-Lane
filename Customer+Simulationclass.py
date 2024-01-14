from datetime import datetime, timedelta
import random
import json
import time



class Customer:
    Customer_Dict = {}
    current_customer_id = 0

    def __init__(self, basket_size):
        self.customer_id = f"C{Customer.current_customer_id}"
        self.customer_num = f"Customer {Customer.current_customer_id}"
        Customer.current_customer_id += 1

        self.basket_size = basket_size
        self.processing_time_cashier = 0
        self.processing_time_self_checkout = 0
        self.lottery_ticket = False

    def basket_size_randomizer(self):
        self.basket_size = random.randint(1, 30)

    @staticmethod
    def create_customer():
        customer = Customer(0)  # Initialize with basket_size = 0
        customer.basket_size_randomizer()  # Use the randomizer to set the basket size
        Customer.Customer_Dict[customer.customer_id] = customer
        return customer

    @staticmethod
    def save_customer_dict_to_json():
        customer_data = {}
        for customer_id, customer in Customer.Customer_Dict.items():
            customer_data[customer.customer_num] = {
                "CustomerID": customer.customer_id,
                "Basket Size": customer.basket_size,
                "Lottery Ticket": customer.lottery_ticket,
                "Time at Cashier": customer.processing_time_cashier,
                "Time at Self-Service": customer.processing_time_self_checkout
            }

        with open("customer_data.json", "w") as json_file:
            json.dump(customer_data, json_file, indent=2
                      )


class ItemProcessing:
    @staticmethod
    def calculate_processing_time(basket_size):
        time_cashier = basket_size * 6
        time_self_checkout = basket_size * 4
        return time_cashier, time_self_checkout

    @staticmethod
    def award_lottery(customer):
        lottery_status = "hard luck, better luck next time!"
        if customer.basket_size > 10:
            customer.lottery_ticket = random.choice([True, False])
            if customer.lottery_ticket:
                lottery_status = "wins lottery"
        return lottery_status

    @staticmethod
    def display_customer_details(customer, lottery_status):
        if customer.lottery_ticket:
            lucky_customer_message = " ### Lucky customer ###"
        else:
            lucky_customer_message = ""

        print(f"{lucky_customer_message}\n"
              f"{customer.customer_id} —> items in basket: {customer.basket_size}, "
              f"{lottery_status}, \n"
              f"Time to process basket at cashier till: {customer.processing_time_cashier} Secs, \n"
              f"Time to process basket at self—service till: {customer.processing_time_self_checkout} Secs. \n")


class Simulation(Customer):
    def __init__(self, basket_size):
        super().__init__(basket_size)
        self.simulation_time = None
        self.opening_time = datetime.strptime('07:00:00', '%H:%M:%S')
        self.closing_time = datetime.strptime('23:00:00', '%H:%M:%S')

    def initialize_customers(self):
        initial_customers = []
        for i in range(random.randint(1, 10)):
            customer = Customer.create_customer()
            initial_customers.append(customer)

        # Display the initial set of customers + increment the time by 30 minutes
        print("## Customer Details ##")
        for customer in initial_customers:
            processing_time_cashier, processing_time_self_checkout = ItemProcessing.calculate_processing_time(
                customer.basket_size)
            customer.processing_time_cashier = processing_time_cashier
            customer.processing_time_self_checkout = processing_time_self_checkout
            lottery_status = ItemProcessing.award_lottery(customer)
            ItemProcessing.display_customer_details(customer, lottery_status)


    def initialize_simulation(self):
        self.simulation_time = self.opening_time
        print(f"Simulation started at {self.simulation_time.strftime('%H:%M')}")
        self.initialize_customers()
        self.simulation_time += timedelta(minutes=30)

    def main_loop(self):
        simulation_interval = 5
        end_simulation = False

        while self.simulation_time.time() < self.closing_time.time() and not end_simulation:
            user_input = input("Enter anything to end the simulation: ")
            if user_input:
                end_simulation = True
            else:
                simulation_time = self.simulation_time
                print(f"Current Time: {simulation_time.strftime('%H:%M')}")

            # Generate a random number of customers (up to 10) every 30 seconds
            num_customers = random.randint(1, 10)
            for i in range(num_customers):
                customer = Customer.create_customer()
                processing_time_cashier, processing_time_self_checkout = ItemProcessing.calculate_processing_time(
                    customer.basket_size)

                customer.processing_time_cashier = processing_time_cashier
                customer.processing_time_self_checkout = processing_time_self_checkout

                lottery_status = ItemProcessing.award_lottery(customer)
                ItemProcessing.display_customer_details(customer, lottery_status)

                Customer.save_customer_dict_to_json()


            # Move time forward in the simulation
            self.simulation_time += timedelta(minutes=30)

            # Simulate real-time passage (sleep for 30 seconds)
            time.sleep(simulation_interval)

if __name__ == "__main__":
    simulation = Simulation(0)
    simulation.initialize_simulation()
    simulation.main_loop()