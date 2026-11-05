
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.collections import LineCollection
from matplotlib import font_manager
from pathlib import Path
import numpy as np
import re

# 1. 페이지 설정
st.set_page_config(
    page_title="구리시 연령별 인구 분석",
    page_icon="🌈",
    layout="wide"
)

st.title("🌈 구리시 연령별 인구 분석")
st.write("행정구역, 성별, 연도를 선택하여 연령대별 인구를 확인해 보세요!")

# 2. 한글 폰트 설정
try:
    import koreanize_matplotlib
except ImportError:
    pass

available_fonts = {
    font.name for font in font_manager.fontManager.ttflist
}

for korean_font in [
    "NanumGothic",
    "NanumBarunGothic",
    "Malgun Gothic",
    "AppleGothic"
]:
    if korean_font in available_fonts:
        plt.rcParams["font.family"] = korean_font
        break

plt.rcParams["axes.unicode_minus"] = False

# 3. CSV 파일 불러오기
@st.cache_data
def load_population_data():

    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "population.csv"

    if not csv_path.exists():
        csv_path = base_dir.parent / "population.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            "population.csv 파일을 찾을 수 없습니다."
        )

    encodings = [
        "cp949",
        "euc-kr",
        "utf-8-sig",
        "utf-8"
    ]

    last_error = None

    for encoding in encodings:
        try:
            data = pd.read_csv(
                csv_path,
                encoding=encoding
            )
            return data
        except UnicodeDecodeError as error:
            last_error = error

    raise UnicodeError(
        f"CSV 인코딩 오류: {last_error}"
    )


try:
    df = load_population_data()

except Exception as error:
    st.error(f"데이터 파일 오류: {error}")
    st.stop()

# 4. 행정구역 이름 정리
if "행정구역" not in df.columns:
    st.error("'행정구역' 열을 찾을 수 없습니다.")
    st.stop()


def clean_region(value):

    name = str(value).strip()
    name = re.sub(r"\s*\(\d+\)\s*$", "", name)

    if name == "경기도 구리시":
        return "구리시 전체"

    prefix = "경기도 구리시 "

    if name.startswith(prefix):
        name = name[len(prefix):]

    return name


df["행정구역_표시"] = df["행정구역"].apply(
    clean_region
)

# 5. 선택 메뉴
st.subheader("🔎 분석 조건 선택")

col1, col2, col3 = st.columns(3)

with col1:
    region_options = df["행정구역_표시"].tolist()

    selected_region = st.selectbox(
        "행정구역",
        region_options
    )

with col2:
    gender_labels = {
        "전체": "계",
        "남성": "남",
        "여성": "여"
    }

    selected_gender_label = st.selectbox(
        "성별",
        list(gender_labels.keys())
    )

    selected_gender = gender_labels[
        selected_gender_label
    ]

with col3:
    selected_year = st.selectbox(
        "연도",
        [2020, 2021, 2022, 2023, 2024, 2025],
        index=5
    )

# 6. 연령대별 데이터 설정
age_groups = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]

selected_row = df.loc[
    df["행정구역_표시"] == selected_region
]

if selected_row.empty:
    st.error("선택한 행정구역 데이터가 없습니다.")
    st.stop()

selected_row = selected_row.iloc[0]

column_names = [
    f"{selected_year}년_{selected_gender}_{age}"
    for age in age_groups
]

missing_columns = [
    column for column in column_names
    if column not in df.columns
]

if missing_columns:
    st.error(
        "CSV에서 다음 열을 찾을 수 없습니다: "
        + ", ".join(missing_columns)
    )
    st.stop()

population_values = []

for column in column_names:

    value = str(
        selected_row[column]
    ).replace(",", "").strip()

    population_values.append(
        pd.to_numeric(value, errors="coerce")
    )

if pd.isna(pd.Series(population_values)).any():
    st.error("인구수 데이터에 잘못된 값이 있습니다.")
    st.stop()

population_values = np.array(
    population_values,
    dtype=float
)

# 7. 선택 결과 표시
total_population = int(population_values.sum())

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "선택 행정구역",
    selected_region
)

metric2.metric(
    "선택 성별",
    selected_gender_label
)

metric3.metric(
    "연령별 인구 합계",
    f"{total_population:,}명"
)

st.divider()

# 8. 무지개색 꺾은선 그래프
fig, ax = plt.subplots(figsize=(13, 6))

x = np.arange(len(age_groups))
y = population_values

# 꺾은선 구간 만들기
points = np.array([x, y]).T.reshape(-1, 1, 2)

segments = np.concatenate(
    [points[:-1], points[1:]],
    axis=1
)

# 무지개색 선 적용
rainbow_colors = plt.cm.rainbow(
    np.linspace(0, 1, len(segments))
)

line_collection = LineCollection(
    segments,
    colors=rainbow_colors,
    linewidths=3.5,
    capstyle="round"
)

ax.add_collection(line_collection)

# 무지개색 점 표시
point_colors = plt.cm.rainbow(
    np.linspace(0, 1, len(x))
)

ax.scatter(
    x,
    y,
    color=point_colors,
    s=65,
    edgecolors="white",
    linewidths=1.2,
    zorder=3
)

# 인구수 표시
for xi, yi in zip(x, y):

    ax.annotate(
        f"{int(yi):,}",
        (xi, yi),
        textcoords="offset points",
        xytext=(0, 9),
        ha="center",
        fontsize=8
    )

# 그래프 제목과 축 이름
ax.set_title(
    f"{selected_region} {selected_gender_label} 인구 - {selected_year}년",
    fontsize=17,
    pad=18
)

ax.set_xlabel(
    "나이 (연령대)",
    fontsize=12,
    labelpad=10
)

ax.set_ylabel(
    "인구수 (명)",
    fontsize=12,
    labelpad=10
)

# 가로축: 10살 단위
ax.set_xticks(x)
ax.set_xticklabels(age_groups)

# 세로축: 100명 단위
max_population = max(float(y.max()), 100)

upper_limit = int(
    np.ceil(max_population / 100) * 100
)

ax.set_ylim(0, upper_limit + 100)

ax.yaxis.set_major_locator(
    ticker.MultipleLocator(100)
)

ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(
        lambda value, position: f"{int(value):,}"
    )
)

# 가로축과 세로축 구분선
ax.grid(
    True,
    which="major",
    axis="both",
    linestyle="--",
    linewidth=0.6,
    alpha=0.45
)

ax.set_xlim(
    -0.3,
    len(age_groups) - 0.7
)

ax.set_axisbelow(True)

fig.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)

# 9. 연령대별 인구수 표
with st.expander("📋 연령대별 인구수 자세히 보기"):

    result_df = pd.DataFrame({
        "연령대": age_groups,
        "인구수": [
            f"{int(value):,}명"
            for value in population_values
        ]
    })

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "자료: population.csv | "
    "연령별 인구는 10살 단위로 집계되어 있습니다."
)
