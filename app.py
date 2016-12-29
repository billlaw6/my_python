#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: app.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 19 Dec 2016 09:10:17 PM CST
import os
from urllib.error import URLError
import logging
import logging.config
import json

import stock_select as ss
import stock_localize_data as sld
from stock import Stock

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

stock_list = ss.basic_select()
ls = os.linesep
with open('./selected.EBK', 'w') as f:
    for stock in stock_list:
        f.write(stock + ls)

try:
    sld.basic_data()
    sld.h_data(stock_list)
    sld.hist_data(stock_list)
except URLError as e:
    logging.error("No internet access, check it!")

#rs = []
#for code in len(stock_list):
    #s = Stock(code)
    #s.add_czsc_data(s.get_hist_data())
    #rs.append(s)










