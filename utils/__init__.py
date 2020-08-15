# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : __init__py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/11 1:29
--------------------------------------
"""
from .web_handler import WebHandler
from .logger import logger
from .file_handler import FileHandler
from .models import GirlPics, Progress, create_db
from .sqlite_utils import PicsTable, ProgressTable
from .constants import Const
from .config_parser import parser

cfg = parser(Const.cfg_path.value)
