import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 설정
st.set_page_config(page_title="인공중력 통합 탐구 시스템", layout="wide")

# ── 1. 메인 타이틀 및 소개 ──
st.title("🛰️ 인공중력 우주 정거장: 통합 탐구 시스템")
st.markdown("정거장의 반지름과 각속도를 조절하여 인공중력이 어떻게 형성되는지 탐구해 보세요.")

st.markdown("---")

# ── 2. 물리량 정밀 제어판 (Main Logic) ──
st.subheader("⚙️ STATION PARAMETERS (정밀 제어)")
ctrl_col1, ctrl_col2 = st.columns(2)

with ctrl_col1:
    st.write("**반지름 (r) [m]**")
    # 슬라이더와 넘버 인풋 연동을 위해 세션 상태를 활용하거나 간단히 순차 정의
    radius_val = st.slider("r_slider", 100, 1000, 500, step=50, label_visibility="collapsed")
    radius_val = st.number_input("정확한 반지름 입력", 100, 1000, radius_val, step=10)

with ctrl_col2:
    st.write("**각속도 (ω) [rad/s]**")
    omega_val = st.slider("w_slider", 0.01, 1.00, 0.15, step=0.01, label_visibility="collapsed")
    omega_val = st.number_input("정확한 각속도 입력", 0.01, 1.00, omega_val, step=0.01)

# 물리 계산 로직
accel = radius_val * (omega_val ** 2)
g_force = accel / 9.8

# 실시간 물리 데이터 대시보드 (Metric)
m1, m2, m3 = st.columns(3)
m1.metric("가속도 (a = rω²)", f"{accel:.2f} m/s²")
m2.metric("체감 중력 (G-force)", f"{g_force:.2f} G", delta=f"{(g_force-1.0):.2f} G" if abs(g_force-1.0)>0.01 else "Earth Normal")
m3.info(f"💡 현재 설정은 지구 중력의 {g_force*100:.1f}% 입니다.")

st.markdown("---")

# ── 3. 상단: 시네마틱 오리지널 뷰 ──
st.subheader("🎬 Cinematic Overview")
cinematic_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background: #010409; overflow: hidden; }}
        canvas {{ display: block; }}
    </style>
</head>
<body>
    <canvas id="cinemaCanvas"></canvas>
<script>
    const canvas = document.getElementById('cinemaCanvas');
    const ctx = canvas.getContext('2d');
    const omega = {omega_val};
    let angle = 0;
    let earthAngle = 0;

    function resize() {{ canvas.width = window.innerWidth; canvas.height = 350; }}
    window.onresize = resize; resize();

    function drawSpace() {{
        ctx.fillStyle = "#010409"; ctx.fillRect(0,0,canvas.width, canvas.height);
        for(let i=0; i<150; i++) {{
            let x = (Math.sin(i*77.7)*0.5+0.5)*canvas.width;
            let y = (Math.cos(i*123.4)*0.5+0.5)*canvas.height;
            ctx.fillStyle = "rgba(255,255,255,0.6)"; ctx.beginPath(); ctx.arc(x, y, 1, 0, Math.PI*2); ctx.fill();
        }}
    }}
    
    function drawEarth(cx, cy) {{
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(earthAngle);
        const grad = ctx.createRadialGradient(-canvas.width*0.2, -canvas.height*0.2, 50, -canvas.width*0.4, -canvas.height*0.4, 300);
        grad.addColorStop(0, '#3b82f6'); grad.addColorStop(1, '#0e1b3d');
        ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(-canvas.width*0.4, -canvas.height*0.3, 180, 0, Math.PI*2); ctx.fill();
        ctx.restore();
    }}

    function drawStation(cx, cy) {{
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(angle);
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 6;
        for(let i=0; i<6; i++) {{
            let a = i*Math.PI/3; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(Math.cos(a)*120, Math.sin(a)*120); ctx.stroke();
        }}
        ctx.strokeStyle = '#475569'; ctx.lineWidth = 20;
        ctx.beginPath(); ctx.arc(0,0, 120, 0, Math.PI*2); ctx.stroke();
        ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.arc(0,0, 30, 0, Math.PI*2); ctx.fill();
        ctx.restore();
    }}

    function render() {{
        drawSpace();
        const cx = canvas.width/2+150, cy = canvas.height/2;
        angle += omega * 0.016;
        drawEarth(cx, cy);
        drawStation(cx, cy);
        requestAnimationFrame(render);
    }}
    render();
</script>
</body>
</html>
"""
components.html(cinematic_html, height=350)

st.markdown("---")

# ── 4. 중단: 듀얼 프레임 시뮬레이션 창 (관성계 vs 비관성계) ──
st.subheader("🔭 차원별 프레임 분석 (Inertial vs Rotating)")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🌍 외부 관찰 시점 (Inertial Frame)")
    inertial_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; background: #000; overflow: hidden; font-family: sans-serif; }}
            #label {{ position: absolute; top: 10px; left: 10px; color: white; font-size: 11px; font-weight: 800; background: rgba(0,0,0,0.5); padding: 5px; border: 1px solid white; }}
        </style>
    </head>
    <body>
        <div id="label">관성계: 배경 고정 | 정거장 회전</div>
        <canvas id="inertialCanvas"></canvas>
    <script>
        const canvas = document.getElementById('inertialCanvas');
        const ctx = canvas.getContext('2d');
        const omega = {omega_val};
        const accelVal = {accel};
        let angle = 0;

        function resize() {{ canvas.width = window.innerWidth; canvas.height = 380; }}
        resize();

        function drawInertial() {{
            ctx.fillStyle = "black"; ctx.fillRect(0,0,canvas.width, canvas.height);
            const cx = canvas.width/2, cy = canvas.height/2;
            angle += omega * 0.016;

            ctx.fillStyle="white"; for(let i=0; i<30; i++) ctx.fillRect(Math.sin(i)*canvas.width, Math.cos(i*i)*canvas.height, 1, 1);
            ctx.strokeStyle = "#2c3e50"; ctx.lineWidth = 25; ctx.beginPath(); ctx.arc(cx, cy, 130, 0, Math.PI*2); ctx.stroke();

            const ax = cx + Math.cos(angle)*125; const ay = cy + Math.sin(angle)*125;
            ctx.fillStyle = "white"; ctx.save(); ctx.translate(ax, ay); ctx.rotate(angle-Math.PI/2); ctx.fillRect(-6,-9, 12, 16); ctx.restore();

            const len = Math.max(30, accelVal * 1.5);
            ctx.save(); ctx.translate(ax, ay); ctx.rotate(angle + Math.PI);
            ctx.strokeStyle = "#ef4444"; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(len, 0); ctx.stroke();
            ctx.fillStyle="#ef4444"; ctx.beginPath(); ctx.moveTo(len, 0); ctx.lineTo(len-10, -5); ctx.lineTo(len-10, 5); ctx.fill();
            ctx.rotate(- (angle+Math.PI)); ctx.font="bold 12px sans-serif"; ctx.fillText("수직항력 (N)", 15, -15);
            ctx.restore();

            requestAnimationFrame(drawInertial);
        }}
        drawInertial();
    </script>
    </body>
    </html>
    """
    components.html(inertial_html, height=380)

with col2:
    st.markdown("#### 👩‍🚀 내부 우주인 시점 (Non-Inertial Frame)")
    rotating_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; background: #000; overflow: hidden; font-family: sans-serif; }}
            #label {{ position: absolute; top: 10px; left: 10px; color: #10b981; font-size: 11px; font-weight: 800; background: rgba(0,0,0,0.5); padding: 5px; border: 1px solid #10b981; }}
        </style>
    </head>
    <body>
        <div id="label">비관성계: 정거장 고정 | 배경 회전</div>
        <canvas id="rotatingCanvas"></canvas>
    <script>
        const canvas = document.getElementById('rotatingCanvas');
        const ctx = canvas.getContext('2d');
        const omega = {omega_val};
        const accelVal = {accel};
        let angle = 0;

        function resize() {{ canvas.width = window.innerWidth; canvas.height = 380; }}
        resize();

        function drawRotating() {{
            ctx.fillStyle = "black"; ctx.fillRect(0,0,canvas.width, canvas.height);
            const cx = canvas.width/2, cy = canvas.height/2;
            angle += omega * 0.016;

            ctx.save(); ctx.translate(cx, cy); ctx.rotate(-angle); ctx.fillStyle="white"; 
            for(let i=0; i<30; i++) ctx.fillRect((Math.sin(i)*1.5)*cx, (Math.cos(i*i)*1.5)*cy, 1, 1);
            ctx.restore();

            ctx.strokeStyle = "#2c3e50"; ctx.lineWidth = 25; ctx.beginPath(); ctx.arc(cx, cy, 130, 0, Math.PI*2); ctx.stroke();

            const ax = cx + 125, ay = cy;
            ctx.fillStyle = "white"; ctx.save(); ctx.translate(ax, ay); ctx.rotate(-Math.PI/2); ctx.fillRect(-6,-9, 12, 16); ctx.restore();

            const len = Math.max(30, accelVal * 1.5);
            ctx.strokeStyle = "#10b981"; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ax+len, ay); ctx.stroke();
            ctx.fillStyle="#10b981"; ctx.beginPath(); ctx.moveTo(ax+len, ay); ctx.lineTo(ax+len-10, ay-5); ctx.lineTo(ax+len-10, ay+5); ctx.fill();
            ctx.fillText("원심력", ax+20, ay+20);
            
            ctx.strokeStyle = "#ef4444"; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ax-len, ay); ctx.stroke();
            ctx.fillStyle="#ef4444"; ctx.beginPath(); ctx.moveTo(ax-len, ay); ctx.lineTo(ax-len+10, ay-5); ctx.lineTo(ax-len+10, ay+5); ctx.fill();
            ctx.fillText("수직항력 (N)", ax-len, ay-15);

            requestAnimationFrame(drawRotating);
        }}
        drawRotating();
    </script>
    </body>
    </html>
    """
    components.html(rotating_html, height=380)

# ── 5. 하단: 비교 분석표 및 자료 ──
st.markdown("---")
st.markdown("### 📊 관성계 vs 비관성계 심층 비교")

# 답변 숨기기 기능 추가 (페다고지컬 기능)
show_answers = st.toggle("🔍 분석 결과 확인하기", value=False, help="먼저 관성계와 비관성계에서 힘의 평형이 어떻게 다를지 생각해 본 뒤 버튼을 눌러보세요.")

# 표 내용 동적 할당
q_move = "정거장과 함께 원운동 중" if show_answers else "💬 스스로 추론해 보세요..."
q_force = "수직항력 (중심 방향)" if show_answers else "💬 어떤 힘들이 작용할까요?"
q_law = "<b>구심력(N) = mrω²</b>" if show_answers else "💬 알짜힘의 관계는?"

r_move = "정거장 내부에서 정지 중" if show_answers else "💬 스스로 추론해 보세요..."
r_force = "수직항력(N) + 원심력(Inertial)" if show_answers else "💬 이곳에만 존재하는 가상의 힘은?"
r_law = "<b>N = 원심력</b> (힘의 평형)" if show_answers else "💬 무엇과 무엇이 평형일까요?"

st.markdown(f"""
<table style="width:100%; border-collapse: collapse; background: white; color: black; border: 1px solid #ddd;">
    <tr style="background: #0f172a; color: white;">
        <th style="padding: 10px; border: 1px solid #444;">분석 항목</th>
        <th style="padding: 10px; border: 1px solid #444;">🌍 외부 관찰자 (관성계)</th>
        <th style="padding: 10px; border: 1px solid #444;">👩‍🚀 내부 우주인 (비관성계)</th>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">해석되는 운동</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{q_move}</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{r_move}</td>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">작용하는 힘</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{q_force}</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{r_force}</td>
    </tr>
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold;">물리 법칙 적용</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{q_law}</td>
        <td style="padding: 10px; border: 1px solid #ddd;">{r_law}</td>
    </tr>
</table>
""", unsafe_allow_html=True)

# 리퍼런스 이미지
st.markdown("#### 🪐 쿠퍼 스테이션 데이터 시각화")
base_path = "physics_sim/"
col_a, col_b = st.columns(2)
with col_a:
    ext_img = base_path + "cooper_exterior.png"
    if os.path.exists(ext_img): st.image(ext_img, caption="영화 인터스텔라: 쿠퍼 스테이션 외부 원경", use_container_width=True)
with col_b:
    int_img = base_path + "cooper_interior.png"
    if os.path.exists(int_img): st.image(int_img, caption="영화 인터스텔라: 쿠퍼 스테이션 내부 주거 구역", use_container_width=True)

st.info("💡 팁: 반지름을 키우고 각속도를 높일수록 내부 우주인이 받는 인공중력(수직항력)의 세기가 강해지는 것을 실시간으로 관찰할 수 있습니다.")
