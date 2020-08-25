import make_db as init
from Store_data_Test import DBconnection
from flask import session
from flask_socketio import emit, join_room, leave_room
from app import socketio



@socketio.on('joined', namespace='/surveilance')
def joined(message):
    id_list, time_list = search_all_table()
    print('move page!! ')
    print(id_list)
    ID = session.get('ID') #웹에서 입력받은 아이디
    join_room(ID)
    msg = 'finish db search'
    socketio.emit('status',{'data':'test message'},room=ID)
