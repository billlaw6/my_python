#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_schema.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 19 Dec 2016 10:05:19 PM CST

from sqlalchemy import MetaData, create_engine

metadata = MetaData()

engine = create_engine('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')

metadata.reflect(bind=engine)

print(metadata.tables.keys())
