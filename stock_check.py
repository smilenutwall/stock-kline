import streamlit as st
import pandas as pd
import numpy as np
import akshare as ak
from pyecharts import options as opts
from pyecharts.charts import Kline,Line,Bar,Grid
import macd as ma
from streamlit_echarts import st_pyecharts


@st.cache_data
def load_stock_overview():
    return pd.read_excel('股票代码总览.xlsx')

st.title('股票数据查询')
st.set_page_config(layout="wide")
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
stock_total_code=load_stock_overview()

st.write('输入股票代码')
stock_code = st.text_input("请输入要查询的6位股票代码：", value='600519',max_chars=6)
if st.button('查看'):
    for code in stock_total_code['代码']:
        if stock_code[-6:]==code[-6:]:
            stock_code=code
            break
    stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")
    stock_data = pd.DataFrame(stock_zh_a_daily_qfq_df)
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    total_count = len(stock_data)
    start_percent = max(0, round((total_count - 40) / total_count * 100, 2)) if total_count > 0 else 0

    #'k线图+均线和布林线'
    #'MA'
    stock_data['MA5']=ma.MA_price(stock_data,5)
    stock_data['MA10']=ma.MA_price(stock_data,10)
    stock_data['MA30']=ma.MA_price(stock_data,30)
    stock_data['MA60']=ma.MA_price(stock_data,60)
    stock_data['MA120']=ma.MA_price(stock_data,120)

    #'布林线'

    stock_data['bull_middle'],stock_data['bull_upper'],stock_data['bull_lower']=ma.bull(stock_data,20)

    #'k线'
    kline_data = []
    for index, row in stock_data.iterrows():
        kline_data.append([row['open'], row['close'], row['low'], row['high']])


    kline_price = (
        Kline(init_opts=opts.InitOpts(
                page_title="%s K线图" % stock_code))
        .add_xaxis(xaxis_data=stock_data['date'].dt.strftime('%Y-%m-%d').tolist())
        .add_yaxis(series_name="Kline",
                   y_axis=kline_data,)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                        title="%s K线及指标图" % stock_code,
                        pos_left="center",
                        pos_top="0.5%"),
            xaxis_opts=opts.AxisOpts(
                name='日期',
                name_location="end",
                is_scale=True),
            yaxis_opts=opts.AxisOpts(
                name='股价/（元）',
                is_scale=True),
            legend_opts=opts.LegendOpts(
                is_show=True,
                type_='scroll',
                pos_top="3.5%",
                pos_left="center",
                orient="horizontal",
                selected_mode="multiple",
                selected_map={
                    "Kline": True,
                    "MA5": True,
                    "MA10": True,
                    "MA30": True,
                    "MA60": False,
                    "MA120": False,
                    "bull_middle": False,
                    "bull_upper": False,
                    "bull_lower": False}),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=True,
                    type_="slider",
                    xaxis_index=[0, 1, 2],
                    pos_bottom="1%",
                    range_start=start_percent,
                    range_end=100,
                    is_show_detail=False),
                opts.DataZoomOpts(
                    type_="inside",
                    xaxis_index=[0, 1, 2])],
            toolbox_opts=opts.ToolboxOpts(
                item_size=22,
                feature={
                    "dataZoom": {"yAxisIndex": "none","title": {"zoom": "区域缩放", "back": "缩放还原"}},
                    "restore": {"title": "重置"},
                    "saveAsImage": {"title": "保存图片"},}),
            tooltip_opts=opts.TooltipOpts(
                        trigger="axis"
                    ),
        )
    )


    line_price = (
        Line()
        .add_xaxis(xaxis_data=stock_data['date'].dt.strftime('%Y-%m-%d').tolist())
        .add_yaxis(series_name='MA5',
                   y_axis=stock_data['MA5'].round(2).tolist(),
                   is_smooth=True,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="white"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="white",width=1))
        .add_yaxis(series_name='MA10',
                   y_axis=stock_data['MA10'].round(2).tolist(),
                   is_smooth=True,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="yellow"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="yellow",width=1))
        .add_yaxis(series_name='MA30',
                   y_axis=stock_data['MA30'].round(2).tolist(),
                   is_smooth=True,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="purple"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="purple",width=1))
        .add_yaxis(series_name='MA60',
                   y_axis=stock_data['MA60'].round(2).tolist(),
                   is_smooth=True,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="green"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="green",width=1))
        .add_yaxis(series_name='MA120',
                   y_axis=stock_data['MA120'].round(2).tolist(),
                   is_smooth=True,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="grey"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="grey",width=1))
        .add_yaxis(series_name='bull_middle',
                   y_axis=stock_data['bull_middle'].round(2).tolist(),
                   is_smooth=True,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="white"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="white",width=1))
        .add_yaxis(series_name='bull_upper',
                   y_axis=stock_data['bull_upper'].round(2).tolist(),
                   is_smooth=True,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="yellow"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="yellow",width=1))
        .add_yaxis(series_name='bull_lower',
                   y_axis=stock_data['bull_lower'].round(2).tolist(),
                   is_smooth=True,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="purple"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="purple",width=1))
    )
    chart_kline = kline_price.overlap(line_price)
    st.success('k线图已绘制完成')

    #'成交量'
    #'成交量柱状图'
    vol_bar_data=[]
    for i,row in stock_data.iterrows():
        if row['open']<=row['close']:
            vol_color='#ef232a'
        else:
            vol_color='#00FFFF'
        vol_bar_data.append(
            opts.BarItem(
                name="",
                value=row['volume'],
                itemstyle_opts=opts.ItemStyleOpts(color=vol_color)))

    bar_vol = (
        Bar()
        .add_xaxis(xaxis_data=stock_data['date'].dt.strftime('%Y-%m-%d').tolist())
        .add_yaxis(series_name="volume", y_axis=vol_bar_data, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_scale=True, axislabel_opts=opts.LabelOpts(is_show=False)),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="volume", name_gap=15, split_number=3),
        )
    )

    #'成交量均线'
    MAV5=ma.MA_volume(stock_data,5)
    MAV10=ma.MA_volume(stock_data,10)

    line_vol=(
        Line()
        .add_xaxis(xaxis_data=stock_data['date'].dt.strftime('%Y-%m-%d').tolist())
        .add_yaxis("vol_MA5", MAV5,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="white"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="white",width=1))
        .add_yaxis("vol_MA10", MAV10,
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="yellow"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="yellow",width=1))
    )
    chart_vol = bar_vol.overlap(line_vol)
    st.success('成交量图已绘制完成')

    #'MACD'
    stock_macd=ma.MACD_DEA(stock_data,'close')
    stock_macd = stock_macd.iloc[::-1]
    stock_macd = stock_macd.reset_index(drop=True)
    macd_data=stock_macd['macd_dif']-stock_macd['macd_dea']
    macd_bar_data=[]
    for i,row in stock_macd.iterrows():
        if row['macd_dif']>=row['macd_dea']:
            macd_color='#ef232a'
        else:
            macd_color='#00FFFF'
        macd_bar_data.append(
            opts.BarItem(
                name="",
                value=round(macd_data.iloc[i], 3),
                itemstyle_opts=opts.ItemStyleOpts(color=macd_color)))

    bar_macd = (
        Bar()
        .add_xaxis(xaxis_data=stock_data['date'].dt.strftime('%Y-%m-%d').tolist())
        .add_yaxis(series_name="MACD柱", y_axis=macd_bar_data, label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_scale=True, name="日期", name_location="end", name_gap=10),
            yaxis_opts=opts.AxisOpts(is_scale=True, name="MACD", name_gap=15, split_number=3),
        )
    )

    line_macd = (
        Line()
        .add_xaxis(xaxis_data=stock_data['date'].dt.strftime('%Y-%m-%d').tolist())
        .add_yaxis("快线", stock_macd['macd_dif'].round(3).tolist(),
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="white"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="white",width=1))
        .add_yaxis("慢线", stock_macd['macd_dea'].round(3).tolist(),
                   symbol_size=0.5,
                   itemstyle_opts=opts.ItemStyleOpts(color="yellow"),
                   z=3,
                   label_opts=opts.LabelOpts(is_show=False),
                   linestyle_opts=opts.LineStyleOpts(color="yellow",width=1))
    )
    chart_macd = bar_macd.overlap(line_macd)
    st.success('macd图已绘制完成')

    #'联合图表'
    grid_chart = Grid(
        init_opts=opts.InitOpts(
            page_title="%s 股票数据可视化" % stock_code
        )
    )

    grid_chart.add(chart_kline, grid_opts=opts.GridOpts(pos_left="7%", pos_right="5%", pos_top="10%", height="40%"))
    grid_chart.add(chart_vol, grid_opts=opts.GridOpts(pos_left="7%", pos_right="5%", pos_top="55%", height="17%"))
    grid_chart.add(chart_macd, grid_opts=opts.GridOpts(pos_left="7%", pos_right="5%", pos_top="76%", height="17%"))

    st_pyecharts(grid_chart, height="1000px")

    st.success('已全部绘制完成')