import pandas as pd
import numpy as np

# df_data=pd.read_excel('C:/Users/27288/Desktop/股票/历史数据/sh688816.xlsx')
# '''12日线收盘价'''
# n=12
# df_high_data=df_data.loc[:,['交易日期','收盘价']]
# expma_list_12=[]
# for i in range(len(df_high_data)-1,-1,-1):
#     if i==len(df_high_data)-1:
#         expma=df_high_data.loc[i,'收盘价']
#     else:
#         expma=(df_high_data.loc[i,'收盘价']*2+expma_list_12[103-i]['EXPMA']*(n-1))/(n+1)
#     expma_list_12.append({'交易日':df_high_data.loc[i,'交易日期'],'EXPMA':expma})
# df_expma_12=pd.DataFrame(expma_list_12)
# print(df_expma_12)
#
# '''26日线收盘价'''
# n=26
# expma_list_26=[]
# for i in range(len(df_high_data)-1,-1,-1):
#     if i==len(df_high_data)-1:
#         expma=df_high_data.loc[i,'收盘价']
#     else:
#         expma=(df_high_data.loc[i,'收盘价']*2+expma_list_26[103-i]['EXPMA']*(n-1))/(n+1)
#     expma_list_26.append({'交易日':df_high_data.loc[i,'交易日期'],'EXPMA':expma})
# df_expma_26=pd.DataFrame(expma_list_26)
# print(df_expma_26)
#
# '''MACD快线收盘价'''
# df_dif=df_expma_12-df_expma_26
# print(df_dif)
# df_dif.rename(columns={'EXPMA':'MACD'}, inplace=True)
# dif_change=1000*((df_dif.loc[0,'MACD']-df_dif.loc[1,'MACD'])/df_high_data.loc[0,'MACD']-(df_dif.loc[1,'MACD']-df_dif.loc[2,'MACD'])/df_high_data.loc[1,'MACD'])
# if dif_change>=5:
#     print(1)

'''12日EXPMA计算'''
def EXPMA_12(data,code,type):
    data=data.loc[:,['date',type]]
    expma_list_12 = []
    n=12
    last_idx = len(data)
    if last_idx >=3:
        for i in range(len(data) - 1, -1, -1):
            if i == len(data) - 1:
                expma = data.loc[i, type]
            else:
                expma = (data.loc[i, type] * 2 + expma_list_12[last_idx-2 - i]['EXPMA_12'] * (n - 1)) / (n + 1)
            expma_list_12.append({'date': data.loc[i, 'date'], 'EXPMA_12': expma})
        df_expma_12 = pd.DataFrame(expma_list_12)
        return df_expma_12
    else:
        return None

'''26日EXPMA计算'''
def EXPMA_26(data,code,type):
    data=data.loc[:,['date',type]]
    expma_list_26 = []
    n=26
    last_idx = len(data)
    if last_idx >=3:
        for i in range(len(data) - 1, -1, -1):
            if i == len(data) - 1:
                expma = data.loc[i, type]
            else:
                expma = (data.loc[i, type] * 2 + expma_list_26[last_idx-2 - i]['EXPMA_26'] * (n - 1)) / (n + 1)
            expma_list_26.append({'date': data.loc[i, 'date'], 'EXPMA_26': expma})
        df_expma_26 = pd.DataFrame(expma_list_26)
        return df_expma_26
    else:
        return None

'''MACD快线计算'''
def MACD_DIF(data,code,type):
    expma_12=EXPMA_12(data,code,type)
    expma_26=EXPMA_26(data,code,type)
    if expma_12 is None or expma_26 is None:
        return None
    else:
        df = pd.merge(expma_12, expma_26, on='date', how='inner')
        df['MACD_dif'] = df['EXPMA_12'] - df['EXPMA_26']
        return df

'''MACD慢线计算'''
def MACD_DEA(data,code,type):
    df_dif=MACD_DIF(data,code,type)
    if df_dif is None:
        return None
    else:
        dea_list = []
        last_idx = len(df_dif)
        for i in range(len(df_dif) - 1, -1, -1):
            if i == len(df_dif) - 1:
                macd = df_dif.loc[i, 'MACD_dif']
            else:
                macd = df_dif.loc[i, 'MACD_dif'] * 0.2 + dea_list[last_idx - 2 - i]['MACD_dea'] * 0.8
            dea_list.append({'date': df_dif.loc[i, 'date'], 'MACD_dea': macd})
        df_dea = pd.DataFrame(dea_list)
        return df_dea


