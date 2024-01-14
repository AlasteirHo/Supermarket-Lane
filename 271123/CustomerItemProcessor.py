import random
import json

class Customer:
    Customer_Dict = {}
    current_customer_id = 0

    def __init__(self, basket_size):
        self.customer_id: str = f"C{Customer.current_customer_id}"
        self.customer_num: str = f"Customer {Customer.current_customer_id}"
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
                "Customer_num": customer.customer_num,
                "Basket Size": customer.basket_size,
                "Lottery Ticket": customer.lottery_ticket,
                "Time at Cashier": customer.processing_time_cashier,
                "Time at Self-Service": customer.processing_time_self_checkout
            }

        with open("customer_data.json", "w") as json_file:
            json.dump(customer_data, json_file, indent=2)

    # @staticmethod
    # def display_customer_dict():
    # for customer_id, customer in Customer.Customer_Dict.items():
    # print(f"CustomerID: {customer.customer_id}, "
    # f"Customer_num: {customer.customer_num}, "
    # f"Basket Size: {customer.basket_size}, "
    # f"Lottery Ticket: {customer.lottery_ticket}, "
    # f"Time at Cashier: {customer.processing_time_cashier}, "
    # f"Time at Self-Service: {customer.processing_time_self_checkout}")


class ItemProcessing:
    # Constants for processing times
    CASHIER_PROCESSING_TIME = 4
    SELF_CHECKOUT_PROCESSING_TIME = 6

    @staticmethod
    def calculate_processing_time(basket_size):
        time_cashier = basket_size * ItemProcessing.CASHIER_PROCESSING_TIME
        time_self_checkout = basket_size * ItemProcessing.SELF_CHECKOUT_PROCESSING_TIME
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
