#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: app.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 19 Dec 2016 09:10:17 PM CST

from sqlalchemy.sql import select

from db import dal

def get_stock_pool( ):
    """ 获取需要分析的股票列表 """
    columns= [dal.stock_hist_data.c.code, dal.stock_hist_data.c.close]

    selected_stocks = select(columns)

    return dal.connection.execute(selected_stocks).fetchall()





