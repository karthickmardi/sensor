import eventlet
import requests
from st2reactor.sensor.base import Sensor


class PyroIncidentSensor(Sensor):
    def __init__(self, sensor_service,config):
        super(PyroIncidentSensor, self).__init__(sensor_service=sensor_service,config=None)
        self._stop = False

    def setup(self):
        pass
    def run(self):
        while not self._stop:
                # Create the payload for the trigger
            service_now_url = 'https:///api/now/table/incident?sysparm_query=short_descriptionLIKEserver is down&sysparm_query=assignment_group=182a2c44d7211100158ba6859e6103a4'
            username = ''
            password = '@'
            headers = {'Content-Type': 'application/json','Accept':'application/json'}
            response = requests.get(service_now_url, headers=headers,auth=(username, password))
            if response.status_code == 200:
                incidents = response.json().get('result', [])
                for incident in incidents:
                    sys_id = incident.get('sys_id', '')
                    description = incident.get('description', '')
                    short_description = incident.get('short_description', '')
                    payload = {'sys_id': sys_id,'description': description,'short_description': short_description}
                    self.sensor_service.dispatch(trigger='pyro_alert.restart', payload=payload)
            else:
                self.sensor_service.log.error(f"Failed to retrieve incidents. Status code: {response.status_code}")

            eventlet.sleep(60)
    def get_base64_credentials(self):
        credentials = f"{self.username}:{self.password}"
        return self.sensor_service.get_value('secret', credentials)

    def cleanup(self):
        self._stop = True

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass
    def remove_trigger(self, trigger):
        pass
                                        
