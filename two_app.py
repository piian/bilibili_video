import os
import sys

from app.bilibili_api import Bilibili

# 838569714   2020年黑马SSM最新就业班Spring+SpringMVC+Mybatis教程
# 38657363    SpringBoot_权威教程_spring boot_springboot核心篇+springboot整合篇-_雷丰阳_尚硅谷
# 668766982   谷粒商城-分布式高级篇-1
# 838831843   谷粒商城-分布式高级篇-2
# 413804162   谷粒商城-分布式高级篇-3
# 245071647   2020微服务分布式电商项目《谷粒商城》高级和集群篇
# 669994685   谷粒商城-高级（包含错漏）
if __name__ == '__main__':
    # 单次下载，每次下载一个集合
    client = Bilibili()
    cid = '669994685'
    info = client.get_info(cid)
    path = info['title']
    if os.path.exists(path) is False:
        os.mkdir(path)
    print('一共%s个视频' % str(len(info['pages'])))
    i = 0

    if len(sys.argv) == 2:
        j = sys.argv[1]
        for video in info['pages']:
            i += 1
            if i == int(j):
                print(video['part'])
                client.get_url(video['cid'], video['part'], path)
        exit()
    for video in info['pages']:
        i += 1
        print(video['part'])
        client.get_url(video['cid'], video['part'], path)
