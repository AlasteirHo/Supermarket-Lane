from CheckoutClass import Checkout
import json
import random

#A  random number between 1 and 10 customers need to join the checkout lane at the beginning of the simulation.
#self.LaneMax = 25
#for self service theres 1 lane of 8 tills = 7 people can be queuing at one time if all 8 tills are open and has customers
# Customers made -> Lane1 -> Is Lane1 Full? -> Open new lane ELSE Put customer in Lane1 -> Process Customer -> Output lane status? -> Remove Customer from lane
class Lane(Checkout):
    def __init__(self):
        self.laneNumber = 1
        self.ServiceLane = 1 #This can hold 8 different lanes
        self.Queue = []
        super().__init__()

    def extract_ordered_customers(self):
        with open("StoringData/OrderedCustomers.json", "r") as f:
            data = json.load(f)
        return data

    # def get_data(self):
    #     a = self.extract_ordered_customers()
    #     print(a)

    def create_first_lane(self):
        customers = self.extract_ordered_customers()
        customer_keys = list(customers.keys())
        # print(random.sample(customer_keys,9))


    def add_lane_to_dict(self):
        pass




b = Lane()
b.create_first_lane()
print("Testing")






