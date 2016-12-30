#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_localize_data.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Tue 21 Dec 2016 07:16:55 PM CST

import os
import time
import datetime
import logging
import logging.config
import json

import tushare as ts
import pandas as pd
from sqlalchemy.exc import IntegrityError
# from sqlalchemy.types import CHAR

from db_core import dal # Data Access Layer
# 确定数据库表存在（不解决表结构变化问题) 
dal.db_init()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# handler = logging.FileHandler('hello.log')
# handler.setFormatter(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


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
        df['date'] = time.strftime('%Y-%m-%d', time.localtime())
        # df.to_sql('get_index', dal.engine, if_exists='append', index=False, dtype={'code': CHAR(6)})
        df.to_sql('get_index', dal.engine, if_exists='append', index=False)
    except IntegrityError as e:
        logging.error("IntegrityError ")
    except Exception as e:
        logging.error("Exception caught in basic_data")
        raise e

    try:
        df = ts.get_stock_basics()
        df['date'] = time.strftime('%Y-%m-%d', time.localtime())
        df.to_sql('get_stock_basics', dal.engine, if_exists='append', index=True)
    except IntegrityError as e:
        logging.error("IntegrityError %s")
    except Exception as e:
        logging.error("Exception caught in basic_data")
        raise e

    try:
        df = ts.get_today_all()
        df['date'] = time.strftime('%Y-%m-%d', time.localtime())
        df.to_sql('get_today_all', dal.engine, if_exists='append', index=False)
    except IntegrityError as e:
        logging.error("IntegrityError %s")
    except Exception as e:
        logging.error("Exception caught in basic_data")
        raise e
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


def h_data(code_list):
    """利用tushare获取数据并存到本地数据库 """
    for code in code_list:
        sql = """select max(date) as max_date from get_h_data
                where code = '%s'""" % (code)
        result = pd.read_sql_query(sql, dal.engine)
        # pandas Timestamp
        max_date_ts = result.ix[0, 0]
        if (max_date_ts is not None and max_date_ts != 'None'):
            max_date = datetime.datetime.strftime(max_date_ts.to_pydatetime(), '%Y-%m-%d')
            if max_date != time.strftime('%Y-%m-%d', time.localtime()):
                print(max_date)
                print(time.strftime('%Y-%m-%d', time.localtime()))
                df = ts.get_h_data(code)
                df['code'] = code
                df['ktype'] = 'D'
                logging.info("getting h data of %s" % (code))
                try:
                    df.to_sql('get_h_data', dal.engine, if_exists='append', index=True)
                    logging.info("h data of %s localized" % (code))
                except IntegrityError as e:
                    logging.error("IntegrityError in h_data")
                except Exception as e:
                    logging.error("Exception caught in h_data %s" % e)
                    raise e
        else:
            df = ts.get_h_data(code)
            df['code'] = code
            df['ktype'] = 'D'
            logging.info("getting h data of %s" % (code))
            try:
                df.to_sql('get_h_data', dal.engine, if_exists='append', index=True)
                logging.info("h data of %s localized" % (code))
            except IntegrityError as e:
                logging.error("IntegrityError in h_data")
            except Exception as e:
                logging.error("Exception caught in h_data %s" % e)
                raise e


def hist_data(code_list):
    """利用tushare获取数据并存到本地数据库 """
    for code in code_list:
        for ktype in ['5', '30']:
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
            else:
                hist_data = ts.get_hist_data(code = code, ktype=ktype)
            
            hist_data['code'] = code
            hist_data['ktype'] = ktype
        try:
            logging.info("getting h data of %s" % (code))
            hist_data.to_sql('get_hist_data', dal.engine, if_exists='append', index=True)
        except IntegrityError as e:
            logging.error("IntegrityError")
        except Exception as e:
            logging.error("Exception caught in hist_data %s" % e)
            raise e

if __name__ == '__main__':
    basic_data()
    h_data(['002695'])
    hist_data(['002695'])

