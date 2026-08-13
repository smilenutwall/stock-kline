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

# '股价上涨'
# def price_inc(data,period,ma_period,ma_inc_times,ma_above_times):
#     if len(data) < period+1:
#         return False
#     ma = MA_price(data,ma_period)
#     ma_inc = ma > ma.shift(1)
#     recent_ma_inc = ma_inc.tail(period)
#     ma_inc_days = recent_ma_inc.sum()
#     if ma_inc_days < ma_inc_times:
#         return False
#     recent_close = data['close'].tail(period)
#     recent_ma = ma.tail(period)
#     days_above_ma = (recent_close > recent_ma).sum()
#     return bool(days_above_ma >= ma_above_times)

'股价上涨及均线偏离限制(最多超过c天)'
def price_inc(data, period, ma_period, ma_inc_times):
    if len(data) < period + 1:
        return False
    ma = MA_price(data, ma_period)
    ma_inc = ma > ma.shift(1)
    recent_ma_inc = ma_inc.tail(period)
    if recent_ma_inc.sum() < ma_inc_times:
        return False
    return True




'股票偏离20日均线标准差'
def std_ma20(data,period):
    if len(data) < period+1:
        return 100000
    data['ma20']=MA_price(data,20)
    bias=(data['close']-data['ma20'])/data['ma20']
    std = bias.tail(period).std()
    return std

'atr变化'
    # def atr(data,period,atr,times):
    #     high_low=data['high']-data['low']
    #     high_close_pre=abs(data['high']-data['close'].shift(1))
    #     low_close_pre=abs(data['low']-data['close'].shift(1))
    #     data['atr']=max(high_low,high_close_pre,low_close_pre)
    #     data['atr_10']=data['atr'].rolling(10).mean()
    #     data['atr_10']=data['atr'].tail(period)
    #     atr/=100
    #     judge=data['atr_10']>atr
    #     if judge>=times:
    #         return False
    #     else:
    #         return True


def atr(data, period=20, atr_pct_limit=5.0, times=3):
    high_low = data['high'] - data['low']
    high_close_pre = (data['high'] - data['close'].shift(1)).abs()
    low_close_pre = (data['low'] - data['close'].shift(1)).abs()
    tr = np.maximum(high_low, np.maximum(high_close_pre, low_close_pre))
    atr = tr.rolling(10).mean()
    atr_pct = (atr / data['close'].shift(1)) * 100
    exceed_days = (atr_pct.tail(period) > atr_pct_limit).sum()
    if exceed_days >= times:
        return False
    return True


