import streamlit as st
import numpy as np

st.title("📝 포물선 운동 실전 연습 문제")
st.markdown("""
학습지 수준의 실전 문제입니다. 각 단계별 풀이 과정을 머리속으로 정리하며 정답을 입력해 보세요.
(단, 모든 문제에서 중력 가속도 $g = 10 m/s^2$으로 계산합니다.)
""")

st.divider()

# --- 문제 1: 수평으로 던진 물체 ---
st.header("1️⃣ 수평으로 던진 물체의 운동")
st.image("https://raw.githubusercontent.com/yuno0154/physics-course/main/assets/prob1.png", caption="문제 1 상황도 (20m 높이, 20m/s 발사)") # 실제 경로는 유동적일 수 있으나 구조상 표시

st.info("**[조건]** 높이 $20m$에서 질량 $2kg$인 물체를 수평 방향 $20m/s$로 던졌습니다. ($g = 10 m/s^2$)")

# (1) 1초 후 속도의 크기
st.subheader("(1) 1초 후 속도의 크기를 구하시오.")
ans1_1 = st.number_input("답 (m/s):", key="ans1_1")
if st.button("정답 확인 (1-1)"):
    # vx = 20, vy = 10*1 = 10. v = sqrt(20^2 + 10^2) = sqrt(500) = 10*sqrt(5) approx 22.36
    correct_val = np.sqrt(20**2 + 10**2)
    if abs(ans1_1 - correct_val) < 0.1 or abs(ans1_1 - 22.36) < 0.1:
        st.success(f"✅ 정답입니다! ($v_x=20, v_y=10 \\rightarrow v=\\sqrt{{500}} \\approx 22.36$ m/s)")
    else:
        st.error("❌ 다시 계산해 보세요. 수평 속도와 연직 속도를 피타고라스 정리로 합산해야 합니다.")

# (2) 지면 도달 시간
st.subheader("(2) 지면에 도달하는 데 걸린 시간을 구하시오.")
ans1_2 = st.number_input("답 (s):", key="ans1_2")
if st.button("정답 확인 (1-2)"):
    # h = 1/2 gt^2 -> 20 = 5t^2 -> t^2 = 4 -> t = 2
    if ans1_2 == 2:
        st.success("✅ 정답입니다! ($20 = \\frac{1}{2} \\cdot 10 \\cdot t^2 \\rightarrow t=2$초)")
    else:
        st.error("❌ 틀렸습니다. 낙하 거리 h=20m를 이용하여 계산하세요.")

# (3) 수평 도달 거리
st.subheader("(3) 수평 도달 거리를 구하시오.")
ans1_3 = st.number_input("답 (m):", key="ans1_3")
if st.button("정답 확인 (1-3)"):
    # R = v0 * t = 20 * 2 = 40
    if ans1_3 == 40:
        st.success("✅ 정답입니다! ($R = 20 m/s \\cdot 2s = 40m$)")
    else:
        st.error("❌ 틀렸습니다. (수평 속도 × 낙하 시간)")

st.divider()

# --- 문제 2: 비스듬히 던진 물체 ---
st.header("2️⃣ 비스듬히 위로 던진 물체의 운동")
st.info("**[조건]** 지면에서 질량 $2kg$인 물체를 $30^\circ$ 각도로 $40m/s$로 던졌습니다. ($g = 10 m/s^2$)")

# (1) 공식 확인
st.subheader("(1) 등가속도 운동 공식을 완성하시오.")
st.latex(r"v = v_0 + at")
st.latex(r"s = v_0t + \frac{1}{2}at^2")
st.latex(r"v^2 - v_0^2 = 2as")

# (3) 1초 후 속도의 크기
st.subheader("(2) 1초 후 속도의 크기를 구하시오.")
ans2_3 = st.number_input("답 (m/s):", key="ans2_3")
if st.button("정답 확인 (2-2)"):
    # v0x = 40 * cos(30) = 40 * sqrt(3)/2 = 20*sqrt(3) approx 34.64
    # v0y = 40 * sin(30) = 20
    # vy(1s) = 20 - 10*1 = 10
    # v = sqrt((20*sqrt(3))^2 + 10^2) = sqrt(1200 + 100) = sqrt(1300) approx 36.06
    correct_val = np.sqrt((20*np.sqrt(3))**2 + 10**2)
    if abs(ans2_3 - 36.06) < 0.1:
        st.success(f"✅ 정답입니다! ($v_x \\approx 34.64, v_y = 10 \\rightarrow v \\approx 36.06$ m/s)")
    else:
        st.error(f"❌ 틀렸습니다. (힌트: 1초 후 vy = {20-10} m/s)")

# (4) 최고점의 높이
st.subheader("(3) 최고점의 높이를 구하시오.")
ans2_4 = st.number_input("답 (m):", key="ans2_4")
if st.button("정답 확인 (2-3)"):
    # H = (v0y^2) / 2g = 20^2 / 20 = 400 / 20 = 20
    if ans2_4 == 20:
        st.success("✅ 정답입니다! ($H = \\frac{20^2}{2 \cdot 10} = 20m$)")
    else:
        st.error("❌ 틀렸습니다. 연직 처음 속도 v0y=20m/s를 이용하세요.")

# (5) 수평 도달 거리
st.subheader("(4) 수평 도달 거리를 구하시오.")
ans2_5 = st.number_input("답 (m):", key="ans2_5")
if st.button("정답 확인 (2-4)"):
    # t_H = 20/10 = 2s. Total t = 4s.
    # R = v0x * 4 = 20*sqrt(3) * 4 = 80*sqrt(3) approx 138.56
    correct_val = 80 * np.sqrt(3)
    if abs(ans2_5 - 138.56) < 0.1:
        st.success(f"✅ 정답입니다! ($R = 34.64 m/s \\cdot 4s \\approx 138.56m$)")
    else:
        st.error("❌ 틀렸습니다. (수평 속도 × 전체 비행 시간)")

st.divider()
st.info("💡 모든 문제를 해결하셨습니다! 이론과 시뮬레이션을 비교해 보며 복습해 보세요.")
