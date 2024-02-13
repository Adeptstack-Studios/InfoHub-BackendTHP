sudo pigpiod
cd /home/pi/InfoHub-BackendTHP
gunicorn app:app -w 3 --threads 2 -b 0.0.0.0:5000
