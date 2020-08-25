import make_db as init
from Store_data_Test import DBconnection
from flask import session
from flask_socketio import emit, join_room, leave_room
from app import socketio

conn_string = 'sqlite:///camera.db'
Table = [init.Cam_1,init.Cam_2,init.Cam_3]


@socketio.on('search_log', namespace='/surveilance')
def joined(message):
    id_list, time_list = search_all_table()
    print('move page!! ')
    print(id_list)
    ID = session.get('ID') #웹에서 입력받은 아이디값
    msg = 'finish db search'
    socketio.emit('search_log',{'data':msg})

def search_all_table():
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
            return id_list, time
        except Exception as e:
            print(e)

