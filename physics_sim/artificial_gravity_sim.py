import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 설정
st.set_page_config(page_title="인공중력 통합 탐구 시스템", layout="wide")

# ── 사이드바 통합 제어판 ──
st.sidebar.title("🧬 MISSION CONTROL")
st.sidebar.markdown("---")
# 슬라이더 - 물리량 제어 (모든 시뮬레이션 공유)
radius_val = st.sidebar.slider("정거장 반지름 (r) [m]", 100, 1000, 500, step=50)
omega_val = st.sidebar.slider("회전 각속도 (ω) [rad/s]", 0.05, 0.40, 0.15, step=0.01)

accel = radius_val * (omega_val ** 2)
g_force = accel / 9.8

st.sidebar.info(f"""
**[실시간 시스템 데이터]**
- 반 지 름: {radius_val} m
- 각 속 도: {omega_val:.2f} rad/s
- 모사중력: {accel:.2f} m/s²
- 중력세기: {g_force:.2f} G
""")

# ── 메인 타이틀 ──
st.title("🛰️ 인공중력 우주 정거장: 통합 탐구 시스템")
st.markdown("상단의 시네마틱 뷰로 현상을 관찰하고, 하단의 듀얼 시ミュ레이션으로 물리 법칙을 분석해 보세요.")

# ── 1. 상단: 시네마틱 오리지널 뷰 (복원) ──
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

    function drawSpace(cx, cy) {{
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
        // Spokes
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 6;
        for(let i=0; i<6; i++) {{
            let a = i*Math.PI/3; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(Math.cos(a)*120, Math.sin(a)*120); ctx.stroke();
        }}
        // Ring
        ctx.strokeStyle = '#475569'; ctx.lineWidth = 20;
        ctx.beginPath(); ctx.arc(0,0, 120, 0, Math.PI*2); ctx.stroke();
        // Hub
        ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.arc(0,0, 30, 0, Math.PI*2); ctx.fill();
        ctx.restore();
    }}

    function render() {{
        drawSpace();
        const cx = canvas.width/2+150, cy = canvas.height/2;
        earthAngle += 0.0002; angle += omega * 0.016;
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

# ── 2. 중단: 듀얼 프레임 시뮬레이션 창 (관성계 vs 비관성계) ──
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🌍 외부 관찰 시점 (Inertial Frame)")
    inertial_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; background: #000; overflow: hidden; font-family: sans-serif; }}
            #label {{ position: absolute; top: 10px; left: 10px; color: white; font-size: 12px; font-weight: 800; background: rgba(0,0,0,0.5); padding: 5px; }}
        </style>
    </head>
    <body>
        <div id="label">관성계: 정거장 회전 | 배경 고정</div>
        <canvas id="inertialCanvas"></canvas>
    <script>
        const canvas = document.getElementById('inertialCanvas');
        const ctx = canvas.getContext('2d');
        const omega = {omega_val};
        const accelVal = {accel};
        let angle = 0;

        function resize() {{ canvas.width = window.innerWidth; canvas.height = 400; }}
        resize();

        function drawInertial() {{
            ctx.fillStyle = "black"; ctx.fillRect(0,0,canvas.width, canvas.height);
            const cx = canvas.width/2, cy = canvas.height/2;
            angle += omega * 0.016;

            // 1. 별 배경 (고정)
            ctx.fillStyle="white"; for(let i=0; i<50; i++) ctx.fillRect(Math.sin(i)*canvas.width, Math.cos(i*i)*canvas.height, 1, 1);

            // 2. 정거장 링
            ctx.strokeStyle = "#2c3e50"; ctx.lineWidth = 30; ctx.beginPath(); ctx.arc(cx, cy, 140, 0, Math.PI*2); ctx.stroke();

            // 3. 우주인 (회전)
            const ax = cx + Math.cos(angle)*135;
            const ay = cy + Math.sin(angle)*135;
            ctx.fillStyle = "white"; ctx.save(); ctx.translate(ax, ay); ctx.rotate(angle-Math.PI/2); ctx.fillRect(-7,-10, 14, 18); ctx.restore();

            // 4. 수직항력 (N) - 중심 방향
            const len = Math.max(30, accelVal*1.8);
            ctx.save(); ctx.translate(ax, ay); ctx.rotate(angle + Math.PI);
            ctx.strokeStyle = "#ef4444"; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(len, 0); ctx.stroke();
            ctx.fillStyle="#ef4444"; ctx.beginPath(); ctx.moveTo(len, 0); ctx.lineTo(len-10, -5); ctx.lineTo(len-10, 5); ctx.fill();
            ctx.rotate(- (angle+Math.PI)); ctx.font="bold 12px sans-serif"; ctx.fillText("수직항력 (N)", 15, -15);
            ctx.restore();

            requestAnimationFrame(drawInertial);
        }
        drawInertial();
    </script>
    </body>
    </html>
    """
    components.html(inertial_html, height=400)

with col2:
    st.markdown("#### 👩‍🚀 내부 우주인 시점 (Non-Inertial Frame)")
    rotating_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; background: #000; overflow: hidden; font-family: sans-serif; }}
            #label {{ position: absolute; top: 10px; left: 10px; color: #10b981; font-size: 12px; font-weight: 800; background: rgba(0,0,0,0.5); padding: 5px; }}
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

        function resize() {{ canvas.width = window.innerWidth; canvas.height = 400; }}
        resize();

        function drawRotating() {{
            ctx.fillStyle = "black"; ctx.fillRect(0,0,canvas.width, canvas.height);
            const cx = canvas.width/2, cy = canvas.height/2;
            angle += omega * 0.016;

            // 1. 별 배경 (거꾸로 회전)
            ctx.save(); ctx.translate(cx, cy); ctx.rotate(-angle); ctx.fillStyle="white"; 
            for(let i=0; i<50; i++) ctx.fillRect((Math.sin(i)*1.5)*cx, (Math.cos(i*i)*1.5)*cy, 1, 1);
            ctx.restore();

            // 2. 정거장 링 (고정)
            ctx.strokeStyle = "#2c3e50"; ctx.lineWidth = 30; ctx.beginPath(); ctx.arc(cx, cy, 140, 0, Math.PI*2); ctx.stroke();

            // 3. 우주인 (고정 - 3시 방향)
            const ax = cx + 135, ay = cy;
            ctx.fillStyle = "white"; ctx.save(); ctx.translate(ax, ay); ctx.rotate(-Math.PI/2); ctx.fillRect(-7,-10, 14, 18); ctx.restore();

            // 4. 원심력 & 수직항력 평형
            const len = Math.max(30, accelVal*1.8);
            // 원심력 (바깥)
            ctx.strokeStyle = "#10b981"; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ax+len, ay); ctx.stroke();
            ctx.fillStyle="#10b981"; ctx.beginPath(); ctx.moveTo(ax+len, ay); ctx.lineTo(ax+len-10, ay-5); ctx.lineTo(ax+len-10, ay+5); ctx.fill();
            ctx.fillText("원심력", ax+20, ay+20);
            
            // 수직항력 (안쪽)
            ctx.strokeStyle = "#ef4444"; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ax-len, ay); ctx.stroke();
            ctx.fillStyle="#ef4444"; ctx.beginPath(); ctx.moveTo(ax-len, ay); ctx.lineTo(ax-len+10, ay-5); ctx.lineTo(ax-len+10, ay+5); ctx.fill();
            ctx.fillText("수직항력 (N)", ax-len, ay-15);

            requestAnimationFrame(drawRotating);
        }
        drawRotating();
    </script>
    </body>
    </html>
    """
    components.html(rotating_html, height=400)

# ── 3. 하단: 비교 분석표 및 리퍼런스 (복원) ──
st.markdown("---")
st.markdown("### 🔍 프레임별 물리 현상 분석")

st.markdown("""
<style>
    .physics-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .physics-table th { background: #0f172a; color: white; padding: 12px; border: 1px solid #334155; }
    .physics-table td { background: white; padding: 12px; border: 1px solid #e2e8f0; text-align: center; }
</style>
<table class="physics-table">
    <thead>
        <tr>
            <th>구분</th>
            <th>🌍 외부 관찰자 (관성계)</th>
            <th>👩‍🚀 내부 우주인 (비관성계)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="font-weight:bold;">운동의 기술</td>
            <td>정거장과 함께 원운동</td>
            <td>정거장 내 정지 상태</td>
        </tr>
        <tr>
            <td style="font-weight:bold;">발생하는 힘</td>
            <td><b>수직항력(N)</b> 하나만 존재</td>
            <td><b>수직항력(N)</b> + <b>원심력(가성력)</b></td>
        </tr>
        <tr>
            <td style="font-weight:bold;">물리적 평형</td>
            <td>수직항력이 <b>구심력</b> 역할</td>
            <td>두 힘의 합력이 0 (평형)</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# 쿠퍼 스테이션 이미지 데이터
st.markdown("#### 🪐 인공중력의 실제 모델")
base_img_path = "physics_sim/" if os.path.exists("physics_sim/cooper_exterior.png") else ""
col_a, col_b = st.columns(2)
with col_a:
    ext_img = base_img_path + "cooper_exterior.png"
    if os.path.exists(ext_img): st.image(ext_img, caption="Cooper Station Exterior View", use_container_width=True)
with col_b:
    int_img = base_path + "cooper_interior.png"
    if os.path.exists(int_img): st.image(int_img, caption="Cooper Station Interior View", use_container_width=True)

st.markdown("""
> [!NOTE]
> **탐구 가이드**: 상단의 고화질 뷰에서 정거장이 회전하는 모습 전체를 감상한 후, 
> 중단의 시뮬레이션을 통해 외부 관찰자(관성계)와 내부 우주인(비관성계)이 왜 서로 다르게 운동을 해석하는지 비교해 보세요.
""")

def run():
    pass

if __name__ == "__main__":
    run()
