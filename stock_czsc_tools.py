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
    for i in range(0, len(data)-2):
        # 当前K线的升降属性由后一根K线组合确定
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
            # 出现包含关系时，保留后一条K线，方便解决合并后但数据未清理时的数据比较
            data.ix[i, 'delete'] = True
            # default type is UP
            if i == 0:
                data.ix[i+1, 'high'] = data.ix[i, 'high']
            #elif data[i-1: i].type[0] == 'up':
            elif up_down_flag == 'up':
                data.ix[i+1, 'high'] = data.ix[i, 'high']
            #elif data[i-1: i].type[0] == 'down':
            elif up_down_flag == 'down':
                data.ix[i+1, 'low'] = data.ix[i, 'low']
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
        else:
            data.ix[i, 'type'] = 'unknown'


    data = data.drop(data[data.delete == True].index)

    if len(data[data.type == 'delete']) > 0:
        data = baohan_process(data.drop(data[data.delete == True].index))
    #
    for i in range(0, len(data)-2):
        # 当前K线的升降属性由后一根K线组合确定
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
    """处理连续的顶或连续的底的情况，顶底处理第三步"""
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

    for i in range(0, len(ding_di_list) - 3):
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
    return data

def find_effective_start(data = None):
    """Must in firt 4 ding di"""
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

    if len(ding_di_list) <= 2:
        print("deng zhe!!!")
    elif len(ding_di_list) == 3:
        if ding_di_list[1]['loc'] - ding_di_list[0]['loc'] > 3 \
       and ding_di_list[2]['loc'] - ding_di_list[1]['loc'] > 3:
            print("Found effective start %s" % data.ix[ding_di_list[0]['loc']])
        else:
            print("ji xu deng zhe!!!")
    elif len(ding_di_list) == 4:
        effective_start_data_index = 0
        effective_start_ding_di_index = 0
        for i in range(0, len(ding_di_list) - 2):
            if ding_di_list[i+1]['loc'] - ding_di_list[i]['loc'] > 3 \
           and ding_di_list[i+2]['loc'] - ding_di_list[i+1]['loc'] > 3:
                print("Found effective start %s" % data.ix[ding_di_list[i]['loc']])
                effective_start_data_index = data.ix[ding_di_list[i]['loc']]
                effective_start_ding_di_index = i
                break

        # 
        if effective_start_data_index > 0:
            for i in range(effective_start_ding_di_index, len(ding_di_list) - 2):
                if ding_di_list[i+1]['loc'] - ding_di_list[i]['loc'] > 3:
                    if data.ix[ding_di_list[i]['loc'], 'fenxing'] == 'ding':
                        data.ix[i, 'bi_line'] == data.ix[i, 'high']
                        data.ix[i+1, 'bi_line'] == data.ix[i, 'low']
                    elif data.ix[ding_di_list[i]['loc'], 'fenxing'] == 'di':
                        data.ix[i, 'bi_line'] == data.ix[i, 'low']
                        data.ix[i+1, 'bi_line'] == data.ix[i, 'high']
                    else:
                        print("Shen ma qing kuang in tag bi line")
                else:
                    pass





    return data


def draw_bi_line(data = None):
    """给clear_continous_ding_di处理之后的数据画笔"""
    if data is None:
        return None

    for i in range(1, len(data) - 3):
        # 在i位置找到首个顶或底，由此开始找后续的顶或底判断当前顶或底是否成立
        if data.ix[i, 'fenxing'].find('di') != -1:
            current_fenxing = data[i, 'fenxing']
            # 从i+1开始找第二个顶底分型，如果满足笔的条件，则继续看后续是否满足笔，满足连续两笔，确定找到正确的开始分型
            for j in range(i+1, len(data) - 3):
                if data.ix[j, 'fenxing'].find('di') != -1 and (j - i > 3):
                    for k in range(j+1, len(data) - 3):
                        if data.ix[k, 'fenxing'].find('di') != -1 and (k - j > 3):
                            print("Found start :%s" % data.ix[i])
                            data.ix[i]
                        else:
                            print("第二段不满足")
    return data


def tech_analysis(data = None):
    """data为get_hist_data取的结果，并且按日期从旧到新排列"""
    if data is None:
        return None
    # 取最大的顶为起始往两边标识有效顶和底
    start_index = data[0:1].index[0]
    end_index = data[len(data)-1:len(data)].index[0]
    start_ding = data.loc[data[data.type=='ding'].groupby('type')['high'].idxmax()].index[0]
    print("start_ding: %s" % start_ding)
    data.loc[start_ding, 'tag'] = 'ding'
    data_a = data[start_index: start_ding].sort_index(ascending=False)
    data_b = data[start_ding: end_index]
    #print("data a: %s" % data_a)
    #print("data b: %s" % data_b)

    # 用原来标识删除的tag字段标识有效的顶和底
    # 首先标识起始点
    data.loc[start_ding, 'tag'] = 'ding'
    # 由起始点往两边标识顶和底
    data_a1 = tag_ding_di(data_a)
    data_b1 = tag_ding_di(data_b)
    #print("data a1: %s" % data_a1)
    #print("data b1: %s" % data_b1)
    # pd.concat([obj1, obj2], axis=1)
    data = data_a1.append(data_b1).sort_index().drop_duplicates()
    #print(data)
    return data
    
def draw_data(data = None):
    """自定义画图"""
    if data is None:
        print("Data is None!")
        exit
    dates = [datetime.datetime(*time.strptime(i, '%Y-%m-%d')[:6]) for i in data.index]

    # 多指标同图
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



def main():
    data = ts.get_hist_data('002047','2016-06-01').sort_index()
    #print(data)
    draw_data(data)
    data1 = clear_data(data)
    print(data1)
    #data2 = find_possible_ding_di(data1)
    #print(data2)
    #draw_data(data)
    #data3 = tech_analysis(data2)
    #print(data3)
    # price = data[['high', 'low']]
    # pic = price.plot()
    # ax = gca()
    # import math
    # #data4 = data3.loc[math.isnan(data3['line'])]
    # data4 = data3.loc[data3['line'] > 0]
    # czsc = data4[['line']]
    # czsc.plot()
    # show()


if __name__ == '__main__':
    main()

