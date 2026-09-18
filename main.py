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
    
    # 숫자형 데이터 변환 및 결측치 처리
    df['total_audi'] = pd.to_numeric(df['total_audi'], errors='coerce').fillna(0)
    df['first_scrn'] = pd.to_numeric(df['first_scrn'], errors='coerce').fillna(0)
    df['first_show'] = pd.to_numeric(df['first_show'], errors='coerce').fillna(0)
    df['first_week_audi'] = pd.to_numeric(df['first_week_audi'], errors='coerce').fillna(0)
    df['days_in_top10'] = pd.to_numeric(df['days_in_top10'], errors='coerce').fillna(0)
    
    # nation 결측치 및 빈 문자열 처리
    df['nation'] = df['nation'].fillna('미상').astype(str)
    
    return df

df = load_data()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 비율")

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig_donut = px.pie(
    genre_counts,
    values='count',
    names='genre',
    hole=0.4,
    title="장르별 영화 분포"
)

fig_donut.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig_donut, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("박스오피스 상위권 영화 중 특정 주요 장르가 차지하는 비중과 장르별 다변화 정도를 한눈에 파악할 수 있습니다.")

st.write("")

# -------------------------------------------------------------------
# 두 번째 그래프: 장르-영화 계층별 총 관객 수 (트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객 수 분포")

df_treemap = df.groupby(['genre', 'movieNm'], as_index=False)['total_audi'].sum()

fig_treemap = px.treemap(
    df_treemap,
    path=['genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 총 관객 수 (Treemap)",
    color='genre'
)

fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("장르 전체의 관객 수 규모와 함께, 각 장르 내에서 어떤 영화가 총 관객 수를 주도했는지 개별 영화의 기여도를 직관적으로 비교할 수 있습니다.")

st.write("")

# -------------------------------------------------------------------
# 세 번째 그래프: 총 관객 수 히스토그램
# -------------------------------------------------------------------
st.subheader("3. 총 관객 수 분포 (히스토그램)")

fig_hist = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객 수 분포",
    labels={'total_audi': '총 관객 수 (명)'}
)

fig_hist.update_traces(
    hovertemplate="관객 수 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
)

fig_hist.update_layout(
    yaxis_title="영화 수 (편)",
    bargap=0.1
)

st.plotly_chart(fig_hist, use_container_width=True)

max_movie = df.loc[df['total_audi'].idxmax()]
max_movie_name = max_movie['movieNm']
max_movie_audi = int(max_movie['total_audi'])

under_5m_count = (df['total_audi'] < 5000000).sum()
under_5m_ratio = (under_5m_count / len(df)) * 100

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info(
    f"대부분의 영화({under_5m_ratio:.1f}%)가 **관객 수 500만 명 미만** 구간에 몰려 있으며, "
    f"가장 많은 관객 수를 기록한 영화는 **'{max_movie_name}'**({max_movie_audi:,.0f}명)입니다."
)

st.write("")

# -------------------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린수 vs 총 관객 수 (산점도)
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린 수와 총 관객 수의 관계")

fig_scatter = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린 수 vs 총 관객 수",
    labels={
        'first_scrn': '개봉일 스크린 수 (개)',
        'total_audi': '총 관객 수 (명)',
        'genre': '장르'
    }
)

fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린 수가 많을수록 대체로 총 관객 수가 증가하는 양의 상관관계를 보이며, 초기 스크린 확보가 흥행 규모에 중요한 요소임을 알 수 있습니다.")

st.write("")

# -------------------------------------------------------------------
# 다섯 번째 그래프: 주요 장르별 총 관객 수 상자 그림 (박스플롯)
# -------------------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 분포 (박스플롯)")

genre_counts_series = df['genre'].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered_genres = df[df['genre'].isin(top_genres)]

fig_box = px.box(
    df_filtered_genres,
    x='genre',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    points='outliers',
    title="영화 10편 이상 주요 장르별 총 관객 수 분포",
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수 (명)'
    }
)

fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig_box, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("주요 장르 간 중간 관객 수 및 변동 폭 차이를 비교할 수 있고, 각 장르 상자 위로 크게 벗어난 이상치 점을 통해 장르 내 초대형 흥행작을 판별할 수 있습니다.")

st.write("")

# -------------------------------------------------------------------
# 여섯 번째 그래프: 개봉일 스크린수 vs 총 관객 수 (버블 차트)
# -------------------------------------------------------------------
st.subheader("6. 개봉일 스크린 수, 총 관객 수, 개봉 첫 주 관객 수의 관계 (버블 차트)")

fig_bubble = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='genre',
    hover_name='movieNm',
    size_max=40,
    title="개봉일 스크린 수 vs 총 관객 수 (버블 크기: 개봉 첫 주 관객 수)",
    labels={
        'first_scrn': '개봉일 스크린 수 (개)',
        'total_audi': '총 관객 수 (명)',
        'first_week_audi': '개봉 첫 주 관객 수 (명)',
        'genre': '장르'
    }
)

fig_bubble.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<br>개봉 첫 주 관객 수: %{marker.size:,.0f}명<extra></extra>"
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린 수와 총 관객 수 관계에 더해, 원의 크기를 통해 초기 흥행(개봉 첫 주 관객 수)이 최종 총 관객 수 형성 및 흥행 지속성에 얼마나 영향을 주었는지 3가지 차원으로 파악할 수 있습니다.")

st.write("")

# -------------------------------------------------------------------
# 일곱 번째 그래프: 제작 국가 -> 장르 계층 구조 (선버스트 차트)
# -------------------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트)")

df_sunburst = df.groupby(['nation', 'genre'], as_index=False).size()
df_sunburst.columns = ['nation', 'genre', 'count']

fig_sunburst = px.sunburst(
    df_sunburst,
    path=['nation', 'genre'],
    values='count',
    title="제작 국가 및 장르별 영화 편수 분포",
    color='nation'
)

fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("영화의 제작 국가별 비중과 각 국가 내에서 어떤 장르의 영화들이 주로 제작되어 상위권에 진입했는지 계층적 비중을 다면적으로 살펴볼 수 있습니다.")

st.write("")

# -------------------------------------------------------------------
# 여덟 번째 그래프: 10위권 체류 날수 vs 총 관객 수 (산점도)
# -------------------------------------------------------------------
st.subheader("8. 10위권 체류 기간과 총 관객 수의 관계")

fig_top10_scatter = px.scatter(
    df,
    x='days_in_top10',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        'days_in_top10': '10위권에 머문 날수 (일)',
        'total_audi': '총 관객 수 (명)',
        'genre': '장르'
    }
)

fig_top10_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>10위권 체류 날수: %{x}일<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig_top10_scatter, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("10위권 내 체류 기간(롱런 여부)이 길수록 총 관객 수 역시 크게 증가하는 강한 양의 상관관계를 보이며, 장기 흥행이 대형 관객 집계의 핵심 요인임을 확인할 수 있습니다.")

st.write("")

# -------------------------------------------------------------------
# 아홉 번째 그래프: 개봉일 상영횟수 vs 개봉 첫 주 관객 수 (산점도)
# -------------------------------------------------------------------
st.subheader("9. 개봉일 상영 횟수와 첫 주 관객 수의 관계")

fig_show_scatter = px.scatter(
    df,
    x='first_show',
    y='first_week_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉 첫날 많이 틀어준 영화가 첫 주에 관객도 많이 들었을까",
    labels={
        'first_show': '개봉일 상영 횟수 (회)',
        'first_week_audi': '개봉 첫 주 관객 수 (명)',
        'genre': '장르'
    }
)

fig_show_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 상영 횟수: %{x:,.0f}회<br>개봉 첫 주 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig_show_scatter, use_container_width=True)

st.divider()
st.markdown("💡 **이 그래프로 알 수 있는 것**")
st.info("개봉 당일 상영 횟수가 많을수록 개봉 첫 주 관객 집중도가 뚜렷하게 높아지며, 초기 상영 회차 배정이 초반 기선 제압 및 흥행 모멘텀 형성에 직결됨을 알 수 있습니다.")
