#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: app.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 19 Dec 2016 09:10:17 PM CST

import stock_select as ss
import stock_localize_data as sld

stock_list = ss.basic_select()
sld.basic_data()
sld.h_data(stock_list)
sld.hist_data(stock_list)







