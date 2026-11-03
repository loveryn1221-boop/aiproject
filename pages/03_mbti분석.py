```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ----------------------------------
# 1. 페이지 설정
# ----------------------------------
st.set_page_config(
    page_title="세계 MBTI 탐험 🌎",
    page_icon="💗",
    layout="wide"
)

# ----------------------------------
# 2. 디자인
# ----------------------------------
st.markdown("""
<style>
    .main {
        background-color: #FFF8FC;
    }

    h1 {
        color: #FF1493;
        text-align: center;
        font-weight: 900;
    }

    h3 {
        color: #E754A5;
    }

    div[data-testid="stMetric"] {
        background-color: #FFE4F1;
        padding: 15px;
        border-radius: 15px;
    }

    .description {
        text-align: center;
        color: #888888;
        font-size: 17px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# 3. 데이터 불러오기
# ----------------------------------
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "countriesMBTI_16types.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "countriesMBTI_16types.csv 파일을 찾을 수 없습니다."
        )

    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip()
    df["Country"] = df["Country"].astype(str).str.strip()

    return df


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# MBTI 16가지 유형
mbti_columns = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# 데이터 확인
missing_columns = [
    col for col in ["Country"] + mbti_columns
    if col not in df.columns
]

if missing_columns:
    st.error(f"CSV 파일에 필요한 열이 없습니다: {missing_columns}")
    st.stop()

# ----------------------------------
# 4. 제목
# ----------------------------------
st.title("🌎 MBTI WORLD")
st.markdown(
    '<p class="description">세계 여러 나라의 MBTI 성향을 탐험해 보자! 💗</p>',
    unsafe_allow_html=True
)

st.divider()

# ----------------------------------
# 5. 국가 선택
# ----------------------------------
st.subheader("🌍 어느 나라를 탐험할까?")

countries = sorted(df["Country"].dropna().unique().tolist())

selected_country = st.selectbox(
    "국가를 선택해 주세요!",
    countries,
    index=countries.index("South Korea")
    if "South Korea" in countries else 0
)

# ----------------------------------
# 6. 선택 국가 데이터 가져오기
# ----------------------------------
country_data = df[
    df["Country"] == selected_country
].iloc[0]

# MBTI 비율 데이터
mbti_data = pd.DataFrame({
    "MBTI": mbti_columns,
    "비율": [
        float(country_data[mbti]) * 100
        for mbti in mbti_columns
    ]
})

# 높은 비율 순서대로 정렬
mbti_data = mbti_data.sort_values(
    by="비율",
    ascending=False
).reset_index(drop=True)

# ----------------------------------
# 7. 주요 정보
# ----------------------------------
st.subheader(f"💗 {selected_country}의 MBTI 분석")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🥇 가장 높은 MBTI",
        value=mbti_data.iloc[0]["MBTI"]
    )

with col2:
    st.metric(
        label="📊 가장 높은 비율",
        value=f'{mbti_data.iloc[0]["비율"]:.2f}%'
    )

with col3:
    st.metric(
        label="🌈 분석 유형",
        value="16가지"
    )

st.divider()

# ----------------------------------
# 8. 핫핑크 그라데이션 색상 만들기
# ----------------------------------
def make_gradient(start_color, end_color, steps):

    start = tuple(
        int(start_color[i:i+2], 16)
        for i in (1, 3, 5)
    )

    end = tuple(
        int(end_color[i:i+2], 16)
        for i in (1, 3, 5)
    )

    colors = []

    for i in range(steps):
        ratio = i / max(steps - 1, 1)

        color = tuple(
            int(start[j] + (end[j] - start[j]) * ratio)
            for j in range(3)
        )

        colors.append(
            "#%02X%02X%02X" % color
        )

    return colors


# 1위 진한 핫핑크 → 16위 연한 핑크
pink_colors = make_gradient(
    "#FF1493",
    "#FFF0F6",
    len(mbti_data)
)

# ----------------------------------
# 9. 막대그래프
# ----------------------------------
st.subheader("📊 국가별 MBTI 비율")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=mbti_data["비율"],
        y=mbti_data["MBTI"],
        orientation="h",

        marker=dict(
            color=pink_colors,
            line=dict(
                color="#FFFFFF",
                width=1
            )
        ),

        text=[
            f"{value:.2f}%"
            for value in mbti_data["비율"]
        ],

        textposition="outside",
        textfont=dict(
            size=13,
            color="#555555"
        ),

        hovertemplate=(
            "<b>%{y}</b><br>"
            "비율: %{x:.2f}%"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    height=650,

    xaxis=dict(
        title="MBTI 비율 (%)",
        showgrid=True,
        gridcolor="#F5DCE9",
        ticksuffix="%",
        rangemode="tozero"
    ),

    yaxis=dict(
        title="MBTI 유형",
        autorange="reversed"
    ),

    plot_bgcolor="#FFF8FC",
    paper_bgcolor="#FFF8FC",

    font=dict(
        family="Arial",
        size=13,
        color="#444444"
    ),

    margin=dict(
        l=60,
        r=80,
        t=30,
        b=60
    ),

    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# 10. MBTI 순위표
# ----------------------------------
st.subheader("🏆 MBTI 순위 TOP 16")

ranking_data = mbti_data.copy()

ranking_data.index = ranking_data.index + 1
ranking_data.index.name = "순위"

ranking_data["비율"] = ranking_data["비율"].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    ranking_data,
    use_container_width=True
)

# ----------------------------------
# 11. CSV 다운로드
# ----------------------------------
st.divider()

st.subheader("📥 데이터 다운로드")

download_df = mbti_data.copy()

download_df["비율"] = download_df["비율"].round(2)

csv = download_df.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="💗 MBTI 분석 결과 다운로드",
    data=csv,
    file_name=f"{selected_country}_MBTI_analysis.csv",
    mime="text/csv"
)

# ----------------------------------
# 12. 안내 문구
# ----------------------------------
st.divider()

st.caption(
    "💡 본 결과는 제공된 CSV 데이터에 기초한 국가별 MBTI 비율입니다. "
    "실제 국민 전체의 성격이나 개인의 성격을 확정하는 자료는 아닙니다."
)

st.markdown(
    "<center>💗 Made with Streamlit | MBTI WORLD 🌎</center>",
    unsafe_allow_html=True
)
```
