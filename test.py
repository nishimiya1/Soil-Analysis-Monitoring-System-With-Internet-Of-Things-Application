import Adafruit_DHT
import time
import RPi.GPIO as gpio
import board
import pyrebase
import serial
config = {
  "apiKey": "GLYZ3rfUD8H3xUxO9KcN34s1rTZ55JOtgE0FETSU",
  "authDomain": "iot-soil-moisure-monitoring.firebaseapp.com",
  "databaseURL": "https://iot-soil-moisure-monitoring-default-rtdb.firebaseio.com/",
  "storageBucket": "iot-soil-moisure-monitoring.appspot.com"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0',9600, timeout = 1)
    ser.flush()

from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor1 = Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
gpio = 4

# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
humidity, temp = Adafruit_DHT.read_retry(sensor1, gpio)

while True:
    soiltemp = sensor.get_temperature()
 #   print(" The temperature is %s celsius" % temperature)
    n = ser.readline().decode('utf-8').rstrip()
    p = ser.readline().decode('utf-8').rstrip()
    k = ser.readline().decode('utf-8').rstrip()
    moisture = ser.readline().decode('utf-8').rstrip()
    irrigation = ser.readline().decode('utf-8').rstrip()
# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.
    if humidity is not None and temp is not None:
        print('Temp={0:0.1f}  Humidity={1:0.1f}'.format(temp, humidity))
        time.sleep(2)
   # else:
   #     print('Failed to get reading. Try again!')
        
    print(f'Nitrogen: {n}, Phosphorus: {p}, Potassium: {k}, Soil Moisture: {moisture}, Irrigation Status: {irrigation}, Soil Temp: {soiltemp:.2f}')
    data = {
         "Temperature" : temp,
         "Humidity" : humidity,
         "SoilTemperature" : soiltemp,
         "Nitrogen" : n,
         "Phosphorus" : p,
         "Potassium" : k,
         "SoilMoisture" : moisture,
         "Irrigation" : irrigation
        
        }
    db.child("Status").push(data)

    db.update(data)
    print("Sent to Firebase")
        