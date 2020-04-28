import requests
from peewee import *


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('video.db')


class PlayList(BaseModel):
    aid = CharField(default=0, unique=True)
    slug = CharField(verbose_name='标识', null=True)
    title = CharField(null=True)
    description = CharField(null=True)
    pic = CharField(null=True)
    author = CharField(null=True)
    is_completed = BooleanField(default=False, )

    def insert_data(self, data):
        count = self.select(self.aid == data['aid']).count()
        print(data['aid'])
        if count == 0:
            print(1)
            insert = {
                'aid': data['aid'],
                'slug': data['bvid'],
                'title': data['title'],
                'description': data['desc'],
                'pic': data['pic'],
                'author': data['owner']['name'],
            }
            return self.insert(insert).execute()
        else:
            return self.get(PlayList.aid == data['aid'])


class Video(BaseModel):
    title = CharField(null=True)
    cid = IntegerField(default=0, unique=True)
    is_completed = BooleanField(default=False)
    play_list = ForeignKeyField(PlayList, backref='videos')

    def insert_data(self, data, play):
        count = self.select(self.cid == data['cid']).count()
        print(count)
        print(data)
        if count == 0:
            return self.create(cid=data['cid'], title=data['part'], is_completed=0, play_list=play)
        else:
            pass
            # return self.get(Video.cid == data['cid'])


def get_play_list(aid):
    start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + str(aid)
    response = requests.get(start_url).json()
    data = response['data']

    count = PlayList.select(PlayList.aid).where(PlayList.aid == data['aid']).count()
    print(data['aid'])
    if count == 0:
        print(1)
        insert = {
            'aid': data['aid'],
            'slug': data['bvid'],
            'title': data['title'],
            'description': data['desc'],
            'pic': data['pic'],
            'author': data['owner']['name'],
        }
        play_list = PlayList.insert(insert).execute()
    else:
        play_list = PlayList.get(PlayList.aid == data['aid'])
    for page in data['pages']:
        print(page['cid'])
        count = Video.select(Video.cid).where(Video.cid == page['cid']).count()
        if count == 0:
            video = Video.create(cid=page['cid'], title=page['part'], is_completed=0, play_list=play_list)
            print(video.id)


if __name__ == '__main__':
    # video = Video.get_by_id(1)
    # print(video.title)
    # exit()
    # PlayList.drop_table()
    # Video.drop_table()
    # PlayList.create_table()
    # Video.create_table()
    mid = 511491630
    response = requests.get('https://api.bilibili.com/x/space/arc/search?mid=' + str(mid) + '&pn=1&ps=100&jsonp=jsonp')
    result = response.json()
    for vlist in result['data']['list']['vlist']:
        get_play_list(vlist['aid'])
