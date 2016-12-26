#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: update_test.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 26 Dec 2016 11:14:51 AM CST
# Description: 

from sqlalchemy import update
from sqlalchemy import create_engine, select, insert, update, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, bindparam
import pandas as pd

from db_core import dal
import czsc

dal.db_init()

s = dal.get_hist_data.select( and_((dal.get_hist_data.c.code == 'sh'),
                             (dal.get_hist_data.c.date == '2016-12-23'),
                             (dal.get_hist_data.c.ktype == 'D')))
rs = dal.connection.execute(s).fetchall()
print(rs)

sql = """select * from get_hist_data
where code= 'sh'
and date >= '2016-12-18'
and ktype= 'D'"""

data = pd.read_sql_query( sql, dal.engine )

data = data.set_index('date', drop=False)
data = czsc.tag_bi_line(data)

u_data = []
tmp = {}
for i in range(len(data)):
    tmp['code'] = data.ix[i, 'code']
    tmp['date'] = data.ix[i, 'date']
    tmp['fenxing'] = data.ix[i, 'fenxing']
    tmp['bi_value'] = data.ix[i, 'bi_value']
    u_data.append(tmp)

u = dal.get_hist_data.update().\
        where(
            and_(dal.get_hist_data.c.code== bindparam('code'),
                 dal.get_hist_data.c.date == bindparam('date')
                )
        ).\
        values(fenxing = bindparam('fenxing'))
dal.connection.execute(u, u_data)
