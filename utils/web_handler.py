# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : web_handler.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/11 1:30
--------------------------------------
"""
from random import choice

import requests
from bs4 import BeautifulSoup as BS

from .constants import Const


class WebHandler:
    """处理网页内容"""
    __agents = {
        'pc': Const.pc_agent.value,
        'phone': Const.phone_agent.value
    }

    __header = Const.headers.value

    bad_str = ('-', '@', ' ', '(', ')', '（', '）')

    def download(self, url: str, encoding: str = 'gb2312'):
        resp = requests.get(url, headers=self.headers)
        resp.encoding = encoding
        return resp.text

    def get_pic(self, url):
        resp = requests.get(url, headers=self.headers)

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

    def get_agent(self, agent_type: str = None) -> str:
        """ 随机生成 user-agent """
        agent_type = agent_type.lower() if agent_type else 'pc'
        agent = choice(self.__agents.get(agent_type))

        return agent

    @property
    def headers(self):
        header = self.__header
        agent = {'User-Agent': self.get_agent()}
        # 请求头
        header.update(agent)

        return header
