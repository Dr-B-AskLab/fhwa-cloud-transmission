import mscl
import csv
import boto3
import tkinter as tk
import os
from sample_rate_mapping import sample_rate_mapping

def start_data_collection(com_port_selected, sensor_types_values, sample_rates_values, node_addresses_values):
    
    ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

    # Table name in DynamoDB
    TABLE_NAME = 'data'

    # Establishes a connection with DynamoDB
    dynamodb = boto3.client('dynamodb', region_name = 'us-east-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    # The COM port of the base station indicated in the configuration window
    COM_PORT = "COM" + str(com_port_selected)

    window = tk.Tk()
    window.title("Data Collection")
    frame = tk.Frame(window)
    frame.pack()

    # Establish connection to the COM port
    connection = mscl.Connection.Serial(COM_PORT)

    global baseStation
    # Initialize base station
    baseStation = mscl.BaseStation(connection)

    def startup():
        global loop
        loop = 0

        if not baseStation.ping():
            print("Failed to ping the Base Station")

        if baseStation.ping():
            print("Pinged Base Station")

        print("Attempting to enable the beacon...")
        startTime = baseStation.enableBeacon()

        print("Successfully enabled the beacon on the Base Station")
        print("Beacon's initial Timestamp: " + str(startTime))
        print("Beacon is active")
        label = tk.Label(window, text="Successfully enabled the beacon on the Base Station", font=("Helvetica", 16))
        label.pack(side="top")
        label = tk.Label(window, text="Beacon's initial Timestamp: " + str(startTime), font=("Helvetica", 16))
        label.pack(side="top")
        label = tk.Label(window, text="Beacon is active", font=("Helvetica", 16))
        label.pack(side="top")

        def setCurrentConfig(node, sample_rate):

            config = mscl.WirelessNodeConfig()

            config.defaultMode(mscl.WirelessTypes.defaultMode_idle)
            config.inactivityTimeout(7200)
            config.samplingMode(mscl.WirelessTypes.samplingMode_sync)
            sample_rate = sample_rate_mapping(sample_rate)
            if sample_rate is not None:
                config.sampleRate(sample_rate)
            config.unlimitedDuration(True)
            try:
                node.applyConfig(config)
            except Exception:
                print("Failed to apply new configuration settings.")
            print("Set configuration settings.")

        global nodes
        nodes = []
        for node_address in node_addresses_values:
            nodes.append(mscl.WirelessNode(int(node_address), baseStation))

        network = mscl.SyncSamplingNetwork(baseStation)

        for node in nodes: 
            if not node.ping():
                print("Failed to ping the Node: " + str(node.nodeAddress()))

            if node.ping():
                print("Pinged Node: " + str(node.nodeAddress()))

        for i in range(len(nodes)):
            setCurrentConfig(nodes[i], sample_rates_values[i])

        for node in nodes:
            try:
                network.addNode(node)
            except Exception:
                for node in nodes:
                    try:
                        node.setToIdle()
                    except Exception:
                        pass
                for node in node_addresses_values:
                    try:
                        baseStation.node_hardReset(node)
                    except Exception:
                        pass
                baseStation.disableBeacon()
                print("Error while adding nodes! Restarting...")
                startup()
        print("Added nodes to the network.")

        network.applyConfiguration()
        network.startSampling()

    startup()

    def sweep_task():
        nonEmptyNodes = []

        sweeps = baseStation.getData()

        items = []

        def writeData(nodeAddress, timestamp, dataPoint, counter):
            
            if str(nodeAddress) not in nonEmptyNodes:
                counter+=1
                nonEmptyNodes.append(str(nodeAddress))

            # data structure
            items.append(    {
                'id': {'N': str(nodeAddress)},
                'timestamp': {'S': str(timestamp)},
                'data': {'N': str(dataPoint)}
            })

            # write data to CSV file
            with open('data.csv', mode='a') as csv_file:
                fieldnames = ['nodeAddress', 'timestamp', 'dataPoint']
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                if csv_file.tell() == 0:
                    csv_writer.writeheader()

                csv_writer.writerow({
                    'nodeAddress': nodeAddress,
                    'timestamp': timestamp,
                    'dataPoint': dataPoint
                })
            return counter

        counter = 0
        for sweep in sweeps:
            nodeAddress = sweep.nodeAddress()
            timestamp = sweep.timestamp()
            dataPoint = sweep.data()[0].as_string()
            print(nodeAddress, timestamp, dataPoint)
            counter = writeData(nodeAddress, timestamp, dataPoint, counter)

        for item in items:
            response = dynamodb.put_item(TableName = TABLE_NAME, Item= item)

        global loop
        loop += 1
        
        # check that the nodes for which data is being ingested matches the nodes in the network
        if(counter != len(nodes) and loop > 3):
            print("Node Diconnected!")
            for node in nodes:
                try:
                    node.setToIdle()
                except Exception:
                    pass
            for node in node_addresses_values:
                try:
                    baseStation.node_hardReset(node)
                except Exception:
                    pass
            baseStation.disableBeacon()
            print("Restarting...")
            startup()
        
        window.after(1000, sweep_task)
        
    window.after(1000, sweep_task)
    window.mainloop()