#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stocks_draw_test.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Tue 15 Nov 2016 10:33:46 AM CST

import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import matplotlib.dates as mdates
import datetime
import numpy as np
import time
import talib as ta
import pandas as pd
import talib

data = ts.get_hist_data('002780', '2016-01-01').sort_index()
# tichutingpanshujv
data[data['volume']==0] = np.nan
data = data.dropna()
dates = [datetime.datetime(*time.strptime(i, '%Y-%m-%d')[:6]) for i in
         data.index]
data['t'] = mdates.date2num(dates)
data = data.set_index('t', drop=False)
adata = data[['t','open','close','high','low','volume']]
ddata = zip(np.array(data.t), np.array(data.open), np.array(data.close),
           np.array(data.high), np.array(data.low), np.array(data.volume))
d_volume = zip(np.array(data.t), np.array(data.volume))

fig, axes = plt.subplots(3, 1, sharex=True)

mpf.candlestick_ochl(axes[0], ddata, width=0.6, colorup='r', colordown='g')
axes[0].xaxis_date()
# axes[0].autoscale_view()

axes[1].bar(np.array(data.t), np.array(data.volume))
#data['volume'].plot(ax = axes[1], kind = 'bar')
axes[1].xaxis_date()
data['m5_v']=talib.MA(np.array(data['volume']), timeperiod=5)
data['m5_v'].plot(ax = axes[1], kind = 'line')


if len(data) > 35:
    macd, macdsignal, macdhist = ta.MACD(np.array(data['close']), fastperiod=12, slowperiod=26, signalperiod=9)
    data['macd']=pd.Series(macd,index=data.index)
    data['macdsignal']=pd.Series(macdsignal,index=data.index)
    data['macdhist']=pd.Series(macdhist,index=data.index)
    data = data.set_index('t', drop=False)
    data[['macd','macdsignal','macdhist']].plot(ax=axes[2])
    axes[2].axhline()
    # axes[2].axhspan()
plt.title('002780')

ope_d = data[data.index.isin([736212.0, 736262.0])]
ope_d['close'].plot(ax = axes[0], kind='line')

plt.show()


