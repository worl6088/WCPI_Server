import paho.mqtt.client as mqtt
import random, threading, json
import boto3
from datetime import datetime
from utils.tools import end_time_maker
from PIL import Image
import io
from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np

# ====================================================
# MQTT Settings
MQTT_Broker = "localhost"
MQTT_Port = 8888
Keep_Alive_Interval = 100
MQTT_Topic_cam1 = "camera/cam1"
MQTT_Topic_cam2 = "camera/cam2"
# AWS S3 setting
bucket_name = 'edgeserv'
s3 = boto3.resource(
    's3',
    aws_access_key_id='AKIAWX6I5TPNM5KSG5KD',
    aws_secret_access_key='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',
    region_name='ap-northeast-2',
)

# ====================================================
with open('C:\\Users\\jacky\\Desktop\\jot.json') as json_file:
    json_data = json.load(json_file)
    pic_data = json_data["pic"]

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



toggle = 0

def publish_Fake_result_to_MQTT():
    threading.Timer(3, publish_Fake_result_to_MQTT).start()
    global toggle
    if toggle == 0:
        try:
            p_id = random.randint(0,11)
            cam_id = 1
            s_time = (datetime.today()).strftime("%d-%b-%Y %H%M%S")
            file_name = "Pid_" + str(p_id) + "_cid_" + str(cam_id) + "_" + s_time + ".png"

            cam1_Data = {}
            cam1_Data['p_id'] = p_id
            cam1_Data['cam_id'] = cam_id
            cam1_Data['start_time'] = s_time
            cam1_Data['end_time'] = end_time_maker()
            cam1_Data['pic'] = file_name

            upload_s3(pic_data, file_name)

            cam1_json_data = json.dumps(cam1_Data)
            print("Publishing fake cam1_result.. ")
            publish_To_Topic(MQTT_Topic_cam1, cam1_json_data)
            toggle = 1

        except:
            pass

    else:
        try:
            p_id = random.randint(5, 15)
            cam_id = 2
            s_time = (datetime.today()).strftime("%d-%b-%Y %H%M%S")
            file_name = "Pid_" + str(p_id) + "_cid_" + str(cam_id) + "_" + s_time + ".png"

            cam2_Data = {}
            cam2_Data['p_id'] = p_id
            cam2_Data['cam_id'] = cam_id
            cam2_Data['start_time'] = s_time
            cam2_Data['end_time'] = end_time_maker()
            cam2_Data['pic'] = file_name

            upload_s3(pic_data, str(file_name))

            cam2_json_data = json.dumps(cam2_Data)
            print("Publishing fake cam2_result.. ")
            publish_To_Topic(MQTT_Topic_cam2, cam2_json_data)
            toggle = 0

        except:
            pass

'''
색상이 꺠짐 
def upload_s3_2(data,name):
    try :
        print(name)
        pic = np.array(data, dtype=np.uint8)
        img = Image.fromarray(pic.astype('uint8'), 'RGB')
        out_img = io.BytesIO()
        img.save(out_img, format='png')
        out_img.seek(0)
        print('finish save')
        s3.Bucket(bucket_name).put_object(Key=name,Body=out_img,ContentType='image/png',ACL='public-read')


    except Exception as e:
        print(e)
'''
#https://stackoverflow.com/questions/53316470/upload-numpy-array-as-grayscale-image-to-s3-bucket 참고
def upload_s3(data,name):
    try :
        pic = np.array(data, dtype=np.uint8)
        data_serial = cv.imencode('.png', pic)[1].tostring()
        s3.Bucket(bucket_name).put_object(Key=name, Body=data_serial, ContentType='image/png', ACL='public-read')
    except Exception as e:
        print(e)


publish_Fake_result_to_MQTT()