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
