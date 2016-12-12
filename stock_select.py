#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_select.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 07 Nov 2016 10:48:52 AM CST

import tushare as ts
import time
import datetime
from pylab import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.finance as mpf
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import stock_czsc_tools as sct

engine_mysql = create_engine('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')
engine_sqlite = create_engine('sqlite:////test_stocks.db3')

def stock_select_tiantian(totals_limit=15000, reservedPerShare_limit=2, esp_limit=0.5, bvps_limit=0.3):
    """
    总市值 totals*price
    totals 总股本
    totalAssets 总资产(万)
    reserved 公积金
    reservedPerShare 每股公积金
    bvps 每股尽资产
    esp 每股收益
    """
    #stocks = ts.get_stock_basics()
    stocks = pd.read_sql_table('stock_basics', engine)
    return stocks[(stocks.totals < totals_limit) & (stocks.esp > esp_limit) & (stocks.reservedPerShare > reservedPerShare_limit) & (stocks.bvps > bvps_limit)]

def limitup_count_filter(stocks=None, duration=30, count_limit=3, continuous=True):
    """ 找出duration天内连续涨停数大于count数目的股票"""
    d_delta = datetime.timedelta(days=duration)
    now = datetime.datetime.now()
    start = now - d_delta
    start_str = datetime.datetime.strftime(start, '%Y-%m-%d')
    print("start date %s" % start_str)
    print("###########################################################################")
    for stock in stocks.index:
        print("Checking stock %s" % stock)
        count = 0
        hist = pd.read_sql_table('stock_basics', engine)
        if hist is None:
            hist = ts.get_hist_data(stock, start_str).sort_index()
        # hist = ts.get_hist_data('603738', start_str).sort_index()
        for i in range(0, len(hist) - 1):
            if (float(hist[i: i+1].p_change) >= 9.5):
                print("limit up %s " % hist[i: i+1].index[0])
                count = count + 1
            else:
                if continuous:
                    count = 0
                else:
                    pass
            if count >= count_limit:
                print("%s meet count limit: %s " % (stock, hist[i: i+1].index[0]))
                stocks.loc[stock, 'limit_count'] = ('enough %s' % count_limit)
                # continue
                print("###########################################################################")
                break
    return stocks[stocks.limit_count == ('enough %s' % count_limit)]

def fltp_slht_filter(stocks, duration=30):
    d_delta = datetime.timedelta(days=duration)
    now = datetime.datetime.now()
    start = now - d_delta
    start_str = datetime.datetime.strftime(start, '%Y-%m-%d')
    if (stocks is None) or (len(stocks) == 0):
        print("Please choose you stocks")
        exit
    import stock_get_data as sgd
    sgd.get_trade_data(stocks)

def czsc_select(data):
    stocks = ts.get_stock_basics()
    basic_stock_list = stocks[(stocks.totals < totals_limit) & (stocks.esp > esp_limit) & (stocks.reservedPerShare > reservedPerShare_limit) & (stocks.bvps > bvps_limit)]
    today_list = ts.get_today_all()
    test_data.to_sql('sh_test_data', con, if_exists='replace', index=True, dtype={'date': 'CHAR'})
    test_data.to_sql('sh_test_data', engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
                       

def main():
    #selected_stocks = stock_select_tiantian()
    ## Tiantian xuangufa
    ## result = limitup_count_filter(selected_stocks, duration=180, count_limit=5)
    #result = limitup_count_filter(selected_stocks)
    #result[result.industry.str.contains(u'医')]
    #print(result)
    data = ts.get_h_data('002675')
    data = sct.baohan_process(data)
    data = sct.find_possible_ding_di(data)
    data = sct.tag_bi_line(data)
    sct.plot_data(data, single=True)


if __name__ == '__main__':
    main()

