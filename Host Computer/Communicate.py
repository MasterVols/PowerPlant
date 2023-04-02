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
from flask import Flask, render_template
# Define the Flask app
app = Flask(__name__)

# Set the port and baud rate for the serial connection
port = "/dev/ttyACM0"
baud_rate = 115200

# Open the serial connection
ser = serial.Serial(port, baud_rate)

# Define a function to read the sensor data
def read_data():
    # Send the "sensors" keyword over serial to the Arduino Mega Receiver
    ser.write(b'sensors\r\n')
    # Read the response from the Arduino Mega Receiver
    response = ser.readline().decode().rstrip()
    # Split the response into separate values
    values = response.split()
    # Return the values as a dictionary
    return {
        "humidity": values[0],
        "luminosity": values[1],
        "temperature_bottom": values[2],
        "temperature_middle": values[3],
        "temperature_surface": values[4],
        "v0": values[5],
        "v1": values[6],
        "v2": values[7],
        "v3": values[8],
        "v4": values[9],
        "v5": values[10]
    }
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
# Define the route for the webpage
from flask import Response, stream_with_context

@app.route('/')
def index():
    def generate():
        while True:
            # Read the sensor data
            data = read_data()
            # Create a new data log file if necessary
            if not hasattr(app, "log_file") or app.log_file.closed:
                app.log_file = create_log_file()
            # Write the data to the log file
            app.log_file.write("{}\t{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\t".join(data.values())))
            app.log_file.flush()
            # Yield the template with the data
            yield render_template("index.html", **data)
            # Wait for 5 seconds before generating the next response
            time.sleep(5)
    return Response(stream_with_context(generate()))


@app.route("/data")
def data():
    # Read the sensor data
    data = read_data()
<<<<<<< HEAD
    # Create a new data log file if necessary
    if not hasattr(app, "log_file") or app.log_file.closed:
        app.log_file = create_log_file()
    # Write the data to the log file
    app.log_file.write("{}\t{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\t".join(data.values())))
    app.log_file.flush()
    # Render the template with the data
    return render_template("index.html", **data)
=======
    # Return the data as a JSON response
    return jsonify(data)

>>>>>>> 042cb28baedaf36524dad1d0c1ad2884e8803b0a
# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)