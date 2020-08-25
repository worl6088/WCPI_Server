from utils.tools import jsondump_processing
from Store_data_Test import result_Data_Handler
from utils.tools import log_maker
from ast import literal_eval

class manager:
    cam1_id = []
    cam2_id = []
    camera_num = 2
    #카메라 수 만큼 accidant 리스트생성
    flag_list  = [{"violence":0,  "fire": 0, "other_acci..": 0 } for i in range(camera_num+1)]

    # 시그널인지 실시간데이터인지 확인
    def data_checker(self, data):
        try:
            to = data['topic'].split('/')
            if to[0] == "camera":
                flag = 0
                j_list = self.rt_data_handler(data)
                return j_list, flag
            elif to[0] == "signal":
                flag = 1
                sig_result = self.signal_handler(to,data["payload"])
                return sig_result, flag
        except Exception as e:
            print('error raised!!! data_checker line 26 ', e)

    def rt_data_handler(self,data):
        Data = jsondump_processing(data['payload'])
        flag = self.check_id(data['topic'],Data[0])

        result_Data_Handler(data['topic'], Data,flag)
        j_list = {
            "id": Data[0],
            "person_pic": Data[3],
            "start_time": Data[1],
            "end_time": Data[2],
        }
        return j_list

    def signal_handler(self, acci_t, data):
        var = acci_t
        det_cam, event = int(var[1]),var[2]
        dic = literal_eval(data)
        sore = dic["signal"]
        print("print sore!!!! ")
        print(sore)
        try:
            if sore == "start":
                self.flag_list[det_cam][event] = 1
                evt_log = log_maker(sore,dic,det_cam,event)
                return evt_log

            elif sore == "end":
                self.flag_list[det_cam][event] = 0
                evt_log = log_maker(sore,dic,det_cam, event)
                return evt_log
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print('error raised singal handler line 60! ', e)

    def check_id(self,topic, id):
        if topic == "camera/cam1":
            if id not in self.cam1_id:
                self.cam1_id.append(id)
                print(self.cam1_id)
                return 0
            else:
                return 1
        elif topic == "camera/cam2":
            if id not in self.cam2_id:
                self.cam2_id.append(id)
                print(self.cam2_id)
                return 0
            else:
                return 1





