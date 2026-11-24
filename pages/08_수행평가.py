
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="나만의 음식 추천",
    page_icon="🍓",
    layout="wide"
)

# =========================================
# 1. 음식 이모티콘 애니메이션 배경
# =========================================

st.markdown("""
<style>
/* 기본 배경 */
.stApp {
    background:
        linear-gradient(135deg, #fff5f8, #fffaf0, #ffeaf2);
    background-attachment: fixed;
}

/* 실제 앱 콘텐츠를 배경 위에 배치 */
.stMainBlockContainer {
    position: relative;
    z-index: 2;
}

/* 움직이는 이모티콘 배경 */
.food-animation {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    pointer-events: none;
    z-index: 1;
}

/* 이모티콘 공통 디자인 */
.food {
    position: absolute;
    font-size: 35px;
    opacity: 0.55;
    will-change: transform;
    animation: flyAcross linear infinite;
}

/* 빠르게 왼쪽에서 오른쪽으로 */
@keyframes flyAcross {
    0% {
        transform: translate(-15vw, 25vh) rotate(0deg);
    }
    100% {
        transform: translate(115vw, -35vh) rotate(720deg);
    }
}

/* 반대 방향으로 이동 */
@keyframes flyBack {
    0% {
        transform: translate(115vw, 35vh) rotate(0deg);
    }
    100% {
        transform: translate(-15vw, -35vh) rotate(-720deg);
    }
}

/* 위에서 아래로 이동 */
@keyframes flyDown {
    0% {
        transform: translate(10vw, -15vh) rotate(0deg);
    }
    100% {
        transform: translate(-10vw, 115vh) rotate(540deg);
    }
}

/* 각 이모티콘 위치와 속도 */
.food:nth-child(1)  {top:10%; left:0%; animation-duration:6s; animation-delay:-2s;}
.food:nth-child(2)  {top:30%; left:5%; animation-duration:8s; animation-delay:-5s; animation-name:flyBack;}
.food:nth-child(3)  {top:50%; left:0%; animation-duration:5s; animation-delay:-3s;}
.food:nth-child(4)  {top:70%; left:10%; animation-duration:9s; animation-delay:-6s; animation-name:flyBack;}
.food:nth-child(5)  {top:85%; left:0%; animation-duration:7s; animation-delay:-1s;}
.food:nth-child(6)  {top:20%; left:20%; animation-duration:6s; animation-delay:-4s; animation-name:flyDown;}
.food:nth-child(7)  {top:40%; left:30%; animation-duration:8s; animation-delay:-3s;}
.food:nth-child(8)  {top:60%; left:40%; animation-duration:5s; animation-delay:-2s; animation-name:flyBack;}
.food:nth-child(9)  {top:80%; left:50%; animation-duration:7s; animation-delay:-5s;}
.food:nth-child(10) {top:15%; left:60%; animation-duration:6s; animation-delay:-3s; animation-name:flyDown;}
.food:nth-child(11) {top:35%; left:70%; animation-duration:9s; animation-delay:-6s;}
.food:nth-child(12) {top:55%; left:80%; animation-duration:5s; animation-delay:-2s; animation-name:flyBack;}
.food:nth-child(13) {top:75%; left:90%; animation-duration:7s; animation-delay:-4s;}
.food:nth-child(14) {top:5%; left:40%; animation-duration:8s; animation-delay:-7s;}
.food:nth-child(15) {top:25%; left:90%; animation-duration:6s; animation-delay:-1s; animation-name:flyBack;}
.food:nth-child(16) {top:45%; left:15%; animation-duration:5s; animation-delay:-4s;}
.food:nth-child(17) {top:65%; left:65%; animation-duration:8s; animation-delay:-2s;}
.food:nth-child(18) {top:90%; left:75%; animation-duration:6s; animation-delay:-5s; animation-name:flyDown;}
.food:nth-child(19) {top:12%; left:80%; animation-duration:7s; animation-delay:-3s;}
.food:nth-child(20) {top:52%; left:50%; animation-duration:5s; animation-delay:-1s; animation-name:flyBack;}
.food:nth-child(21) {top:72%; left:25%; animation-duration:9s; animation-delay:-4s;}
.food:nth-child(22) {top:32%; left:55%; animation-duration:6s; animation-delay:-2s;}
.food:nth-child(23) {top:88%; left:35%; animation-duration:7s; animation-delay:-6s; animation-name:flyBack;}
.food:nth-child(24) {top:18%; left:45%; animation-duration:5s; animation-delay:-3s;}

/* 모바일 화면 */
@media (max-width: 768px) {
    .food {
        font-size: 23px;
        opacity: 0.4;
    }
}

/* 제목 */
h1, h2, h3 {
    color: #d63384 !important;
}

/* 버튼 */
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

/* 음식 카드 */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: rgba(255,255,255,0.88);
    border-radius: 18px;
    border: 1px solid #ffd1df;
}

div[data-testid="stMetric"] {
    background: #fff3f7;
    padding: 12px;
    border-radius: 12px;
}
</style>

<div class="food-animation">
    <span class="food">🍕</span>
    <span class="food">🍓</span>
    <span class="food">🍔</span>
    <span class="food">🍰</span>
    <span class="food">🍩</span>
    <span class="food">🥑</span>
    <span class="food">🍟</span>
    <span class="food">🍎</span>
    <span class="food">🥐</span>
    <span class="food">🧁</span>
    <span class="food">🍒</span>
    <span class="food">🥗</span>
    <span class="food">🍉</span>
    <span class="food">🍪</span>
    <span class="food">🍦</span>
    <span class="food">🥨</span>
    <span class="food">🍇</span>
    <span class="food">🍮</span>
    <span class="food">🍜</span>
    <span class="food">🍤</span>
    <span class="food">🥞</span>
    <span class="food">🍫</span>
    <span class="food">🍊</span>
    <span class="food">🍽️</span>
</div>
""", unsafe_allow_html=True)

# =========================================
# 2. 음식 이름 한국어 변환
# =========================================

food_names = {
    "apple_pie": "애플파이",
    "baby_back_ribs": "돼지 등갈비",
    "baklava": "바클라바",
    "beef_carpaccio": "소고기 카르파초",
    "beef_tartare": "소고기 타르타르",
    "beet_salad": "비트 샐러드",
    "beignets": "베녜",
    "bibimbap": "비빔밥",
    "bread_pudding": "브레드 푸딩",
    "breakfast_burrito": "아침 부리토",
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

def korean_name(label):
    return food_names.get(
        str(label),
        str(label).replace("_", " ").title()
    )

# =========================================
# 3. 데이터 불러오기
# =========================================

@st.cache_data
def load_data():

    current_dir = Path(__file__).resolve().parent

    paths = [
        current_dir.parent / "nutrition.csv",
        current_dir / "nutrition.csv",
        Path.cwd() / "nutrition.csv"
    ]

    csv_path = next((p for p in paths if p.exists()), None)

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
        st.error(f"필요한 데이터 열이 없습니다: {missing}")
        st.stop()

    for col in required[1:]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    return data.dropna(subset=required)


df = load_data()

# =========================================
# 4. 메인 화면
# =========================================

st.title("🍓 나만의 맞춤형 음식 추천!")
st.markdown("""
### 🍽️ 맛있는 음식, 내 취향대로 찾아보자!

원하는 영양 성분을 선택하면 가장 잘 맞는 음식을 추천해 줄게요.
""")

st.divider()

# =========================================
# 5. 영양 성분 선택
# =========================================

calorie_options = [f"{i} ~ {i+100}" for i in range(0, 1000, 100)]
protein_options = [f"{i} ~ {i+20}" for i in range(0, 60, 20)]
fat_options = [f"{i} ~ {i+20}" for i in range(0, 100, 20)]
carb_options = [f"{i} ~ {i+20}" for i in range(0, 100, 20)]

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 칼로리")
    calorie_choice = st.selectbox(
        "칼로리 범위 (kcal)", calorie_options
    )

    st.subheader("💪 단백질")
    protein_choice = st.selectbox(
        "단백질 범위 (g)", protein_options
    )

with col2:
    st.subheader("🥑 지방")
    fat_choice = st.selectbox(
        "지방 범위 (g)", fat_options
    )

    st.subheader("🍞 탄수화물")
    carb_choice = st.selectbox(
        "탄수화물 범위 (g)", carb_options
    )


def get_range(choice):
    start, end = choice.split(" ~ ")
    return int(start), int(end)


cal_min, cal_max = get_range(calorie_choice)
pro_min, pro_max = get_range(protein_choice)
fat_min, fat_max = get_range(fat_choice)
carb_min, carb_max = get_range(carb_choice)

# =========================================
# 6. 선택 조건 표시
# =========================================

st.divider()
st.subheader("📝 선택한 영양 성분")

a, b, c, d = st.columns(4)

a.metric("🔥 칼로리", f"{cal_min}~{cal_max} kcal")
b.metric("💪 단백질", f"{pro_min}~{pro_max} g")
c.metric("🥑 지방", f"{fat_min}~{fat_max} g")
d.metric("🍞 탄수화물", f"{carb_min}~{carb_max} g")

st.divider()

# =========================================
# 7. 음식 추천
# =========================================

if st.button("🍓 맛있는 음식 추천받기!", use_container_width=True):

    exact = df[
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
    st.header("🎀 추천 음식")

    # =====================================
    # 조건에 맞는 음식이 있는 경우
    # =====================================

    if not exact.empty:

        st.success(
            f"🎉 선택한 조건에 딱 맞는 음식 {len(exact)}개를 찾았어요!"
        )

        result = exact.sort_values("calories")

    # =====================================
    # 조건에 맞는 음식이 없는 경우
    # =====================================

    else:

        st.warning(
            "😢 아쉽지만 선택한 네 가지 조건을 모두 만족하는 음식이 없어요."
        )

        st.info(
            "대신 선택한 영양 성분과 가장 비슷한 음식 5개를 추천해 드릴게요! 💗"
        )

        similar = df.copy()

        # 각 영양 성분이 선택 범위에서 얼마나 벗어났는지 계산
        similar["calorie_diff"] = np.maximum(
            cal_min - similar["calories"], 0
        ) + np.maximum(
            similar["calories"] - cal_max, 0
        )

        similar["protein_diff"] = np.maximum(
            pro_min - similar["protein"], 0
        ) + np.maximum(
            similar["protein"] - pro_max, 0
        )

        similar["fat_diff"] = np.maximum(
            fat_min - similar["fats"], 0
        ) + np.maximum(
            similar["fats"] - fat_max, 0
        )

        similar["carb_diff"] = np.maximum(
            carb_min - similar["carbohydrates"], 0
        ) + np.maximum(
            similar["carbohydrates"] - carb_max, 0
        )

        # 영양 성분별 범위 간격을 기준으로 정규화
        similar["similarity_score"] = np.sqrt(
            (similar["calorie_diff"] / 100) ** 2 +
            (similar["protein_diff"] / 20) ** 2 +
            (similar["fat_diff"] / 20) ** 2 +
            (similar["carb_diff"] / 20) ** 2
        )

        result = similar.sort_values(
            "similarity_score"
        ).head(5)

        st.subheader("🏆 가장 비슷한 음식 TOP 5")
        st.caption("점수가 낮을수록 선택한 영양 조건에 가까워요.")

    # =====================================
    # 8. 추천 음식 카드 출력
    # =====================================

    for rank, (_, row) in enumerate(result.iterrows(), 1):

        name = korean_name(row["label"])

        with st.container(border=True):

            if exact.empty:
                st.subheader(f"🏆 {rank}위 | 🍽️ {name}")
            else:
                st.subheader(f"🍽️ {name}")

            st.caption(f"제공량: {row['weight']}g")

            x1, x2, x3, x4 = st.columns(4)

            x1.metric("🔥 칼로리", f"{row['calories']} kcal")
            x2.metric("💪 단백질", f"{row['protein']} g")
            x3.metric("🥑 지방", f"{row['fats']} g")
            x4.metric("🍞 탄수화물", f"{row['carbohydrates']} g")

            if exact.empty:
                st.caption(
                    f"선택 조건과의 차이 점수: "
                    f"{row['similarity_score']:.2f}"
                )

    # =====================================
    # 9. 전체 결과 표
    # =====================================

    st.divider()
    st.subheader("📊 음식 영양 정보 한눈에 보기")

    display = result.copy()
    display["음식 이름"] = display["label"].apply(korean_name)

    display = display[
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
        display,
        use_container_width=True,
        hide_index=True
    )

# =========================================
# 10. 하단 장식
# =========================================

st.divider()

st.markdown("""
<div style="
text-align:center;
font-size:35px;
padding:20px;
">
🍓 🍰 🥐 🍕 🥗 🍔 🍩 🍮 🍽️
</div>

<div style="
text-align:center;
color:#d63384;
font-size:17px;
font-weight:bold;
">
맛있는 음식과 함께 행복한 하루 보내세요! 💗
</div>
""", unsafe_allow_html=True)

st.caption("영양 정보는 nutrition.csv 데이터를 기준으로 합니다.")
