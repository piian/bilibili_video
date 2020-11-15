import os
import time

from flask import Flask

import api
import video
from model import Video
from utils import thread_download_list

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'video.db'),
)
app.debug = True

@app.template_filter('datetime')
def filter_datetime(s):
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(s))

app.register_blueprint(video.bp)
app.register_blueprint(api.api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run()

