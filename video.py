import os

import requests
from flask import (
    Blueprint, render_template, request
)

from bilibili_api import Bilibili
from model import PlayList, Video, get_play_list
from utils import models_to_dict, thread_download, thread_download_list

bp = Blueprint('video', __name__)


@bp.route('/')
def index():
    return render_template('play_list.html', list=models_to_dict(PlayList.select()))


@bp.route('/search')
def search():
    search_type = request.args.get("type")
    if search_type == 'mid':
        # 获取当前视频库的所有视频
        play_list = PlayList.select(PlayList.aid)
        aids = [item.aid for item in play_list]

        # 根据用户id获取用户的视频列表
        response = Bilibili.search_by_mid(request.args.get("keyword"))
        data = response['data']['list']['vlist']
        # 判断是否已经加入下载列表
        for item in data:
            item['is_join'] = str(item['aid']) in aids
        return render_template("search.html", list=response['data']['list']['vlist'])
    elif search_type == 'keyword':
        # 获取当前视频库的所有视频
        play_list = PlayList.select(PlayList.aid)
        aids = [item.aid for item in play_list]

        # 根据用户id获取用户的视频列表
        response = Bilibili.search_by_keyword(request.args.get("keyword"))
        data = response['data']['list']['vlist']
        # 判断是否已经加入下载列表
        for item in data:
            item['is_join'] = str(item['aid']) in aids
        return render_template("search.html", list=response['data']['list']['vlist'])
    else:
        # 获取指定视频集合
        data = Bilibili.get_view_by_bvid(request.args.get("keyword"))['data']
        view_list = [
            {'aid': data['aid'], "bvid": data['bvid'], "title": data['title'], "length": 0, "created": data['ctime'],
             "video_review": data['videos'],
             "is_join": PlayList.select().where(PlayList.aid == data['aid']).exists()
             }
        ]
        return render_template("search.html", list=view_list)


@bp.route("/play/<int:play_id>")
def play(play_id):
    play_list = PlayList.select().where(PlayList.id == play_id).first()

    videos = Video.select().where(Video.play_list_id == play_id)
    video_dict = models_to_dict(videos)
    client = Bilibili()
    for video in video_dict:
        file = Bilibili.download_path+ '/' + play_list.title + "/" + video['title'] + '.mp4'

        if video['size'] == 0:
            html = client.get_response_by_cid(video['cid'])
            if 'durl' in html.keys() and len(html['durl']) == 1:
                # 如果只有一个链接，则表示单视频
                print(html['durl'][0])
                Video.update(size=html['durl'][0]['size']).where(Video.cid == video['cid']).execute()
            print(html)

        if os.path.exists(file) is True:
            video['file_size'] = os.path.getsize(file)
        else:
            video['file_size'] = 0
    return render_template("play.html", play=play_list, videos=video_dict)


@bp.route("/get_list_info/<b_vid>")
def get_info(b_vid):
    return Bilibili.get_view_by_bvid(b_vid)['data']


@bp.route("/download_video/<video_id>")
def download_video(video_id: str):
    thread_download(video_id)
    return "ok"


@bp.route("/play_list/<string:bvid>", methods=['POST'])
def play_list_store(bvid: str) -> str:
    play_list = get_play_list(bvid)
    # print(play_list.id)
    return {"msg":"ok", "data":play_list.id}


@bp.route("/download_list/<play_list_id>", methods=['POST'])
def download_list(play_list_id: str):
    thread_download_list(play_list_id)
    return "ok"
