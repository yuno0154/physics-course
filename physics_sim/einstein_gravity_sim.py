import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 설정
st.set_page_config(page_title="아인슈타인의 중력: 시공간의 마술", layout="wide")

# 에셋 경로 설정 (상대 경로 및 환경 호환성 확보)
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

img_blackhole = os.path.join(assets_dir, "blackhole.png")
img_reunion = os.path.join(assets_dir, "reunion.png")
img_logic = os.path.join(assets_dir, "disk_logic.png")

# HTML/JavaScript 공통 템플릿
HTML_TEMPLATE = """
<div id="root"></div>
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
function drawGrid(ctx, W, H, mode, sunX, sunY) {
    ctx.save();
    ctx.strokeStyle = mode === 'newton' ? 'rgba(100, 116, 139, 0.4)' : 'rgba(99, 102, 241, 0.6)';
    ctx.lineWidth = 1.2;
    const step = 45;
    const cols = Math.ceil(W/step) + 2;
    const rows = Math.ceil(H/step) + 2;

    for (let i = -1; i <= cols; i++) {
        ctx.beginPath();
        for (let j = -1; j <= rows; j++) {
            let px = i * step, py = j * step;
            if (mode === 'einstein') {
                const dx = px - sunX, dy = py - sunY;
                const dist = Math.sqrt(dx*dx + dy*dy);
                const force = 3500 / (dist + 60); 
                px -= (dx / (dist + 1)) * force;
                py -= (dy / (dist + 1)) * force;
            }
            if (j === -1) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    for (let j = -1; j <= rows; j++) {
        ctx.beginPath();
        for (let i = -1; i <= cols; i++) {
            let px = i * step, py = j * step;
            if (mode === 'einstein') {
                const dx = px - sunX, dy = py - sunY;
                const dist = Math.sqrt(dx*dx + dy*dy);
                const force = 3500 / (dist + 60);
                px -= (dx / (dist + 1)) * force;
                py -= (dy / (dist + 1)) * force;
            }
            if (i === -1) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    ctx.restore();
}

/* ── 에딩턴의 일식 ── */
function drawEddington(ctx, W, H, mode, t) {
    const sunX = W * 0.5, sunY = H * 0.45, sunR = 60;
    const earthX = W * 0.5, earthY = H * 0.92;
    drawGrid(ctx, W, H, mode, sunX, sunY);
    drawStars(ctx, W, H, t);
    
    const starRealX = sunX + 5, starRealY = H * 0.08;
    const prog = (t * 0.0006) % 1;

    if(mode === 'newton') {
        ctx.strokeStyle = 'rgba(255,255,255,0.2)'; ctx.lineWidth = 1.5; ctx.setLineDash([5,5]);
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.lineTo(earthX, earthY); ctx.stroke(); ctx.setLineDash([]);
        const hitSunY = sunY - sunR * 0.92;
        const currentT = Math.min(1, prog / 0.4); 
        const beamY = starRealY + (hitSunY - starRealY) * currentT;
        ctx.save(); ctx.shadowBlur = 10; ctx.shadowColor = '#fff';
        ctx.beginPath(); ctx.arc(starRealX, beamY, 3.5, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
        ctx.fillStyle='#f87171'; ctx.font='bold 15px Noto Sans KR'; ctx.textAlign='center';
        ctx.fillText('뉴턴: 평평한 시공간 (빛의 직진)', sunX, sunY - 120);
        ctx.fillText('→ 태양에 빛이 차단됨', sunX, sunY - 98);
    } else {
        ctx.strokeStyle = '#6366f1'; ctx.lineWidth = 3; 
        const cpX = sunX + 130, cpY = sunY;
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.quadraticCurveTo(cpX, cpY, earthX, earthY); ctx.stroke();
        const appStarX = sunX + 220, appStarY = 40; 
        ctx.strokeStyle = 'rgba(99,102,241,0.5)'; ctx.setLineDash([6,4]);
        ctx.beginPath(); ctx.moveTo(earthX, earthY); ctx.lineTo(appStarX, appStarY); ctx.stroke(); ctx.setLineDash([]);
        const px = (1-prog)*(1-prog)*starRealX + 2*(1-prog)*prog*cpX + prog*prog*earthX;
        const py = (1-prog)*(1-prog)*starRealY + 2*(1-prog)*prog*cpY + prog*prog*earthY;
        ctx.save(); ctx.shadowBlur = 15; ctx.shadowColor = '#6366f1';
        ctx.beginPath(); ctx.arc(px, py, 4.5, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
        ctx.save(); ctx.shadowBlur=20; ctx.shadowColor='#818cf8';
        ctx.beginPath(); ctx.arc(appStarX, appStarY, 7, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
        ctx.fillStyle='#fff'; ctx.font='bold 13px Noto Sans KR'; ctx.textAlign='left';
        ctx.fillText('관측된 겉보기 위치', appStarX + 15, appStarY + 5);
        ctx.fillStyle='#818cf8'; ctx.font='bold 15px Noto Sans KR'; ctx.textAlign='center';
        ctx.fillText('아인슈타인: 휘어진 시공간 (빛의 우회)', sunX, sunY - 140);
    }
    ctx.beginPath(); ctx.arc(starRealX, starRealY, 6, 0, Math.PI*2); ctx.fillStyle='#fbbf24'; ctx.fill();
    ctx.fillStyle='#fbbf24'; ctx.font='bold 13px Noto Sans KR'; ctx.textAlign='right';
    ctx.fillText('실제 위치   ', starRealX - 8, starRealY + 5);
    const sg = ctx.createRadialGradient(sunX, sunY, sunR*0.7, sunX, sunY, sunR*1.7);
    sg.addColorStop(0, 'rgba(253, 224, 71, 0.5)'); sg.addColorStop(1, 'transparent');
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR*1.7, 0, Math.PI*2); ctx.fillStyle=sg; ctx.fill();
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR, 0, Math.PI*2); ctx.fillStyle='#000'; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.4)'; ctx.lineWidth=1.5; ctx.stroke();
    const eg = ctx.createRadialGradient(earthX-6, earthY-6, 3, earthX, earthY, 28);
    eg.addColorStop(0,'#3b82f6'); eg.addColorStop(1,'#1e3a8a');
    ctx.beginPath(); ctx.arc(earthX, earthY, 28, 0, Math.PI*2); ctx.fillStyle=eg; ctx.fill();
}

/* ── 회전 원판 ── */
function drawRotatingDisk(ctx, W, H, vel, t, clocks, discStep) {
    const cx = W*0.5, cy = H*0.5, r = 240;
    const ang = t * 0.001 * vel;

    if (discStep === 2 || discStep === 3) {
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(-ang); ctx.translate(-cx, -cy);
        drawStars(ctx, W, H, t); ctx.restore();
    } else {
        drawStars(ctx, W, H, t);
    }

    ctx.save();
    if (discStep === 2 || discStep === 3) ctx.translate(cx, cy);
    else { ctx.translate(cx, cy); ctx.rotate(ang); }
    
    const grad = ctx.createRadialGradient(0,0, r*0.8, 0,0, r);
    grad.addColorStop(0, 'rgba(30, 41, 59, 0.9)'); grad.addColorStop(1, 'rgba(71, 85, 105, 0.4)');
    ctx.beginPath(); ctx.arc(0,0, r, 0, Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth=2; ctx.stroke();
    
    for(let i=0; i<360; i+=30) {
        const rad = i*Math.PI/180;
        ctx.beginPath(); ctx.moveTo(r*0.85*Math.cos(rad), r*0.85*Math.sin(rad));
        ctx.lineTo(r*Math.cos(rad), r*Math.sin(rad)); ctx.stroke();
    }
    
    ctx.beginPath(); ctx.arc(0,0, 10, 0, Math.PI*2); ctx.fillStyle='#10b981'; ctx.fill();
    drawLabel(ctx, 0, -20, 'B (중심)');
    drawSmallClock(ctx, 0, 15, clocks.B, '#10b981');

    const cx_off = r * 0.85, cy_off = 0;
    ctx.beginPath(); ctx.arc(cx_off, cy_off, 10, 0, Math.PI*2); ctx.fillStyle='#f59e0b'; ctx.fill();
    drawLabel(ctx, cx_off, -20, 'C (가장자리)');
    drawSmallClock(ctx, cx_off, 15, clocks.C, '#f59e0b');
    
    if (discStep === 3) {
        ctx.strokeStyle='#ef4444'; ctx.lineWidth=4;
        ctx.beginPath(); ctx.moveTo(cx_off, cy_off); ctx.lineTo(cx_off + 60, 0); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx_off+60, 0); ctx.lineTo(cx_off+50, -5); ctx.lineTo(cx_off+50, 5); ctx.closePath(); ctx.fillStyle='#ef4444'; ctx.fill();
        ctx.fillStyle='#ef4444'; ctx.font='bold 14px Noto Sans KR'; ctx.fillText('강력한 관성력', cx_off+10, 40);
    }
    ctx.restore();

    if (discStep === 1 || discStep === 4) {
        const ax = cx - r - 80, ay = cy;
        ctx.beginPath(); ctx.arc(ax, ay, 10, 0, Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill();
        drawLabel(ctx, ax, -20, 'A (지면)');
        drawSmallClock(ctx, ax, 15, clocks.A, '#3b82f6');
    }

    ctx.fillStyle = '#fff'; ctx.font = '16px Noto Sans KR'; ctx.textAlign = 'center';
    let msg = discStep === 1 ? "Step 1: 지면 관찰자 A가 볼 때, C는 매우 빠르게 회전 운동을 합니다." :
              discStep === 2 ? "Step 2: 중심 관찰자 B가 볼 때, 원판은 정지해 있고 외부 우주가 회전합니다." :
              discStep === 3 ? "Step 3: 가장자리 관찰자 C는 강력한 관성력(가속도)을 직접 느낍니다." :
                               "Step 4 (결론): 가속도 = 중력(등가 원리). 따라서 가속되는 C의 시간이 가장 느립니다.";
    ctx.fillText(msg, W*0.5, H - 40);
}

function drawLabel(ctx, x, y, txt) {
    ctx.fillStyle='#fff'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
    ctx.fillText(txt, x, y);
}

function drawSmallClock(ctx, x, y, time, color) {
    ctx.save(); ctx.translate(x, y + 25);
    ctx.beginPath(); ctx.arc(0,0, 20, 0, Math.PI*2); ctx.strokeStyle=color; ctx.lineWidth=2; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0,0); ctx.rotate(time * 0.002); ctx.lineTo(0, -15); ctx.stroke();
    ctx.restore();
    ctx.fillStyle=color; ctx.font='12px monospace'; ctx.fillText(time.toFixed(1), x, y + 60);
}

const Main = () => {
    const canvasRef = React.useRef(null);
    const [t, setT] = React.useState(0);
    const [clocks, setClocks] = React.useState({ A: 0, B: 0, C: 0 });

    React.useEffect(() => {
        let frame;
        const loop = (time) => {
            setT(time);
            setClocks(prev => {
                const speed = (window.stParams?.speed || 1);
                const discVel = (window.stParams?.discVel || 1);
                const factorC = Math.max(0.2, 1 - (discVel * 0.08)); 
                return { A: prev.A + 0.1 * speed, B: prev.B + 0.1 * speed, C: prev.C + 0.1 * speed * factorC };
            });
            frame = requestAnimationFrame(loop);
        };
        frame = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(frame);
    }, []);

    React.useEffect(() => {
        const ctx = canvasRef.current.getContext('2d');
        const { width: W, height: H } = canvasRef.current;
        const mode = window.stParams?.mode || 'eddington';
        const discStep = window.stParams?.discStep || 1;
        ctx.clearRect(0, 0, W, H);
        if (mode === 'eddington') {
            const theory = window.stParams?.theory || 'newton';
            drawEddington(ctx, W, H, theory, t);
        } else {
            const discVel = window.stParams?.discVel || 1;
            drawRotatingDisk(ctx, W, H, discVel, t, clocks, discStep);
        }
    }, [t, clocks]);

    return <canvas ref={canvasRef} width={800} height={600} style={{ width: '100%', height: 'auto', borderRadius: '12px' }} />;
};

ReactDOM.render(<Main />, document.getElementById('root'));
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
body { font-family: 'Noto Sans KR', sans-serif; background: transparent; margin: 0; padding: 0; overflow: hidden; }
</style>
"""

def render_ui():
    st.markdown("### 🌌 아인슈타인의 중력: 시공간의 탐구")
    
    tab1, tab2, tab3 = st.tabs(["🔭 에딩턴의 일식", "🎡 회전 원판 탐구", "🎬 인터스텔라 스토리"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.info("**에딩턴의 일식 실험 (1919)**")
            theory = st.radio("물리 모델 선택", ["newton", "einstein"], 
                              format_func=lambda x: "뉴턴 (평평한 시공간)" if x=="newton" else "아인슈타인 (휘어진 시공간)")
            st.write("---")
            if theory == 'newton':
                st.markdown("빛은 질량이 없으므로 중력의 영향을 받지 않고 직진하며, 태양 뒤의 별은 보이지 않아야 합니다.")
            else:
                st.markdown("중력은 공간을 휘게 하며, 빛은 휘어진 공간을 따라 굴절되어 보이지 않아야 할 별이 관측됩니다.")
        with col2:
            components.html(f"<script>window.stParams = {{ mode: 'eddington', theory: '{theory}' }};</script>" + HTML_TEMPLATE, height=620)

    with tab2:
        col_c, col_v = st.columns([1, 2])
        with col_c:
            st.success("**회전 원판과 등가 원리**")
            disc_step = st.select_slider("탐구 단계", options=[1, 2, 3, 4], format_func=lambda x: f"Step {x}")
            disc_vel = st.slider("회전 속도 (ω)", 0.5, 10.0, 3.0)
            st.write("---")
            steps_desc = [
                "**Step 1**: 외부 관찰자 A의 시점. C는 고속 이동 중이므로 특상 이론에 의해 시간이 느려집니다.",
                "**Step 2**: 중심 관찰자 B의 시점. 자신은 정지해 있고 외부 우주가 회전하는 것처럼 보입니다.",
                "**Step 3**: 가장자리 관찰자 C의 시점. 밖으로 튕겨나려는 관성력을 느끼며, 이는 곧 중력과 같습니다.",
                "**Step 4**: 결론. 등가 원리에 의해 가속(관성력)은 중력과 같으며, 중력이 강할수록 시간은 느려집니다."
            ]
            st.markdown(steps_desc[disc_step-1])
        with col_v:
            components.html(f"<script>window.stParams = {{ mode: 'disk', discStep: {disc_step}, discVel: {disc_vel}, speed: 1.0 }};</script>" + HTML_TEMPLATE, height=620)

    with tab3:
        st.markdown("#### 🎬 인터스텔라: 중력 시간 지연의 증거")
        c1, c2 = st.columns(2)
        with c1:
            st.image(img_blackhole, caption="블랙홀 '가르강튀아' 주변의 극심한 시공간 왜곡")
            st.markdown("**밀러 행성에서의 1시간 = 지구의 7년**\n블랙홀의 엄청난 질량으로 인해 시공간이 극도로 휘어져 시간이 매우 천천히 흐릅니다.")
        with c2:
            st.image(img_reunion, caption="시간의 차이를 극복한 쿠퍼와 머피의 재회")
            st.markdown("**늙은 딸과 젊은 아버지**\n중력의 차이가 만들어낸 수십 년의 시차는 상대성 이론이 실제 우주의 법칙임을 보여줍니다.")
        
        st.image(img_logic, caption="관찰자 관점에 따른 시간 지연의 논리적 구조")
        st.info("💡 GPS 위성도 매일 0.00004초의 시간 차이를 상대성 이론으로 보정하고 있습니다.")

if __name__ == "__main__":
    render_ui()
