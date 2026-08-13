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

st.markdown(
    """
    <style>
    /* 修改主内容区域背景 */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* 修改侧边栏背景 */
    section[data-testid="stSidebar"] {
        background-color: #262730;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('潜力股票筛选')

st.sidebar.header("筛选条件设置")
"收盘价低于等于布林线上轨（暂不使用）"
use_bull = st.sidebar.checkbox("收盘价低于等于布林线上轨", value=False)
if use_bull:
    bull_period=st.number_input('请输入布林线周期：',value=20)
"a日内b次均线MAc上涨"
use_inc = st.sidebar.checkbox("a日内b次均线MAc上涨", value=False)
if use_inc:
    price_inc_length=st.number_input('请输入判断周期时间a：',value=30)
    ma_inc_times=st.number_input('请输入均线上涨的次数b：:',value=20)
    ma_period=st.number_input('请输入均线周期c：',value=10)
"macd大幅上涨（暂不使用）"
use_macd = st.sidebar.checkbox("macd大幅上涨", value=False)
if use_macd:
    macd_change=st.number_input('请输入macd变化的幅度：',value=5,step=0.1)
'股价偏离20日均线(暂不使用)'
use_ma20=st.sidebar.checkbox("股票偏离MA20的标准差", value=False)
if use_ma20:
    ma20_period=st.number_input('计算标准差的周期',value=120)
    ma20_std = st.number_input('请输入偏离MA20的标准差：', value=0.1,step=0.01)
'a日atr振幅超过b%的次数小于c次'
use_atr=st.sidebar.checkbox('a日atr振幅超过b%的次数小于c次', value=False)
if use_atr:
    atr_period=st.number_input('请输入筛选时间a',value=60)
    atr=st.number_input('请输入振幅大小b:',value=6.0,step=0.1)
    atr_times=st.number_input('超过b的最大次数c：',value=10)


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
        st.stop()
else:
    print('请上传文件')
    st.stop()

stock_overview['num_code']=stock_overview['代码'].astype(str).str.extract(r'(\d{6})')
code_map = dict(zip(stock_overview['num_code'], stock_overview['代码']))
total_stock_code = total_stock_code.astype(str).str.extract(r'(\d+)')[0].str.zfill(6)
total_stock_code = total_stock_code.map(code_map).dropna()


if st.button("开始筛选"):
    result=[]
    k=0
    for stock_code in total_stock_code:
        k+=1
        if k%100==0:
            st.write('已筛选%s次，当前股票为：%s'%(k,stock_code))
        stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")
        if stock_zh_a_daily_qfq_df is None or stock_zh_a_daily_qfq_df.empty:
            continue
        stock_data = pd.DataFrame(stock_zh_a_daily_qfq_df)
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        bull_judge=inc_judge=macd_judge=True
        if use_bull:
            stock_data['bull_middle'], stock_data['bull_upper'], stock_data['bull_lower'] = ma.bull(stock_data, bull_period)
            bull_judge=stock_data.iloc[-1]['close']<=stock_data.iloc[-1]['bull_upper']
            if not bull_judge:
                continue
        if use_inc:
            inc_judge=ma.price_inc(stock_data,price_inc_length,ma_period,ma_inc_times)
            if not inc_judge:
                continue
        if use_macd:
            macd_judge=ma.MACD_change(stock_data,'close')>=macd_change
            if not macd_judge:
                continue
        if use_ma20:
            ma20_judge=ma.std_ma20(stock_data,ma20_period)
            if ma20_judge > ma20_std:
                continue
        if use_atr:
            atr_judge=ma.atr(stock_data,atr_period,atr,atr_times)
            if not atr_judge:
                continue
        st.success('%s符合筛选条件'%(stock_code))
        result.append({'代码':stock_code})
    result=pd.DataFrame(result)
    result.to_excel('%s筛选结果.xlsx'%uploaded_file.name)


    st.success('已全部筛选完')



