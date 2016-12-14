#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: Stock_CZSC_Analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 14 Dec 2016 07:16:55 PM CST

import tushare as ts
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.finance as mpf
import numpy as np
import pandas as pd
import talib as ta
import sqlalchemy
from sqlalchemy import create_engine
from czsc import CZSC

class Stock(object):
    """获取股票数据、分析并将结果存于本地数据库"""
    code = None
    engine = None
    basic_info = None
    hist_data_5 = None
    hist_data_30 = None
    hist_data_D = None
    hist_data_W = None
    hist_data_M = None
    today_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    def __init__(self, code = None, engine = None):
        self.code = code
        if self.code is None:
            self.code = 'sh'
        self.engine = engine
        if self.engine is None:
            self.engine = create_engine('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')

    def localise_hist_data(self, ktype = None):
        """利用tushare获取数据并存到本地数据库 """
        sql = """select max(date) as max_date from stock_hist_data
                where code = '%s'
                and ktype= '%s'""" % (self.code, ktype)

        result = pd.read_sql_query(sql, self.engine)
        # pandas Timestamp
        max_date_ts = result.ix[0, 0]
        max_date = max_date_ts.to_datetime()
        delta = datetime.timedelta(seconds=1)
        start_date = str(max_date + delta)
        if (start_date is not None and start_date != 'None'):
            hist_data = ts.get_hist_data(code = self.code, start=start_date, ktype=ktype)
        else:
            hist_data = ts.get_hist_data(code = self.code, ktype=ktype)
        hist_data['code'] = self.code
        hist_data['ktype'] = ktype
        try:
            hist_data.to_sql('stock_hist_data', self.engine, if_exists='append', index=True, dtype={'date': sqlalchemy.types.DateTime,'code': sqlalchemy.types.CHAR(6),'ktype': sqlalchemy.types.CHAR(10)})
        except Exception as e:
            raise e

    def prepare_hist_data(self, ktypes = ['5', '30', 'D']):
        """利用tushare获取数据并存到本地数据库 """
        for ktype in ktypes:
            try:
                self.localise_hist_data(self.code, ktype)
            except Exception as e:
                raise e

    def get_hist_data_5(self):
        return self.hist_data_5


