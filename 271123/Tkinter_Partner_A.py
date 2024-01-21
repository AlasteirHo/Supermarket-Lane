import tkinter as tk
import json
from Lane import Lanes
from CashierLanes import CashierLanes
from SelfCheckoutLanes import SelfCheckout

# Creating global instances of each class to be used as the gui.
lane = Lanes()
cashier_lanes = CashierLanes()
self_checkout = SelfCheckout()
class SimulatorGUI:
    is_running = False
    @staticmethod
    def prerequisites():
        # Functions are called to create lanes.
        lane.create_lane("cashier")
        lane.create_lane("self_checkout")
        self_checkout.create_self_checkout_file()
        cashier_lanes.create_cashier_file()
    def main(self):
        self.is_running = True
        if self.is_running:
            print("Starting Lane Simulation...")
            self.prerequisites()
            print("Files have been created.")
            self_checkout_total = lane.self_checkout_customer_total()
            cashier_total = lane.cashier_customer_total()
            total_customers = self_checkout_total + cashier_total
            if total_customers == 40:
                print("Lane saturation")
            else:
                self_checkout.main()
                cashier_lanes.main()

    @staticmethod
    def delete_json_contents(file_path):
        try:
            with open(file_path, 'w') as json_file:
                # Write an empty dictionary to clear the contents
                json.dump({}, json_file, indent=2)
            print(f"Contents of {file_path} deleted successfully.")
        except Exception as e:
            print(f"Error deleting contents of {file_path}: {e}")

    def stop_simulation(self):
        self.is_running = False
        lane.create_lane("cashier")
        lane.create_lane("self_checkout")

        self.delete_json_contents("StoringData/CashierData/Cashier.json")
        self.delete_json_contents("StoringData/SelfCheckoutData/SelfCheckout.json")

    def interface(self):
        gui = tk.Tk()
        gui.title("Simulation Interface")

        button1 = tk.Button(gui, text="Run Simulation", command=self.main)
        button1.pack()

        button2 = tk.Button(gui, text="Stop Simulation", command=self.stop_simulation)
        button2.pack()

        button3 = tk.Button(gui, text="Display Lane Status", command=lane.display_lane_status)
        button3.pack()

        button4 = tk.Button(gui, text="Exit Simulation", command=exit)
        button4.pack()
        tk.mainloop()

Sim = SimulatorGUI()
# Sim.main()
Sim.interface()
# Sim.prerequisites()
# Sim.stop_simulation()