
import streamlit as st
import folium
from streamlit_folium import st_folium

# ---------------------------------
# 1. 페이지 기본 설정
# ---------------------------------
st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# ---------------------------------
# 2. 관광지 데이터
# ---------------------------------
PLACES = [
    {
        "name": "경복궁",
        "en": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "area": "종로구",
        "desc": "조선 왕조의 대표 궁궐로, 근정전과 경회루 등 아름다운 전통 건축을 만날 수 있어요.",
        "tip": "한복을 입고 방문하면 특별한 사진을 남기기 좋아요.",
        "emoji": "🏯"
    },
    {
        "name": "명동",
        "en": "Myeongdong",
        "lat": 37.5636,
        "lon": 126.9869,
        "area": "중구",
        "desc": "쇼핑 거리와 길거리 음식, 화장품 매장이 모여 있는 활기찬 관광 중심지예요.",
        "tip": "저녁 시간대에 방문하면 먹거리와 거리 분위기를 즐기기 좋아요.",
        "emoji": "🛍️"
    },
    {
        "name": "N서울타워",
        "en": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "area": "용산구",
        "desc": "남산 정상에서 서울 도심을 한눈에 내려다볼 수 있는 전망 명소예요.",
        "tip": "해 질 무렵부터 야경 시간까지 추천해요.",
        "emoji": "🗼"
    },
    {
        "name": "북촌 한옥마을",
        "en": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "area": "종로구",
        "desc": "전통 한옥이 이어진 골목에서 서울의 옛 정취를 느낄 수 있어요.",
        "tip": "주민이 거주하는 곳이므로 조용히 관람해 주세요.",
        "emoji": "🏘️"
    },
    {
        "name": "인사동",
        "en": "Insadong",
        "lat": 37.5742,
        "lon": 126.9855,
        "area": "종로구",
        "desc": "전통 공예품과 갤러리, 찻집이 모여 있어 한국 문화를 경험하기 좋은 거리예요.",
        "tip": "기념품을 찾거나 전통차를 맛보기에 좋아요.",
        "emoji": "🎎"
    },
    {
        "name": "창덕궁",
        "en": "Changdeokgung Palace",
        "lat": 37.5794,
        "lon": 126.9910,
        "area": "종로구",
        "desc": "자연 지형을 살린 궁궐 건축으로 유명하며 후원이 특히 아름다워요.",
        "tip": "후원 관람은 예약과 운영 일정을 확인하세요.",
        "emoji": "🌳"
    },
    {
        "name": "홍대",
        "en": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "area": "마포구",
        "desc": "개성 있는 카페와 상점, 거리 공연 등 젊고 자유로운 분위기를 즐길 수 있어요.",
        "tip": "주말에는 거리 공연을 구경해 보세요.",
        "emoji": "🎸"
    },
    {
        "name": "동대문디자인플라자",
        "en": "Dongdaemun Design Plaza",
        "lat": 37.5671,
        "lon": 127.0095,
        "area": "중구",
        "desc": "독특한 곡선형 건축물과 전시, 디자인 행사가 열리는 서울의 랜드마크예요.",
        "tip": "건물 외관과 야간 조명도 멋진 볼거리예요.",
        "emoji": "✨"
    },
    {
        "name": "광장시장",
        "en": "Gwangjang Market",
        "lat": 37.5701,
        "lon": 126.9997,
        "area": "종로구",
        "desc": "빈대떡과 김밥 등 다양한 한국 길거리 음식을 맛볼 수 있는 전통 시장이에요.",
        "tip": "혼잡할 수 있으니 소지품을 잘 챙기세요.",
        "emoji": "🥢"
    },
    {
        "name": "롯데월드타워",
        "en": "Lotte World Tower",
        "lat": 37.5125,
        "lon": 127.1025,
        "area": "송파구",
        "desc": "높은 전망대에서 서울과 한강을 조망하고 쇼핑 공간도 즐길 수 있어요.",
        "tip": "날씨가 맑은 날 방문하면 시야가 더 좋아요.",
        "emoji": "🌆"
    }
]

# ---------------------------------
# 3. 화면 제목
# ---------------------------------
st.title("🗺️ 서울 외국인 인기 관광지 TOP 10")

st.subheader(
    "대한민국 서울의 아름다운 관광지를 만나보세요! 🇰🇷"
)

st.write(
    "외국인 관광객에게 널리 알려진 "
    "서울의 대표 관광지 10곳을 지도에서 확인할 수 있어요."
)

st.info(
    "※ 공식 방문객 수 순위가 아닌 대표 관광지 추천 목록입니다."
)

# ---------------------------------
# 4. 사이드바 관광지 선택
# ---------------------------------
st.sidebar.header("🔎 관광지 선택")

selected = st.sidebar.multiselect(
    "지도에 표시할 관광지를 선택하세요.",
    [p["name"] for p in PLACES],
    default=[p["name"] for p in PLACES]
)

visible = [
    p for p in PLACES
    if p["name"] in selected
]

# ---------------------------------
# 5. 서울 지도 만들기
# ---------------------------------
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="OpenStreetMap",
    control_scale=True
)

# ---------------------------------
# 6. 지도에 관광지 마커 표시
# ---------------------------------
for i, p in enumerate(visible, 1):

    popup_html = f"""
    <div style="width:220px">
        <h4>{p['emoji']} {p['name']}</h4>
        <b>{p['en']}</b>
        <br>
        <small>{p['area']}</small>
        <br><br>
        {p['desc']}
    </div>
    """

    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=f"{i}. {p['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=280
        ),
        icon=folium.Icon(
            color="blue",
            icon="info-sign"
        )
    ).add_to(m)

# 선택한 관광지가 화면에 모두 보이도록 설정
if visible:
    bounds = [
        [p["lat"], p["lon"]]
        for p in visible
    ]
    m.fit_bounds(bounds, padding=(30, 30))

# ---------------------------------
# 7. 지도 화면 출력
# ---------------------------------
st.subheader("📍 서울 관광지 지도")

st_folium(
    m,
    use_container_width=True,
    height=570,
    returned_objects=[]
)

# ---------------------------------
# 8. 관광지 설명 출력
# ---------------------------------
st.subheader("✨ 서울 관광지 TOP 10 소개")

st.write(
    "관심 있는 관광지를 살펴보고 "
    "서울 여행 계획을 세워보세요!"
)

for start in range(0, len(PLACES), 2):

    cols = st.columns(2)

    for col, p in zip(
        cols,
        PLACES[start:start + 2]
    ):

        with col:

            st.markdown(
                f"### {p['emoji']} {p['name']}"
            )

            st.caption(
                f"{p['en']} · {p['area']}"
            )

            st.write(p["desc"])

            st.write(
                f"💡 **여행 팁:** {p['tip']}"
            )

            st.markdown("---")

# ---------------------------------
# 9. 하단 안내
# ---------------------------------
st.success(
    "🎉 서울의 아름다운 관광지를 즐겁게 여행해 보세요!"
)

st.caption(
    "방문 전 관광지 공식 홈페이지에서 "
    "운영 시간과 휴무일을 확인하세요."
)
