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
    
    # genre 열 전처리: '|' 기호로 연결된 장르 중 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    
    # total_audi 수치형 변환
    df['total_audi'] = pd.to_numeric(df['total_audi'], errors='coerce').fillna(0)
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
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 분석 구역
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

# 마우스 호버 시 영화명/장르 및 총 관객 수 표기
fig2.update_traces(
    hovertemplate="<b>구분:</b> %{label}<br><b>총 관객 수:</b> %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 분석 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 각 장르 내에서 어떤 영화가 총 관객 수의 대부분을 차지하며 흥행을 주도했는지 한눈에 비교해 볼 수 있습니다.")

st.divider()
```eof

기존 도넛 그래프 아래에 트리맵 그래프와 해당 분석 문구 구역을 새롭게 구성했습니다. 추가로 필요한 그래프가 있다면 언제든 말씀해 주세요!Plotly 기반(Python)에서 기존 코드 뒤에 두 번째 그래프로 **트리맵(Treemap)**을 추가하는 예시 코드입니다. 

`px.treemap`을 활용하면 장르(parents) - 영화명(labels) 계층 구조와 관객수(values)에 따른 크기를 손쉽게 표현할 수 있으며, 마우스 호버 시 지정한 정보가 표시됩니다.

```python
import plotly.express as px

# 1. 데이터 예시 (기존 df에 맞춰 컬럼명을 확인해 주세요)
# df: 'genre', 'title', 'total_audi' 컬럼을 포함하는 DataFrame

# 2. 트리맵 그래프 생성
fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), "genre", "title"],  # 계층 구조: 전체 -> 장르 -> 영화명
    values="total_audi",  # 칸의 크기: 총 관객 수
    color="genre",  # 장르별 색상 구분
    title="장르 및 영화별 총 관객 수 (Treemap)",
    custom_data=["title", "total_audi"],  # 호버 툴팁에 사용할 데이터
)

# 3. 마우스 호버(Hover) 툴팁 설정
fig_treemap.update_traces(
    hovertemplate="<b>영화명:</b> %{customdata[0]}<br>"
    + "<b>총 관객수:</b> %{customdata[1]:,}명<extra></extra>"
)

# 4. 레이아웃 설정 및 출력
fig_treemap.update_layout(margin=dict(t=50, l=10, r=10, b=10))
fig_treemap.show()
