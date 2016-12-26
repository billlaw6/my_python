#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: Stock_CZSC_Analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 14 Dec 2016 07:16:55 PM CST

import tushare as ts
import datetime
import pandas as pd
from sqlalchemy import create_engine, select, insert, update, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, bindparam

from db_core import dal # Data Access Layer
import czsc
from db_core import dal
dal.db_init('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')


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
        sql = """select max(date) as max_date from get_hist_data
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
            hist_data.to_sql('get_hist_data', dal.engine, if_exists='append', index=True)
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
        sql = """select * from get_hist_data
        where code= '%s'
        and date >= '%s' and date <= '%s'
        and ktype= '%s'""" % (self.code, start, end, ktype)
        data = pd.read_sql_query( sql, dal.engine )
        data.set_index('date', drop=False, inplace=True)
        return data

    def czsc_analysis(self):
        d = self.get_hist_data(ktype='D')
        d['date'] = d.index
        d1 = czsc.baohan_process(d)
        d2 = czsc.find_possible_ding_di(d1)
        d3 = czsc.tag_bi_line(d2)
        #d3 = d3[pd.isnull(d3.fenxing)]
        d3 = d3[pd.notnull(d3.fenxing)]
        if len(d3) > 0:
            stmt = dal.get_hist_data.update().\
                where(
                    and_(dal.get_hist_data.c.code == bindparam('s_code'),
                         dal.get_hist_data.c.date == bindparam('p_date'),
                         dal.get_hist_data.c.ktype == bindparam('_ktype')
                        )
                ).\
                values(fenxing = bindparam('fenxing'))
            u_data = []
            tmp = {}
            for i in range(len(d3)):
                tmp['s_code'] = d3.ix[i, 'code']
                tmp['p_date'] = str(d3.ix[i, 'date'])
                tmp['_ktype'] = str(d3.ix[i, 'ktype'])
                tmp['fenxing'] = d3.ix[i, 'fenxing']
                tmp['bi_value'] = str(d3.ix[i, 'bi_value'])
                u_data.append(tmp)
            print(u_data)
            dal.connection.execute(stmt, u_data)

if __name__ == '__main__':
    s = Stock('sh')
    s1 = Stock('002675')

    s.czsc_analysis()
