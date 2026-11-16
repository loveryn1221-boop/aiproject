
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# ==========================================
# 1. 페이지 기본 설정
# ==========================================

st.set_page_config(
    page_title="Bloom AI - 붓꽃 예측",
    page_icon="🌸",
    layout="wide"
)

# ==========================================
# 2. 봄 느낌 핑크 테마 CSS
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
    background: #ffffff;
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

.stButton button:hover {
    background: #dc4b91;
    color: white;
}

div[data-baseweb="select"] {
    border-color: #ffacd0;
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
st.subheader("봄바람처럼 산뜻하게, AI가 붓꽃의 품종을 찾아줄게!")

st.markdown("""
꽃잎의 길이와 너비를 입력해 봐!
인공지능이 어떤 붓꽃인지 예측해 줄 거야. 🌷
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
        "CSV 파일을 프로젝트에 업로드해 줘."
    )
    st.stop()

try:
    try:
        df = pd.read_csv(csv_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

except Exception as e:
    st.error(f"데이터 파일을 읽지 못했어: {e}")
    st.stop()


# 필요한 열 확인
required_columns = [
    "꽃잎 길이",
    "꽃잎 너비",
    "품종"
]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일의 열 이름을 확인해 줘.")
    st.stop()

df = df.dropna(subset=required_columns).copy()

df["꽃잎 길이"] = pd.to_numeric(
    df["꽃잎 길이"], errors="coerce"
)

df["꽃잎 너비"] = pd.to_numeric(
    df["꽃잎 너비"], errors="coerce"
)

df = df.dropna(subset=["꽃잎 길이", "꽃잎 너비"])


# ==========================================
# 5. 학습 데이터와 AI 모델 만들기
# ==========================================

X = df[["꽃잎 길이", "꽃잎 너비"]]
y = df["품종"]

# SVM + 표준화
model = make_pipeline(
    StandardScaler(),
    SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale"
    )
)

# 전체 데이터 학습
model.fit(X, y)


# ==========================================
# 6. 입력 범위 계산
# ==========================================

petal_length_min = float(df["꽃잎 길이"].min())
petal_length_max = float(df["꽃잎 길이"].max())

petal_width_min = float(df["꽃잎 너비"].min())
petal_width_max = float(df["꽃잎 너비"].max())


st.markdown("## 🌷 나의 붓꽃 정보 입력하기")

st.info("""
📌 입력 범위는 업로드한 Iris 데이터의 실제 최솟값과 최댓값을 기준으로 해.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌸 꽃잎 길이")

    st.caption(
        f"입력 가능 범위: "
        f"{petal_length_min:.1f} ~ "
        f"{petal_length_max:.1f} cm"
    )

    petal_length = st.slider(
        "꽃잎 길이(cm)",
        min_value=petal_length_min,
        max_value=petal_length_max,
        value=3.0,
        step=0.1
    )

with col2:
    st.markdown("### 🌸 꽃잎 너비")

    st.caption(
        f"입력 가능 범위: "
        f"{petal_width_min:.1f} ~ "
        f"{petal_width_max:.1f} cm"
    )

    petal_width = st.slider(
        "꽃잎 너비(cm)",
        min_value=petal_width_min,
        max_value=petal_width_max,
        value=1.0,
        step=0.1
    )


# ==========================================
# 7. 품종 예측
# ==========================================

st.divider()

st.markdown("## 🌺 AI 품종 예측 결과")

input_data = pd.DataFrame(
    [[petal_length, petal_width]],
    columns=["꽃잎 길이", "꽃잎 너비"]
)

prediction = model.predict(input_data)[0]

# 품종 한글 이름
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
    f"🌸 AI가 예측한 품종은 "
    f"**{korean_name}** 이야!"
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
        "예측 품종",
        prediction.replace("Iris-", "")
    )


# ==========================================
# 8. 입력값 그래프
# ==========================================

st.divider()

st.markdown("## ⭐ 나의 붓꽃 위치 확인하기")

st.write("""
가로축은 꽃잎 길이, 세로축은 꽃잎 너비야.
핑크색 별표가 네가 입력한 꽃의 위치를 나타내!
""")

# 실제 데이터 그래프
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
    hover_data=["품종"],
    labels={
        "꽃잎 길이": "꽃잎 길이 (cm)",
        "꽃잎 너비": "꽃잎 너비 (cm)",
        "품종": "붓꽃 품종"
    }
)

# 사용자가 입력한 값: 핑크 별표
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
                color="#FFFFFF",
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
# 9. 마무리
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
        작은 꽃잎의 차이로도 품종을 구분할 수 있다니 신기하지?
    </p>
    <p style="font-size:25px;">
        🌷 🌸 🌺 🌸 🌷
    </p>
</div>
""", unsafe_allow_html=True)
