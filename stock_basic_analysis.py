#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_basic_analysis.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Mon 21 Nov 2016 10:19:41 AM CST

import tushare as ts
import matplotlib.pyplot as plt


def turnoverratio_ana():
    df = ts.get_today_all()
    pos = df[df.changepercent > 0].turnoverratio
    neg = df[df.changepercent < 0].turnoverratio

    fig, axes = plt.subplots(2, 1, sharex=True)

    pos.plot(ax = axes[0], kind='hist', bins=10)
    neg.plot(ax = axes[1], kind='hist', bins=10)
    plt.show()


    stage1 = df[(df.changepercent > -10) & (df.changepercent < -5)].turnoverratio
    stage2 = df[(df.changepercent > -5) & (df.changepercent < 0)].turnoverratio
    stage3 = df[(df.changepercent > 0) & (df.changepercent < 5)].turnoverratio
    stage4 = df[(df.changepercent > 5) & (df.changepercent < 10)].turnoverratio

    fig, axes = plt.subplots(4, 1, sharex=True)

    stage1.plot(ax = axes[0], kind='hist', bins=10)
    axes[0].set_ylabel = 'stage0'
    stage2.plot(ax = axes[1], kind='hist', bins=10)
    axes[1].set_ylabel = 'stage1'
    stage3.plot(ax = axes[2], kind='hist', bins=10)
    axes[2].set_ylabel = 'stage2'
    stage4.plot(ax = axes[3], kind='hist', bins=10)
    axes[3].set_ylabel = 'stage3'
    plt.show()

# turnoverratio between 2.7 ~ 6 

def main():
    turnoverratio_ana()

if __name__ == '__main__':
    main()
