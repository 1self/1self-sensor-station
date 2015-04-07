from datetime import datetime
import requests, json
import os

APP_NAME = "1self-sensor-station"
APP_VERSION = "0.1"

API_URL = os.getenv('API_URL')
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
IBEACON_UUID = os.getenv('IBEACON_UUID')
IBEACON_MAJOR = os.getenv('IBEACON_MAJOR')
IBEACON_MINOR = os.getenv('IBEACON_MINOR')

print (API_URL)

global STREAM

def create_geofence():
    return 'ibeacon://' + IBEACON_UUID + '/' + IBEACON_MAJOR + '/' + IBEACON_MINOR

def create_humidity_event(humidity_value, geofence):
    event = {}
    event['source'] = APP_NAME
    event['version'] = APP_VERSION
    event['objectTags'] = ["ambient", "humidity"]
    event['actionTags'] = ["sample"]
    event['dateTime'] = datetime.utcnow().isoformat()
    event['properties'] = {"humidity-percent": humidity_value, "geofence": geofence}
    return event

def send_event(event, stream):
    url = API_URL + "/streams/" + stream['streamid'] + "/events"
    print (url)
    headers = {"Authorization": stream['writeToken'], "Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(event), headers=headers)
    try:
        response = json.loads(r.text)
        return response, r.status_code
    except ValueError:
        return r.text, r.status_code

def send_events(stream, humidity_value, geofence):
    try:
        #send humidity event
        humidity_event = create_humidity_event(humidity_value, geofence)
        print (humidity_event)
        response, status_code = send_event(humidity_event, stream)
        print (status_code)

    except:
        return 401

    return 200

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

def do_capture_and_send(stream2):

    if len(stream2.items()) == 0:
        stream2 = get_new_stream()
        print ('new stream')
        print (stream2)
        
    return_value = send_events(stream2, 14, create_geofence())
    print ('events sent to 1self')
    print (return_value)
    return stream2

## App run
STREAM = {}
for i in range(2):
    STREAM = do_capture_and_send(STREAM)
