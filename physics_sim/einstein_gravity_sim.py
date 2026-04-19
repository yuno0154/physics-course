import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 설정
st.set_page_config(page_title="중력 렌즈와 시공간의 곡률", layout="wide")

# 에셋 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

img_blackhole = os.path.join(assets_dir, "blackhole.png")
img_reunion = os.path.join(assets_dir, "reunion.png")

# HTML/JavaScript 공통 템플릿
HTML_TEMPLATE = """
<div id="root" style="width: 100%; height: 500px; overflow: hidden; background: #05070a; border-radius: 12px;"></div>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

/* ── 별 배경 ── */
const STARS = Array.from({length:100},(_,i)=>{
    const s=(n)=>{let x=Math.sin(n)*43758.54;return x-Math.floor(x);};
    return { x:s(i*1.1), y:s(i*2.3), r:s(i*3.2)*1.2+0.2, ph:s(i*5)*Math.PI*2 };
});

const drawStars = (ctx, W, H, t) => {
    STARS.forEach(st=>{
        const op = 0.15 + 0.35*Math.sin(st.ph+t*0.001);
        ctx.beginPath(); ctx.arc(st.x*W, st.y*H, st.r, 0, Math.PI*2);
        ctx.fillStyle=`rgba(255,255,255,${op})`; ctx.fill();
    });
};

/* ── 시공간 격자 (Grid) ── */
function drawGrid(ctx, W, H, mode, sunX, sunY, mass) {
    ctx.save();
    ctx.strokeStyle = mode === 'newton' ? 'rgba(100, 116, 139, 0.4)' : 'rgba(99, 102, 241, 0.6)';
    ctx.lineWidth = 1.0;
    const step = 45;
    const cols = Math.ceil(W/step) + 2;
    const rows = Math.ceil(H/step) + 2;

    for (let i = -1; i <= cols; i++) {
        ctx.beginPath();
        for (let j = -1; j <= rows; j++) {
            let px = i * step, py = j * step;
            if (mode === 'einstein') {
                const dx = px - sunX, dy = py - sunY;
                const d = Math.sqrt(dx*dx + dy*dy);
                const force = (mass * 700) / (d + 40); // 질량에 비례하는 왜곡
                px -= (dx / (d + 1)) * force; py -= (dy / (d + 1)) * force;
            }
            if (j === -1) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    for (let j = -1; j <= rows; j++) {
        ctx.beginPath();
        for (let i = -1; i <= cols; i++) {
            let px = i * step, py = j * step;
            if (mode === 'einstein') {
                const dx = px - sunX, dy = py - sunY;
                const d = Math.sqrt(dx*dx + dy*dy);
                const force = (mass * 700) / (d + 40);
                px -= (dx / (d + 1)) * force; py -= (dy / (d + 1)) * force;
            }
            if (i === -1) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    ctx.restore();
}

/* ── 중력 렌즈 시뮬레이션 ── */
function drawLensing(ctx, W, H, mode, mass, t) {
    const sunX = W * 0.5, sunY = H * 0.35, sunR = 40 + mass*2; 
    const earthX = W * 0.5, earthY = H * 0.75;
    drawGrid(ctx, W, H, mode, sunX, sunY, mass);
    drawStars(ctx, W, H, t);
    
    const starRealX = sunX + 5, starRealY = H * 0.08;
    const prog = (t * 0.0006) % 1;

    // 굴절 로직 (아인슈타인은 뉴턴의 2배)
    const deflectionScale = mode === 'einstein' ? mass * 25 : mass * 12.5;

    if (mode === 'newton') {
        // 뉴턴의 예측: 질량에 의한 인력으로 절반만 굴절
        const cpX = sunX + deflectionScale * 0.5, cpY = sunY;
        ctx.strokeStyle = 'rgba(248, 113, 113, 0.4)'; ctx.lineWidth = 2; ctx.setLineDash([5,5]);
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.quadraticCurveTo(cpX, cpY, earthX, earthY); ctx.stroke();
        ctx.setLineDash([]);
    } else {
        // 아인슈타인의 예측: 시공간 곡률에 의한 2배 굴절 (중력 렌즈)
        const cpX = sunX + deflectionScale, cpY = sunY;
        ctx.strokeStyle = '#6366f1'; ctx.lineWidth = 3; 
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.quadraticCurveTo(cpX, cpY, earthX, earthY); ctx.stroke();
        
        // 겉보기 위치 (측지선의 연장선)
        const appStarX = sunX + deflectionScale * 1.8, appStarY = 40; 
        ctx.strokeStyle = 'rgba(99,102,241,0.5)'; ctx.setLineDash([6,4]);
        ctx.beginPath(); ctx.moveTo(earthX, earthY); ctx.lineTo(appStarX, appStarY); ctx.stroke(); ctx.setLineDash([]);
        
        ctx.save(); ctx.shadowBlur=20; ctx.shadowColor='#818cf8';
        ctx.beginPath(); ctx.arc(appStarX, appStarY, 7, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
        ctx.fillStyle='#fff'; ctx.font='bold 13px Noto Sans KR'; ctx.textAlign='left';
        ctx.fillText('관측된 겉보기 위치 (Shifted)', appStarX + 15, appStarY + 5);
    }
    
    // 광자 애니메이션
    const cpX_anim = sunX + (mode === 'einstein' ? deflectionScale : deflectionScale*0.5);
    const px = (1-prog)*(1-prog)*starRealX + 2*(1-prog)*prog*cpX_anim + prog*prog*earthX;
    const py = (1-prog)*(1-prog)*starRealY + 2*(1-prog)*prog*sunY + prog*prog*earthY;
    ctx.save(); ctx.shadowBlur = 15; ctx.shadowColor = mode==='einstein'?'#6366f1':'#f87171';
    ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();

    // 렌즈 천체 (태양/블랙홀)
    const sg = ctx.createRadialGradient(sunX, sunY, sunR*0.7, sunX, sunY, sunR*1.7);
    sg.addColorStop(0, 'rgba(253, 224, 71, 0.3)'); sg.addColorStop(1, 'transparent');
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR*1.7, 0, Math.PI*2); ctx.fillStyle=sg; ctx.fill();
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR, 0, Math.PI*2); ctx.fillStyle='#000'; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.4)'; ctx.lineWidth=2; ctx.stroke();

    // 지구
    const eg = ctx.createRadialGradient(earthX-5, earthY-5, 3, earthX, earthY, 25);
    eg.addColorStop(0,'#3b82f6'); eg.addColorStop(1,'#1e3a8a');
    ctx.beginPath(); ctx.arc(earthX, earthY, 25, 0, Math.PI*2); ctx.fillStyle=eg; ctx.fill();
    ctx.fillStyle='#fff'; ctx.font='bold 14px Noto Sans KR'; ctx.textAlign='center';
    ctx.fillText('지구 (관측자)', earthX, earthY + 45);
    
    // 별 실제 위치 마커
    ctx.beginPath(); ctx.arc(starRealX, starRealY, 6, 0, Math.PI*2); ctx.fillStyle='#fbbf24'; ctx.fill();
    ctx.fillStyle='#fbbf24'; ctx.font='bold 13px Noto Sans KR'; ctx.textAlign='right';
    ctx.fillText('실제 위치  ', starRealX - 8, starRealY + 5);
}

/* ── 시간 대시보드 (고정형) ── */
function drawDashboard(ctx, clocks) {
    const sX = 15, sY = 15, bW = 180, bH = 160;
    ctx.fillStyle = 'rgba(15, 23, 42, 0.95)'; ctx.strokeStyle = 'rgba(99, 102, 241, 0.6)';
    ctx.lineWidth = 2; ctx.beginPath(); ctx.rect(sX, sY, bW, bH); ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.font = 'bold 14px Noto Sans KR'; ctx.textAlign = 'center';
    ctx.fillText('🕒 시간 흐름 비교', sX + bW/2, sY + 25);
    const renderClock = (y, label, time, color) => {
        ctx.save(); ctx.translate(sX + 30, y);
        ctx.beginPath(); ctx.arc(0, 0, 14, 0, Math.PI*2); ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.rotate(time * 0.002); ctx.lineTo(0, -11); ctx.stroke();
        ctx.restore();
        ctx.fillStyle = color; ctx.font = 'bold 12px Noto Sans KR'; ctx.textAlign = 'left';
        ctx.fillText(label, sX + 55, y - 5);
        ctx.font = '12px monospace'; ctx.fillText(time.toFixed(1), sX + 55, y + 10);
    };
    renderClock(sY + 60, 'A (지면/정지)', clocks.A, '#3b82f6');
    renderClock(sY + 105, 'B (중심/회전)', clocks.B, '#10b981');
    renderClock(sY + 150, 'C (끝단/가속)', clocks.C, '#f59e0b');
}

/* ── 회전 원판 ── */
function drawRotatingDisk(ctx, W, H, vel, t, clocks, pov) {
    const cx = W*0.5, cy = H*0.45, r = 160;
    const ang = t * 0.001 * vel;
    drawStars(ctx, W, H, t);
    ctx.save();
    if (pov === 'B') { ctx.translate(cx, cy); }
    else if (pov === 'C') {
        ctx.translate(cx, cy); ctx.rotate(-ang);
        ctx.translate(-r * 0.85, 0); ctx.translate(cx, cy);
    } else { ctx.translate(cx, cy); ctx.rotate(ang); }
    const grad = ctx.createRadialGradient(0,0, r*0.8, 0,0, r);
    grad.addColorStop(0, 'rgba(30, 41, 59, 0.9)'); grad.addColorStop(1, 'rgba(71, 85, 105, 0.4)');
    ctx.beginPath(); ctx.arc(0,0, r, 0, Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth = 2; ctx.stroke();
    for(let i=0; i<360; i+=30) {
        const rad = i*Math.PI/180; ctx.beginPath(); ctx.moveTo(r*0.85*Math.cos(rad), r*0.85*Math.sin(rad));
        ctx.lineTo(r*Math.cos(rad), r*Math.sin(rad)); ctx.stroke();
    }
    ctx.beginPath(); ctx.arc(0,0, 10, 0, Math.PI*2); ctx.fillStyle='#10b981'; ctx.fill();
    const cx_off = r * 0.85; ctx.beginPath(); ctx.arc(cx_off, 0, 10, 0, Math.PI*2); ctx.fillStyle='#f59e0b'; ctx.fill();
    ctx.restore();
    if (pov === 'A') {
        const ax = cx - r - 60, ay = cy; ctx.beginPath(); ctx.arc(ax, ay, 10, 0, Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill();
    } else {
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(-ang); ctx.beginPath(); ctx.arc(-r - 60, 0, 10, 0, Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill(); ctx.restore();
    }
    drawDashboard(ctx, clocks);
    ctx.fillStyle = '#fff'; ctx.font = 'bold 15px Noto Sans KR'; ctx.textAlign = 'center';
    ctx.fillText("회전 원판과 시간의 상대성 (등가 원리)", W*0.5, H - 20);
}

const Main = () => {
    const canvasRef = React.useRef(null);
    const [t, setT] = React.useState(0);
    const [clocks, setClocks] = React.useState({ A: 0, B: 0, C: 0 });

    React.useEffect(() => {
        let frame;
        const loop = (t_val) => {
            setT(t_val);
            setClocks(prev => {
                const speed = (window.stParams?.speed || 1);
                const discVel = (window.stParams?.discVel || 1);
                const factorC = Math.max(0.1, 1 - (discVel * 0.08)); 
                return { A: prev.A + 0.1 * speed, B: prev.B + 0.1 * speed, C: prev.C + 0.1 * speed * factorC };
            });
            frame = requestAnimationFrame(loop);
        };
        frame = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(frame);
    }, []);

    React.useEffect(() => {
        const ctx = canvasRef.current.getContext('2d');
        const W = 800, H = 500;
        const mode = window.stParams?.mode || 'lensing';
        const pov = window.stParams?.pov || 'A';
        ctx.clearRect(0, 0, W, H);
        if (mode === 'lensing') {
            const theory = window.stParams?.theory || 'einstein';
            const mass = window.stParams?.mass || 5;
            drawLensing(ctx, W, H, theory, mass, t);
        } else {
            const discVel = window.stParams?.discVel || 1;
            drawRotatingDisk(ctx, W, H, discVel, t, clocks, pov);
        }
    }, [t, clocks]);

    return <canvas ref={canvasRef} width={800} height={500} style={{ width: '100%', height: '500px', borderRadius: '12px' }} />;
};

ReactDOM.render(<Main />, document.getElementById('root'));
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
body { font-family: 'Noto Sans KR', sans-serif; background: transparent; margin: 0; padding: 0; overflow: hidden; }
</style>
"""

def render_ui():
    st.markdown("### 🌌 중력 렌즈와 시공간의 곡률: 우주의 돋보기")
    
    tab1, tab2 = st.tabs(["🔭 중력 렌즈 (시공간 왜곡)", "🎡 등가 원리 (회전 원판)"])
    
    with tab1:
        col1, col2 = st.columns([1, 2.5])
        with col1:
            st.info("**중력 렌즈와 시공간 곡률**")
            mass = st.slider("렌즈 천체 질량 (Mass)", 1, 10, 5)
            theory = st.radio("물리 모델 선택", ["newton", "einstein"], 
                              format_func=lambda x: "뉴턴 (질량 인력 - 1.0x)" if x=="newton" else "아인슈타인 (시공간 곡률 - 2.0x)")
            
            with st.expander("📖 원리 보기"):
                st.markdown("""
                - **시공간 곡률**: 질량이 시공간을 휘게 하며, 빛은 그 휘어진 경로(측지선)를 따라갑니다.
                - **중력 렌즈**: 질량이 돋보기처럼 빛을 모으거나 왜곡시키는 현상입니다.
                - **뉴턴 vs 아인슈타인**: 아인슈타인은 뉴턴보다 **2배 더 큰** 별빛의 휘어짐을 예측했고, 이는 1919년 일식 관측으로 증명되었습니다.
                """)
            
            st.write("---")
            st.markdown("**🔍 탐구 포인트**")
            st.write(f"- 질량이 `{mass}`일 때, 아인슈타인 모델의 시공간 왜곡은 뉴턴 모델의 **2배**입니다.")
            st.write("- 별의 겉보기 위치가 실제 위치보다 더 멀리 벗어나 보이는 현상을 관찰하세요.")
            
        with col2:
            components.html(f"<script>window.stParams = {{ mode: 'lensing', theory: '{theory}', mass: {mass} }};</script>" + HTML_TEMPLATE, height=520)

    with tab2:
        col_c, col_v = st.columns([1.2, 2.5])
        with col_c:
            st.success("**회전 원판: 중력과 가속도의 관계**")
            pov = st.radio("관찰 시점(POV)", ["A", "B", "C"], index=0,
                           format_func=lambda x: f"POV {x}" + (" (지면)" if x=='A' else " (중심)" if x=="B" else " (가장자리)"))
            disc_vel = st.slider("원판 회전 속도 (ω)", 0.5, 10.0, 5.0)
            
            st.markdown("**📊 분석 데이터**")
            inquiry_data = [
                {"관측": "A (정지)", "C의 운동": "원운동", "원인": "속도 (SR)"},
                {"관측": "B (중심)", "C의 운동": "정지", "원인": "가속계 시차 (GR)"},
                {"관측": "C (가중)", "C의 운동": "정지", "원인": "관성력 (Equiv)"}
            ]
            st.table(inquiry_data)
        with col_v:
            components.html(f"<script>window.stParams = {{ mode: 'disk', pov: '{pov}', discVel: {disc_vel}, speed: 1.0 }};</script>" + HTML_TEMPLATE, height=520)

    st.write("---")
    st.markdown("#### 🎬 영화 '인터스텔라'와 일반 상대성 이론")
    c1, c2 = st.columns(2)
    with c1:
        st.image(img_blackhole, use_container_width=True, caption="블랙홀 가르강튀아는 우주에서 가장 강력한 중력 렌즈입니다.")
        st.markdown("**중력 렌즈의 극치** : 블랙홀 주변의 빛이 완전히 꺾여 고리 모양(`Einstein Ring`)을 형성하는 것을 볼 수 있습니다.")
    with c2:
        st.image(img_reunion, use_container_width=True, caption="서로 다른 시간의 흐름이 만든 극적인 재회")
        st.markdown("**시간의 상대성** : 중력이 강할수록 시공간이 더 많이 휘어지고, 시간은 상대적으로 느리게 흐릅니다.")
    
    st.info("💡 **현대 천문학의 핵심**: 중력 렌즈는 보이지 않는 '암흑 물질'을 찾거나, 아주 멀리 있는 우주 초기의 은하를 관측하는 핵심 도구로 사용됩니다.")

if __name__ == "__main__":
    render_ui()
