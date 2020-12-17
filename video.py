import os

import requests
from flask import (
    Blueprint, render_template, request
)

from bilibili_api import Bilibili
from model import PlayList, Video, get_play_list
from utils import models_to_dict, thread_download, thread_download_list, thead_list

bp = Blueprint('video', __name__)


@bp.route('/')
def index():
    return render_template('play_list.html', list=models_to_dict(PlayList.select()))


@bp.route('/search')
def search():
    type = request.args.get("type")
    if type == 'mid':
        play_list = PlayList.select(PlayList.aid)
        aids = [item.aid for item in play_list]
        print(aids)
        url = "https://api.bilibili.com/x/space/arc/search?mid=" + request.args.get("keyword")
        response = requests.get(url).json()
        print(response)
        data = response['data']['list']['vlist']
        for item in data:
            item['is_join'] = str(item['aid']) in aids
        return render_template("search.html", list=response['data']['list']['vlist'])
    else:
        start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + request.args.get("keyword")
        response = requests.get(start_url).json()
        data = response['data']
        list = [
            {'aid': data['aid'], "bvid": data['bvid'], "title": data['title'], "length": 0, "created": data['ctime'],
             "video_review": data['videos'],
             "is_join":  PlayList.select().where(PlayList.aid == data['aid']).exists()
             }
        ]
        return render_template("search.html", list=list)


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


@bp.route("/get_list_info/<b_vid>")
def get_info(b_vid):
    start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + str(b_vid)
    start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + str(b_vid)
    response = requests.get(start_url).json()
    data = response['data']
    return data
    print(data)
    # get_play_list(b_vid)
    print(b_vid)


@bp.route("/download_video/<int:id>")
def download_video(id):
    thread_download(id)
    return "ok"


@bp.route("/play_list/<string:bvid>", methods=['POST'])
def play_list_store(bvid):
    get_play_list(bvid)
    return "ok"


@bp.route("/download_list/<string:id>", methods=['POST'])
def download_list(id):
    # thead_list(id)
    thread_download_list(id)

    # videos = Video.select().where(Video.play_list_id == id)
    # for video in videos:
    #     client = Bilibili()
    #     client.download_by_id(video.id)
    #     Video.update(is_completed=True).where(Video.id == video.id).execute()
    return "ok"
