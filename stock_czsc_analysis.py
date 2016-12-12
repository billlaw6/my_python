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



def main():
    #data = ts.get_hist_data('sh', end='2007-06-30', ktype='W').sort_index()
    #data = ts.get_hist_data('sh', '2002-01-01', '2016-01-01', ktype='M').sort_index()
    #data = pd.read_sql_table('sh_test_data', engine)
    #print(data)
    #data = pd.read_csv(u'./sh_M.csv')
    data = ts.get_hist_data('002047', '2016-10-01', ktype='D').sort_index()
    #data = data.set_index('date')
    #draw_czsc(data)


if __name__ == '__main__':
    main()

