import os

from bilibili_api import Bilibili
from model import PlayList

if __name__ == '__main__':

    client = Bilibili()
    # cid = input('请输入aid:')
    # client.get_list(cid)
    list = PlayList.select().where(PlayList.is_completed == False)
    for play in list:
        title = 'downloads/' + play.title
        if os.path.exists(title) is False:
            os.mkdir(title)
        for video in play.videos:
            print(play.title)
            client.get_url(video.cid, video.title, title)
            video.is_completed = True
            video.save()
            print(video.title)
        play.is_completed = True
        play.save()
    # client.get_url(cid, filename, title)
