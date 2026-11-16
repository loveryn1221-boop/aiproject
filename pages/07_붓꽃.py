
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier


# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="Bloom AI - 나의 붓꽃 찾기",
    page_icon="🌸",
    layout="wide"
)


# ==========================================
# 2. 핑크 봄 테마 CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #fff0f6,
        #fff8fb,
        #ffe6f0
    );
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #d94f91 !important;
}

p, label {
    color: #75465e;
}

div[data-testid="stMetric"] {
    background: white;
    border: 2px solid #ffc4dc;
    border-radius: 15px;
    padding: 15px;
}

.stButton button {
    background: linear-gradient(
        90deg,
        #ff91bd,
        #e95d9e
    );
    color: white;
    border: none;
    border-radius: 20px;
    font-weight: bold;
}

@keyframes falling {
    0% {
        transform: translateY(-10vh) rotate(0deg);
        opacity: 0;
    }

    15% {
        opacity: 1;
    }

    100% {
        transform: translateY(110vh) rotate(360deg);
        opacity: 0;
    }
}

.flower-petals {
    position: fixed;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
}

.flower-petals span {
    position: absolute;
    top: -10%;
    font-size: 23px;
    animation: falling linear infinite;
}

</style>

<div class="flower-petals">
    <span style="left:5%;animation-duration:13s;">🌸</span>
    <span style="left:18%;animation-duration:17s;animation-delay:3s;">🌷</span>
    <span style="left:30%;animation-duration:15s;animation-delay:5s;">🌸</span>
    <span style="left:45%;animation-duration:19s;animation-delay:1s;">🌺</span>
    <span style="left:58%;animation-duration:14s;animation-delay:4s;">🌸</span>
    <span style="left:72%;animation-duration:18s;animation-delay:2s;">🌷</span>
    <span style="left:85%;animation-duration:16s;animation-delay:6s;">🌸</span>
    <span style="left:95%;animation-duration:20s;animation-delay:3s;">🌺</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 3. 제목
# ==========================================

st.title("🌸 Bloom AI : 나의 붓꽃 찾기")

st.subheader(
    "봄바람처럼 산뜻하게, AI가 붓꽃의 품종을 찾아줄게!"
)

st.markdown("""
꽃잎의 길이와 너비를 입력하고
인공지능 알고리즘을 선택해 봐!

어떤 붓꽃인지 AI가 예측해 줄 거야. 🌷
""")

st.divider()


# ==========================================
# 4. CSV 파일 불러오기
# ==========================================

base_dir = Path(__file__).resolve().parent

file_candidates = [
    base_dir / "Iris.csv",
    base_dir.parent / "Iris.csv",
    base_dir / "Iris(2).csv",
    base_dir.parent / "Iris(2).csv"
]

csv_path = next(
    (p for p in file_candidates if p.exists()),
    None
)

if csv_path is None:
    st.error(
        "Iris.csv 파일을 찾을 수 없어! "
        "GitHub에 CSV 파일을 업로드해 줘."
    )
    st.stop()


# 한글 인코딩 자동 확인
df = None

for encoding in ["cp949", "utf-8-sig", "utf-8"]:
    try:
        df = pd.read_csv(
            csv_path,
            encoding=encoding
        )
        break
    except UnicodeDecodeError:
        continue

if df is None:
    st.error("CSV 파일의 인코딩을 확인해 줘.")
    st.stop()


# ==========================================
# 5. 데이터 전처리
# ==========================================

required_columns = [
    "꽃잎 길이",
    "꽃잎 너비",
    "품종"
]

if not all(
    col in df.columns
    for col in required_columns
):
    st.error(
        "CSV 파일의 열 이름을 확인해 줘."
    )
    st.stop()

df["꽃잎 길이"] = pd.to_numeric(
    df["꽃잎 길이"],
    errors="coerce"
)

df["꽃잎 너비"] = pd.to_numeric(
    df["꽃잎 너비"],
    errors="coerce"
)

df = df.dropna(
    subset=required_columns
).copy()

if len(df) < 5:
    st.error("학습 데이터가 5개 이상 필요해.")
    st.stop()

X = df[
    ["꽃잎 길이", "꽃잎 너비"]
]

y = df["품종"]


# ==========================================
# 6. 알고리즘 3개 준비
# ==========================================

models = {

    "① 서포트 벡터 머신 (SVM)": make_pipeline(
        StandardScaler(),
        SVC(
            kernel="rbf",
            C=1.0,
            gamma="scale"
        )
    ),

    "② 랜덤 포레스트 (Random Forest)":
        RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ),

    "③ K-최근접 이웃 (KNN)": make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(
            n_neighbors=5
        )
    )

}


# ==========================================
# 7. 알고리즘 선택
# ==========================================

st.markdown("## 🤖 AI 알고리즘 선택하기")

st.write(
    "3가지 알고리즘 중 하나를 선택해 봐!"
)

selected_algorithm = st.selectbox(
    "예측 알고리즘 선택",
    list(models.keys())
)

model = models[selected_algorithm]

# 선택한 알고리즘 학습
model.fit(X, y)


# ==========================================
# 8. 입력 가능한 범위 계산
# ==========================================

length_min = float(
    df["꽃잎 길이"].min()
)

length_max = float(
    df["꽃잎 길이"].max()
)

width_min = float(
    df["꽃잎 너비"].min()
)

width_max = float(
    df["꽃잎 너비"].max()
)


# ==========================================
# 9. 사용자 입력
# ==========================================

st.divider()

st.markdown("## 🌷 나의 붓꽃 정보 입력하기")

st.info(
    f"""
    🌸 꽃잎 길이 입력 범위:
    {length_min:.1f} ~ {length_max:.1f} cm

    🌸 꽃잎 너비 입력 범위:
    {width_min:.1f} ~ {width_max:.1f} cm

    입력 범위는 업로드한 데이터의 실제 최솟값과 최댓값이야!
    """
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🌸 꽃잎 길이")

    petal_length = st.slider(
        "꽃잎 길이 (cm)",
        min_value=length_min,
        max_value=length_max,
        value=3.0,
        step=0.1
    )

with col2:

    st.markdown("### 🌸 꽃잎 너비")

    petal_width = st.slider(
        "꽃잎 너비 (cm)",
        min_value=width_min,
        max_value=width_max,
        value=1.0,
        step=0.1
    )


# ==========================================
# 10. 품종 예측
# ==========================================

st.divider()

st.markdown("## 🌺 AI 품종 예측 결과")

input_data = pd.DataFrame(
    [[petal_length, petal_width]],
    columns=[
        "꽃잎 길이",
        "꽃잎 너비"
    ]
)

prediction = model.predict(
    input_data
)[0]

species_names = {
    "Iris-setosa": "아이리스 세토사 🌼",
    "Iris-versicolor": "아이리스 버시컬러 🌷",
    "Iris-virginica": "아이리스 버지니카 🌸"
}

korean_name = species_names.get(
    prediction,
    prediction
)

st.success(
    f"🌸 AI 예측 결과: **{korean_name}**"
)

result1, result2, result3 = st.columns(3)

with result1:
    st.metric(
        "꽃잎 길이",
        f"{petal_length:.1f} cm"
    )

with result2:
    st.metric(
        "꽃잎 너비",
        f"{petal_width:.1f} cm"
    )

with result3:
    st.metric(
        "사용 알고리즘",
        selected_algorithm.split(" ")[0]
    )


# ==========================================
# 11. 그래프
# ==========================================

st.divider()

st.markdown(
    "## ⭐ 나의 붓꽃 위치 확인하기"
)

st.write("""
가로축은 꽃잎 길이, 세로축은 꽃잎 너비야.

핑크색 별표가 네가 입력한 꽃의 위치를 나타내!
""")

fig = px.scatter(
    df,
    x="꽃잎 길이",
    y="꽃잎 너비",
    color="품종",
    color_discrete_sequence=[
        "#F7A8C4",
        "#E88BB7",
        "#BD78A9"
    ],
    opacity=0.65,
    labels={
        "꽃잎 길이": "꽃잎 길이 (cm)",
        "꽃잎 너비": "꽃잎 너비 (cm)",
        "품종": "붓꽃 품종"
    }
)

# 사용자가 입력한 위치를 핑크색 별표로 표시
fig.add_trace(
    go.Scatter(
        x=[petal_length],
        y=[petal_width],
        mode="markers+text",
        name="내가 입력한 꽃 ⭐",
        marker=dict(
            symbol="star",
            size=25,
            color="#FF1493",
            line=dict(
                color="white",
                width=2
            )
        ),
        text=["나의 꽃 ⭐"],
        textposition="top center",
        textfont=dict(
            color="#D41475",
            size=14
        )
    )
)

fig.update_layout(
    title="🌸 꽃잎 길이와 너비 비교",
    xaxis_title="꽃잎 길이 (cm)",
    yaxis_title="꽃잎 너비 (cm)",
    plot_bgcolor="#FFF8FC",
    paper_bgcolor="#FFF0F6",
    font=dict(
        color="#75465E",
        size=13
    ),
    legend_title="붓꽃 품종",
    height=550
)

fig.update_xaxes(
    gridcolor="#F7D7E6"
)

fig.update_yaxes(
    gridcolor="#F7D7E6"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 12. 알고리즘 작동 원리 설명
# ==========================================

st.divider()

st.markdown(
    "## 📚 AI 알고리즘별 작동 원리"
)

st.write("""
세 가지 알고리즘은 데이터를 판단하는 방법이 서로 달라.

아래 설명을 읽으면서 차이점을 알아보자! 🌷
""")

algorithm_info = {

    "① 서포트 벡터 머신 (SVM)": {
        "emoji": "📐",
        "principle": """
### ⚙️ 작동 원리

1. 입력한 꽃잎 길이와 너비를 확인해.
2. 각 품종의 데이터를 구분하는 경계선을 찾아.
3. 품종 사이의 간격이 최대가 되도록 경계를 결정해.
4. 새로운 꽃이 어느 영역에 속하는지 판단해 품종을 예측해.

### ✨ 주요 특징

- 데이터 사이의 복잡한 경계도 구분할 수 있어.
- RBF 커널을 이용해 비선형적인 관계를 학습해.
- 표준화를 통해 측정값의 크기 차이를 보정해.

**핵심:** 데이터를 가장 잘 구분하는 경계면을 찾는 알고리즘이야.
"""
    },

    "② 랜덤 포레스트 (Random Forest)": {
        "emoji": "🌳",
        "principle": """
### ⚙️ 작동 원리

1. 학습 데이터에서 여러 표본을 무작위로 선택해.
2. 각각의 표본으로 의사결정나무를 학습시켜.
3. 여러 나무가 새로운 꽃의 품종을 각각 예측해.
4. 가장 많은 표를 얻은 품종을 최종 결과로 결정해.

### ✨ 주요 특징

- 여러 개의 의사결정나무를 사용해.
- 각각의 나무가 독립적으로 판단해.
- 다수결을 이용해 최종 품종을 결정해.

**핵심:** 여러 나무의 예측 결과를 모아서 판단하는 알고리즘이야.
"""
    },

    "③ K-최근접 이웃 (KNN)": {
        "emoji": "🌷",
        "principle": """
### ⚙️ 작동 원리

1. 새로운 꽃의 꽃잎 길이와 너비를 확인해.
2. 기존 데이터와의 거리를 계산해.
3. 가장 가까운 데이터 5개를 찾아.
4. 5개 중 가장 많이 등장하는 품종을 예측해.

### ✨ 주요 특징

- 주변 데이터의 영향을 받아 품종을 예측해.
- 가까운 데이터의 품종을 활용해.
- 이번 프로그램에서는 가장 가까운 5개를 기준으로 판단해.
- 거리 계산을 위해 표준화를 적용해.

**핵심:** 나와 가까운 이웃들이 어떤 품종인지 살펴보고 판단하는 알고리즘이야.
"""
    }

}


# 그래프 바로 아래에 세 알고리즘 설명 표시
for algorithm_name, info in algorithm_info.items():

    is_selected = (
        algorithm_name == selected_algorithm
    )

    if is_selected:
        title = f"⭐ {info['emoji']} {algorithm_name} (현재 선택됨)"
    else:
        title = f"{info['emoji']} {algorithm_name}"

    with st.expander(
        title,
        expanded=is_selected
    ):

        st.markdown(
            info["principle"]
        )


# ==========================================
# 13. 마무리
# ==========================================

st.divider()

st.markdown("""
<div style="
    background:linear-gradient(90deg,#ffe1ee,#fff1f7);
    padding:25px;
    border-radius:20px;
    text-align:center;
">
    <h2 style="color:#D94F91;">
        🌸 오늘의 꽃을 찾았어! 🌸
    </h2>

    <p style="color:#75465E;font-size:17px;">
        세 가지 인공지능 알고리즘으로
        붓꽃의 세계를 탐험해 봤어!
    </p>

    <p style="font-size:25px;">
        🌷 🌸 🌺 🌸 🌷
    </p>
</div>
""", unsafe_allow_html=True)

