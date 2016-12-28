#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_select.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 07 Nov 2016 10:48:52 AM CST

import tushare as ts
import datetime
import pandas as pd
from sqlalchemy import select, and_

from db_core import dal
dal.db_init()


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
    stocks = pd.read_sql_table('get_stock_basics', dal.engine)
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
        hist = pd.read_sql_table('get_stock_basics', dal.engine)
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

def fltp_slht_select(stocks, duration=30):
    d_delta = datetime.timedelta(days=duration)
    now = datetime.datetime.now()
    start = now - d_delta
    start_str = datetime.datetime.strftime(start, '%Y-%m-%d')
    if (stocks is None) or (len(stocks) == 0):
        print("Please choose you stocks")
        exit
    import stock_get_data as sgd
    sgd.get_trade_data(stocks)

def basic_select():
    s = select([dal.get_stock_basics, dal.get_today_all]).\
            where( and_((dal.get_stock_basics.c.code == dal.get_today_all.c.code),
                    (dal.get_today_all.c.turnoverratio > 1.5),
                    (dal.get_today_all.c.turnoverratio < 4),
                    # (dal.get_today_all.c.per > 35),
                    # (dal.get_today_all.c.per < 65),
                    # (dal.get_stock_basics.c.pb > 3),
                    # (dal.get_stock_basics.c.pb < 8),
                    (dal.get_stock_basics.c.reservedPerShare > 0),
                    (dal.get_stock_basics.c.esp > 0.01),
                    (dal.get_stock_basics.c.profit > 0),
                    # (dal.get_stock_basics.c.totals > 1.4),
                    (dal.get_stock_basics.c.totals < 8)
                    ))
    rs = dal.connection.execute(s)
    stock_list = []
    for row in rs:
        print("%s, %s" % (row[1], row[2]))
        print("%s stock seleted" % rs.rowcount)
        stock_list.append(row[1])
    return stock_list

def main():
    basic_select()


if __name__ == '__main__':
    main()

