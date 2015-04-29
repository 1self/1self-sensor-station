import time
from modules32 import htu21d

def get_humidity_percent(sensor):
    humidity_percent = sensor.get_rel_humidity()
    return humidity_percent

def get_temperature(sensor):
    temperature = sensor.get_temp()
    return temperature

## App run
print ("Getting sensor reading from HTU21D")

SENSOR = htu21d.HTU21D()
SENSOR.reset()

for x in range(10):
    humidity_percent = get_humidity_percent(SENSOR)
    print (x, "Current humidity %", humidity_percent)

    temperature = get_temperature(SENSOR)
    print (x, "Current temperature C", temperature)

    print ("----------------------")
    time.sleep(10)
    
