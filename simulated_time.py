import json
import random
import time


class Customer:
    Customer_Dict = {}
    current_customer_id = 1

    def __init__(self, basket_size):
        self.customer_id = f"C{Customer.current_customer_id}"
        self.customer_num = f"Customer {Customer.current_customer_id}"
        Customer.current_customer_id += 1

        self.basket_size = basket_size
        self.processing_time_cashier = 0
        self.processing_time_self_checkout = 0
        self.lottery_ticket = False
        self.shopping_method = None

    def calculate_processing_time(self):
        raise NotImplementedError("This method should be overridden in a subclass")

    def award_lottery(self):
        if self.basket_size >= 10:
            self.lottery_ticket = random.choice([True, False])

    def display_customer_details(self):
        if self.lottery_ticket:
            lottery_status = "wins a lottery ticket"
        else:
            lottery_status = "hard luck, no lottery ticket this time!"

        print(f"{self.customer_id} -> items in basket: {self.basket_size}, {lottery_status},\n "
              f"time to process basket at cashier till: {self.processing_time_cashier} Secs,\n "
              f"time to process basket at self—service till: {self.processing_time_self_checkout} Secs \n")

    @staticmethod
    def create_customer():
        basket_size = random.randint(1, 30)
        if basket_size > 10:
            customer = TrolleyCustomer(basket_size)
        else:
            customer = BasketCustomer(basket_size)
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
                "Time at Self-Service": customer.processing_time_self_checkout,
                "Shopping Method": customer.shopping_method
            }

        with open("customer_data.json", "w") as json_file:
            json.dump(customer_data, json_file, indent=4)


class BasketCustomer(Customer):
    def __init__(self, basket_size):
        super().__init__(basket_size)
        self.processing_time_cashier = self.basket_size * 4
        self.processing_time_self_checkout = self.basket_size * 6
        self.shopping_method = "Basket"
        self.award_lottery()


class TrolleyCustomer(Customer):
    def __init__(self, basket_size):
        super().__init__(basket_size)
        self.processing_time_cashier = self.basket_size * 4
        self.processing_time_self_checkout = self.basket_size * 6
        self.shopping_method = "Trolley"
        self.award_lottery()


def main_loop():
    def create_initial_customers():
        initial_customers = []
        for i in range(random.randint(1, 10)):
            customer = Customer.create_customer()
            initial_customers.append(customer)
        return initial_customers

    def display_initial_customers(initial_customers):
        print("## Customer Details ##")
        for customer in initial_customers:
            customer.display_customer_details()

    initial_customers = create_initial_customers()
    display_initial_customers(initial_customers)

    while True:
        customer = Customer.create_customer()
        customer.display_customer_details()

        # Save customer data to JSON
        Customer.save_customer_dict_to_json()
        time.sleep(5)  # Pause for 5 seconds


# Create and display initial customers

if __name__ == "__main__":
    main_loop()
