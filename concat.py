import requests

from download_file import download


def get_range(base_url):
    headers = get_headers(10)
    response = requests.get(url=base_url, headers=headers, stream=True, verify=False)
    if response.status_code == 206:
        range = response.headers['Content-Range'].split('/')[-1]
        return int(range)


def get_headers(max=0, min=0):
    fun_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Sec-Fetch-Mode': 'cors'
    }
    if max > 0:
        fun_headers['Range'] = 'bytes=' + str(min) + '-' + str(max)

    return fun_headers


if __name__ == '__main__':
    url = 'http://cn-zjnb-cmcc-v-02.acgvideo.com/upgcxcode/84/69/56276984/56276984-1-30064.m4s?expires=1571213700&platform=pc&ssig=ZRopbRYJFFXL_CuLY-NTnA&oi=3086393504&trid=0c048e40623946ba9dd12544ee3a53fcu&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&mid=0'
    name = 'temp/test.zip'

    headers = get_headers(0, 2000)
    download(url, name, headers)
