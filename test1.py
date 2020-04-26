# import exifread
#
# # Open image file for reading (binary mode)
# f = open('test.jpg', 'rb')
#
# # Return Exif tags
# tags = exifread.process_file(f)
#
# print(tags)
import hashlib
import os

import requests

from download_file import download

entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
# appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
# print(appkey, sec)
# exit()
next_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Range': 'bytes=0-',  # Range 的值要为 bytes=0- 才能下载完整视频
    'Referer': 'https://www.bilibili.com',  # 注意修改referer,必须要加的!
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive',
}
cid = '19516333'
# 短
cid = '32170391'
# 系列
cid = '32317625'
# 3小时教你入门numpy
cid = '50452482'
cid = '32170391'
cid = '19817183'
cid = '98652168'
cid = '94404010'  # 大型网站Mysql性能优化之索引原理分析


# url = 'http://cn-hbsjz-cmcc-bcache-02.acgvideo.com/upgcxcode/14/76/32317614/32317614-1-64.flv?e=ig8euxZM2rNcNbRV7WdVhoM1hwUVhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNC8xNEVE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==&deadline=1571391269&gen=playurl&nbs=1&oi=3086393504&os=bcache&platform=pc&trid=c44a25b386af45a3a3405f638531aa93&uipk=5&upsig=6cab1dc33437f879da3d20fd804c3d4d&uparams=e,deadline,gen,nbs,oi,os,platform,trid,uipk&mid=0&origin_cdn=ks3'
# url = 'http://cn-hbsjz-cmcc-bcache-04.acgvideo.com/upgcxcode/14/76/32317614/32317614-2-64.flv?e=ig8euxZM2rNcNbR1hbUVhoM1hWNBhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNC8xNEVE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==&deadline=1571391269&gen=playurl&nbs=1&oi=3086393504&os=bcache&platform=pc&trid=c44a25b386af45a3a3405f638531aa93&uipk=5&upsig=cebb3c0c032f4a81d6c3ec3e9934ed2d&uparams=e,deadline,gen,nbs,oi,os,platform,trid,uipk&mid=0&origin_cdn=cos'
# download(url, 'test121222222.mp4', next_headers)
# exit()


def get_info(cid):
    start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + cid
    response = requests.get(start_url).json()
    title = response['data']['title']
    pages = response['data']['pages']
    if os.path.exists(title) is False:
        os.mkdir(title)
    return {'title': title, "pages": [{'part': page['part'], 'cid': page['cid']} for page in pages]}


def merge_video(audio, title, video):
    """
    合并音频和视频
    :param audio:
    :param title:
    :param video:
    """
    os.system('ffmpeg -y -i ' + video + ' -i ' + audio + ' -vcodec copy -acodec copy ' + title + '.mp4')
    os.remove(video)
    os.remove(audio)


def get_url(page, file_name):
    cid = page['cid']
    part = page['part']
    appkey = 'iVGUTjsxvpLeuDCf'
    sec = 'aHRmhWMLkdeMuILqORnYZocwMBpMEOdt'
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, 80, 80)
    sign = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, sign)
    headers = {
        'Referer': 'www.bilibili.com',  # 注意加上referer
    }
    html = requests.get(url_api, headers=headers).json()
    video_list = []
    print(html['durl'])
    if len(html['durl']) == 1:
        download(html['durl'][0]['url'], file_name + '/' + part + '.mp4', next_headers)
    else:
        temps = []
        for i in html['durl']:
            temp = file_name + '/' + part + '.tmp'
            temps.append(temp)
            download(i['url'], temp, next_headers)
    return video_list


info = get_info(cid)
file = info['title']
print(file)
for vid in info['pages']:
    get_url(vid, file)
print(vid)
exit()
