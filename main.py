import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 파일 업로드 또는 경로 지정
file1 = "202504_202504_연령별인구현황_월간_남녀구분.csv"
file2 = "202504_202504_연령별인구현황_남녀합계.csv"

# 데이터 불러오기
df_nm = pd.read_csv(file1, encoding='utf-8')
df_total = pd.read_csv(file2, encoding='utf-8')

st.title("연령별 인구현황 시각화")

# 데이터 컬럼명 미리보기
st.subheader("데이터 미리보기")
st.write("남/녀 구분 데이터")
st.dataframe(df_nm.head())
st.write("남녀 합계 데이터")
st.dataframe(df_total.head())

# 시각화 1: 연령대별 남녀 인구 비교 (막대그래프)
st.subheader("연령대별 남녀 인구 비교")
age_col = "연령"
male_col = "남자"
female_col = "여자"

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_nm[age_col],
    y=df_nm[male_col],
    name='남자',
    orientation='v'
))
fig.add_trace(go.Bar(
    x=df_nm[age_col],
    y=df_nm[female_col],
    name='여자',
    orientation='v'
))

fig.update_layout(
    barmode='group',
    xaxis_title='연령',
    yaxis_title='인구수',
    title='연령별 남녀 인구수'
)
st.plotly_chart(fig)

# 시각화 2: 인구 피라미드 (남/녀)
st.subheader("인구 피라미드 (남/녀)")
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    y=df_nm[age_col],
    x=-df_nm[male_col],  # 남성: 왼쪽(음수)
    name='남자',
    orientation='h'
))
fig2.add_trace(go.Bar(
    y=df_nm[age_col],
    x=df_nm[female_col],  # 여성: 오른쪽(양수)
    name='여자',
    orientation='h'
))

fig2.update_layout(
    barmode='relative',
    xaxis=dict(title='인구수'),
    yaxis=dict(title='연령'),
    title='연령별 인구 피라미드',
)
st.plotly_chart(fig2)

# 시각화 3: 연령별 전체 인구 (선그래프)
st.subheader("연령별 전체 인구(합계)")
if "합계" in df_total.columns:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_total[age_col],
        y=df_total["합계"],
        mode='lines+markers',
        name='합계'
    ))
    fig3.update_layout(
        xaxis_title='연령',
        yaxis_title='인구수',
        title='연령별 전체 인구수(합계)'
    )
    st.plotly_chart(fig3)
else:
    st.write("합계 컬럼이 없습니다.")

st.markdown("---")
st.info("CSV 파일 컬럼명이 다를 경우 코드에서 컬럼명을 맞춰주세요!")
