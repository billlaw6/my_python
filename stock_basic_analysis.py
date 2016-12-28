#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_basic_analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 21 Nov 2016 10:19:41 AM CST
import time

import pandas as pd
import matplotlib.pyplot as plt

from db_core import dal
dal.db_init()

def today_all_ana():
    """ """
    sql = """select * from get_today_all where date='%s'""" % time.strftime('%Y-%m-%d', time.localtime())
    df = pd.read_sql(sql, dal.engine)
    pos = df[(df.changepercent > 0) & (df.turnoverratio < 4)].turnoverratio
    neg = df[(df.changepercent < 0) & (df.turnoverratio < 4)].turnoverratio

    fig, axes = plt.subplots(2, 1, sharex=True)

    pos.plot(ax = axes[0], kind='hist', bins=100)
    neg.plot(ax = axes[1], kind='hist', bins=100)
    plt.show()

    stage1 = df[(df.changepercent > -10) & (df.changepercent < -5) & (df.turnoverratio < 4)].turnoverratio
    stage2 = df[(df.changepercent > -5) & (df.changepercent < 0) & (df.turnoverratio < 4)].turnoverratio
    stage3 = df[(df.changepercent > 0) & (df.changepercent < 5) & (df.turnoverratio < 4)].turnoverratio
    stage4 = df[(df.changepercent > 5) & (df.changepercent < 10) & (df.turnoverratio < 4)].turnoverratio

    fig, axes = plt.subplots(4, 1, sharex=True)
    stage1.plot(ax = axes[0], kind='hist', bins=100)
    axes[0].set_ylabel = 'stage0'
    stage2.plot(ax = axes[1], kind='hist', bins=100)
    axes[1].set_ylabel = 'stage1'
    stage3.plot(ax = axes[2], kind='hist', bins=100)
    axes[2].set_ylabel = 'stage2'
    stage4.plot(ax = axes[3], kind='hist', bins=100)
    axes[3].set_ylabel = 'stage3'
    plt.show()
# turnoverratio between 1.7 ~ 4 

    pos = df[(df.changepercent > 0) & (df.per < 4)].per
    neg = df[(df.changepercent < 0) & (df.per < 4)].per

    fig, axes = plt.subplots(2, 1, sharex=True)

    pos.plot(ax = axes[0], kind='hist', bins=100)
    neg.plot(ax = axes[1], kind='hist', bins=100)
    plt.show()

    stage1 = df[(df.changepercent > -10) & (df.changepercent < -5) & (df.per < 4)].per
    stage2 = df[(df.changepercent > -5) & (df.changepercent < 0) & (df.per < 4)].per
    stage3 = df[(df.changepercent > 0) & (df.changepercent < 5) & (df.per < 4)].per
    stage4 = df[(df.changepercent > 5) & (df.changepercent < 10) & (df.per < 4)].per

    fig, axes = plt.subplots(4, 1, sharex=True)
    stage1.plot(ax = axes[0], kind='hist', bins=100)
    axes[0].set_ylabel = 'stage0'
    stage2.plot(ax = axes[1], kind='hist', bins=100)
    axes[1].set_ylabel = 'stage1'
    stage3.plot(ax = axes[2], kind='hist', bins=100)
    axes[2].set_ylabel = 'stage2'
    stage4.plot(ax = axes[3], kind='hist', bins=100)
    axes[3].set_ylabel = 'stage3'
    plt.show()
# per between 

    pos = df[(df.changepercent > 0) & (df.pb < 4)].pb
    neg = df[(df.changepercent < 0) & (df.pb < 4)].pb

    fig, axes = plt.subplots(2, 1, sharex=True)

    pos.plot(ax = axes[0], kind='hist', bins=100)
    neg.plot(ax = axes[1], kind='hist', bins=100)
    plt.show()

    stage1 = df[(df.changepercent > -10) & (df.changepercent < -5) & (df.pb < 4)].pb
    stage2 = df[(df.changepercent > -5) & (df.changepercent < 0) & (df.pb < 4)].pb
    stage3 = df[(df.changepercent > 0) & (df.changepercent < 5) & (df.pb < 4)].pb
    stage4 = df[(df.changepercent > 5) & (df.changepercent < 10) & (df.pb < 4)].pb

    fig, axes = plt.subplots(4, 1, sharex=True)
    stage1.plot(ax = axes[0], kind='hist', bins=100)
    axes[0].set_ylabel = 'stage0'
    stage2.plot(ax = axes[1], kind='hist', bins=100)
    axes[1].set_ylabel = 'stage1'
    stage3.plot(ax = axes[2], kind='hist', bins=100)
    axes[2].set_ylabel = 'stage2'
    stage4.plot(ax = axes[3], kind='hist', bins=100)
    axes[3].set_ylabel = 'stage3'
    plt.show()
# per between 

    pos = df[(df.changepercent > 0) & (df.mktcap < 4)].mktcap
    neg = df[(df.changepercent < 0) & (df.mktcap < 4)].mktcap

    fig, axes = plt.subplots(2, 1, sharex=True)

    pos.plot(ax = axes[0], kind='hist', bins=100)
    neg.plot(ax = axes[1], kind='hist', bins=100)
    plt.show()

    stage1 = df[(df.changepercent > -10) & (df.changepercent < -5) & (df.mktcap < 4)].mktcap
    stage2 = df[(df.changepercent > -5) & (df.changepercent < 0) & (df.mktcap < 4)].mktcap
    stage3 = df[(df.changepercent > 0) & (df.changepercent < 5) & (df.mktcap < 4)].mktcap
    stage4 = df[(df.changepercent > 5) & (df.changepercent < 10) & (df.mktcap < 4)].mktcap

    fig, axes = plt.subplots(4, 1, sharex=True)
    stage1.plot(ax = axes[0], kind='hist', bins=100)
    axes[0].set_ylabel = 'stage0'
    stage2.plot(ax = axes[1], kind='hist', bins=100)
    axes[1].set_ylabel = 'stage1'
    stage3.plot(ax = axes[2], kind='hist', bins=100)
    axes[2].set_ylabel = 'stage2'
    stage4.plot(ax = axes[3], kind='hist', bins=100)
    axes[3].set_ylabel = 'stage3'
    plt.show()
# per between 

def today_all_box():
    """ """
    sql = """select a.*,b.changepercent,b.turnoverratio,b.per
        from get_stock_basics a,get_today_all b
        where a.code=b.code
        and a.date=b.date
        and b.date='%s'""" % time.strftime('%Y-%m-%d', time.localtime())
    df = pd.read_sql(sql, dal.engine)

    # # aim = df[(df.changepercent > 2)].turnoverratio
    # # total = df.turnoverratio
    # aim = df[(df.changepercent > 2) & (df.turnoverratio < 10)].turnoverratio
    # total = df[(df.turnoverratio < 10)].turnoverratio

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # turnoverratio between 1.2 ~ 4 

    # # aim = df[(df.changepercent > 2)].per
    # # total = df.per
    # aim = df[(df.changepercent > 2) & (df.per > 0) & (df.per < 130)].per
    # total = df[(df.per > 0) & (df.per < 130)].per

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# per between 35 ~ 65 

    # aim = df[(df.changepercent > 2)].pb
    # total = df.pb
    aim = df[(df.changepercent > 2) & (df.pb > 0) & (df.pb < 130)].pb
    total = df[(df.pb > 0) & (df.pb < 130)].pb

    fig, axes = plt.subplots(1, 2, sharey=True)

    total.plot(ax = axes[0], kind='box')
    aim.plot(ax = axes[1], kind='box')
    plt.show()
# pb between 3 ~ 8 

    # # aim = df[(df.changepercent > 2)].pe
    # # total = df.pe
    # aim = df[(df.changepercent > 2) & (df.pe > 0) & (df.pe < 130)].pe
    # total = df[(df.pe > 0) & (df.pe < 130)].pe

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # pe between 30 ~ 85 

    # # aim = df[(df.changepercent > 2)].outstanding
    # # total = df.outstanding
    # aim = df[(df.changepercent > 2) & (df.outstanding < 50)].outstanding
    # total = df[(df.outstanding < 50)].outstanding

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # outstanding between 0.8 ~ 5 

    # # aim = df[(df.changepercent > 2)].totals
    # # total = df.totals
    # aim = df[(df.changepercent > 2) & (df.totals < 50)].totals
    # total = df[(df.totals < 50)].totals

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # totals between 1.4 ~ 7.1 

    # # aim = df[(df.changepercent > 2)].totalAssets
    # # total = df.totalAssets
    # aim = df[(df.changepercent > 2) & (df.totalAssets < 5e+6)].totalAssets
    # total = df[(df.totalAssets < 5e+6)].totalAssets

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # totalAssets between 80000 ~ 1000000

    # # aim = df[(df.changepercent > 2)].liquidAssets
    # # total = df.liquidAssets
    # aim = df[(df.changepercent > 2) & (df.liquidAssets < 5e+6)].liquidAssets
    # total = df[(df.liquidAssets < 5e+6)].liquidAssets

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # liquidAssets between 13000 ~ 200000

    # aim = df[(df.changepercent > 2)].esp
    # total = df.esp
    aim = df[(df.changepercent > 2) & (df.esp < 5e+6)].esp
    total = df[(df.esp < 5e+6)].esp

    fig, axes = plt.subplots(1, 2, sharey=True)

    total.plot(ax = axes[0], kind='box')
    aim.plot(ax = axes[1], kind='box')
    plt.show()
# esp between 1.2 ~ 5

    # # aim = df[(df.changepercent > 2)].bvps
    # # total = df.bvps
    # aim = df[(df.changepercent > 2) & (df.bvps < 5e+6)].bvps
    # total = df[(df.bvps < 5e+6)].bvps

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # bvps between 1.2 ~ 5

    # # aim = df[(df.changepercent > 2)].perundp
    # # total = df.perundp
    # aim = df[(df.changepercent > 2) & (df.perundp > -0.03) & (df.perundp < 3)].perundp
    # total = df[(df.perundp < 3) & (df.perundp > -0.03)].perundp

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # perundp between -0.03 ~ 1.3

    # # aim = df[(df.changepercent > 2)].profit
    # # total = df.profit
    # aim = df[(df.changepercent > 2) & (df.profit > -100) & (df.profit < 100)].profit
    # total = df[(df.profit < 100) & (df.profit > -100)].profit

    # fig, axes = plt.subplots(1, 2, sharey=True)

    # total.plot(ax = axes[0], kind='box')
    # aim.plot(ax = axes[1], kind='box')
    # plt.show()
# # profit between -20 ~ 20

def main():
    today_all_box()

if __name__ == '__main__':
    main()
