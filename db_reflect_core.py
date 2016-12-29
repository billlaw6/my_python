#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_reflect_core.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 19 Dec 2016 10:05:19 PM CST

from sqlalchemy import MetaData, create_engine, Table, select

metadata = MetaData()

engine = create_engine('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')

metadata.reflect(bind=engine)

print(metadata.tables.keys())
shd = Table('stock_hist_data1', metadata, autoload=True, autoload_with=engine)
print(shd.columns.keys())
print(metadata.tables['stock_hist_data1'])

shd = metadata.tables['stock_hist_data1']
s = select([shd]).limit(10)
engine.execute(s).fetchall()



