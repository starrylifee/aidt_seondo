import streamlit as st
from langchain_teddynote import logging
from langchain_openai import ChatOpenAI
import os

# secrets.toml 파일에서 환경 변수 로드
try:
    openai_api_key = st.secrets["openai"]["api_key"]
    langchain_project = st.secrets["langchain"]["project"]
    langchain_endpoint = st.secrets["langchain"]["endpoint"]
    langchain_api_key = st.secrets["langchain"]["api_key"]
except KeyError as e:
    st.error(f"필수 API 키 또는 설정이 누락되었습니다: {e}")
    openai_api_key = None
    langchain_project = None
    langchain_endpoint = None
    langchain_api_key = None

if openai_api_key and langchain_project and langchain_api_key and langchain_endpoint:
    # 환경 변수 설정
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    os.environ["LANGCHAIN_ENDPOINT"] = langchain_endpoint
    
    # LangChain 프로젝트 설정
    try:
        logging.langsmith(langchain_project)
    except Exception as e:
        st.error(f"LangChain 프로젝트 설정 중 오류가 발생했습니다: {e}")

    # ChatOpenAI 객체 생성
    try:
        llm = ChatOpenAI(
            temperature=0.1,  # 창의성 (0.0 ~ 2.0)
            model_name="gpt-4",  # 모델명
            openai_api_key=openai_api_key  # API 키 전달
        )
    except Exception as e:
        llm = None
        st.error(f"ChatOpenAI 객체 생성 중 오류가 발생했습니다: {e}")

    if llm:
        st.title("LangChain OpenAI Chat Example")
        user_input = st.text_area("질문을 입력하세요:", "대한민국의 아름다운 관광지 10곳과 주소를 알려주세요!", height=200)

        if st.button("질문하기"):
            try:
                # 스트림 방식으로 질의
                answer = llm.stream(user_input)

                # 응답 출력
                with st.spinner('답변을 기다리는 중...'):
                    response = []
                    response_container = st.empty()  # Create a container for the response
                    for token in answer:
                        response.append(token.content)
                        response_text = ''.join(response)
                        response_container.write(response_text)  # Update the container with the new content
                    
            except Exception as e:
                st.error(f"질의 중 오류가 발생했습니다: {e}")
else:
    st.error("API 키가 설정되지 않았습니다. secrets.toml 파일을 확인해주세요.")

# Add custom CSS to handle word wrapping
st.markdown(
    """
    <style>
    .stTextArea textarea {
        white-space: pre-wrap;  /* CSS3 */
        white-space: -moz-pre-wrap; /* Firefox */
        white-space: -pre-wrap; /* Opera 4-6 */
        white-space: -o-pre-wrap; /* Opera 7 */
        word-wrap: break-word; /* Internet Explorer 5.5+ */
    }
    </style>
    """,
    unsafe_allow_html=True
)
