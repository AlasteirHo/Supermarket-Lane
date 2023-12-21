# import json
# import asyncio
# import random
import json

# class Checkout:
#     def __init__(self):
#         # (Your existing initialization code)
#
#     async def process_items_async(self, customer_id, process_time):
#         await asyncio.sleep(process_time)
#         print(f"Customer {customer_id} time has been completed.")
#
#     async def process_cashier_customers(self):
#         customers_in_cashier = self.ExtractCustomerData()
#         tasks = []
#
#         for customer_id, customer_data in customers_in_cashier.items():
#             process_time = customer_data["Process Time"]
#             task = asyncio.create_task(self.process_items_async(customer_id, process_time))
#             tasks.append(task)
#
#         await asyncio.gather(*tasks)
#
#     def run_simulation(self):
#         # (Your existing simulation logic)
#
#         # Start the asynchronous processing of cashier customers
#         asyncio.run(self.process_cashier_customers())
#
#         # Continue with the rest of your simulation
#
#     def ExtractCustomerData(self):
#         pass
#
#
# # Example usage:
# checkout_instance = Checkout()
# checkout_instance.run_simulation()


def ExtractCustomerData():
    with open("StoringData/CashierLane.json", "r") as f:
        CustomersInCashier = json.load(f)
    return CustomersInCashier


def find_best_lane():
    data = ExtractCustomerData()

def find_least_customers_lane():
    data = ExtractCustomerData()
    min_customers = float('inf')
    min_lane = None

    for lane, info in data.items():
        if info['CustomersInLane'] < min_customers:
            min_customers = info['CustomersInLane']
            min_lane = lane

    print(min_lane)
    return min_lane

# Example data

# Call the function with your data
find_least_customers_lane()

# Print the result

