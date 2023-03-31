#Sensor Data Logger
This program reads sensor data from an Arduino Mega Receiver and logs it into a file. It also displays the sensor data on a webpage using Flask.

##Requirements
*Python 3.x
*Flask
*An Arduino Mega Receiver
##Usage
*Connect the Arduino Mega Receiver to the computer via USB.
*Find the port of the Arduino Mega Receiver. On Linux, this is usually /dev/ttyACM0. On Windows, this is usually COM3 or similar.
*Clone or download this repository to your computer.
*Install Flask by running pip install flask in the terminal.
*Create a directory called sensor_data in the same directory as the Python file.
*Run the Python file by running python app.py in the terminal.
*Open a web browser and go to http://localhost:5000 to see the sensor data.
##Customization
*You can change the port of the Arduino Mega Receiver by modifying the port variable in the Python file.
*You can change the baud rate of the Arduino Mega Receiver by modifying the baud_rate variable in the Python file.
*You can change the format of the log file name by modifying the strftime format string in the create_log_file function.
*You can change the format of the timestamp in the log file by modifying the strftime format string in the index function.