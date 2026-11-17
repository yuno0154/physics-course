import streamlit as st
import streamlit.components.v1 as components
import os

# 헤더 섹션
st.title("🚀 [탐구] 뉴턴 대포: 던진 포탄에서 인공위성까지")
st.markdown("산꼭대기에서 수평으로 쏜 포탄의 발사 속력을 바꾸며 지면에 떨어지는 운동, 원 궤도, 타원 궤도를 비교하는 가상 실험실 (활동지 19쪽 E-1. 뉴턴 대포)")

# HTML 파일 로드
html_path = os.path.join(os.path.dirname(__file__), "newton-cannon-sim.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=1150, scrolling=True)
else:
    st.error("⚠️ 뉴턴 대포 시뮬레이터 HTML 파일(newton-cannon-sim.html)을 찾을 수 없습니다.")
