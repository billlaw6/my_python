#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: test_app.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 19 Dec 2016 09:38:43 PM CST

import unittest

from db import dal

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dal.db_init('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')


