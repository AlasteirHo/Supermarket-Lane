import random
import json

class ItemProcessing:
    # Constants for processing times
    cashier_checkout_time = 4
    self_checkout_time = 6

    @staticmethod
    def calculate_processing_time(basket_size):
        time_cashier = basket_size * ItemProcessing.cashier_checkout_time
        time_self_checkout = basket_size * ItemProcessing.self_checkout_time
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
            lucky_customer_message = "### Lucky customer ###"
        else:
            lucky_customer_message = ""

        print(
            f"{lucky_customer_message}\n"
            f"{customer.customer_id} —> items in basket: {customer.basket_size}, "
            f"{lottery_status}, \n"
            f"Time to process basket at cashier till: {customer.processing_time_cashier} Secs, \n"
            f"Time to process basket at self—service till: {customer.processing_time_self_checkout} Secs. \n"
        )

class Customer(ItemProcessing):
    Customer_Dict = {}
    current_customer_id = 0

    def __init__(self):
        super().__init__()
        self.customer_id: str = f"C{Customer.current_customer_id}"
        Customer.current_customer_id += 1
        self.basket_size = self.basket_size_randomizer()
        self.processing_time_cashier, self.processing_time_self_checkout = self.calculate_processing_time(self.basket_size)
        self.lottery_ticket = False

    def basket_size_randomizer(self):
        return random.randint(1, 30)

    @staticmethod
    def create_customer():
        customer = Customer()
        customer.basket_size_randomizer()
        customer.award_lottery(customer)
        Customer.Customer_Dict[customer.customer_id] = customer
        return customer

    @staticmethod
    def save_customer_dict_to_json():
        customer_data = {}
        for customer_id, customer in Customer.Customer_Dict.items():
            customer_data[customer.customer_id] = {
                "customer_id": customer.customer_id,
                "basket_size": customer.basket_size,
                "lottery_ticket": customer.lottery_ticket,
                "time_at_cashier": customer.processing_time_cashier,
                "time_at_self_service": customer.processing_time_self_checkout,
            }

        with open("StoringData/customer_data.json", "w") as json_file:
            json.dump(customer_data, json_file, indent=2)

    @staticmethod
    def display_customer_dict():
        for customer_id, customer in Customer.Customer_Dict.items():
            print(
                f"CustomerID: {customer.customer_id}, "
                f"Basket_Size: {customer.basket_size}, "
                f"Lottery_Ticket: {customer.lottery_ticket}, "
                f"Time at Cashier: {customer.processing_time_cashier}, "
                f"Time at Self-Service: {customer.processing_time_self_checkout}"
            )

C1 = Customer()
C1.create_customer()
C1.save_customer_dict_to_json()
C1.display_customer_dict()