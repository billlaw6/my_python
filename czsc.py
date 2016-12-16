#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: Stock_CZSC_Analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 14 Dec 2016 07:16:55 PM CST

import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.finance as mpf
import numpy as np
import pandas as pd
import talib as ta
import pandas as pd

class DataError(ValueError):
    str = "Data should be DataFrame from tushare.get_hist_data() \n"
    pass

class CZSC(object):
    """缠中说缠股票分析工具"""
    data_ori = None
    data_no_baohan = None
    data_ding_di = None
    data_bi = None
    data_bi_mm = None
    data_duan = None

    def baohan_process(self, data = None):
        """
        1、2、3根K线，只2和3有包含关系，包含关系的处理由1和2两K线的升降决定
        Class65.
        必须从左至右顺序处理包含关系，单次遍历就行。包含处理只会缩短K线，不会产生新的包含关系。
        """
        if type(data) != pd.core.frame.DataFrame:
            raise DataError('Data should be DataFrame from tushare.get_hist_data()')
        self.data_ori = data
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
        self.data_no_baohan = data.drop(data[data.delete==True].index)
        return self.data_no_baohan


    def find_possible_ding_di(self, data = None):
        """寻找和标识顶和底，数据类型应该是处理完包含关系之后的数据"""
        if data is None:
            data = self.data_ori
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
        self.data_ding_di = data
        return self.data_ding_di

    def tag_bi_line_mm(self, data = None):
        """给标记顶底之后的数据画笔，采用最高或最低顶底优先原则"""
        # 取出笔开始的所有顶底标记，方便循环处理
        ding_di_list = []
        for i in range(0, len(self.data)-1):
            if type(self.data.ix[i, 'fenxing']) == str:
                if self.data.ix[i, 'fenxing'].find('di') != -1:
                    ding_di = {}
                    ding_di['loc'] = i
                    ding_di['fenxing'] = self.data.ix[i, 'fenxing']
                    ding_di['high'] = self.data.ix[i, 'high']
                    ding_di['low'] = self.data.ix[i, 'low']
                    ding_di_list.append(ding_di)
                else:
                    pass

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
        self.data_bi_mm = data
        return self.data_bi_mm

    def tag_bi_line(self, data = None):
        """给标记顶底之后的数据画笔，采用后出现的顶底优先原则"""
        if data is None:
            data = self.data_ding_di

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
        self.data_bi = data
        return self.data_bi

    def tag_duan_line(self, data = None, show = False):
        """Class 67"""
        if data is None:
            data = self.data_bi
        # 取出所有标记为笔节点的顶底标记，方便循环处理
        if 'bi_value' in data.columns:
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
        else:
            raise DataError('No bi_value attribute in data')

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
                xia = {}
            elif bi_ding_di_list[i]['fenxing'] == 'di':
                shang['low_loc'] = bi_ding_di_list[i]['loc']
                shang['low_value'] = bi_ding_di_list[i]['low']
                shang['high_loc'] = bi_ding_di_list[i+1]['loc']
                shang['high_value'] = bi_ding_di_list[i+1]['high']
                shang_list.append(shang)
                shang = {}

        pd_shang = pd.DataFrame(shang_list)
        pd_xia = pd.DataFrame(xia_list)
        # 处理上行笔特征序列包含关系，往底靠
        for i in range(0, len(pd_shang) - 1):
            if pd_shang.ix[i, 'low_value'] < pd_shang.ix[i+1, 'low_value'] \
            and pd_shang.ix[i, 'high_value'] > pd_shang.ix[i+1, 'high_value']:
                for j in range(1, len(pd_shang) - i - 1):
                    if pd_shang.ix[i, 'low_value'] < pd_shang.ix[i+j, 'low_value'] \
                    and pd_shang.ix[i, 'high_value'] > pd_shang.ix[i+j, 'high_value']:
                        pd_shang.ix[i, 'high_value'] = pd_shang.ix[i+j, 'high_value']
                        pd_shang.ix[i+j, 'remove'] = True
                    else:
                        break
            elif pd_shang.ix[i, 'low_value'] > pd_shang.ix[i+1, 'low_value'] \
            and pd_shang.ix[i, 'high_value'] < pd_shang.ix[i+1, 'high_value']:
                pd_shang.ix[i+1, 'high_value'] = pd_shang.ix[i, 'high_value']
                pd_shang.ix[i, 'remove'] = True
        if 'remove' in pd_shang.columns:
            pd_shang = pd_shang.drop(pd_shang[pd_shang.remove==True].index)
        pd_shang = pd_shang.set_index('low_loc')
        pd_shang = pd_shang.reset_index()
        # 处理上行笔特征序列包含关系，往顶靠
        for i in range(0, len(pd_xia) - 1):
            if pd_xia.ix[i, 'low_value'] < pd_xia.ix[i+1, 'low_value'] \
            and pd_xia.ix[i, 'high_value'] > pd_xia.ix[i+1, 'high_value']:
                for j in range(1, len(pd_xia) - i - 1):
                    if pd_xia.ix[i, 'low_value'] < pd_xia.ix[i+j, 'low_value'] \
                    and pd_xia.ix[i, 'high_value'] > pd_xia.ix[i+j, 'high_value']:
                        pd_xia.ix[i, 'high_value'] = pd_xia.ix[i+j, 'high_value']
                        pd_xia.ix[i+j, 'remove'] = True
                    else:
                        break
            elif pd_xia.ix[i, 'low_value'] > pd_xia.ix[i+1, 'low_value'] \
            and pd_xia.ix[i, 'high_value'] < pd_xia.ix[i+1, 'high_value']:
                pd_xia.ix[i+1, 'low_value'] = pd_xia.ix[i, 'low_value']
                pd_xia.ix[i, 'remove'] = True
        if 'remove' in pd_xia.columns:
            pd_xia = pd_xia.drop(pd_xia[pd_xia.remove==True].index)
        pd_xia = pd_xia.set_index('high_loc')
        pd_xia = pd_xia.reset_index()

        # 标记笔特征序列的顶底,上行笔序列中找底，下行笔序列中找顶
        for i in range(1, len(pd_shang) - 1):
            if pd_shang.ix[i, 'low_value'] <= pd_shang.ix[i-1, 'low_value'] \
            and pd_shang.ix[i, 'low_value'] <= pd_shang.ix[i+1, 'low_value'] \
            and pd_shang.ix[i, 'high_value'] <= pd_shang.ix[i-1, 'high_value'] \
            and pd_shang.ix[i, 'high_value'] <= pd_shang.ix[i+1, 'high_value']:
                pd_shang.ix[i, 'duan_value'] = pd_shang.ix[i, 'low_value']
                data.ix[pd_shang.ix[i, 'low_loc'], 'bi_fenxing'] = 'di'
                data.ix[pd_shang.ix[i, 'low_loc'], 'duan_value'] = pd_shang.ix[i, 'low_value']
        for i in range(1, len(pd_xia) - 1):
            if pd_xia.ix[i, 'high_value'] >= pd_xia.ix[i-1, 'high_value'] \
            and pd_xia.ix[i, 'high_value'] >= pd_xia.ix[i+1, 'high_value'] \
            and pd_xia.ix[i, 'low_value'] >= pd_xia.ix[i-1, 'low_value'] \
            and pd_xia.ix[i, 'low_value'] >= pd_xia.ix[i+1, 'low_value']:
                pd_xia.ix[i, 'duan_value'] = pd_xia.ix[i, 'high_value']
                data.ix[pd_xia.ix[i, 'high_loc'], 'bi_fenxing'] = 'ding'
                data.ix[pd_xia.ix[i, 'high_loc'], 'duan_value'] = pd_xia.ix[i, 'high_value']

        if show:
            # 查看处理后笔特征序列
            plt.rcParams['font.family'] = ['sans-serif'] # 用来正常显示中文标签
            plt.rcParams['font.sans-serif'] = ['Liberation Sans'] # 用来正常显示中文标签
            plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
            fig, axes = plt.subplots(2, 1, sharex=True, figsize=(8,6))
            mpf.candlestick2_ochl(axes[0], pd_shang['low_value'],pd_shang['low_value'],pd_shang['high_value'],pd_shang['low_value'], width=0.6, colorup='r', colordown='g')
            axes[0].set_title("Shang")
            di_pd_shang = pd_shang[pd_shang.duan_value>0]
            axes[0].plot(np.array(di_pd_shang.index), np.array(di_pd_shang.low_value), '^')
            mpf.candlestick2_ochl(axes[1], pd_xia['low_value'],pd_xia['low_value'],pd_xia['high_value'],pd_xia['low_value'], width=0.6, colorup='r', colordown='g')
            axes[1].set_title("Xia")
            ding_pd_xia = pd_xia[pd_xia.duan_value>0]
            axes[1].plot(np.array(ding_pd_xia.index), np.array(ding_pd_xia.high_value), 'v')
            plt.show()
        return  self.data_duan


    def plot_data(self, data = None, single=False):
        """自定义画图"""
        if data is None:
            data = self.data_duan
        plt.rcParams['font.family'] = ['sans-serif'] # 用来正常显示中文标签
        plt.rcParams['font.sans-serif'] = ['Liberation Sans'] # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

        if len(str(data.index[0])) == 10:
            dates = [datetime.datetime(*time.strptime(str(i), '%Y-%m-%d')[:6]) for i in data.index]
        else:
            dates = [datetime.datetime(*time.strptime(str(i), '%Y-%m-%d %H:%M:%S')[:6]) for i in data.index]

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
            dflen = len(self.data)
            if dflen > 35:
                macd, macdsignal, macdhist = ta.MACD(np.array(self.data['close']),
                                                     fastperiod=12, slowperiod=26,
                                                     signalperiod=9)
                self.data['macd']=pd.Series(macd,index=self.data.index)
                self.data['macdsignal']=pd.Series(macdsignal,index=self.data.index)
                self.data['macdhist']=pd.Series(macdhist,index=self.data.index)
                self.data.set_index('t')
                self.data = self.data.set_index('t')
                self.data[['macd','macdsignal','macdhist']].plot(ax=axes[2])
                axes[2].axhline()
        else:
            self.data['t'] = mdates.date2num(dates)
            adata = self.data[['t','open','close','high','low','volume']]
            ddata = zip(np.array(adata.t), np.array(adata.open), np.array(adata.close), np.array(adata.high), np.array(adata.low), np.array(adata.volume))
            fig, ax = plt.subplots(1, 1, figsize=(8,6))

            mpf.candlestick_ochl(ax, ddata, width=0.6, colorup='r', colordown='g')
            ax.set_ylabel('price')
            ax.grid(True)
            ax.xaxis_date()
            ax.autoscale_view()

        # 有顶底标记时画顶底标记
        if 'fenxing' in self.data.columns:
            p_data = self.data[self.data.fenxing == 'ding']
            b_data = self.data[self.data.fenxing == 'di']
            ax = plt.gca()
            ax.plot(np.array(p_data.t), np.array(p_data.high), 'v')
            ax.plot(np.array(b_data.t), np.array(b_data.low), '^')

        # 有笔标记时添加笔线条 
        if 'bi_value' in self.data.columns:
            bi_data = self.data[~np.isnan(self.data.bi_value)]
            ax.plot(np.array(bi_data.t), np.array(bi_data.bi_value))

        # 有段标记时添加段线条 
        if 'duan_value' in self.data.columns:
            duan_data = self.data[~np.isnan(self.data.duan_value)]
            # print("duan_data %s" % duan_data)
            ax.plot(np.array(duan_data.t), np.array(duan_data.duan_value), color='b', linewidth=2)
        plt.show()



