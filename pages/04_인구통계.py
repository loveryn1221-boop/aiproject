
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path
import re

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="구리시 연령대별 인구 비교",
    page_icon="🌈",
    layout="wide"
)

st.title("🌈 구리시 연령대별 인구 비교")
st.write(
    "연도, 성별, 연령대를 선택하면 해당 연령대 인구가 "
    "많은 구리시 행정동을 순서대로 비교합니다."
)

# ==========================================
# 2. 한글 폰트 설정
# ==========================================

try:
    import koreanize_matplotlib
except Exception:
    st.warning(
        "한글 폰트를 불러오지 못했습니다. "
        "requirements.txt를 확인해 주세요."
    )

plt.rcParams["axes.unicode_minus"] = False

font_candidates = [
    "NanumGothic",
    "NanumBarunGothic",
    "Malgun Gothic",
    "AppleGothic"
]

installed_fonts = {
    font.name for font in fm.fontManager.ttflist
}

for font_name in font_candidates:
    if font_name in installed_fonts:
        plt.rcParams["font.family"] = font_name
        break

# ==========================================
# 3. CSV 파일 불러오기
# ==========================================

@st.cache_data
def load_data():

    folder = Path(__file__).resolve().parent
    csv_path = folder / "population.csv"

    if not csv_path.exists():
        csv_path = folder.parent / "population.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            "population.csv 파일을 찾지 못했습니다. "
            "app.py와 같은 폴더에 population.csv를 올려주세요."
        )

    for encoding in [
        "cp949",
        "euc-kr",
        "utf-8-sig",
        "utf-8"
    ]:
        try:
            data = pd.read_csv(
                csv_path,
                encoding=encoding
            )
            return data

        except UnicodeDecodeError:
            continue

    raise ValueError(
        "CSV 파일의 인코딩을 확인할 수 없습니다."
    )


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 파일 오류: {e}")
    st.stop()

# ==========================================
# 4. 행정구역 이름 정리
# ==========================================

if "행정구역" not in df.columns:
    st.error("'행정구역' 열이 없습니다.")
    st.stop()


def clean_region(value):

    name = str(value).strip()

    name = re.sub(
        r"\s*\(\d+\)\s*$",
        "",
        name
    )

    if name == "경기도 구리시":
        return "구리시 전체"

    prefix = "경기도 구리시 "

    if name.startswith(prefix):
        name = name[len(prefix):]

    return name


df["행정구역_표시"] = df["행정구역"].apply(
    clean_region
)

# 구리시 전체 합계는 제외하고 8개 동만 비교
dong_df = df[
    df["행정구역_표시"] != "구리시 전체"
].copy()

if dong_df.empty:
    st.error("비교할 행정동 데이터가 없습니다.")
    st.stop()

# ==========================================
# 5. 연도, 성별, 연령대 선택
# ==========================================

st.subheader("🔎 분석 조건 선택")

col1, col2, col3 = st.columns(3)

with col1:

    year = st.selectbox(
        "연도 선택",
        [2020, 2021, 2022, 2023, 2024, 2025],
        index=5
    )

with col2:

    gender_label = st.selectbox(
        "성별 선택",
        ["전체", "남성", "여성"]
    )

gender_code = {
    "전체": "계",
    "남성": "남",
    "여성": "여"
}[gender_label]

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

with col3:

    age_group = st.selectbox(
        "연령대 선택",
        age_groups
    )

# ==========================================
# 6. 선택 조건의 인구수 추출
# ==========================================

target_column = (
    f"{year}년_{gender_code}_{age_group}"
)

if target_column not in dong_df.columns:

    st.error(
        f"CSV에서 '{target_column}' 열을 찾을 수 없습니다."
    )

    st.stop()


def to_number(value):

    return pd.to_numeric(
        str(value).replace(",", "").strip(),
        errors="coerce"
    )


result = dong_df[
    ["행정구역_표시", target_column]
].copy()

result["인구수"] = result[target_column].apply(
    to_number
)

result = result.dropna(
    subset=["인구수"]
)

# 인구수가 많은 순서대로 정렬
result = result.sort_values(
    by="인구수",
    ascending=False
).reset_index(drop=True)

if result.empty:
    st.error("인구 데이터가 없습니다.")
    st.stop()

# ==========================================
# 7. 가장 인구가 많은 행정동 표시
# ==========================================

top_region = result.iloc[0]["행정구역_표시"]

top_population = int(
    result.iloc[0]["인구수"]
)

m1, m2, m3 = st.columns(3)

m1.metric(
    "선택 연도",
    f"{year}년"
)

m2.metric(
    "선택 연령대",
    age_group
)

m3.metric(
    "인구가 가장 많은 행정동",
    top_region,
    f"{top_population:,}명"
)

st.success(
    f"🏆 {year}년 {gender_label} {age_group} 인구가 "
    f"가장 많은 곳은 {top_region}이며, "
    f"{top_population:,}명입니다."
)

# ==========================================
# 8. 무지개 그라데이션 막대그래프
# ==========================================

st.subheader("🌈 행정동별 인구수 순위")

fig, ax = plt.subplots(figsize=(12, 7))

names = result["행정구역_표시"].tolist()

values = result["인구수"].astype(int).tolist()

bar_positions = np.arange(len(names))

bar_width = 0.62

# 투명한 막대 틀 생성
bars = ax.bar(
    bar_positions,
    values,
    width=bar_width,
    color="none",
    edgecolor="#444444",
    linewidth=0.8,
    zorder=3
)

# 무지개색 세로 그라데이션 생성
rainbow_gradient = np.linspace(
    0, 1, 256
).reshape(256, 1)

rainbow_gradient = np.repeat(
    rainbow_gradient,
    20,
    axis=1
)

# 각 막대 내부를 무지개 그라데이션으로 채우기
for bar in bars:

    x0 = bar.get_x()
    x1 = x0 + bar.get_width()

    y0 = 0
    y1 = bar.get_height()

    if y1 <= 0:
        continue

    gradient_image = ax.imshow(
        rainbow_gradient,
        extent=[x0, x1, y0, y1],
        origin="lower",
        aspect="auto",
        cmap="rainbow",
        interpolation="bicubic",
        zorder=2
    )

    # 그라데이션이 해당 막대 안에서만 보이도록 설정
    gradient_image.set_clip_path(bar)

# 막대 위에 인구수 표시
for position, value in zip(
    bar_positions,
    values
):

    ax.text(
        position,
        value,
        f"{value:,}명",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold"
    )

# 그래프 제목
ax.set_title(
    f"{year}년 {gender_label} {age_group} 행정동별 인구수",
    fontsize=17,
    pad=20
)

ax.set_xlabel(
    "행정구역",
    fontsize=12,
    labelpad=10
)

ax.set_ylabel(
    "인구수 (명)",
    fontsize=12,
    labelpad=10
)

ax.set_xticks(bar_positions)

ax.set_xticklabels(names)

# 세로축 눈금 간격 설정
max_value = max(values) if values else 100

if max_value > 5000:
    step = 1000
elif max_value > 1500:
    step = 500
else:
    step = 100

ax.yaxis.set_major_locator(
    ticker.MultipleLocator(step)
)

ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(
        lambda v, p: f"{int(v):,}"
    )
)

ax.set_ylim(
    0,
    max_value * 1.18 if max_value > 0 else 100
)

# 격자선
ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.35,
    zorder=0
)

ax.set_axisbelow(True)

fig.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)

# ==========================================
# 9. 행정동별 순위표
# ==========================================

with st.expander("📋 행정동별 인구수 순위표 보기"):

    display_result = result[
        ["행정구역_표시", "인구수"]
    ].copy()

    display_result.columns = [
        "행정구역",
        "인구수"
    ]

    display_result["인구수"] = (
        display_result["인구수"].astype(int)
    )

    display_result.index = range(
        1,
        len(display_result) + 1
    )

    display_result.index.name = "순위"

    st.dataframe(
        display_result,
        use_container_width=True
    )

st.caption(
    "자료: population.csv | "
    "구리시 전체 합계 행은 제외하고 실제 행정동 8곳을 비교합니다."
)
