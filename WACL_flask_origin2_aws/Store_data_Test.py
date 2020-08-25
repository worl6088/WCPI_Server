from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import make_db as init


#DB 연동하는 부분

conn_string = 'sqlite:///camera.db'
Table = [init.Cam_1,init.Cam_2,init.Cam_3]

class DBconnection(object):
	def __init__(self, connection_string):
		self.connection_string = connection_string
		self.session = None

	def __enter__(self):
		engine = create_engine(self.connection_string)
		Session = sessionmaker()
		self.session = Session(bind=engine)
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.session.close()



def add_del_update_db_record(data, args,flag):
	db = DBconnection(conn_string)
	with db:
		try:
			if args == 1:
				if flag==0:
					table_class = init.Cam_1()
					table_class.id = data[0]
					table_class.start_time = data[1]
					table_class.end_time = data[2]
					table_class.person_image = data[3]
					db.session.add(table_class)
					db.session.commit()
				else:
					q_id = db.session.query(init.Cam_1).filter_by(id=data[0]).first()
					change1 = q_id.start_time + '|' + data[1]
					change2 = q_id.end_time + '|' + data[2]
					q_id.start_time, q_id.end_time = change1, change2
					db.session.commit()
			else:
				if flag==0:
					table_class = init.Cam_2()
					table_class.id = data[0]
					table_class.start_time = data[1]
					table_class.end_time = data[2]
					table_class.person_image = data[3]
					db.session.add(table_class)
					db.session.commit()
				else:
					q_id = db.session.query(init.Cam_2).filter_by(id=data[0]).first()
					change1 = q_id.start_time + '|' + data[1]
					change2 = q_id.end_time + '|' + data[2]
					q_id.start_time, q_id.end_time = change1, change2
					db.session.commit()

		except Exception as ex:
			print('error raised!!! ',ex)


def search_all_table():
	global Table
	db  = DBconnection(conn_string)
	with db:
		try:
			id_list = []
			time = []
			for cam in Table:
				id_table = []
				time_table = []
				for instance in db.session.query(cam).order_by(cam.id):
					id_table.append(instance.id)
					time_table.append((instance.start_time,instance.end_time))
				id_list.append(id_table)
				time.append(time_table)
				#print(str(instance.id)+"_"+str(instance.person_image))
			print("finish db search ~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			return id_list, time
		except Exception as e:
			print(e)


#===============================================================
# 데이터베이스에 가상 cam 데이터 저장

def cam1_Data_Handler(Data,flag):
	print("cam1 handler is started! ")
	add_del_update_db_record(Data,1,flag)
	print("Inserted test Data into Database.")
	print("")

def cam2_Data_Handler(Data,flag):
	print("cam2 handler is started! ")
	add_del_update_db_record(Data, 2,flag)
	print("Inserted test Data into Database.")
	print("")


def result_Data_Handler(Topic, jsonData,flag):
	if Topic == "camera/cam1":
		cam1_Data_Handler(jsonData,flag)
	elif Topic == "camera/cam2":
		cam2_Data_Handler(jsonData,flag)

