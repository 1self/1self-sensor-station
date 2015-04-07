from datetime import datetime
import requests, json
import os
import time
import sys
from modules import testimport

APP_NAME = "1self-sensor-station"
APP_VERSION = "0.1"

API_URL = os.getenv('API_URL')
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
IBEACON_UUID = os.getenv('IBEACON_UUID')
IBEACON_MAJOR = os.getenv('IBEACON_MAJOR')
IBEACON_MINOR = os.getenv('IBEACON_MINOR')

global STREAM

def create_geofence():
    return 'ibeacon://' + IBEACON_UUID + '/' + IBEACON_MAJOR + '/' + IBEACON_MINOR

def create_humidity_event(humidity_value, geofence):
    event = {}
    event['source'] = APP_NAME
    event['version'] = APP_VERSION
    event['objectTags'] = ["ambient", "humidity"]
    event['actionTags'] = ["sample"]
    event['geofence'] = geofence
    event['dateTime'] = datetime.utcnow().isoformat()
    event['properties'] = {"humidity-percent": humidity_value}
    return event

def create_temperature_event(temperature, geofence):
    event = {}
    event['source'] = APP_NAME
    event['version'] = APP_VERSION
    event['objectTags'] = ["ambient", "temperature"]
    event['actionTags'] = ["sample"]
    event['dateTime'] = datetime.utcnow().isoformat()
    event['properties'] = {"celsius": temperature}
    return event

def send_event(event, stream):
    url = API_URL + "/streams/" + stream['streamid'] + "/events"
    headers = {"Authorization": stream['writeToken'], "Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(event), headers=headers)
    try:
        response = json.loads(r.text)
        return response, r.status_code
    except ValueError:
        return r.text, r.status_code

def send_events(stream, humidity_percent, temperature, geofence):

    return_values = {}
    
    #send humidity event
    try:
        humidity_event = create_humidity_event(humidity_percent, geofence)
        
        response, status_code = send_event(humidity_event, stream)

        return_values["humidity_event"] = status_code

    except:
        return_values["humidity_event"] = 401
    
    #send temperature event
    try:
        temperature_event = create_temperature_event(temperature, geofence)
        
        response, status_code = send_event(temperature_event, stream)

        return_values["temperature_event"] = status_code

    except:
        return_values["temperature_event"] = 401

    return return_values

def get_new_stream():
    url = API_URL + "/streams"
    app_id = APP_ID
    app_secret = APP_SECRET
    auth_string = app_id + ":" + app_secret
    headers = {"Authorization": auth_string, "Content-Type": "application/json"}
    body = ""
    r = requests.post(url, headers=headers, data=body)
    response = json.loads(r.text)
    return response

def get_humidity_percent():
    return 12

def get_temperature():
    return 22

def do_capture_and_send(stream2):

    if len(stream2.items()) == 0:
        stream2 = get_new_stream()
##        print ('new stream')
##        print (stream2)

    humidity_percent = get_humidity_percent()
    temperature = get_temperature()
    geofence = create_geofence()
    
    return_values = send_events(stream2, humidity_percent, temperature, geofence)
##    print ('events sent to 1self')
    print (return_values)
    return stream2

## App run
STREAM = {}
testy = testimport.testimport()
print (testy.returntest())
sys.stdout.flush()

for i in range(3):
    STREAM = do_capture_and_send(STREAM)
    sys.stdout.flush()
    time.sleep(3)
