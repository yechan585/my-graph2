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
    
    # 수치형 변환 (쉼표 제거 및 숫자 파싱)
    num_cols = ['total_audi', 'first_scrn', 'first_week_audi']
    for col in num_cols:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
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

# Plotly 트리맵 생성 (계층 구조: 전체 -> 장르 -> 영화명)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    title="장르 내 영화별 총 관객 수 트리맵"
)

# 마우스 호버 시 영화명과 총 관객 수가 표기되도록 설정
fig2.update_traces(
    hovertemplate="<b>영화명:</b> %{label}<br><b>총 관객 수:</b> %{value:,}명<extra></extra>"
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

# 4. 개봉일 스크린수와 총 관객수의 관계 (산점도)
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객수 산점도",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객수(명)',
        'genre': '장르'
    }
)

fig4.update_traces(
    hovertemplate="<b>영화명:</b> %{hovertext}<br><b>개봉일 스크린수:</b> %{x:,}개<br><b>총 관객수:</b> %{y:,}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 대체로 개봉일 스크린수가 많을수록 총 관객수도 증가하는 양의 상관관계를 보이지만, 스크린수에 비해 유독 높은 관객수를 기록한 흥행 대박 작품이나 그 반대의 케이스도 존재함을 확인할 수 있습니다.")

st.divider()

# 5. 주요 장르별 총 관객 수 상자 그림 (박스플롯)
st.subheader("5. 주요 장르별 총 관객 수 상자 그림")

# 영화가 10편 이상인 장르만 필터링
genre_counts_series = df['genre'].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df['genre'].isin(top_genres)]

fig5 = px.box(
    df_filtered,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="영화 수 10편 이상 장르별 총 관객 수 분포 (박스플롯)",
    labels={
        'genre': '장르',
        'total_audi': '총 관객수(명)'
    }
)

fig5.update_traces(
    hovertemplate="<b>영화명:</b> %{hovertext}<br><b>총 관객수:</b> %{y:,}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중간값과 분포 범위를 비교할 수 있으며, 상자 밖의 점(이상치)을 통해 장르 평균을 훨씬 뛰어넘는 대형 흥행작들을 한눈에 확인할 수 있습니다.")

st.divider()

# 6. 스크린수, 총 관객수, 첫 주 관객수의 관계 (버블 차트)
st.subheader("6. 개봉일 스크린수·총 관객수·첫 주 관객수의 관계 (버블 차트)")

fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=50,
    title="개봉일 스크린수 vs 총 관객수 (버블 크기: 개봉 첫 주 관객수)",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객수(명)',
        'first_week_audi': '개봉 첫 주 관객수(명)',
        'genre': '장르'
    }
)

fig6.update_traces(
    hovertemplate="<b>영화명:</b> %{hovertext}<br><b>개봉일 스크린수:</b> %{x:,}개<br><b>총 관객수:</b> %{y:,}명<br><b>개봉 첫 주 관객수:</b> %{marker.size:,}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 점의 크기(첫 주 관객수)를 통해 초반 흥행 몰이에 성공하여 최종 관객수까지 이어진 영화와, 초반에는 작았지만(작은 버블) 입소문을 통해 입체적으로 대형 흥행(높은 위치)을 이뤄낸 영화를 한눈에 구분할 수 있습니다.")

st.divider()
 
