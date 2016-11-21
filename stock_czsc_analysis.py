#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_czsc_analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 21 Nov 2016 03:36:27 PM CST

import tushare as ts
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.finance as mpf
import numpy as np
import stock_auto as sa


plt.rcParams['font.family'] = ['sans-serif'] # 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['Liberation Sans'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

def draw_czsc(data = None):
    if data is None:
        return None
    else:
        dates = [datetime.datetime(*time.strptime(i, '%Y-%m-%d')[:6]) for i in data.index]
        data['t'] = mdates.date2num(dates)

    ddata = zip(np.array(data.t), np.array(data.open), np.array(data.close), np.array(data.high), np.array(data.low), np.array(data.volume))
    fig, axes = plt.subplots(2, 1, sharex=True)

    mpf.candlestick_ochl(axes[0], ddata, width=0.6, colorup='r', colordown='g')
    axes[0].set_ylabel('price')
    axes[0].grid(True)
    axes[0].xaxis_date()
    axes[0].autoscale_view()

    print("data columns before find: %s" % data.columns)
    czsc_data = sa.find_peak_buttom(data)
    print("data columns after find: %s" % data.columns)

    sa.tag_peak_buttom(data)
    print("data columns after tag: %s" % data.columns)
    czsc_data = data[data.line != 0]
    print(len(czsc_data))
    print("czsc_data columns: %s" % czsc_data.columns)
    data.set_index('t')
    # data['line'].plot(ax = axes[0], kind='line')
    axes[0].plot(np.array(czsc_data.t), np.array(czsc_data.line))
    axes[1].plot(np.array(czsc_data.t), np.array(czsc_data.line))
    print(czsc_data['line'])
    plt.show()



def main():
    data = ts.get_hist_data('002047','2016-01-01').sort_index()
    draw_czsc(data)


if __name__ == '__main__':
    main()

