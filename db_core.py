#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_core.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 15 Dec 2016 01:48:26 PM CST

from datetime import datetime
from sqlalchemy import (create_engine, MetaData, Table, Column, DateTime,
                        Integer, Numeric, String, Index)

class DataAccessLayer(object):
    connection = None
    engine = None
    conn_string = None
    metadata = MetaData()

    stock_hist_data = Table('stock_hist_data', metadata,
        Column('id', Integer, primary_key=True),
        Column('date', DateTime(), nullable = False),
        Column('open',Numeric(12, 4)),
        Column('high', Numeric(12, 4)),
        Column('close', Numeric(12, 4)),
        Column('low', Numeric(12, 4)),
        Column('volume', Numeric(12, 4)),
        Column('price_change', Numeric(12, 4)),
        Column('p_change', Numeric(12, 4)),
        Column('ma5', Numeric(12, 4)),
        Column('ma10', Numeric(12, 4)),
        Column('ma20', Numeric(12, 4)),
        Column('v_ma5', Numeric(12, 4)),
        Column('v_ma10', Numeric(12, 4)),
        Column('v_ma20', Numeric(12, 4)),
        Column('turnover', Numeric(12, 4)),
        Column('code', String(6)),
        Column('ktype', String(6)),
        Column('type', String(6)),
        Column('fenxing', String(6)),
        Column('bi_value', Numeric(12, 4)),
        Column('duan_value', Numeric(12, 4)),
        Index('ix_stock_hist_data', 'code', 'date', 'ktype', unique=True),
    )

    stock_basics = Table('stock_basics', metadata,
        Column('id', Integer, primary_key=True),
        Column('code', String(6)),
        Column('name', String(30), index=True), #
        Column('industry', String(30)), # 所属行业
        Column('area', String(30)), # 地区
        Column('pe', Numeric(12, 4)), # 市盈率
        Column('outstanding', Numeric(12, 4)), # 流通股本(亿)
        Column('totals', Numeric(12, 4)), # 总股本(亿)
        Column('totalAssets', Numeric(12, 4)), # 总资产(万)
        Column('liquidAssets', Numeric(12, 4)), # 流动资产
        Column('fixedAssets', Numeric(12, 4)), # 固定资产
        Column('reserved', Numeric(12, 4)), # 公积金
        Column('reservedPerShare', Numeric(12, 4)), # 每股公积金
        Column('esp', Numeric(12, 4)), # 每股收益
        Column('bvps', Numeric(12, 4)), # 每股净资
        Column('pb', Numeric(12, 4)), # 市净率
        Column('timeToMarket', Numeric(12, 4)), # 上市日期
        Column('undp', Numeric(12, 4)), # 未分利润
        Column('perundp', Numeric(12, 4)), # 每股未分配
        Column('rev', Numeric(12, 4)), # 收入同比(%)
        Column('profit', Numeric(12, 4)), # 利润同比(%)
        Column('gpr', Numeric(12, 4)), # 毛利率(%)
        Column('npr', Numeric(12, 4)), # 净利润率(%)
        Column('holders', Integer()), # 股东人数
        Column('created_on', DateTime(), default = datetime.now), # 获取时间
        Index('ix_stock_basics', 'code', 'industry'),
    )

    def db_init(self, conn_string):
        self.engine = create_engine(conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()



dal = DataAccessLayer()




