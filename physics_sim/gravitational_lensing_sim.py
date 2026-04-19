import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 설정
st.set_page_config(page_title="아인슈타인의 중력 실험실", layout="wide")

# 에셋 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

# 생성된 이미지 경로 (에셋 폴더 내 파일 사용)
img_cross = os.path.join(assets_dir, "einstein_cross.png")
img_3d_curve = os.path.join(assets_dir, "spacetime_curvature.png")
img_blackhole = os.path.join(assets_dir, "blackhole.png")
img_reunion = os.path.join(assets_dir, "reunion.png")

# 상단 관측 사례 카드 UI
def render_header_cards():
    st.markdown("#### 🔭 현대 우주론의 결정적 관측 및 이론적 모델")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(img_cross, use_container_width=True, caption="아인슈타인의 십자가 (관측 모델)")
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); padding: 10px; border-radius: 8px;">
            <p style="font-size: 0.8rem; color: #cbd5e1; margin: 0;">중심 은하의 중력으로 뒤쪽 퀘이사의 상이 4개로 분리된 모습입니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.image(img_3d_curve, use_container_width=True, caption="3D 시공간 곡률과 빛의 경로")
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); padding: 10px; border-radius: 8px;">
            <p style="font-size: 0.8rem; color: #cbd5e1; margin: 0;">질량이 시공간을 함몰시키면, 빛은 그 골짜기를 따라 입체적으로 굴절됩니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.7); padding: 15px; border-radius: 12px; border-left: 5px solid #10b981; height: 100%;">
            <strong style="color: #10b981;">허블 딥 필드 (HDF)</strong><br/>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin-top: 8px;">
                중력 렌즈는 '우주의 돋보기' 역할을 하여 인류가 관측할 수 있는 한계를 수십 배 이상 확장해 줍니다. 
                현재 시뮬레이션의 3D 모드로 이 원리를 직접 탐구해 보세요.
            </p>
        </div>
        """, unsafe_allow_html=True)

# 시뮬레이션 HTML/JS 코드
HTML_TEMPLATE = """
<div id="root"></div>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

/* ── 별 배경 ── */
const STARS = Array.from({length:120},(_,i)=>{
    const s=(n)=>{let x=Math.sin(n)*43758.54;return x-Math.floor(x);};
    return { x:s(i*1.1), y:s(i*2.3), r:s(i*3.2)*1.2+0.1, ph:s(i*5)*Math.PI*2 };
});

const drawStars = (ctx, W, H, t) => {
    STARS.forEach(st=>{
        const op = 0.15 + 0.35*Math.sin(st.ph+t*0.001);
        ctx.beginPath(); ctx.arc(st.x*W, st.y*H, st.r, 0, Math.PI*2);
        ctx.fillStyle=`rgba(255,255,255,${op})`; ctx.fill();
    });
};

/* ── 3D 투영 엔진 ── */
const project3D = (x, y, z, W, H) => {
    const angle = 0.45; // 기울기
    const scale = 0.85; 
    const sx = (x - W/2) * scale;
    const sy = (y - H/2) * scale * Math.sin(angle) - z * 0.5; // Z-depth 적용
    return { x: sx + W/2, y: sy + H*0.48 };
};

function drawGrid(ctx, W, H, sunX, sunY, mass, isLensing) {
    if(!isLensing) return;
    ctx.save(); ctx.strokeStyle = 'rgba(99, 102, 241, 0.3)'; ctx.lineWidth = 0.8;
    const step = 40;
    const getZ = (x, y) => {
        const dx = x - sunX, dy = y - sunY;
        const d = Math.sqrt(dx*dx + dy*dy);
        return -(mass * 800) / (d/2 + 60); // 질량에 의한 시공간 함몰
    };

    for (let i = -1; i <= W/step+1; i++) {
        ctx.beginPath();
        for (let j = -1; j <= H/step+1; j++) {
            const px = i * step, py = j * step;
            const p = project3D(px, py, getZ(px, py), W, H);
            if (j === -1) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();
    }
    for (let j = -1; j <= H/step+1; j++) {
        ctx.beginPath();
        for (let i = -1; i <= W/step+1; i++) {
            const px = i * step, py = j * step;
            const p = project3D(px, py, getZ(px, py), W, H);
            if (i === -1) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();
    }
    ctx.restore();
}

/* ── 중력 렌즈 시뮬레이터 (3D 고도화) ── */
function drawLensing(ctx, W, H, caseMode, mass, t) {
    const cx = W * 0.5, cy = H * 0.5;
    const rLen = 30 + mass * 4;
    const earthPos = { x: W * 0.5, y: H * 0.85, z: 0 };
    const starRealPos = { x: W * 0.5, y: H * 0.1, z: 0 };
    
    drawStars(ctx, W, H, t);
    drawGrid(ctx, W, H, cx, cy, mass, true);

    // 3D 좌표 보정
    const pE = project3D(earthPos.x, earthPos.y, earthPos.z, W, H);
    const pS = project3D(starRealPos.x, starRealPos.y, starRealPos.z, W, H);
    const pC = project3D(cx, cy, -(mass * 12), W, H); // 은하중심도 살짝 가라앉음

    // 렌즈 천체 (은하단)
    const gradSun = ctx.createRadialGradient(pC.x, pC.y, 0, pC.x, pC.y, rLen * 2);
    gradSun.addColorStop(0, 'rgba(99, 102, 241, 0.5)'); 
    gradSun.addColorStop(1, 'transparent');
    ctx.beginPath(); ctx.arc(pC.x, pC.y, rLen * 2, 0, Math.PI*2); ctx.fillStyle = gradSun; ctx.fill();
    ctx.beginPath(); ctx.arc(pC.x, pC.y, rLen, 0, Math.PI*2); ctx.fillStyle = '#fff'; ctx.fill(); 
    ctx.fillStyle='#a5b4fc'; ctx.font='bold 11px Inter'; ctx.textAlign='center';
    ctx.fillText('중심 은하단 (Gravity Well)', pC.x, pC.y + rLen + 15);

    if (caseMode === 'shift') {
        const deflection = mass * 45;
        // 3D 입체 광선 궤적 (좌우 대칭)
        ctx.strokeStyle='#fbbf24'; ctx.lineWidth=3;
        ctx.shadowColor='#fbbf24'; ctx.shadowBlur=12;

        const drawCurvedPath = (side) => {
            ctx.beginPath();
            ctx.moveTo(pS.x, pS.y);
            const midX = cx + side * deflection;
            const midY = cy;
            const midZ = -(mass * 25); // 중간 지점이 골짜기 아래로 휘어짐
            const pMid = project3D(midX, midY, midZ, W, H);
            ctx.quadraticCurveTo(pMid.x, pMid.y, pE.x, pE.y);
            ctx.stroke();
        };

        drawCurvedPath(1);
        drawCurvedPath(-1);

        // Apparent Positions (가이드라인 포함)
        ctx.shadowBlur=0;
        ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.setLineDash([5,5]);
        const appX = cx + deflection * 1.8;
        const appP = project3D(appX, H * 0.1, 0, W, H);
        ctx.beginPath(); ctx.moveTo(pE.x, pE.y); ctx.lineTo(appP.x, appP.y); ctx.stroke();
        ctx.setLineDash([]);
        
        ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(appP.x, appP.y, 6, 0, Math.PI*2); ctx.fill();
        ctx.fillText(mass > 6 ? '겉보기 위치 A (질량 대)' : '겉보기 위치 B (질량 소)', appP.x, appP.y - 12);

    } else if (caseMode === 'cross') {
        const d = 45 + mass * 3;
        const subPositions = [
            {x:cx+d, y:cy, z:-mass*15}, {x:cx-d, y:cy, z:-mass*15},
            {x:cx, y:cy+d, z:-mass*15}, {x:cx, y:cy-d, z:-mass*15}
        ];
        
        ctx.strokeStyle='rgba(251, 191, 36, 0.7)'; ctx.lineWidth=2;
        ctx.shadowColor='#fbbf24'; ctx.shadowBlur=10;
        
        subPositions.forEach(pos => {
            const pSub = project3D(pos.x, pos.y, pos.z, W, H);
            ctx.beginPath(); ctx.moveTo(pS.x, pS.y); 
            ctx.quadraticCurveTo(pSub.x, pSub.y, pE.x, pE.y);
            ctx.stroke();
            
            // 상 (Image)
            const pImg = project3D(cx + (pos.x-cx)*1.4, cy + (pos.y-cy)*1.4, 0, W, H);
            ctx.fillStyle='#fbbf24'; ctx.beginPath(); ctx.arc(pImg.x, pImg.y, 5, 0, Math.PI*2); ctx.fill();
        });
        ctx.shadowBlur=0;
        ctx.fillStyle='#fbbf24'; ctx.fillText('아인슈타인의 십자가 (Isometric View)', pC.x, pC.y - rLen - 35);
    }

    // 지구
    ctx.beginPath(); ctx.arc(pE.x, pE.y, 22, 0, Math.PI*2); 
    const gradEarth = ctx.createRadialGradient(pE.x-5, pE.y-5, 2, pE.x, pE.y, 22);
    gradEarth.addColorStop(0, '#60a5fa'); gradEarth.addColorStop(1, '#1e40af');
    ctx.fillStyle=gradEarth; ctx.fill();
    ctx.fillStyle='#fff'; ctx.fillText('지구 (관측자)', pE.x, pE.y + 35);
}

/* ── 회전 원판 (등가 원리) ── */
function drawDashboard(ctx, clocks) {
    const sX = 20, sY = 20, bW = 180, bH = 160;
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)'; ctx.strokeStyle = 'rgba(99, 102, 241, 0.6)';
    ctx.lineWidth = 2; ctx.beginPath(); ctx.rect(sX, sY, bW, bH); ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.font = 'bold 14px Inter'; ctx.textAlign = 'center';
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
    renderClock(sY + 100, 'B (중심/회전)', clocks.B, '#10b981');
    renderClock(sY + 140, 'C (가장자리)', clocks.C, '#f59e0b');
}

function drawRotatingDisk(ctx, W, H, vel, t, clocks, pov) {
    const cx = W*0.5, cy = H*0.45, r = 160;
    const ang = t * 0.001 * vel;
    drawStars(ctx, W, H, t);
    ctx.save();
    if (pov === 'B') { ctx.translate(cx, cy); }
    else if (pov === 'C') { ctx.translate(cx, cy); ctx.rotate(-ang); ctx.translate(-r * 0.85, 0); ctx.translate(cx, cy); }
    else { ctx.translate(cx, cy); ctx.rotate(ang); }
    const grad = ctx.createRadialGradient(0,0, r*0.8, 0,0, r);
    grad.addColorStop(0, 'rgba(30, 41, 59, 0.9)'); grad.addColorStop(1, 'rgba(71, 85, 105, 0.4)');
    ctx.beginPath(); ctx.arc(0,0, r, 0, Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth = 2; ctx.stroke();
    ctx.beginPath(); ctx.arc(0,0, 10, 0, Math.PI*2); ctx.fillStyle='#10b981'; ctx.fill();
    ctx.beginPath(); ctx.arc(r*0.85, 0, 10, 0, Math.PI*2); ctx.fillStyle='#f59e0b'; ctx.fill();
    ctx.restore();
    if (pov === 'A') { ctx.beginPath(); ctx.arc(cx - r - 60, cy, 10, 0, Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill(); }
    else { ctx.save(); ctx.translate(cx, cy); ctx.rotate(-ang); ctx.beginPath(); ctx.arc(-r-60,0,10,0,Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill(); ctx.restore(); }
    drawDashboard(ctx, clocks);
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
                const fac = Math.max(0.1, 1 - (discVel * 0.08)); 
                return { A: prev.A + 0.1 * speed, B: prev.B + 0.1 * speed, C: prev.C + 0.1 * speed * fac };
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
        ctx.clearRect(0, 0, W, H);
        if (mode === 'lensing') {
            drawLensing(ctx, W, H, window.stParams.case, window.stParams.mass, t);
        } else {
            drawRotatingDisk(ctx, W, H, window.stParams.discVel, t, clocks, window.stParams.pov);
        }
    }, [t, clocks]);

    return <canvas ref={canvasRef} width={800} height={500} style={{ width: '100%', height: '500px', borderRadius: '12px', background: '#05070a' }} />;
};

ReactDOM.render(<Main />, document.getElementById('root'));
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Noto+Sans+KR:wght@400;700&display=swap');
body { font-family: 'Inter', 'Noto Sans KR', sans-serif; background: transparent; margin: 0; padding: 0; overflow: hidden; color: #fff; }
</style>
"""

# 사이드바 설정
st.sidebar.title("🛠️ 아인슈타인 탐구 메뉴")
mode = st.sidebar.radio("탐구 모드 선택", ["🔭 중력 렌즈 탐구", "🎡 등가 원리 학습", "🎬 인터스텔라 스토리"])

# 통합 UI 렌더링
render_header_cards()
st.write("---")

if mode == "🔭 중력 렌즈 탐구":
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.success("**🔬 중력 렌즈 현상 탐구**")
        case = st.radio("실험 케이스 선택", ["별의 위치 변화 (A/B)", "아인슈타인의 십자가"], index=0)
        mass = st.slider("렌즈 천체(은하단)의 질량", 1.0, 10.0, 5.0)
        
        st.write("---")
        if case == "별의 위치 변화 (A/B)":
            st.markdown("""
            **교과서 탐구 내용**
            - 질량이 작을 때 : 별이 원래 위치와 가까운 **B** 부근에 보임.
            - 질량이 클 때 : 빛이 더 많이 휘어 별이 더 먼 **A** 위치에 보임.
            """)
        else:
            st.markdown("""
            **아인슈타인의 십자가**
            - 매우 먼 곳의 퀘이사 빛이 중간 은하의 중력으로 4개로 쪼개져 보이는 환상적인 현상입니다.
            """)
    with col2:
        case_val = 'shift' if case == "별의 위치 변화 (A/B)" else 'cross'
        components.html(f"<script>window.stParams = {{ mode: 'lensing', case: '{case_val}', mass: {mass}, speed: 1.0 }};</script>" + HTML_TEMPLATE, height=520)

elif mode == "🎡 등가 원리 학습":
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.success("**🎢 가속도와 중력의 등가성**")
        pov = st.radio("관찰 시점 선택", ["A (지면)", "B (중심)", "C (가장자리)"])
        disc_vel = st.slider("원판 회전 속도 (ω)", 0.5, 10.0, 5.0)
        
        st.write("---")
        st.markdown("**특징 요약**")
        if "A" in pov: st.write("- 정지한 지면에서 회전하는 C의 시간이 느려지는 것을 관찰합니다.")
        elif "B" in pov: st.write("- 회전 축에서 주변부가 왜곡되어 보이는 기하학적 효과를 경험합니다.")
        else: st.write("- 가속도를 느끼는 C는 자신을 정지했다 생각하나, 관성력이 중력처럼 작용해 시간이 느려집니다.")
    with col2:
        pov_val = pov[0]
        components.html(f"<script>window.stParams = {{ mode: 'disk', pov: '{pov_val}', discVel: {disc_vel}, speed: 1.0 }};</script>" + HTML_TEMPLATE, height=520)

else:
    # 인터스텔라 스토리
    st.markdown("### 🎬 영화 '인터스텔라'로 배우는 상대성 이론")
    col_img1, col_txt1 = st.columns([1, 1.2])
    with col_img1:
        st.image(img_blackhole, use_container_width=True, caption="블랙홀 가르강튀아")
    with col_txt1:
        st.markdown("""
        #### 1. 블랙홀의 중력 렌즈 효과
        영화 속 블랙홀 주변의 빛나는 고리는 실제 중력 렌즈 효과를 물리적으로 정확히 계산하여 렌더링한 결과입니다.
        빛이 블랙홀을 한 바퀴 돌아 우리에게 오기 때문에 위아래로 고리가 형성됩니다.
        """)
    st.write("")
    col_txt2, col_img2 = st.columns([1.2, 1])
    with col_txt2:
        st.markdown("""
        #### 2. 밀러 행성에서의 1시간 = 지구의 7년
        질량이 무지막지한 블랙홀 주변에서는 시공간 곡률이 극심합니다.
        블랙홀에 가까운 밀러 행성에서는 시간이 매우 느리게 흐르며, 이는 등가 원리에 의해 '강한 중력'이 시간을 느리게 만드는 실제 현상입니다.
        """)
    with col_img2:
        st.image(img_reunion, use_container_width=True, caption="시간의 상대성이 만든 재회")

    st.info("💡 **결론**: 아인슈타인의 일반 상대성 이론은 '중력 = 시공간의 휘어짐'임을 증명하며, 이는 중력 렌즈와 시간 지연이라는 놀라운 현상으로 나타납니다.")
