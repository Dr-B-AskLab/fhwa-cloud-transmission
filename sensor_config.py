import tkinter as tk

class SensorConfig:
    def __init__(self, window):
        self.window = window
        self.sensor_types = []
        self.sample_rates = []
        self.node_addresses = []

        self.port_frame = tk.Frame(self.window)
        self.port_frame.pack()
        self.port_label = tk.Label(self.port_frame, text="Please enter the COM PORT # for the Wireless Base:", font=("Helvetica", 16))
        self.port_label.pack(side="left")
        self.port_entry = tk.Entry(self.port_frame, font=("Helvetica", 16))
        self.port_entry.pack(side="left")
        self.error_label = tk.Label(self.port_frame, text="", fg="red", font=("Helvetica", 16))
        self.error_label.pack(side="left")

        self.add_sensor_frame = tk.Frame(self.window)
        self.add_sensor_frame.pack()
        self.add_sensor_button = tk.Button(text="Add Sensor", command=self.add_sensor, font=("Helvetica", 16))
        self.add_sensor_button.pack(side="left")

        self.collect_button = tk.Button(text="Start Collecting", command=self.start_collecting, font=("Helvetica", 16))

    def show(self):
        self.collect_button.pack(anchor='s')
        self.add_sensor()

    def add_sensor(self):
        self.collect_button.pack_forget()

        sensor_frame = tk.Frame(self.window)
        sensor_frame.pack(anchor='n')

        sensor_type_var = tk.StringVar(self.window)
        sensor_type_var.set("Acceleration")
        self.sensor_types.append(sensor_type_var)
        sensor_type_menu = tk.OptionMenu(sensor_frame, sensor_type_var, "Acceleration", "Displacement", "Strain")
        sensor_type_menu.configure(font=("Helvetica", 16))
        sensor_type_menu.pack(side="left")

        sample_rate_label = tk.Label(sensor_frame, text="Sample Rate (Hz): ", font=("Helvetica", 16))
        sample_rate_label.pack(side="left")

        sample_rate_entry = tk.Entry(sensor_frame, font=("Helvetica", 16))
        sample_rate_entry.pack(side="left")
        self.sample_rates.append(sample_rate_entry)

        node_address_label = tk.Label(sensor_frame, text="Node Address: ", font=("Helvetica", 16))
        node_address_label.pack(side="left")

        node_address_entry = tk.Entry(sensor_frame, font=("Helvetica", 16))
        node_address_entry.pack(side="left")
        self.node_addresses.append(node_address_entry)

        self.collect_button.pack(anchor='s')

    def start_collecting(self):
        com_port = self.port_entry.get()

        if com_port.isdigit() and 1 <= int(com_port) <= 99:
            valid_entries = True

            for sample_rate_entry in self.sample_rates:
                if not sample_rate_entry.get().isdigit():
                    self.error_label.config(text="Please enter a valid Sample Rate")
                    valid_entries = False
            for node_address_entry in self.node_addresses:
                if not node_address_entry.get().isdigit():
                    self.error_label.config(text="Please enter a valid Sample Rate")
                    valid_entries = False

            if valid_entries:
                self.com_port_selected = com_port
                self.sensor_types_values = [sensor_type_var.get() for sensor_type_var in self.sensor_types]
                self.sample_rates_values = [sample_rate_entry.get() for sample_rate_entry in self.sample_rates]
                self.node_addresses_values = [node_address_entry.get() for node_address_entry in self.node_addresses]
                self.window.destroy()
        else:
            self.error_label.config(text="Please enter a valid COM PORT #")

    def get_sensor_config(self):
        return self.com_port_selected, self.sensor_types_values, self.sample_rates_values, self.node_addresses_values