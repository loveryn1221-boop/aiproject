
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="서울 기온 분석",
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
    color: #ff1493 !important;
    text-align: center;
    text-shadow: 0 0 10px #ff1493,
                 0 0 20px #ff1493;
}

h2, h3, p, label {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: #ff69b4;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. CSV 파일 불러오기
# ==========================================

@st.cache_data
def load_data():

    # 현재 파일은 pages 폴더에 있음
    # CSV는 상위 폴더에 있음
    base_path = Path(__file__).resolve().parent.parent

    csv_path = base_path / "temperature.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"temperature.csv 파일을 찾을 수 없습니다.\n{csv_path}"
        )

    # 한글 깨짐 방지: CP949
    df = pd.read_csv(
        csv_path,
        encoding="cp949"
    )

    return df


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 불러오기 오류: {e}")
    st.stop()


# ==========================================
# 4. 필요한 열 확인
# ==========================================

required_columns = [
    "일시",
    "평균기온(℃)",
    "최고기온(℃)",
    "최저기온(℃)"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"CSV에 필요한 열이 없습니다: {missing_columns}"
    )
    st.stop()


# ==========================================
# 5. 날짜 데이터 전처리
# ==========================================

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

month_names = [
    "1월", "2월", "3월", "4월",
    "5월", "6월", "7월", "8월",
    "9월", "10월", "11월", "12월"
]

df["일시"] = df["일시"].astype(str).str.strip()

df["월_영문"] = df["일시"].str[:3].str.title()

df["월"] = df["월_영문"].map(month_dict)

# 날짜 형식 확인
if df["월"].isna().any():
    st.error("날짜의 월 정보를 읽을 수 없습니다.")
    st.stop()


# ==========================================
# 6. 연도 복원
# ==========================================

# 데이터는 1907년부터 시작
# 두 자리 연도가 99에서 00으로 바뀌면
# 100년을 더하여 실제 연도를 복원

years = []
previous_year = None

for date in df["일시"]:

    try:
        short_year = int(date.split("-")[-1])
    except ValueError:
        st.error(f"연도 형식 오류: {date}")
        st.stop()

    current_year = 1900 + short_year

    if previous_year is not None:

        while current_year < previous_year:
            current_year += 100

    years.append(current_year)
    previous_year = current_year

df["연도"] = years


# ==========================================
# 7. 기온 데이터 숫자 변환
# ==========================================

temperature_columns = [
    "평균기온(℃)",
    "최고기온(℃)",
    "최저기온(℃)"
]

for col in temperature_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# 연도와 월 순서대로 정렬
df = df.sort_values(
    ["연도", "월"]
).reset_index(drop=True)


# ==========================================
# 8. 앱 제목
# ==========================================

st.title("🌡️ 서울 기온 데이터 분석")

st.markdown(
    """
    <p style="text-align:center; color:#ccccdd;">
    서울의 기온 변화를 그래프로 살펴보고
    서로 다른 연도의 기온도 비교해 보세요!
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 9. 네온 그래프 함수
# ==========================================

def add_neon_line(
    fig,
    x,
    y,
    name,
    color,
    glow_colors,
    showlegend=True
):

    # 빛 번짐 효과
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
            showlegend=showlegend,
            connectgaps=False,
            hovertemplate=(
                "%{x}<br>"
                + name + ": %{y:.1f}℃"
                + "<extra></extra>"
            )
        )
    )


# ==========================================
# 10. 공통 그래프 디자인
# ==========================================

def style_graph(fig, title, x_title, height=500):

    fig.update_layout(

        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(
                size=25,
                color="white"
            )
        ),

        xaxis=dict(
            title=x_title,
            title_font=dict(
                color="white",
                size=16
            ),
            tickfont=dict(color="white"),
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)"
        ),

        yaxis=dict(
            title="온도(℃)",
            title_font=dict(
                color="white",
                size=16
            ),
            tickfont=dict(color="white"),
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)"
        ),

        legend=dict(
            title="기온 종류",
            font=dict(
                color="white",
                size=13
            ),
            bgcolor="rgba(20,20,35,0.8)"
        ),

        plot_bgcolor="#171727",
        paper_bgcolor="#10101c",

        hovermode="x unified",

        height=height,

        margin=dict(
            l=50,
            r=40,
            t=80,
            b=60
        )
    )

    return fig


pink_glow = [
    "rgba(255,20,147,0.10)",
    "rgba(255,20,147,0.20)",
    "rgba(255,20,147,0.35)"
]

blue_glow = [
    "rgba(0,191,255,0.10)",
    "rgba(0,191,255,0.20)",
    "rgba(0,191,255,0.35)"
]


# ==========================================
# 11. 그래프 1
# 서울의 월별 평균기온
# ==========================================

st.header("📈 ① 서울의 월별 평균기온")

st.write(
    "전체 관측 기간을 기준으로 1월부터 12월까지 "
    "각 월의 평균기온을 비교합니다."
)

monthly_avg = (
    df.groupby("월")["평균기온(℃)"]
    .mean()
    .reindex(range(1, 13))
)

fig1 = go.Figure()

add_neon_line(
    fig1,
    month_names,
    monthly_avg.values,
    "월별 평균기온",
    "#ff1493",
    pink_glow
)

style_graph(
    fig1,
    "서울의 월별 평균기온",
    "월"
)

fig1.update_layout(
    showlegend=True
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.divider()


# ==========================================
# 12. 그래프 2
# 연도별 최고기온과 최저기온
# ==========================================

st.header("🔥 ② 연도별 최고기온과 최저기온")

st.write(
    "각 연도에서 관측된 가장 높은 기온과 "
    "가장 낮은 기온을 비교합니다."
)

yearly_temp = (
    df.groupby("연도")
    .agg(
        최고기온=("최고기온(℃)", "max"),
        최저기온=("최저기온(℃)", "min")
    )
    .reset_index()
)

fig2 = go.Figure()

# 최고기온: 네온 핫핑크
add_neon_line(
    fig2,
    yearly_temp["연도"],
    yearly_temp["최고기온"],
    "연도별 최고기온",
    "#ff1493",
    pink_glow
)

# 최저기온: 네온 파란색
add_neon_line(
    fig2,
    yearly_temp["연도"],
    yearly_temp["최저기온"],
    "연도별 최저기온",
    "#00bfff",
    blue_glow
)

style_graph(
    fig2,
    "연도별 최고기온과 최저기온",
    "연도"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()


# ==========================================
# 13. 그래프 3
# 두 연도의 기온 비교
# ==========================================

st.header("📊 ③ 두 연도의 기온 비교")

st.write(
    "비교할 연도 두 개를 선택하면 "
    "각 연도의 1월부터 12월까지 평균기온을 비교합니다."
)

available_years = sorted(
    df["연도"].dropna().unique().tolist()
)

if len(available_years) < 2:

    st.warning("비교할 연도가 2개 이상 필요합니다.")

    st.stop()


# 기본값: 가장 최근의 두 연도
default_years = available_years[-2:]

selected_years = st.multiselect(
    "비교할 연도 2개를 선택하세요.",
    options=available_years,
    default=default_years,
    max_selections=2,
    format_func=lambda x: f"{int(x)}년"
)

if len(selected_years) != 2:

    st.info("비교 그래프를 보려면 연도를 정확히 2개 선택하세요.")

else:

    selected_years = sorted(selected_years)

    compare_df = df[
        df["연도"].isin(selected_years)
    ].copy()

    fig3 = go.Figure()

    colors = [
        "#ff1493",
        "#00bfff"
    ]

    glows = [
        pink_glow,
        blue_glow
    ]

    for i, year in enumerate(selected_years):

        year_data = (
            compare_df[
                compare_df["연도"] == year
            ]
            .groupby("월")["평균기온(℃)"]
            .mean()
            .reindex(range(1, 13))
        )

        add_neon_line(
            fig3,
            month_names,
            year_data.values,
            f"{int(year)}년 평균기온",
            colors[i],
            glows[i]
        )

    style_graph(
        fig3,
        f"{int(selected_years[0])}년과 {int(selected_years[1])}년 기온 비교",
        "월"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# ==========================================
# 14. 선택 연도 데이터 표
# ==========================================

    st.subheader("📋 선택한 두 연도의 월별 평균기온")

    comparison_table = compare_df.pivot_table(
        index="월",
        columns="연도",
        values="평균기온(℃)",
        aggfunc="mean"
    ).reindex(range(1, 13))

    comparison_table.index = month_names

    comparison_table.columns = [
        f"{int(year)}년"
        for year in comparison_table.columns
    ]

    st.dataframe(
        comparison_table.round(1),
        use_container_width=True
    )


# ==========================================
# 15. 데이터 정보
# ==========================================

st.divider()

st.subheader("📌 데이터 분석 정보")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "전체 데이터 개수",
        f"{len(df):,}개"
    )

with col2:

    st.metric(
        "데이터 시작 연도",
        f"{int(df['연도'].min())}년"
    )

with col3:

    st.metric(
        "데이터 마지막 연도",
        f"{int(df['연도'].max())}년"
    )

st.caption(
    "※ 월별 평균기온은 전체 관측 기간의 해당 월 평균입니다. "
    "연도별 최고·최저기온은 해당 연도의 월별 관측값 중 "
    "가장 높은 최고기온과 가장 낮은 최저기온입니다. "
    "결측치는 계산에서 제외됩니다."
)
