from datetime import datetime
import cv2 as cv
import numpy as np
import json
from time import sleep
import base64
import cv2 as cv
pic_path = 'https://edgeserv.s3.ap-northeast-2.amazonaws.com/'

def jsondump_processing(payload):
    global pic_path
    try:
        json_load = json.loads(payload)
        p_id_restored = int(json_load['p_id'])
        s_time_restored = json_load['start_time']
        e_time_restored = json_load['end_time']
        pic_restored = pic_path+ json_load['pic']
        data_ = [p_id_restored,s_time_restored,e_time_restored, pic_restored]
        return data_
    except Exception as ex:
        print('error!!! in jsondemp_processing  ', ex)


def end_time_maker():
    date = (datetime.today()).strftime("%d-%b-%Y %H%M%S")
    a = list(date)
    b = a[-2:]
    c = int("".join(b))
    d = str(c + 5)
    if a[-2] == '0':
        a[-2:] = ['0', d[1]]
    else:
        a[-2:] = [d[0], d[1]]

    changed_date = "".join(a)
    return changed_date

def log_maker(flag,data,cam, event):
    if flag == "start":
        evt_log = "<Cam "+str(cam)+"> "+ event +" event deteceted!!"
        return evt_log
    else:
        time = data["start_time"] + " ~ " + data["end_time"]
        evt_log = "<Cam "+str(cam)+"> "+ event +" event terminated!!" + "   time: " + str(time)
        return evt_log


def path_maker(p_id,cam_id,s_time):
    file_name = "Pid_"+ str(p_id) + "_cid_"+str(cam_id) + "_" + s_time + ".jpg"
    path = pic_path + file_name
    return path, file_name


