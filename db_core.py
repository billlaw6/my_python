#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_core.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Thu 15 Dec 2016 01:48:26 PM CST

from datetime import datetime
from sqlalchemy import (create_engine, MetaData, Table, Column, DateTime, Boolean,
                       Date, Integer, Numeric, String, Text, Index)

class DataAccessLayer(object):
    """ 缠中学缠数据库结构层 """
    connection = None
    engine = None
    conn_string = 'mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8'
    metadata = MetaData()


    # 大盘指数行情列表
    get_index = Table('get_index', metadata,
        Column('code', String(6)), # 指数代码
        Column('name', String(50)), # 指数名称
        Column('change', Numeric(12, 4)), # 涨跌幅
        Column('open', Numeric(12, 4)), # 开盘点位
        Column('preclose', Numeric(12, 4)), # 昨日收盘点位
        Column('close', Numeric(12, 4)), # 收盘点位
        Column('high', Numeric(12, 4)), # 最高点位
        Column('low', Numeric(12, 4)), # 最低点位
        Column('volume', Numeric(20, 4)), # 成交量(手)
        Column('amount', Integer()), # 成交金额（亿元）
        Column('date', Date(), default = datetime.now), # 获取时间
        Index('ix_get_index', 'code', 'date', unique=True),
    )

    # 股票列表
    get_stock_basics = Table('get_stock_basics', metadata,
        Column('id', Integer(), primary_key=True),
        Column('code', String(6)),
        Column('name', String(50), index=True), #
        Column('industry', String(30)), # 所属行业
        Column('area', String(30)), # 地区
        Column('pe', Numeric(12, 4)), # 市盈率
        Column('outstanding', Numeric(12, 4)), # 流通股本(亿)
        Column('totals', Numeric(12, 4)), # 总股本(亿)
        Column('totalAssets', Numeric(20, 4)), # 总资产(万)
        Column('liquidAssets', Numeric(20, 4)), # 流动资产
        Column('fixedAssets', Numeric(20, 4)), # 固定资产
        Column('reserved', Numeric(20, 4)), # 公积金
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
        Column('date', DateTime(), default = datetime.now), # 获取时间
        Index('ix_get_stock_basics', 'code', 'date', unique=True),
    )

    get_today_all = Table('get_today_all', metadata,
        Column('code', String(6), index=True), # 代码
        Column('name', String(50), index=True), # 名称
        Column('changepercent', Numeric(12, 4)), # 涨跌幅
        Column('trade', Numeric(12, 4)), # 现价
        Column('open', Numeric(12, 4)), # 开盘价
        Column('high', Numeric(12, 4)), # 最高价
        Column('low', Numeric(12, 4)), # 最低价
        Column('settlement', Numeric(12, 4)), # 昨日收盘价
        Column('volume', Numeric(20, 4)), # 成交量
        Column('turnoverratio', Numeric(20, 6)), # 换手率
        Column('amount', Numeric(20, 4)), # 成交量
        Column('per', Numeric(12, 4)), # 市盈率
        Column('pb', Numeric(12, 4)), # 市净率
        Column('mktcap', Numeric(20, 6)), # 总市值
        Column('nmc', Numeric(20, 6)), # 流通市值
        Column('date', Date(), default = datetime.now), # 获取时间
        Index('ix_today_all', 'code', 'date', unique=True),
     )


    get_hist_data = Table('get_hist_data', metadata,
        Column('id', Integer(), primary_key=True),
        Column('date', DateTime(), nullable = False),
        Column('open',Numeric(12, 4)),
        Column('high', Numeric(12, 4)),
        Column('close', Numeric(12, 4)),
        Column('low', Numeric(12, 4)),
        Column('volume', Numeric(20, 4)),
        Column('price_change', Numeric(12, 4)),
        Column('p_change', Numeric(12, 4)),
        Column('ma5', Numeric(12, 4)),
        Column('ma10', Numeric(12, 4)),
        Column('ma20', Numeric(12, 4)),
        Column('v_ma5', Numeric(20, 4)),
        Column('v_ma10', Numeric(20, 4)),
        Column('v_ma20', Numeric(20, 4)),
        Column('turnover', Numeric(12, 4)),
        Column('diff', Numeric(12, 4)),
        Column('dea', Numeric(12, 4)),
        Column('macd', Numeric(12, 4)),
        Column('code', String(6)),
        Column('ktype', String(6)), # K线周期
        Column('type', String(6)),  # 当前K线与后K线形成up还是down关系
        Column('delete', Boolean()),  # 当前K线与后K线形成up还是down关系
        Column('fenxing', String(6)), # 顶ding和底di标识
        Column('fx_weight', Numeric(12, 4)), # 分型权重
        Column('bi_to_be', Numeric(12, 4)), # 可能的笔节点的值
        Column('bi_value', Numeric(12, 4)), # 确定的笔节点的值
        Column('duan_value', Numeric(12, 4)), # 段节点的值
        Column('operate', String(6)),
        Index('ix_get_hist_data', 'code', 'date', 'ktype', unique=True),
    )

    # qfq
    get_h_data = Table('get_h_data', metadata,
        Column('id', Integer(), primary_key=True),
        Column('date', DateTime(), nullable = False),
        Column('open',Numeric(12, 4)),
        Column('high', Numeric(12, 4)),
        Column('close', Numeric(12, 4)),
        Column('low', Numeric(12, 4)),
        Column('volume', Numeric(20, 4)),
        Column('amount', Numeric(20, 4)),
        Column('price_change', Numeric(12, 4)),
        Column('p_change', Numeric(12, 4)),
        Column('ma5', Numeric(12, 4)),
        Column('ma10', Numeric(12, 4)),
        Column('ma20', Numeric(12, 4)),
        Column('v_ma5', Numeric(20, 4)),
        Column('v_ma10', Numeric(20, 4)),
        Column('v_ma20', Numeric(20, 4)),
        Column('diff', Numeric(12, 4)),
        Column('dea', Numeric(12, 4)),
        Column('macd', Numeric(12, 4)),
        Column('code', String(6)),
        Column('ktype', String(6), default='D'), # K线周期
        Column('type', String(6)),  # 当前K线与后K线形成up还是down关系
        Column('delete', Boolean()),  # 当前K线与后K线形成up还是down关系
        Column('fenxing', String(6)), # 顶ding和底di标识
        Column('fx_weight', Numeric(12, 4)), # 分型权重
        Column('bi_to_be', Numeric(12, 4)), # 可能的笔节点的值
        Column('bi_value', Numeric(12, 4)), # 确定的笔节点的值
        Column('duan_value', Numeric(12, 4)), # 段节点的值
        Column('operate', String(6)),
        Index('ix_get_hist_data', 'code', 'date', 'ktype', unique=True),
    )

    # 业绩报告（主表）
    get_report_data = Table('get_report_data', metadata,
        Column('code', String(6), index=True), # 代码
        Column('name', String(50), index=True), # 股票名称
        Column('esp', Numeric(12, 4)), # 每股收益
        Column('esp_yoy', Numeric(12, 4)), # 每股收益同比(%)
        Column('bvps', Numeric(12, 4)), # 每股净资产
        Column('roe', Numeric(12, 4)), # 净资产收益率(%)
        Column('epcf', Numeric(12, 4)), # 每股现金流量(元)
        Column('net_profits', Numeric(12, 4)), # 净利润(万元)
        Column('profits_yoy', Numeric(12, 4)), # 净利润同比(%)
        Column('distrib', Text()), # 分配方案
        Column('report_date', Date( )), # 公布日期
        Column('year', Integer(), primary_key=True),
        Column('quarter', Integer(), primary_key=True),
        Column('created_on', Date(), default = datetime.now), # 获取时间
        Index('ix_report_data', 'code', 'year', 'quarter', unique=True),
    )

    # 分配预案
    profit_data = Table('profit_data', metadata,
        Column('code', String(6), index=True), # 代码
        Column('name', String(50), index=True), # 股票名称
        Column('year', Integer()), # 分配年份
        Column('report_date', Date( )), # 公布日期
        Column('divi', Numeric(12, 4)), # 分红金额（每10股）
        Column('shares', Numeric(12, 4)), # 转增和送股数（每10股）
        Column('created_on', Date(), default = datetime.now), # 获取时间
        Index('ix_profit_data', 'code', 'report_date', unique=True),
    )

    # 业绩预告
    forecast_data = Table('forecast_data', metadata,
        Column('code', String(6), index=True), # 代码
        Column('name', String(50), index=True), # 股票名称
        Column('type', String(6)),  # 业绩变动类型【预增、预亏等】
        Column('report_date', Date( )), # 公布日期
        Column('pre_eps', Numeric(12, 4)), # 上年同期每股收益
        Column('range', Numeric(12, 4)), # 业绩变动范围
        Column('created_on', Date(), default = datetime.now), # 获取时间
        Index('ix_forecast_data', 'code', 'report_date', unique=True),
    )

    # 限售股解禁
    xsg_data = Table('xsg_data', metadata,
        Column('code', String(6), index=True), # 代码
        Column('name', String(50), index=True), # 股票名称
        Column('date', Date()), # 解禁日期
        Column('count', Integer()), # 解禁数量（万股）
        Column('ratio', Numeric(12, 4)), # 占总盘比率
        Column('created_on', Date(), default = datetime.now), # 获取时间
        Index('ix_xsg_data', 'code', 'date', 'count', unique=True),
    )

    # 基金持股
    fund_holdings = Table('fund_holdings', metadata,
        Column('code', String(6), index=True), # 代码
        Column('name', String(50), index=True), # 股票名称
        Column('date', Date()), # 报告日期
        Column('nums', Integer()), # 基金家数
        Column('nlast', Integer()), # 与上期相比（增加或减少了）
        Column('count', Integer()), # 基金持股数（万股）
        Column('clast', Integer()), # 与上期相比
        Column('amount', Numeric(12, 4)), # 基金持股市值
        Column('ratio', Numeric(12, 4)), # 占流通盘比率
        Column('created_on', Date(), default = datetime.now), # 获取时间
        Index('ix_fund_holdings', 'code', 'date', unique=True),
    )

    # 新股数据
    new_stocks = Table('new_stocks', metadata,
        Column('code', String(6), index=True), # 代码
        Column('name', String(50), index=True), # 股票名称
        Column('ipo_date', Date()), # 上网发行日期
        Column('issue_date', Date(), index=True), # 上市日期
        Column('amount', Numeric(12, 4)), # 上网发行数量(万股)
        Column('price', Numeric(12, 4)), # 发行价格(元)
        Column('pe', Numeric(12, 4)), # 发行市盈率
        Column('limit', Numeric(12, 4)), # 个人申购上限(万股)
        Column('funds', Numeric(12, 4)), # 募集资金(亿元)
        Column('ballot', Numeric(12, 4)), # 网上中签率(%)
        Column('created_on', Date(), default = datetime.now), # 获取时间
        Index('ix_new_stocks', 'code', 'issue_date', unique=True),
    )

    def db_init(self, conn_string = None):
        self.engine = create_engine(conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

dal = DataAccessLayer()

if __name__=='__main__':
    dal = DataAccessLayer()




