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
    """
    1、2、3根K线，只2和3有包含关系，包含关系的处理由1和2两K线的升降决定
    Class65.
    必须从左至右顺序处理包含关系，单次遍历就行。包含处理只会缩短K线，不会产生新的包含关系。
    """

    if data is None:
        return None

    up_down_flag = 'up'
    for i in range(0, len(data)-1):
        # 当前K线的升降属性由后一根K线组合确定
        if data.ix[i, 'high'] < data.ix[i+1, 'high'] \
        and data.ix[i, 'low'] < data.ix[i+1, 'low']:
            data.ix[i, 'type'] = 'up'
            up_down_flag = 'up'
        elif data.ix[i, 'high'] > data.ix[i+1, 'high'] \
        and data.ix[i, 'low'] > data.ix[i+1, 'low']:
            data.ix[i, 'type'] = 'down'
            up_down_flag = 'down'

        # 出现前K线包含后K线时，删除后K线，并且继续向后找包含关系
        elif data.ix[i, 'high'] >= data.ix[i+1, 'high'] \
        and data.ix[i, 'low'] <= data.ix[i+1, 'low']:
            # 标记被包含的K线及与包含K线的位置关系及UP、DOWN
            data.ix[i+1, 'delete'] = True
            if i == 0:
                data.ix[i, 'low'] = data.ix[i+1, 'low']
            elif up_down_flag == 'up':
                data.ix[i, 'low'] = data.ix[i+1, 'low']
            elif up_down_flag == 'down':
                data.ix[i, 'high'] = data.ix[i+1, 'high']
            # 继续向后分析处理包含关系
            for j in range(2, len(data) - i):
                if data.ix[i, 'high'] >= data.ix[i+j, 'high'] \
                and data.ix[i, 'low'] <= data.ix[i+j, 'low']:
                    data.ix[i+j, 'delete'] = True
                    if i == 0:
                        data.ix[i, 'low'] = data.ix[i+j, 'low']
                    elif up_down_flag == 'up':
                        data.ix[i, 'low'] = data.ix[i+j, 'low']
                    elif up_down_flag == 'down':
                        data.ix[i, 'high'] = data.ix[i+j, 'high']
                else:
                    break
        # 出现后K线包含前K线时
        elif data.ix[i, 'high'] <= data.ix[i+1, 'high'] \
        and data.ix[i, 'low'] >= data.ix[i+1, 'low']:
            # 标记被包含的K线及与包含K线的位置关系及UP、DOWN
            # default type is UP
            data.ix[i, 'delete'] = True
            if i == 0:
                data.ix[i+1, 'low'] = data.ix[i, 'low']
            elif up_down_flag == 'up':
                data.ix[i+1, 'low'] = data.ix[i, 'low']
            elif up_down_flag == 'down':
                data.ix[i+1, 'high'] = data.ix[i, 'low']
        else:
            print("Shem Ma K xian guanxi?")
            data.ix[i, 'type'] = 'unknown'
    return data.drop(data[data.delete==True].index)

def find_possible_ding_di(data = None):
    """寻找和标识顶和底，数据类型应该是tushare.get_hist_data获得的dataFrame格式"""
    if data is None:
        return None

    for i in range(2, len(data)-2):
        if data.ix[i, 'high'] > data.ix[i - 1, 'high'] \
        and data.ix[i, 'high'] > data.ix[i - 2, 'high'] \
        and data.ix[i, 'high'] > data.ix[i + 1, 'high'] \
        and data.ix[i, 'high'] > data.ix[i + 2, 'high'] \
        and data.ix[i, 'low'] > data.ix[i - 1, 'low'] \
        and data.ix[i, 'low'] > data.ix[i + 1, 'low']:
            data.ix[i, 'fenxing'] = 'ding'
        elif data.ix[i, 'high'] < data.ix[i - 1, 'high'] \
        and data.ix[i, 'high'] < data.ix[i + 1, 'high'] \
        and data.ix[i, 'low'] < data.ix[i - 1, 'low'] \
        and data.ix[i, 'low'] < data.ix[i - 2, 'low'] \
        and data.ix[i, 'low'] < data.ix[i + 1, 'low'] \
        and data.ix[i, 'low'] < data.ix[i + 2, 'low']:
            data.ix[i, 'fenxing'] = 'di'
        else:
            data.ix[i, 'fenxing'] = data.ix[i, 'type']
    return data


def tag_bi_line_mm(data = None):
    """给标记顶底之后的数据画笔
    """
    if data is None:
        return None

    # 取出笔开始的所有顶底标记，方便循环处理
    ding_di_list = []
    for i in range(0, len(data)-1):
        if type(data.ix[i, 'fenxing']) == str:
            if data.ix[i, 'fenxing'].find('di') != -1:
                ding_di = {}
                ding_di['loc'] = i
                ding_di['fenxing'] = data.ix[i, 'fenxing']
                ding_di['high'] = data.ix[i, 'high']
                ding_di['low'] = data.ix[i, 'low']
                ding_di_list.append(ding_di)
            else:
                pass

    # 顶底数不够4个时，不标线
    if len(ding_di_list) < 4:
        print("Number of ding_di less than 4, please wait!")
        exit

    possible_ding_start = {'loc': -1, 'value': 0}
    possible_di_start = {'loc': -1, 'value': 0}
    ding_list = []
    di_list = []
    # 走出一个新顶或底就判断一次是否调整笔的结束点
    for i in range(0, len(ding_di_list) - 1):
        # 当前为底分型  
        if ding_di_list[i]['fenxing'] == 'di':
            di_list.append(ding_di_list[i]['low'])
            # 底 前面没有可能为笔起点的顶分型，暂标记当前底为笔起点
            if possible_ding_start['loc'] < 0 and ding_di_list[i]['low'] == min(di_list):
                possible_di_start['loc'] = ding_di_list[i]['loc']
                possible_di_start['value'] = ding_di_list[i]['low']
                continue
            # 底 前面有暂标记为笔起点的顶分型，但与当前底分型间隔不够3根K线，前面没有标记为笔起点的底分型时，暂标记当前底为笔起点
            elif possible_ding_start['loc'] >= 0 \
            and ding_di_list[i]['loc'] - possible_ding_start['loc'] <= 3 \
            and possible_di_start['loc'] < 0:
                # 标识当前底为可能的笔节点
                possible_di_start['loc'] = ding_di_list[i]['loc']
                possible_di_start['value'] = ding_di_list[i]['low']
                continue
            # 底 前面有暂标记为笔起点的顶分型，但与之间隔不够3根K线，前面有标记为笔起点的底分型而当前底更低时，将当前底标记为笔起点
            elif possible_ding_start['loc'] >= 0 \
            and ding_di_list[i]['loc'] - possible_ding_start['loc'] <= 3 \
            and possible_di_start['loc'] > 0 \
            and ding_di_list[i]['low'] < possible_di_start['value']:
                # 标识当前底为可能的笔节点
                possible_di_start['loc'] = ding_di_list[i]['loc']
                possible_di_start['value'] = ding_di_list[i]['low']
                ding_list = []
                continue
            # 底 前面有可能为笔起点的顶，并且与之间隔3根K线以上，同时当前K线底小于前面可能顶的顶并且是最低底时
            elif possible_ding_start['loc'] >= 0 \
            and ding_di_list[i]['loc'] - possible_ding_start['loc'] > 3 \
            and ding_di_list[i]['low'] == min(di_list) \
            and data.ix[possible_ding_start['loc'], 'high'] > ding_di_list[i]['low']:
                # 如果前面有标记为笔起点的底，并且与后面的顶间隔3根K线以上时确认前面的底为确定的笔起点
                if possible_di_start['loc'] >= 0 \
                and possible_ding_start['loc'] - possible_di_start['loc'] > 3:
                    # 确定前底为笔节点
                    data.ix[possible_di_start['loc'], 'bi_value'] = possible_di_start['value']
                # 标识当前底为可能的笔节点
                possible_di_start['loc'] = ding_di_list[i]['loc']
                possible_di_start['value'] = ding_di_list[i]['low']
                ding_list = []
                continue
        # 当前为顶分型  
        elif ding_di_list[i]['fenxing'] == 'ding':
            ding_list.append(ding_di_list[i]['high'])
            # 顶 前面没有可能为笔起点的底分型，暂标记当前顶为笔起点
            if possible_di_start['loc'] < 0 and ding_di_list[i]['high'] == max(ding_list):
                possible_ding_start['loc'] = ding_di_list[i]['loc']
                possible_ding_start['value'] = ding_di_list[i]['high']
                continue
            # 顶 前面有暂标记为笔起点的底分型，但与当前顶分型间隔不够3根K线，前面没有标记为笔起点的顶分型时，暂标记当前顶为笔起点
            elif possible_di_start['loc'] > 0 \
            and ding_di_list[i]['loc'] - possible_di_start['loc'] <= 3 \
            and possible_ding_start['loc'] < 0:
                # 标识当前顶为可能的笔节点
                possible_ding_start['loc'] = ding_di_list[i]['loc']
                possible_ding_start['value'] = ding_di_list[i]['high']
                continue
            # 顶 前面有暂标记为笔起点的底分型，但与之间隔不够3根K线，前面有标记为笔起点的顶分型而当前顶更高时，将当前顶标记为笔起点
            elif possible_di_start['loc'] > 0 \
            and ding_di_list[i]['loc'] - possible_di_start['loc'] <= 3 \
            and possible_ding_start['loc'] > 0 \
            and ding_di_list[i]['high'] > possible_ding_start['value']:
                # 标识当前顶为可能的笔节点
                possible_ding_start['loc'] = ding_di_list[i]['loc']
                possible_ding_start['value'] = ding_di_list[i]['high']
                di_list = []
                continue
            # 顶 前面有可能为笔起点的底，并且与之间隔3根K线以上，同时当前K线顶小于前面可能底的底并且是最高顶时
            elif possible_di_start['loc'] >= 0 \
            and ding_di_list[i]['loc'] - possible_di_start['loc'] > 3 \
            and ding_di_list[i]['high'] == max(ding_list) \
            and data.ix[possible_di_start['loc'], 'low'] < ding_di_list[i]['high']:
                # 如果前面有标记为笔起点的顶，并且与后面的底间隔3根K线以上时确认前面的顶为确定的笔起点
                if possible_ding_start['loc'] >= 0 \
                and possible_di_start['loc'] - possible_ding_start['loc'] > 3:
                    # 确定前顶为笔节点
                    data.ix[possible_ding_start['loc'], 'bi_value'] = data.ix[possible_ding_start['loc'], 'high']
                # 标识当前顶为可能的笔节点
                possible_ding_start['loc'] = ding_di_list[i]['loc']
                possible_ding_start['value'] = ding_di_list[i]['high']
                di_list = []
                continue
    return data

def tag_bi_line(data = None):
    """给标记顶底之后的数据画笔 """
    if data is None:
        return None

    # 取出所有顶底标记，方便循环处理
    ding_di_list = []
    for i in range(0, len(data)-1):
        if type(data.ix[i, 'fenxing']) == str:
            if data.ix[i, 'fenxing'].find('di') != -1:
                ding_di = {}
                ding_di['loc'] = i
                ding_di['fenxing'] = data.ix[i, 'fenxing']
                ding_di['high'] = data.ix[i, 'high']
                ding_di['low'] = data.ix[i, 'low']
                ding_di_list.append(ding_di)
            else:
                pass

    # 顶底数不够4个时，不标线
    if len(ding_di_list) < 4:
        print("Number of ding_di less than 4, please wait!")
        exit

    pre_ding_start = {'loc': -1, 'value': 0}
    pre_di_start = {'loc': -1, 'value': 0}
    ding_start = {'loc': -1, 'value': 0}
    di_start = {'loc': -1, 'value': 0}
    # 走出一个新顶或底就判断一次是否调整笔的结束点
    for i in range(0, len(ding_di_list) - 1):
        if ding_di_list[i]['fenxing'] == 'ding':
            if ding_start['loc'] < 0:
                pre_ding_start['loc'] = ding_start['loc']
                pre_ding_start['value'] = ding_start['value']
                ding_start['loc'] = ding_di_list[i]['loc']
                ding_start['value'] = ding_di_list[i]['high']
                continue
            elif ding_start['loc'] >= 0:
                if di_start['loc'] < 0:
                    if ding_di_list[i]['high'] > ding_start['value']:
                        pre_ding_start['loc'] = ding_start['loc']
                        pre_ding_start['value'] = ding_start['value']
                        ding_start['loc'] = ding_di_list[i]['loc']
                        ding_start['value'] = ding_di_list[i]['high']
                        continue
                elif di_start['loc'] >= 0:
                    if di_start['loc'] < ding_start['loc']:
                        if ding_di_list[i]['loc'] - di_start['loc'] > 3 \
                        and ding_di_list[i]['high'] > ding_start['value']:
                            pre_ding_start['loc'] = ding_start['loc']
                            pre_ding_start['value'] = ding_start['value']
                            ding_start['loc'] = ding_di_list[i]['loc']
                            ding_start['value'] = ding_di_list[i]['high']
                            if pre_ding_start['loc'] > 0 \
                            and di_start['loc'] - pre_ding_start['loc'] > 3:
                                data.ix[pre_ding_start['loc'], 'bi_value'] = pre_ding_start['value']
                            continue
                    elif di_start['loc'] > ding_start['loc']:
                        if ding_di_list[i]['loc'] - di_start['loc'] > 3 \
                        and ding_di_list[i]['high'] > di_start['value']:
                            pre_ding_start['loc'] = ding_start['loc']
                            pre_ding_start['value'] = ding_start['value']
                            ding_start['loc'] = ding_di_list[i]['loc']
                            ding_start['value'] = ding_di_list[i]['high']
                            if pre_ding_start['loc'] > 0 \
                            and di_start['loc'] - pre_ding_start['loc'] > 3:
                                data.ix[pre_ding_start['loc'], 'bi_value'] = pre_ding_start['value']
                            continue
                        elif ding_di_list[i]['loc'] - di_start['loc'] <= 3:
                            if ding_di_list[i]['high'] > ding_start['value']:
                                ding_start['loc'] = ding_di_list[i]['loc']
                                ding_start['value'] = ding_di_list[i]['high']
                                di_start['loc'] = pre_di_start['loc']
                                di_start['value'] = pre_di_start['value']
                                pre_di_start['loc'] = -1
                                pre_di_start['value'] = 0
                                if pre_ding_start['loc'] > 0 \
                                and di_start['loc'] - pre_ding_start['loc'] > 3:
                                    data.ix[pre_ding_start['loc'], 'bi_value'] = pre_ding_start['value']
                                continue


        elif ding_di_list[i]['fenxing'] == 'di':
            if di_start['loc'] < 0:
                pre_di_start['loc'] = di_start['loc']
                pre_di_start['value'] = di_start['value']
                di_start['loc'] = ding_di_list[i]['loc']
                di_start['value'] = ding_di_list[i]['low']
                continue
            elif di_start['loc'] >= 0:
                if ding_start['loc'] < 0:
                    if ding_di_list[i]['low'] < di_start['loc']:
                        pre_di_start['loc'] = di_start['loc']
                        pre_di_start['value'] = di_start['value']
                        di_start['loc'] = ding_di_list[i]['loc']
                        di_start['value'] = ding_di_list[i]['low']
                        continue
                elif ding_start['loc'] >= 0:
                    if di_start['loc'] > ding_start['loc']:
                        if ding_di_list[i]['loc'] - ding_start['loc'] > 3 \
                        and ding_di_list[i]['low'] < di_start['value']:
                            pre_di_start['loc'] = di_start['loc']
                            pre_di_start['value'] = di_start['value']
                            di_start['loc'] = ding_di_list[i]['loc']
                            di_start['value'] = ding_di_list[i]['low']
                            if pre_di_start['loc'] > 0 \
                            and ding_start['loc'] - pre_di_start['loc'] > 3:
                                data.ix[pre_di_start['loc'], 'bi_value'] = pre_di_start['value']
                            continue
                    elif di_start['loc'] < ding_start['loc']:
                        if ding_di_list[i]['loc'] - ding_start['loc'] > 3 \
                        and ding_di_list[i]['low'] < ding_start['value']:
                            pre_di_start['loc'] = di_start['loc']
                            pre_di_start['value'] = di_start['value']
                            di_start['loc'] = ding_di_list[i]['loc']
                            di_start['value'] = ding_di_list[i]['low']
                            if pre_di_start['loc'] > 0 \
                            and ding_start['loc'] - pre_di_start['loc'] > 3:
                                data.ix[pre_di_start['loc'], 'bi_value'] = pre_di_start['value']
                            continue
                        elif ding_di_list[i]['loc'] - ding_start['loc'] <= 3:
                            if ding_di_list[i]['low'] < di_start['value']:
                                di_start['loc'] = ding_di_list[i]['loc']
                                di_start['value'] = ding_di_list[i]['low']
                                ding_start['loc'] = pre_ding_start['loc']
                                ding_start['value'] = pre_ding_start['value']
                                pre_ding_start['loc'] = -1
                                pre_ding_start['value'] = 0
                                if pre_di_start['loc'] > 0 \
                                and ding_start['loc'] - pre_di_start['loc'] > 3:
                                    data.ix[pre_di_start['loc'], 'bi_value'] = pre_di_start['value']
                                continue
    return data


def tag_duan_line(data = None):
    """Class 67"""
    if data is None:
        return None

    # 取出所有标记为笔节点的顶底标记，方便循环处理
    bi_ding_di_list = []
    for i in range(0, len(data)):
        if type(data.ix[i, 'fenxing']) == str:
            if data.ix[i, 'fenxing'].find('di') != -1 \
            and data.ix[i, 'bi_value'] > 0:
                ding_di = {}
                ding_di['loc'] = i
                ding_di['fenxing'] = data.ix[i, 'fenxing']
                ding_di['high'] = data.ix[i, 'high']
                ding_di['low'] = data.ix[i, 'low']
                bi_ding_di_list.append(ding_di)
            else:
                pass

    # 顶底数不够4个时，不构成段
    if len(bi_ding_di_list) < 4:
        print("Number of ding_di less than 4, please wait!")
        exit

    shang = {}
    shang_list = []
    xia = {}
    xia_list = []
    for i in range(0, len(bi_ding_di_list)-1):
        if bi_ding_di_list[i]['fenxing'] == 'ding':
            xia['high_loc'] = bi_ding_di_list[i]['loc']
            xia['high_value'] = bi_ding_di_list[i]['high']
            xia['low_loc'] = bi_ding_di_list[i+1]['loc']
            xia['low_value'] = bi_ding_di_list[i+1]['low']
            xia_list.append(xia)
        elif bi_ding_di_list[i]['fenxing'] == 'di':
            shang['low_loc'] = bi_ding_di_list[i]['loc']
            shang['low_value'] = bi_ding_di_list[i]['low']
            shang['high_loc'] = bi_ding_di_list[i+1]['loc']
            shang['high_value'] = bi_ding_di_list[i+1]['high']
            shang_list.append(xia)

    # 处理包含关系
    for i in range(0, len(shang_list) - 1):
        if shang_list[i]['low_value'] < shang_list[i+1]['low_value'] \
        and shang_list[i]['high_value'] > shang_list[i+1]['high_value']:
            shang_list.remove(i+1)
            if i >= len(shang_list) - 1:
                break
        elif shang_list[i]['low_value'] > shang_list[i+1]['low_value'] \
        and shang_list[i]['high_value'] < shang_list[i+1]['high_value']:
            shang_list.remove(i)
            if i >= len(shang_list) - 1:
                break
    for i in range(0, len(xia_list) - 1):
        if xia_list[i]['low_value'] < xia_list[i+1]['low_value'] \
        and xia_list[i]['high_value'] > xia_list[i+1]['high_value']:
            xia_list.remove(i+1)
            if i >= len(xia_list) - 1:
                break
        elif xia_list[i]['low_value'] > xia_list[i+1]['low_value'] \
        and xia_list[i]['high_value'] < xia_list[i+1]['high_value']:
            xia_list.remove(i)
            if i >= len(xia_list) - 1:
                break

    # 标记笔特征序列的顶底,上行笔序列中找底，下行笔序列中找顶
    for i in range(1, len(shang_list) - 1):
        if shang_list[i]['low_value'] < shang_list[i-1]['low_value'] \
        and shang_list[i]['low_value'] < shang_list[i+1]['low_value'] \
        and shang_list[i]['high_value'] < shang_list[i-1]['high_value'] \
        and shang_list[i]['high_value'] < shang_list[i+1]['high_value']:
            data.ix[shang_list[i]['low_loc'], 'bi_fenxing'] = 'di'
            data.ix[shang_list[i]['low_loc'], 'duan_value'] = shang_list[i]['low_value']
    for i in range(1, len(xia_list) - 1):
        if xia_list[i]['high_value'] > xia_list[i-1]['high_value'] \
        and xia_list[i]['high_value'] > xia_list[i+1]['high_value'] \
        and xia_list[i]['low_value'] > xia_list[i-1]['low_value'] \
        and xia_list[i]['low_value'] > xia_list[i+1]['low_value']:
            data.ix[xia_list[i]['high_loc'], 'bi_fenxing'] = 'ding'
            data.ix[shang_list[i]['high_loc'], 'duan_value'] = shang_list[i]['high_value']

    return data

def plot_data(data = None, single=False):
    """自定义画图"""
    if data is None:
        print("Data is None!")
        exit
    dates = [datetime.datetime(*time.strptime(i, '%Y-%m-%d')[:6]) for i in data.index]

    # 多指标同图
    if not single:
        data['t'] = mdates.date2num(dates)
        adata = data[['t','open','close','high','low','volume']]
        ddata = zip(np.array(adata.t), np.array(adata.open), np.array(adata.close), np.array(adata.high), np.array(adata.low), np.array(adata.volume))
        fig, axes = plt.subplots(3, 1, sharex=True, figsize=(8,6))

        mpf.candlestick_ochl(axes[0], ddata, width=0.6, colorup='r', colordown='g')
        axes[0].set_title(u'宝鹰股份')
        axes[0].set_ylabel('price')
        axes[0].grid(True)
        axes[0].xaxis_date()
        axes[0].autoscale_view()
        axes[1].bar(np.array(adata.t), np.array(adata.volume))
        axes[1].set_ylabel('volume')
        axes[1].grid(True)
        axes[1].autoscale_view()
        plt.setp(plt.gca().get_xticklabels(), rotation=30)
        # dflen = df.shape[0]
        dflen = len(data)
        if dflen > 35:
            macd, macdsignal, macdhist = ta.MACD(np.array(data['close']),
                                                 fastperiod=12, slowperiod=26,
                                                 signalperiod=9)
            data['macd']=pd.Series(macd,index=data.index)
            data['macdsignal']=pd.Series(macdsignal,index=data.index)
            data['macdhist']=pd.Series(macdhist,index=data.index)
            data.set_index('t')
            data = data.set_index('t')
            data[['macd','macdsignal','macdhist']].plot(ax=axes[2])
            axes[2].axhline()
    else:
        data['t'] = mdates.date2num(dates)
        adata = data[['t','open','close','high','low','volume']]
        ddata = zip(np.array(adata.t), np.array(adata.open), np.array(adata.close), np.array(adata.high), np.array(adata.low), np.array(adata.volume))
        fig, ax = plt.subplots(1, 1, figsize=(8,6))

        mpf.candlestick_ochl(ax, ddata, width=0.6, colorup='r', colordown='g')
        ax.set_ylabel('price')
        ax.grid(True)
        ax.xaxis_date()
        ax.autoscale_view()

    # 有顶底标记时画顶底标记
    if 'fenxing' in data.columns:
        p_data = data[data.fenxing == 'ding']
        b_data = data[data.fenxing == 'di']
        ax = plt.gca()
        ax.plot(np.array(p_data.t), np.array(p_data.high), 'v')
        ax.plot(np.array(b_data.t), np.array(b_data.low), '^')

    # 有笔标记时添加笔线条 
    if 'bi_value' in data.columns:
        bi_data = data[~np.isnan(data.bi_value)]
        ax.plot(np.array(bi_data.t), np.array(bi_data.bi_value))

    # 有段标记时添加段线条 
    if 'duan_value' in data.columns:
        print("duan line added")
        duan_data = data[~np.isnan(data.duan_value)]
        ax.plot(np.array(duan_data.t), np.array(duan_data.duan_value), color='b', linewidth=2)
    plt.show()

def main():
    #data = ts.get_hist_data('002047','2016-01-11').sort_index()
    data = ts.get_hist_data('sh','2013-01-11',ktype='W').sort_index()
    # data = pd.read_csv(u'./sh_M.csv')
    # data = data.set_index('date')
    print("Before baohan process: %s" % len(data))
    #plot_data(data, single=True)

    data = baohan_process(data)
    print("After baohan process: %s" % len(data))
    data = find_possible_ding_di(data)
    print("After find ding di: %s" % len(data))
    data = tag_bi_line(data)
    plot_data(data, single=True)

    data = tag_duan_line(data)
    plot_data(data, single=True)



if __name__ == '__main__':
    main()

