
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# =====================================
# 1. 페이지 설정
# =====================================

st.set_page_config(
    page_title="MBTI WORLD",
    page_icon="💗",
    layout="wide"
)

# =====================================
# 2. CSV 파일 경로 설정
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "countriesMBTI_16types.csv"


# =====================================
# 3. 화면 디자인
# =====================================

st.markdown("""
<style>
.stApp {
    background-color: #FFF8FC;
}

h1 {
    color: #FF1493;
    text-align: center;
    font-weight: 900;
}

h2, h3 {
    color: #E754A5;
}

div[data-testid="stMetric"] {
    background-color: #FFE4F1;
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)


# =====================================
# 4. 데이터 불러오기
# =====================================

@st.cache_data
def load_data(file_path):

    data = pd.read_csv(file_path)

    data.columns = data.columns.str.strip()

    return data


if not CSV_PATH.exists():

    st.error("CSV 파일을 찾을 수 없습니다.")

    st.write("현재 Python 파일 위치:", Path(__file__).resolve())

    st.write("찾으려는 CSV 경로:", CSV_PATH)

    st.stop()


try:

    df = load_data(str(CSV_PATH))

except Exception as error:

    st.error(f"데이터 불러오기 오류: {error}")

    st.stop()


# =====================================
# 5. MBTI 유형 설정
# =====================================

mbti_list = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

required_columns = ["Country"] + mbti_list

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(f"CSV에 필요한 열이 없습니다: {missing_columns}")

    st.stop()


# =====================================
# 6. 데이터 정리
# =====================================

df["Country"] = df["Country"].astype(str).str.strip()

for mbti in mbti_list:

    df[mbti] = pd.to_numeric(
        df[mbti],
        errors="coerce"
    )

df = df.dropna(subset=["Country"])

countries = sorted(df["Country"].unique().tolist())


# =====================================
# 7. 제목
# =====================================

st.title("🌎 MBTI WORLD")

st.markdown(
    """
    <p style="
        text-align:center;
        font-size:18px;
        color:#888888;
    ">
    세계 여러 나라의 MBTI 성향을 탐험해 보자! 💗
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# =====================================
# 8. 국가 선택
# =====================================

st.subheader("🌍 어느 나라를 탐험할까?")

default_index = 0

if "South Korea" in countries:

    default_index = countries.index("South Korea")

selected_country = st.selectbox(
    "국가를 선택해 주세요!",
    countries,
    index=default_index
)


# =====================================
# 9. 국가 데이터 가져오기
# =====================================

country_data = df[
    df["Country"] == selected_country
].iloc[0]

mbti_data = pd.DataFrame({

    "MBTI": mbti_list,

    "비율": [
        country_data[mbti] * 100
        for mbti in mbti_list
    ]

})

mbti_data["비율"] = mbti_data["비율"].fillna(0)

mbti_data = mbti_data.sort_values(
    by="비율",
    ascending=False
).reset_index(drop=True)


# =====================================
# 10. 주요 통계
# =====================================

st.subheader(f"💗 {selected_country}의 MBTI 분석")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🥇 가장 높은 MBTI",
        mbti_data.iloc[0]["MBTI"]
    )

with col2:

    st.metric(
        "📊 가장 높은 비율",
        f'{mbti_data.iloc[0]["비율"]:.2f}%'
    )

with col3:

    st.metric(
        "🌈 분석 유형",
        "16가지"
    )

st.divider()


# =====================================
# 11. 핫핑크 그라데이션
# =====================================

pink_colors = [
    "#FF1493",
    "#FF2E9F",
    "#FF48AB",
    "#FF62B7",
    "#FF7CC3",
    "#FF96CF",
    "#FFB0DB",
    "#FFC0E1",
    "#FFCBE6",
    "#FFD2EA",
    "#FFD9EE",
    "#FFE0F2",
    "#FFE7F5",
    "#FFEDF8",
    "#FFF2FA",
    "#FFF5FC"
]


# =====================================
# 12. MBTI 막대그래프
# =====================================

st.subheader("📊 MBTI 비율 막대그래프")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=mbti_data["비율"],

        y=mbti_data["MBTI"],

        orientation="h",

        marker_color=pink_colors[:len(mbti_data)],

        text=[
            f"{value:.2f}%"
            for value in mbti_data["비율"]
        ],

        textposition="outside",

        textfont=dict(
            color="#555555",
            size=13
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

    plot_bgcolor="#FFF8FC",

    paper_bgcolor="#FFF8FC",

    showlegend=False,

    font=dict(
        family="Arial",
        size=13,
        color="#444444"
    ),

    margin=dict(
        l=60,
        r=90,
        t=30,
        b=60
    ),

    xaxis=dict(
        title="MBTI 비율 (%)",
        ticksuffix="%",
        showgrid=True,
        gridcolor="#F5DCE9",
        rangemode="tozero"
    ),

    yaxis=dict(
        title="MBTI 유형",
        autorange="reversed"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================
# 13. MBTI 순위표
# =====================================

st.subheader("🏆 MBTI 순위 TOP 16")

ranking_data = mbti_data.copy()

ranking_data.insert(
    0,
    "순위",
    range(1, len(ranking_data) + 1)
)

ranking_data["비율"] = ranking_data["비율"].map(
    lambda value: f"{value:.2f}%"
)

st.dataframe(
    ranking_data,
    use_container_width=True,
    hide_index=True
)


# =====================================
# 14. CSV 다운로드
# =====================================

st.divider()

st.subheader("📥 분석 결과 다운로드")

download_data = mbti_data.copy()

download_data["비율"] = download_data["비율"].round(2)

csv_data = download_data.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="💗 MBTI 분석 결과 다운로드",
    data=csv_data,
    file_name=f"{selected_country}_MBTI.csv",
    mime="text/csv"
)


# =====================================
# 15. 안내 문구
# =====================================

st.divider()

st.info(
    "💡 본 결과는 제공된 CSV 데이터에 기반한 "
    "국가별 MBTI 유형 비율입니다. "
    "실제 국민 전체의 성격을 확정하는 통계는 아닙니다."
)

st.markdown(
    """
    <div style="
        text-align:center;
        color:#FF69B4;
        padding:20px;
        font-size:16px;
    ">
        💗 Made with Streamlit | MBTI WORLD 🌎
    </div>
    """,
    unsafe_allow_html=True
)
```
