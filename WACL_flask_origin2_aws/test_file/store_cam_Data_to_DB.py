import json
import pymysql
import numpy as np
import cv2 as cv


db_name = "mqtt_test"
db_host = "127.0.0.1"
db_user = 'root'
db_pw = '0000'
charset = "utf8"
pic_path = "C:\\Users\\worl6\\Desktop\\person_pic\\"
#DB 연동하는 부분
class DatabaseManager():

	def __init__(self):

		self.conn = pymysql.connect(host='localhost',
							   user=db_user,
							   password=db_pw,
							   database=db_name,
							   charset=charset )

		#self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		print("디비 connect 했고 커밋이랑 커서까지 연결하였습니당 ")


	def add_del_update_db_record(self, sql_query, args):
		print(args)
		try:
			self.cur.execute(sql_query, args)
			print("에러는 안나지만 여기서 실행되지 않음 ")
		except Exception as ex:
			print('에러가 발생하였습니다',ex)


		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# 데이터베이스에 가상 cam 데이터 저장

def cam1_Data_Handler(jsonData):
	print("cam1 handler is started! ")
	json_Dict = json.loads(jsonData)
	Date_and_Time = json_Dict['Date']
	Result = json_Dict['pic']
	print(type(Date_and_Time))
	query = "insert into cam1_result_table(cameraID, Date_n_Time, result) values (%s, %s, %s)"
	# DB 테이블 push
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record(query, ('1', Date_and_Time, Result))
	del dbObj
	print("Inserted test Data into Database.")
	print("")

def cam2_Data_Handler(jsonData):
	print("cam2 handler is started! ")
	json_Dict = json.loads(jsonData)
	camera_ID = json_Dict['camera_ID']
	Data_and_Time = json_Dict['Date']
	Result = json_Dict['result']
	# DB 테이블에 push
	query = "insert into cam2_result_table(cameraID, Date_n_Time, result) values (%s, %s, %s)"
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record(query,('2', Data_and_Time, Result))
	del dbObj
	print("Inserted test Data into Database.")
	print("")


def save_image(json_load):
	pic_restored = np.array(json_load['pic'], dtype=np.uint8)
	p_id_restored = int(json_load['p_id'])
	cam_id_restored = int(json_load['cam_id'])
	s_time_restored = str(json_load['start_time1'])
	e_time_restored = str(json_load['end_time1'])
	print("p_id : ", p_id_restored)
	print("cam_id : ", cam_id_restored)
	print("s_time : ", s_time_restored)
	print("e_time : ", e_time_restored)
	cv.imshow("restored", pic_restored)
#===============================================================
# Master가 Topic에 따라서 다른 핸들러를 적용하여 해당하는 db에 저장시킨다

def result_Data_Handler(Topic, jsonData):
	if Topic == "camera/cam1":
		cam1_Data_Handler(jsonData)
	elif Topic == "camera/cam2":
		cam2_Data_Handler(jsonData)

#==============================================================
