import Adafruit_DHT
import time
import RPi.GPIO as gpio
import board
import pyrebase
import serial
import pickle
import numpy as np
import joblib
import random
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
soiltemp = sensor.get_temperature()

# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
humidity, temp = Adafruit_DHT.read_retry(sensor1, gpio)
#moistRead = ser.readline().decode('utf-8').rstrip()

def sensorReadings():
    if humidity is not None and temp is not None:
        print(f'Temp={temp}  Humidity={humidity}')
    else:
        print('Failed to get reading. Try again!')
    print(f'Nitrogen: {nitrogen}, Phosphorus: {phos}, Potassium: {potassium}, Soil Moisture: {moistRead}, Soil Temp: {soiltemp:.2f}')
    data = {
         "Temperature" : temp,
         "Humidity" : humidity,
         "SoilTemperature" : soiltemp,
         "Nitrogen" : nitrogen,
         "Phosphorus" : phos,
         "Potassium" : potassium,
         "SoilMoisture" : moistRead
         
        
        }
    db.child("Status").push(data)

    db.update(data)
    print("Sent to Firebase")
    time.sleep(1)
def moistureTemp():
    regressor = joblib.load('/home/rasp/Downloads/soil_moisture_temperature_classifier.pkl')
    moistRead = ser.readline().decode().rstrip()
    moisture = moistRead
    soil_temp = soiltemp
    
    new_data = np.array([[moisture,soil_temp]])
    predicted_moisture = regressor.predict(new_data)
    
    if predicted_moisture == [0]:
        text_predict = 'Low Moisture/High Temperature'
    if predicted_moisture ==[1]:
        text_predict = 'Moderate Moisture/Moderate Temperature'
    if predicted_moisture == [2]:
        text_predict = 'High Moisture/Low Temperature'
   # print(f'Given Moisture [{moisture}]')
   # print (f'Given Temp [{soil_temp:.2f}]')
    print(f"Predicted: {predicted_moisture}", text_predict)
    data = {
        "predictmoisture" : text_predict
        }
    db.child("Status").push(data)
    db.update(data)
    time.sleep(2)
def npkReadings():
    pkl_file = '/home/rasp/Downloads/NPK_classifier.pkl'
   # nitrogen = ser.readline().decode().rstrip()
   # phos = ser.readline().decode('utf-8').rstrip()
   # potassium = ser.readline().decode('utf-8').rstrip()
    regressor = joblib.load('/home/rasp/Downloads/NPK_classifier.pkl')
    n = nitrogen
    p = phos
    k = potassium
    if n == '':
        n = 0
    if p == '':
        p = 0
    if k == '':
        k = 0

    new_data = np.array([[n,p,k]])

    predicted_moisture = regressor.predict(new_data)

    if predicted_moisture == [0]:
        text_predict = 'High Nutrients'
    if predicted_moisture == [1]:
        text_predict = 'Low Nutrients'

   # print(f'given nitrogen [{n}]')
   # print(f'given phos [{p}]')
   # print(f'given potassium [{k}]')
    print(f"Predicted soil nutrient level: {predicted_moisture}",text_predict)
    data = {
        "predictnutrients" : text_predict
        }
    db.child("Status").push(data)
    db.update(data)
    time.sleep(2)
while True:
    #soiltemp = sensor.get_temperature()
 #   print(" The temperature is %s celsius" % temperature)
    nitrogen = ser.readline().decode('utf-8').rstrip()
    phos = ser.readline().decode('utf-8').rstrip()
    potassium = ser.readline().decode('utf-8').rstrip()
    moistRead = ser.readline().decode('utf-8').rstrip()
# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.
    print(sensorReadings())
    print(moistureTemp())
    print(npkReadings())
