import time
import sys
from modules32.lib_1self import lib_1self
from modules32 import htu21d

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

def get_humidity_percent(sensor, obj_1self):

    humidity_percent = sensor.get_rel_humidity()
    current_time = obj_1self.get_localtime_isoformat()

    print ("Current humidity %", humidity_percent, current_time)
    
    sensor_item = {}
    sensor_item["object_tags"] = ["ambient", "humidity"]
    sensor_item["action_tags"] = ["sample"]
    sensor_item["properties"] = {"humidity-percent": humidity_percent}
    sensor_item["reading_time"] = current_time
    return sensor_item

def get_temperature(sensor, obj_1self):

    temperature = sensor.get_temp()
    current_time = obj_1self.get_localtime_isoformat()

    print ("Current temperature C", temperature, current_time)
    
    sensor_item = {}
    sensor_item["object_tags"] = ["ambient", "temperature"]
    sensor_item["action_tags"] = ["sample"]
    sensor_item["properties"] = {"celsius": temperature}
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
        humidity_item = get_humidity_percent(sensor, obj_1self)
        SENSOR_DATA.append(humidity_item)
    except Exception as err:
        print ("failed to get humidity reading", err)

    try: 
        temperature_item = get_temperature(sensor, obj_1self)
        SENSOR_DATA.append(temperature_item)
    except Exception as err:
        print ("failed to get temperature reading", err)

    print ("Pending sensor readings count:", len(SENSOR_DATA))

## App run
get_set_env_vars()

print ("Writing events to ", ENV_VARS['API_URL'])

SENSOR = htu21d.HTU21D()
SENSOR.reset()

GEOFENCE = create_geofence()

OBJ_1SELF = lib_1self(ENV_VARS['APP_NAME'], ENV_VARS['APP_VERSION'], ENV_VARS['API_URL'], ENV_VARS['APP_ID'], ENV_VARS['APP_SECRET'])

SENSOR_DATA = []

while 1 == 1:
    do_capture(SENSOR, OBJ_1SELF)

    do_send_to_1self(OBJ_1SELF, GEOFENCE)
    
    print ("Now sleeping for 1200 seconds")
    sys.stdout.flush()
    time.sleep(1200)
