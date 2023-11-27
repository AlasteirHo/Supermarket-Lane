from CheckoutClass import Checkout
import json

# Customers made -> Lane1 -> Is Lane1 Full? -> Open new lane ELSE Put customer in Lane1 -> Process Customer -> Output lane status? -> Remove Customer from lane
class Lane(Checkout):
    def __init__(self):
        super().__init__()

    def extract_ordered_customers(self):
        with open("StoringData/OrderedCustomers.json", "r") as f:
            data = json.load(f)
        return data


    def get_data(self):
        a = self.extract_ordered_customers()
        print(a)

b = Lane()
b.get_data()






