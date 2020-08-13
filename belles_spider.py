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

    def page_parser(self, soup) -> list:
        """ 解析单个页面中的美女列表"""
        tag_a = soup.select('.m-list > ul > li > a')
        urls = [(self.trans_words(x['title']), x['href']) for x in tag_a]

        return urls


def spider(start_url: str, base_url: str):
    web_handler = WebHandler()
    belle_spider = BellesSpider()

    soup = web_handler.soup(start_url)
    result = soup.find_all('a', attrs={"target": "_blank"})

    # 所有分类 (name, url)
    urls = []
    for tag in result:
        tag_url = base_url + tag['href']
        tag_name = web_handler.trans_words(tag.text)
        urls.append((tag_name, tag_url))

    # 进入具体网站
    for site in urls:
        # 获取网站最大页数
        site_soup = web_handler.soup(site[-1])
        max_number = belle_spider.site_max_page_number(site_soup)

        # 访问网站具体页面
        for page_nbr in range(1, max_number + 1):
            page_url = f"{site[-1]}list_9_{page_nbr}.html"

            page_soup = web_handler.soup(page_url)
            girls = belle_spider.page_parser(page_soup)

            for girl_name, girl_url in girls:
                girl_page_counter = 1
                girl_max_page_nbr = 6

                soup = web_handler.soup(girl_url)
                girl_max_page_nbr = belle_spider.girl_max_page_number(soup)
                break
                # while girl_page_counter < girl_max_page_nbr:
                #     if girl_page_counter == 1:
                #         pass



            break
        break


def main():
    start_url = 'https://www.ku137.net/b/tag/'
    base_url = 'https://www.ku137.net'
    spider(start_url, base_url)


if __name__ == '__main__':
    main()
