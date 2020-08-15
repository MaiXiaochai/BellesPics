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

from utils import logger, WebHandler, FileHandler, PicsTable, ProgressTable, create_db, cfg
from belles_spider import BellesSpider


def spider(start_url: str, base_url: str, log, data_dir: str):
    file_handler = FileHandler()
    data_dir = file_handler.trans_dir(data_dir)

    web_handler = WebHandler()
    belle_spider = BellesSpider()

    db_pic = PicsTable()
    next_id_pic = db_pic.get_next_id()
    db_pro = ProgressTable()

    soup = web_handler.soup(start_url)
    result = soup.find_all('a', attrs={"target": "_blank"})
    site_length = len(result)
    log.info(f"网站总数: {site_length}")

    # 所有分类 (name, url)
    urls = []
    for tag in result:
        tag_url = base_url + tag['href']
        tag_name = web_handler.trans_words(tag.text)
        urls.append((tag_name, tag_url))

    # 进入具体网站
    for site_idx, site in enumerate(urls, 1):
        site_name, site_url = site
        log.debug(f"{site_name} | {site_url}")

        # 如果下载进度表中没有该网站，则插入信息
        if not db_pro.has_site(site_name):
            site_data = {
                'site_name': site_name,
                'page_number': 0,
                'girl_number': 0
            }
            db_pro.insert(**site_data)

        else:
            finished = db_pro.get_value(site_name, 'finished') == 1

            if finished:
                log.info(f"{site_name}: finished.")
                continue

        # 获取网站最大页数
        site_soup = web_handler.soup(site_url)
        max_page_number = belle_spider.site_max_page_number(site_soup)
        log.info(f"{site_name} | total page: {max_page_number}")

        # 创建网站文件夹
        site_dir = f"{data_dir}{site_name}/"
        file_handler.make_dirs(site_dir)

        # 访问网站具体页面
        start_page_number = db_pro.get_value(site_name, 'page_number')
        log.info(f"Download from: {site_name}: {start_page_number}/{max_page_number}")

        for page_nbr in range(start_page_number, max_page_number + 1):
            page_url = f"{site[-1]}list_9_{page_nbr}.html"
            page_soup = web_handler.soup(page_url)
            girls = belle_spider.girls_parser(page_soup)
            girls_length = len(girls)

            start_girl_number = db_pro.get_value(site_name, 'girl_number')

            for girl_idx, girl_item in enumerate(girls, 1):
                girl_name, girl_url = girl_item
                soup = web_handler.soup(girl_url)

                # girl_idx < start_gir_number 说明已经下载完了
                if girl_idx < start_girl_number:
                    continue

                # 创建 girl 文件夹
                girl_dir = f"{site_dir}{girl_name}/"
                file_handler.make_dirs(girl_dir)

                girl_max_page_nbr = belle_spider.girl_max_page_number(soup)
                log.debug(f"{girl_name} | Pages: {girl_max_page_nbr} | parsing ...")

                pic_counter = 0
                girl_page_counter = 0
                tasks = []

                while girl_page_counter <= girl_max_page_nbr:
                    girl_page_counter += 1
                    girl_page_url = girl_url.replace('.html', f'_{girl_page_counter}.html')

                    girl_page_soup = web_handler.soup(girl_page_url)
                    pic_urls = belle_spider.pics_parser(girl_page_soup)

                    for pic_url in pic_urls:
                        if db_pic.has_url(pic_url):
                            log.debug(f'existed | {pic_url}')
                            continue

                        file_path = f"{girl_dir}{girl_name}_{pic_counter + 1}.jpg"

                        data = {
                            'id': next_id_pic,
                            'site_name': site_name,
                            'site_url': site_url,
                            'girl_name': girl_name,
                            'pic_url': pic_url,
                            'file_path': file_path
                        }

                        pic_counter += 1
                        next_id_pic += 1

                        tasks.append(
                            ensure_future(file_handler.download_img(db_pic, data)
                                          )
                        )
                log.debug(f"{girl_name} | Pages: {girl_max_page_nbr} | parsed")
                if tasks:
                    log.info(f"{site_name} | {site_idx}/{site_length} | {page_nbr}/{max_page_number}-{girl_idx}/{girls_length} | {girl_name} | {pic_counter} | downloading ...")
                    loop = get_event_loop()
                    loop.run_until_complete(wait(tasks))
                    log.info(f"{site_name} | {site_idx}/{site_length} | {page_nbr}/{max_page_number}-{girl_idx}/{girls_length} | {girl_name} | {pic_counter} | saved.")

                # 如果 girl_idx > 保存在进度中的 start_girl_number, 更新
                if girl_idx > start_girl_number:
                    db_pro.update(site_name, girl_number=girl_idx)

            # 如果 page_nbr > 保存在进度中的 start_page_number, 更新
            if page_nbr > start_page_number:
                db_pro.update(site_name, page_number=page_nbr)

        # 该网站下载完成
        db_pro.update(site_name, finished=1)
        log.info(f"{site_name}: finished.")


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
