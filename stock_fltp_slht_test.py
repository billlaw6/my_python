#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_fltp_slht_test.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 16 Nov 2016 03:57:02 PM CST

import tushare as ts

p_threshold = 2
v_threshold = 0.05
count_limit = 3
continuous = True


count = 0
data = ts.get_hist_data('002780', '2016-01-01').sort_index()
for i in range(0, len(data) - 1):
    if (float(data[i: i+1].p_change) >= p_threshold) and ((float(data[i+1: i+2].p_change)/float(data[i: i+1].p_change)) > (1+v_threshold)):
        print("limit up %s " % data[i: i+1].index[0])
        count = count + 1
    else:
        if continuous:
            count = 0
        else:
            pass
    if count >= count_limit:
        print("meet count limit: %s " % (data[i: i+1].index[0]))
