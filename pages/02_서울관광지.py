
import streamlit as st
import folium
from streamlit_folium import st_folium

# =====================================
# 1. 페이지 설정
# =====================================
# 반드시 가장 먼저 실행해야 합니다.
st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# =====================================
# 2. 관광지 데이터
# =====================================
PLACES = [
    {
        "name": "경복궁",
        "en": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "area": "종로구",
        "desc": "조선 왕조의 대표 궁궐입니다. 근정전과 경회루 등 아름다운 전통 건축을 볼 수 있습니다.",
        "tip": "한복을 입고 방문하면 특별한 사진을 남기기 좋아요.",
        "emoji": "🏯"
    },
    {
        "name": "명동",
        "en": "Myeongdong",
        "lat": 37.5636,
        "lon": 126.9869,
        "area": "중구",
        "desc": "쇼핑 거리와 길거리 음식, 화장품 매장이 모여 있는 서울의 대표 관광지입니다.",
        "tip": "저녁 시간에 방문하면 다양한 길거리 음식을 즐길 수 있어요.",
        "emoji": "🛍️"
    },
    {
        "name": "N서울타워",
        "en": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "area": "용산구",
        "desc": "남산 정상에서 서울 도심을 한눈에 내려다볼 수 있는 전망 명소입니다.",
        "tip": "해 질 무렵 방문하면 아름다운 야경을 볼 수 있어요.",
        "emoji": "🗼"
    },
    {
        "name": "북촌 한옥마을",
        "en": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "area": "종로구",
        "desc": "전통 한옥이 이어진 골목에서 서울의 옛 정취를 느낄 수 있습니다.",
        "tip": "주민이 실제 거주하는 곳이므로 조용히 관람해 주세요.",
        "emoji": "🏘️"
    },
    {
        "name": "인사동",
        "en": "Insadong",
        "lat": 37.5742,
        "lon": 126.9855,
        "area": "종로구",
        "desc": "전통 공예품과 갤러리, 찻집이 모여 있어 한국 문화를 경험하기 좋은 거리입니다.",
        "tip": "전통차를 마시거나 한국 기념품을 구경해 보세요.",
        "emoji": "🎎"
    },
    {
        "name": "창덕궁",
        "en": "Changdeokgung Palace",
        "lat": 37.5794,
        "lon": 126.9910,
        "area": "종로구",
        "desc": "자연 지형을 살린 아름다운 궁궐로 후원이 특히 유명합니다.",
        "tip": "후원 관람은 예약과 운영 일정을 확인하세요.",
        "emoji": "🌳"
    },
    {
        "name": "홍대",
        "en": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "area": "마포구",
        "desc": "개성 있는 카페와 상점, 거리 공연 등 젊고 자유로운 분위기를 즐길 수 있습니다.",
        "tip": "주말에는 거리 공연을 구경해 보세요.",
        "emoji": "🎸"
    },
    {
        "name": "동대문디자인플라자",
        "en": "Dongdaemun Design Plaza",
        "lat": 37.5671,
        "lon": 127.0095,
        "area": "중구",
        "desc": "독특한 곡선형 건축물과 다양한 전시가 열리는 서울의 랜드마크입니다.",
        "tip": "건물 외관과 야간 조명을 감상해 보세요.",
        "emoji": "✨"
    },
    {
        "name": "광장시장",
        "en": "Gwangjang Market",
        "lat": 37.5701,
        "lon": 126.9997,
        "area": "종로구",
        "desc": "빈대떡과 김밥 등 다양한 한국 음식을 맛볼 수 있는 전통 시장입니다.",
        "tip": "다양한 한국 길거리 음식을 경험해 보세요.",
        "emoji": "🥢"
    },
    {
        "name": "롯데월드타워",
        "en": "Lotte World Tower",
        "lat": 37.5125,
        "lon": 127.1025,
        "area": "송파구",
        "desc": "높은 전망대에서 서울과 한강을 조망할 수 있는 대표적인 랜드마크입니다.",
        "tip": "날씨가 맑은 날 방문하면 전망이 더욱 좋아요.",
        "emoji": "🌆"
    }
]

# =====================================
# 3. 메인 화면
# =====================================
st.title("🗺️ 서울 외국인 인기 관광지 TOP 10")

st.subheader(
    "🇰🇷 대한민국 서울의 아름다운 관광지를 만나보세요!"
)

st.write(
    "서울을 방문하는 외국인 관광객에게 "
    "널리 알려진 대표 관광지 10곳을 소개합니다."
)

st.info(
    "※ 공식 방문객 수 순위가 아닌 "
    "대표 관광지를 선정한 추천 목록입니다."
)

# =====================================
# 4. 사이드바
# =====================================
st.sidebar.title("🔎 관광지 선택")

selected_places = st.sidebar.multiselect(
    "지도에 표시할 관광지를 선택하세요.",
    options=[p["name"] for p in PLACES],
    default=[p["name"] for p in PLACES]
)

visible_places = [
    p for p in PLACES
    if p["name"] in selected_places
]

# =====================================
# 5. 서울 지도 생성
# =====================================
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="OpenStreetMap",
    control_scale=True
)

# =====================================
# 6. 지도에 관광지 표시
# =====================================
for i, place in enumerate(visible_places, start=1):

    popup_content = f"""
    <div style="width:230px">
        <h3>{place['emoji']} {place['name']}</h3>
        <b>{place['en']}</b>
        <br>
        <small>{place['area']}</small>
        <hr>
        <p>{place['desc']}</p>
        <p>💡 {place['tip']}</p>
    </div>
    """

    folium.Marker(
        location=[
            place["lat"],
            place["lon"]
        ],
        tooltip=f"{i}. {place['name']}",
        popup=folium.Popup(
            popup_content,
            max_width=300
        ),
        icon=folium.Icon(
            color="blue",
            icon="info-sign"
        )
    ).add_to(seoul_map)

# 선택한 관광지에 맞춰 지도 크기 조정
if visible_places:

    bounds = [
        [p["lat"], p["lon"]]
        for p in visible_places
    ]

    seoul_map.fit_bounds(
        bounds,
        padding=(30, 30)
    )

# =====================================
# 7. 지도 출력
# =====================================
st.markdown("---")

st.header("📍 서울 관광지 위치")

if visible_places:

    st_folium(
        seoul_map,
        width=None,
        height=570,
        use_container_width=True,
        returned_objects=[]
    )

else:

    st.warning(
        "관광지를 하나 이상 선택해 주세요."
    )

# =====================================
# 8. 관광지 설명
# =====================================
st.markdown("---")

st.header("✨ 서울 관광지 TOP 10 소개")

st.write(
    "지도에서 위치를 확인하고 "
    "각 관광지의 특징도 살펴보세요!"
)

for start in range(0, len(PLACES), 2):

    columns = st.columns(2)

    for column, place in zip(
        columns,
        PLACES[start:start + 2]
    ):

        with column:

            st.subheader(
                f"{place['emoji']} {place['name']}"
            )

            st.caption(
                f"{place['en']} | {place['area']}"
            )

            st.write(place["desc"])

            st.info(
                f"💡 여행 팁: {place['tip']}"
            )

            st.markdown("---")

# =====================================
# 9. 하단 안내
# =====================================
st.success(
    "🎉 서울의 아름다운 관광지 10곳을 모두 살펴봤어요!"
)

st.caption(
    "관광지 방문 전 공식 홈페이지에서 "
    "운영 시간과 휴무일을 확인해 주세요."
)
