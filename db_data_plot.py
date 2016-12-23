#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_data_plot.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Fri 23 Dec 2016 08:47:47 AM CST
# Description: 

import pandas as pd
import numpy as np
import matplotlib.finance as mpf
import matplotlib.pyplot as plt

from db_core import dal
import czsc

dal.db_init('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')

sql = """select * from get_hist_data
    where code = '%s' and ktype = '%s'
    order by date desc
    limit 30""" % ('sh', '30')
data = pd.read_sql(sql, dal.engine)
data.sort_values(by='date', ascending=True, inplace=True)
data['x_axis'] = range(len(data))
data.set_index(keys='date', drop=False, inplace=True)
data = czsc.tag_bi_line(data)


# fig, ax = plt.subplots(1, 1)
# mpf.candlestick2_ochl(ax, np.array(data.open), np.array(data.close), np.array(data.high), np.array(data.low), width=0.6, colorup='r', colordown='g')
# plt.show()

czsc.plot_data(data, single=True, ktype='30')
