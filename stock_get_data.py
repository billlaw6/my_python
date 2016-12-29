#!/usr/bin/env python
# -*- coding: utf8 -*-
# File Name: stock_get_data.py
# Author: bill_law6
# mail: bill_law6@163.com
# Created Time: Tue 08 Nov 2016 10:00:09 AM CST
# Get stock data regularly

import h5py
import tushare as ts # 0.4.3 version
import datetime
import sqlalchemy
from sqlalchemy import create_engine
import sqlite3

var_names = locals()
today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
engine = create_engine('mysql+pymysql://root:654321@127.0.0.1/stocks?charset=utf8')
con = sqlite3.connect(u'./stocks.db3')

def get_basic_data(year_s=2015, year_e=2017, season_s=1, season_e=5):
    # Basics data
    stocks = ts.get_stock_basics()
    stocks.to_sql('stock_basics', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
    stocks.to_sql('stock_basics', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    # fun_names = ['report', 'profit', 'operation', 'growth', 'debtpaying', 'cashflow']
    fun_names = ['cashflow']
    for fun_name in fun_names:
        for y in range(year_s, year_e):
            for s in range(season_s, season_e):
                print('executing ts.get_%s_data(%s, %s)' % (fun_name, y, s))
                var_names['%s_%s_%s' % (fun_name, y, s)] = eval("ts.get_%s_data(%s, %s)" % (fun_name, y, s))
                if var_names['%s_%s_%s' % (fun_name, y, s)] is not None:
                    var_name = 'basics_%s_%s_%s' % (fun_name, y, s)
                    print('\n%s' % var_name)
                    var_names['%s_%s_%s' % (fun_name, y, s)].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
                    var_names['%s_%s_%s' % (fun_name, y, s)].to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

def get_classified_data():
    # classified data
    # fun_names = ['industry', 'concept', 'area', 'sme', 'gem', 'st']
    fun_names = ['concept']
    for fun_name in fun_names:
        print('executing ts.get_%s_classified( )' % (fun_name))
        var_names['%s' % (fun_name)] = eval("ts.get_%s_classified( )" % (fun_name))
        if var_names['%s' % (fun_name)] is not None:
            var_name = 'classified_%s' % (fun_name)
            print('%s' % var_name)
            var_names['%s' % (fun_name)].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
            var_names['%s' % (fun_name)].to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})
    hs300s = ts.get_hs300s()
    if hs300s is not None:
        hs300s.to_sql('classified_hs300s', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        hs300s.to_sql('classified_hs300s', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})


    sz50s = ts.get_sz50s()
    if sz50s is not None:
        sz50s.to_sql('classified_sz50s', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        sz50s.to_sql('classified_sz50s', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})


    zz500s = ts.get_zz500s()
    if zz500s is not None:
        zz500s.to_sql('classified_zz500s', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        zz500s.to_sql('classified_zz500s', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})


    terminated = ts.get_terminated()
    if terminated is not None:
        terminated.to_sql('classified_terminated', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        terminated.to_sql('classified_terminated', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})


    suspended = ts.get_suspended()
    if suspended is not None:
        suspended.to_sql('classified_suspended', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        suspended.to_sql('classified_suspended', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})



def get_invent_reference_data():
    profit_data = ts.profit_data(year=2016, top=50)
    if profit_data is not None:
        profit_data.to_sql('invent_reference_profit_data', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        profit_data.to_sql('invent_reference_profit_data', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    fun_name = 'forecast_data'
    for y in range(2014, 2016):
        for s in range(1, 5):
            print('executing ts.%s(%s, %s)' % (fun_name, y, s))
            var_names['%s_%s_%s' % (fun_name, y, s)] = eval("ts.%s(%s, %s)" % (fun_name, y, s))
            if (var_names['%s_%s_%s' % (fun_name, y, s)] is not None) and len(var_names['%s_%s_%s' % (fun_name, y, s)])>0:
                var_name = 'invent_reference_%s_%s_%s' % (fun_name, y, s)
                print('\n%s' % var_name)
                var_names['%s_%s_%s' % (fun_name, y, s)].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
                var_names['%s_%s_%s' % (fun_name, y, s)].to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    fun_name = 'xsg_data'
    for y in range(2014, 2018):
        for m in range(1, 13):
            print('executing ts.%s(%s, %s)' % (fun_name, y, m))
            var_names['%s_%s_%s' % (fun_name, y, m)] = eval("ts.%s(%s, %s)" % (fun_name, y, m))
            if var_names['%s_%s_%s' % (fun_name, y, m)] is not None:
                var_name = 'invent_reference_%s_%s_%s' % (fun_name, y, m)
                print('\n%s' % var_name)
                var_names['%s_%s_%s' % (fun_name, y, m)].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
                var_names['%s_%s_%s' % (fun_name, y, m)].to_sql(var_name, con, if_exists='replace', index=True, index_label='index', dtype={'code': 'CHAR'})

    fun_name = 'fund_holdings'
    for y in range(2014, 2016):
        for s in range(1, 5):
            print('executing ts.%s(%s, %s)' % (fun_name, y, s))
            var_names['%s_%s_%s' % (fun_name, y, s)] = eval("ts.%s(%s, %s)" % (fun_name, y, s))
            if var_names['%s_%s_%s' % (fun_name, y, s)] is not None:
                var_name = 'invent_reference_%s_%s_%s' % (fun_name, y, s)
                print('\n%s' % var_name)
                var_names['%s_%s_%s' % (fun_name, y, s)].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
                var_names['%s_%s_%s' % (fun_name, y, s)].to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    new_stocks = ts.new_stocks( )
    if new_stocks is not None:
        new_stocks.to_sql('invent_reference_new_stocks', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        new_stocks.to_sql('invent_reference_new_stocks', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    sh_margins = ts.sh_margins( )
    if sh_margins is not None:
        sh_margins.to_sql('invent_reference_sh_margins', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        sh_margins.to_sql('invent_reference_sh_margins', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    sh_margin_details = ts.sh_margin_details( )
    if sh_margin_details is not None:
        sh_margin_details.to_sql('invent_reference_sh_margins_detail', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        sh_margin_details.to_sql('invent_reference_sh_margins_detail', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    sz_margins = ts.sz_margins( )
    if sz_margins is not None:
        sz_margins.to_sql('invent_reference_sz_margins', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        sz_margins.to_sql('invent_reference_sz_margins', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    sz_margin_details = ts.sz_margin_details( )
    if sz_margin_details is not None:
        sz_margin_details.to_sql('invent_reference_sz_margin_details', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        sz_margin_details.to_sql('invent_reference_sz_margin_details', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

def get_longhubang_data():
    today_str = today.replace('-','_')
    var_names['top_list_%s' % today_str] = ts.top_list(today)
    var_name = 'longhubang_top_list_%s' % today_str
    if (var_names['top_list_%s' % today_str] is not None) and len(var_names['top_list_%s' % today_str]) > 0 :
        var_names['top_list_%s' % today_str].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        var_names['top_list_%s' % today_str].to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    cap_tops = ts.cap_tops(days = 5)
    if cap_tops is not None:
        var_name = 'longhubang_cap_tops_%s' % today_str
        cap_tops.to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        cap_tops.to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    broker_tops = ts.broker_tops(days = 5)
    if broker_tops is not None:
        var_name = 'longhubang_broker_tops_%s' % today_str
        broker_tops.to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        broker_tops.to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    inst_tops = ts.inst_tops(days = 5)
    if inst_tops is not None:
        var_name = 'longhubang_inst_tops_%s' % today_str
        inst_tops.to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        inst_tops.to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    inst_detail = ts.inst_detail( )
    if inst_detail is not None:
        var_name = 'longhubang_inst_detail_%s' % today_str
        inst_detail.to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        inst_detail.to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

def get_macro_economy_data():
    deposit_rate = ts.get_deposit_rate()
    if deposit_rate is not None:
        deposit_rate.to_sql('macro_deposit_rate', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        deposit_rate.to_sql('macro_deposit_rate', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    loan_rate = ts.get_loan_rate()
    if loan_rate is not None:
        loan_rate.to_sql('macro_loan_rate', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        loan_rate.to_sql('macro_loan_rate', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    rrr = ts.get_rrr()
    if rrr is not None:
        rrr.to_sql('macro_rrr', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        rrr.to_sql('macro_rrr', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    money_supply = ts.get_money_supply()
    if money_supply is not None:
        money_supply.to_sql('macro_money_supply', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        money_supply.to_sql('macro_money_supply', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    money_supply_bal = ts.get_money_supply_bal()
    if money_supply_bal is not None:
        money_supply_bal.to_sql('macro_money_supply_bal', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        money_supply_bal.to_sql('macro_money_supply_bal', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    gdp_year = ts.get_gdp_year()
    if gdp_year is not None:
        gdp_year.to_sql('macro_gdp_year', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        gdp_year.to_sql('macro_gdp_year', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    gdp_quarter = ts.get_gdp_quarter()
    if gdp_quarter is not None:
        gdp_quarter.to_sql('macro_gdp_quarter', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        gdp_quarter.to_sql('macro_gdp_quarter', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    gdp_for = ts.get_gdp_for()
    if gdp_for is not None:
        gdp_for.to_sql('macro_gdp_for', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        gdp_for.to_sql('macro_gdp_for', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    gdp_pull = ts.get_gdp_pull()
    if gdp_pull is not None:
        gdp_pull.to_sql('macro_gdp_pull', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        gdp_pull.to_sql('macro_gdp_pull', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    gdp_contrib = ts.get_gdp_contrib()
    if gdp_contrib is not None:
        gdp_contrib.to_sql('macro_gdp_contrib', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        gdp_contrib.to_sql('macro_gdp_contrib', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    cpi = ts.get_cpi()
    if cpi is not None:
        cpi.to_sql('macro_cpi', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        cpi.to_sql('macro_cpi', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

    ppi = ts.get_ppi()
    if ppi is not None:
        ppi.to_sql('macro_ppi', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
        ppi.to_sql('macro_ppi', con, if_exists='replace', index=True, dtype={'code': 'CHAR'})

def get_trade_data(stocks=None):
    stock_list = []
    if stocks is None:
        stocks = ts.get_stock_basics()
    for stock in stocks.index:
        stock_list.append("'"+stock+"'")
    stock_list.append("'sh'")
    stock_list.append("'sz'")
    stock_list.append("'hs300'")
    stock_list.append("'sz50'")
    stock_list.append("'zxb'")
    stock_list.append("'cyb'")
    print("stock_list %s" % stock_list)
    for stock in stock_list:
        print("executing ts.get_hist_data(%s)" % (stock))
        # Day
        var_names['hist_d_%s' % stock] = eval("ts.get_hist_data(%s)" % stock)
        if var_names['hist_d_%s' % stock] is not None:
            var_name = 'trade_data_hist_d_%s' % stock.replace("'",'')
            print('\n%s' % var_name)
            var_names['hist_d_%s' % stock].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
            var_names['hist_d_%s' % stock].to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})
        # Week
        var_names['hist_w_%s' % stock] = eval("ts.get_hist_data(%s, ktype='W')" % stock)
        if var_names['hist_w_%s' % stock] is not None:
            var_name = 'trade_data_hist_w_%s' % stock.replace("'",'')
            print('\n%s' % var_name)
            var_names['hist_w_%s' % stock].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
            var_names['hist_w_%s' % stock].to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})
        # Month
        var_names['hist_m_%s' % stock] = eval("ts.get_hist_data(%s, ktype='M')" % stock)
        if var_names['hist_m_%s' % stock] is not None:
            var_name = 'trade_data_hist_m_%s' % stock.replace("'",'')
            print('\n%s' % var_name)
            var_names['hist_m_%s' % stock].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
            var_names['hist_m_%s' % stock].to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})
        # 5min
        var_names['hist_5m_%s' % stock] = eval("ts.get_hist_data(%s, ktype='5')" % stock)
        if var_names['hist_5m_%s' % stock] is not None:
            var_name = 'trade_data_hist_5m_%s' % stock.replace("'",'')
            print('\n%s' % var_name)
            var_names['hist_5m_%s' % stock].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
            var_names['hist_5m_%s' % stock].to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})
        # 15min
        var_names['hist_15m_%s' % stock] = eval("ts.get_hist_data(%s, ktype='15')" % stock)
        if var_names['hist_15m_%s' % stock] is not None:
            var_name = 'trade_data_hist_15m_%s' % stock.replace("'",'')
            print('\n%s' % var_name)
            var_names['hist_15m_%s' % stock].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
            var_names['hist_15m_%s' % stock].to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})
        # 30min
        var_names['hist_30m_%s' % stock] = eval("ts.get_hist_data(%s, ktype='30')" % stock)
        if var_names['hist_30m_%s' % stock] is not None:
            var_name = 'trade_data_hist_30m_%s' % stock.replace("'",'')
            print('\n%s' % var_name)
            var_names['hist_30m_%s' % stock].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
            var_names['hist_30m_%s' % stock].to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})
        # 60min
        var_names['hist_60m_%s' % stock] = eval("ts.get_hist_data(%s, ktype='60')" % stock)
        if var_names['hist_60m_%s' % stock] is not None:
            var_name = 'trade_data_hist_60m_%s' % stock.replace("'",'')
            print('\n%s' % var_name)
            var_names['hist_60m_%s' % stock].to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
            var_names['hist_60m_%s' % stock].to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})

    today_all = ts.get_today_all()
    if today_all is not None:
        var_name = 'trade_data_%s' % today.replace('-','')
        today_all.to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
        today_all.to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})

    for stock in stock_list:
        tick_data = ts.get_tick_data(stock, today)
        if tick_data is not None:
            var_name = 'trade_data_%s' % today.replace('-','')
            tick_data.to_sql(var_name, engine, if_exists='replace', index=True, dtype={'date': sqlalchemy.types.CHAR(20)})
            tick_data.to_sql(var_name, con, if_exists='replace', index=True, dtype={'date': 'CHAR'})

    # for stock in stock_list:
        # realtime_quotes = ts.get_realtime_quotes(stock)
        # if realtime_quotes is not None:
            # var_name = 'trade_data_%s' % today.replace('-','')
            # realtime_quotes.to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
            # realtime_quotes.to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
    # realtime_quotes = ts.get_realtime_quotes(stock_list)
    # realtime_quotes = ts.get_realtime_quotes(['002780','sh','sz','hs300'])

    # for stock in stock_list:
        # today_ticks = ts.get_today_ticks(stock)
        # if today_ticks is not None:
            # var_name = 'trade_data_%s' % today.replace('-','')
            # today_ticks.to_sql(var_name, engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
            # today_ticks.to_sql(var_name, con, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})

    # df = ts.get_index()
    # df = ts.get_sina_dd('600848', date='2015-12-24')
    # ts.get_latest_news(top=5,show_content=True)


def analysis_hdf5_data():
    # Analysis 
    with h5py.File('./stock_data.hdf5', 'r') as f:
        # list all members
        members = []
        f.visit(members.append)
        print(members)
        # d = f['basics']
        # print(d)


def main():
    get_basic_data(2015, 2017)
    get_classified_data()
    get_invent_reference_data()
    get_longhubang_data()
    get_macro_economy_data()
    stocks = ts.get_stock_basics()
    get_trade_data(stocks[stocks.index=='002790'])
    # analysis_hdf5_data()


if __name__ == '__main__':
    main()

# stocks.to_sql('stock_basics', con, if_exists='replace',  index=True, # dtype={'code': 'CHAR'})
# stocks.to_sql('stock_basics', engine, if_exists='replace', index=True, dtype={'code': sqlalchemy.types.CHAR(6)})
