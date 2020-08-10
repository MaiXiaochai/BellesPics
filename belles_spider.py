# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : belles_spider.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/11 1:30
--------------------------------------
"""

from utils import WebHandler


def spider(start_url: str, base_url: str):
    encoding = 'gb2312'
    wh = WebHandler()
    resp = wh.download(start_url, encoding)
    soup = wh.parser(resp)
    result = soup.find_all('a', attrs={"target": "_blank"})

    urls = []
    for i in result:
        tag_url = base_url + i['href']
        tag_name = wh.trans_words(i.text)
        urls.append((tag_name, tag_url))

    for j in urls:
        print(j)


def main():
    start_url = 'https://www.ku137.net/b/tag/'
    base_url = 'https://www.ku137.net'
    spider(start_url, base_url)


if __name__ == '__main__':
    main()
