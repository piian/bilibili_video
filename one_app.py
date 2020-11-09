from app.bilibili_api import Bilibili
from app.model import PlayList, Video, inserListByAid

if __name__ == '__main__':
    # 单次下载，每次下载一个集合
    # 73576628
    aid = input("请输入你要下载的avid：")
    client = Bilibili()
    client.downloadById(10)
    exit()
    if aid != '':
        inserListByAid(str(aid))
    else:
        list = PlayList.select()
        for play in list:
            print(" / ".join([str(play.id), play.aid, play.title]))
        id = input("请输入你要下载的视频集：")
        play = PlayList.select().where(PlayList.id == id).first()
        videos = Video.select().where(Video.play_list_id == id)
        for video in videos:
            print(" / ".join([str(video.id), str(video.cid), str(video.is_completed), video.title]))
        vid = input("请输入你要下载的视频,0下载全部：")
        if id == 0:
            pass
        else:
            video = Video.select().where(Video.id == vid).first()
            play = PlayList.select().where(PlayList.id == video.play_list_id).first()

            print("开始下载"+video.title+"，视频集："+play.title)
            client.get_url(video.cid, video.title, 'downloads/'+play.title)

# print("id:"+str(play.id), " / "+play.title)
    # list = PlayList.select().where(PlayList.aid == aid).first()
    # print(list.title)
