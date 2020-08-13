# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : sqlite_utils.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/8/14 2:21
--------------------------------------
"""

from sqlalchemy.orm import sessionmaker

from .models import engine, GirlPics


class DataBase:
    def __init__(self):
        # 统一使用同一个变量，便于维护
        self.tb_data = GirlPics
        self.tv_data_keys = ["id", "site_name", "site_url", "girl_name", "pic_url", "file_path"]
        sess = sessionmaker(bind=engine)
        self.session = sess()

    def get_next_id(self) -> int:
        """获取最大值"""
        row = self.session.query(self.tb_data).order_by(self.tb_data.id.desc()).first()
        next_id = (row.id + 1) if row else 1

        return next_id

    def insert(self, **kwargs):
        """插入数据"""
        tb_data = self.tb_data()

        for k in self.tv_data_keys:
            if k in kwargs:
                v = kwargs.get(k)
                setattr(tb_data, k, v)

        self.session.add(tb_data)
        self.commit()

    def has_url(self, pic_url: str) -> bool:
        """通过判断MD5值，确定视频是否存在"""
        row = self.session.query(self.tb_data).filter(self.tb_data.pic_url == pic_url).first()
        result = True if row else False

        return result

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    def __del__(self):
        self.close()
