#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: Stock_CZSC_Analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 14 Dec 2016 07:16:55 PM CST

import tushare as ts
import datetime
import pandas as pd
from sqlalchemy import create_engine, select, insert, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from db_core import dal # Data Access Layer
import czsc


class Stock(object):
    """获取股票数据、分析并将结果存于本地数据库"""
    code = None
    data_layer = None
    basic_info = None
    hist_data_5 = None
    hist_data_30 = None
    hist_data_D = None
    hist_data_W = None
    hist_data_M = None

    def __init__(self, code = None):
        self.code = code
        if self.code is None:
            self.code = 'sh'

        dal.db_init('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')
        self._prepare_hist_data()

    def _localise_hist_data(self, ktype = None):
        """利用tushare获取数据并存到本地数据库 """
        sql = """select max(date) as max_date from stock_hist_data
                where code = '%s'
                and ktype= '%s'""" % (self.code, ktype)
        result = pd.read_sql_query(sql, dal.engine)
        # pandas Timestamp
        max_date_ts = result.ix[0, 0]
        if (max_date_ts is not None and max_date_ts != 'None'):
            max_date = max_date_ts.to_pydatetime()
            delta = datetime.timedelta(seconds=1)
            start_date = str(max_date + delta)
            hist_data = ts.get_hist_data(code = self.code, start=start_date, ktype=ktype)
        else:
            hist_data = ts.get_hist_data(code = self.code, ktype=ktype)
        hist_data['code'] = self.code
        hist_data['ktype'] = ktype
        try:
            hist_data.to_sql('stock_hist_data', dal.engine, if_exists='append', index=True)
        except Exception as e:
            raise e

    def _prepare_hist_data(self, ktypes = ['5', '30', 'D']):
        """利用tushare获取数据并存到本地数据库 """
        for ktype in ktypes:
            try:
                self._localise_hist_data(ktype)
            except Exception as e:
                raise e

    def get_hist_data(self, start = None, end = None, ktype = '30'):
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
        data = pd.read_sql_query( sql, dal.engine )
        data = data.set_index('date')
        return data

    def czsc_analysis(self):
        d = self.get_hist_data()
        d1 = czsc.baohan_process(d)
        d2 = czsc.find_possible_ding_di(d1)
        d3 = czsc.tag_bi_line(d2)
        d4 = czsc.tag_duan_line(d3)
        print(d4)

if __name__ == '__main__':
    s = Stock('sh')
    s1 = Stock('002675')

    s.czsc_analysis()
