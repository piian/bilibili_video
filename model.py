import requests
from peewee import *


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('video.db')


class PlayList(BaseModel):
    id = PrimaryKeyField()
    aid = CharField(default=0, unique=True)
    slug = CharField(verbose_name='标识', null=True)
    title = CharField(null=True)
    description = CharField(null=True)
    pic = CharField(null=True)
    author = CharField(null=True)
    mid = IntegerField(default=0)
    is_completed = BooleanField(default=False)

    def __str__(self):
        return self.__data__

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
    is_progress = BooleanField(default=False)
    play_list = ForeignKeyField(PlayList, backref='videos')
    size = IntegerField(default=0)

    def insert_data(self, data, play):
        count = self.select(self.cid == data['cid']).count()
        # print(count)
        # print(data)
        if count == 0:
            return self.create(cid=data['cid'], title=data['part'], is_completed=0, play_list=play)
        else:
            pass
            # return self.get(Video.cid == data['cid'])


def get_play_list(bvid):
    # aid
    start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + str(bvid)
    response = requests.get(start_url).json()
    data = response['data']
    list = PlayList.select().where(PlayList.aid == data['aid'])
    if list.count() == 0:
        play_list = PlayList.create(aid=data['aid'],
                        slug=data["bvid"],
                        title=data['title'],
                        description=data['desc'],
                        pic=data['pic'],
                        author=data['owner']['name'],
                        mid=data['owner']['mid']
                        )

    else:
        play_list = list.get()

    for page in data['pages']:
        print(page['cid'])
        count = Video.select(Video.cid).where(Video.cid == page['cid']).count()
        print(count)
        if count == 0:
            print("数据库没有，插入")
            video = Video.create(cid=page['cid'], title=page['part'], is_completed=0, play_list=play_list)
            print("play_list_id:"+str(video.play_list_id))
        # else:
        #     res = Video.update({Video.play_list_id: play_list.id}).where(Video.cid == page['cid'])
        #     print(res)
    return play_list

if __name__ == '__main__':
    list = PlayList.select(PlayList.aid).where(PlayList.aid == 83622425)
    if list.count() != 0:
        print(list.get())
    # list = PlayList.create(title="123", aid=123)
    # Video.create(play_list= list, title="234")
