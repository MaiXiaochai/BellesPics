# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : proxy.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/15 19:06
--------------------------------------
"""
from re import compile

import requests
from .web_handler import WebHandler


class BaseProxySpider(WebHandler):
    __rule_ip = compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
    __rule_port = compile(r"<td>(\d+)</td>")
    __test_url = 'http://www.baidu.com'

    base_url = "http://www.66ip.cn/{}.html"

    def __init__(self, max_page: int = None):
        self.max_page = max_page or 5

    def proxy_parser(self, url):
        soup = self.soup(url)
        content = soup.select('table[border="2px"] > tr')

        result = []
        for i in content[1: -1]:
            s = str(i)
            ip = self.__rule_ip.findall(s)[0]
            port = self.__rule_port.findall(s)[0]

            result.append(
                (ip, int(port))
            )

        return result

    def get_proxy(self):
        proxy_data = []
        for i in range(1, self.max_page + 1):
            url = self.base_url.format(i)
            proxy = self.proxy_parser(url)
            proxy_data += proxy

        print(f"Total: {len(proxy_data)}")
        for idx, item in enumerate(proxy_data, 1):
            ip, port = item
            result = self.test_proxy(ip, port)
            print(f"[ {idx} ][ {ip} ][ {port} ][ {result} ]")

    def test_proxy(self, ip: str, port: int or str):
        proxies = {
            'http': f'http://{ip}:{port}',
            'https': f'https://{ip}:{port}'
        }
        try:
            resp = requests.get(self.__test_url, headers=self.headers, proxies=proxies)
            code = resp.status_code

        except Exception as err:
            code = -1

        return code == 200
