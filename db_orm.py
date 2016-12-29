#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: db_orm.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Tue 20 Dec 2016 09:32:04 AM CST


from sqlalchemy import create_engine, Table, Column, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cookie(Base):
	__tablename__ = 'cookies'

	cookie_id = Column(Integer(), primary_key=True)
	cookie_name = Column(String(50), index=True)
	cookie_recipe_url = Column(String(255))
	open = Column(String(55))
	quantity = Column(Integer())
	unit_cost = Column(Numeric(12, 2))

engine = create_engine('sqlite:////:memory:')
Base.metadata.create_all(engine)


