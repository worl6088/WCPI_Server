import paho.mqtt.client as mqtt
from .store_cam_Data_to_DB import result_Data_Handler

# MQTT 설정
MQTT_Broker = "localhost"
MQTT_Port = 8001
Keep_Alive_Interval = 60
MQTT_Topic = "camera/#"

#브로커와 연결됐는지 확인
def on_connect(mosq, obj, rc):
	if rc == 0:
		print("connected with result code " + str(rc))
	mqttc.subscribe(MQTT_Topic, 0)

#데이터 DB에 저장
def on_message(mosq, obj, msg):

	print("MQTT Data Received...")
	print("MQTT Topic: " + msg.topic )
	print("Data: " + str(msg.payload.decode("utf-8")))
	result_Data_Handler(msg.topic, msg.payload)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_subscribe(mosq, obj, mid, granted_qos):
	print("subscribed:" +str(mid) + " "+ str(granted_qos))

mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message


#연결
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
# 네트위크 이벤트 루프를 지속시킨다
mqttc.loop_forever()

