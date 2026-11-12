
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="서울 미래 기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 미래 기온 예측")
st.write(
    "과거 기온 데이터를 활용하여 "
    "3가지 머신러닝 회귀 알고리즘의 예측 결과를 비교해 봐요!"
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
# 3. CSV 파일 불러오기
# ==========================================
# 현재 py 파일은 pages 폴더
# CSV 파일은 상위 폴더

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "temperature.csv"

if not CSV_PATH.exists():
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.write(f"확인한 경로: {CSV_PATH}")
    st.stop()

try:
    try:
        df = pd.read_csv(CSV_PATH, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

except Exception as e:
    st.error(f"CSV 파일 읽기 오류: {e}")
    st.stop()

# ==========================================
# 4. 데이터 전처리
# ==========================================
required_columns = ["일시", "평균기온(℃)"]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 열 이름을 확인해주세요.")
    st.write(df.columns.tolist())
    st.stop()

month_dict = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
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
# 6. 알고리즘 선택
# ==========================================
st.subheader("🤖 회귀 알고리즘 선택")

algorithm_names = [
    "선형회귀",
    "다항회귀",
    "랜덤 포레스트 회귀"
]

selected_algorithm = st.radio(
    "그래프에서 강조할 알고리즘을 선택하세요.",
    algorithm_names,
    horizontal=True
)

# ==========================================
# 7. 선택한 월의 데이터 추출
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
# 8. 세 가지 회귀 알고리즘 학습
# ==========================================

# ① 선형회귀
linear_model = LinearRegression()
linear_model.fit(X, y)

# ② 다항회귀 (2차 곡선)
polynomial_model = make_pipeline(
    PolynomialFeatures(degree=2),
    LinearRegression()
)

polynomial_model.fit(X, y)

# ③ 랜덤 포레스트 회귀
random_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=5,
    min_samples_leaf=2,
    random_state=42
)

random_model.fit(X, y)

models = {
    "선형회귀": linear_model,
    "다항회귀": polynomial_model,
    "랜덤 포레스트 회귀": random_model
}

# ==========================================
# 9. 세 가지 알고리즘의 미래 기온 예측
# ==========================================
future_X = pd.DataFrame({
    "연도": [prediction_year]
})

predictions = {}

scores = {}

for name, model in models.items():

    predictions[name] = float(
        model.predict(future_X)[0]
    )

    scores[name] = float(
        model.score(X, y)
    )

# ==========================================
# 10. 선택한 알고리즘 결과
# ==========================================
selected_model = models[selected_algorithm]

selected_prediction = predictions[selected_algorithm]

selected_score = scores[selected_algorithm]

st.divider()

st.subheader("🔮 선택한 알고리즘의 예측 결과")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "선택한 알고리즘",
        selected_algorithm
    )

with col2:
    st.metric(
        "예측 연도",
        f"{prediction_year}년"
    )

with col3:
    st.metric(
        f"{selected_month}월 예측 평균기온",
        f"{selected_prediction:.2f}℃"
    )

st.success(
    f"🌡️ {prediction_year}년 {selected_month}월의 "
    f"예상 평균기온은 {selected_prediction:.2f}℃입니다!"
)

# ==========================================
# 11. 세 가지 알고리즘 결과 비교
# ==========================================
st.divider()

st.subheader("🏆 세 가지 알고리즘 예측 결과 비교")

st.write(
    "같은 월과 같은 예측 연도를 기준으로 "
    "각 알고리즘이 계산한 기온을 비교해 보세요."
)

comparison_df = pd.DataFrame({
    "알고리즘": list(predictions.keys()),
    "예측 평균기온(℃)": list(predictions.values()),
    "결정계수(R²)": [
        scores[name] for name in predictions.keys()
    ]
})

comparison_df["선택 여부"] = comparison_df["알고리즘"].apply(
    lambda x: "⭐ 선택됨" if x == selected_algorithm else ""
)

st.dataframe(
    comparison_df.style.format({
        "예측 평균기온(℃)": "{:.2f}",
        "결정계수(R²)": "{:.3f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 12. 예측 기온 비교 막대그래프
# ==========================================
st.subheader("📊 알고리즘별 예측 기온 비교")

fig2, ax2 = plt.subplots(figsize=(10, 5))

names = list(predictions.keys())
values = list(predictions.values())

bar_colors = [
    "#ff4b8b",
    "#ff9ac2",
    "#2471e8"
]

bars = ax2.bar(
    names,
    values,
    color=bar_colors,
    width=0.55
)

for bar, value in zip(bars, values):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.2f}℃",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

# 선택된 알고리즘 강조
selected_index = names.index(selected_algorithm)

bars[selected_index].set_edgecolor("black")
bars[selected_index].set_linewidth(3)

ax2.set_title(
    f"{prediction_year}년 {selected_month}월 알고리즘별 예측 비교",
    fontsize=14
)

ax2.set_ylabel("예측 평균기온 (℃)")
ax2.grid(axis="y", linestyle="--", alpha=0.3)

fig2.tight_layout()
st.pyplot(fig2)

# ==========================================
# 13. 알고리즘별 회귀 그래프
# ==========================================
st.divider()

st.subheader("📈 알고리즘 작동 과정 비교")

st.write(
    "분홍색 점은 실제 기온이고, "
    "각 선은 알고리즘이 학습한 예측 결과입니다. "
    "선택한 알고리즘은 굵은 선으로 강조됩니다."
)

start_year = int(month_df["연도"].min())

line_X = pd.DataFrame({
    "연도": np.linspace(
        start_year,
        prediction_year,
        400
    )
})

fig, ax = plt.subplots(figsize=(13, 6))

# 실제 기온 데이터
ax.scatter(
    month_df["연도"],
    month_df["평균기온(℃)"],
    color="#ff4b8b",
    s=65,
    label="실제 평균기온",
    zorder=5
)

colors = {
    "선형회귀": "#2471e8",
    "다항회귀": "#f39c12",
    "랜덤 포레스트 회귀": "#16a085"
}

for name, model in models.items():

    line_y = model.predict(line_X)

    is_selected = (name == selected_algorithm)

    ax.plot(
        line_X["연도"],
        line_y,
        color=colors[name],
        linewidth=4 if is_selected else 1.8,
        alpha=1.0 if is_selected else 0.65,
        linestyle="-" if is_selected else "--",
        label=(
            f"{name} (선택)"
            if is_selected
            else name
        )
    )

# 미래 예측점
for name, value in predictions.items():

    is_selected = (name == selected_algorithm)

    ax.scatter(
        prediction_year,
        value,
        color=colors[name],
        marker="*",
        s=240 if is_selected else 110,
        edgecolors="black" if is_selected else "none",
        linewidths=1.2,
        zorder=6,
        label=f"{name} 예측값"
    )

ax.set_title(
    f"{selected_month}월 기온 회귀 알고리즘 비교",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("연도")
ax.set_ylabel("평균기온 (℃)")

ax.grid(
    True,
    linestyle="--",
    alpha=0.35
)

ax.legend(
    fontsize=9,
    loc="best"
)

fig.tight_layout()

st.pyplot(fig)

# ==========================================
# 14. 알고리즘별 예측 차이 설명
# ==========================================
st.subheader("🔍 알고리즘별 예측값 차이")

max_name = max(predictions, key=predictions.get)
min_name = min(predictions, key=predictions.get)

difference = (
    predictions[max_name] - predictions[min_name]
)

st.info(
    f"가장 높은 예측값은 {max_name}의 "
    f"{predictions[max_name]:.2f}℃이고, "
    f"가장 낮은 예측값은 {min_name}의 "
    f"{predictions[min_name]:.2f}℃입니다."
)

st.write(
    f"세 알고리즘의 예측 기온 차이는 "
    f"약 {difference:.2f}℃입니다."
)

# ==========================================
# 15. 선택한 알고리즘의 회귀식
# ==========================================
st.divider()

st.subheader("🧮 선택한 알고리즘의 분석 결과")

if selected_algorithm == "선형회귀":

    slope = linear_model.coef_[0]
    intercept = linear_model.intercept_

    st.latex(
        rf"\hat{{y}} = {slope:.4f}x + ({intercept:.4f})"
    )

    st.write(f"기울기: {slope:.4f}")
    st.write(f"절편: {intercept:.4f}")

    st.write(
        "선형회귀는 과거 데이터에 가장 잘 맞는 "
        "직선 형태의 관계를 찾아 예측합니다."
    )

elif selected_algorithm == "다항회귀":

    regression = polynomial_model.named_steps["linearregression"]

    coefficients = regression.coef_
    intercept = regression.intercept_

    st.latex(
        rf"\hat{{y}} = {coefficients[2]:.6f}x^2 "
        rf"+ ({coefficients[1]:.4f})x "
        rf"+ ({intercept:.4f})"
    )

    st.write(
        "다항회귀는 2차 함수를 이용해 "
        "곡선 형태의 기온 변화를 학습합니다."
    )

else:

    st.write(
        "랜덤 포레스트는 여러 결정트리의 예측을 "
        "평균하여 최종 기온을 계산합니다."
    )

    st.write(
        "하나의 직선을 찾는 대신 여러 트리의 "
        "학습 결과를 결합하는 방식입니다."
    )

st.metric(
    "선택한 알고리즘의 학습 결정계수(R²)",
    f"{selected_score:.3f}"
)

# ==========================================
# 16. 알고리즘 설명
# ==========================================
st.divider()

st.subheader("📚 세 가지 회귀 알고리즘 알아보기")

with st.expander("① 선형회귀 (Linear Regression)"):

    st.markdown("""
    **어떤 알고리즘인가요?**

    과거 데이터의 관계를 가장 잘 나타내는
    직선 하나를 찾아 예측하는 방법입니다.

    **작동 원리**

    1. 연도와 평균기온 데이터를 수집합니다.
    2. 실제 기온과 직선 사이의 오차를 계산합니다.
    3. 오차 제곱합이 최소가 되는 직선을 찾습니다.
    4. 미래 연도를 직선에 대입해 기온을 예측합니다.

    **그래프 특징**

    - 파란색 직선으로 표현됩니다.
    - 전체적인 상승 또는 하락 추세를 확인하기 좋습니다.

    **수학 공식**

    y = ax + b
    """)

with st.expander("② 다항회귀 (Polynomial Regression)"):

    st.markdown("""
    **어떤 알고리즘인가요?**

    직선 대신 곡선 형태로 데이터의 관계를
    표현하여 예측하는 방법입니다.

    이번 프로그램에서는 2차 다항회귀를 사용합니다.

    **작동 원리**

    1. 과거 연도와 기온 데이터를 수집합니다.
    2. 연도를 제곱한 항목도 추가합니다.
    3. 실제 데이터에 가장 잘 맞는 곡선을 찾습니다.
    4. 미래 연도를 곡선에 대입해 예측합니다.

    **그래프 특징**

    - 주황색 곡선으로 표현됩니다.
    - 직선으로 표현하기 어려운 굴곡을 학습할 수 있습니다.

    **수학 공식**

    y = ax² + bx + c
    """)

with st.expander("③ 랜덤 포레스트 회귀 (Random Forest Regression)"):

    st.markdown("""
    **어떤 알고리즘인가요?**

    여러 개의 결정트리를 만들고
    각각의 예측 결과를 평균하여 최종 값을 구하는 방법입니다.

    **작동 원리**

    1. 여러 개의 학습용 데이터 표본을 만듭니다.
    2. 각각의 표본으로 여러 결정트리를 학습합니다.
    3. 각 트리가 예측한 값을 계산합니다.
    4. 여러 트리의 예측값을 평균하여 최종 결과를 만듭니다.

    **그래프 특징**

    - 초록색 계단 형태의 그래프가 나타날 수 있습니다.
    - 복잡한 비선형 관계를 학습할 수 있습니다.

    **주의할 점**

    랜덤 포레스트는 과거 데이터의 범위를 넘어서는
    미래 추세를 직선처럼 연장하지 못합니다.
    따라서 먼 미래를 예측할 때는 주의해야 합니다.
    """)

# ==========================================
# 17. 결정계수 설명
# ==========================================
st.subheader("📖 결정계수(R²) 비교하기")

st.write("""
결정계수는 모델이 학습에 사용한 과거 데이터를
얼마나 잘 설명하는지 나타내는 지표입니다.

- 1에 가까울수록 과거 데이터에 잘 맞습니다.
- 0에 가까울수록 과거 데이터의 변화를 잘 설명하지 못합니다.
- 음수가 나올 수도 있습니다.

단, 학습 데이터의 결정계수가 높다고 해서
미래 예측도 정확하다는 의미는 아닙니다.
""")

score_df = pd.DataFrame({
    "알고리즘": list(scores.keys()),
    "학습 결정계수(R²)": list(scores.values())
})

st.dataframe(
    score_df.style.format({
        "학습 결정계수(R²)": "{:.4f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 18. 실제 기온 데이터 확인
# ==========================================
st.divider()

with st.expander("📋 과거 기온 데이터 확인하기"):

    st.dataframe(
        month_df[
            ["연도", "월", "평균기온(℃)"]
        ],
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "🌱 temperature.csv 기반 기온 예측 프로그램"
)
