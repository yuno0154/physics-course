import streamlit as st
import streamlit.components.v1 as components
import os

# 헤더 섹션
st.title("📍 [기학] 벡터의 합성과 분해")
st.markdown("벡터의 덧셈(합성), 다중 벡터의 합성, 벡터의 분해, 성분법에 의한 합성을 시각적으로 탐구할 수 있는 가상 실험실")

# HTML 파일 로드
html_path = os.path.join(os.path.dirname(__file__), "vector-sim.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    # Streamlit에 컴포넌트 삽입
    components.html(html_content, height=850, scrolling=True)
else:
    st.error("⚠️ 벡터의 합성과 분해 시뮬레이터 HTML 파일(vector-sim.html)을 찾을 수 없습니다.")
