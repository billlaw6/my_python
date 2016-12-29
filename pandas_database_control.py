#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: pandas_database_control.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Tue 13 Dec 2016 09:38:57 AM CST

import tushare as ts # 0.4.3 version
import datetime
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd

var_names = locals()
today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
engine = create_engine('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')
# engine = create_engine('sqlite:////db_name.sqlite')
# engine = create_engine('sqlite:////:memory:')

def localise_data_for_select():
    """ """
    basics = ts.get_stock_basics()
    #basics.to_sql('stock_basics', engine, if_exists='fail', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
    try:
        basics.to_sql('stock_basics', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
    except Exception as e:
        print(e)
    today_data = ts.get_today_all()
    today_data['date'] = today
    try:
        today_data.to_sql('today_data', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
    except Exception as e:
        print(e)


def localise_trade_hist_data(code, ktype):
    """ """
    sql = """select max(date) as max_date from stock_hist_data
            where code = '%s'
            and ktype= '%s'""" % (code, ktype)

    result = pd.read_sql_query(sql, engine)
    # pandas Timestamp
    max_date_ts = result.ix[0, 0]
    max_date = max_date_ts.to_datetime()
    delta = datetime.timedelta(seconds=1)
    start_date = str(max_date + delta)
    if (start_date is not None and start_date != 'None'):
        hist_data = ts.get_hist_data(code=code, start=start_date, ktype=ktype)
    else:
        hist_data = ts.get_hist_data(code=code, ktype=ktype)
    hist_data['code'] = code
    hist_data['ktype'] = ktype
    try:
        hist_data.to_sql('stock_hist_data', engine, if_exists='append', index=True, dtype={'date': sqlalchemy.types.DateTime,'code': sqlalchemy.types.CHAR(6),'ktype': sqlalchemy.types.CHAR(10)})
    except Exception as e:
        print(e)

def main():
    # code = '002675'
    # ktype = '5'
    # hist_data = ts.get_hist_data(code, ktype=ktype)
    # hist_data['code'] = code
    # hist_data['ktype'] = ktype
    # try:
        # hist_data.to_sql('stock_hist_data', engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.DateTime,'code': sqlalchemy.types.CHAR(6),'ktype': sqlalchemy.types.CHAR(10)})
    # except Exception as e:
        # print(e)

    localise_data_for_select()
    # localise_trade_hist_data('002675', 'D')
    localise_trade_hist_data('002675', '30')
    localise_trade_hist_data('002675', '5')

if __name__ == '__main__':
    main()
