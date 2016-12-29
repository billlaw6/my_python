#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: analyse_data.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Wed 21 Dec 2016 10:13:27 PM CST

import os
import logging
import logging.config
import json
import datetime
import time

import pandas as pd
import matplotlib.dates as mdates
from sqlalchemy import select, update

import czsc
from db_core import dal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# handler = logging.FileHandler('hello.log')
# handler.setFormatter(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

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


def update_czsc_data(code=None, ktype='5'):
    """ 从本地数据库取K线数据作缠论分析并将结果写回数据库 """
    sql = """select * from get_hist_data
        where code = '%s' and ktype = '%s'""" % (code, ktype)
    data = pd.read_sql(sql, dal.engine)
    if len(data) == 0:
        logging.error("No data selected")
        raise
    data.set_index(keys='date', drop=False, inplace=True)
    if len(str(data.index[0])) == 10:
        dates = [datetime.datetime(*time.strptime(str(i), '%Y-%m-%d')[:6]) for i in data.index]
    else:
        dates = [datetime.datetime(*time.strptime(str(i), '%Y-%m-%d %H:%M:%S')[:6]) for i in data.index]
    data['t'] = mdates.date2num(dates)
    data = czsc.tag_bi_line(data)
    czsc.plot_data2(data, single=True)

if __name__ == '__main__':
    update_czsc_data('sh', '5')
