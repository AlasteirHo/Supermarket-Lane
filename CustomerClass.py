import random
import json

class Customer:
    def __init__(self):
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
        self.Items = random.randint(0,30)

        return self.RandomNum, self.CustomerUI, self.Items


    def createCustomerDict(self):
        for i in range(1,11): #This part will be replaced with something in the future to automate the process.
            self.random_generator()
            NumOfCustomer = f"Customer{i}"
            self.NewCustomer = {
                    "UniqueIdentifier": self.CustomerUI,
                    "Items": self.Items,
                    "ProcessTime": self.Items * 4
            }
            self.CustomerDict[NumOfCustomer] = self.NewCustomer
        print(self.CustomerDict)
        self.writeCustomerDict()

    def writeCustomerDict(self):
        with open("Customers.txt", "w") as f:
            f.write(json.dumps(self.CustomerDict,indent=2))

