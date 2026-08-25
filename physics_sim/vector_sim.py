import streamlit as st
import streamlit.components.v1 as components
import os

# 공통 스타일 시트
st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.info-card {
    background: linear-gradient(135deg, #1e3a8a, #0f172a);
    border-left: 5px solid #3b82f6;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
}
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown("<h1 class='main-title'>📍 [기학] 벡터의 합성과 분해</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: -5px;'>벡터의 덧셈(합성), 다중 벡터의 합성, 벡터의 분해, 성분법에 의한 합성을 시각적으로 탐구할 수 있는 가상 실험실</p>", unsafe_allow_html=True)

# HTML 파일 로드
html_path = os.path.join(os.path.dirname(__file__), "vector-sim.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    # Streamlit에 컴포넌트 삽입
    components.html(html_content, height=850, scrolling=True)
else:
    st.error("⚠️ 벡터의 합성과 분해 시뮬레이터 HTML 파일(vector-sim.html)을 찾을 수 없습니다.")
