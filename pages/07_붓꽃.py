
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from collections import Counter

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
# 2. 더욱 핑크핑크한 봄 테마
# ==========================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #ffd1e5, transparent 35%),
        radial-gradient(circle at 90% 30%, #ffb8da, transparent 35%),
        linear-gradient(135deg, #fff0f8, #ffe0ef, #fff5fa);
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
}

h1 {
    color: #e60073 !important;
    font-weight: 900 !important;
}

h2, h3 {
    color: #e83e91 !important;
}

p, label {
    color: #75405f;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.85);
    border: 2px solid #ff9dcc;
    border-radius: 18px;
    padding: 15px;
    box-shadow: 0 5px 15px rgba(255,80,160,0.12);
}

.stButton button {
    background: linear-gradient(
        90deg,
        #ff65ad,
        #ed1681
    );
    color: white;
    border: none;
    border-radius: 20px;
    font-weight: bold;
}

.stButton button:hover {
    background: #d90070;
    color: white;
}

div[data-testid="stTabs"] button {
    color: #d41475;
    font-weight: bold;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    background: #ffcae2;
    border-radius: 12px;
}

div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.75);
    border: 1px solid #ffb0d4;
    border-radius: 15px;
}

div[data-testid="stAlert"] {
    border-radius: 15px;
}

@keyframes falling {
    0% {
        transform: translate3d(0, -10vh, 0) rotate(0deg);
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    50% {
        transform: translate3d(45px, 50vh, 0) rotate(180deg);
        opacity: 1;
    }

    100% {
        transform: translate3d(-30px, 110vh, 0) rotate(450deg);
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
    animation-name: falling;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
    filter: drop-shadow(0 2px 5px rgba(230,0,115,0.2));
}

</style>

<div class="flower-petals">
    <span style="left:2%;font-size:24px;animation-duration:6s;">🌸</span>
    <span style="left:7%;font-size:19px;animation-duration:8s;animation-delay:1s;">🌺</span>
    <span style="left:12%;font-size:28px;animation-duration:5s;animation-delay:2s;">🌸</span>
    <span style="left:17%;font-size:18px;animation-duration:7s;animation-delay:1s;">🌷</span>
    <span style="left:22%;font-size:25px;animation-duration:6s;animation-delay:3s;">🌸</span>
    <span style="left:27%;font-size:20px;animation-duration:5s;animation-delay:2s;">🌺</span>
    <span style="left:32%;font-size:27px;animation-duration:8s;animation-delay:1s;">🌸</span>
    <span style="left:37%;font-size:19px;animation-duration:6s;animation-delay:4s;">🌷</span>
    <span style="left:42%;font-size:25px;animation-duration:5s;animation-delay:2s;">🌸</span>
    <span style="left:47%;font-size:21px;animation-duration:7s;animation-delay:3s;">🌺</span>
    <span style="left:52%;font-size:28px;animation-duration:6s;">🌸</span>
    <span style="left:57%;font-size:18px;animation-duration:5s;animation-delay:2s;">🌷</span>
    <span style="left:62%;font-size:25px;animation-duration:8s;animation-delay:3s;">🌸</span>
    <span style="left:67%;font-size:20px;animation-duration:6s;animation-delay:1s;">🌺</span>
    <span style="left:72%;font-size:27px;animation-duration:5s;animation-delay:2s;">🌸</span>
    <span style="left:77%;font-size:19px;animation-duration:7s;animation-delay:4s;">🌷</span>
    <span style="left:82%;font-size:25px;animation-duration:6s;animation-delay:1s;">🌸</span>
    <span style="left:87%;font-size:22px;animation-duration:5s;animation-delay:3s;">🌺</span>
    <span style="left:92%;font-size:28px;animation-duration:8s;animation-delay:2s;">🌸</span>
    <span style="left:97%;font-size:19px;animation-duration:6s;animation-delay:4s;">🌷</span>
    <span style="left:4%;font-size:16px;animation-duration:5s;animation-delay:3s;">🌸</span>
    <span style="left:35%;font-size:17px;animation-duration:7s;animation-delay:2s;">🌸</span>
    <span style="left:65%;font-size:18px;animation-duration:6s;animation-delay:3s;">🌺</span>
    <span style="left:90%;font-size:17px;animation-duration:5s;animation-delay:1s;">🌸</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 3. 제목
# ==========================================

st.title("🌸 BLOOM AI : 나의 붓꽃 찾기")

st.markdown("""
<div style="
    background:linear-gradient(100deg,#ffb4d5,#ff6eaf,#ed1681);
    padding:20px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 5px 18px rgba(230,0,115,0.18);
">
    <h2 style="color:white !important;">
        🌷 AI와 함께하는 핑크빛 꽃의 세계 🌷
    </h2>
    <p style="color:white;font-size:17px;">
        꽃의 길이와 너비를 입력하면
        세 가지 인공지능이 품종을 예측해 줘!
    </p>
    <p style="font-size:25px;">
        🌸 🌺 🌷 🌸 🌺 🌷 🌸
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")


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
    st.error("Iris.csv 파일을 찾을 수 없어!")
    st.stop()


# 인코딩 확인
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
    st.error("CSV 파일 인코딩을 확인해 줘.")
    st.stop()


# ==========================================
# 5. 데이터 전처리
# ==========================================

required_columns = [
    "꽃받침 길이",
    "꽃받침 너비",
    "꽃잎 길이",
    "꽃잎 너비",
    "품종"
]

if not all(
    col in df.columns
    for col in required_columns
):
    st.error(
        "CSV 파일의 열 이름이 올바르지 않아. "
        "원본 Iris.csv 파일을 확인해 줘."
    )
    st.stop()

for col in required_columns[:4]:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

df = df.dropna(
    subset=required_columns
).copy()

if len(df) < 5:
    st.error("학습 데이터가 부족해.")
    st.stop()

if df["품종"].nunique() < 2:
    st.error("두 종류 이상의 품종 데이터가 필요해.")
    st.stop()


# ==========================================
# 6. 품종 이름
# ==========================================

species_names = {
    "Iris-setosa": "아이리스 세토사 🌼",
    "Iris-versicolor": "아이리스 버시컬러 🌷",
    "Iris-virginica": "아이리스 버지니카 🌸"
}


def korean_species(name):
    return species_names.get(name, str(name))


# ==========================================
# 7. 알고리즘 설명
# ==========================================

algorithm_info = {

    "SVM": {
        "name": "서포트 벡터 머신 (SVM)",
        "emoji": "📐",
        "principle": """
**작동 원리**

1. 입력된 꽃의 길이와 너비를 확인해.
2. 각 품종의 데이터를 가장 잘 구분하는 경계를 찾아.
3. 품종 사이의 간격이 최대가 되도록 경계를 결정해.
4. 새로운 꽃이 어느 영역에 속하는지 판단해.

**핵심:** 데이터를 구분하는 최적의 경계선을 찾는 알고리즘이야.

**특징**
- RBF 커널로 복잡한 경계를 학습할 수 있어.
- 데이터 표준화를 함께 사용해.
"""
    },

    "Random Forest": {
        "name": "랜덤 포레스트 (Random Forest)",
        "emoji": "🌳",
        "principle": """
**작동 원리**

1. 학습 데이터에서 여러 표본을 무작위로 선택해.
2. 각각의 표본으로 의사결정나무를 학습시켜.
3. 여러 나무가 각각 꽃의 품종을 예측해.
4. 가장 많은 표를 받은 품종을 최종 결과로 결정해.

**핵심:** 여러 의사결정나무가 함께 판단하는 알고리즘이야.

**특징**
- 100개의 의사결정나무를 사용해.
- 각 나무의 예측을 모아 다수결로 결정해.
"""
    },

    "KNN": {
        "name": "K-최근접 이웃 (KNN)",
        "emoji": "🌷",
        "principle": """
**작동 원리**

1. 새로운 꽃의 길이와 너비를 확인해.
2. 기존 꽃 데이터와의 거리를 계산해.
3. 가장 가까운 데이터 5개를 찾아.
4. 가장 많이 등장하는 품종을 예측해.

**핵심:** 가까운 이웃들의 품종을 참고하는 알고리즘이야.

**특징**
- 주변 데이터의 영향을 받아.
- 가장 가까운 5개의 데이터를 활용해.
- 거리 계산을 위해 표준화를 적용해.
"""
    }

}


# ==========================================
# 8. 알고리즘 3개 만들기
# ==========================================

def create_models():

    return {

        "SVM": make_pipeline(
            StandardScaler(),
            SVC(
                kernel="rbf",
                C=1.0,
                gamma="scale"
            )
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ),

        "KNN": make_pipeline(
            StandardScaler(),
            KNeighborsClassifier(
                n_neighbors=5
            )
        )

    }


# ==========================================
# 9. 예측 및 그래프를 만드는 함수
# ==========================================

def prediction_section(
    feature1,
    feature2,
    title,
    description,
    default1,
    default2
):

    st.markdown(f"## {title}")

    st.write(description)

    # 입력 범위
    min1 = float(df[feature1].min())
    max1 = float(df[feature1].max())

    min2 = float(df[feature2].min())
    max2 = float(df[feature2].max())

    st.info(
        f"""
        🌸 {feature1} 입력 범위:
        {min1:.1f} ~ {max1:.1f} cm

        🌸 {feature2} 입력 범위:
        {min2:.1f} ~ {max2:.1f} cm
        """
    )

    # 입력 화면
    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"### 🌺 {feature1}")

        value1 = st.slider(
            f"{feature1} (cm)",
            min_value=min1,
            max_value=max1,
            value=float(default1),
            step=0.1,
            key=f"{feature1}_slider"
        )

    with col2:

        st.markdown(f"### 🌺 {feature2}")

        value2 = st.slider(
            f"{feature2} (cm)",
            min_value=min2,
            max_value=max2,
            value=float(default2),
            step=0.1,
            key=f"{feature2}_slider"
        )

    st.divider()

    # 학습 데이터
    X = df[[feature1, feature2]]
    y = df["품종"]

    # 입력 데이터
    input_data = pd.DataFrame(
        [[value1, value2]],
        columns=[feature1, feature2]
    )

    # 세 가지 알고리즘 모두 예측
    models = create_models()

    predictions = {}

    for model_key, model in models.items():

        model.fit(X, y)

        predictions[model_key] = model.predict(
            input_data
        )[0]

    # ======================================
    # 10. 세 알고리즘 결과 비교
    # ======================================

    st.markdown("## 🏆 AI 예측 결과 비교")

    st.write(
        "같은 꽃의 입력값으로 세 가지 알고리즘이 "
        "각각 어떤 품종을 예측하는지 비교해 봐!"
    )

    result_cols = st.columns(3)

    for i, (model_key, prediction) in enumerate(
        predictions.items()
    ):

        with result_cols[i]:

            st.markdown(
                f"### {algorithm_info[model_key]['emoji']}"
            )

            st.caption(
                algorithm_info[model_key]["name"]
            )

            st.success(
                f"**{korean_species(prediction)}**"
            )

    # 결과 비교표
    comparison = pd.DataFrame({
        "알고리즘": [
            "SVM",
            "Random Forest",
            "KNN"
        ],
        "예측 품종": [
            korean_species(predictions["SVM"]),
            korean_species(predictions["Random Forest"]),
            korean_species(predictions["KNN"])
        ],
        "예측 결과": [
            predictions["SVM"],
            predictions["Random Forest"],
            predictions["KNN"]
        ]
    })

    st.markdown("### 📊 알고리즘별 예측 비교표")

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    # 다수결
    counts = Counter(predictions.values())

    max_votes = max(counts.values())

    winners = [
        name for name, count in counts.items()
        if count == max_votes
    ]

    st.markdown("### 👑 최종 다수결 결과")

    if len(winners) == 1:

        winner = winners[0]

        st.success(
            f"""
            🌸 세 알고리즘 중 {max_votes}개가
            **{korean_species(winner)}**으로 예측했어!
            """
        )

    else:

        st.warning(
            "세 알고리즘의 예측 결과가 동률이야. "
            "하나의 최종 품종으로 결정하지 않았어."
        )

    # ======================================
    # 11. 입력값 그래프
    # ======================================

    st.divider()

    st.markdown("## ⭐ 나의 꽃 위치 그래프")

    st.write(
        f"""
        가로축: {feature1}

        세로축: {feature2}

        핑크색 별표가 네가 입력한 꽃의 위치야!
        """
    )

    fig = px.scatter(
        df,
        x=feature1,
        y=feature2,
        color="품종",
        color_discrete_sequence=[
            "#FF9ACB",
            "#F45CA8",
            "#C83E91"
        ],
        opacity=0.7,
        labels={
            feature1: f"{feature1} (cm)",
            feature2: f"{feature2} (cm)",
            "품종": "붓꽃 품종"
        }
    )

    # 입력한 위치 별표
    fig.add_trace(
        go.Scatter(
            x=[value1],
            y=[value2],
            mode="markers+text",
            name="내가 입력한 꽃 ⭐",
            marker=dict(
                symbol="star",
                size=27,
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
        title=f"🌸 {feature1}과 {feature2} 비교",
        xaxis_title=f"{feature1} (cm)",
        yaxis_title=f"{feature2} (cm)",
        plot_bgcolor="#FFF5FA",
        paper_bgcolor="#FFEAF4",
        font=dict(
            color="#8A2858",
            size=13
        ),
        legend_title="붓꽃 품종",
        height=550
    )

    fig.update_xaxes(
        gridcolor="#FFC5DE"
    )

    fig.update_yaxes(
        gridcolor="#FFC5DE"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ======================================
    # 12. 그래프 아래 알고리즘 원리
    # ======================================

    st.divider()

    st.markdown("## 📚 AI 알고리즘 작동 원리")

    st.write(
        "각 알고리즘이 어떤 방식으로 품종을 예측했는지 알아보자!"
    )

    for model_key, info in algorithm_info.items():

        prediction = predictions[model_key]

        with st.expander(
            f"{info['emoji']} {info['name']} "
            f"- 예측: {korean_species(prediction)}",
            expanded=False
        ):

            st.markdown(
                info["principle"]
            )

    # 현재 탭의 입력값
    st.divider()

    st.markdown("### 💗 내가 입력한 꽃 정보")

    m1, m2 = st.columns(2)

    with m1:
        st.metric(
            feature1,
            f"{value1:.1f} cm"
        )

    with m2:
        st.metric(
            feature2,
            f"{value2:.1f} cm"
        )


# ==========================================
# 13. 데이터 소개
# ==========================================

st.divider()

st.markdown("## 🌷 붓꽃 데이터 소개")

info1, info2, info3 = st.columns(3)

with info1:
    st.metric(
        "전체 데이터",
        f"{len(df)}개"
    )

with info2:
    st.metric(
        "붓꽃 품종",
        f"{df['품종'].nunique()}종"
    )

with info3:
    st.metric(
        "예측 알고리즘",
        "3개"
    )


# ==========================================
# 14. 탭 구성
# ==========================================

st.divider()

st.markdown("## 🌸 어떤 부분을 측정할까?")

st.write(
    "꽃잎 또는 꽃받침을 선택해서 품종을 예측해 봐!"
)

tab1, tab2 = st.tabs([
    "🌸 꽃잎으로 예측하기",
    "🌷 꽃받침으로 예측하기"
])


# ==========================================
# 탭 1: 꽃잎
# ==========================================

with tab1:

    prediction_section(
        feature1="꽃잎 길이",
        feature2="꽃잎 너비",
        title="🌸 꽃잎으로 붓꽃 품종 예측하기",
        description="""
        꽃잎의 길이와 너비를 입력하면
        세 가지 AI 알고리즘이 품종을 예측해 줘!
        """,
        default1=3.0,
        default2=1.0
    )


# ==========================================
# 탭 2: 꽃받침
# ==========================================

with tab2:

    prediction_section(
        feature1="꽃받침 길이",
        feature2="꽃받침 너비",
        title="🌷 꽃받침으로 붓꽃 품종 예측하기",
        description="""
        이번에는 꽃받침의 길이와 너비만 사용해 볼 거야!

        꽃잎을 사용했을 때와 예측 결과가 어떻게 다른지 비교해 봐!
        """,
        default1=5.5,
        default2=3.0
    )


# ==========================================
# 15. 마무리 화면
# ==========================================

st.divider()

st.markdown("""
<div style="
    background:linear-gradient(
        100deg,
        #ffacd1,
        #ff70b5,
        #ed1681
    );
    padding:30px;
    border-radius:25px;
    text-align:center;
    box-shadow:0 5px 20px rgba(230,0,115,0.2);
">

    <h1 style="color:white !important;">
        🌸 BLOOM AI 🌸
    </h1>

    <h3 style="color:white !important;">
        오늘도 핑크빛 꽃처럼 아름다운 하루!
    </h3>

    <p style="color:white;font-size:18px;">
        세 가지 AI 알고리즘과 함께
        붓꽃의 비밀을 찾아봤어!
    </p>

    <p style="font-size:32px;">
        🌷 🌸 🌺 🌸 🌷
    </p>

</div>
""", unsafe_allow_html=True)
