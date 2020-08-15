# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : db_utils.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/14 2:21
--------------------------------------
"""

from sqlalchemy.orm import sessionmaker

from .models import engine, GirlPics, Progress, Proxy


class BaseDataBase:
    table_names = {
        'pic': GirlPics,
        'pro': Progress,
        'proxy': Proxy
    }

    def __init__(self, table_name: str):
        # 统一使用同一个变量，便于维护
        table_name = table_name.lower().strip()
        self.table_name = self.table_names.get(table_name)

        sess = sessionmaker(bind=engine)
        self.session = sess()

    def get_next_id(self) -> int:
        """获取最大 id 值"""
        row = self.session.query(self.table_name).order_by(self.table_name.id.desc()).first()
        next_id = (row.id + 1) if row else 1

        return next_id

    def insert(self, **kwargs):
        """插入数据"""
        tb_data = self.table_name()

        for k in kwargs:
            v = kwargs.get(k)
            setattr(tb_data, k, v)

        self.session.add(tb_data)
        self.commit()

    def update(self, query_key: str, query_value, **kwargs):
        row = self.session.query(self.table_name).filter(getattr(self.table_name, query_key) == query_value).first()
        for k in kwargs:
            v = kwargs.get(k)
            setattr(row, k, v)
            self.commit()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    def __del__(self):
        self.close()


class PicsTable(BaseDataBase):
    """ 图片信息的一些方法 """

    def __init__(self):
        super().__init__('pic')

    def has_url(self, pic_url: str) -> bool:
        """判断该张图片是否已经下载"""
        row = self.session.query(self.table_name).filter(self.table_name.pic_url == pic_url).first()
        result = True if row else False

        return result

    def has_girl_name(self, girl_name: str) -> bool:
        """判断该美女的图片是否已经下载"""
        row = self.session.query(self.table_name).filter(self.table_name.girl_name == girl_name).first()
        result = True if row else False

        return result


class ProgressTable(BaseDataBase):
    """ 进度表的一些方法 """

    def __init__(self):
        super().__init__('pro')

    def has_site(self, site_name: str) -> bool:
        """判断该张图片是否已经下载"""
        row = self.session.query(self.table_name).filter(self.table_name.site_name == site_name).first()
        result = True if row else False

        return result

    def get_value(self, site_name, column: str) -> int:
        """ 获取数值 """
        row = self.session.query(self.table_name).filter(self.table_name.site_name == site_name).first()
        result = getattr(row, column)

        return result


class ProxyDB(BaseDataBase):
    def __init__(self):
        super().__init__('proxy')

