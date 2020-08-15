# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : models.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/14 2:19
--------------------------------------
"""
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from .constants import Const

DB_URI = Const.db_uri.value
engine = sqlalchemy.create_engine(DB_URI)
Base = declarative_base()


# 定义映射类User，其继承上一步创建的Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    createdOn = Column(DateTime, server_default=func.now(), comment='创建时间')
    updatedOn = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')  # 时间自动更新


class GirlPics(BaseModel):
    __tablename__ = "GirlPics"
    site_name = Column(String, comment='网站名称')
    site_url = Column(String, comment='网站地址')
    girl_name = Column(String, index=True, comment='模特名称')
    pic_url = Column(String, index=True, comment='图片地址')
    file_path = Column(String, index=True, comment='文件保存地址')


class Progress(BaseModel):
    __tablename__ = "Progress"
    site_name = Column(String, index=True, comment='网站名称')
    page_number = Column(Integer, index=True, default=1, comment='页数')
    girl_number = Column(Integer, index=True, default=1, comment='第几个girl')
    finished = Column(Integer, default=0, comment='0: 下载未完成, 1: 下载完成')


def create_db():
    Base.metadata.create_all(engine)
