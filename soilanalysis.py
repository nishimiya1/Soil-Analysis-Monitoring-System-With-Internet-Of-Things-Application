import Adafruit_DHT
import time
import RPi.GPIO as gpio
import board
import pyrebase
import serial
import numpy as np
import joblib

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
soiltemp = sensor.get_temperature()
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor1 = Adafruit_DHT.DHT11

# Set GPIO sensor is connected to
gpio = 4
# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
humidity, temp = Adafruit_DHT.read_retry(sensor1, gpio)
n = ser.readline().decode('utf-8').rstrip()
p = ser.readline().decode('utf-8').rstrip()
k = ser.readline().decode('utf-8').rstrip()
moistRead = ser.readline().decode('utf-8').rstrip()
irrigation = ser.readline().decode('utf-8').rstrip()
def sensorReading():
    
    if humidity is not None and temp is not None:
        print('Temp={}  Humidity={}'.format(temp, humidity))
        time.sleep(2)
    print(f'Nitrogen: {n}, Phosphorus: {p}, Potassium: {k}, Soil Moisture: {moistRead}, Irrigation Status: {irrigation}, Soil Temp: {soiltemp:.2f}')
    data = {
         "Temperature" : temp,
         "Humidity" : humidity,
         "SoilTemperature" : soiltemp,
         "Nitrogen" : n,
         "Phosphorus" : p,
         "Potassium" : k,
         "SoilMoisture" : moistRead,
         "Irrigation" : irrigation
        
        }
    db.child("Status").push(data)

    db.update(data)
    print("Sent to Firebase")

    time.sleep(3)
def moistureTempReadings():
    regressor = ''
    soil_m = soiltemp
    soil_temp = soiltemp
    new_data = np.array([[soil_m, soil_temp]])
    predicted_moisture = regressor.predict(new_data)

    if predicted_moisture == [0]:
        text_predict = 'Low Moisture/High Temperature'
    if predicted_moisture == [1]:
        text_predict = 'Moderate Moisture/Moderate Temperature'
    if predicted_moisture == [2]:
        text_predict = 'High Moisture/Low Temperature'
    print(f'given soil moisture [{soil_m}]')
    print(f'given soil temperature [{soil_temp}]')
    print(f"Predicted: {predicted_moisture}",text_predict)
    time.sleep(3)

def npkReadings():
    regressor = ''
    new_data = np.array([[n,p,k]])
    predicted_moisture = regressor.predict(new_data)

    if predicted_moisture == [0]:
        text_predict = 'High Nutrients'
    if predicted_moisture == [1]:
        text_predict = 'Low Nutrients'
    print(f'given soil moisture [{moistRead}]')
    print(f'given soil temperature [{soiltemp}]')
    print(f"Predicted: {predicted_moisture}",text_predict)
    time.sleep(3)

while True:
    print(sensorReading())
    print(moistureTempReadings())
    print(npkReadings())
