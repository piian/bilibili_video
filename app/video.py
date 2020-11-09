import os

from flask import (
    Blueprint, render_template, request
)

from app import models_to_dict, thread_download
from app.model import PlayList, Video, get_play_list

bp = Blueprint('video', __name__)


@bp.route('/')
def index():
    list = PlayList.select()
    return render_template('play_list.html', list=models_to_dict(list))


@bp.route("/play/<int:play_id>")
def play(play_id):
    play = PlayList.select().where(PlayList.id == play_id).first()
    videos = Video.select().where(Video.play_list_id == play_id)
    video_dict = models_to_dict(videos)
    for video in video_dict:
        file = 'downloads/' + play.title + "/" + video['title'] + '.mp4'
        if os.path.exists(file) is True:
            video['size'] = os.path.getsize(file)
        else:
            video['size'] = 0
    print(video_dict)
    return render_template("play.html", play=play, videos=video_dict)


@bp.route("/download_video/<int:id>")
def download_video(id):
    thread_download(id)
    return "ok"

@bp.route("/download_list", methods=['POST'])
def download_list():
    name = request.get_json()['name']
    get_play_list(name)
    # thread_download(id)
    return "ok"
