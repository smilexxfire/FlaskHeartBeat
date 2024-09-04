import json

from flask import Flask, render_template, jsonify
import socket
import threading
import datetime

app = Flask(__name__)

# 用于存储每个IP的首次接收到消息的时间和最新消息的时间
heartbeat_data = {}

# UDP监听端口和地址
UDP_IP = "0.0.0.0"
UDP_PORT = 5006
# 前端页面监听地址
HTTP_PORT = 8081

# 接收心跳信息的函数
def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            message = json.loads(message)

            current_time = datetime.datetime.now()
            ip = addr[0]
            # 更新
            heartbeat_data[ip] = {
                "hostname": message["hostname"],
                "duration": message["duration"],
                "latest_time": current_time
            }
            print(f"Received message from {addr}: {message} at {current_time}")
        except:
            pass

# 后台启动UDP监听线程
listener_thread = threading.Thread(target=udp_listener)
listener_thread.daemon = True
listener_thread.start()
# Flask路由，用于展示心跳信息
@app.route('/')
def index():
    return render_template('index.html')

def purge():
    """
    超过20分钟未发送心跳，信息从库里删除

    :return:
    """
    now = datetime.datetime.now()
    for ip in heartbeat_data.keys():
        time_difference = abs((now - heartbeat_data[ip]["latest_time"]).total_seconds())
        # 20分钟的秒数
        twenty_minutes = 20 * 60
        # 差值是否大于20分钟，大于则删除
        if time_difference > twenty_minutes:
            del heartbeat_data[ip]

@app.route('/api/heartbeat')
def api_heartbeat():
    purge()
    return jsonify(heartbeat_data)


if __name__ == '__main__':
    # 启动web应用
    app.run(host='0.0.0.0', port=HTTP_PORT)
