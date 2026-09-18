# 2. 장르 및 영화별 총 관객 수 (트리맵)
st.subheader("2. 장르 및 영화별 총 관객 수 분포")

# 동일 장르 내 중복된 영화명이 있는 경우 합산하여 정리
df_treemap = df.groupby(['genre', 'movieNm'], as_index=False)['total_audi'].sum()

# Plotly 트리맵 생성 (계층 구조: 전체 -> 장르 -> 영화명)
fig2 = px.treemap(
    df_treemap,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    title="장르 내 영화별 총 관객 수 트리맵"
)

# 마우스 호버 시 영화명과 총 관객 수가 표기되도록 설정
fig2.update_traces(
    hovertemplate="<b>영역/영화명:</b> %{label}<br><b>총 관객 수:</b> %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

st.info("💡 **이 그래프로 알 수 있는 것:** 각 장르 내에서 어떤 영화가 총 관객 수의 대부분을 차지하며 흥행을 주도했는지 한눈에 비교해 볼 수 있습니다.")
