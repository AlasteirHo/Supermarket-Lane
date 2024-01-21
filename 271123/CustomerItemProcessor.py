import random
import json


class ItemProcessing:
    def __init__(self):
        # Define per item processing times for cashier and self-checkout
        self.cashier_checkout_time = 4
        self.self_checkout_time = 6

    @staticmethod
    def calculate_processing_time(basket_size, processing):
        # Calculate processing times for cashier and self-checkout based on basket size
        try:
            # Ensure basket_size is a valid integer between 1 and 30
            basket_size = int(basket_size)
            if basket_size < 1 or basket_size > 30:
                raise ValueError("Basket size must be between 1 and 30.")
        except ValueError as e:
            print(f"Error in calculate_processing_time: {e}")  # Error message if basket_size is out of range
            return None, None

        # Calculate processing times for both cashier and self-checkout
        time_cashier = basket_size * processing.cashier_checkout_time
        time_self_checkout = basket_size * processing.self_checkout_time
        return time_cashier, time_self_checkout

    @staticmethod
    def award_lottery(customer):
        # Determines if the customer wins a lottery ticket based on basket size
        try:
            # Error handling to ensure that basket_size is an integer between 1 and 30
            lottery_status = "hard luck, better luck next time!"
            basket_size = int(customer.basket_size)
            if 10 < basket_size <= 30:  # If a basket size is within range, it will randomly assign the customer a
                # ticket
                customer.lottery_ticket = random.choice([True, False])
                if customer.lottery_ticket:
                    lottery_status = "Lucky Winner!"
            return lottery_status
        except ValueError as e:
            print(f"Error awarding customer a lottery ticket: {e} ")
            return "Lottery status unable to assign due to invalid basket size"

    @staticmethod
    def display_customer_details(customer_dict):
        # Display details of each customer, by traversing through the customer dictionary
        for customer_id, customer in customer_dict.items():
            customer_key = "C" + str(customer.customer_id)
            if customer.lottery_ticket:  # If a customer has been awarded a ticket, a message will be printed
                print("### Lucky customer ###")
            print(
                f"{customer_key} —> items in basket: {customer.basket_size}, "
                f"{customer.lottery_status}, \n"
                f"Time to process basket at cashier till: {customer.processing_time_cashier} Secs, \n"
                f"Time to process basket at self—service till: {customer.processing_time_self_checkout} Secs. \n")


class Customer(ItemProcessing):
    # Global variables
    current_customer_id = 1  # Acts as a counter/pointer
    customer_dict = {}  # Creates a customer dictionary

    def __init__(self):
        super().__init__()
        # Initialize customer attributes
        self.customer_id = Customer.current_customer_id
        self.basket_size = self.basket_size_randomizer()
        self.processing_time_cashier, self.processing_time_self_checkout = self.calculate_processing_time(
            self.basket_size, ItemProcessing())
        self.lottery_ticket = False

    def create_customer(self):
        # Create a new customer, store in the Customer_Dict and JSON file, and increments current_customer_id
        customer = Customer()
        customer.lottery_status = ItemProcessing.award_lottery(customer)
        self.customer_dict[customer.customer_id] = customer  # Adds customer to dictionary
        Customer.current_customer_id += 1
        customer.save_customer_dict_to_json()
        return customer

    @staticmethod
    def basket_size_randomizer():
        # Generate a random basket size between 1 and 30
        return random.randint(1, 30)

    def save_customer_dict_to_json(self):
        # Save customer_dict into a JSON file
        customer_data = {}
        for customer_id, customer in Customer.customer_dict.items():
            customer_data["Customer" + str(customer.customer_id)] = {
                "customer_id": "C" + str(customer.customer_id),
                "basket_size": customer.basket_size,
                "lottery_ticket": customer.lottery_ticket,
                "time_at_cashier": customer.processing_time_cashier,
                "time_at_self_service": customer.processing_time_self_checkout,
            }

        with open("StoringData/customer_data.json", "w") as f:
            json.dump(customer_data, f, indent=2)

    @staticmethod
    def display_customer_dict():
        # Display details of each customer in the Customer_Dict(for demonstration purposes)
        for customer_id, customer in Customer.customer_dict.items():
            print(
                f"customer_id: {'C' + str(customer.customer_id)}, "
                f"basket_size: {customer.basket_size}, "
                f"lottery_ticket: {customer.lottery_ticket}, "
                f"time_at_cashier: {customer.processing_time_cashier}, "
                f"time_at_self_service: {customer.processing_time_self_checkout}\n"
            )


# Uncomment the following lines to test the code:
C1 = Customer()
C1.create_customer()
C1.display_customer_details(C1.customer_dict)
# Display's customer_dict for demonstration purposes(not required for functionality)
C1.display_customer_dict()
