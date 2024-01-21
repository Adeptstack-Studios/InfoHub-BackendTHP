sudo apt-get update && 
sudo apt-get install python3-pip && 
sudo apt-get install git && 
sudo pip3 install flask && 
sudo pip3 install pigpio-dht && 
sudo pip3 install gunicorn && 
sudo pip3 install adafruit-circuitpython-bmp280 && 
sudo pip3 install adafruit-circuitpython-lis3dh
sudo pigpiod

sudo mv InfoHubAutoStart /etc/init.d
sudo chmod 755 /etc/init.d/InfoHubAutoStart
sudo update-rc.d InfoHubAutoStart defaults

echo
echo don\'t forget to activate spi interface!
echo
