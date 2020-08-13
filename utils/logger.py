# -*- coding: utf-8 -*-

"""
---------------------------------------
@File       : logger.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/7/9 11:28
---------------------------------------
"""

from os import makedirs
from os.path import basename, exists
from logging.handlers import RotatingFileHandler
from logging import getLogger, StreamHandler, Formatter, DEBUG


def logger(log_dir: str = None, file_name: str = None, back_count: int = None, log_size: float or int = None):
    log_dir = log_dir or 'logs'
    file_name = file_name or (basename(__file__).split('.')[0] + '.log')
    back_count = back_count or 8
    log_size = (log_size or 512) * 1024 ** 2

    log_dir = log_dir if log_dir.endswith("/") else log_dir + '/'
    log_file_path = f"{log_dir}{file_name}"

    # 如果 log_dir 不存在，则创建
    if not exists(log_dir):
        makedirs(log_dir)

    logger_ = getLogger(file_name)

    handler1 = StreamHandler()
    handler2 = RotatingFileHandler(filename=log_file_path, maxBytes=log_size, backupCount=back_count, encoding="utf-8")

    logger_.setLevel(DEBUG)
    handler1.setLevel(DEBUG)
    handler2.setLevel(DEBUG)

    formatter = Formatter("[ %(asctime)s ][ %(levelname)s ][ %(filename)s:%(funcName)s ][ %(message)s ]")
    handler1.setFormatter(formatter)
    handler2.setFormatter(formatter)

    logger_.addHandler(handler1)
    logger_.addHandler(handler2)

    return logger_
