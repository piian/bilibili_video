import hashlib
import os

import requests
from tqdm import tqdm
from model import PlayList, Video


class Bilibili:
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
    appkey = 'iVGUTjsxvpLeuDCf'  # appkey
    sec = 'aHRmhWMLkdeMuILqORnYZocwMBpMEOdt'  # 秘钥

    def get_list(self, cid):
        info = self.get_info(cid)
        title = info['title']
        # 标题
        print(title)
        print('一共' + str(len(info['pages'])) + '视频')
        for vid in info['pages']:
            # 打印当前视频标题
            print(vid['part'])
            self.get_url(vid['cid'], vid['part'], title)

    def get_list_by_mid(self, mid):
        start_url = ""
        response = requests.get(start_url).json()
        print(response)

    @staticmethod
    def get_info(cid):
        """获取视频信息"""
        start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + cid
        response = requests.get(start_url).json()
        download_path = "downloads"
        title = response['data']['title']
        if os.path.exists(download_path) is False:
            os.mkdir(download_path)
        title = download_path + '/' + title
        pages = response['data']['pages']
        if os.path.exists(title) is False:
            os.mkdir(title)
        return {'title': title, "pages": [{'part': page['part'], 'cid': page['cid']} for page in pages]}

    def make_params(self, params):
        base = {
            'appkey': self.appkey,
            "otype": "json"
        }
        params.update(base)
        params = sorted(params.iteritems(), key=lambda d: d[0])
        list = "&".join([i+"="+str(params.get(i)) for i in params])
        sign = hashlib.md5(bytes(list + self.sec, 'utf8')).hexdigest()
        return list + "&sign="+sign

    def get_play_url_by_cid(self, cid):
        params = self.make_params({"cid": cid, "qn": 80, "quality": 80})
        print(params)
        return 'https://interface.bilibili.com/v2/playurl?' + params

    def get_response_by_cid(self, cid):
        url_api = self.get_play_url_by_cid(cid)
        headers = {
            'Referer': 'www.bilibili.com',  # 注意加上referer
        }
        html = requests.get(url_api, headers=headers).json()
        return html

    def get_url(self, cid, filename, path):
        """获取每个链接并下载"""
        html = self.get_response_by_cid(cid=cid)
        print(html)
        video_list = []
        if len(html['durl']) == 1:
            # 如果只有一个链接，则表示单视频
            print(html['durl'][0])
            Video.update(size=html['durl'][0]['size']).where(Video.cid==cid).execute()
            self.download(html['durl'][0]['url'], path +
                          '/' + filename + '.mp4', self.next_headers)
        else:
            # 否则是列表
            temps = []
            for i in html['durl']:
                print(i)
                exit()
                temp = path + '/' + filename + '.tmp'
                temps.append(temp)
                self.download(i['url'], temp, self.next_headers)
        return video_list

    @staticmethod
    def check_exists(file):
        exists = os.path.exists(file)
        if exists:
            return True
        else:
            return False

    @staticmethod
    def get_view_by_bvid(bvid):
        start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + str(bvid)
        return requests.get(start_url).json()

    @staticmethod
    def search_by_mid(mid):
        url = "https://api.bilibili.com/x/space/arc/search?mid=" + mid
        return requests.get(url).json()

    @staticmethod
    def download(url, file, headers):
        """
        下载文件、写入文件到缓存文件、显示当前进度
        :param url:
        :param file:
        :param headers:
        """
        r = requests.get(url, headers=headers, stream=True, timeout=50)
        # 获取总长度
        length = r.headers['Content-Length']
        exists = os.path.exists(file)
        if exists:
            size = os.path.getsize(file)
            if size == int(length):
                print("已存在文件，并且大小一致，跳过下载")
                return
        # 打开文件
        f = open(file, 'wb')
        # 初始化进度条并设置标题
        pbar = tqdm(total=int(length))
        for chunk in r.iter_content(chunk_size=2048):
            if chunk:
                # 进度条更新每次数据的长度
                pbar.update(len(chunk))
                # 写入到文件里
                f.write(chunk)
        # 关闭进度条
        pbar.close()
        # 关闭文件
        f.close()

    def download_by_id(self, video_id):
        video = Video.select().where(Video.id == video_id).first()
        play = PlayList.select().where(PlayList.id == video.play_list_id).first()

        print("开始下载" + video.title + "，视频集：" + play.title)
        download_path = 'downloads/' + play.title
        if os.path.exists(download_path) is False:
            os.mkdir(download_path)
        self.get_url(video.cid, video.title, download_path)
if __name__ == '__main__':
    client = Bilibili()
    client.make_params({"cid":1,"qn":80, "quality":80})
