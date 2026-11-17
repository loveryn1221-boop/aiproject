
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

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
    page_title="아이리스 플라워 예측 연구소",
    page_icon="🌸",
    layout="wide"
)


# ==========================================
# 2. 꽃잎 폭풍 애니메이션
# ==========================================

flower_emojis = [
    "🌸", "🌺", "🌷", "🌼",
    "💮", "🪷", "✿", "❀", "🌹"
]

flower_html = ""

for i in range(100):

    left = random.randint(0, 100)
    size = random.randint(16, 34)
    duration = random.uniform(2.5, 5.5)
    delay = random.uniform(0, 5.5)
    sway = random.randint(-180, 180)

    flower = random.choice(flower_emojis)

    flower_html += f"""
    <div class="flower"
         style="
            left:{left}%;
            font-size:{size}px;
            animation-duration:{duration}s;
            animation-delay:-{delay}s;
            --sway:{sway}px;
         ">
         {flower}
    </div>
    """


# ==========================================
# 3. 핑크 그라데이션 디자인
# ==========================================

st.markdown(f"""
<style>

/* 전체 배경 */
.stApp {{
    background:
        radial-gradient(
            circle at 10% 10%,
            #FFF0F8 0%,
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 20%,
            #FFC1E0 0%,
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #FFF0F5 0%,
            #FFD1E8 35%,
            #FFB6D9 70%,
            #FF8FC7 100%
        );

    background-attachment: fixed;
}}

/* 제목 */
h1 {{
    color: #D63384 !important;
    font-weight: 900 !important;
    text-shadow: 2px 2px 8px white;
}}

/* 소제목 */
h2, h3 {{
    color: #C21870 !important;
    font-weight: bold !important;
}}

/* 일반 글씨 */
p, label, .stMarkdown {{
    color: #71304F;
}}

/* 탭 */
button[data-baseweb="tab"] {{
    color: #C21870 !important;
    font-weight: bold;
}}

/* 선택 상자 */
div[data-baseweb="select"] {{
    background-color: #FFF5FA;
    border-radius: 12px;
}}

/* 입력 영역 */
div[data-testid="stNumberInput"],
div[data-testid="stSlider"] {{
    background-color: rgba(255,255,255,0.45);
    border-radius: 15px;
    padding: 8px;
}}

/* 결과 카드 */
div[data-testid="stMetric"] {{
    background: linear-gradient(
        135deg,
        #FFFFFF,
        #FFE0EF
    );
    border: 2px solid #FFB6D9;
    border-radius: 18px;
    padding: 15px;
    box-shadow: 0 5px 15px rgba(214, 51, 132, 0.15);
}}

/* 버튼 */
.stButton button {{
    background: linear-gradient(
        90deg,
        #FF69B4,
        #FF1493
    );
    color: white;
    border: none;
    border-radius: 15px;
    font-weight: bold;
}}

/* 표 */
div[data-testid="stDataFrame"] {{
    background-color: rgba(255,255,255,0.75);
    border-radius: 15px;
}}

/* 꽃잎 */
.flower {{
    position: fixed;
    top: -60px;
    z-index: 999;
    pointer-events: none;
    user-select: none;
    animation-name: flowerFall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
    will-change: transform;
    opacity: 0.9;
    filter: drop-shadow(
        0 2px 5px rgba(255,20,147,0.3)
    );
}}

/* 빠르게 휘날리는 효과 */
@keyframes flowerFall {{

    0% {{
        transform: translate3d(0, -60px, 0) rotate(0deg);
        opacity: 0;
    }}

    10% {{
        opacity: 1;
    }}

    50% {{
        transform: translate3d(var(--sway), 50vh, 0) rotate(360deg);
        opacity: 0.95;
    }}

    100% {{
        transform: translate3d(
            calc(var(--sway) * -1),
            110vh,
            0
        ) rotate(900deg);
        opacity: 0;
    }}
}}

</style>

{flower_html}

""", unsafe_allow_html=True)


# ==========================================
# 4. CSV 파일 불러오기
# ==========================================

@st.cache_data
def load_data():

    current_folder = Path(__file__).resolve().parent

    possible_paths = [
        current_folder / "Iris.csv",
        current_folder.parent / "Iris.csv",
        current_folder / "iris.csv",
        current_folder.parent / "iris.csv"
    ]

    file_path = None

    for path in possible_paths:
        if path.exists():
            file_path = path
            break

    if file_path is None:
        raise FileNotFoundError(
            "Iris.csv 파일을 찾을 수 없습니다. "
            "상위 폴더에 CSV 파일을 넣어주세요."
        )

    for encoding in ["cp949", "utf-8-sig", "utf-8"]:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError("CSV 파일의 인코딩을 확인해주세요.")


try:
    df = load_data()

except Exception as e:
    st.error(f"데이터 파일 오류: {e}")
    st.stop()


# ==========================================
# 5. 데이터 확인
# ==========================================

required_columns = [
    "꽃받침 길이",
    "꽃받침 너비",
    "꽃잎 길이",
    "꽃잎 너비",
    "품종"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "CSV 파일에 다음 열이 없습니다: "
        + ", ".join(missing_columns)
    )
    st.stop()

df = df.dropna(subset=required_columns).copy()

if len(df) < 5:
    st.error("예측을 위해 최소 5개 이상의 데이터가 필요합니다.")
    st.stop()

species_names = sorted(df["품종"].unique())


# ==========================================
# 6. 제목과 소개
# ==========================================

st.title("🌸 아이리스 플라워 예측 연구소 🌸")

st.markdown("""
### 💗 나만의 꽃을 입력하고 어떤 아이리스인지 알아보자!

꽃의 길이와 너비를 입력하면
세 가지 인공지능 알고리즘이 꽃의 품종을 예측해 줘.

🌷 작은 꽃 모양은 실제 데이터야!

🌺 커다란 꽃 이모지는 내가 입력한 데이터야!
""")

st.divider()


# ==========================================
# 7. 인공지능 알고리즘
# ==========================================

models = {
    "서포트 벡터 머신 (SVM)": make_pipeline(
        StandardScaler(),
        SVC(kernel="rbf")
    ),

    "랜덤 포레스트 (Random Forest)": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),

    "K-최근접 이웃 (KNN)": make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=5)
    )
}


# ==========================================
# 8. 예측 함수
# ==========================================

def prediction_section(x_col, y_col, tab_name):

    st.subheader(f"🌷 {tab_name}")

    st.write(
        f"선택한 꽃의 특성: **{x_col}**와 **{y_col}**"
    )

    col1, col2 = st.columns(2)

    with col1:

        x_min = float(df[x_col].min())
        x_max = float(df[x_col].max())

        x_value = st.slider(
            x_col,
            min_value=x_min,
            max_value=x_max,
            value=float(round((x_min + x_max) / 2, 1)),
            step=0.1
        )

    with col2:

        y_min = float(df[y_col].min())
        y_max = float(df[y_col].max())

        y_value = st.slider(
            y_col,
            min_value=y_min,
            max_value=y_max,
            value=float(round((y_min + y_max) / 2, 1)),
            step=0.1
        )

    st.markdown(
        f"### 🌺 내가 입력한 꽃: {x_value} / {y_value}"
    )

    # 학습 데이터
    X = df[[x_col, y_col]]
    y = df["품종"]

    input_data = pd.DataFrame(
        [[x_value, y_value]],
        columns=[x_col, y_col]
    )

    # 세 가지 알고리즘 예측
    predictions = {}

    for model_name, model in models.items():

        model.fit(X, y)

        prediction = model.predict(input_data)[0]

        predictions[model_name] = prediction

    # ======================================
    # 알고리즘별 예측 결과
    # ======================================

    st.markdown("## 💖 인공지능 예측 결과")

    result_columns = st.columns(3)

    for i, (model_name, prediction) in enumerate(
        predictions.items()
    ):

        with result_columns[i]:

            st.metric(
                label=model_name,
                value=str(prediction)
            )

    # ======================================
    # 다수결 결과
    # ======================================

    vote_result = pd.Series(
        list(predictions.values())
    ).value_counts()

    max_votes = vote_result.max()

    winners = sorted(
        vote_result[vote_result == max_votes].index.tolist()
    )

    st.markdown("### 🏆 최종 예측 결과")

    if len(winners) == 1:

        st.success(
            f"다수결 결과는 **{winners[0]}** 입니다! 🌺"
        )

    else:

        st.info(
            "공동 1위 결과: " + ", ".join(winners)
        )

    # ======================================
    # 꽃 그래프
    # ======================================

    st.markdown("## 🌸 아이리스 꽃 분포 그래프")

    fig = go.Figure()

    flower_colors = [
        "#FF1493",
        "#C71585",
        "#FF69B4"
    ]

    # 실제 데이터: 꽃 모양
    for i, species in enumerate(species_names):

        species_data = df[df["품종"] == species]

        fig.add_trace(
            go.Scatter(
                x=species_data[x_col],
                y=species_data[y_col],
                mode="text",
                name=str(species),
                text=["✿"] * len(species_data),
                textposition="middle center",
                textfont=dict(
                    size=19,
                    color=flower_colors[i % len(flower_colors)]
                ),
                customdata=species_data[["품종"]],
                hovertemplate=(
                    "<b>🌸 실제 꽃 데이터</b><br>"
                    + x_col + ": %{x}<br>"
                    + y_col + ": %{y}<br>"
                    + "품종: %{customdata[0]}"
                    + "<extra></extra>"
                )
            )
        )

    # 사용자 입력: 아름다운 꽃
    fig.add_trace(
        go.Scatter(
            x=[x_value],
            y=[y_value],
            mode="text",
            name="내가 입력한 꽃 🌺",
            text=["🌺"],
            textposition="top center",
            textfont=dict(
                size=38,
                color="#FF1493"
            ),
            hovertemplate=(
                "<b>🌺 내가 입력한 꽃</b><br>"
                + x_col + ": %{x}<br>"
                + y_col + ": %{y}"
                + "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=600,
        plot_bgcolor="rgba(255,255,255,0.72)",
        paper_bgcolor="rgba(255,255,255,0.0)",

        font=dict(
            family="Arial",
            color="#8B2252",
            size=13
        ),

        title=dict(
            text="🌷 실제 아이리스 데이터와 나의 꽃 비교",
            font=dict(
                size=21,
                color="#D63384"
            )
        ),

        legend=dict(
            bgcolor="rgba(255,255,255,0.65)",
            bordercolor="#FFB6D9",
            borderwidth=1
        ),

        margin=dict(
            l=40,
            r=30,
            t=80,
            b=50
        ),

        xaxis=dict(
            gridcolor="#F8C6DF",
            zerolinecolor="#F8C6DF"
        ),

        yaxis=dict(
            gridcolor="#F8C6DF",
            zerolinecolor="#F8C6DF"
        )
    )

    fig.update_traces(
        hoverlabel=dict(
            bgcolor="#FFF0F8",
            font_color="#C21870"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "🌸 작은 꽃 점은 실제 데이터이고, "
        "큰 꽃 이모지 🌺는 입력한 값이에요."
    )

    # ======================================
    # 알고리즘 설명
    # ======================================

    st.markdown("## 📚 인공지능 알고리즘 알아보기")

    with st.expander("🌸 1. 서포트 벡터 머신 (SVM)"):

        st.write("""
        SVM은 데이터를 가장 잘 구분할 수 있는 경계선을
        찾는 알고리즘이야.

        - 꽃의 특징을 바탕으로 품종을 구분해.
        - 데이터 사이의 경계를 잘 나누려고 해.
        - 복잡한 데이터 분류에도 활용할 수 있어.
        """)

    with st.expander("🌺 2. 랜덤 포레스트 (Random Forest)"):

        st.write("""
        랜덤 포레스트는 여러 개의 결정 트리를 만들어
        각각의 예측 결과를 모으는 알고리즘이야.

        - 여러 결정 트리의 결과를 종합해.
        - 다양한 분류 문제에 활용돼.
        - 여러 트리를 함께 사용해 예측해.
        """)

    with st.expander("🌷 3. K-최근접 이웃 (KNN)"):

        st.write("""
        KNN은 입력한 꽃과 가까운 데이터 5개를 찾아
        주변 데이터의 품종을 참고하는 알고리즘이야.

        - 입력한 꽃과 비슷한 데이터를 찾아.
        - 가까운 5개 데이터의 품종을 비교해.
        - 주변에서 가장 많이 나타나는 품종을 예측해.
        """)

    # ======================================
    # 결과 비교표
    # ======================================

    st.markdown("## 💗 알고리즘별 결과 비교")

    result_df = pd.DataFrame({
        "알고리즘": list(predictions.keys()),
        "예측 품종": list(predictions.values())
    })

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "💡 입력값을 조금씩 바꾸면서 "
        "세 알고리즘의 예측 결과가 어떻게 달라지는지 확인해 봐!"
    )


# ==========================================
# 9. 두 가지 예측 탭
# ==========================================

tab1, tab2 = st.tabs([
    "🌸 꽃잎으로 예측하기",
    "🌷 꽃받침으로 예측하기"
])

with tab1:

    prediction_section(
        "꽃잎 길이",
        "꽃잎 너비",
        "꽃잎 특성으로 품종 예측하기"
    )

with tab2:

    prediction_section(
        "꽃받침 길이",
        "꽃받침 너비",
        "꽃받침 특성으로 품종 예측하기"
    )


# ==========================================
# 10. 하단 디자인
# ==========================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    background:linear-gradient(
        90deg,
        #FFF0F5,
        #FFB6D9,
        #FF69B4,
        #FFB6D9,
        #FFF0F5
    );
    padding:25px;
    border-radius:22px;
    border:2px solid white;
    box-shadow:0 5px 20px rgba(214,51,132,0.2);
">
    <h3 style="color:#C21870;">
        🌸 오늘도 꽃처럼 반짝이는 하루! 🌸
    </h3>
    <p style="color:#9C2862;">
        AI와 함께 아이리스 꽃의 비밀을 찾아보자 💗
    </p>
</div>
""", unsafe_allow_html=True)
