# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : belles_spider.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/11 1:30
--------------------------------------
"""
import re

from utils import WebHandler


class BellesSpider(WebHandler):
    """ url带名字的信息，格式为 (name, url)"""

    @staticmethod
    def site_max_page_number(soup) -> int:
        """获取网页的最大页数 """
        page_content = soup.find_all('span', class_='pageinfo')
        max_number = page_content[0].strong.text

        return int(max_number)

    @staticmethod
    def girl_max_page_number(soup):
        """ 获取具体图片页面的最大页数"""
        number = soup.select('.page > a')[0].text
        number = re.findall(r'\d+', number)[0]

        return int(number)

    @staticmethod
    def get_full_girl_name(soup):
        content = soup.select(".content > img")[0]['alt']

        return content

    def girls_parser(self, soup) -> list:
        """ 解析单个页面中的美女列表"""
        tag_a = soup.select('.m-list > ul > li > a')
        urls = [(self.trans_words(x['title']), x['href']) for x in tag_a]

        return urls

    @staticmethod
    def pics_parser(soup) -> list:
        """ 解析图片 url"""
        pics = soup.select('.content > img')
        urls = [x['src'] for x in pics]

        return urls

    @staticmethod
    def get_tag_number(url: str) -> int:
        sep = '/'
        url = url if url.endswith(sep) else f"{url}{sep}"
        number = url.split(sep)[-2]

        return int(number)


class Spider(BellesSpider):
    """ 用于流程的spider"""

    def get_all_sites(self, url) -> list:
        soup = self.soup(url)
        result = soup.find_all('a', attrs={"target": "_blank"})

        # 所有分类 (name, url)
        urls = []
        for tag in result:
            tag_url = url + tag['href']
            tag_name = self.trans_words(tag.text)
            urls.append((tag_name, tag_url))

        return result

    def get_girls_on_page(self, url):
        pass
