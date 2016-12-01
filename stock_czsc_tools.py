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
    """1、2、3根K线，只2和3有包含关系，包含关系的处理由1和2两K线的升降决定 Class65"""
    if data is None:
        return None

    up_down_flag = 'up'
    for i in range(0, len(data)-1):
        # 当前K线的升降属性由后一根K线组合确定
        if float(data.ix[i, 'high']) < float(data.ix[i+1, 'high']) \
        and float(data.ix[i, 'low']) < float(data.ix[i+1, 'low']):
            data.ix[i, 'type'] = 'up'
            up_down_flag = 'up'
        elif float(data.ix[i, 'high']) > float(data.ix[i+1, 'high']) \
        and float(data.ix[i, 'low']) > float(data.ix[i+1, 'low']):
            data.ix[i, 'type'] = 'down'
            up_down_flag = 'down'
        elif float(data.ix[i, 'high']) >= float(data.ix[i+1, 'high']) \
        and float(data.ix[i, 'low']) <= float(data.ix[i+1, 'low']):
            # 出现包含关系时，保留后一条K线，方便解决合并后但数据未清理时的数据比较
            data.ix[i, 'delete'] = True
            # default type is UP
            if i == 0:
                data.ix[i+1, 'high'] = data.ix[i, 'high']
            elif up_down_flag == 'up':
                data.ix[i+1, 'high'] = data.ix[i, 'high']
            elif up_down_flag == 'down':
                data.ix[i+1, 'low'] = data.ix[i, 'low']
            else:
                print("Error")
        elif float(data.ix[i, 'high']) <= float(data.ix[i+1, 'high']) \
        and float(data.ix[i, 'low']) >= float(data.ix[i+1, 'low']):
            data.ix[i, 'delete'] = True
            # default type is UP
            if i == 0:
                data.ix[i+1, 'low'] = data.ix[i, 'low']
            elif up_down_flag == 'up':
                data.ix[i+1, 'low'] = data.ix[i, 'low']
            elif up_down_flag == 'down':
                data.ix[i+1, 'high'] = data.ix[i, 'high']
            else:
                print("Error")
        else:
            data.ix[i, 'type'] = 'unknown'


    data = data.drop(data[data.delete == True].index)

    if len(data[data.type == 'delete']) > 0:
        data = baohan_process(data.drop(data[data.delete == True].index))

    # Again
    for i in range(0, len(data)-2):
        if float(data[i:i+1].high) < float(data[i+1:i+2].high) \
        and float(data[i:i+1].low) < float(data[i+1:i+2].low):
            data.ix[i, 'type'] = 'up'
        elif float(data[i:i+1].high) > float(data[i+1:i+2].high) \
        and float(data[i:i+1].low) > float(data[i+1:i+2].low):
            data.ix[i, 'type'] = 'down'
    return data.drop(data[data.delete == True].index)

def find_possible_ding_di(data = None):
    """寻找和标识顶和底，数据类型应该是tushare.get_hist_data获得的dataFrame格式"""
    if data is None:
        return None

    for i in range(1, len(data)-3):
        if float(data.ix[i, 'high']) > float(data.ix[i - 1, 'high']) \
        and float(data.ix[i, 'high']) > float(data.ix[i + 1, 'high']) \
        and float(data.ix[i, 'low']) > float(data.ix[i - 1, 'low']) \
        and float(data.ix[i, 'low']) > float(data.ix[i + 1, 'low']):
            data.ix[i, 'fenxing'] = 'ding'
        elif float(data.ix[i, 'high']) < float(data.ix[i - 1, 'high']) \
        and float(data.ix[i, 'high']) < float(data.ix[i + 1, 'high']) \
        and float(data.ix[i, 'low']) < float(data.ix[i - 1, 'low']) \
        and float(data.ix[i, 'low']) < float(data.ix[i + 1, 'low']):
            data.ix[i, 'fenxing'] = 'di'
        else:
            data.ix[i, 'fenxing'] = data.ix[i, 'type']
    return data


def clear_3lian_ding_di(data = None):
    """处理三个连续互为边的顶底，顶底处理第一步"""
    for i in range(0, len(data) - 2):
        if data.ix[i, 'fenxing'] == 'ding' and data.ix[i+2, 'fenxing'] == 'ding':
            if data.ix[i, 'high'] > data.ix[i+2, 'high']:
                data.ix[i+2, 'fenxing'] = data.ix[i+2, 'type']
            else:
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
        elif data.ix[i, 'fenxing'] == 'di' and data.ix[i+2, 'fenxing'] == 'di':
            if data.ix[i, 'low'] < data.ix[i+2, 'low']:
                data.ix[i+2, 'fenxing'] = data.ix[i+2, 'type']
            else:
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
    return data

def clear_2lian_ding_di(data = None):
    """处理仅两个连续互为边的顶底，顶底处理第二步"""
    for i in range(0, len(data) - 3):
        if data.ix[i, 'fenxing'] == 'ding' and data.ix[i+1, 'fenxing'] == 'di':
            if i == 1:
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
            elif data.ix[i-2, 'type'] == 'down' and data.ix[i+3, 'type'] =='up':
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
            elif data.ix[i-2, 'type'] == 'up' and data.ix[i+3, 'type'] =='down':
                data.ix[i+1, 'fenxing'] = data.ix[i, 'type']
            elif data.ix[i-2, 'type'] == data.ix[i+3, 'type'] and data.ix[i+3, 'fenxing'] == 'ding':
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
            # 下面处理i+3为ding但被3lian处理掉的情况
            elif data.ix[i-2, 'type'] == data.ix[i+3, 'type'] and data.ix[i+4, 'fenxing'] == 'di':
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
            else:
                #print("shen me qing kuang? \n %s" % data.ix[i-2:i+6, ['high','low','type','fenxing']])
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
                data.ix[i+1, 'fenxing'] = data.ix[i, 'type']
        elif data.ix[i, 'fenxing'] == 'di' and data.ix[i+1, 'fenxing'] == 'ding':
            if i == 1:
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
            elif data.ix[i-2, 'type'] == 'down' and data.ix[i+3, 'type'] =='up':
                data.ix[i+1, 'fenxing'] = data.ix[i, 'type']
            elif data.ix[i-2, 'type'] == 'up' and data.ix[i+3, 'type'] =='down':
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
            elif data.ix[i-2, 'type'] == data.ix[i+3, 'type'] and data.ix[i+3, 'fenxing'] == 'di':
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
            # 下面处理i+3为di但被3lian处理掉的情况
            elif data.ix[i-2, 'type'] == data.ix[i+3, 'type'] and data.ix[i+4, 'fenxing'] == 'ding':
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
            else:
                #print("shen me qing kuang? \n %s" % data.ix[i-2:i+6, ['high','low','type','fenxing']])
                data.ix[i, 'fenxing'] = data.ix[i, 'type']
                data.ix[i+1, 'fenxing'] = data.ix[i, 'type']
    return data

def clear_continous_ding_di(data = None):
    """处理连续的顶或连续的底的情况，顶底处理第三步"""
    if len(data) < 4:
        print("clear_continous_ding_di: data length less than 4")
        exit
    for i in range(1, len(data) - 3):
        if data.ix[i, 'fenxing'].find('di') != -1:
            for j in range(i+1, len(data) - 3):
                if (data.ix[j, 'fenxing'].find('di') != -1) and data.ix[i, 'fenxing'] == data.ix[j, 'fenxing']:
                    if data.ix[j, 'fenxing'] == 'ding':
                        if data.ix[i, 'high'] < data.ix[j, 'high']:
                            data.ix[i, 'fenxing'] = data.ix[i, 'type']
                        else:
                            data.ix[j, 'fenxing'] = data.ix[j, 'type']
                    else:
                        if data.ix[i, 'low'] < data.ix[j, 'low']:
                            data.ix[j, 'fenxing'] = data.ix[j, 'type']
                        else:
                            data.ix[i, 'fenxing'] = data.ix[i, 'type']
                if (data.ix[j, 'fenxing'].find('di') != -1) and data.ix[i, 'fenxing'] != data.ix[j, 'fenxing']:
                    break
                else:
                    continue 
    return data

def clear_jin_ding_di(data = None):
    """处理明确的上升或下降趋势中间隔小于3根K线的顶和底，顶底处理第四步"""
    if len(data) < 4:
        print("clear_continous_ding_di: data length less than 4")
        exit
    ding_di_list = []
    for i in range(1, len(data) - 3):
        if data.ix[i, 'fenxing'].find('di') != -1:
            ding_di = {}
            ding_di['loc'] = i
            ding_di['fenxing'] = data.ix[i, 'fenxing']
            ding_di['high'] = data.ix[i, 'high']
            ding_di['low'] = data.ix[i, 'low']
            ding_di_list.append(ding_di)
        else:
            pass
    # Data check
    for i in range(0, len(ding_di_list) - 1):
        if ding_di_list[i]['fenxing'] == ding_di_list[i+1]['fenxing']:
            print("Error: Lian xu ding di!")
            exit
        else:
            pass

    for i in range(0, len(ding_di_list) - 4):
        # print("%s: %s" % (len(ding_di_list), i))
        if ding_di_list[i]['fenxing'] == 'ding' and \
        ding_di_list[i+2]['loc'] - ding_di_list[i+1]['loc'] <= 3 \
        and ding_di_list[i]['high'] > ding_di_list[i+2]['high'] \
        and ding_di_list[i+1]['low'] > ding_di_list[i+3]['low']:
            data.ix[ding_di_list[i+1]['loc'], 'fenxing'] = data.ix[ding_di_list[i+1]['loc'], 'type']
            data.ix[ding_di_list[i+2]['loc'], 'fenxing'] = data.ix[ding_di_list[i+1]['loc'], 'type']
        elif ding_di_list[i]['fenxing'] == 'di' and \
        ding_di_list[i+2]['loc'] - ding_di_list[i+1]['loc'] <= 3 \
        and ding_di_list[i]['low'] < ding_di_list[i+2]['low'] \
        and ding_di_list[i+1]['high'] < ding_di_list[i+3]['high']:
            data.ix[ding_di_list[i+1]['loc'], 'fenxing'] = data.ix[ding_di_list[i+1]['loc'], 'type']
            data.ix[ding_di_list[i+2]['loc'], 'fenxing'] = data.ix[ding_di_list[i+1]['loc'], 'type']
            del ding_di_list[i+1]
            del ding_di_list[i+2]
        else:
            pass
        # 动态调整结束循环条件，防止索引值超范围
        if i == len(ding_di_list) - 4:
            break
    return data

def find_bi_start(data = None):
    """在前6个顶底中找出笔的起点，超过6个仍不确认则返回None"""
    if len(data) < 4:
        print("clear_continous_ding_di: data length less than 4")
        exit

    ding_di_list = []
    for i in range(1, len(data) - 3):
        if data.ix[i, 'fenxing'].find('di') != -1:
            ding_di = {}
            ding_di['loc'] = i
            ding_di['fenxing'] = data.ix[i, 'fenxing']
            ding_di['high'] = data.ix[i, 'high']
            ding_di['low'] = data.ix[i, 'low']
            ding_di_list.append(ding_di)
        else:
            pass

    # Data check
    for i in range(0, len(ding_di_list) - 1):
        if ding_di_list[i]['fenxing'] == ding_di_list[i+1]['fenxing']:
            print("Error: Lian xu ding di!")
            exit
        else:
            pass

    if len(ding_di_list) >= 3:
        if ding_di_list[1]['loc'] - ding_di_list[0]['loc'] > 3 \
       and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] > 3:
            print("3 > >")
            return data.ix[ding_di_list[0]['loc']]
        else:
            pass
    if len(ding_di_list) >= 4:
        if ding_di_list[1]['loc'] - ding_di_list[0]['loc'] <= 3 \
        and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] <= 3:
            if ding_di_list[0]['fenxing'] == 'ding' \
           and ding_di_list[0]['high'] > ding_di_list[2]['high'] \
           and ding_di_list[1]['low'] > ding_di_list[3]['low']:
               print("4 < <")
               return data.ix[ding_di_list[0]['loc']]
            elif ding_di_list[0]['fenxing'] == 'di' \
           and ding_di_list[0]['low'] < ding_di_list[2]['low'] \
           and ding_di_list[1]['high'] < ding_di_list[3]['high']:
               print("4 < <")
               return data.ix[ding_di_list[0]['loc']]
        elif ding_di_list[1]['loc'] - ding_di_list[0]['loc'] <= 3 \
       and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] > 3 \
       and ding_di_list[3]['loc'] - ding_di_list[2]['loc'] > 3:
            print("4 < > >")
            return data.ix[ding_di_list[1]['loc']]
        elif ding_di_list[1]['loc'] - ding_di_list[0]['loc'] > 3 \
       and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] <= 3 \
       and ding_di_list[3]['loc'] - ding_di_list[2]['loc'] <= 3:
            print("4 > < <")
            return data.ix[ding_di_list[0]['loc']]
        elif ding_di_list[1]['loc'] - ding_di_list[0]['loc'] > 3 \
       and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] <= 3 \
       and ding_di_list[3]['loc'] - ding_di_list[2]['loc'] > 3:
            if ding_di_list[0]['fenxing'] == 'ding' \
           and ding_di_list[0]['high'] > ding_di_list[2]['high'] \
           and ding_di_list[1]['low'] > ding_di_list[3]['low']:
                print("4 ding > < >")
                return data.ix[ding_di_list[0]['loc']]
            elif ding_di_list[0]['fenxing'] == 'di' \
           and ding_di_list[0]['low'] < ding_di_list[2]['low'] \
           and ding_di_list[1]['high'] < ding_di_list[3]['high']:
               print("4 di > < >")
               return data.ix[ding_di_list[0]['loc']]
        else:
            pass
    if len(ding_di_list) >= 5:
        if ding_di_list[1]['loc'] - ding_di_list[0]['loc'] <= 3 \
           and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] > 3 \
           and ding_di_list[3]['loc'] - ding_di_list[2]['loc'] <= 3:
            if ding_di_list[0]['fenxing'] == 'ding' \
           and ding_di_list[4]['high'] > ding_di_list[2]['high']:
                print("5 ding < > <")
                return data.ix[ding_di_list[1]['loc']]
            elif ding_di_list[0]['fenxing'] == 'di' \
           and ding_di_list[4]['low'] > ding_di_list[2]['low']:
                print("5 di < > <")
                return data.ix[ding_di_list[0]['loc']]
        elif ding_di_list[1]['loc'] - ding_di_list[0]['loc'] > 3 \
           and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] <= 3 \
           and ding_di_list[3]['loc'] - ding_di_list[2]['loc'] > 3:
            if ding_di_list[0]['fenxing'] == 'ding' \
           and ding_di_list[0]['high'] > ding_di_list[2]['high'] \
           and ding_di_list[1]['low'] > ding_di_list[3]['low']:
                print("5 ding > < >")
                return data.ix[ding_di_list[0]['loc']]
            elif ding_di_list[0]['fenxing'] == 'di' \
           and ding_di_list[0]['low'] < ding_di_list[2]['low'] \
           and ding_di_list[1]['high'] > ding_di_list[3]['high']:
                print("5 di > < >")
                return data.ix[ding_di_list[0]['loc']]
    if len(ding_di_list) >= 6:
        if ding_di_list[1]['loc'] - ding_di_list[0]['loc'] <= 3 \
           and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] > 3 \
           and ding_di_list[3]['loc'] - ding_di_list[2]['loc'] < 3:
            if ding_di_list[0]['fenxing'] == 'ding' \
           and ding_di_list[3]['low'] > ding_di_list[5]['low']:
                print("6 ding < > <")
                return data.ix[ding_di_list[1]['loc']]
            elif ding_di_list[0]['fenxing'] == 'di' \
           and ding_di_list[3]['high'] < ding_di_list[5]['high']:
                print("6 di < > <")
                return data.ix[ding_di_list[1]['loc']]

    print("Found no bi start in qian 6 ding di, shen ma qing kuang?")
    return None


def tag_bi_line(data = None, start_index = None, strict = False):
    """给标记笔起点之后的数据画笔
    strict为True时，严格要求顶底之间间隔至少3根K线，为False时允许只有两根K线。
    69课上证月线图缠少画了前面两个顶底，画线起点"""
    if data is None or start_index is None:
        print("No data or no start_index given!")
        return None

    # 取出笔开始的所有顶底标记，方便循环处理
    ding_di_list = []
    for i in range(start_index, len(data) - 3):
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

    for i in range(0, len(ding_di_list) - 3):
        """走出一个新顶或底就判断一次是否调整笔的结束点"""
        if ding_di_list[i+1]['loc'] - ding_di_list[i]['loc'] > 3:
            if ding_di_list[i]['fenxing'] == 'ding':
                data.ix[ding_di_list[i]['loc'], 'bi_value'] = data.ix[ding_di_list[i]['loc'], 'high']
                data.ix[ding_di_list[i+1]['loc'], 'bi_value'] = data.ix[ding_di_list[i+1]['loc'], 'low']
            elif ding_di_list[i]['fenxing'] == 'di':
                data.ix[ding_di_list[i]['loc'], 'bi_value'] = data.ix[ding_di_list[i]['loc'], 'low']
                data.ix[ding_di_list[i+1]['loc'], 'bi_value'] = data.ix[ding_di_list[i+1]['loc'], 'high']
            else:
                print("Error value %s" % ding_di_list[i])
        elif (ding_di_list[i+1]['loc'] - ding_di_list[i]['loc'] <= 3) and i == 0:
            if ding_di_list[i]['fenxing'] == 'ding':
                if data.ix[ding_di_list[i]['loc'], 'low'] >= data.ix[ding_di_list[i]['loc'], 'low']:
                    data.ix[ding_di_list[i+1]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i+3]['loc'], 'bi_value'] = data.ix[ding_di_list[i+2]['loc'], 'low']
                    del ding_di_list[i+1]
                    del ding_di_list[i+2]
            elif ding_di_list[i]['fenxing'] == 'di':
                if data.ix[ding_di_list[i]['loc'], 'high'] <= data.ix[ding_di_list[i]['loc'], 'high']:
                    data.ix[ding_di_list[i+1]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i+3]['loc'], 'bi_value'] = data.ix[ding_di_list[i+3]['loc'], 'high']
                    del ding_di_list[i+1]
                    del ding_di_list[i+2]
            else:
                print("Error value %s" % ding_di_list[i])
        # bi end
        elif (ding_di_list[i+1]['loc'] - ding_di_list[i]['loc'] <= 3) \
        and (not np.isnan(data.ix[ding_di_list[i]['loc'], 'bi_value'])) \
        and i > 0:
            if ding_di_list[i]['fenxing'] == 'ding':
                if data.ix[ding_di_list[i-1]['loc'], 'low'] >= data.ix[ding_di_list[i+1]['loc'], 'low']:
                    data.ix[ding_di_list[i-1]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i-1]['loc'], 'end_change'] = True
                    data.ix[ding_di_list[i]['loc'], 'end_change'] = True
                    data.ix[ding_di_list[i+3]['loc'], 'bi_value'] = data.ix[ding_di_list[i+2]['loc'], 'low']
                    del ding_di_list[i+1]
                    del ding_di_list[i+2]
                else:
                    print("Not sertain yet at %s, wait" % ding_di_list[i])

            elif ding_di_list[i]['fenxing'] == 'di':
                if data.ix[ding_di_list[i-1]['loc'], 'high'] <= data.ix[ding_di_list[i+1]['loc'], 'high']:
                    data.ix[ding_di_list[i-1]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i-1]['loc'], 'end_change'] = True
                    data.ix[ding_di_list[i]['loc'], 'end_change'] = True
                    data.ix[ding_di_list[i+1]['loc'], 'bi_value'] = data.ix[ding_di_list[i+1]['loc'], 'high']
                else:
                    print("Not sertain yet at %s, wait" % ding_di_list[i])
            else:
                print("Error value %s" % ding_di_list[i])
        # not bi_end
        elif (ding_di_list[i+1]['loc'] - ding_di_list[i]['loc'] <= 3) \
        and (np.isnan(data.ix[ding_di_list[i]['loc'], 'bi_value'])) \
        and i > 0:
            if ding_di_list[i]['fenxing'] == 'ding':
                if data.ix[ding_di_list[i-1]['loc'], 'low'] >= data.ix[ding_di_list[i+1]['loc'], 'low']:
                    data.ix[ding_di_list[i-1]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i-1]['loc'], 'end_change'] = True
                    data.ix[ding_di_list[i]['loc'], 'end_change'] = True
                    data.ix[ding_di_list[i+3]['loc'], 'bi_value'] = data.ix[ding_di_list[i+2]['loc'], 'low']
                    del ding_di_list[i+1]
                    del ding_di_list[i+2]
                else:
                    data.ix[ding_di_list[i+2]['loc'], 'bi_value'] = data.ix[ding_di_list[i+2]['loc'], 'high']
                    del ding_di_list[i+1]

            elif ding_di_list[i]['fenxing'] == 'di':
                if data.ix[ding_di_list[i-1]['loc'], 'high'] <= data.ix[ding_di_list[i+1]['loc'], 'high']:
                    data.ix[ding_di_list[i-1]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i]['loc'], 'bi_value'] = np.nan
                    data.ix[ding_di_list[i-1]['loc'], 'end_change'] = True
                    data.ix[ding_di_list[i]['loc'], 'end_change'] = True
                    data.ix[ding_di_list[i+1]['loc'], 'bi_value'] = data.ix[ding_di_list[i+1]['loc'], 'high']
                else:
                    data.ix[ding_di_list[i+2]['loc'], 'bi_value'] = data.ix[ding_di_list[i+2]['loc'], 'low']
                    del ding_di_list[i+1]
            else:
                print("Error value %s" % ding_di_list[i])

        if i >= len(ding_di_list) - 3:
            break
    return data


def tag_duan_line(data = None):
    """Class 67"""
    if data is None:
        return None
    bi_data = data[~np.isnan(data.bi_value)]
    print(bi_data)

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
        plt.show()
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
        plt.show()


def main():
    data = ts.get_hist_data('002047','2016-10-01').sort_index()
    plot_data(data, single=True)
    data = baohan_process(data)
    data = find_possible_ding_di(data)
    plot_data(data, single=True)


if __name__ == '__main__':
    main()

