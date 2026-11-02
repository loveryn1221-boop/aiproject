
import streamlit as st

st.set_page_config(
    page_title="MBTI 취향 추천소",
    page_icon="🪄",
    layout="centered"
)

# 화면 디자인
st.markdown("""
<style>
.stApp {
    background-color: #F3F5FF;
}
h1, h2, h3 {
    color: #493B79;
}
.stButton button {
    background-color: #7865C5;
    color: white;
    border-radius: 12px;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# MBTI별 추천 데이터
data = {
    "INTJ": ("🦉", ["마법사의 돌", "불사조 기사단"],
             ["아이언맨", "닥터 스트레인지"]),
    "INTP": ("🧠", ["비밀의 방", "혼혈 왕자"],
             ["앤트맨", "닥터 스트레인지"]),
    "ENTJ": ("🦁", ["불의 잔", "죽음의 성물 1"],
             ["어벤져스", "캡틴 아메리카: 시빌 워"]),
    "ENTP": ("🦊", ["아즈카반의 죄수", "불의 잔"],
             ["가디언즈 오브 갤럭시", "토르: 라그나로크"]),
    "INFJ": ("🦋", ["불사조 기사단", "죽음의 성물 2"],
             ["블랙 팬서", "어벤져스: 엔드게임"]),
    "INFP": ("🧚", ["마법사의 돌", "아즈카반의 죄수"],
             ["가디언즈 오브 갤럭시", "스파이더맨: 노 웨이 홈"]),
    "ENFJ": ("🌻", ["불의 잔", "죽음의 성물 2"],
             ["캡틴 아메리카: 퍼스트 어벤져", "어벤져스: 엔드게임"]),
    "ENFP": ("🌈", ["마법사의 돌", "불의 잔"],
             ["토르: 라그나로크", "가디언즈 오브 갤럭시"]),
    "ISTJ": ("🐢", ["비밀의 방", "혼혈 왕자"],
             ["캡틴 아메리카: 윈터 솔져", "아이언맨"]),
    "ISFJ": ("🐻", ["아즈카반의 죄수", "불사조 기사단"],
             ["스파이더맨: 홈커밍", "블랙 팬서"]),
    "ESTJ": ("🦅", ["불의 잔", "죽음의 성물 1"],
             ["아이언맨", "캡틴 아메리카: 시빌 워"]),
    "ESFJ": ("🐰", ["마법사의 돌", "죽음의 성물 2"],
             ["스파이더맨: 노 웨이 홈", "어벤져스"]),
    "ISTP": ("🐺", ["혼혈 왕자", "아즈카반의 죄수"],
             ["아이언맨", "블랙 위도우"]),
    "ISFP": ("🐱", ["마법사의 돌", "불사조 기사단"],
             ["닥터 스트레인지", "블랙 팬서"]),
    "ESTP": ("🐯", ["불의 잔", "아즈카반의 죄수"],
             ["스파이더맨: 파 프롬 홈", "토르: 라그나로크"]),
    "ESFP": ("🐬", ["마법사의 돌", "불의 잔"],
             ["가디언즈 오브 갤럭시", "스파이더맨: 홈커밍"])
}

# 책과 영화 전체 제목
books = {
    "마법사의 돌": "해리 포터와 마법사의 돌",
    "비밀의 방": "해리 포터와 비밀의 방",
    "아즈카반의 죄수": "해리 포터와 아즈카반의 죄수",
    "불의 잔": "해리 포터와 불의 잔",
    "불사조 기사단": "해리 포터와 불사조 기사단",
    "혼혈 왕자": "해리 포터와 혼혈 왕자",
    "죽음의 성물 1": "해리 포터와 죽음의 성물",
    "죽음의 성물 2": "해리 포터와 죽음의 성물"
}

# 제목이 겹치는 죽음의 성물 구분
# 서로 다른 책 2권이 추천되도록 설정
for mbti in data:
    emoji, book_list, movie_list = data[mbti]
    if book_list[0] == "죽음의 성물 1":
        book_list[0] = "죽음의 성물"
    if book_list[1] == "죽음의 성물 2":
        book_list[1] = "죽음의 성물"

st.title("🪄 MBTI 취향 추천소")
st.subheader("나의 MBTI에 어울리는 책과 영화는?")
st.write("16가지 MBTI 중 나의 유형을 선택해 봐! 🎉")

# MBTI 선택
mbti = st.selectbox(
    "🧩 나의 MBTI를 선택해 줘!",
    list(data.keys())
)

if st.button("✨ 나의 취향 확인하기!"):

    emoji, book_list, movie_list = data[mbti]

    st.balloons()

    st.markdown("---")

    st.header(f"{emoji} 이거 내 이모지야~!")
    st.success(f"너의 MBTI는 {mbti}!")

    st.subheader("📚 너에게 추천하는 해리포터 책 2권!")

    for i, book in enumerate(book_list, 1):
        st.markdown(f"### {i}. 📖 {books[book]}")
        st.write(
            "마법과 모험이 가득한 해리포터 세계로 떠나 보자!"
        )

    st.markdown("---")

    st.subheader("🎬 너에게 추천하는 마블 영화 2편!")

    for i, movie in enumerate(movie_list, 1):
        st.markdown(f"### {i}. 🍿 {movie}")
        st.write(
            "흥미진진한 마블의 세계를 즐겨 봐!"
        )

    st.markdown("---")
    st.success(
        "🎉 추천 결과가 마음에 들었으면 좋겠어! "
        "책과 영화로 즐거운 시간을 보내자!"
    )

st.markdown("---")
st.caption("💜 MBTI 취향 추천소 | 재미로 즐기는 성격별 추천 프로그램")
