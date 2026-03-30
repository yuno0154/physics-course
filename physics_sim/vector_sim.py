import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
# st.set_page_config(page_title="물리학 I/II 벡터 시각화 도구", layout="wide")

st.title("📍 위치 벡터와 변위 탐구")
st.markdown("""
이 도구는 **위치 벡터**와 **변위 벡터**의 관계를 시각적으로 이해하고 계산 과정을 학습하기 위해 제작되었습니다.
좌측 사이드바에서 점 A와 B의 좌표를 자유롭게 변경해 보세요.
""")

# --- 사이드바: 입력값 설정 ---
with st.sidebar:
    st.header("📌 좌표 설정")
    st.info("격자 위 점 A와 B의 위치를 정해 주세요.")
    ax = st.number_input("점 A의 x좌표 (A_x)", value=5)
    ay = st.number_input("점 A의 y좌표 (A_y)", value=2)
    st.markdown("---")
    bx = st.number_input("점 B의 x좌표 (B_x)", value=7)
    by = st.number_input("점 B의 y좌표 (B_y)", value=-1)

# --- 벡터 계산 ---
vec_a = np.array([ax, ay])
vec_b = np.array([bx, by])
disp = vec_b - vec_a  # 변위 벡터 (B - A)
dist = np.linalg.norm(disp) # 변위의 크기

# --- Plotly 시각화 ---
fig = go.Figure()

# 1. 격자 및 축 설정
fig.update_xaxes(range=[-2, 12], dtick=1, showgrid=True, gridcolor='lightgray', zerolinecolor='black', zerolinewidth=2)
fig.update_yaxes(range=[-6, 8], dtick=1, showgrid=True, gridcolor='lightgray', zerolinecolor='black', zerolinewidth=2)

# 2. 기준점(Origin) 표시
fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text', name='기준점 (O)',
                         text=['O'], textposition="bottom left",
                         marker=dict(color='black', size=14, line=dict(color='white', width=2))))

# 3. 위치 벡터 A (Origin -> A)
fig.add_annotation(x=ax, y=ay, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=3, arrowcolor="blue")
fig.add_annotation(x=ax/2, y=ay/2, text="<b><i>r</i>&#x20d7;<sub>A</sub></b>", showarrow=False, 
                   font=dict(color="blue", size=18), xshift=15, yshift=15)
fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='위치 벡터 r⃗<sub>A</sub>', line=dict(color='blue', width=3)))

# 4. 위치 벡터 B (Origin -> B)
fig.add_annotation(x=bx, y=by, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=3, arrowcolor="red")
fig.add_annotation(x=bx/2, y=by/2, text="<b><i>r</i>&#x20d7;<sub>B</sub></b>", showarrow=False, 
                   font=dict(color="red", size=18), xshift=15, yshift=15)
fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='위치 벡터 r⃗<sub>B</sub>', line=dict(color='red', width=3)))

# 5. 변위 벡터 (A -> B)
fig.add_annotation(x=bx, y=by, ax=ax, ay=ay, xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=4, arrowcolor="purple")
fig.add_annotation(x=(ax+bx)/2, y=(ay+by)/2, text="<b>Δ<i>r</i>&#x20d7;</b>", showarrow=False, 
                   font=dict(color="purple", size=20), xshift=20, yshift=20)
fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='변위 벡터 Δr⃗', line=dict(color='purple', width=4)))

# 6. 점 A, B 표시
fig.add_trace(go.Scatter(x=[ax, bx], y=[ay, by], mode='markers+text', 
                         text=['A', 'B'], textposition="top center",
                         marker=dict(color='black', size=12, symbol='circle'), showlegend=False))

fig.update_layout(height=650, showlegend=True, 
                  margin=dict(l=20, r=20, t=20, b=20),
                  plot_bgcolor='white',
                  legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01,
                              font=dict(color="black", size=12),
                              bgcolor="rgba(255, 255, 255, 0.9)", bordercolor="black", borderwidth=1))

# 메인 화면에 그래프 출력
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 계산 결과 및 핵심 개념 (클릭 시 나타나도록 구성) ---
st.subheader("📚 단계별 학습 및 계산 결과")

with st.expander("📍 1단계: 위치 벡터(Position Vector)의 정의", expanded=False):
    st.markdown("""
    **핵심 개념:** 기준점$O(0,0)$에서 어떤 점까지 이은 화살표를 그 점의 **위치 벡터**라고 합니다.
    보통 점 $A$의 위치 벡터는 $\\vec{r}_A$로 나타냅니다.
    """)
    st.info(f"**점 A의 위치 벡터:** $\\vec{{r}}_A = ({ax}, {ay})$")
    st.info(f"**점 B의 위치 벡터:** $\\vec{{r}}_B = ({bx}, {by})$")

with st.expander("↔️ 2단계: 변위 벡터(Displacement Vector)의 계산", expanded=False):
    st.markdown("""
    **핵심 개념:** 물체가 처음 위치에서 나중 위치로 이동했을 때의 위치 변화를 **변위**라고 합니다.
    변위는 나중 위치 벡터에서 처음 위치 벡터를 빼서 구할 수 있습니다.
    
    $$\\Delta\\vec{r} = \\vec{r}_B - \\vec{r}_A = (x_B - x_A, y_B - y_y)$$
    """)
    st.success(f"**변위 벡터 $\\Delta\\vec{{r}}$:** $({bx}-{ax}, {by}-{ay}) = ({disp[0]}, {disp[1]})$")
    st.write(f"의미: 점 A에서 점 B로 가기 위해 x방향으로 {disp[0]}, y방향으로 {disp[1]}만큼 이동해야 함을 뜻합니다.")

with st.expander("📏 3단계: 변위의 크기 (피타고라스 정리 활용)", expanded=False):
    st.markdown("""
    **핵심 개념:** 변위 벡터의 크기는 두 지점 사이의 **최단 직선 거리**를 의미합니다.
    격자판 위에서 직각삼각형을 그린다고 생각하고 피타고라스 정리를 적용합니다.
    
    $$|\\Delta\\vec{r}| = \\sqrt{\\Delta x^2 + \\Delta y^2}$$
    """)
    st.latex(rf"|\Delta\vec{{r}}| = \sqrt{{{disp[0]}^2 + ({disp[1]})^2}} = \sqrt{{{disp[0]**2} + {disp[1]**2}}} = \sqrt{{{disp[0]**2 + disp[1]**2}}} \approx {dist:.2f}")
    st.warning(f"**물체가 이동한 직선 거리:** 약 {dist:.2f}")

st.sidebar.markdown("---")
st.sidebar.caption("사곡고등학교 물리학 시뮬레이션 v1.1")
