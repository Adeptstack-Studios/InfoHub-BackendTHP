from flask import Flask, jsonify, request
from json import dumps
from pigpio_dht import DHT11, DHT22
import board
import busio
import adafruit_bmp280
import digitalio #Using SPI
import requests
import threading

app = Flask(__name__)

gpio = 4 # BCM Numbering
#sensor = DHT11(gpio)
sensordht = DHT22(gpio)

temperature = 0
humidity = 0
pressure = 0
altitude = 0

def repeated_timer(interval, function, *args, **kwargs):
    function(*args, **kwargs)
    threading.Timer(interval, repeated_timer, [interval, function] + list(args), kwargs).start()

def doTimer():
    temperature, humidity = getDHT22Values()
    pressure, altitude = getBMP280Values()
    print("Timer ausgeführt!")

def getDHT22Values():
    result = sensordht.sample(samples=1)
    temp = result["temp_c"]
    humidity = result["humidity"]
    return temp, humidity

def getBMP280Values():
    # API Call for current Sealevel Pressure values
    psea = 0
    api_url = "" # Your url for an api call to retrieve the sea level pressure
    response = requests.get(api_url)
    if response.status_code == 200:
        api_data = response.json()
        psea = api_data['current']['pressure_msl']
    else:
        print(f"Error during API call. Status code: {response.status_code}")

    # Read sensor data
    spi = board.SPI()
    bmp_cs = digitalio.DigitalInOut(board.D5)
    sensorbmp = adafruit_bmp280.Adafruit_BMP280_SPI(spi, bmp_cs)
    # This value must be changed to the current air pressure at your location
    # otherwise there will be inaccuracies
    # weather services can give you information
    # 1013.25 hPa is the mean air pressure at sea level
    sensorbmp.sea_level_pressure = psea
    # Output of the measured values
    pressure = round(sensorbmp.pressure, 1)
    altitude = round(sensorbmp.altitude, 2)
    return pressure, altitude

@app.route('/GetCurrentValues')
def send_json():
    jsondict = {"temperature": temperature, "humidity": humidity, "pressure": pressure, "altitude": altitude }

    data = dumps(jsondict)
    print("send")
    return data

# Beispiel: Wiederholender Timer, der alle 3 Sekunden eine Funktion ausführt
repeated_timer(3, doTimer)

if __name__ == '__main__':
    app.run()
