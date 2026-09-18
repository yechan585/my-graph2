import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열 전처리: 세로막대 기호(|)로 분리 후 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

df = load_data()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 비율")

# 장르별 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# 도넛 그래프 생성
fig_donut = px.pie(
    genre_counts,
    values='count',
    names='genre',
    hole=0.4,
    title="장르별 영화 분포"
)

# 마우스오버 시 편수(value)와 비율(percent) 및 장르명(label) 표시
fig_donut.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig_donut, use_container_width=True)

# 구분선 및 알 수 있는 것 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("박스오피스 상위권 영화 중 특정 주요 장르가 차지하는 비중과 장르별 다변화 정도를 한눈에 파악할 수 있습니다.")

st.write("") # 공간 여백

# -------------------------------------------------------------------
# 두 번째 그래프: 장르-영화 계층별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객 수 분포")

# 트리맵 그래프 생성 (계층 구조: genre -> movieNm, 크기: total_audi)
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), 'genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 총 관객 수 (Treemap)",
    color='genre'
)

# 마우스오버 시 영화명(label)과 총 관객 수(value) 표시
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig_treemap, use_container_width=True)

# 구분선 및 알 수 있는 것 구역
st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("장르 전체의 관객 수 규모와 함께, 각 장르 내에서 어떤 영화가 총 관객 수를 주도했는지 개별 영화의 기여도를 직관적으로 비교할 수 있습니다.")
