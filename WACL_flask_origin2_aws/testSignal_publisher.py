import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime
from utils.tools import end_time_maker

import time

# ====================================================
# MQTT Settings
MQTT_Broker = "116.124.106.60"
MQTT_Port = 8002
Keep_Alive_Interval = 100
MQTT_Topic_cam1 = "signal/1/violence"
MQTT_Topic_cam2 = "signal/2/violence"
# ====================================================


def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker: " + str(MQTT_Broker))


def on_publish(client, userdata, mid):
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


def publish_To_Topic(topic, message):
    mqttc.publish(topic, message)
    print("Published on MQTT Topic: " + str(topic))
    print("")


def publish_Fake_result_to_MQTT():
    try:
            start_time = (datetime.today()).strftime("%b-%d %H%M%S")
            print(start_time)
            cam1_startData = {}
            cam1_startData['signal'] = "start"
            cam1_json_data = json.dumps(cam1_startData)
            publish_To_Topic(MQTT_Topic_cam1, cam1_json_data)
            print("Published start_signal.. ")


            time.sleep(2)
            cam1_endData = {}
            cam1_endData['signal'] = 'end'
            cam1_endData['start_time'] = start_time
            cam1_endData['end_time'] = (datetime.today()).strftime("%b-%d %H%M%S")
            cam1_end_data = json.dumps(cam1_endData)
            publish_To_Topic(MQTT_Topic_cam1, cam1_end_data)
            print("Published end_signal.. ")
    except Exception:
            pass



publish_Fake_result_to_MQTT()