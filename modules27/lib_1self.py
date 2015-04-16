from datetime import datetime
import requests, json

class lib_1self:

    # Private vars
    app_name = None
    app_version = None
    api_url = None
    app_id = None
    app_secret = None
    stream = None

    # Constructor
    def __init__(self, app_name, app_version, api_url, app_id, app_secret):
       self.app_name = app_name
       self.app_version = app_version
       self.api_url = api_url
       self.app_id = app_id
       self.app_secret = app_secret

    def get_localtime_isoformat(self):
        now = datetime.now()
        utcnow = datetime.utcnow()
        diff = now - utcnow
        hh,mm = divmod((diff.days * 24 * 60 * 60 + diff.seconds + 30) // 60, 60)
        return "%s%+03d:%02d" % (now.isoformat(), hh, mm)

    def stream_id(self):
        if self.stream is not None:
            streamid = self.stream['streamid']
            return streamid
        else:
            return None

    def create_1self_event(self, object_tag_list, action_tag_list, properties_dict, local_event_time_ISO, geofence = None):
        event = {}
        event['source'] = self.app_name
        event['version'] = self.app_version
        event['objectTags'] = object_tag_list
        event['actionTags'] = action_tag_list
        event['dateTime'] = local_event_time_ISO
        event['properties'] = properties_dict
        if geofence is not None:
            event['geofence'] = geofence
        return event

    def send_to_1self(self, _1self_event):
        status_code = 200
        error_text = "OK"
        
        if self.stream is None:
            self.stream, error_text, status_code = self.get_new_stream()

        if status_code == 200 and self.stream is not None:
            url = self.api_url + "/streams/" + self.stream['streamid'] + "/events"
            headers = {"Authorization": self.stream['writeToken'], "Content-Type": "application/json"}
            try:
                r = requests.post(url, data=json.dumps(_1self_event), headers=headers)
                try:
                    response = json.loads(r.text)
                    return response, "OK", r.status_code
                except ValueError:
                    return None, r.text, r.status_code
            except Exception as err:
                return None, err, 500
        else:
            return None, error_text, status_code 

    def get_new_stream(self):
        
        url = self.api_url + "/streams"
        app_id = self.app_id
        app_secret = self.app_secret
        auth_string = app_id + ":" + app_secret
        headers = {"Authorization": auth_string, "Content-Type": "application/json"}
        body = ""
        try:
            r = requests.post(url, headers=headers, data=body)
            try:
                response = json.loads(r.text)
                return response, "OK", r.status_code
            except ValueError:
                return None, r.text, r.status_code
        except Exception as err:
            return None, err, 500

