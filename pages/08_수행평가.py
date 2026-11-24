
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
.stApp {
    background: linear-gradient(135deg, #fff5f8, #fffaf0, #ffeaf2);
    background-attachment: fixed;
}

.stMainBlockContainer {
    position: relative;
    z-index: 2;
}

.food-animation {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 1;
}

.food {
    position: absolute;
    font-size: 35px;
    opacity: 0.45;
    animation: flyAcross linear infinite;
    will-change: transform;
}

@keyframes flyAcross {
    0% {
        transform: translate(-15vw, 25vh) rotate(0deg);
    }
    100% {
        transform: translate(115vw, -35vh) rotate(720deg);
    }
}

@keyframes flyBack {
    0% {
        transform: translate(115vw, 35vh) rotate(0deg);
    }
    100% {
        transform: translate(-15vw, -35vh) rotate(-720deg);
    }
}

.food:nth-child(1) {top:10%; animation-duration:6s;}
.food:nth-child(2) {top:30%; animation-duration:8s; animation-name:flyBack;}
.food:nth-child(3) {top:50%; animation-duration:5s;}
.food:nth-child(4) {top:70%; animation-duration:7s; animation-name:flyBack;}
.food:nth-child(5) {top:85%; animation-duration:6s;}
.food:nth-child(6) {top:20%; animation-duration:5s; animation-name:flyBack;}
.food:nth-child(7) {top:40%; animation-duration:8s;}
.food:nth-child(8) {top:60%; animation-duration:6s; animation-name:flyBack;}
.food:nth-child(9) {top:80%; animation-duration:5s;}
.food:nth-child(10) {top:15%; animation-duration:7s; animation-name:flyBack;}
.food:nth-child(11) {top:35%; animation-duration:6s;}
.food:nth-child(12) {top:55%; animation-duration:5s; animation-name:flyBack;}
.food:nth-child(13) {top:75%; animation-duration:8s;}
.food:nth-child(14) {top:5%; animation-duration:6s; animation-name:flyBack;}
.food:nth-child(15) {top:25%; animation-duration:7s;}
.food:nth-child(16) {top:45%; animation-duration:5s; animation-name:flyBack;}
.food:nth-child(17) {top:65%; animation-duration:8s;}
.food:nth-child(18) {top:90%; animation-duration:6s; animation-name:flyBack;}
.food:nth-child(19) {top:12%; animation-duration:5s;}
.food:nth-child(20) {top:52%; animation-duration:7s; animation-name:flyBack;}
.food:nth-child(21) {top:72%; animation-duration:6s;}
.food:nth-child(22) {top:32%; animation-duration:8s; animation-name:flyBack;}
.food:nth-child(23) {top:88%; animation-duration:5s;}
.food:nth-child(24) {top:18%; animation-duration:7s; animation-name:flyBack;}

@media (max-width: 768px) {
    .food {font-size:22px;}
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
    background-color: rgba(255,255,255,0.9);
    border-radius: 18px;
    border: 1px solid #ffd1df;
}

div[data-testid="stMetric"] {
    background: #fff3f7;
    padding: 12px;
    border-radius: 12px;
}

.selection-notice {
    background: linear-gradient(110deg, #ffe0ed, #fff0d9);
    border: 3px solid #ff8bb8;
    border-radius: 22px;
    padding: 25px 15px;
    text-align: center;
    margin: 15px 0 25px 0;
    box-shadow: 0 5px 15px rgba(255,105,164,0.15);
}

.selection-notice h2 {
    color: #d63384 !important;
    font-size: 30px !important;
    margin-bottom: 12px;
}

.selection-notice p {
    color: #a83d70;
    font-size: 19px;
    font-weight: bold;
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
# 2. 음식 이름 한국어 사전
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
# 3. CSV 데이터 불러오기
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

# 여러 개 선택 안내를 크게 표시
st.markdown("""
<div class="selection-notice">
    <h2>📢 여러 개를 선택할 수 있어요!</h2>
    <p>각 영양 성분에서 원하는 범위를 여러 개 골라보세요!</p>
    <p>예시: 칼로리 100~200 + 300~400을 동시에 선택 가능!</p>
    <p>💗 선택한 범위 중 하나라도 만족하면 검색돼요!</p>
</div>
""", unsafe_allow_html=True)

# =========================================
# 5. 선택 범위 설정
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
# 6. 다중 선택 화면
# =========================================

st.subheader("🎀 원하는 영양 성분 범위를 선택하세요!")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🔥 칼로리")

    calorie_choices = st.multiselect(
        "칼로리 범위 (kcal) - 여러 개 선택 가능",
        options=calorie_options,
        placeholder="원하는 칼로리 범위를 모두 선택하세요"
    )

    st.markdown("### 💪 단백질")

    protein_choices = st.multiselect(
        "단백질 범위 (g) - 여러 개 선택 가능",
        options=protein_options,
        placeholder="원하는 단백질 범위를 모두 선택하세요"
    )

with col2:

    st.markdown("### 🥑 지방")

    fat_choices = st.multiselect(
        "지방 범위 (g) - 여러 개 선택 가능",
        options=fat_options,
        placeholder="원하는 지방 범위를 모두 선택하세요"
    )

    st.markdown("### 🍞 탄수화물")

    carb_choices = st.multiselect(
        "탄수화물 범위 (g) - 여러 개 선택 가능",
        options=carb_options,
        placeholder="원하는 탄수화물 범위를 모두 선택하세요"
    )

# =========================================
# 7. 선택한 범위 숫자로 변환
# =========================================

def convert_ranges(choices):
    return [
        tuple(map(int, choice.split(" ~ ")))
        for choice in choices
    ]


cal_ranges = convert_ranges(calorie_choices)
pro_ranges = convert_ranges(protein_choices)
fat_ranges = convert_ranges(fat_choices)
carb_ranges = convert_ranges(carb_choices)

# =========================================
# 8. 선택 조건 확인
# =========================================

st.divider()
st.subheader("📝 내가 선택한 조건")

if all([
    cal_ranges,
    pro_ranges,
    fat_ranges,
    carb_ranges
]):

    def format_choices(choices, unit):
        return ", ".join(
            f"{choice} {unit}"
            for choice in choices
        )

    c1, c2 = st.columns(2)

    with c1:
        st.info(
            "🔥 칼로리\n\n" +
            format_choices(calorie_choices, "kcal")
        )

        st.info(
            "💪 단백질\n\n" +
            format_choices(protein_choices, "g")
        )

    with c2:
        st.info(
            "🥑 지방\n\n" +
            format_choices(fat_choices, "g")
        )

        st.info(
            "🍞 탄수화물\n\n" +
            format_choices(carb_choices, "g")
        )

else:
    st.warning("네 가지 영양 성분에서 각각 하나 이상의 범위를 선택해 주세요!")

st.divider()

# =========================================
# 9. 여러 범위 중 하나라도 만족하는지 확인
# =========================================

def matches_ranges(series, ranges):
    result = pd.Series(False, index=series.index)

    for start, end in ranges:
        result |= (
            (series >= start) &
            (series < end)
        )

    return result


# =========================================
# 10. 선택 범위와의 최소 거리 계산
# =========================================

def distance_to_ranges(series, ranges, interval_width):

    distances = []

    for start, end in ranges:

        distance = np.maximum(
            np.maximum(start - series, 0),
            series - end
        )

        distances.append(distance / interval_width)

    return pd.concat(distances, axis=1).min(axis=1)


# =========================================
# 11. 음식 추천 버튼
# =========================================

if st.button(
    "🍓 나에게 맞는 음식 추천받기!",
    use_container_width=True
):

    # 네 항목 모두 선택했는지 확인
    if not all([
        cal_ranges,
        pro_ranges,
        fat_ranges,
        carb_ranges
    ]):

        st.error(
            "⚠️ 칼로리, 단백질, 지방, 탄수화물 범위를 모두 선택해 주세요!"
        )

    else:

        # 네 가지 영양 조건을 각각 검색
        exact = df[
            matches_ranges(df["calories"], cal_ranges) &
            matches_ranges(df["protein"], pro_ranges) &
            matches_ranges(df["fats"], fat_ranges) &
            matches_ranges(df["carbohydrates"], carb_ranges)
        ].copy()

        st.divider()
        st.header("🎀 음식 추천 결과")

        # =================================
        # 12. 정확히 일치하는 음식
        # =================================

        if not exact.empty:

            st.success(
                f"🎉 선택한 조건에 맞는 음식 {len(exact)}개를 찾았어요!"
            )

            result = exact.sort_values("calories")

        # =================================
        # 13. 비슷한 음식 추천
        # =================================

        else:

            st.warning(
                "😢 선택한 네 가지 조건을 모두 만족하는 음식이 없어요!"
            )

            st.info(
                "💗 걱정하지 마세요! "
                "선택한 영양 성분과 가장 비슷한 음식 5개를 추천해 드릴게요."
            )

            similar = df.copy()

            # 각 항목에서 선택한 범위 중 가장 가까운 범위까지의 거리
            similar["calorie_diff"] = distance_to_ranges(
                similar["calories"], cal_ranges, 100
            )

            similar["protein_diff"] = distance_to_ranges(
                similar["protein"], pro_ranges, 20
            )

            similar["fat_diff"] = distance_to_ranges(
                similar["fats"], fat_ranges, 20
            )

            similar["carb_diff"] = distance_to_ranges(
                similar["carbohydrates"], carb_ranges, 20
            )

            # 네 가지 영양 성분을 종합한 유사도 점수
            similar["similarity_score"] = np.sqrt(
                similar["calorie_diff"] ** 2 +
                similar["protein_diff"] ** 2 +
                similar["fat_diff"] ** 2 +
                similar["carb_diff"] ** 2
            )

            result = similar.sort_values(
                "similarity_score"
            ).head(5)

            st.subheader("🏆 가장 비슷한 음식 TOP 5")
            st.caption(
                "점수가 낮을수록 선택한 영양 조건에 가까워요."
            )

        # =================================
        # 14. 추천 음식 카드
        # =================================

        for rank, (_, row) in enumerate(result.iterrows(), 1):

            name = korean_name(row["label"])

            with st.container(border=True):

                if exact.empty:
                    st.subheader(f"🏆 {rank}위 | 🍽️ {name}")
                else:
                    st.subheader(f"🍽️ {name}")

                st.caption(
                    f"제공량: {row['weight']}g"
                )

                a, b, c, d = st.columns(4)

                a.metric(
                    "🔥 칼로리",
                    f"{row['calories']} kcal"
                )

                b.metric(
                    "💪 단백질",
                    f"{row['protein']} g"
                )

                c.metric(
                    "🥑 지방",
                    f"{row['fats']} g"
                )

                d.metric(
                    "🍞 탄수화물",
                    f"{row['carbohydrates']} g"
                )

                if exact.empty:
                    st.caption(
                        f"조건과의 차이 점수: "
                        f"{row['similarity_score']:.2f}"
                    )

        # =================================
        # 15. 전체 결과 표
        # =================================

        st.divider()
        st.subheader("📊 추천 음식 영양 정보")

        display = result.copy()

        display["음식 이름"] = display["label"].apply(
            korean_name
        )

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
# 16. 하단 디자인
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
font-size:19px;
font-weight:bold;
">
맛있는 음식과 함께 행복한 하루 보내세요! 💗
</div>
""", unsafe_allow_html=True)

st.caption(
    "※ 음식 및 영양 정보는 nutrition.csv 데이터를 기준으로 합니다."
)
