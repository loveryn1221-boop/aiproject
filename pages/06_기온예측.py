
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from sklearn.linear_model import LinearRegression
from pathlib import Path

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="서울 기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 미래 기온 예측")
st.write(
    "과거 기온 데이터를 분석하고 "
    "선형회귀 알고리즘으로 미래 기온을 예측해 봐요!"
)

st.divider()

# ==========================================
# 2. 한글 폰트 설정
# ==========================================
font_candidates = [
    "Malgun Gothic",
    "NanumGothic",
    "AppleGothic"
]

available_fonts = {
    f.name for f in fm.fontManager.ttflist
}

for font in font_candidates:
    if font in available_fonts:
        plt.rcParams["font.family"] = font
        break

plt.rcParams["axes.unicode_minus"] = False

# ==========================================
# 3. CSV 파일 경로 설정
# ==========================================
# 현재 파일은 pages 폴더 아래에 있고
# CSV 파일은 그 상위 폴더에 있음

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "temperature.csv"

# CSV 파일 불러오기
if not CSV_PATH.exists():
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.write(f"확인한 파일 경로: {CSV_PATH}")
    st.stop()

try:
    df = pd.read_csv(
        CSV_PATH,
        encoding="cp949"
    )
except UnicodeDecodeError:
    try:
        df = pd.read_csv(
            CSV_PATH,
            encoding="utf-8-sig"
        )
    except Exception as e:
        st.error(f"CSV 파일 읽기 오류: {e}")
        st.stop()

# ==========================================
# 4. 데이터 확인 및 전처리
# ==========================================
required_columns = [
    "일시",
    "평균기온(℃)"
]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 열 이름을 확인해주세요.")
    st.write(df.columns.tolist())
    st.stop()

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

def parse_date(value):
    try:
        parts = str(value).strip().split("-")

        if len(parts) != 2:
            return pd.Series([np.nan, np.nan])

        month_name = parts[0].strip().title()
        year = int(parts[1].strip())

        month = month_dict.get(month_name)

        if month is None:
            return pd.Series([np.nan, np.nan])

        if year < 100:
            year = 2000 + year if year <= 26 else 1900 + year

        return pd.Series([year, month])

    except (ValueError, TypeError):
        return pd.Series([np.nan, np.nan])


df[["연도", "월"]] = df["일시"].apply(parse_date)

df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"],
    errors="coerce"
)

df = df.dropna(
    subset=["연도", "월", "평균기온(℃)"]
).copy()

df["연도"] = df["연도"].astype(int)
df["월"] = df["월"].astype(int)

df = df.sort_values("연도")

if df.empty:
    st.error("분석할 수 있는 데이터가 없습니다.")
    st.stop()

# ==========================================
# 5. 사용자 입력
# ==========================================
st.subheader("📌 예측 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "🌱 예측할 월을 선택하세요.",
        range(1, 13),
        format_func=lambda x: f"{x}월"
    )

with col2:
    last_year = int(df["연도"].max())

    prediction_year = st.number_input(
        "🔮 예측할 연도를 입력하세요.",
        min_value=last_year + 1,
        max_value=2100,
        value=max(2030, last_year + 1),
        step=1
    )

prediction_year = int(prediction_year)

# ==========================================
# 6. 선택한 월 데이터 추출
# ==========================================
month_df = df[
    df["월"] == selected_month
].copy()

month_df = month_df.sort_values("연도")

if len(month_df) < 2:
    st.warning("선택한 월의 데이터가 부족합니다.")
    st.stop()

X = month_df[["연도"]]
y = month_df["평균기온(℃)"]

# ==========================================
# 7. 선형회귀 학습
# ==========================================
model = LinearRegression()

model.fit(X, y)

# 과거 데이터의 회귀 예측값
month_df["회귀 예측기온"] = model.predict(X)

# 미래 기온 예측
future_X = pd.DataFrame({
    "연도": [prediction_year]
})

predicted_temp = model.predict(future_X)[0]

# 회귀식
slope = model.coef_[0]
intercept = model.intercept_

# 결정계수
r2 = model.score(X, y)

# ==========================================
# 8. 예측 결과
# ==========================================
st.divider()
st.subheader("🔮 미래 기온 예측 결과")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "예측 연도",
        f"{prediction_year}년"
    )

with col2:
    st.metric(
        f"{selected_month}월 예측 평균기온",
        f"{predicted_temp:.1f}℃"
    )

with col3:
    st.metric(
        "결정계수 R²",
        f"{r2:.3f}"
    )

st.success(
    f"🌡️ {prediction_year}년 {selected_month}월의 "
    f"예상 평균기온은 {predicted_temp:.1f}℃입니다!"
)

# ==========================================
# 9. 그래프 그리기
# ==========================================
st.divider()

st.subheader(
    f"📈 {selected_month}월 과거 기온과 미래 예측"
)

start_year = int(month_df["연도"].min())

line_X = pd.DataFrame({
    "연도": np.linspace(
        start_year,
        prediction_year,
        300
    )
})

line_y = model.predict(line_X)

fig, ax = plt.subplots(figsize=(13, 6))

# 실제 과거 데이터
ax.scatter(
    month_df["연도"],
    month_df["평균기온(℃)"],
    color="#ff4b8b",
    s=65,
    label="실제 평균기온",
    zorder=3
)

# 선형회귀 직선
ax.plot(
    line_X["연도"],
    line_y,
    color="#2471e8",
    linewidth=2.5,
    label="선형회귀 직선"
)

# 실제 데이터와 회귀선 사이의 오차
for _, row in month_df.iterrows():
    ax.plot(
        [row["연도"], row["연도"]],
        [
            row["평균기온(℃)"],
            row["회귀 예측기온"]
        ],
        color="gray",
        linestyle=":",
        alpha=0.6
    )

# 미래 예측값
ax.scatter(
    prediction_year,
    predicted_temp,
    color="#16a085",
    marker="*",
    s=220,
    edgecolors="black",
    label="미래 예측 기온",
    zorder=5
)

ax.annotate(
    f"{prediction_year}년\n{predicted_temp:.1f}℃",
    xy=(prediction_year, predicted_temp),
    xytext=(10, 15),
    textcoords="offset points",
    fontsize=11,
    color="#087f5b",
    fontweight="bold"
)

ax.set_title(
    f"{selected_month}월 평균기온 선형회귀 분석",
    fontsize=17
)

ax.set_xlabel("연도")
ax.set_ylabel("평균기온 (℃)")

ax.grid(
    True,
    linestyle="--",
    alpha=0.35
)

ax.legend()

fig.tight_layout()

st.pyplot(fig)

# ==========================================
# 10. 회귀식 설명
# ==========================================
st.subheader("🧮 선형회귀 분석 결과")

st.write("컴퓨터가 과거 데이터를 학습하여 만든 회귀식입니다.")

st.latex(
    rf"\hat{{y}} = {slope:.4f}x + ({intercept:.4f})"
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "기울기",
        f"{slope:.4f}"
    )

with col2:
    st.metric(
        "절편",
        f"{intercept:.4f}"
    )

if slope > 0:
    st.info(
        f"📈 매년 평균적으로 약 {slope:.3f}℃ "
        "상승하는 장기 추세가 나타납니다."
    )
elif slope < 0:
    st.info(
        f"📉 매년 평균적으로 약 {abs(slope):.3f}℃ "
        "하락하는 장기 추세가 나타납니다."
    )
else:
    st.info("기온의 장기적인 변화 추세가 거의 없습니다.")

# ==========================================
# 11. 선형회귀 알고리즘 설명
# ==========================================
st.divider()

st.subheader("📚 선형회귀 알고리즘 알아보기")

st.markdown("""
### ① 선형회귀란?

선형회귀(Linear Regression)는 과거 데이터를 분석해서
데이터의 관계를 가장 잘 나타내는 직선을 찾고,
그 직선을 이용해 미래의 값을 예측하는 알고리즘입니다.

### ② 알고리즘 작동 과정

**1단계: 데이터 수집**

temperature.csv에서 선택한 월의 과거 평균기온을 가져옵니다.

**2단계: 데이터 학습**

- X축: 연도
- Y축: 평균기온

컴퓨터는 연도와 기온 사이의 관계를 학습합니다.

**3단계: 최적의 직선 찾기**

실제 데이터와 직선 사이의 오차 제곱합이
가장 작아지는 직선을 찾습니다.

**4단계: 미래 기온 예측**

사용자가 입력한 미래 연도를 회귀식에 넣어
예상 평균기온을 계산합니다.

### ③ 그래프 읽는 방법

- 🔴 분홍색 점: 실제 과거 평균기온
- 🔵 파란색 직선: 컴퓨터가 학습한 회귀 직선
- 🟢 초록색 별: 미래 예측 평균기온
- 회색 점선: 실제 기온과 회귀 직선 사이의 오차

### ④ 결정계수(R²)란?

결정계수는 회귀모델이 과거 데이터의 변화를
얼마나 잘 설명하는지 나타내는 값입니다.

- 1에 가까울수록 과거 데이터에 잘 맞습니다.
- 0에 가까울수록 과거 데이터의 변화를 잘 설명하지 못합니다.

### ⑤ 주의할 점

실제 기온은 기후변화, 계절적 특성,
자연적인 기온 변동 등 여러 요인의 영향을 받습니다.

따라서 선형회귀의 예측값은 실제 미래 기온을
보장하는 값이 아니라 과거의 추세를 바탕으로 계산한
통계적 추정값입니다.
""")

# ==========================================
# 12. 과거 데이터 확인
# ==========================================
st.divider()

with st.expander("📋 과거 기온 데이터 확인하기"):

    display_df = month_df[
        ["연도", "평균기온(℃)", "회귀 예측기온"]
    ].copy()

    display_df.columns = [
        "연도",
        "실제 평균기온(℃)",
        "회귀 예측기온(℃)"
    ]

    st.dataframe(
        display_df.round(2),
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "🌱 temperature.csv 데이터를 이용한 "
    "선형회귀 기반 기온 예측 프로그램"
)
