import threading

from playhouse.shortcuts import model_to_dict

from bilibili_api import Bilibili
from model import Video, PlayList


def models_to_dict(models):
    return [model_to_dict(orm) for orm in models]


def thead(video_id):
    client = Bilibili()
    client.download_by_id(video_id)
    Video.update(is_completed=True).where(Video.id == video_id).execute()


def thread_download(video_id):
    n = threading.Thread(target=thead, args=(video_id,))
    n.start()
    return "ok"


def thead_list(play_list_id):
    play = PlayList.get_by_id(play_list_id)
    while True:
        first_video = play.videos\
            .where(Video.is_progress == 0) \
            .where(Video.is_completed == 0) \
            .first()

        if first_video is None:
            break
        updated = Video.update(is_progress=1) \
            .where(Video.is_progress == 0) \
            .where(Video.id == first_video.id).execute()
        if updated == 1:
            client = Bilibili()
            client.download_by_id(first_video.id)
            Video.update(is_completed=True).where(Video.id == first_video.id).execute()


def thread_download_list(play_list_id):
    for i in range(1, 5):
        n = threading.Thread(target=thead_list, args=(play_list_id,))
        n.start()
    return "ok"
