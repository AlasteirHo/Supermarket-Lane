import random
import json

class Customer:
    RandomNum: int
    def __init__(self):
        self.Items = None
        self.CustomerUI = None
        self.NumberOfItems = 0
        self.ProcessTime = 0
        self.UniqueIdentifier = ""
        self.CustomerDict = {}
        self.NewCustomer = {}
    def random_generator(self):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.RandomNum = random.randint(0,30)
        CustomerLetter = random.choice(letters)
        CustomerNumber = random.choice(numbers)
        self.CustomerUI = CustomerLetter + str(CustomerNumber)
        self.Items = random.randint(1,30)

        return self.RandomNum, self.CustomerUI, self.Items


    def createCustomerDict(self):
        for i in range(1,20):
            self.random_generator()
            NumOfCustomer = f"Customer{i}"
            self.NewCustomer = {
                    "UniqueIdentifier": self.CustomerUI,
                    "Items": self.Items,
                    "ProcessTime": self.Items * 4
            }
            self.CustomerDict[NumOfCustomer] = self.NewCustomer
        self.writeCustomerDict()
        return self.CustomerDict
    def writeCustomerDict(self):
        with open("StoringData/Customers.json", "w") as f:
            f.write(json.dumps(self.CustomerDict,indent=2))

    def processingtime(self):
        # #N = Number of items
        # #T = Fixed time
        # calc = n * t
        for key in self.CustomerDict.keys():
            print(key)

    def get_customerDict(self):
        return self.CustomerDict

# my_dict = {'key1': 'value1', 'key2': 'value2'}
#
# # Add a new key-value pair
# my_dict['key3'] = 'value3'
#
# print(my_dict)

# Customer1 = Customer()
# Customer1.processingtime()
# Customer1.createCustomerDict()
