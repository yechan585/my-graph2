import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열 전처리: '|' 기호로 연결된 장르 중 첫 번째 장르만 extraction
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

df = load_data()

st.divider()

# 1. 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 편수 비율"
)

# 마우스 호버 시 편수와 비율 표기
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 분석 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 특정 장르(예: 드라마, 애니메이션 등)가 박스오피스 상위권 영화 중 가장 큰 비중을 차지하고 있음을 확인할 수 있습니다.")

st.divider()
