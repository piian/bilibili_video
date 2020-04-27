import hashlib
import os

import requests

from download_file import download


class Bilibili():
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

    def get_list(self, cid):
        info = self.get_info(cid)
        file = info['title']
        # 标题
        print(file)
        print('一共' + str(len(info['pages'])) + '视频')
        for vid in info['pages']:
            self.get_url(vid, file)

    @staticmethod
    def get_info(cid):
        start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + cid
        response = requests.get(start_url).json()
        title = response['data']['title']
        title = 'downloads/' + title
        pages = response['data']['pages']
        if os.path.exists(title) is False:
            os.mkdir(title)
        return {'title': title, "pages": [{'part': page['part'], 'cid': page['cid']} for page in pages]}

    def get_url(self, page, file_name):
        """获取每个链接"""
        cid = page['cid']
        part = page['part']
        # 打印当前视频标题
        print(part)
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
        # print(html['durl'])  # 打印数据
        # exit()
        if len(html['durl']) == 1:
            # 如果只有一个链接，则表示单视频
            download(html['durl'][0]['url'], file_name + '/' + part + '.mp4', self.next_headers)
        else:
            # 否则是列表
            temps = []
            for i in html['durl']:
                print(i)
                exit()
                temp = file_name + '/' + part + '.tmp'
                temps.append(temp)
                download(i['url'], temp, self.next_headers)
        return video_list

    @staticmethod
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
