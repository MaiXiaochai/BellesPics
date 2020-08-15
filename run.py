# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : run.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/15 12:50
--------------------------------------
"""
from asyncio import ensure_future, get_event_loop, wait

from utils import logger, WebHandler, FileHandler, DataBase, create_db, cfg
from belles_spider import BellesSpider


def spider(start_url: str, base_url: str, log, data_dir: str):
    file_handler = FileHandler()
    data_dir = file_handler.trans_dir(data_dir)

    web_handler = WebHandler()
    belle_spider = BellesSpider()
    db = DataBase()
    next_id = db.get_next_id()

    soup = web_handler.soup(start_url)
    result = soup.find_all('a', attrs={"target": "_blank"})
    log.debug(f"网站列表 | total:{len(result)} ")

    # 所有分类 (name, url)
    urls = []
    for tag in result:
        tag_url = base_url + tag['href']
        tag_name = web_handler.trans_words(tag.text)
        urls.append((tag_name, tag_url))

    # 进入具体网站
    for site in urls:
        site_name, site_url = site
        log.debug(f"{site_name} | {site_url}")

        # 获取网站最大页数
        site_soup = web_handler.soup(site_url)
        max_number = belle_spider.site_max_page_number(site_soup)
        log.debug(f"{site_name} | total page: {max_number}")

        # 创建网站文件夹
        site_dir = f"{data_dir}{site_name}/"
        file_handler.make_dirs(site_dir)

        # 访问网站具体页面
        for page_nbr in range(1, max_number + 1):
            log.debug(f"{site_name}: {page_nbr}")

            page_url = f"{site[-1]}list_9_{page_nbr}.html"
            page_soup = web_handler.soup(page_url)
            girls = belle_spider.girls_parser(page_soup)
            log.debug(f"{site_name} | {page_nbr} | girls: {len(girls)}")

            for girl_name, girl_url in girls:
                soup = web_handler.soup(girl_url)

                if db.has_girl_name(girl_name):
                    log.debug(f"{girl_name} | existed.")
                    continue

                # 创建 girl 文件夹
                girl_dir = f"{site_dir}{girl_name}/"
                file_handler.make_dirs(girl_dir)

                girl_max_page_nbr = belle_spider.girl_max_page_number(soup)
                log.debug(f"{site_name} | {girl_name} | total number: {girl_max_page_nbr}")
                pic_counter = 0
                girl_page_counter = 0
                tasks = []

                while girl_page_counter <= girl_max_page_nbr:
                    girl_page_counter += 1
                    girl_page_url = girl_url.replace('.html', f'_{girl_page_counter}.html')
                    log.debug(f"{girl_name}: {girl_page_url}")

                    girl_page_soup = web_handler.soup(girl_page_url)
                    pic_urls = belle_spider.pics_parser(girl_page_soup)

                    for pic_url in pic_urls:
                        if db.has_url(pic_url):
                            log.debug(f'existed | {pic_url}')
                            continue

                        file_path = f"{girl_dir}{girl_name}_{pic_counter + 1}.jpg"

                        data = {
                            'id': next_id,
                            'site_name': site_name,
                            'site_url': site_url,
                            'girl_name': girl_name,
                            'pic_url': pic_url,
                            'file_path': file_path
                        }

                        pic_counter += 1
                        next_id += 1

                        tasks.append(
                            ensure_future(file_handler.download_img(pic_counter, db, data, log)
                                          )
                        )

                if tasks:
                    loop = get_event_loop()
                    loop.run_until_complete(wait(tasks))
                    log.debug(f"{site_name}: {girl_name} | saved: {pic_counter}")


def main():
    cfg_log = cfg['log']
    log_dir = cfg_log['log_dir']
    log_name = cfg_log['log_name']

    cfg_site = cfg['site']
    base_url = cfg_site['base_url']
    start_url = cfg_site['start_url']

    data_dir = cfg['data']['data_dir']

    log = logger(log_dir, log_name)

    try:
        create_db()
    except Exception as err:
        log.error(str(err))

    log.debug(f"url: {base_url} | 下载开始.")
    spider(start_url, base_url, log, data_dir)
    log.debug(f"url: {base_url} | 下载结束.")


if __name__ == '__main__':
    main()
