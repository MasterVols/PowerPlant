#   Matthew L Bringle
#   This file should expect the data in the following format:
#   Humidity Luminosity Temperature_Bottom Temperature_Middle Temperature_Surface V0 V1 V2 V3 V4 V5
#   All this data is retrieved from sending the command "sensors" over serial at 115200 BAUD (Arduino Mega Receiver)
#   
#
#   What this program should do:
#       Check for an available com port that is the Arduino Mega Receiver
#       Create a serial connection at 115200 BAUD
#       Check at a variable rate the value of all sensors by sending the "sensors" keyword
#       Show all data on a webpage hosted by the computer. You can assume the host computer that this is going to run on is a RPI 3B
#       Log all data into a folder called "sensor_data". Each file in that folder should be named the date and the hour span that is was recorded on. A new file should be created every hour.
import serial
import datetime
import os
import time

# Set the port and baud rate for the serial connection
port = "/dev/ttyACM0"
baud_rate = 115200

# Open the serial connection
ser = serial.Serial(port, baud_rate)

# Define a function to read the sensor data
def read_data():
    # Send the "sensors" keyword over serial to the Arduino Mega Receiver
    ser.write(b'sensors\r\n')

    # Wait for 5 second before reading again
    time.sleep(5)

    # Check if there is any data available in the input buffer
    if ser.in_waiting > 0:
        # Read the response from the Arduino Mega Receiver
        response = ser.readline().decode().rstrip()
        # Split the response into separate values
        values = response.split()
        # Return the values as a dictionary
        return {
            "Humidity": values[0],
            "Luminosity": values[1],
            "Temperature_Bottom": values[2],
            "Temperature_Middle": values[3],
            "Temperature_Surface": values[4],
            "V0": values[5],
            "V1": values[6],
            "V2": values[7],
            "V3": values[8],
            "V4": values[9],
            "V5": values[10]
        }
    else:
        # Return an empty dictionary if there is no data available
        return {}

# Define a function to create a new data log file
def create_log_file():
    # Get the current date and time
    now = datetime.datetime.now()
    # Create a new file with the date and hour span in the name
    filename = now.strftime("sensor_data/%Y-%m-%d_%H-%M-%S.txt")
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # Return the file object
    return open(filename, "w")

# Create a new data log file
log_file = create_log_file()

# Continuously read and store sensor data
while True:
    # Read the sensor data
    sensor_data = read_data()
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    
    # Write the sensor data to the log file
    log_file.write(f"{timestamp} {str(sensor_data)}\n")
    # Flush the buffer to ensure that the data is written immediately
    log_file.flush()
    # Print the sensor data and timestamp to the terminal
    print(f"{timestamp} {sensor_data}")
    
    print(sensor_data)
    # Wait for 1 second before reading again
    #time.sleep(1)
