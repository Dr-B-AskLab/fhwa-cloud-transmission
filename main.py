import tkinter as tk
from sensor_config import SensorConfig
from data_collection import start_data_collection

def main():
    window = tk.Tk()
    window.title("Sensor Configuration")
    sensor_config = SensorConfig(window)
    sensor_config.show()
    window.mainloop()
    
    com_port_selected, sensor_types_values, sample_rates_values, node_addresses_values = sensor_config.get_sensor_config()
    start_data_collection(com_port_selected, sensor_types_values, sample_rates_values, node_addresses_values)

if __name__ == '__main__':
    main()