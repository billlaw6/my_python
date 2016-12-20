#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_reflect_orm.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 19 Dec 2016 10:35:40 PM CST

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

Base = automap_base()

engine = create_engine('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')

Base.prepare(engine, reflect=True)

print(Base.classes.keys())
print(Base.classes['stock_hist_data1'])


