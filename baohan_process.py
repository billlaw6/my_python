#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_czsc_tools.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 23 Nov 2016 01:37:38 PM CST

import tushare as ts
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.finance as mpf
import talib as ta
import numpy as np
import pandas as pd

plt.rcParams['font.family'] = ['sans-serif'] # 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['Liberation Sans'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

def baohan_process(data = None):
    """"""
    if data is None:
        return None

    up_down_flag = 'up'
    for i in range(0, len(data)-2):
        if float(data[i:i+1].high) < float(data[i+1:i+2].high) \
        and float(data[i:i+1].low) < float(data[i+1:i+2].low):
            data.ix[i, 'type'] = 'up'
            up_down_flag = 'up'
        elif float(data[i:i+1].high) > float(data[i+1:i+2].high) \
        and float(data[i:i+1].low) > float(data[i+1:i+2].low):
            data.ix[i, 'type'] = 'down'
            up_down_flag = 'down'
        elif float(data[i:i+1].high) >= float(data[i+1:i+2].high) \
        and float(data[i:i+1].low) <= float(data[i+1:i+2].low):
            data.ix[i+1, 'delete'] = True
            # default type is UP
            if i == 0:
                data.ix[i, 'low'] = data.ix[i+1, 'low']
            #elif data[i-1: i].type[0] == 'up':
            elif up_down_flag == 'up':
                data.ix[i, 'low'] = data.ix[i+1, 'low']
            #elif data[i-1: i].type[0] == 'down':
            elif up_down_flag == 'down':
                data.ix[i, 'high'] = data.ix[i+1, 'high']
            else:
                print("Error")
        elif float(data[i:i+1].high) <= float(data[i+1:i+2].high) \
        and float(data[i:i+1].low) >= float(data[i+1:i+2].low):
            data.ix[i, 'delete'] = True
            # default type is UP
            if i == 0:
                data.ix[i+1, 'low'] = data.ix[i, 'low']
            #elif data[i-1: i].type[0] == 'up':
            elif up_down_flag == 'up':
                data.ix[i+1, 'low'] = data.ix[i, 'low']
            #elif data[i-1: i].type[0] == 'down':
            elif up_down_flag == 'down':
                data.ix[i+1, 'high'] = data.ix[i, 'high']
            else:
                print("Error")

    data = data.drop(data[data.delete == True].index)

    if len(data[data.type == 'delete']) > 0:
        data = baohan_process(data.drop(data[data.delete == True].index))
    return data.drop(data[data.delete == True].index)
