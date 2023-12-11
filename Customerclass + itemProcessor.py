import json
import random
import time


class Customer:
    Customer_Dict = {}
    current_customer_id = 1

    def __init__(self, basket_size):
        self.customer_id = f"C{Customer.current_customer_id}"
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
            customer_data[customer_id] = {
                "Basket Size": customer.basket_size,
                "Lottery Ticket": customer.lottery_ticket,
                "Time at Cashier": customer.processing_time_cashier,
                "Time at Self-Service": customer.processing_time_self_checkout
            }

        with open("customer_data.json", "w") as json_file:
            json.dump(customer_data, json_file, indent=4)


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


# Create a random number of customers (between 1 and 10) at the start
initial_customers = []
for i in range(random.randint(1, 10)):
    customer = Customer.create_customer()
    initial_customers.append(customer)

# Display the initial set of customers
print("## Customer Details ##")
for customer in initial_customers:
    processing_time_cashier, processing_time_self_checkout = ItemProcessing.calculate_processing_time(
        customer.basket_size)
    customer.processing_time_cashier = processing_time_cashier
    customer.processing_time_self_checkout = processing_time_self_checkout
    lottery_status = ItemProcessing.award_lottery(customer)
    ItemProcessing.display_customer_details(customer, lottery_status)


# Loop to generate customers and add them to the customer_dict every 2 seconds
def main_loop():
    while True:
        customer = Customer.create_customer()

        processing_time_cashier, processing_time_self_checkout = ItemProcessing.calculate_processing_time(
            customer.basket_size)

        customer.processing_time_cashier = processing_time_cashier
        customer.processing_time_self_checkout = processing_time_self_checkout

        lottery_status = ItemProcessing.award_lottery(customer)
        ItemProcessing.display_customer_details(customer, lottery_status)

        Customer.save_customer_dict_to_json()

        time.sleep(2)


if __name__ == "__main__":
    main_loop()
