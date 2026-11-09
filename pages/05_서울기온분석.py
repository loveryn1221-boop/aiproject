import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ==========================================
# 1. 페이지 기본 설정
# ==========================================

st.set_page_config(
    page_title="월별기온 분석",
    page_icon="🌡️",
    layout="wide"
)

# ==========================================
# 2. 화면 디자인
# ==========================================

st.markdown("""
<style>
    .stApp {
        background-color: #10101c;
        color: white;
    }

    h1 {
        color: #ff4da6 !important;
        text-align: center;
        text-shadow: 0 0 10px #ff1493,
                     0 0 20px #ff1493;
    }

    h2, h3 {
        color: #ffffff !important;
    }

    p, label {
        color: white !important;
    }

    div[data-baseweb="select"] {
        background-color: #25253a;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CSV 파일 불러오기
# ==========================================

@st.cache_data
def load_data():

    # app.py가 루트 또는 pages 폴더에 있을 때 모두 대응
    current_folder = Path(__file__).resolve().parent

    possible_paths = [
        current_folder / "temperature.csv",
        current_folder.parent / "temperature.csv"
    ]

    csv_path = None

    for path in possible_paths:
        if path.exists():
            csv_path = path
            break

    if csv_path is None:
        raise FileNotFoundError(
            "temperature.csv 파일을 찾을 수 없습니다."
        )

    # CP949 인코딩으로 한글 깨짐 방지
    df = pd.read_csv(
        csv_path,
        encoding="cp949"
    )

    return df


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 파일을 불러오지 못했습니다: {e}")
    st.stop()


# ==========================================
# 4. 데이터 전처리
# ==========================================

required_columns = [
    "일시",
    "최고기온(℃)",
    "최저기온(℃)"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"CSV 파일에 필요한 열이 없습니다: {missing_columns}"
    )
    st.stop()


# 영문 월 이름을 숫자로 변환
month_dict = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

df["월_영문"] = (
    df["일시"]
    .astype(str)
    .str.strip()
    .str[:3]
    .str.title()
)

df["월"] = df["월_영문"].map(month_dict)

if df["월"].isna().any():
    st.error("날짜 데이터에 인식할 수 없는 월이 있습니다.")
    st.stop()


# ==========================================
# 5. 두 자리 연도 복원
# ==========================================

# 첫 데이터 Oct-07은 1907년 10월부터 시작하는
# 연속 월별 기온 자료이므로 월이 12월에서 1월로
# 넘어갈 때마다 연도를 1 증가시킴.

start_year = 1907

years = []
current_year = start_year
previous_month = None

for month in df["월"]:

    month = int(month)

    if previous_month is not None:
        if month < previous_month:
            current_year += 1

    years.append(current_year)
    previous_month = month

df["연도"] = years


# 기온 데이터 숫자형 변환
df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"],
    errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"],
    errors="coerce"
)


# ==========================================
# 6. 앱 제목
# ==========================================

st.title("🌡️ 월별기온 분석")

st.markdown(
    "<p style='text-align:center; color:#ccccdd;'>"
    "원하는 월을 선택하여 연도별 최고기온과 최저기온을 비교해 보세요!"
    "</p>",
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 7. 월 선택
# ==========================================

month_names = [
    "1월", "2월", "3월", "4월",
    "5월", "6월", "7월", "8월",
    "9월", "10월", "11월", "12월"
]

selected_month = st.selectbox(
    "📅 분석할 월을 선택하세요.",
    month_names,
    index=0
)

selected_month_num = month_names.index(
    selected_month
) + 1


# ==========================================
# 8. 선택한 월의 데이터 추출
# ==========================================

filtered_df = df[
    df["월"] == selected_month_num
].copy()

filtered_df = filtered_df.sort_values(
    by="연도"
)

if filtered_df.empty:
    st.warning("선택한 월에 해당하는 데이터가 없습니다.")
    st.stop()


# ==========================================
# 9. 그래프 데이터 생성
# ==========================================

# 최고기온과 최저기온은 각각 결측치를 제외
high_df = filtered_df.dropna(
    subset=["최고기온(℃)"]
)

low_df = filtered_df.dropna(
    subset=["최저기온(℃)"]
)


# ==========================================
# 10. 네온 그래프 생성
# ==========================================

fig = go.Figure()


# 네온 핫핑크 최고기온 그래프
def add_neon_line(
    fig,
    x,
    y,
    name,
    color,
    glow_colors
):

    # 빛나는 효과를 위한 바깥쪽 레이어
    for width, glow_color in zip(
        [18, 12, 7],
        glow_colors
    ):

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line=dict(
                    color=glow_color,
                    width=width
                ),
                hoverinfo="skip",
                showlegend=False
            )
        )

    # 실제 데이터 선
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            name=name,
            line=dict(
                color=color,
                width=3.5
            ),
            marker=dict(
                color=color,
                size=8,
                line=dict(
                    color="white",
                    width=1
                )
            ),
            hovertemplate=(
                "연도: %{x}년<br>"
                + name + ": %{y:.1f}℃"
                + "<extra></extra>"
            )
        )
    )


# 최고기온: 네온 핫핑크
add_neon_line(
    fig,
    high_df["연도"],
    high_df["최고기온(℃)"],
    "최고기온",
    "#ff1493",
    [
        "rgba(255, 20, 147, 0.10)",
        "rgba(255, 20, 147, 0.20)",
        "rgba(255, 20, 147, 0.35)"
    ]
)


# 최저기온: 네온 파란색
add_neon_line(
    fig,
    low_df["연도"],
    low_df["최저기온(℃)"],
    "최저기온",
    "#00bfff",
    [
        "rgba(0, 191, 255, 0.10)",
        "rgba(0, 191, 255, 0.20)",
        "rgba(0, 191, 255, 0.35)"
    ]
)


# ==========================================
# 11. 그래프 레이아웃 설정
# ==========================================

fig.update_layout(

    title=dict(
        text="월별기온 분석",
        x=0.5,
        xanchor="center",
        font=dict(
            size=27,
            color="white"
        )
    ),

    xaxis=dict(
        title="연도",
        title_font=dict(
            size=16,
            color="white"
        ),
        tickfont=dict(
            color="white"
        ),
        showgrid=True,
        gridcolor="rgba(255,255,255,0.12)",
        zeroline=False
    ),

    yaxis=dict(
        title="온도(℃)",
        title_font=dict(
            size=16,
            color="white"
        ),
        tickfont=dict(
            color="white"
        ),
        showgrid=True,
        gridcolor="rgba(255,255,255,0.12)",
        zeroline=False
    ),

    legend=dict(
        title="기온 종류",
        font=dict(
            color="white",
            size=14
        ),
        bgcolor="rgba(20,20,35,0.8)",
        bordercolor="#555577",
        borderwidth=1
    ),

    plot_bgcolor="#171727",
    paper_bgcolor="#10101c",

    hovermode="x unified",

    height=600,

    margin=dict(
        l=50,
        r=40,
        t=90,
        b=60
    )
)


# ==========================================
# 12. 그래프 출력
# ==========================================

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 13. 데이터 표 출력
# ==========================================

st.subheader("📊 선택한 월의 연도별 기온 데이터")

display_df = filtered_df[
    [
        "연도",
        "최고기온(℃)",
        "최저기온(℃)"
    ]
].copy()

display_df.columns = [
    "연도",
    "최고기온(℃)",
    "최저기온(℃)"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# 14. 데이터 요약
# ==========================================

col1, col2 = st.columns(2)

with col1:

    if not high_df.empty:

        max_temp = high_df["최고기온(℃)"].max()

        st.metric(
            "🔥 선택 월의 최고기온 최댓값",
            f"{max_temp:.1f}℃"
        )

with col2:

    if not low_df.empty:

        min_temp = low_df["최저기온(℃)"].min()

        st.metric(
            "❄️ 선택 월의 최저기온 최솟값",
            f"{min_temp:.1f}℃"
        )

st.caption(
    "※ 결측치는 그래프와 통계에서 자동으로 제외됩니다."
)
