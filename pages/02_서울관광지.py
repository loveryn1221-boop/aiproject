import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top 10 Tourist Spots", page_icon="🗺️", layout="wide")

# 주요 관광지는 외국인 관광객 선호도가 높은 대표 명소를 중심으로 구성한 추천 목록입니다.
# 공식 단일 순위가 아닌 여행 안내용 큐레이션입니다.
PLACES = [
    {"name":"경복궁", "en":"Gyeongbokgung Palace", "lat":37.5796, "lon":126.9770, "area":"종로구",
     "desc":"조선 왕조의 대표 궁궐로, 근정전과 경회루 등 아름다운 전통 건축을 만날 수 있어요.",
     "tip":"한복을 입고 방문하면 특별한 사진을 남기기 좋아요.", "emoji":"🏯"},
    {"name":"명동", "en":"Myeongdong", "lat":37.5636, "lon":126.9869, "area":"중구",
     "desc":"쇼핑 거리와 길거리 음식, 화장품 매장이 모여 있는 활기찬 관광 중심지예요.",
     "tip":"저녁 시간대에 방문하면 먹거리와 거리 분위기를 즐기기 좋아요.", "emoji":"🛍️"},
    {"name":"N서울타워", "en":"N Seoul Tower", "lat":37.5512, "lon":126.9882, "area":"용산구",
     "desc":"남산 정상에서 서울 도심을 한눈에 내려다볼 수 있는 전망 명소예요.",
     "tip":"해 질 무렵부터 야경 시간까지 추천해요.", "emoji":"🗼"},
    {"name":"북촌 한옥마을", "en":"Bukchon Hanok Village", "lat":37.5826, "lon":126.9830, "area":"종로구",
     "desc":"전통 한옥이 이어진 골목에서 서울의 옛 정취를 느낄 수 있어요.",
     "tip":"실제 주민이 거주하는 곳이므로 조용히 관람하고 출입 제한 안내를 지켜주세요.", "emoji":"🏘️"},
    {"name":"인사동", "en":"Insadong", "lat":37.5742, "lon":126.9855, "area":"종로구",
     "desc":"전통 공예품과 갤러리, 찻집이 모여 있어 한국 문화를 경험하기 좋은 거리예요.",
     "tip":"기념품을 찾거나 전통차를 맛보기에 좋아요.", "emoji":"🎎"},
    {"name":"창덕궁", "en":"Changdeokgung Palace", "lat":37.5794, "lon":126.9910, "area":"종로구",
     "desc":"자연 지형을 살린 궁궐 건축으로 유명하며 후원(비원)이 특히 아름다워요.",
     "tip":"후원 관람은 예약·운영 일정 확인을 추천해요.", "emoji":"🌳"},
    {"name":"홍대", "en":"Hongdae", "lat":37.5563, "lon":126.9236, "area":"마포구",
     "desc":"개성 있는 카페와 상점, 거리 공연 등 젊고 자유로운 분위기를 즐길 수 있어요.",
     "tip":"주말에는 거리 공연과 플리마켓을 구경해 보세요.", "emoji":"🎸"},
    {"name":"동대문디자인플라자(DDP)", "en":"Dongdaemun Design Plaza", "lat":37.5671, "lon":127.0095, "area":"중구",
     "desc":"독특한 곡선형 건축물과 전시·디자인 행사가 열리는 서울의 랜드마크예요.",
     "tip":"건물 외관과 주변 야간 조명도 멋진 볼거리예요.", "emoji":"✨"},
    {"name":"광장시장", "en":"Gwangjang Market", "lat":37.5701, "lon":126.9997, "area":"종로구",
     "desc":"빈대떡과 김밥 등 다양한 한국 길거리 음식을 맛볼 수 있는 전통 시장이에요.",
     "tip":"혼잡할 수 있으니 소지품을 잘 챙기고 현장 가격을 확인하세요.", "emoji":"🥢"},
    {"name":"롯데월드타워·서울스카이", "en":"Lotte World Tower & Seoul Sky", "lat":37.5125, "lon":127.1025, "area":"송파구",
     "desc":"높은 전망대에서 서울과 한강을 조망하고 주변 복합 쇼핑 공간도 즐길 수 있어요.",
     "tip":"날씨가 맑은 날 방문하면 시야가 더 좋아요.", "emoji":"🌆"},
]

st.title("🗺️ 서울 외국인 인기 관광지 TOP 10")
st.caption("서울 여행을 계획할 때 참고하기 좋은 대표 명소 10곳을 지도에서 확인해 보세요.")
st.info("안내: 아래 목록은 외국인 관광객에게 널리 알려진 대표 명소를 바탕으로 한 여행 추천 큐레이션이며, 특정 연도의 공식 방문객 수 순위는 아닙니다.")

with st.sidebar:
    st.header("🔎 관광지 찾기")
    selected = st.multiselect("지도에 표시할 관광지", [p["name"] for p in PLACES],
                              default=[p["name"] for p in PLACES])
    st.markdown("---")
    st.caption("마커를 클릭하면 관광지 이름과 간단한 정보를 볼 수 있어요.")

visible = [p for p in PLACES if p["name"] in selected]
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11, tiles="OpenStreetMap", control_scale=True)

for i, p in enumerate(visible, 1):
    popup_html = f"""
    <div style='width:220px'>
      <b>{i}. {p['emoji']} {p['name']}</b><br>
      <span>{p['en']}</span><br>
      <small>{p['area']}</small><br><br>{p['desc']}
    </div>"""
    folium.Marker(
        location=[p["lat"], p["lon"]],
        tooltip=f"{i}. {p['name']}",
        popup=folium.Popup(popup_html, max_width=280),
        icon=folium.Icon(color="red" if i == 1 else "blue", icon="info-sign")
    ).add_to(m)

if visible:
    bounds = [[p["lat"], p["lon"]] for p in visible]
    m.fit_bounds(bounds, padding=(30, 30))

st.subheader("📍 서울 관광지 지도")
st_folium(m, use_container_width=True, height=570, returned_objects=[])

st.subheader("✨ 관광지 한눈에 보기")
for start in range(0, len(PLACES), 2):
    cols = st.columns(2)
    for col, p in zip(cols, PLACES[start:start+2]):
        with col:
            st.markdown(f"### {p['emoji']} {p['name']}")
            st.caption(f"{p['en']} · {p['area']}")
            st.write(p["desc"])
            st.write(f"💡 **여행 팁:** {p['tip']}")
            st.markdown("---")

st.caption("방문 전 각 관광지의 공식 홈페이지에서 운영 시간, 휴무일, 예약 및 입장 정보를 확인하세요.")
