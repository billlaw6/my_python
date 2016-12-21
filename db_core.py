#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_core.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 15 Dec 2016 01:48:26 PM CST

from datetime import datetime
from sqlalchemy import (create_engine, MetaData, Table, Column, DateTime,
                        Date, Integer, Numeric, String, Index, ForeignKey)

class DataAccessLayer(object):
    connection = None
    engine = None
    conn_string = None
    metadata = MetaData()

    index_data = Table('index_data', metadata,
        Column('code', String(6)), # 指数代码
        Column('name', String(50)), # 指数名称
        Column('change', Numeric(12, 4)), # 涨跌幅
        Column('open', Numeric(12, 4)), # 开盘点位
        Column('preclose', Numeric(12, 4)), # 昨日收盘点位
        Column('close', Numeric(12, 4)), # 收盘点位
        Column('high', Numeric(12, 4)), # 最高点位
        Column('low', Numeric(12, 4)), # 最低点位
        Column('volume', Numeric(12, 4)), # 成交量(手)
        Column('amount', Integer()), # 成交金额（亿元）
        Column('created_on', Date(), default = datetime.now), # 获取时间
    )

    stock_basics = Table('stock_basics', metadata,
        Column('id', Integer, primary_key=True),
        Column('code', String(6)),
        Column('name', String(50), index=True), #
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

    today_all = Table('today_all', metadata,
        Column('code', String(6), ForeignKey('stock_basics.code')), # 代码
        Column('name', String(50), index=True), # 名称
        Column('changepercent', Numeric(12, 4)), # 涨跌幅
        Column('trade', Numeric(12, 4)), # 现价
        Column('open', Numeric(12, 4)), # 开盘价
        Column('high', Numeric(12, 4)), # 最高价
        Column('low', Numeric(12, 4)), # 最低价
        Column('settlement', Numeric(12, 4)), # 昨日收盘价
        Column('volume', Numeric(12, 4)), # 成交量
        Column('turnoverratio', Numeric(12, 4)), # 换手率
        Column('amount', Numeric(12, 4)), # 成交量
        Column('per', Numeric(12, 4)), # 市盈率
        Column('pb', Numeric(12, 4)), # 市净率
        Column('mktcap', Numeric(12, 4)), # 总市值
        Column('nmc', Numeric(12, 4)), # 流通市值
        Column('created_on', Date(), default = datetime.now), # 获取时间
     )


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
        Column('ktype', String(6)), # K
        Column('type', String(6)),  # ding_di
        Column('fenxing', String(6)),
        Column('bi', Numeric(12, 4)),
        Column('bi_value', Numeric(12, 4)),
        Column('duan_value', Numeric(12, 4)),
        Index('ix_stock_hist_data', 'code', 'date', 'ktype', unique=True),
    )

    profit_data = Table('profit_data', metadata,
        Column('code', String(6), ForeignKey('stock_basics.code')), # 代码
        Column('name', String(50), index=True), # 股票名称
        Column('year', Integer( )), # 分配年份
        Column('report_date', Date( )), # 公布日期
        Column('divi', Numeric(12, 4)), # 分红金额（每10股）
        Column('shares', Numeric(12, 4)), # 转增和送股数（每10股）
	)

	# 
    forecast_data = Table('forecast_data', metadata,
        Column('code', String(6), ForeignKey('stock_basics.code')), # 代码
        Column('name', String(50), index=True), # 股票名称
        Column('type', String(6)),  # 业绩变动类型【预增、预亏等】
        Column('report_date', Date( )), # 公布日期
        Column('pre_eps', Numeric(12, 4)), # 上年同期每股收益
        Column('range', Numeric(12, 4)), # 业绩变动范围
	)

	#
    code：股票代码
    name：股票名称
    date:解禁日期
    count:解禁数量（万股）
    ratio:占总盘比率

	# 基金持股

    code：股票代码
    name：股票名称
    date:报告日期
    nums:基金家数
    nlast:与上期相比（增加或减少了）
    count:基金持股数（万股）
    clast:与上期相比
    amount:基金持股市值
    ratio:占流通盘比率


    code：股票代码
    name：股票名称
    ipo_date:上网发行日期
    issue_date:上市日期
    amount:发行数量(万股)
    markets:上网发行数量(万股)
    price:发行价格(元)
    pe:发行市盈率
    limit:个人申购上限(万股)
    funds：募集资金(亿元)
    ballot:网上中签率(%)



    db_init(self, conn_string):
        self.engine = create_engine(conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

dal = DataAccessLayer()




