
import streamlit as st
import pandas as pd
from pathlib import Path

# =====================================
# 1. 페이지 설정
# =====================================
st.set_page_config(
    page_title="맞춤형 음식 추천",
    page_icon="🍓",
    layout="wide"
)

# =====================================
# 2. 디자인
# =====================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff0f5, #fff8fc, #ffe4ec);
}

h1, h2, h3 {
    color: #d63384;
}

.stButton > button {
    background-color: #ff69a4;
    color: white;
    border-radius: 12px;
    border: none;
    height: 55px;
    font-size: 20px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #e64980;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 3. CSV 파일 불러오기
# =====================================
@st.cache_data
def load_data():

    current_dir = Path(__file__).resolve().parent

    possible_paths = [
        current_dir.parent / "nutrition.csv",
        current_dir / "nutrition.csv",
        Path.cwd() / "nutrition.csv"
    ]

    csv_path = None

    for path in possible_paths:
        if path.exists():
            csv_path = path
            break

    if csv_path is None:
        st.error("nutrition.csv 파일을 찾을 수 없습니다.")
        st.stop()

    data = None

    for encoding in ["utf-8-sig", "utf-8", "cp949"]:
        try:
            data = pd.read_csv(csv_path, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    if data is None:
        st.error("CSV 파일을 읽을 수 없습니다.")
        st.stop()

    required_columns = [
        "label",
        "weight",
        "calories",
        "protein",
        "fats",
        "carbohydrates"
    ]

    if not all(col in data.columns for col in required_columns):
        st.error("CSV 파일의 열 이름을 확인해 주세요.")
        st.stop()

    for col in required_columns[1:]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=required_columns)

    return data


df = load_data()

# =====================================
# 4. 제목
# =====================================
st.title("🍓 나만의 맞춤형 음식 추천!")

st.markdown("""
### 💗 원하는 영양 성분을 선택해 보세요!

내가 원하는 칼로리와 영양 성분에 맞는 음식을 찾아드릴게요.
4가지 조건을 모두 선택하고 추천 버튼을 눌러보세요!
""")

st.divider()

# =====================================
# 5. 선택 범위 설정
# =====================================
calorie_options = [
    f"{i} ~ {i+100}"
    for i in range(0, 1000, 100)
]

protein_options = [
    f"{i} ~ {i+20}"
    for i in range(0, 60, 20)
]

fat_options = [
    f"{i} ~ {i+20}"
    for i in range(0, 100, 20)
]

carb_options = [
    f"{i} ~ {i+20}"
    for i in range(0, 100, 20)
]

# =====================================
# 6. 사용자 선택 화면
# =====================================
st.subheader("🔥 1. 원하는 칼로리")

calorie_choice = st.selectbox(
    "칼로리 범위를 선택하세요.",
    calorie_options,
    key="calorie"
)

st.subheader("💪 2. 원하는 단백질 함량")

protein_choice = st.selectbox(
    "단백질 범위를 선택하세요.",
    protein_options,
    key="protein"
)

st.subheader("🥑 3. 원하는 지방 함량")

fat_choice = st.selectbox(
    "지방 범위를 선택하세요.",
    fat_options,
    key="fat"
)

st.subheader("🍞 4. 원하는 탄수화물 함량")

carb_choice = st.selectbox(
    "탄수화물 범위를 선택하세요.",
    carb_options,
    key="carbohydrates"
)

# =====================================
# 7. 선택 범위 숫자 변환
# =====================================
def get_range(choice):
    start, end = choice.split(" ~ ")
    return int(start), int(end)


cal_min, cal_max = get_range(calorie_choice)
pro_min, pro_max = get_range(protein_choice)
fat_min, fat_max = get_range(fat_choice)
carb_min, carb_max = get_range(carb_choice)

st.divider()

# =====================================
# 8. 선택 조건 확인
# =====================================
st.subheader("📝 내가 선택한 영양 성분")

col1, col2 = st.columns(2)

with col1:
    st.info(f"🔥 칼로리: {cal_min} ~ {cal_max} kcal")
    st.info(f"💪 단백질: {pro_min} ~ {pro_max} g")

with col2:
    st.info(f"🥑 지방: {fat_min} ~ {fat_max} g")
    st.info(f"🍞 탄수화물: {carb_min} ~ {carb_max} g")

# =====================================
# 9. 음식 추천
# =====================================
if st.button("🍓 내 맞춤 음식 추천받기!", use_container_width=True):

    result = df[
        (df["calories"] >= cal_min) &
        (df["calories"] < cal_max) &
        (df["protein"] >= pro_min) &
        (df["protein"] < pro_max) &
        (df["fats"] >= fat_min) &
        (df["fats"] < fat_max) &
        (df["carbohydrates"] >= carb_min) &
        (df["carbohydrates"] < carb_max)
    ].copy()

    st.divider()
    st.header("🎀 나에게 맞는 음식 추천 결과")

    if not result.empty:

        result["음식 이름"] = (
            result["label"]
            .astype(str)
            .str.replace("_", " ", regex=False)
            .str.title()
        )

        result = result.sort_values(
            by="calories"
        )

        st.success(
            f"🎉 총 {len(result)}개의 음식을 찾았어요!"
        )

        # 음식별 정보 출력
        for _, row in result.iterrows():

            with st.container(border=True):

                st.subheader(f"🍽️ {row['음식 이름']}")

                st.write(f"⚖️ 섭취량: {row['weight']} g")

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "🔥 칼로리",
                    f"{row['calories']} kcal"
                )

                c2.metric(
                    "💪 단백질",
                    f"{row['protein']} g"
                )

                c3.metric(
                    "🥑 지방",
                    f"{row['fats']} g"
                )

                c4.metric(
                    "🍞 탄수화물",
                    f"{row['carbohydrates']} g"
                )

        # 전체 추천 결과 표
        st.divider()
        st.subheader("📊 추천 음식 전체 목록")

        display_df = result[
            [
                "음식 이름",
                "weight",
                "calories",
                "protein",
                "fats",
                "carbohydrates"
            ]
        ].rename(columns={
            "weight": "섭취량(g)",
            "calories": "칼로리(kcal)",
            "protein": "단백질(g)",
            "fats": "지방(g)",
            "carbohydrates": "탄수화물(g)"
        })

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "😢 선택한 네 가지 조건에 모두 맞는 음식이 없어요!"
        )

        st.info(
            "영양 성분 범위를 조금 변경해서 다시 검색해 보세요."
        )

# =====================================
# 10. 하단 안내
# =====================================
st.divider()

st.caption(
    "💗 본 음식 추천 결과는 nutrition.csv 데이터에 기반합니다."
)
