import streamlit as st
import openai

st.title("📚 부경대 도서관 챗봇")

api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
if api_key:
    st.session_state.api_key = api_key

rules = """
- 운영 시간: 평일 09:00~22:00, 주말 10:00~18:00
- 연체 시 하루당 100원의 연체료가 발생합니다.
- 열람실은 정숙하게 이용해 주세요.
- 도서 대출은 최대 5권, 14일입니다.
"""

question = st.text_input("도서관에 대해 궁금한 점을 물어보세요")

@st.cache_data
def get_answer(context, user_question):
    openai.api_key = st.session_state.api_key
    prompt = f"""
    다음은 부경대학교 도서관 규정입니다:\n{context}\n\n사용자 질문: {user_question}\n답변:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if st.button("답변 받기"):
    if not api_key:
        st.warning("API Key를 입력하세요.")
    elif not question:
        st.warning("질문을 입력하세요.")
    else:
        with st.spinner("답변 생성 중..."):
            answer = get_answer(rules, question)
            st.success("📚 도서관 챗봇 응답")
            st.write(answer)
