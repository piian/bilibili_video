import os

from bilibili_api import Bilibili
from model import PlayList

def download_by_aid(aid):
    """根据已经插入到数据库中的aid 去下载"""
    client = Bilibili()
    list = PlayList.select().where(PlayList.is_completed == False).where(PlayList.aid == '38657363')
    for play in list:
        # 播放列表名称
        print(play.title)
        path = 'downloads/' + play.title
        if os.path.exists(path) is False:
            os.mkdir(path)
        print('一共%s个视频' % str(len(play.videos)))
        for video in play.videos:
            print(video.title)
            client.get_url(video.cid, video.title, path)
            # 完成该视频
            video.is_completed = True
            video.save()

        # 完成播放列表
        play.is_completed = True
        play.save()

def download_url_aid():
    """根据输入的aid 下载视频 不保存到数据库"""
    client = Bilibili()
    cid = input('请输入aid:')
    client.get_list(cid)


if __name__ == '__main__':

    # download_url_aid()
    download_by_aid("38657363")