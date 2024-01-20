from flask import Flask, jsonify, request
from json import dumps
from pigpio_dht import DHT11, DHT22
import board
import busio
import adafruit_bmp280
import digitalio #Using SPI
import requests

app = Flask(__name__)

def getDHT22Values():
    gpio = 4 # BCM Numbering
    #sensor = DHT11(gpio)
    sensor = DHT22(gpio)
    result = sensor.sample(samples=1)
    temp = result["temp_c"]
    humidity = result["humidity"]
    print(f"temperature: {temp}°C")
    print(f"humidity: {humidity}%")
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
    sensor = adafruit_bmp280.Adafruit_BMP280_SPI(spi, bmp_cs)
    # This value must be changed to the current air pressure at your location
    # otherwise there will be inaccuracies
    # weather services can give you information
    # 1013.25 hPa is the mean air pressure at sea level
    sensor.sea_level_pressure = psea
    # Output of the measured values
    print("\nTemperatur: %0.1f *C" % sensor.temperature)
    print("Luftdruck: %0.1f hPa" % sensor.pressure)
    print("Hoehe: %0.2f m" % sensor.altitude)
    pressure = round(sensor.temperature, 1)
    altitude = round(sensor.altitude, 2)
    return pressure, altitude

@app.route('/GetCurrentValues')
def send_json():
    temperature, humidity = getDHT22Values()
    pressure, altitude = getBMP280Values()
    json = {"temperature": temperature, "humidity": humidity, "pressure": pressure, "altitude": altitude }

    data = json.dumps(json)
    return data


if __name__ == '__main__':
    app.run()
