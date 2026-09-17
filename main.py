import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    
    # URL에서 직접 텍스트를 받아와 StringIO로 전달
    response = requests.get(url)
    response.raise_for_status()
    csv_data = io.StringIO(response.text)
    
    df = pd.read_csv(csv_data)
    
    # genre 열 전처리: '|' 기호로 연결된 장르 중 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    # total_audi 수치형 변환
    df['total_audi'] = df['total_audi'].astype(str).str.replace(',', '')
    df['total_audi'] = pd.to_numeric(df['total_audi'], errors='coerce').fillna(0)
    
    return df

df = load_data()

st.divider()

# 1. 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수")

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig1 = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 편수 비율"
)

fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 특정 장르(예: 드라마, 애니메이션 등)가 박스오피스 상위권 영화 중 가장 큰 비중을 차지하고 있음을 확인할 수 있습니다.")

st.divider()

# 2. 장르 및 영화별 총 관객 수 (트리맵)
st.subheader("2. 장르 및 영화별 총 관객 수 분포")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    title="장르 내 영화별 총 관객 수 트리맵"
)

fig2.update_traces(
    hovertemplate="<b>구분:</b> %{label}<br><b>총 관객 수:</b> %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 각 장르 내에서 어떤 영화가 총 관객 수의 대부분을 차지하며 흥행을 주도했는지 한눈에 비교해 볼 수 있습니다.")

st.divider()

# 3. 총 관객 수 분포 (히스토그램)
st.subheader("3. 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x='total_audi',
    hover_data=['movieNm'],
    title="영화별 총 관객 수 분포 (히스토그램)",
    labels={'total_audi': '총 관객 수(명)'}
)

fig3.update_traces(
    hovertemplate="<b>관객 수 구간:</b> %{x}<br><b>영화 수:</b> %{y}편<extra></extra>"
)

fig3.update_layout(
    yaxis_title="영화 수 (편)"
)

st.plotly_chart(fig3, use_container_width=True)

# 최다 관객 영화 정보 자동 추출
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = int(top_movie['total_audi'])

st.info(f"💡 **이 그래프로 알 수 있는 것:** 대다수의 영화는 하위 관객 수 구간(왼쪽 구간)에 분포하여 집중되어 있으며, 일부 대형 흥행작만이 오른쪽에 외딴 위치로 분포합니다. 이 중 가장 많은 관객을 모은 영화는 **'{top_movie_name}'** (약 {top_movie_audi:,}명)입니다.")

st.divider()
