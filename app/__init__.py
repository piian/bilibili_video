import os
import threading

from flask import Flask
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

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

        # a simple page that says hello

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import video
    app.register_blueprint(video.bp)

    return app
