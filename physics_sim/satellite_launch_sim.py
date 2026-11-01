import os

import streamlit as st
import streamlit.components.v1 as components

# ============================================================
#  수행평가 자료: 위성 발사·궤도 시뮬레이션 (학생 관찰용)
#  - 평가지 [자료 1~3]의 상황을 학생이 직접 움직여 관찰하는 페이지
#  - 평가 답안을 직접 제공하지 않도록 교사 시연용에서
#    힌트, 계산 확인, 힘 비교 막대, 필요한 에너지 표시, 운동량 막대,
#    원 궤도 속력 기준선, 식의 각 항 이름표를 제거한 버전
# ============================================================

st.title("🚀 [수행자료] 위성 발사·궤도 시뮬레이션")
st.markdown(
    "평가지 **[자료 1~3]**의 상황을 직접 움직여 보며 관찰하는 가상 실험입니다. "
    "화면의 값은 평가지 자료와 같으며, 답안은 **식과 자료를 근거로** 서술합니다."
)

html_path = os.path.join(os.path.dirname(__file__), "satellite-launch-sim.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=1750, scrolling=True)
else:
    st.error("⚠️ 시뮬레이션 HTML 파일(satellite-launch-sim.html)을 찾을 수 없습니다.")
