import streamlit as st

st.title("📝 가속도와 포물선 운동 연습 문제")
st.markdown("""
학습한 내용을 바탕으로 연습 문제를 풀어 보세요. 정답을 확인하면 상세한 해설을 볼 수 있습니다.
""")

st.divider()

# --- 1번 문제 ---
st.subheader("💡 문제 1")
st.write("공기 저항이 없을 때, 포물선 운동을 하는 물체의 가속도 방향은?")
q1_options = ["속도의 방향과 같다.", "운동 방향과 수평이다.", "항상 연직 아래 방향이다.", "물체의 질량에 따라 달라진다."]
q1_choice = st.radio("정답을 선택하세요:", q1_options, key="q1")

if st.button("정답 확인 (1번)"):
    if q1_choice == "항상 연직 아래 방향이다.":
        st.success("✅ 정답입니다! 중력만이 작용하므로 가속도는 항상 중력 가속도(g)의 방향인 연직 아래입니다.")
    else:
        st.error("❌ 틀렸습니다. 다시 고민해 보세요.")
        st.info("힌트: 물체에 작용하는 알짜힘(중력)의 방향을 생각해 보세요.")

st.divider()

# --- 2번 문제 ---
st.subheader("💡 문제 2")
st.write("수평으로 $20 m/s$로 던진 물체가 $5초$ 동안 날아가서 지면에 닿았다면, 낙하하는 동안 수평 거리는?")
q2_options = ["4 m", "50 m", "100 m", "200 m"]
q2_choice = st.radio("정답을 선택하세요:", q2_options, key="q2")

if st.button("정답 확인 (2번)"):
    if q2_choice == "100 m":
        st.success("✅ 정답입니다! 수평 방향으로는 등속 직선 운동을 하므로 $x = v_0 \cdot t = 20 \cdot 5 = 100(m)$ 입니다.")
    else:
        st.error("❌ 틀렸습니다.")
        st.latex(r"x = v_x \cdot t")

st.divider()

# --- 3번 문제 ---
st.subheader("💡 문제 3")
st.write("발사 속도가 일정할 때, 수평 거리를 최대화하려면 발사 각도를 몇 도로 설정해야 할까요?")
q3_options = ["30도", "45도", "60도", "90도"]
q3_choice = st.radio("정답을 선택하세요:", q3_options, key="q3")

if st.button("정답 확인 (3번)"):
    if q3_choice == "45도":
        st.success("✅ 정답입니다! $\sin(2\theta)$가 최대가 되는 지점은 $2\theta = 90^\circ$ 즉, $\theta = 45^\circ$일 때입니다.")
    else:
        st.error("❌ 틀렸습니다. 45도일 때 사정 거리가 최대가 됩니다.")

st.divider()
st.info("축하합니다! 연습 문제를 모두 풀어보셨습니다. 궁금한 점은 선생님께 질문하세요.")
