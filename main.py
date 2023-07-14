import os
import threading
import time

from flask import Flask, request, send_file
from flask_cors import CORS
import numpy as np
import random
from settings import img_save_path
from flask_socketio import SocketIO
import openai
import db_question

from utils import stop_thread

openai.api_key = 'xxx'

app = Flask(__name__)
CORS(app)
socket_io = SocketIO(app, cors_allowed_origins='*')
user_th = {}


def sendChat(prompt, user_id):
    body = {
        'model': "gpt-3.5-turbo-0613",
        'messages': prompt,
        'max_tokens': 2048,
        'stream': True
    }
    try:
        resp = openai.ChatCompletion.create(**body)
    except Exception as E:
        time.sleep(2)
        print(E)
        try:
            resp = openai.ChatCompletion.create(**body)
        except Exception as E:
            print(E)
            socket_io.emit('answer', data={'msg': 'failure'}, to=user_id)
            return
    socket_io.emit('answer', data={'msg': '__begin__'}, to=user_id)
    for res in resp:
        socket_io.emit('answer', data={'msg': res["choices"][0]["delta"].get("content", "")}, to=user_id)


@app.route('/get_img/<string:img_name>', methods=['GET', 'POST'])
def get_img(img_name):
    return send_file(os.path.join(img_save_path, img_name), mimetype='image/jpeg')


@socket_io.on('questions')
def getQ(data):
    prompt = data['prompt']
    socket_id = data['socket_id']
    if user_th.get(socket_id, None) is not None and user_th[socket_id].is_alive():
        stop_thread(user_th[socket_id])
    th = threading.Thread(target=sendChat, args=[prompt, socket_id])
    user_th[socket_id] = th
    th.start()


# 题目
# 创建数据库操作实例
db = db_question.Database('localhost', 3306, 'root', '123456', 'qa')
db.connect()
@app.route('/question', methods=['GET', 'POST'])
def question():
    # 进行数据库题库查询
    results = db.get_random_questions()
    # print('results:', results)
    return results


if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0', port=12345, allow_unsafe_werkzeug=True)
