import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

# ====================================================
# MQTT Settings 
MQTT_Broker = "localhost"
MQTT_Port = 8001
Keep_Alive_Interval = 60
MQTT_Topic_cam1 = "camera/cam1"
MQTT_Topic_cam2 = "camera/cam2"


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
    print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
    print("")


# ====================================================
# FAKE SENSOR 
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

toggle = 0


def publish_Fake_Sensor_Values_to_MQTT(pic):
    threading.Timer(2.0, publish_Fake_Sensor_Values_to_MQTT).start()
    global toggle
    if toggle == 0:
        p_id_random_Value = random.randint(0,11)
        cam1_Data = {}
        cam1_Data['cam_id'] = "0"
        cam1_Data['p_id'] = p_id_random_Value
        cam1_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        cam1_Data['pic'] = pic
        cam1_json_data = json.dumps(cam1_Data)

        print("Publishing fake cam1_result.. ")
        publish_To_Topic(MQTT_Topic_cam1, cam1_json_data)
        toggle = 1

    else:
        p_id_random_Value = random.randint(0, 11)
        cam2_Data = {}
        cam2_Data['cam_id'] = "1"
        cam2_Data['p_id'] = p_id_random_Value
        cam2_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        cam2_Data['Temperature'] = pic
        cam2_json_data = json.dumps(cam2_Data)

        print("Publishing fake cam2_result.. ")
        publish_To_Topic(MQTT_Topic_cam2, cam2_json_data)
        toggle = 0

with open('C:\\Users\\worl6\\Desktop\\jot.json') as json_file:
    json_data = json.load(json_file)
    pic_data = json_data["pic"]

publish_Fake_Sensor_Values_to_MQTT(pic_data)