
import RPi.GPIO as GPIO
import time
import board
import adafruit_dht
import pyrebase
import serial
import csv
config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "storageBucket": ""
}

with open('soil_data_day1_no_fert.csv', 'w', new):
  writer.writerow(['time', 
                   'nitrogen', 
                   'phosphorus', 
                   'potassium', 
                   'soil_m', 
                   'temp', 
                   'soil_temp', 
                   'humidity', 
                   'irrigation'])

firebase = pyrebase.initialize_app(config)

db = firebase.database()


dhtDevice = adafruit_dht.DHT11(board.D4)

gfg
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0',9600, timeout =1)
    ser.flush()
t0 = time.time()    
while True:
    n = ser.readline().decode('utf-8').rstrip()
    p = ser.readline().decode('utf-8').rstrip()
    k = ser.readline().decode('utf-8').rstrip()
    moisture = ser.readline().decode('utf-8').rstrip()
    irrigation = ser.readline().decode('utf-8').rstrip()
    try:
        soiltemp = sensor.get_temperature()
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% Soil Temperature: {} C Nitrogen: {} ppm/kg Phosphorus: {} ppm/kg Potassium: {} ppm/kg Soil Moisture: {} % Irrigation Status: {} ".format(
                temperature_f, temperature_c,humidity,soiltemp, n,p,k,moisture,irrigation
            )
        )
       
        data = {
         "Temperature" : temperature_c,
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
        
        if round(time.time()-t0, 1) % 60 == 0:
          print(f'hello record na akooo! time: {time.time()-t0}')
          with open('soil_data_day1_no_fert.csv', 'w', new):
            writer.writerows([((time.time()-t0)/60), 
                              n, 
                              p,
                              k, 
                              moisture, 
                              temperature_c, 
                              soiltemp,
                              humidity, 
                              irrigation])  

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

