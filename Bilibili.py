import json
import math
import os
import re
import sys
import threading

import requests
from bs4 import BeautifulSoup

from download_file import download


class Bilibili:
    def __init__(self):
        requests.packages.urllib3.disable_warnings()

    @staticmethod
    def get_url(response):
        """
        解析返回的数据，获取将要下载的视频
        :param response:
        :return:
        """
        pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
        temp = json.loads(re.findall(pattern, response.text)[0])
        if 'dash' in temp['data']:
            video_url = temp['data']['dash']['video'][0]['baseUrl']
            audio_url = temp['data']['dash']['audio'][0]['baseUrl']
            return {'video_url': video_url, 'audio_url': audio_url}
        else:
            return None

    @staticmethod
    def get_headers(max=0, min=0):
        """
        生成请求头部
        :param max:
        :param min:
        :return:
        """
        fun_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Referer': 'https://www.bilibili.com',
            'Origin': 'https://www.bilibili.com',
            'Sec-Fetch-Mode': 'cors'
        }
        if max > 0:
            fun_headers['Range'] = 'bytes=' + str(min) + '-' + str(max)

        return fun_headers

    def get_range(self, base_url):
        """
        获取资源总大小
        :param base_url:
        :return:
        """
        headers = self.get_headers(10)
        response = requests.get(url=base_url, headers=headers, stream=True, verify=False)
        if response.status_code == 206:
            range = response.headers['Content-Range'].split('/')[-1]
            return int(range)

    def thread_file(self, base_url, range_min, range_max, file_name):
        """
        任务主体
        :param base_url:
        :param range_min:
        :param range_max:
        :param file_name:
        """
        headers = self.get_headers(range_max, range_min)
        download(base_url, file_name, headers)

    def load(self, url):
        """
        主下载方法
        :param url:
        """
        headers = self.get_headers()
        response = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, 'html5lib')
        title = soup.find('title').text.split('_')[0]

        urls = self.get_url(response)
        if urls is None:
            raise TypeError('不是常规哔哩哔哩视频')

        # 获取线程数
        m = 5 if len(sys.argv) < 3 else int(sys.argv[2])

        video = self.get_video(urls['video_url'], title, m)
        audio = self.get_audio(urls['audio_url'], title)

        self.merge_video(audio, title, video)
        print(title + '下载成功')

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

    def get_video(self, base_url, title, m=5):
        """
        获取视频
        :param base_url:
        :param title:
        :param m:
        :return:
        """
        file_name = title + 'video' + '.mp4'
        range_length = self.get_range(base_url)
        size = math.ceil(range_length / m)
        lists = [[size * i, ((i + 1) * size - 1)] for i in range(m)]
        lists[-1][1] = range_length

        threads = []
        files = []
        i = 1
        for range_arr in lists:
            # 创建新线程
            temp_name = '/tmp/' + file_name + '.tmp' + str(i)
            files.append(temp_name)
            i += 1
            # thread_file(base_url, range_arr[0], range_arr[1], filename)
            thread1 = threading.Thread(target=self.thread_file, args=(base_url, range_arr[0], range_arr[1], temp_name,))
            thread1.start()
            threads.append(thread1)

        # # 等待所有线程完成
        for t in threads:
            t.join()
        return self.concat_video(files, file_name)

    @staticmethod
    def concat_video(files, file_name):
        """
        合并缓存视频
        :param files:
        :param file_name:
        :return:
        """
        file_str = '|'.join(str(i) for i in files)
        ffmpeg_cmd = 'ffmpeg -y -i "concat:' + file_str + '" -c copy ' + file_name
        os.system(ffmpeg_cmd)
        for file in files:
            os.remove(file)
        return file_name

    def get_audio(self, base_url, title):
        """
        获取音频
        :param base_url:
        :param title:
        :return:
        """
        file_name = title + '.mp3'
        range_length = self.get_range(base_url)
        headers = self.get_headers(range_length)
        response = requests.get(url=base_url, headers=headers, stream=True, verify=False)
        filename = '/tmp/' + file_name + '.tmp'
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
