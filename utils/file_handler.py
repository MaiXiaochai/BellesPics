# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : file_handler.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/13 23:53
--------------------------------------
"""

from os import makedirs
from os.path import exists

import aiohttp


class FileHandler:
    @staticmethod
    def trans_dir(dir_path: str):
        dir_path = dir_path.replace('\\', '') if '\\' in dir_path else dir_path
        dir_path = dir_path if dir_path.endswith("/") else dir_path + '/'

        return dir_path

    @staticmethod
    def make_dirs(dir_path: str):
        # 如果 log_dir 不存在，则创建
        if not exists(dir_path):
            makedirs(dir_path)

    @staticmethod
    def save_file(file_path: str, content):
        with open(file_path, 'wb') as f:
            f.write(content)

    @staticmethod
    async def __get_content(link):
        async with aiohttp.ClientSession() as session:
            response = await session.get(link)
            content = await response.read()
            return content

    async def download_img(self, db, insert_data):
        url, file_path, girl_name = insert_data.get('pic_url'), insert_data.get('file_path'), insert_data.get('girl_name')

        content = await self.__get_content(url)
        self.save_file(file_path, content)
        db.insert(**insert_data)
