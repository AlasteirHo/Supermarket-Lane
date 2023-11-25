import random
import time

# Dictionary to store customer information
customer_dict = {}

# Customer class + Data stored within the customer class
class Customer:
    def __init__(self, CustomerID, basket_size):
        self.CustomerID = CustomerID
        self.basket_size = basket_size
        self.lottery_ticket = False

# Constants for cashier/self-checkout processing time per item
cashier_processing_time = 4
self_processing_time = 6
# Constant for starting customerID
CustomerID = 1

# Generate a random number of items in a basket between 1 and 30
    def basket_size_randomizer():
        return random.randint(1, 30)

# Function to randomly award a lottery ticket to a customer who has more than or equal to 10 items in their basket
    def award_lottery_ticket(customer):
        if customer.basket_size >= 10:
            customer.lottery_ticket = random.choice([True, False])

# Function to calculate the time needed to process a customer's basket


# Function to display customer details
    def display_customer_details(customer):
        basket_size = customer.basket_size


        if basket_size >=10:
        # Checks if the customer has a lottery ticket and prints the respective messages if they won a lottery ticket
            win_lottery = "wins a lottery ticket!" if customer.lottery_ticket else "hard luck, no lottery ticket this time!"
        else:
            win_lottery = "Less than 10 items, no ticket awarded"
        sctotal = customer.basket_size * self_processing_time
        cashiertotal = customer.basket_size * cashier_processing_time

        print(f"\nC{customer.CustomerID} —> items in basket: {basket_size}, {win_lottery}")
        print(f"Time to process basket at cashier till: {sctotal} Secs")
        print(f"Time to process basket at self service till: {cashiertotal} Secs")
        if customer.lottery_ticket:
            print("### Lucky customer ###")


# Adds a customer to the queue every 5 seconds
def customerSpawner():
    global CustomerID
    while True:
        # On final iteration replace with time.sleep(random.randint(1,5)
        time.sleep(5)
        new_customer = Customer(CustomerID, basket_size_randomizer())
        award_lottery_ticket(new_customer)
        customer_dict[CustomerID] = new_customer.__dict__  # Add customer to dictionary
        display_customer_details(new_customer)
        CustomerID += 1  # Increment the customer counter

        # print("Customers in dictionary:", customer_dict)  # Print the customers dictionary
# Spawns customers
customerSpawner()