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

    fig, axes = plt.subplots(2, 1, sharex=True)
    # Before clear
    ddata = zip(np.array(data.t), np.array(data.open), np.array(data.close), np.array(data.high), np.array(data.low), np.array(data.volume))
    mpf.candlestick_ochl(axes[0], ddata, width=0.6, colorup='r', colordown='g')
    axes[0].xaxis_date()
    axes[0].set_title('Before clear')
    p_b_data = sa.find_possible_peak_buttom(data)
    p_data = p_b_data[p_b_data.type == 'peak']
    b_data = p_b_data[p_b_data.type == 'buttom']
    axes[0].plot(np.array(p_data.t), np.array(p_data.high), 'v')
    axes[0].plot(np.array(b_data.t), np.array(b_data.low), '^')
    # After clear
    c_data = sa.clear_data(data)
    ddata = zip(np.array(c_data.t), np.array(c_data.open), np.array(c_data.close), np.array(c_data.high), np.array(c_data.low), np.array(c_data.volume))
    mpf.candlestick_ochl(axes[1], ddata, width=0.6, colorup='r', colordown='g')
    axes[1].xaxis_date()
    axes[1].set_title('After clear')
    p_b_data = sa.find_possible_peak_buttom(c_data)
    p_data = p_b_data[p_b_data.type == 'peak']
    b_data = p_b_data[p_b_data.type == 'buttom']

    data.set_index('t')
    axes[1].plot(np.array(p_data.t), np.array(p_data.high), 'v')
    axes[1].plot(np.array(b_data.t), np.array(b_data.low), '^')

    czsc_data = sa.tech_analysis(p_b_data)
    line_data = czsc_data[~np.isnan(czsc_data.line)]
    print(line_data['line'])
    axes[1].plot(np.array(line_data.t), np.array(line_data.line))

    plt.show()

def main():
    data = ts.get_hist_data('002047','2015-06-01','2016-03-01').sort_index()
    draw_czsc(data)


if __name__ == '__main__':
    main()

