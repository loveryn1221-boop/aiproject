
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# =========================================
# 1. 페이지 설정
# =========================================
st.set_page_config(
    page_title="나만의 음식 추천 🍽️",
    page_icon="🍓",
    layout="wide"
)

# =========================================
# 2. 음식 테마 디자인
# =========================================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 20%, #ffe0eb 0%, transparent 25%),
        radial-gradient(circle at 90% 30%, #fff0c9 0%, transparent 25%),
        radial-gradient(circle at 30% 90%, #ffe4d6 0%, transparent 30%),
        linear-gradient(135deg, #fff8f0, #fff0f5);
    background-attachment: fixed;
}

h1, h2, h3 {
    color: #d63384 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #ff69a4, #ff9a76);
    color: white;
    border-radius: 15px;
    border: none;
    height: 55px;
    font-size: 19px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #e64980, #ff805c);
    color: white;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: rgba(255,255,255,0.82);
    border-radius: 18px;
    border: 1px solid #ffd1df;
}

div[data-testid="stMetric"] {
    background: #fff3f7;
    padding: 12px;
    border-radius: 12px;
}

.emoji-banner {
    text-align: center;
    font-size: 36px;
    padding: 15px;
    background: rgba(255,255,255,0.65);
    border-radius: 20px;
    margin-bottom: 15px;
    letter-spacing: 8px;
}

.intro {
    text-align: center;
    color: #bd477b;
    font-size: 17px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 3. 음식 이름 한국어 사전
# =========================================
food_names = {
    "Cupcakes": "컵케이크",
    "Fish and Chips": "피시 앤 칩스",
    "Grilled Cheese": "그릴드 치즈 샌드위치",
    "Hot and Sour Soup": "새콤매콤 수프",
    "Lobster Roll": "랍스터 롤",
    "Macaroni and Cheese": "마카로니 치즈",
    "Shrimp and Grits": "새우와 그리츠",

    "apple_pie": "애플파이",
    "baby_back_ribs": "돼지 등갈비",
    "baklava": "바클라바",
    "beef_carpaccio": "소고기 카르파초",
    "beef_tartare": "소고기 타르타르",
    "beet_salad": "비트 샐러드",
    "beignets": "베녜",
    "bibimbap": "비빔밥",
    "bread_pudding": "브레드 푸딩",
    "breakfast_burrito": "브렉퍼스트 부리토",
    "bruschetta": "브루스케타",
    "caesar_salad": "시저 샐러드",
    "cannoli": "카놀리",
    "caprese_salad": "카프레제 샐러드",
    "carrot_cake": "당근 케이크",
    "ceviche": "세비체",
    "cheese_plate": "치즈 플래터",
    "cheesecake": "치즈케이크",
    "chicken_curry": "치킨 카레",
    "chicken_quesadilla": "치킨 케사디야",
    "chicken_wings": "치킨 윙",
    "chocolate_cake": "초콜릿 케이크",
    "chocolate_mousse": "초콜릿 무스",
    "churros": "츄러스",
    "clam_chowder": "클램 차우더",
    "club_sandwich": "클럽 샌드위치",
    "crab_cakes": "크랩 케이크",
    "creme_brulee": "크렘 브륄레",
    "croque_madame": "크로크 마담",
    "deviled_eggs": "데빌드 에그",
    "donuts": "도넛",
    "dumplings": "만두",
    "edamame": "에다마메",
    "eggs_benedict": "에그 베네딕트",
    "escargots": "에스카르고",
    "falafel": "팔라펠",
    "filet_mignon": "필레 미뇽",
    "foie_gras": "푸아그라",
    "french_fries": "감자튀김",
    "french_onion_soup": "프렌치 어니언 수프",
    "french_toast": "프렌치토스트",
    "fried_calamari": "오징어튀김",
    "fried_rice": "볶음밥",
    "frozen_yogurt": "프로즌 요거트",
    "garlic_bread": "마늘빵",
    "gnocchi": "뇨키",
    "greek_salad": "그릭 샐러드",
    "grilled_salmon": "구운 연어",
    "guacamole": "과카몰리",
    "gyoza": "교자",
    "hamburger": "햄버거",
    "hot_dog": "핫도그",
    "huevos_rancheros": "우에보스 란체로스",
    "hummus": "후무스",
    "ice_cream": "아이스크림",
    "lasagna": "라자냐",
    "lobster_bisque": "랍스터 비스크",
    "macarons": "마카롱",
    "miso_soup": "미소 된장국",
    "mussels": "홍합 요리",
    "nachos": "나초",
    "omelette": "오믈렛",
    "onion_rings": "어니언링",
    "oysters": "굴 요리",
    "pad_thai": "팟타이",
    "paella": "파에야",
    "pancakes": "팬케이크",
    "panna_cotta": "판나코타",
    "peking_duck": "베이징덕",
    "pho": "쌀국수",
    "pizza": "피자",
    "pork_chop": "돼지갈비 스테이크",
    "poutine": "푸틴",
    "prime_rib": "프라임 립",
    "pulled_pork_sandwich": "풀드 포크 샌드위치",
    "ramen": "라멘",
    "ravioli": "라비올리",
    "red_velvet_cake": "레드벨벳 케이크",
    "risotto": "리소토",
    "samosa": "사모사",
    "sashimi": "회",
    "scallops": "가리비 요리",
    "seaweed_salad": "해초 샐러드",
    "spaghetti_bolognese": "스파게티 볼로네제",
    "spaghetti_carbonara": "스파게티 카르보나라",
    "spring_rolls": "스프링롤",
    "steak": "스테이크",
    "strawberry_shortcake": "딸기 쇼트케이크",
    "sushi": "초밥",
    "tacos": "타코",
    "takoyaki": "타코야키",
    "tiramisu": "티라미수",
    "tuna_tartare": "참치 타르타르",
    "waffles": "와플"
}

# =========================================
# 4. CSV 파일 불러오기
# =========================================
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

    required = [
        "label", "weight", "calories",
        "protein", "fats", "carbohydrates"
    ]

    missing = [c for c in required if c not in data.columns]

    if missing:
        st.error(f"CSV에 필요한 열이 없습니다: {missing}")
        st.stop()

    for col in required[1:]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=required)

    return data


df = load_data()

# =========================================
# 5. 음식 이름 변환
# =========================================
def korean_name(label):
    return food_names.get(
        str(label),
        str(label).replace("_", " ").title()
    )

# =========================================
# 6. 메인 화면
# =========================================
st.markdown("""
<div class="emoji-banner">
🍕 🍰 🥗 🍓 🍩 🍔 🍽️ 🍴 🥄 🧁
</div>
""", unsafe_allow_html=True)

st.title("🍓 나만의 맞춤형 음식 추천!")

st.markdown("""
<div class="intro">
오늘은 어떤 음식이 먹고 싶나요? 💗<br>
원하는 영양 성분을 선택하면 딱 맞는 음식을 찾아드릴게요!
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================
# 7. 영양 성분 선택 범위
# =========================================
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

# =========================================
# 8. 사용자 선택
# =========================================
st.subheader("🎀 원하는 영양 성분을 선택해 주세요!")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔥 칼로리")
    calorie_choice = st.selectbox(
        "칼로리 범위 (kcal)",
        calorie_options
    )

    st.markdown("### 💪 단백질")
    protein_choice = st.selectbox(
        "단백질 범위 (g)",
        protein_options
    )

with col2:
    st.markdown("### 🥑 지방")
    fat_choice = st.selectbox(
        "지방 범위 (g)",
        fat_options
    )

    st.markdown("### 🍞 탄수화물")
    carb_choice = st.selectbox(
        "탄수화물 범위 (g)",
        carb_options
    )

# =========================================
# 9. 선택 범위 숫자 변환
# =========================================
def get_range(choice):
    start, end = choice.split(" ~ ")
    return int(start), int(end)


cal_min, cal_max = get_range(calorie_choice)
pro_min, pro_max = get_range(protein_choice)
fat_min, fat_max = get_range(fat_choice)
carb_min, carb_max = get_range(carb_choice)

# =========================================
# 10. 선택 조건 확인
# =========================================
st.divider()
st.subheader("📝 내가 선택한 조건")

c1, c2, c3, c4 = st.columns(4)

c1.metric("🔥 칼로리", f"{cal_min}~{cal_max}")
c2.metric("💪 단백질", f"{pro_min}~{pro_max}g")
c3.metric("🥑 지방", f"{fat_min}~{fat_max}g")
c4.metric("🍞 탄수화물", f"{carb_min}~{carb_max}g")

st.divider()

# =========================================
# 11. 음식 추천 버튼
# =========================================
if st.button("🍽️ 나에게 맞는 음식 찾기!", use_container_width=True):

    # 네 가지 조건을 모두 만족하는 음식
    exact_result = df[
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
    st.header("🍓 음식 추천 결과")

    # =====================================
    # 12. 조건에 정확히 맞는 음식이 있는 경우
    # =====================================
    if not exact_result.empty:

        st.success(
            f"🎉 선택한 조건에 맞는 음식 {len(exact_result)}개를 찾았어요!"
        )

        result = exact_result.copy()
        result["음식 이름"] = result["label"].apply(korean_name)

        for _, row in result.iterrows():

            with st.container(border=True):

                st.subheader(f"🍽️ {row['음식 이름']}")

                st.caption(f"1회 제공량: {row['weight']}g")

                a, b, c, d = st.columns(4)

                a.metric("🔥 칼로리", f"{row['calories']} kcal")
                b.metric("💪 단백질", f"{row['protein']} g")
                c.metric("🥑 지방", f"{row['fats']} g")
                d.metric("🍞 탄수화물", f"{row['carbohydrates']} g")

    # =====================================
    # 13. 정확히 맞는 음식이 없는 경우
    # =====================================
    else:

        st.warning(
            "😢 아쉽게도 네 가지 조건을 모두 만족하는 음식이 없어요!"
        )

        st.info(
            "하지만 걱정하지 마세요! 💗 "
            "선택한 영양 성분과 가장 비슷한 음식을 찾아드릴게요."
        )

        # 선택 범위와 음식 영양 성분의 차이 계산
        similar = df.copy()

        similar["calorie_diff"] = np.maximum(
            np.maximum(cal_min - similar["calories"], 0),
            similar["calories"] - cal_max
        )

        similar["protein_diff"] = np.maximum(
            np.maximum(pro_min - similar["protein"], 0),
            similar["protein"] - pro_max
        )

        similar["fat_diff"] = np.maximum(
            np.maximum(fat_min - similar["fats"], 0),
            similar["fats"] - fat_max
        )

        similar["carb_diff"] = np.maximum(
            np.maximum(carb_min - similar["carbohydrates"], 0),
            similar["carbohydrates"] - carb_max
        )

        # 각 영양 성분의 차이를 범위 간격으로 정규화
        similar["similarity_score"] = np.sqrt(
            (similar["calorie_diff"] / 100) ** 2 +
            (similar["protein_diff"] / 20) ** 2 +
            (similar["fat_diff"] / 20) ** 2 +
            (similar["carb_diff"] / 20) ** 2
        )

        # 차이가 가장 적은 음식 5개
        similar = similar.sort_values(
            by="similarity_score"
        ).head(5)

        st.subheader("💗 선택한 조건과 가장 비슷한 음식 TOP 5")

        st.caption(
            "네 가지 영양 성분의 범위와 차이를 종합하여 가까운 순서로 정렬했어요."
        )

        for rank, (_, row) in enumerate(similar.iterrows(), 1):

            with st.container(border=True):

                st.subheader(
                    f"🏆 {rank}위 | {korean_name(row['label'])}"
                )

                st.caption(f"1회 제공량: {row['weight']}g")

                a, b, c, d = st.columns(4)

                a.metric("🔥 칼로리", f"{row['calories']} kcal")
                b.metric("💪 단백질", f"{row['protein']} g")
                c.metric("🥑 지방", f"{row['fats']} g")
                d.metric("🍞 탄수화물", f"{row['carbohydrates']} g")

                st.caption(
                    f"선택 범위와의 차이 점수: "
                    f"{row['similarity_score']:.2f}"
                )

# =========================================
# 14. 하단 디자인
# =========================================
st.divider()

st.markdown("""
<div class="emoji-banner">
🍓 🥐 🍰 🍕 🥗 🍔 🍩 🍮 🍽️
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;color:#d63384;'>"
    "💗 맛있는 음식과 함께 즐거운 하루 보내세요! 💗"
    "</p>",
    unsafe_allow_html=True
)

st.caption(
    "※ 음식 및 영양 정보는 nutrition.csv 데이터에 기반합니다."
)
