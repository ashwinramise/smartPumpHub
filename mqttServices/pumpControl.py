import time
from datetime import datetime
import pandas as pd
import paho.mqtt.client as mqtt
import json
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from mqttServices import mqtt_config as config

mqtt_client = mqtt.Client(config.mqtt_client)
topic = config.publish_topic
broker = config.mqtt_broker

pumpON = {'register': [100, 103], 'bit': [0x01, 0x00]}
pumpOFF = {'register': [100, 103], 'bit': [0x01, 0x01]}


def powerPump(powerButton):
    mqtt_client.connect(broker)
    if powerButton:
        package = json.dumps(pumpON)
    if not powerButton:
        package = json.dumps(pumpOFF)
    try:
        mqtt_client.publish(topic, package, qos=0)  # publish to MQTT Broker every 5s
        print(f'{datetime.now()}: publishing {package} to {topic}')
    except:
        print('There was an issue sending data')