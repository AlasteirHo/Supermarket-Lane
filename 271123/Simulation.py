from CustomerItemProcessor import Customer, ItemProcessing
import random
import time


class Simulation:
    @staticmethod
    def start_simulation():
        num_customers = random.randint(1, 10)

        for i in range(num_customers):
            C1 = Customer.create_customer()
            ItemProcessing.display_customer_details({C1.customer_id: C1})
        Simulation.main_loop()

    @staticmethod
    def main_loop():
        while True:
            time.sleep(random.uniform(1, 5))
            customer = Customer.create_customer()

            # Display details of the newly created customer
            ItemProcessing.display_customer_details({customer.customer_id: customer})


if __name__ == "__main__":
    sim = Simulation()
    sim.start_simulation()
    # Uncomment the line below if you want the main loop to run continuously
    sim.main_loop()
