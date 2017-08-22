"""
Author: Javier López Martínez
Email: javier.lopez@beeva.com
Date: Aug 2017
Licensed by Apache 2.0
"""
from locust import Locust, TaskSet, task, events
from locust.stats import RequestStats
import paho.mqtt.client as mqtt
import json
import ssl
import random
import string
import time
import random
import jwt
import datetime

def noop(*arg, **kwargs):
    print ("Stats reset prevented by monkey patch!")
RequestStats.reset_all = noop
class MyTaskSet(TaskSet):
    def on_start(self):
        """
        Method executed only at the beginning of each client
        :return:
        """
        self.mqtt_client = mqtt.Client(client_id='projects/[project id]/locations/[location]/registries/[device resgitry id]/devices/[devide name]')
        self.mqtt_client.on_publish = self.on_publish
    	# self.mqtt_client.on_connect = self.on_connect
        # self.mqtt_client.on_disconnect = self.on_disconnect
        # self.mqtt_client.on_log = self.on_log

        self.mqtt_client.username_pw_set(username='unused', 
			password=create_jwt('[project id]','./ec_private.pem','ES256'))
	"""
        Download roots.pem file from Google Web Authority page.
        """		
        self.mqtt_client.tls_set("./roots.pem")
        self.mqtt_client.connect_async("mqtt.googleapis.com", 8883, 60)
        self.mqtt_client.loop_start()
        time.sleep(2)

    @task
    def publish(self):
        """
        Publishing  via mqtt in Google Cloud
        :return:
        """
        self.start_time = time.time()
        measure = self.generate_message()
        err, mid = self.mqtt_client.publish('/devices/[device id]/events', payload=measure, qos=1)
        if err:
            events.request_failure.fire(
                        request_type='MQTT',
                        name='1' + str(err),
                        response_time=0,
                        exception='1')

    def generate_message(self):
        """
        Generates message to send in mqtt
        :return: str
        """
        payload = {"measure": random.uniform(1,20)}
        # print("[THING {}]".format(payload))
        return json.dumps(payload)
    """
    def on_connect(self, client, userdata, flags, rc):
        print "CONNECTED"
        print rc
    def on_disconnect(self, client, userdata, rc):
        print "DISCONNECTED"
        print client
    def on_log(self, client, userdata, level, buf):
        print "LOG"
        print buf
    """
    def on_publish(self, client, userdata, mid):
        """
        Waits to receive confirmation with qos 1 that a message has been delivered to the broker
        :param client:
        :param userdata:
        :param mid:
        :return:
        """
        events.request_success.fire(
            request_type='MQTT',
            name='prueba',
            response_time=int(time.time() - self.start_time) * 1000,
            response_length=len("a1"))

class MyLocust(Locust):
    task_set = MyTaskSet
    min_wait = 100
    max_wait = 100

def create_jwt(project_id, private_key_file, algorithm):
    """Create a JWT (https://jwt.io) to establish an MQTT connection."""
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
      private_key = f.read()
    # print ('Creating JWT using {} from private key file {}'.format(algorithm, private_key_file))
    return jwt.encode(token, private_key, algorithm=algorithm)

