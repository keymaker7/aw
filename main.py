import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("연령별 인구현황 시각화")

# 1. 파일 업로드
st.write("두 개의 CSV 파일(남녀구분, 남녀합계)을 차례로 업로드 해주세요.")
file_nm = st.file_uploader("남녀 구분 데이터 업로드", type="csv")
file_total = st.file_uploader("남녀 합계 데이터 업로드", type="csv")

if file_nm is not None and file_total is not None:
    # 2. 데이터 읽기
    df_nm = pd.read_csv(file_nm, encoding='utf-8')
    df_total = pd.read_csv(file_total, encoding='utf-8')

    # 3. 데이터 미리보기
    st.subheader("데이터 미리보기")
    st.write("남/녀 구분 데이터")
    st.dataframe(df_nm.head())
    st.write("남녀 합계 데이터")
    st.dataframe(df_total.head())

    # 4. 시각화
    st.subheader("연령대별 남녀 인구 비교")
    age_col = "연령"
    male_col = "남자"
    female_col = "여자"

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_nm[age_col],
        y=df_nm[male_col],
        name='남자'
    ))
    fig.add_trace(go.Bar(
        x=df_nm[age_col],
        y=df_nm[female_col],
        name='여자'
    ))

    fig.update_layout(
        barmode='group',
        xaxis_title='연령',
        yaxis_title='인구수',
        title='연령별 남녀 인구수'
    )
    st.plotly_chart(fig)

    st.subheader("인구 피라미드 (남/녀)")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        y=df_nm[age_col],
        x=-df_nm[male_col],
        name='남자',
        orientation='h'
    ))
    fig2.add_trace(go.Bar(
        y=df_nm[age_col],
        x=df_nm[female_col],
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
else:
    st.info("먼저 두 개의 CSV 파일을 모두 업로드 해주세요.")

st.markdown("---")
st.info("CSV 파일 컬럼명이 다를 경우 코드에서 컬럼명을 맞춰주세요!")
