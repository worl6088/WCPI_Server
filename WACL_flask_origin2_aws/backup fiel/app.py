import eventlet
from flask import Flask, render_template, url_for
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from init_DB import remove_last_data
from data_manager import manager

eventlet.monkey_patch()
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["MQTT_BROKER_URL"] = "localhost"
app.config["MQTT_BROKER_PORT"] = 8888
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 100
app.config["MQTT_TLS_ENABLED"] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
remove_last_data()
dm = manager()

@app.route("/")
def index():
    return render_template("showup2.html")


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("camera/#")
    mqtt.subscribe("signal/#")


@socketio.on('subscribe')
def handle_client_connected(json):
    print('received json: {0}'.format(str(json)))


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode("utf-8"),
        qos=message.qos
    )

    print(client, data['topic'])
    rt_show_save(data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

@app.route('/index', methods=['GET', 'POST'])
def lionel():
    return render_template('surveilance.html')

def rt_show_save(data):
    result, flag = dm.data_checker(data)
    try:
        if flag == 0:
            socketio.emit('rt_data_show', {'data': result})
        else:
            socketio.emit('event_log_show', {'data': result})
    except Exception as e:
        print('error raised!!! ', e)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=8000, use_reloader=True, debug=True)