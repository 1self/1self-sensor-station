import sys
import time
from modules27.lib_1self import lib_1self
from modules27.lib_si1145 import SI1145

ENV_VARS = {}

global STREAM

def get_set_env_vars():
    lines = None
    with open('/home/pi/Desktop/Programming/1self-sensor-station/.env') as f:
        lines = f.readlines()

    for line in range(len(lines)):
        param = lines[line].strip()
        args = param.split('=')
        ENV_VARS[args[0]] = args[1]        

def create_geofence():
    return 'ibeacon://' + ENV_VARS['IBEACON_UUID'] + '/' + ENV_VARS['IBEACON_MAJOR'] + '/' + ENV_VARS['IBEACON_MINOR']

def get_IR_lux(sensor, obj_1self):

    IR_lux = sensor.readIRLight()
    current_time = obj_1self.get_localtime_isoformat()

    print ("Current IR (Lux)", IR_lux, current_time)
    
    sensor_item = {}
    sensor_item["object_tags"] = ["ambient", "infrared"]
    sensor_item["action_tags"] = ["sample"]
    sensor_item["properties"] = {"lux": IR_lux}
    sensor_item["reading_time"] = current_time
    return sensor_item

def get_vis_lux(sensor, obj_1self):

    vis_lux = sensor.readAmbientLight()
    current_time = obj_1self.get_localtime_isoformat()

    print ("Current visible light (Lux)", vis_lux, current_time)
    
    sensor_item = {}
    sensor_item["object_tags"] = ["ambient", "visible-light"]
    sensor_item["action_tags"] = ["sample"]
    sensor_item["properties"] = {"lux": vis_lux}
    sensor_item["reading_time"] = current_time
    return sensor_item

def get_UV_index(sensor, obj_1self):

    UV_index = float(sensor.readUVIndex())/100
    current_time = obj_1self.get_localtime_isoformat()

    print ("Current UV index", UV_index, current_time)
    
    sensor_item = {}
    sensor_item["object_tags"] = ["ambient", "ultraviolet"]
    sensor_item["action_tags"] = ["sample"]
    sensor_item["properties"] = {"ultraviolet-index": UV_index}
    sensor_item["reading_time"] = current_time
    return sensor_item

def do_send_to_1self(obj_1self, geofence):

    print("sending pending data to 1self")

    send_error = False
    counter = 0
    while len(SENSOR_DATA) > 0 and send_error == False:
        sensor_item = SENSOR_DATA[0]
        object_tags = sensor_item["object_tags"]
        action_tags = sensor_item["action_tags"]
        properties = sensor_item["properties"]
        event_time = sensor_item["reading_time"]

        event = obj_1self.create_1self_event(object_tags, action_tags, properties, event_time, geofence)
        
        response, error_text, status_code = obj_1self.send_to_1self(event)

        print ("streamid:", obj_1self.stream_id())

        if status_code == 200:
            counter = counter + 1
            print (counter, "- sent event to 1self")
            SENSOR_DATA.pop(0)
        else:
            print ("Error", error_text, status_code)
            send_error = True

def do_capture(sensor, obj_1self):    
    try:
        IR_item = get_IR_lux(sensor, obj_1self)
        SENSOR_DATA.append(IR_item)
    except Exception as err:
        print ("failed to get IR reading", err)

    try:
        vis_item = get_vis_lux(sensor, obj_1self)
        SENSOR_DATA.append(vis_item)
    except Exception as err:
        print ("failed to get visible light reading", err)

    try: 
        UV_item = get_UV_index(sensor, obj_1self)
        SENSOR_DATA.append(UV_item)
    except Exception as err:
        print ("failed to get UV reading", err)

    print ("Pending sensor readings count:", len(SENSOR_DATA))

## App run
get_set_env_vars()

SLEEP_FOR = 600

print ("Writing events to ", ENV_VARS['API_URL'])

SENSOR = SI1145()

GEOFENCE = create_geofence()

OBJ_1SELF = lib_1self(ENV_VARS['APP_NAME'], ENV_VARS['APP_VERSION'], ENV_VARS['API_URL'], ENV_VARS['APP_ID'], ENV_VARS['APP_SECRET'])

SENSOR_DATA = []

while 1 == 1:
    do_capture(SENSOR, OBJ_1SELF)

    do_send_to_1self(OBJ_1SELF, GEOFENCE)
    
    print ("Now sleeping for", SLEEP_FOR, "seconds")
    sys.stdout.flush()
    time.sleep(SLEEP_FOR)
