import paho.mqtt.client as mqtt
import json
import time
import subprocess

client = mqtt.Client()

client.connect("core-mosquitto", 1883)

def publish():
    while True:
        stats = subprocess.getoutput("chronyc tracking")
        payload = {"chrony": stats}

        client.publish("gpsntp/status", json.dumps(payload))

        time.sleep(5)

publish()
