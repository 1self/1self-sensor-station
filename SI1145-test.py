import time
from modules27.lib_si1145 import SI1145

def get_IR_lux(sensor):
    IR_lux = sensor.readIRLight()
    return IR_lux

def get_vis_lux(sensor):
    vis_lux = sensor.readAmbientLight()
    return vis_lux

def get_UV_index(sensor):
    UV_index = float(sensor.readUVIndex())/100
    return UV_index

## App run
print "Getting sensor reading from SI1145"

SENSOR = SI1145()

for x in range(10):
    IR_lux = get_IR_lux(SENSOR)
    print x, "Current IR (Lux)", IR_lux

    vis_lux = get_vis_lux(SENSOR)
    print x, "Current visible light (Lux)", vis_lux

    UV_index = get_UV_index(SENSOR)
    print x, "Current UV index", UV_index
    
    print "----------------------"
    time.sleep(10)
