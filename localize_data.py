#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: localize_data.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Tue 21 Dec 2016 07:16:55 PM CST

import datetime
import os
import logging
import logging.config
import json

import pandas as pd
import tushare as ts
from sqlalchemy.exc import IntegrityError

from db_core import dal # Data Access Layer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# handler = logging.FileHandler('hello.log')
# handler.setFormatter(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# 确定数据库表存在（不解决表结构变化问题) 
dal.db_init('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')

def setup_logging(
    default_path="logging.json",
    default_level=logging.INFO,
    env_key="LOG_CFG"
):
    """ Setup logging configuration """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def basic_data():
    """利用tushare获取股票基本面数据存到本地数据库 """
    try:
        df = ts.get_index()
        df.to_sql('get_index', dal.engine, if_exists='append', index=False)
        df = ts.get_stock_basics()
        df.to_sql('get_stock_basics', dal.engine, if_exists='append', index=True)
        df = ts.get_today_all()
        df.to_sql('get_today_all', dal.engine, if_exists='append', index=False)
        # df = ts.get_report_data()
        # df.to_sql('get_report_data', dal.engine, if_exists='append', index=True)
        # df = ts.profit_data()
        # df.to_sql('profit_data', dal.engine, if_exists='append', index=True)
        # df = ts.forecast_data()
        # df.to_sql('forecast_data', dal.engine, if_exists='append', index=True)
        # df = ts.xsg_data()
        # df.to_sql('xsg_data', dal.engine, if_exists='append', index=True)
        # df = ts.fund_holdings()
        # df.to_sql('fund_holdings', dal.engine, if_exists='append', index=True)
        # df = ts.new_stocks()
        # df.to_sql('new_stocks', dal.engine, if_exists='append', index=True)

        logging.info("basic_data localized")
    except IntegrityError as e:
        logging.error("IntegrityError %s" % e)
    except Exception as e:
        logging.error("Exception caught in basic_data")
        raise e


def k_data(code=None, ktypes=['5', '30', 'D', 'W']):
    """利用tushare获取数据并存到本地数据库 """
    code = code or 'sh'
    for ktype in ktypes:
        sql = """select max(date) as max_date from get_hist_data
                where code = '%s'
                and ktype= '%s'""" % (code, ktype)
        result = pd.read_sql_query(sql, dal.engine)
        # pandas Timestamp
        max_date_ts = result.ix[0, 0]
        if (max_date_ts is not None and max_date_ts != 'None'):
            max_date = max_date_ts.to_pydatetime()
            delta = datetime.timedelta(seconds=1)
            start_date = str(max_date + delta)
            hist_data = ts.get_hist_data(code = code, start=start_date, ktype=ktype)
            logging.info("getting hist data %s %s from %s" % (code, ktype, start_date))
        else:
            hist_data = ts.get_hist_data(code = code, ktype=ktype)
            logging.info("getting hist data %s %s from begin" % (code, ktype))
        hist_data['code'] = code
        hist_data['ktype'] = ktype
        try:
            hist_data.to_sql('get_hist_data', dal.engine, if_exists='append', index=True)
            logging.info("hist data of %s %s localized" % (code, ktype))
        except IntegrityError as e:
            logging.error("IntegrityError %s" % e)
        except Exception as e:
            logging.error("Exception caught in k_data")
            raise e

if __name__ == '__main__':
    basic_data()
    k_data()
