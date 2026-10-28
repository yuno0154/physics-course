import streamlit as st
import streamlit.components.v1 as components
import os

# 헤더 섹션
st.title("💹 [융합] 우주 거래소의 시계")
st.markdown("2045년 지구·우주 정거장·달 기지의 주민이 같은 주식을 주문할 때, **거리에 따른 시간 차**(신호 지연)와 **상대성에 따른 시간 차**(중력 효과·속도 효과)를 구별하고, 시각을 환산해 공정한 체결 순서를 판단하는 가상 실험실")
st.caption("① 시계 맞추기 → ② 주문하기 → ③ 하루가 지나면 → ④ 체결 비교 · 활동지 C~F와 연계")

# HTML 파일 로드
html_path = os.path.join(os.path.dirname(__file__), "space-exchange.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=1500, scrolling=True)
else:
    st.error("⚠️ 우주 거래소의 시계 시뮬레이터 HTML 파일(space-exchange.html)을 찾을 수 없습니다.")
