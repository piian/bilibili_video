import os

from bilibili_api import Bilibili

# 838569714   2020年黑马SSM最新就业班Spring+SpringMVC+Mybatis教程
# 38657363    SpringBoot_权威教程_spring boot_springboot核心篇+springboot整合篇-_雷丰阳_尚硅谷
if __name__ == '__main__':
    # 单次下载，每次下载一个集合 
    client = Bilibili()
    cid = '838569714'
    info = client.get_info(cid)
    path = info['title']
    if os.path.exists(path) is False:
        os.mkdir(path)
    print('一共%s个视频' % str(len(info['pages'])))
    for video in info['pages']:
        print(video['part'])
        client.get_url(video['cid'], video['part'], path)
