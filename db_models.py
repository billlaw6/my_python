#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_models.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 15 Dec 2016 01:48:26 PM CST

import enum
from sqlalchemy import (create_engine, MetaData, Table, Column, DateTime, Integer, Numeric, String, Enum)
from sqlalchemy import and_, or_, not_
from sqlalchemy.dialects.mysql import \
                BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
                DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
                LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
                NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
                TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

metadata = MetaData()

class Ktype(enum.Enum):
	m5 = "5"
	m30 = "30"
	D = "D"
	W = "W"
	M = "M"

stock_hist_data = Table('stock_hist_data1', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(30)), # or Column(String(30))
	Column('date', DateTime(), nullable = False),
	Column('open',Numeric(12, 2)),
	Column('high', Numeric(12, 2)),
	Column('close', Numeric(12, 2)),
	Column('low', Numeric(12, 2)),
	Column('volume', Numeric(12, 2)),
	Column('price_change', Numeric(12, 2)),
	Column('p_change', Numeric(12, 2)),
	Column('ma5', Numeric(12, 2)),
	Column('ma10', Numeric(12, 2)),
	Column('ma20', Numeric(12, 2)),
	Column('v_ma5', Numeric(12, 2)),
	Column('v_ma10', Numeric(12, 2)),
	Column('v_ma20', Numeric(12, 2)),
	Column('turnover', Numeric(12, 2)),
	Column('code', String(6)),
	#Column('ktype', Enum(Ktype)),
	Column('ktype', String(6)),
	Column('type', String(6)),
	Column('fenxing', String(6)),
	Column('bi_value', Numeric(12, 2)),
	Column('duan_value', Numeric(12, 2))
)

engine = create_engine('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')
metadata.create_all(engine)

s = select([stock_hist_data]).where(
    and_(
        stock_hist_data.c.close > 10,
        stock_hist_data.c.column < 15
    )
)


