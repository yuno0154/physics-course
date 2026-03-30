import streamlit as st
import os

# 페이지 설정
st.set_page_config(layout="centered")

st.title("🧩 포물선 운동 실전 연습 문제")
st.markdown("""
지금까지 학습한 내용을 바탕으로 연습 문제를 풀어봅시다. 
각 문제 위에 제시된 **그림**을 보고 상황을 분석해 보세요!
""")

# 이미지 경로 설정
ASSETS_DIR = os.path.join(os.getcwd(), "assets")

# --- 연습 문제 세션 상태 관리 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'ans1' not in st.session_state:
    st.session_state.ans1 = None
if 'ans2' not in st.session_state:
    st.session_state.ans2 = None

# --- 문제 1: 수평 투사 ---
st.divider()
st.subheader("📝 문제 1. 수평 절벽에서의 투사")

# 이미지 출력
img1_path = os.path.join(ASSETS_DIR, "horizontal_cliff.png")
if os.path.exists(img1_path):
    st.image(img1_path, caption="[그림 1] 수평 던지기 상황 도식", use_container_width=True)
else:
    st.warning("그림 파일을 찾을 수 없습니다. (assets/horizontal_cliff.png)")

st.markdown("""
높이가 **20m**인 절벽 끝에서 공을 수평 방향으로 **10m/s**의 속도로 던졌습니다. 
(단, 중력 가속도 $g = 10m/s^2$, 공기 저항은 무시함)
""")

q1 = st.radio(
    "1) 공이 지면에 도달하는 데 걸리는 시간(초)은?",
    ["1초", "2초", "3초", "4초"],
    index=None, key="q1"
)

if q1:
    if q1 == "2초":
        st.success("✅ 정답입니다! (연직 방향 자유 낙하 $h = \\frac{1}{2}gt^2$ 이용)")
    else:
        st.error("❌ 다시 생각해 보세요. 연직 방향은 자유 낙하와 같습니다.")

# --- 문제 2: 비스듬한 투사 ---
st.divider()
st.subheader("📝 문제 2. 비스듬히 차올린 공")

# 이미지 출력
img2_path = os.path.join(ASSETS_DIR, "oblique_launch.png")
if os.path.exists(img2_path):
    st.image(img2_path, caption="[그림 2] 비스듬히 던진 물체의 포물선 궤적", use_container_width=True)
else:
    st.warning("그림 파일을 찾을 수 없습니다. (assets/oblique_launch.png)")

st.markdown("""
지면에서 어떤 물체를 **30m/s**의 속도로 지면과 **30도** 각도로 던졌습니다. 
(단, $\sin 30^\circ = 0.5$, $g = 10m/s^2$)
""")

q2 = st.radio(
    "2) 물체의 최고점 도달 시간(초)은 얼마인가요?",
    ["0.5초", "1초", "1.5초", "3초"],
    index=None, key="q2"
)

if q2:
    if q2 == "1.5초":
        st.success("✅ 정답입니다! (연직 속도 성분 $v_y = v_0 \sin\theta$ 이므로 $vy = 15m/s$, $t = vy/g = 1.5s$)")
    else:
        st.error("❌ 연직 방향 초기 속도 성분을 먼저 구해보세요.")

# --- 피드백 및 시뮬레이션 연결 ---
st.divider()
st.info("💡 문제가 잘 안 풀린다면, 왼쪽 메뉴의 **시뮬레이션** 페이지에서 동일한 값을 입력하여 확인해 보세요!")
