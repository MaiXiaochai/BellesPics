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
    def download(url: str, encoding: str = 'utf-8'):
        resp = requests.get(url)
        resp.encoding = encoding
        return resp.text

    @staticmethod
    def parser(resp):
        soup = BS(resp, 'lxml')

        return soup

    def trans_words(self, words: str) -> str:
        for i in self.bad_str:
            words = words.replace(i, '_')

        return words
