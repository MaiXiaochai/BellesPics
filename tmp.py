# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : tmp.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/15 19:40
--------------------------------------
"""
from utils import BaseProxySpider


def proxy_spider():
    ps = BaseProxySpider()
    ps.get_proxy()


if __name__ == '__main__':
    proxy_spider()
