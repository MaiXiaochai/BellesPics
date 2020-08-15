# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : config_parser.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/15 12:44
--------------------------------------
"""
from toml import load


def parser(file_path):
    data = load(file_path, _dict=dict)

    return data


cfg_path = 'config.toml'
cfg = parser(cfg_path)
