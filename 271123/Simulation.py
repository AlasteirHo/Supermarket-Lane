import random
import time
from CustomerItemProcessor import Customer, ItemProcessing
from CashierLanes import CashierLanes
from Lane import Lanes
from SelfCheckoutLanes import SelfCheckout

lane = Lanes()
self_checkout = SelfCheckout()
cashier = CashierLanes()


class Simulation(Customer):
    def __init__(self):
        super().__init__()

    def start_simulation(self):
        num_customers = random.randint(1, 10)  # Randomly creates 1 to 10 customers
        print(f"Simulation started at: {time.strftime('%H:%M:%S')}\n")
        for i in range(num_customers):
            C1 = Customer.create_customer(self)
            ItemProcessing.display_customer_details({C1.customer_id: C1})

        lane.create_lane("cashier")
        lane.create_lane("self_checkout")

        # Once initialization steps are complete, run the main loop
        self.main_loop()

    def spawn_customers(self):
        time.sleep(random.randint(1, 5))  # Creates a customer at a random interval between 1 and 5 seconds
        Customer.create_customer(self)

    def main_loop(self):
        # start_time = time.time()
        while True:
            # elapsed_time = time.time() - start_time
            lane.create_lane("cashier")
            lane.create_lane("self_checkout")
            lane.sort_customer()

            self_checkout_total = lane.self_checkout_customer_total()
            cashier_total = lane.cashier_customer_total()
            self.spawn_customers()
            total_customers = self_checkout_total + cashier_total

            self_checkout.create_self_checkout_file()
            cashier.create_cashier_file()
            # ItemProcessing.display_customer_details({customer.customer_id: customer})
            if total_customers == 40:
                print("Lane Saturation")

            else:
                import Lane
                lane.display_lane_status()
                self_checkout.main()
                cashier.main()

            # Display details of the newly created customer (Add a new If/while loop to validate if a button is clicked)


if __name__ == "__main__":
    sim = Simulation()
    sim.start_simulation()
