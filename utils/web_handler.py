# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : web_handler.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/11 1:30
--------------------------------------
"""

import requests
from bs4 import BeautifulSoup as BS


class WebHandler:
    """处理网页内容"""

    bad_str = ('-', '@', ' ', '(', ')', '（', '）')

    @staticmethod
    def download(url: str, encoding: str = 'gb2312'):
        resp = requests.get(url)
        resp.encoding = encoding
        return resp.text

    @staticmethod
    def get_pic(url):
        resp = requests.get(url)

        return resp.content

    @staticmethod
    def parser(resp):
        soup = BS(resp, 'lxml')

        return soup

    def soup(self, url: str):
        resp = self.download(url)
        soup_ = self.parser(resp)

        return soup_

    def trans_words(self, words: str) -> str:
        for i in self.bad_str:
            words = words.replace(i, '_')

        return words
