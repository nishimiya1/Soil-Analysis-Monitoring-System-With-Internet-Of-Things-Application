# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import RPi.GPIO as GPIO
import time
import board
import adafruit_dht
import pyrebase
import serial

moisture_sensor_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture_sensor_pin, GPIO.IN)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()
#def read_moisture_sensor():
 # moisture_sensor_value = 0
  # Read moisture sensor value multiple times and take the average
  #for i in range(10):
   # moisture_sensor_value += GPIO.input(moisture_sensor_pin)
  #moisture_sensor_value = moisture_sensor_value / 10
  #return moisture_sensor_value
while True:
    try:
        #moisture_sensor_value = read_moisture_sensor()
        #moisture_percent = moisture_sensor_value * 100
        # Print the values to the serial port
        #line = ser.readline().decode('utf-8').rstrip()
        soiltemp = sensor.get_temperature()
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% Soil Temperature: {}%  ".format(
                temperature_f, temperature_c, humidity,soiltemp
            )
        )
        data = {
        "Temperature" : temperature_c,
        "Humidity" : humidity,
        "Soil Temperature" : soiltemp,
       # "Soil Moisture" : moisture_percent
        
        }
        db.child("Status").push(data)

        db.update(data)
        print("Sent to Firebase")

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

