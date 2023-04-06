# fhwa-cloud-transmission

Set-Up Instructions

1. This repo makes use of the MicroStrain Communication Library. This Python package is only available pre-built for Python versions 2.7 and 3.6. This repo uses the version prebuilt for Python 3.6. It is possible to compile the library yourself for a different version of Python if you would like to, but to run the repo as is you will need a Python 3.6 installation. You can install Python 3.6 here: https://www.python.org/downloads/release/python-360/
2. The code in this repo continuously collects data from a sensor network and transmits it to the AWS DynamoDB database service. To establish a connection with this service, you need to create an AWS account: https://aws.amazon.com/. The free tier of AWS provides 25GB of DynamoDB storage, so there is no need to pay for anything.
3. Navigate to the DynamoDB service in the AWS client and create a table to be used. The code assumes that you use the table name data, but if you choose to use a different name you can just change the value for TABLE_NAME at the top of the data_collection.py file.
4. You need to retrieve your AWS keys: https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html
5. The code is written assuming that you save the AWS keys as environment variables called AWS_ACCESS_KEY and AWS_SECRET_KEY. Another option is to edit where they are initialized at the top of the data_collection.py file and hardcode them in. 
6. To start the program run the main.py file using Python 3.6. The program will run indefinitely, if you are running the program in the terminal, you can interrupt the program with Ctrl+C. 

Structure

1. The main.py file is the point of execution and passes data from the code that handles the user configuration (sensor_config.py) to the code that handles the sensor network (data_collection.py). The main.py file first passes control to the sensor_config.py file.
2. The sensor_config.py file runs a small UI component to collect the information needed to bring up the sensor network. This includes the com port for the base station, the sample rates, and the node addresses. When the start collecting button is pressed, the UI component is destroyed and control is passed back to the main.py file. The returned values for the configuration are then passed to the data_collection.py file.
3. The data_collection.py file establishes a connection with AWS, starts the sampling network with the specifications made in the UI, begins collecting data from the network, and both pushes the data to DynamoDB and records the data locally in a csv file. 

