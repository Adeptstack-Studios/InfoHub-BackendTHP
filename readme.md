# InfoHub-Backend for sensors
#### for Raspberry Pi with the following sensors: DHT22 and BMP280.

## Installation
Clone the GitHub repository in `/home/pi/`:
```
git clone https://github.com/Adeptstack-Studios/InfoHub-Backend
```

If git is not installed, you can install it this way:
```
sudo apt-get update
sudo apt-get install git
```

Once this is done, navigate to the cloned repository:
```
cd /home/pi/InfoHub-Backend
```

The repository contains the installation script, which installs all the necessary applications and libraries when you run it.
```
bash installation.sh
```

The script also informs you that you need to activate the SPI interface on the Raspberry Pi, as this is required by one of the sensors.
You can activate this under `Interface Options` in `raspi-config`.
```
sudo raspi-config
```

However, before the server is started, you create a new screen in which the server then runs. This is done so that the server continues to run even after the ssh session has ended.
```
screen -SO InfoHub
```

Once this has been done and all sensors have been connected correctly, you can put the sensor module into operation. You will find the `start.sh` script file in the repository that you need to execute to start it.
```
bash start.sh
```
And now everything should work :)

## Documentation
The API can usually be accessed as follows:
```
localhost:5000/GetCurrentValues
```

The API returns a json string that is structured like this:
```json
{"temperature": 20.8, "humidity": 49.4, "pressure": 980, "altitude": 342.63}
```

The values are given in the following units:
```
temperature: °C
humidity: %
pressure: hPa
altitude: m
```

## Libraries
The following libraries are used:
```
- flask
- gunicorn
- pigpio-dht
- adafruit-circuitpython-bmp280
- adafruit-circuitpython-lis3dh
```