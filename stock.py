#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: Stock_CZSC_Analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 14 Dec 2016 07:16:55 PM CST

import tushare as ts
import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

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
        self._prepare_hist_data()

    def _localise_hist_data(self, ktype = None):
        """利用tushare获取数据并存到本地数据库 """
        sql = """select max(date) as max_date from stock_hist_data
                where code = '%s'
                and ktype= '%s'""" % (self.code, ktype)
        result = pd.read_sql_query(sql, self.engine)
        # pandas Timestamp
        max_date_ts = result.ix[0, 0]
        if (max_date_ts is not None and max_date_ts != 'None'):
            max_date = max_date_ts.to_datetime()
            delta = datetime.timedelta(seconds=1)
            start_date = str(max_date + delta)
            hist_data = ts.get_hist_data(code = self.code, start=start_date, ktype=ktype)
        else:
            hist_data = ts.get_hist_data(code = self.code, ktype=ktype)
        hist_data['code'] = self.code
        hist_data['ktype'] = ktype
        hist_data['type'] = None
        hist_data['fenxing'] = None
        hist_data['bi_value'] = None
        hist_data['duan_value'] = None
        try:
            hist_data.to_sql('stock_hist_data', self.engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.DateTime,'code': sqlalchemy.types.CHAR(6),'ktype': sqlalchemy.types.CHAR(10),'type': sqlalchemy.types.CHAR(10),'fenxing': sqlalchemy.types.CHAR(10),'bi_value': sqlalchemy.types.Float,'duan_value': sqlalchemy.types.Float})
        except Exception as e:
            raise e

    def _prepare_hist_data(self, ktypes = ['5', '30', 'D']):
        """利用tushare获取数据并存到本地数据库 """
        for ktype in ktypes:
            try:
                self._localise_hist_data(ktype)
            except Exception as e:
                raise e

    def get_hist_data(self, start = None, end = None, ktype = None):
        """Get data from local database"""
        if start is None:
            now = datetime.datetime.now()
            delta = datetime.timedelta(days = 7)
            start = str(now - delta)
            start = datetime.datetime.strftime(now - delta, '%Y-%m-%d %H:%M:%S')
        if end is None:
            end = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql = """select * from stock_hist_data
        where code= '%s'
        and date >= '%s' and date <= '%s'
        and ktype= '%s'""" % (self.code, start, end, ktype)
        data = pd.read_sql_query( sql, self.engine )
        return data

