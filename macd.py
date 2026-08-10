import pandas as pd
import numpy as np

'''12日EXPMA计算'''
def EXPMA_12(data,type):   #data数据需要从旧往新的
    data['expma_12']=data[type].ewm(span=12,adjust=False).mean()
    return data

'''26日EXPMA计算'''
def EXPMA_26(data,type):
    data['expma_26']=data[type].ewm(span=26,adjust=False).mean()
    return data

'''MACD快线计算'''
def MACD_DIF(data,type):
    expma_12=EXPMA_12(data,type)
    expma_26=EXPMA_26(expma_12,type)
    expma_26['macd_dif']=expma_26['expma_12']-expma_26['expma_26']
    return expma_26

'''MACD慢线计算'''
def MACD_DEA(data,type):
    data=MACD_DIF(data,type)
    data['macd_dea']=data['macd_dif'].ewm(span=9,adjust=False).mean()
    return data

'布林线'
def bull(data,period):#第一行是最旧数据
    bull_middle = data['close'].rolling(window=period).mean()
    std = data['close'].rolling(window=period).std()
    bull_upper=bull_middle+2*std
    bull_lower=bull_middle-2*std
    return bull_middle, bull_upper, bull_lower

'价格均线'
def MA_price(data,period):
    ma_list=data['close'].rolling(window=period).mean()
    return ma_list

'成交量均线'
def MA_volume(data,period):
    ma_list = data['volume'].rolling(window=period).mean()
    return ma_list

'macd变化筛选'
def MACD_change(data,type):
    data=MACD_DEA(data,type)
    last_idx=len(data)-1
    today_change=(data.loc[last_idx,'macd_dif']-data.loc[last_idx-1,'macd_dif'])/data.loc[last_idx,'close']
    yesterday_change=(data.loc[last_idx-1,'macd_dif']-data.loc[last_idx-2,'macd_dif'])/data.loc[last_idx-1,'close']
    change=1000*(today_change-yesterday_change)
    return change

'股价上涨'
def price_inc(data):
    recent_5_days_inc = (data['close'].diff() > 0).tail(5)
    if recent_5_days_inc.sum() >= 4:
        return 1
    else:
        return 0