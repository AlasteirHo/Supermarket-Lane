import time
import random
import tkinter as tk
from tkinter import messagebox
from Run import Simulation
from CustomerItemProcessor import Customer


class SimulatorGUI:
    def __init__(self):
        self.gui = None
        self.start_time = 0  # Added start_time attribute
        self.simulation = Simulation()  # Create an instance of the Simulation class

    def interface(self):
        # Buttons

        gui = tk.Tk()
        gui.title("Simulation Interface")

        window_width = 625
        gui.geometry(f"{window_width}x50")

        start_button = tk.Button(gui, text="Start Simulation", command=self.start_simulation)
        start_button.grid(row=1, column=0, padx=10, pady=10)

        display_button = tk.Button(gui, text="Display Customer Details", command=self.display)
        display_button.grid(row=1, column=1, padx=10, pady=10)

        stop_button = tk.Button(gui, text="Stop Simulation", command=self.stop_button)
        stop_button.grid(row=1, column=2, padx=10, pady=10)

        exit_button = tk.Button(gui, text="Exit", command=exit)
        exit_button.grid(row=1, column=3, padx=10, pady=10)

        self.gui = gui

    def start_simulation(self):
        self.start_time = time.time()
        self.clear_customer_data() # Clears the dictionary as well as the JSON file before starting a new simulation
        self.simulation.initialize_simulation()
        self.spawn_customers()

    def spawn_customers(self): # Whilst the simulation is running, run the main loop in the Run file
        if self.simulation.is_running:
            self.simulation.main_loop()
            interval = random.randint(1,5) # Creates customers at a random interval between 1 and 5 seconds
            self.gui.after(1000 * interval, self.spawn_customers)

    def display(self):
        self.simulation.display_cus_details()

    def stop_button(self):  # Pause simulation when clicked and display's elapsed time
        elapsed_time = time.time() - self.start_time
        print(f"Total Elapsed Time: {elapsed_time:.2f} seconds")
        self.simulation.stop_simulation()
        messagebox.showinfo("Simulation Stopped", "Simulation has been stopped.") # Informs user

    @staticmethod
    def clear_customer_data(): # Clears the customer_dict and json file whenc
        Customer.customer_dict = {}
        Customer.current_customer_id = 1
        with open("StoringData/customer_data.json", "w") as f:
            f.write("{}")
        messagebox.showinfo("Restart Simulation", "Simulation has reset.")


if __name__ == "__main__":
    simulator = SimulatorGUI()
    simulator.interface()
    tk.mainloop()
