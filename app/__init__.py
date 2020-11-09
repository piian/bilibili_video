import os
import threading

from flask import Flask
from flask_sockets import Sockets
from playhouse.shortcuts import model_to_dict

from app.bilibili_api import Bilibili
from app.model import Video


def models_to_dict(models):
    return [model_to_dict(orm) for orm in models]


def thead(video_id):
    client = Bilibili()
    client.downloadById(video_id)
    Video.update(is_completed=True).where(Video.id == video_id).execute()


def thread_download(id):
    n = threading.Thread(target=thead, args=(id,))
    n.start()
    return "ok"


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'video.db'),
    )
    app.debug = True

    sockets = Sockets(app)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        # a simple page that says hello

    @sockets.route('/test')  # 指定路由
    def echo_socket(ws):
        while not ws.closed:
            ws.send(str("message test!"))  # 回传给clicent
            """ 服务端必须接收到客户端发的消息才能保持该服务运行，如果ws.receive()没有接收到客户端发送的
             消息，那么它会关闭与客户端建立的链接
             底层解释：Read and return a message from the stream. If `None` is returned, then
            the socket is considered closed/errored.
            所以客户端只建立连接，不与服务端交互通信，则无法实现自由通信状态，之后在客户端代码处会有详细内容。
             """
            message = ws.receive()  # 接收到消息
            if message is not None:
                """ 如果客户端未发送消息给服务端，就调用接收消息方法，则会导致receive()接收消息为空，关闭此次连接 """
                ws.send('12')  # 回传给clicent
            else:
                print("no receive")


    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import video
    app.register_blueprint(video.bp)

    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('127.0.0.1', 6000), app, handler_class=WebSocketHandler)
    # server.serve_forever()

    return app
