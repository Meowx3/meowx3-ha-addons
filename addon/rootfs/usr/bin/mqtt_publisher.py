# mqtt_publisher.py
import time, json
import paho.mqtt.client as mqtt
from chrony_stats import parse

client = mqtt.Client()

client.connect("core-mosquitto", 1883, 60)

while True:
    stats = parse()
    client.publish("gpsntp/chrony", json.dumps(stats))
    time.sleep(5)
