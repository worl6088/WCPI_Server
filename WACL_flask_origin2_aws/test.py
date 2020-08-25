'''
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import text, create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import time
import make_db as md


conn_string = 'sqlite:///camera.db'


#DB 연동하는 부분

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


db = DBconnection(conn_string)

with db:
    start = time.time()

    알고리즘
    1. 쿼리탐색, 기존값 가져옴 
    2. 기존값에 새로운 값 덧붙여서 넣기 

    id_num =0

    q_id = db.session.query(md.Cam_1).filter_by(id=id_num).first()
    change1 = q_id.end_time + '|' + "test_data"
    change2 = q_id.end_time + '|' + "new_data"
    q_id.end_time, q_id.start_time = change1,change2
    db.session.commit()
    print("time :", time.time() - start)
    #query = db.session.query(Cam_1).filter_by(id=1).load_only("start_time", "end_time")
'''

''''
구현해야할 기능
1. 시그널이 들어오면 : 경고문구 발생 - cam_id + acci_name + alert !!
2.

mqtt acci_signal -> signal/cam1/violence, fire, .. 
					signal/cam2/violence, fire .. 
					
멀티프로세스? 
비동기처리? 

accidant handler 를 따로 만들기 

동선 추적 : 문제가 있다고 판단한 아이디를 따로 저장해서 감시.
'''

#app에서는 들어오는 메시지에 대해서 이거 하나만 해주면 됌
def rt_show_save(data)

#시그널 처리를 다루는 부분
class manager:
	#메니저란 클래스 안에 선언됌
	# 시그널인지 실시간데이터인지 확인
	def data_checker(self, data):
		to = data['topic'].split('/')
		if to[0] == "camera":
			flag = 0
			j_list = self.rt_data_handler(data)
			return j_list, flag
		'''
		위 실시간데이터에 대해선 문제가없음, 문제는 시그널에 관한 문제 
		시그널이 한종류라면 문제가 없음, 만약 종류가 여러개가 된다면 단순히 숫자로 플래그를 지정해주는 것만으로는 동작이 겹칠수있다.
		'''
		elif to[0] == "signal":
			flag = 1
			sig_result = self.signal_handler(data['topic'], data["payload"])
			return sig_result, flag

#일단 시그널 핸들러로 카메라별, 이벤트별 start/end flag를 구별할 수 있다.
	def signal_handler(self, acci_t, data):
		var = acci_t.split('/')
		detected_cam, event = int(var[1]), var[2]
		if data["payload"]['signal'] == "start":
			self.flag_list[detected_cam][event] = 1
			return
		elif data["payload"]['signal'] == "end":
			self.flag_list[detected_cam][event] = 0
			return start/endtime
