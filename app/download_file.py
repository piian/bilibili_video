import os

import requests
from tqdm import tqdm


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
    # pbar.set_description(file)
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
