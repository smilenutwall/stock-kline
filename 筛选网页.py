import streamlit as st
import pandas as pd
import numpy as np
import akshare as ak
from pyecharts import options as opts
from pyecharts.charts import Kline,Line,Bar,Grid
import macd as ma
from streamlit_echarts import st_pyecharts
import sys

@st.cache_data
def load_stock_overview():
    return pd.read_excel('股票代码总览.xlsx')
stock_overview = load_stock_overview()

st.title('潜力股票筛选')
st.subheader("上传你的Excel文件")
uploaded_file = st.file_uploader('仅xlsx文件,将股票列名改为‘code’或‘代码’',type=["xlsx"])
if uploaded_file is not None:
    total_stock=pd.read_excel(uploaded_file)
    if 'code' in total_stock.columns:
        total_stock_code=total_stock['code'].dropna()
    elif '代码' in total_stock.columns:
        total_stock_code=total_stock['代码'].dropna()
    else:
        print('文件不符合要求')
        sys.exit()
else:
    print('请上传文件')
    sys.exit()

stock_overview['num_code']=stock_overview['代码'].astype(str).str.extract(r'(\d{6})')
code_map = dict(zip(stock_overview['num_code'], stock_overview['代码']))

total_stock_code = total_stock_code.map(code_map).dropna()





for stock_code in total_stock_code:
    stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")
    if stock_zh_a_daily_qfq_df is None or stock_zh_a_daily_qfq_df.empty:
        continue
    stock_data = pd.DataFrame(stock_zh_a_daily_qfq_df)
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    stock_data['bull_middle'], stock_data['bull_upper'], stock_data['bull_lower'] = ma.bull(stock_data, 20)
    #st.success('%s筛选中'%stock_code)
    if stock_data.iloc[-1]['close']<=stock_data.iloc[-1]['bull_middle'] :
        if ma.price_inc(stock_data)==1:
            st.success('%s符合要求'%stock_code)
        #change=ma.MACD_change(stock_data_inc,'close')
        #if change>=5:
            #st.success('%s符合要求'%stock_code)

st.success('已全部筛选完')



