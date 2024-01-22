import tkinter as tk
import time
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

        title_length = len(gui.title())
        window_width = 200 + title_length * 10
        gui.geometry(f"{window_width}x400")

        start_button = tk.Button(gui, text="Start Simulation", command=self.start_simulation)
        start_button.grid(row=1, column=0, padx=10, pady=10)

        display_button = tk.Button(gui, text="Display Customer Details", command=self.display)
        display_button.grid(row=1, column=1, padx=10, pady=10)

        stop_button = tk.Button(gui, text="Stop Simulation", command=self.stop_button)
        stop_button.grid(row=1, column=2, padx=10, pady=10)

        exit_button = tk.Button(gui, text="Exit", command=self.exit_button)
        exit_button.grid(row=1, column=3, padx=10, pady=10)

        self.gui = gui

    def start_simulation(self):
        self.start_time = time.time()
        self.clear_customer_data()
        self.simulation.initialize_simulation()
        self.spawn_customers()

    def spawn_customers(self):
        if self.simulation.is_running:
            self.simulation.run_sim()
            self.gui.after(1000, self.spawn_customers)

    def display(self):
        self.simulation.display_cus_details()

    def stop_button(self):
        elapsed_time = time.time() - self.start_time
        print(f"Total Elapsed Time: {elapsed_time:.2f} seconds")
        self.simulation.stop_simulation()
        messagebox.showinfo("Simulation Stopped", "Simulation has been stopped.")

    def exit_button(self):
        self.gui.destroy()

    @staticmethod
    def clear_customer_data():
        Customer.customer_dict = {}
        Customer.current_customer_id = 1
        with open("StoringData/customer_data.json", "w") as f:
            f.write("{}")
        messagebox.showinfo("Restart Simulation", "Simulation has reset.")



simulator = SimulatorGUI()
simulator.interface()
tk.mainloop()
