import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
# st.set_page_config(page_title="물리학 I/II 평균 및 순간 속도 탐구", layout="wide")

st.title("🚀 속도(Velocity)의 정의와 극한 탐구")
st.markdown("""
이 도구는 **평균 속도**의 정의에서 출발하여, 시간 간격($\Delta t$)을 줄임으로써 **순간 속도**의 개념으로 확장되는 과정을 시각화합니다.
""")

# --- 사이드바: 모드 및 시각 설정 ---
with st.sidebar:
    st.header("⚙️ 탐구 설정")
    mode = st.radio("탐구 모드 선택", ["평균 속도 모드", "순간 속도 모드"])
    
    st.markdown("---")
    if mode == "평균 속도 모드":
        st.subheader("⏱️ 시각 설정")
        t1 = st.slider("처음 시각 t₁ (s)", 0.0, 8.0, 2.0, 0.5)
        t2 = st.slider("나중 시각 t₂ (s)", 0.5, 10.0, 6.0, 0.5)
        dt = t2 - t1
    else:
        st.subheader("⏱️ 극한 탐구 설정")
        t1 = st.slider("기준 시각 t (s)", 0.0, 9.0, 4.0, 0.1)
        dt = st.slider("시간 간격 Δt (s)", 0.01, 2.0, 1.0, 0.01)
        t2 = t1 + dt
        st.info(f"선택된 구간: {t1:.2f}s ~ {t2:.2f}s")

# --- 운동 경로 정의 ---
def get_position(t):
    x = t
    y = -0.15 * (t - 5)**2 + 5
    return np.array([x, y])

# 수치적 미분 (순간 속도 계산용)
def get_instantaneous_velocity(t):
    h = 0.0001
    v = (get_position(t + h) - get_position(t)) / h
    return v

# 전체 경로 데이터
t_range = np.linspace(0, 10, 100)
path_points = np.array([get_position(t) for t in t_range])

# 선택된 지점 계산
p1 = get_position(t1)
p2 = get_position(t2)
dr = p2 - p1
v_avg = dr / dt if dt > 0 else np.array([0, 0])
v_inst = get_instantaneous_velocity(t1)

# --- Plotly 시각화 ---
fig = go.Figure()

# 1. 격자 및 축 설정
fig.update_xaxes(range=[-1, 11], dtick=1, showgrid=True, gridcolor='lightgray', zerolinecolor='black', zerolinewidth=2)
fig.update_yaxes(range=[-1, 7], dtick=1, showgrid=True, gridcolor='lightgray', zerolinecolor='black', zerolinewidth=2)

# 2. 운동 경로
fig.add_trace(go.Scatter(x=path_points[:, 0], y=path_points[:, 1], 
                         mode='lines', name='운동 경로 (궤적)', 
                         line=dict(color='gray', width=2, dash='dot')))

# 3. 기준점(Origin)
fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text', name='기준점 (O)',
                         text=['O'], textposition="bottom left",
                         marker=dict(color='black', size=14, line=dict(color='white', width=2))))

# 4. 위치 벡터 (Origin -> P)
fig.add_annotation(x=p1[0], y=p1[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="blue", opacity=0.4)

# 5. 변위 벡터 Δr
fig.add_annotation(x=p2[0], y=p2[1], ax=p1[0], ay=p1[1], xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=4, arrowcolor="purple")
fig.add_annotation(x=(p1[0]+p2[0])/2, y=(p1[1]+p2[1])/2, text="<b>Δ<i>r</i>&#x20d7;</b>", showarrow=False, 
                   font=dict(color="purple", size=18), xshift=15, yshift=15)

# 6. 평균 속도 벡터 v_avg
fig.add_annotation(x=p1[0] + v_avg[0], y=p1[1] + v_avg[1], 
                   ax=p1[0], ay=p1[1], xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=5, arrowcolor="rgba(34, 139, 34, 0.7)")
fig.add_annotation(x=p1[0] + v_avg[0]/2, y=p1[1] + v_avg[1]/2, 
                   text="<b><i>v</i>&#x20d7;<sub>avg</sub></b>", showarrow=False, 
                   font=dict(color="rgba(34, 139, 34, 0.7)", size=16), xshift=-10, yshift=10)

# 7. 순간 속도 벡터 (순간 속도 모드에서만 강조)
if mode == "순간 속도 모드":
    fig.add_annotation(x=p1[0] + v_inst[0], y=p1[1] + v_inst[1], 
                       ax=p1[0], ay=p1[1], xref="x", yref="y", axref="x", ayref="y",
                       text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=8, arrowcolor="darkgreen")
    fig.add_annotation(x=p1[0] + v_inst[0], y=p1[1] + v_inst[1], 
                       text="<b><i>v</i>&#x20d7;<sub>inst</sub> (접선)</b>", showarrow=False, 
                       font=dict(color="darkgreen", size=22), xshift=20, yshift=20)

# 8. 점 P, Q
fig.add_trace(go.Scatter(x=[p1[0], p2[0]], y=[p1[1], p2[1]], mode='markers+text', 
                         text=['P', 'Q' if mode == "평균 속도 모드" or dt > 0.1 else ""], 
                         textposition="top center",
                         marker=dict(color=['blue', 'red'], size=12), showlegend=False))

# 범례
fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='변위 Δr⃗', line=dict(color='purple', width=4)))
fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='평균 속도 v⃗<sub>avg</sub>', line=dict(color='rgba(34, 139, 34, 0.7)', width=5)))
if mode == "순간 속도 모드":
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='순간 속도 v⃗<sub>inst</sub>', line=dict(color='darkgreen', width=8)))

fig.update_layout(height=650, showlegend=True, 
                  margin=dict(l=20, r=20, t=20, b=20),
                  plot_bgcolor='white',
                  legend=dict(font=dict(color="black"), bgcolor="rgba(255, 255, 255, 0.9)", bordercolor="black", borderwidth=1))

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 계산 결과 ---
if mode == "평균 속도 모드":
    st.subheader("📚 평균 속도 교육 콘텐츠")
    with st.expander("⏱️ 평균 속도의 계산", expanded=True):
        latex_formula = r"\vec{v}_{avg} = \frac{\Delta\vec{r}}{\Delta t} = \frac{(%.2f, %.2f)}{%.1f} = (%.2f, %.2f) \text{ m/s}" % (dr[0], dr[1], dt, v_avg[0], v_avg[1])
        st.latex(latex_formula)
        st.info(f"평균 속도의 크기: {np.linalg.norm(v_avg):.2f} m/s")
else:
    st.subheader("📚 순간 속도와 미분 탐구")
    st.markdown(f"**기준 시각 t = {t1}s**에서 시간 간격 **Δt = {dt:.2f}s**를 점차 줄여보세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("📈 **변화하는 평균 속도**")
        st.latex(r"v_{avg} = (%.3f, %.3f)" % (v_avg[0], v_avg[1]))
    with col2:
        st.write("🎯 **목표: 순간 속도 (Δt → 0)**")
        st.latex(r"v_{inst} = (%.3f, %.3f)" % (v_inst[0], v_inst[1]))

    with st.expander("💡 순간 속도의 물리적 의미", expanded=True):
        st.markdown(f"""
        1. **극한(Limit)**: $\Delta t$가 매우 작아질수록 물체는 거의 점 P 주변에 머물게 됩니다.
        2. **접선의 방향**: 그래프를 보면 $\Delta t$가 작아질수록 평균 속도 화살표가 점 P에서의 **접선(Tangent line)**과 일치해가는 것을 볼 수 있습니다.
        3. **미분계수**: 이것이 바로 수학에서 배우는 위치의 시각에 대한 **미분계수**이며, 물리학에서의 **순간 속도**입니다.
        
        $$\\vec{{v}}(t) = \\lim_{{\\Delta t \\to 0}} \\frac{{\\Delta\\vec{{r}}}}{{\\Delta t}} = \\frac{{d\\vec{{r}}}}{{dt}}$$
        """)

st.sidebar.markdown("---")
st.sidebar.caption("사곡고등학교 물리학 시뮬레이션 v1.3")
