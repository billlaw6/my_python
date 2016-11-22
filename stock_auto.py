#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: 当前日期: 2016-08-25 星期四 输入新日期: (年月日) 
#
# @desc:
#
# @history
#
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

def clear_data(data = None):
    """清理被包含的数据便于分析顶和底，数据类型应该是tushare.get_hist_data获得的dataFrame格式"""
    if data is None:
        return None
    #print("Length of data before clean is %s" % len(data))

    for i in range(0, len(data)-2):
        if float(data[i:i+1].high) >= float(data[i+1:i+2].high) \
        and float(data[i:i+1].low) <= float(data[i+1:i+2].low):
            data.loc[data[i+1:i+2].index[0], 'tag'] = 'delete'
        elif float(data[i:i+1].high) <= float(data[i+1:i+2].high) \
        and float(data[i:i+1].low) >= float(data[i+1:i+2].low):
            data.loc[data[i:i+1].index[0], 'tag'] = 'delete'

    #print(data[data.tag == 'delete'])
    if len(data[data.tag == 'delete']) > 0:
        #data, count = clear_data(data.drop(data[data.tag == 'delete'].index))
        data = clear_data(data.drop(data[data.tag == 'delete'].index))
    #return data.drop(data[data.tag == 'delete'].index), len(data[data.tag == 'delete'])
    return data.drop(data[data.tag == 'delete'].index)

def find_possible_ding_di(data = None):
    """寻找和标识顶和底，数据类型应该是tushare.get_hist_data获得的dataFrame格式"""
    if data is None:
        return None

    for i in range(1, len(data)-3):
        if float(data[i: i + 1].high) > float(data[i - 1: i].high) \
        and float(data[i: i + 1].high) > float(data[i + 1: i + 2].high) \
        and float(data[i: i + 1].low) > float(data[i - 1: i].low) \
        and float(data[i: i + 1].low) > float(data[i + 1: i + 2].low):
            data.loc[data[i: i + 1].index[0], 'type'] = 'ding'
        elif float(data[i: i + 1].high) < float(data[i - 1: i].high) \
        and float(data[i: i + 1].high) < float(data[i + 1: i + 2].high) \
        and float(data[i: i + 1].low) < float(data[i - 1: i].low) \
        and float(data[i: i + 1].low) < float(data[i + 1: i + 2].low):
            data.loc[data[i: i + 1].index[0], 'type'] = 'di'
        else:
            data.loc[data[i: i + 1].index[0], 'type'] = 'phase'
    return data

def tag_ding_di(data = None):
    """标记有效的顶和底，参数为清理并初标了顶和底，以最高顶为起点的数据。"""
    # 记录当前有效标记为顶还是底，以便明确接下来寻找的标记。
    current_state = data[0:1].type[0]
    data.loc[data[0:1].index[0], 'line'] = data.loc[data[0:1].index[0], 'high']
    # 有效间隔数量
    count = 0
    for i in range(1, len(data) - 1):
        # 根据当前状态找3个phase之外的顶或底
        if current_state == 'ding':
            if data[i: i+1].type[0] == 'di' and count >= 3:
                count_b = 0
                for j in range(i, len(data) - 1):
                    if data[j: j+1].type[0] == 'ding' and count_b >= 3:
                        data.loc[data[i:i+1].index[0], 'tag'] = 'di'
                        data.loc[data[i:i+1].index[0], 'line'] = data.loc[data[i:i+1].index[0], 'low']
                        current_state = 'di'
                        count = 0
                    elif data[j: j+1].type[0] == 'di' and (float(data[j: j+1].low) < float(data[i: i+1].low)):
                        i = j
                        break
                    else:
                        count_b += 1
            else:
                data.loc[data[i:i+1].index[0], 'tag'] = 'phase'
                count += 1
        elif current_state == 'di':
            if data[i: i+1].type[0] == 'ding' and count >= 3:
                count_b = 0
                for j in range(i, len(data) - 1):
                    if data[j: j+1].type[0] == 'di' and count_b >= 3:
                        data.loc[data[i:i+1].index[0], 'tag'] = 'ding'
                        data.loc[data[i:i+1].index[0], 'line'] = data.loc[data[i:i+1].index[0], 'high']
                        current_state = 'ding'
                        count = 0
                    elif data[j: j+1].type[0] == 'ding' and (float(data[j: j+1].low) > float(data[i: i+1].low)):
                        i = j
                        break
                    else:
                        count_b += 1
            else:
                data.loc[data[i:i+1].index[0], 'tag'] = 'phase'
                count += 1
    return data

def tag_ding_di_t(data = None):
    """按时间顺序标顶和底"""
    if data is None:
        return None

    # 找到首个可能的顶或底，由此开始找后续的顶或底判断当前顶或底是否成立
    for i in range(0, len(data) - 1):
        if data[i: i+1].type[0] == 'ding' or data[i: i+1].type[0] == 'di':
            current_type = data[i: i+1].type[0]
            start_index = i
            print("date: %s, start_index: %s, type: %s" % (data[start_index: start_index+1].index, start_index, data[start_index: start_index+1].type[0]))
            break

    # 有效间隔数量
    count = 0
    for i in range(start_index + 1, len(data) - 1):
        # 根据当前状态找3个phase之外的顶或底
        if current_type == 'ding':
            if data[i: i+1].type[0] == 'di' and count >= 3:
                count_b = 0
                for j in range(i, len(data) - 1):
                    if data[j: j+1].type[0] == 'ding' and count_b >= 3:
                        data.loc[data[i:i+1].index[0], 'tag'] = 'di'
                        data.loc[data[start_index:start_index+1].index[0], 'line'] = data.loc[data[i:i+1].index[0], 'high']
                        data.loc[data[i:i+1].index[0], 'line'] = data.loc[data[i:i+1].index[0], 'low']
                        current_type = 'di'
                        count = 0
                    elif data[j: j+1].type[0] == 'di' and (float(data[j: j+1].low) < float(data[i: i+1].low)):
                        i = j
                        break
                    else:
                        count_b += 1
            elif data[i: i+1].type[0] == 'di':
                start_index = i
                current_type = data[i: i+1].type[0]
                print("New start ___ date: %s, start_index: %s, type: %s, current_type: %s" % (data[start_index: start_index+1].index, start_index, data[start_index: start_index+1].type[0], current_type))
                continue
            elif data[i: i+1].type[0] == 'ding' and (float(data[i: i+1].high) >= float(data[start_index: start_index+1].high)):
                start_index = i
                current_type = data[i: i+1].type[0]
                print("New start ___ date: %s, start_index: %s, type: %s, current_type: %s" % (data[start_index: start_index+1].index, start_index, data[start_index: start_index+1].type[0], current_type))
                continue
            else:
                data.loc[data[i:i+1].index[0], 'tag'] = 'phase'
                count += 1
        elif current_type == 'di':
            if data[i: i+1].type[0] == 'ding' and count >= 3:
                count_b = 0
                for j in range(i, len(data) - 1):
                    if data[j: j+1].type[0] == 'di' and count_b >= 3:
                        data.loc[data[i:i+1].index[0], 'tag'] = 'ding'
                        data.loc[data[start_index:start_index+1].index[0], 'line'] = data.loc[data[i:i+1].index[0], 'low']
                        data.loc[data[i:i+1].index[0], 'line'] = data.loc[data[i:i+1].index[0], 'high']
                        current_type = 'ding'
                        count = 0
                    elif data[j: j+1].type[0] == 'ding' and (float(data[j: j+1].low) > float(data[i: i+1].low)):
                        i = j
                        break
                    else:
                        count_b += 1
            elif data[i: i+1].type[0] == 'di':
                start_index = i
                current_type = data[i: i+1].type[0]
                print("New start ___ date: %s, start_index: %s, type: %s" % (data[start_index: start_index+1].index, start_index, data[start_index: start_index+1].type[0]))
            elif data[i: i+1].type[0] == 'di' and (float(data[i: i+1].low) >= float(data[start_index: start_index+1].low)):
                start_index = i
                current_type = data[i: i+1].type[0]
                print("New start ___ date: %s, start_index: %s, type: %s" % (data[start_index: start_index+1].index, start_index, data[start_index: start_index+1].type[0]))
            else:
                data.loc[data[i:i+1].index[0], 'tag'] = 'phase'
                count += 1
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

