import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("📹 포물선 운동 영상 분석 실습")
st.markdown("""
스마트폰 카메라로 촬영한 포물선 운동 영상을 **Tracker** 등의 소프트웨어로 분석한 데이터를 업로드하거나 직접 입력하여 정밀 분석을 수행합니다.
""")

st.info("💡 **실습 방법**: Tracker 프로그램에서 추출한 (t, x, y) 좌표 데이터를 아래 표에 입력하거나 엑셀 파일을 업로드하세요.")

# --- 사이드바: 설정 ---
with st.sidebar:
    st.header("⚙️ 분석 설정")
    g_standard = st.radio("참조 중력 가속도 (m/s²)", options=[9.8, 10.0], index=0)
    st.divider()
    st.caption("사곡고등학교 물리학 II 수행평가 지원 도구")

# --- 데이터 입력부 ---
st.subheader("📝 관찰 데이터 입력")

# 입력을 위한 기본 데이터 프레임 생성
if 'video_df' not in st.session_state:
    st.session_state.video_df = pd.DataFrame({
        "시간(t)": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
        "x위치(m)": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        "y위치(m)": [0.0, 0.35, 0.6, 0.75, 0.8, 0.75]
    })

# 데이터 에디터 (사용자가 직접 수정 가능)
edited_df = st.data_editor(
    st.session_state.video_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "시간(t)": st.column_config.NumberColumn(format="%.3f"),
        "x위치(m)": st.column_config.NumberColumn(format="%.3f"),
        "y위치(m)": st.column_config.NumberColumn(format="%.3f"),
    }
)

if st.button("🔄 데이터 분석 실행"):
    st.session_state.video_df = edited_df

df = st.session_state.video_df

# --- 데이터 계산 및 분석 ---
if len(df) > 2:
    # 속도 계산 (중앙 차분법 또는 전방 차분법)
    dt = df["시간(t)"].diff()
    dx = df["x위치(m)"].diff()
    dy = df["y위치(m)"].diff()
    
    df["vx"] = dx / dt
    df["vy"] = dy / dt
    
    # 가속도 계산 (vy의 변화량)
    dvy = df["vy"].diff()
    df["ay"] = dvy / dt
    
    # 평균 가속도(실험적 중력 가속도) 계산 - 속도-시간 그래프의 기울기
    # 유효한(NaN이 아닌) 가속도 값들의 평균
    g_exp = -df["ay"].dropna().mean()
    
    st.divider()
    
    # --- 결과 리포트 ---
    st.subheader("📊 실험 결과 분석 리포트")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("실험적 중력 가속도 (g_exp)", f"{g_exp:.2f} m/s²")
    with c2:
        error = abs(g_exp - g_standard) / g_standard * 100
        st.metric("표준값과의 오차율", f"{error:.1f} %")
    with c3:
        initial_v0 = np.sqrt(df["vx"].iloc[1]**2 + df["vy"].iloc[1]**2) if len(df) > 1 else 0
        st.metric("초기 속도 (추정)", f"{initial_v0:.2f} m/s")

    # --- 그래프 시각화 ---
    st.subheader("📈 실측 데이터 그래프")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("시간-x위치 (등속성 확인)", "시간-y위치 (포물선 확인)", 
                        "시간-vx (수평 속도 보존)", "시간-vy (기울기=중력가속도)"),
        vertical_spacing=0.15
    )

    # x-t
    fig.add_trace(go.Scatter(x=df["시간(t)"], y=df["x위치(m)"], mode='markers+lines', name='x(t)'), row=1, col=1)
    # y-t
    fig.add_trace(go.Scatter(x=df["시간(t)"], y=df["y위치(m)"], mode='markers+lines', name='y(t)', line=dict(color='red')), row=1, col=2)
    # vx-t
    fig.add_trace(go.Scatter(x=df["시간(t)"].iloc[1:], y=df["vx"].iloc[1:], mode='markers+lines', name='vx(t)', line=dict(color='green')), row=2, col=1)
    # vy-t
    fig.add_trace(go.Scatter(x=df["시간(t)"].iloc[1:], y=df["vy"].iloc[1:], mode='markers+lines', name='vy(t)', line=dict(color='orange')), row=2, col=2)

    fig.update_layout(height=700, showlegend=False, plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    # --- 수행평가 가이드 ---
    st.divider()
    with st.expander("📚 수행평가 보고서 작성 가이드"):
        st.markdown(f"""
        1. **실험 목적**: 포물선 운동 영상을 분석하여 수평 및 연직 방향의 운동 특징을 파악한다.
        2. **이론적 배경**: $x = v_{{0x}}t$, $y = v_{{0y}}t - \\frac{{1}}{{2}}gt^2$. $v_y-t$ 그래프의 기울기는 $-g$이다.
        3. **결과 해석**:
           - $x-t$ 그래프가 직선인가? (수평 방향 알짜힘=0 확인)
           - $v_y-t$ 그래프가 직선이며 기울기가 약 ${-g_standard}$인가?
        4. **오차 분석**: 공기 저항, 영상 촬영 시 카메라 각도(왜곡), 기준자(Reference) 설정 오류 등을 고려한다.
        """)

else:
    st.warning("분석을 위해 최소 3개 이상의 데이터 포인트를 입력해 주세요.")
