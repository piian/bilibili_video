import hashlib
import os

import requests
from tqdm import tqdm


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
            self.download(html['durl'][0]['url'], file_name + '/' + part + '.mp4', self.next_headers)
        else:
            # 否则是列表
            temps = []
            for i in html['durl']:
                print(i)
                exit()
                temp = file_name + '/' + part + '.tmp'
                temps.append(temp)
                self.download(i['url'], temp, self.next_headers)
        return video_list

    @staticmethod
    def download(url, file, headers):
        """
        下载文件、写入文件到缓存文件、显示当前进度
        :param url:
        :param file:
        :param headers:
        """
        r = requests.get(url, headers=headers, stream=True, timeout=5)
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
