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
# 2. CSV 파일 경로
# =====================================

# 현재 파일은 pages 폴더 안에 있음
# 상위 폴더로 이동해서 CSV 파일 찾기

PROJECT_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = PROJECT_DIR / "countriesMBTI_16types.csv"


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
# 4. MBTI 유형 설정
# =====================================

MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]


# =====================================
# 5. 데이터 불러오기
# =====================================

@st.cache_data
def load_data(file_path):

    data = pd.read_csv(file_path)

    data.columns = data.columns.str.strip()

    return data


if not CSV_PATH.is_file():

    st.error("CSV 파일을 찾을 수 없습니다.")

    st.write("현재 파일 위치:", str(Path(__file__).resolve()))

    st.write("찾는 CSV 위치:", str(CSV_PATH))

    st.stop()


try:

    df = load_data(str(CSV_PATH))

except Exception as error:

    st.error(f"CSV 읽기 오류: {error}")

    st.stop()


# =====================================
# 6. 데이터 확인
# =====================================

required_columns = ["Country"] + MBTI_TYPES

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        f"CSV에 필요한 열이 없습니다: {missing_columns}"
    )

    st.stop()


df["Country"] = df["Country"].astype(str).str.strip()

for mbti in MBTI_TYPES:

    df[mbti] = pd.to_numeric(
        df[mbti],
        errors="coerce"
    )

df = df.dropna(subset=["Country"])

countries = sorted(
    df["Country"].dropna().unique().tolist()
)

if not countries:

    st.error("국가 데이터가 없습니다.")

    st.stop()


# =====================================
# 7. 제목
# =====================================

st.title("🌎 MBTI WORLD")

st.markdown(
    """
    <p style="
        text-align:center;
        color:#888888;
        font-size:18px;
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
# 9. 선택한 국가 데이터
# =====================================

selected_rows = df[
    df["Country"] == selected_country
]

country_data = selected_rows.iloc[0]

result = pd.DataFrame({

    "MBTI": MBTI_TYPES,

    "비율": [
        country_data[mbti] * 100
        for mbti in MBTI_TYPES
    ]

})

result["비율"] = result["비율"].fillna(0)

result = result.sort_values(
    by="비율",
    ascending=False
).reset_index(drop=True)


# =====================================
# 10. 주요 통계
# =====================================

st.subheader(
    f"💗 {selected_country}의 MBTI 분석"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🥇 가장 높은 MBTI",
        result.iloc[0]["MBTI"]
    )

with col2:

    st.metric(
        "📊 가장 높은 비율",
        f'{result.iloc[0]["비율"]:.2f}%'
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
        x=result["비율"],

        y=result["MBTI"],

        orientation="h",

        marker_color=pink_colors[:len(result)],

        text=[
            f"{value:.2f}%"
            for value in result["비율"]
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

    margin=dict(
        l=60,
        r=90,
        t=30,
        b=60
    ),

    font=dict(
        family="Arial",
        size=13,
        color="#444444"
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

ranking = result.copy()

ranking.insert(
    0,
    "순위",
    range(1, len(ranking) + 1)
)

ranking["비율"] = ranking["비율"].map(
    lambda value: f"{value:.2f}%"
)

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)


# =====================================
# 14. CSV 다운로드
# =====================================

st.divider()

st.subheader("📥 분석 결과 다운로드")

download_data = result.copy()

download_data["비율"] = (
    download_data["비율"].round(2)
)

csv_data = download_data.to_csv(
    index=False
).encode("utf-8-sig")

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
    <p style="
        text-align:center;
        color:#FF69B4;
        padding:20px;
        font-size:16px;
    ">
    💗 Made with Streamlit | MBTI WORLD 🌎
    </p>
    """,
    unsafe_allow_html=True
)
