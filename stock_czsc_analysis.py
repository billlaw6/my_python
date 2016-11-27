#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_czsc_analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 21 Nov 2016 03:36:27 PM CST

import tushare as ts
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.finance as mpf
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import stock_czsc_tools as sct
#import sqlite3


plt.rcParams['font.family'] = ['sans-serif'] # 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['Liberation Sans'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

#con = sqlite3.connect(u'./test_stocks.db3')
engine = create_engine('sqlite:////test_stocks.db3')

def get_test_data_to_local(code=''):
    test_data = ts.get_hist_data('sh', end='2007-06-30', ktype='M').sort_index()
    #test_data.to_sql('sh_test_data', con, if_exists='replace', index=True, dtype={'date': 'CHAR'})
    test_data.to_sql('sh_test_data', engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})

def data_check(data = None):
    if data is None:
        return None
    else:
        dates = [datetime.datetime(*time.strptime(i, '%Y-%m-%d')[:6]) for i in data.date]
        data['t'] = mdates.date2num(dates)

    fig, ax = plt.subplots()
    # Before clear
    ddata = zip(np.array(data.t), np.array(data.open), np.array(data.close), np.array(data.high), np.array(data.low), np.array(data.volume))
    mpf.candlestick_ochl(ax, ddata, width=0.6, colorup='r', colordown='g')
    ax.xaxis_date()
    ax.set_title('Before clear')
    plt.show()

def ding_di_check(data = None):
    if data is None:
        return None
    else:
        dates = [datetime.datetime(*time.strptime(i, '%Y-%m-%d')[:6]) for i in data.index]
        data['t'] = mdates.date2num(dates)

    # 合一张图显示 # #############################################
    fig, axes = plt.subplots(2, 1, sharex=True)
    cdata = sct.baohan_process(data)
    # print(cdata)
    c_ddata = zip(np.array(cdata.t), np.array(cdata.open), np.array(cdata.close), np.array(cdata.high), np.array(cdata.low), np.array(cdata.volume))
    mpf.candlestick_ochl(axes[1], c_ddata, width=0.6, colorup='r', colordown='g')
    axes[0].xaxis_date()
    axes[0].autoscale_view()
    axes[0].set_title('Before clear')
    p_b_cdata = sct.find_possible_ding_di(cdata)
    #print(p_b_cdata)
    p_cdata = p_b_cdata[p_b_cdata.fenxing == 'ding']
    b_cdata = p_b_cdata[p_b_cdata.fenxing == 'di']
    axes[0].plot(np.array(p_cdata.t), np.array(p_cdata.high), 'v')
    axes[0].plot(np.array(b_cdata.t), np.array(b_cdata.low), '^')

    p_b_ddata = sct.clear_3lian_ding_di(p_b_cdata)
    p_b_ddata = sct.clear_2lian_ding_di(p_b_ddata)
    p_b_ddata = sct.clear_continous_ding_di(p_b_ddata)
    p_b_ddata = sct.clear_jin_ding_di(p_b_ddata)
    # 画完以后第二张是白板，重新zip才能画出来，原因不明。
    c_ddata = zip(np.array(cdata.t), np.array(cdata.open), np.array(cdata.close), np.array(cdata.high), np.array(cdata.low), np.array(cdata.volume))
    mpf.candlestick_ochl(axes[0], c_ddata, width=0.6, colorup='r', colordown='g')
    axes[1].xaxis_date()
    axes[1].autoscale_view()
    axes[1].set_title('After clear')
    #print(p_b_ddata)
    p_cdata = p_b_ddata[p_b_ddata.fenxing == 'ding']
    b_cdata = p_b_ddata[p_b_ddata.fenxing == 'di']
    axes[1].plot(np.array(p_cdata.t), np.array(p_cdata.high), 'v')
    axes[1].plot(np.array(b_cdata.t), np.array(b_cdata.low), '^')

    # 分两张图显示
    fig, ax = plt.subplots()
    c_ddata = zip(np.array(cdata.t), np.array(cdata.open), np.array(cdata.close), np.array(cdata.high), np.array(cdata.low), np.array(cdata.volume))
    mpf.candlestick_ochl(ax, c_ddata, width=0.6, colorup='r', colordown='g')
    ax.xaxis_date()
    ax.autoscale_view()
    ax.set_title('After clear')
    # print(p_b_ddata)
    p_cdata = p_b_ddata[p_b_ddata.fenxing == 'ding']
    b_cdata = p_b_ddata[p_b_ddata.fenxing == 'di']
    ax.plot(np.array(p_cdata.t), np.array(p_cdata.high), 'v')
    ax.plot(np.array(b_cdata.t), np.array(b_cdata.low), '^')
    # 标记笔的起点
    bi_start = sct.find_bi_start(p_b_ddata)
    if bi_start is not None:
        plt.annotate("bi start", (bi_start.t, bi_start.high))
    for i in range(len(p_b_ddata) - 1):
        if p_b_ddata.ix[i, 't'] == bi_start.t:
            sct.tag_bi_line(p_b_ddata, i, strict=True)
            break
    print("Found no bi_start!")
    exit
    #print(p_b_ddata)
    bi_data = p_b_ddata[~np.isnan(p_b_ddata.bi_value)]
    ax.plot(np.array(bi_data.t), np.array(bi_data.bi_value))

    plt.show()


def main():
    #get_test_data_to_local('sh')
    #c_data = ts.get_hist_data('sh', end='2007-06-30', ktype='M').sort_index()
    #c_data = pd.read_sql_table('sh_test_data', con)
    #print(c_data.ix[0:15])
    #data_check(c_data)
    #data = ts.get_hist_data('sh', end='2007-06-30', ktype='W').sort_index()
    #data = ts.get_hist_data('sh', '2002-01-01', '2016-01-01', ktype='M').sort_index()
    #data = pd.read_sql_table('sh_test_data', engine)
    #print(data)
    data = pd.read_csv(u'./sh_M.csv')
    data = data.set_index('date')
    ding_di_check(data)
    #draw_czsc(data)


if __name__ == '__main__':
    main()

