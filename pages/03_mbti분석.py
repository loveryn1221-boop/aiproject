import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import sample_colorscale
from pathlib import Path

# =====================================
# 1. 기본 설정
# =====================================

st.set_page_config(
    page_title="MBTI WORLD",
    page_icon="💗",
    layout="wide"
)

# 현재 파일은 pages 폴더 안에 있음
# CSV 파일은 프로젝트 최상위 폴더에 있음
PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "countriesMBTI_16types.csv"


# =====================================
# 2. 화면 디자인
# =====================================

st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)


# =====================================
# 3. MBTI 유형 목록
# =====================================

MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]


# =====================================
# 4. CSV 파일 불러오기
# =====================================

@st.cache_data
def load_data(csv_path):
    data = pd.read_csv(csv_path)
    data.columns = data.columns.str.strip()
    return data


# =====================================
# 5. 제목
# =====================================

st.title("🌎 MBTI WORLD")

st.markdown(
    """
    <p style='text-align:center; color:#888; font-size:18px;'>
    내가 선택한 MBTI는 어느 나라에서 가장 많이 나타날까? 💗
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# =====================================
# 6. CSV 파일 확인
# =====================================

if not CSV_PATH.is_file():
    st.error("CSV 파일을 찾을 수 없습니다.")

    st.write("현재 실행 파일:", str(Path(__file__).resolve()))
    st.write("찾는 CSV 파일:", str(CSV_PATH))

    st.stop()


try:
    df = load_data(str(CSV_PATH))

except Exception as exc:
    st.error(f"CSV 파일 읽기 오류: {exc}")
    st.stop()


# =====================================
# 7. 필요한 열 확인
# =====================================

required_columns = ["Country"] + MBTI_TYPES

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"CSV에 필요한 열이 없습니다: {', '.join(missing_columns)}"
    )
    st.stop()


# =====================================
# 8. 데이터 정리
# =====================================

df["Country"] = df["Country"].astype(str).str.strip()

for mbti in MBTI_TYPES:
    df[mbti] = pd.to_numeric(
        df[mbti],
        errors="coerce"
    )

df = df.dropna(subset=["Country"])

df = df[df["Country"] != ""]

if df.empty:
    st.error("국가 데이터가 없습니다.")
    st.stop()


# =====================================
# 9. MBTI 선택
# =====================================

st.subheader("💗 나의 MBTI를 선택해 보자!")

selected_mbti = st.selectbox(
    "어떤 MBTI를 분석할까요?",
    MBTI_TYPES,
    index=0
)

st.divider()


# =====================================
# 10. 국가별 MBTI 비율 분석
# =====================================

result = df[["Country", selected_mbti]].copy()

result = result.rename(
    columns={
        selected_mbti: "비율"
    }
)

# CSV의 비율 데이터를 퍼센트로 변환
result["비율"] = result["비율"] * 100

# 결측값 제거
result = result.dropna(subset=["비율"])

# 국가별 중복 데이터가 있다면 평균 계산
result = (
    result.groupby("Country", as_index=False)["비율"]
    .mean()
)

# 비율이 높은 국가부터 정렬
result = result.sort_values(
    by="비율",
    ascending=False
).reset_index(drop=True)

# 순위 추가
result.insert(
    0,
    "순위",
    range(1, len(result) + 1)
)

if result.empty:
    st.warning("분석할 데이터가 없습니다.")
    st.stop()


# =====================================
# 11. 상위 국가 정보
# =====================================

top_country = result.iloc[0]["Country"]
top_ratio = result.iloc[0]["비율"]

st.subheader(f"🌍 {selected_mbti} 국가별 분석")

col1, col2, col3 = st.columns(3)

col1.metric(
    "🥇 1위 국가",
    top_country
)

col2.metric(
    "📊 1위 비율",
    f"{top_ratio:.2f}%"
)

col3.metric(
    "🌎 분석 국가 수",
    f"{len(result)}개"
)

st.divider()


# =====================================
# 12. 핫핑크 그라데이션 만들기
# =====================================

def make_pink_colors(count):

    if count <= 1:
        return ["#FF1493"]

    colors = sample_colorscale(
        ["#FF1493", "#FFF5FC"],
        [
            i / (count - 1)
            for i in range(count)
        ]
    )

    return colors


pink_colors = make_pink_colors(len(result))


# =====================================
# 13. 국가별 순위 막대그래프
# =====================================

st.subheader(
    f"🏆 {selected_mbti} 국가별 순위"
)

st.caption(
    "🥇 1위부터 순서대로 표시됩니다. "
    "막대 색상은 진한 핫핑크에서 연한 핑크로 변합니다."
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=result["비율"],
        y=result["Country"],
        orientation="h",

        marker=dict(
            color=pink_colors
        ),

        text=[
            f"{value:.2f}%"
            for value in result["비율"]
        ],

        textposition="outside",

        textfont=dict(
            color="#555555",
            size=11
        ),

        hovertemplate=(
            "<b>%{y}</b><br>"
            "MBTI 비율: %{x:.2f}%"
            "<extra></extra>"
        )
    )
)


# =====================================
# 14. 그래프 디자인
# =====================================

fig.update_layout(
    height=max(650, len(result) * 24),

    plot_bgcolor="#FFF8FC",
    paper_bgcolor="#FFF8FC",

    showlegend=False,

    margin=dict(
        l=130,
        r=90,
        t=30,
        b=60
    ),

    font=dict(
        family="Arial",
        size=12,
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
        title="국가",
        autorange="reversed"
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================
# 15. 국가별 순위표
# =====================================

st.divider()

st.subheader(
    f"📋 {selected_mbti} 국가별 TOP 순위표"
)

ranking_table = result.copy()

ranking_table["비율"] = ranking_table["비율"].map(
    lambda value: f"{value:.2f}%"
)

st.dataframe(
    ranking_table,
    use_container_width=True,
    hide_index=True
)


# =====================================
# 16. CSV 다운로드
# =====================================

st.divider()

st.subheader("📥 분석 결과 다운로드")

download_df = result.copy()

download_df["비율"] = download_df["비율"].round(2)

csv_bytes = download_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="💗 국가별 MBTI 순위 다운로드",

    data=csv_bytes,

    file_name=f"{selected_mbti}_국가별순위.csv",

    mime="text/csv"
)


# =====================================
# 17. 안내 문구
# =====================================

st.divider()

st.info(
    "💡 이 결과는 제공된 CSV 데이터에 기반한 분석입니다. "
    "실제 국가 전체 인구의 성격을 확정하는 통계는 아닙니다."
)

st.markdown(
    """
    <p style='text-align:center; color:#FF69B4;'>
    💗 Made with Streamlit | MBTI WORLD 🌎
    </p>
    """,
    unsafe_allow_html=True
)
