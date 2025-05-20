import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

# 글로벌 시가총액 Top10 (2024년 기준) 티커 리스트
# Apple, Microsoft, Saudi Aramco, Alphabet, Amazon, Nvidia, Berkshire Hathaway, Meta, Eli Lilly, TSMC
TICKERS = [
    ("Apple", "AAPL"),
    ("Microsoft", "MSFT"),
    ("Saudi Aramco", "2222.SR"),
    ("Alphabet (Google)", "GOOGL"),
    ("Amazon", "AMZN"),
    ("Nvidia", "NVDA"),
    ("Berkshire Hathaway", "BRK-B"),
    ("Meta (Facebook)", "META"),
    ("Eli Lilly", "LLY"),
    ("TSMC", "TSM"),
]

st.title("🌏 글로벌 시가총액 Top10 기업의 최근 1년간 주가 변화")
st.write("야후 파이낸스 데이터를 활용하여 시각화합니다.")

# 최근 1년 구간
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# 데이터 수집
data = {}
for name, ticker in TICKERS:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        if not hist.empty:
            data[name] = hist['Close']
    except Exception as e:
        st.warning(f"{name}({ticker}) 데이터 로딩 실패: {e}")

# Plotly 시각화
fig = go.Figure()

for name, series in data.items():
    fig.add_trace(go.Scatter(x=series.index, y=series.values, mode='lines', name=name))

fig.update_layout(
    title="글로벌 시가총액 Top10 기업 주가 변화(최근 1년)",
    xaxis_title="날짜",
    yaxis_title="종가(USD)",
    legend_title="기업명",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
