import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="아인슈타인의 중력 실험실", layout="wide")

current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

img_cross = os.path.join(assets_dir, "einstein_cross.png")
img_3d_curve = os.path.join(assets_dir, "spacetime_curvature.png")
img_blackhole = os.path.join(assets_dir, "blackhole.png")
img_reunion = os.path.join(assets_dir, "reunion.png")


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
                아래 3D 시뮬레이션에서 마우스로 직접 회전하며 탐구해 보세요.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ── 3D 중력 렌즈 시뮬레이션 (Three.js) ──────────────────────────────────────
LENSING_3D_HTML = """
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#030608; overflow:hidden; }
#glc { width:100%; height:560px; position:relative; cursor:grab; }
#glc:active { cursor:grabbing; }
#hint {
  position:absolute; bottom:14px; left:50%; transform:translateX(-50%);
  color:#64748b; font:12px/1 "Inter",sans-serif;
  background:rgba(0,0,0,0.55); padding:6px 14px; border-radius:20px;
  pointer-events:none; white-space:nowrap;
}
#mass-badge {
  position:absolute; top:12px; left:12px;
  color:#a5b4fc; font:bold 12px "Inter",sans-serif;
  background:rgba(15,23,42,0.82); padding:6px 14px; border-radius:8px;
  border:1px solid rgba(99,102,241,0.35); pointer-events:none;
}
#inset {
  position:absolute; top:12px; right:12px;
  width:160px; height:160px; border-radius:12px;
  background:rgba(5,8,18,0.88); border:1px solid rgba(99,102,241,0.35);
  pointer-events:none;
}
</style>
<div id="glc">
  <div id="hint">🖱️ 드래그: 회전 &nbsp;|&nbsp; 스크롤: 줌 &nbsp;|&nbsp; 우클릭 드래그: 이동</div>
  <div id="mass-badge">질량: <span id="mv">5.0</span> M☉</div>
  <canvas id="inset" width="160" height="160"></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.157.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.157.0/examples/js/controls/OrbitControls.js"></script>
<script>
(function () {
  const MASS   = +(window.stParams?.mass ?? 5);
  const CASE   = window.stParams?.case ?? 'cross';

  document.getElementById('mv').textContent = MASS.toFixed(1);

  const container = document.getElementById('glc');
  const W = container.clientWidth || 820;
  const H = 560;

  // ── 렌더러 ──
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(W, H);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x030608);
  container.insertBefore(renderer.domElement, container.firstChild);

  // ── 씬 / 카메라 ──
  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(52, W / H, 1, 12000);
  camera.position.set(0, 220, 820);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping  = true;
  controls.dampingFactor  = 0.07;
  controls.minDistance    = 150;
  controls.maxDistance    = 3000;
  controls.target.set(0, 0, 0);

  // ── 별 배경 ──
  (function () {
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(3000 * 3);
    for (let i = 0; i < pos.length; i++) pos[i] = (Math.random() - 0.5) * 9000;
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    scene.add(new THREE.Points(geo,
      new THREE.PointsMaterial({ color: 0xffffff, size: 1.3, transparent: true, opacity: 0.65 })));
  })();

  // ── 주요 위치 / 아인슈타인 반경 ──
  const SRC = new THREE.Vector3(-540, 0, 0);
  const OBS = new THREE.Vector3( 540, 0, 0);
  const LENS_R  = 16 + MASS * 2.2;
  const EIN_R   = 32 + MASS * 13;   // 아인슈타인 반경 (시뮬레이션 단위)

  // ── 광원 (퀘이사) ──
  const srcMesh = new THREE.Mesh(
    new THREE.SphereGeometry(11, 20, 20),
    new THREE.MeshBasicMaterial({ color: 0xfbbf24 })
  );
  srcMesh.position.copy(SRC);
  scene.add(srcMesh);
  [22, 40].forEach((r, i) => {
    const g = new THREE.Mesh(
      new THREE.SphereGeometry(r, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xfbbf24, transparent: true, opacity: 0.10 - i * 0.04, side: THREE.BackSide })
    );
    g.position.copy(SRC);
    scene.add(g);
  });

  // ── 중력 렌즈 (은하단) ──
  const lensMesh = new THREE.Mesh(
    new THREE.SphereGeometry(LENS_R, 36, 36),
    new THREE.MeshBasicMaterial({ color: 0xffffff })
  );
  scene.add(lensMesh);
  [2.2, 4.0, 7.5].forEach((s, i) => {
    scene.add(Object.assign(new THREE.Mesh(
      new THREE.SphereGeometry(LENS_R * s, 24, 24),
      new THREE.MeshBasicMaterial({
        color: [0x9999ff, 0x4455bb, 0x1a1a55][i],
        transparent: true, opacity: [0.18, 0.10, 0.05][i],
        side: THREE.BackSide
      })
    )));
  });

  // ── 관측자 (지구) ──
  const obsMesh = new THREE.Mesh(
    new THREE.SphereGeometry(14, 20, 20),
    new THREE.MeshBasicMaterial({ color: 0x3b82f6 })
  );
  obsMesh.position.copy(OBS);
  scene.add(obsMesh);
  const obsGlow = new THREE.Mesh(
    new THREE.SphereGeometry(28, 16, 16),
    new THREE.MeshBasicMaterial({ color: 0x3b82f6, transparent: true, opacity: 0.10, side: THREE.BackSide })
  );
  obsGlow.position.copy(OBS);
  scene.add(obsGlow);

  // ── 라벨 스프라이트 ──
  function makeLabel(text, color, w, h) {
    const cv = document.createElement('canvas');
    cv.width = w * 2; cv.height = h * 2;
    const c = cv.getContext('2d');
    c.scale(2, 2);
    c.font = 'bold 14px "Noto Sans KR","Inter",sans-serif';
    c.fillStyle = color;
    c.textAlign = 'center';
    c.textBaseline = 'middle';
    c.fillText(text, w / 2, h / 2);
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(cv), transparent: true }));
    sp.scale.set(w, h, 1);
    return sp;
  }
  const lSrc  = makeLabel('실제 광원 (퀘이사)',     '#fbbf24', 200, 30);
  lSrc.position.set(SRC.x, SRC.y + 30, 0); scene.add(lSrc);
  const lLens = makeLabel('중력 렌즈 (중심 은하단)', '#a5b4fc', 210, 30);
  lLens.position.set(0, -(LENS_R + 30), 0); scene.add(lLens);
  const lObs  = makeLabel('지구 (관측자)',           '#60a5fa', 160, 30);
  lObs.position.set(OBS.x, OBS.y + 36, 0); scene.add(lObs);

  // ── 시공간 격자 (중력에 의해 변형) ──
  (function () {
    const mat  = new THREE.LineBasicMaterial({ color: 0x2d3acc, transparent: true, opacity: 0.32 });
    const RNG  = 520;
    const STEP = 52;
    const wellDepth = MASS * 55;

    function dip(x, y) {
      const r = Math.sqrt(x * x + y * y) + 1;
      return Math.max(-wellDepth, -MASS * 550 / r);
    }

    for (let i = -RNG; i <= RNG; i += STEP) {
      const px = [], py = [];
      for (let v = -RNG; v <= RNG; v += 14) {
        px.push(new THREE.Vector3(v,  i, dip(v, i)));
        py.push(new THREE.Vector3(i,  v, dip(i, v)));
      }
      scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(px), mat));
      scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(py), mat));
    }
  })();

  // ── 굴절된 광선 (Bezier 곡선 튜브) ──
  // 광원 S(-540,0,0) → 제어점(0, by, bz) → 관측자 O(540,0,0)
  // 빛이 렌즈를 충격 인자 b로 통과 후 굴절되어 관측자에게 도달
  function bezierPts(by, bz, n) {
    const ctrl = new THREE.Vector3(0, by, bz);
    const pts  = [];
    for (let i = 0; i <= n; i++) {
      const t = i / n;
      pts.push(new THREE.Vector3(
        (1-t)*(1-t)*SRC.x + 2*(1-t)*t*ctrl.x + t*t*OBS.x,
        (1-t)*(1-t)*SRC.y + 2*(1-t)*t*ctrl.y + t*t*OBS.y,
        (1-t)*(1-t)*SRC.z + 2*(1-t)*t*ctrl.z + t*t*OBS.z
      ));
    }
    return pts;
  }

  const photonData = [];  // { curve, t, mesh }

  (function buildRays() {
    // b값 레벨: 아인슈타인 반경 기준 배수
    const cfg = CASE === 'cross'
      ? [
          { bFac: 0.30, n: 16, col: 0xffd700, op: 0.90, rad: 0.85 },
          { bFac: 0.55, n: 16, col: 0xfbbf24, op: 0.75, rad: 0.75 },
          { bFac: 0.85, n: 16, col: 0xf59e0b, op: 0.60, rad: 0.65 },
          { bFac: 1.40, n: 12, col: 0xd97706, op: 0.38, rad: 0.50 },
          { bFac: 2.40, n:  8, col: 0x92400e, op: 0.20, rad: 0.38 },
        ]
      : [
          { bFac: 0.28, n:  8, col: 0xffd700, op: 0.92, rad: 0.85 },
          { bFac: 0.55, n:  8, col: 0xfbbf24, op: 0.72, rad: 0.70 },
          { bFac: 0.90, n:  6, col: 0xf59e0b, op: 0.50, rad: 0.55 },
          { bFac: 1.60, n:  4, col: 0xd97706, op: 0.28, rad: 0.40 },
        ];

    cfg.forEach(({ bFac, n, col, op, rad }) => {
      const b = EIN_R * bFac;
      for (let j = 0; j < n; j++) {
        const ang = (j / n) * Math.PI * 2;
        const pts = bezierPts(b * Math.cos(ang), b * Math.sin(ang), 60);
        const curve = new THREE.CatmullRomCurve3(pts);
        scene.add(new THREE.Mesh(
          new THREE.TubeGeometry(curve, 60, rad, 6, false),
          new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: op })
        ));
        // 광자 (각 광선당 1개)
        const pm = new THREE.Mesh(
          new THREE.SphereGeometry(2.8, 8, 8),
          new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.9 })
        );
        scene.add(pm);
        photonData.push({ curve, t: j / n, mesh: pm });
      }
    });
  })();

  // ── 관측자 뷰 인셋 (2D 캔버스 오버레이) ──
  const inset = document.getElementById('inset');
  const ic    = inset.getContext('2d');

  function drawInset(ft) {
    ic.clearRect(0, 0, 160, 160);
    ic.font = 'bold 9px sans-serif';
    ic.fillStyle = '#64748b';
    ic.textAlign = 'center';
    ic.fillText("EARTH'S VIEW (TELESCOPE)", 80, 13);

    // 원형 시야
    ic.beginPath(); ic.arc(80, 88, 58, 0, Math.PI * 2);
    ic.strokeStyle = 'rgba(51,65,85,0.55)'; ic.lineWidth = 1; ic.stroke();

    // 렌즈 은하 (중심)
    const gr = ic.createRadialGradient(80, 88, 0, 80, 88, 9);
    gr.addColorStop(0, 'rgba(255,255,255,0.95)');
    gr.addColorStop(1, 'rgba(165,180,252,0.15)');
    ic.beginPath(); ic.arc(80, 88, 9, 0, Math.PI * 2);
    ic.fillStyle = gr; ic.fill();

    const eR = 17 + MASS * 1.9;

    if (CASE === 'cross') {
      // 아인슈타인 링 (맥동)
      const pulse = 0.92 + 0.08 * Math.sin(ft * 0.038);
      ic.beginPath(); ic.arc(80, 88, eR * pulse, 0, Math.PI * 2);
      ic.strokeStyle = `rgba(251,191,36,${0.45 + 0.2 * Math.sin(ft * 0.038)})`;
      ic.lineWidth = 2.8; ic.stroke();

      // 4개 상 (아인슈타인 십자가)
      [[80, 88 - eR * 1.18], [80, 88 + eR * 1.18],
       [80 - eR * 1.18, 88], [80 + eR * 1.18, 88]].forEach(([px, py]) => {
        ic.save();
        ic.shadowColor = '#ffd700'; ic.shadowBlur = 10;
        ic.beginPath(); ic.arc(px, py, 4, 0, Math.PI * 2);
        ic.fillStyle = '#ffd700'; ic.fill();
        ic.restore();
      });
    } else {
      // 별의 위치 변화: A·B 두 상
      const shiftA = eR * (0.8 + MASS * 0.07);
      const shiftB = eR * 0.55;
      [
        [80 - shiftA, 88, 'A', MASS > 5 ? 0.95 : 0.45],
        [80 + shiftB, 88, 'B', 0.95],
      ].forEach(([px, py, lbl, op]) => {
        ic.save();
        ic.shadowColor = '#fbbf24'; ic.shadowBlur = 8;
        ic.beginPath(); ic.arc(px, py, 4, 0, Math.PI * 2);
        ic.fillStyle = `rgba(251,191,36,${op})`; ic.fill();
        ic.restore();
        ic.font = 'bold 10px sans-serif';
        ic.fillStyle = '#fbbf24'; ic.textAlign = 'center';
        ic.fillText(lbl, px, py - 9);
      });
    }
  }

  // ── 애니메이션 루프 ──
  let ft = 0;
  (function animate() {
    requestAnimationFrame(animate);
    ft++;
    controls.update();

    // 광자 이동
    photonData.forEach(p => {
      p.t = (p.t + 0.0038) % 1;
      const pos = p.curve.getPoint(p.t);
      p.mesh.position.copy(pos);
      const distLens = pos.length();
      const boost = Math.max(0, 1 - distLens / 180);
      p.mesh.scale.setScalar(1 + boost * 2.5);
      p.mesh.material.opacity = 0.55 + boost * 0.45;
    });

    // 광원 맥동
    const pulse = 1 + 0.07 * Math.sin(ft * 0.055);
    srcMesh.scale.setScalar(pulse);

    drawInset(ft);
    renderer.render(scene, camera);
  })();

  // ── 리사이즈 ──
  window.addEventListener('resize', () => {
    const nw = container.clientWidth;
    camera.aspect = nw / H;
    camera.updateProjectionMatrix();
    renderer.setSize(nw, H);
  });
})();
</script>
"""

# ── 구 버전 2D 캔버스 (등가원리 디스크 전용) ──────────────────────────────
DISK_HTML = """
<div id="root"></div>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

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

function drawDashboard(ctx, clocks) {
    const sX=20,sY=20,bW=180,bH=160;
    ctx.fillStyle='rgba(15,23,42,0.9)'; ctx.strokeStyle='rgba(99,102,241,0.6)';
    ctx.lineWidth=2; ctx.beginPath(); ctx.rect(sX,sY,bW,bH); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#fff'; ctx.font='bold 14px Inter'; ctx.textAlign='center';
    ctx.fillText('🕒 시간 흐름 비교', sX+bW/2, sY+25);
    const renderClock=(y,label,time,color)=>{
        ctx.save(); ctx.translate(sX+30,y);
        ctx.beginPath(); ctx.arc(0,0,14,0,Math.PI*2); ctx.strokeStyle=color; ctx.lineWidth=2; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0,0); ctx.rotate(time*0.002); ctx.lineTo(0,-11); ctx.stroke();
        ctx.restore();
        ctx.fillStyle=color; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='left';
        ctx.fillText(label,sX+55,y-5);
        ctx.font='12px monospace'; ctx.fillText(time.toFixed(1),sX+55,y+10);
    };
    renderClock(sY+60,'A (지면/정지)',clocks.A,'#3b82f6');
    renderClock(sY+100,'B (중심/회전)',clocks.B,'#10b981');
    renderClock(sY+140,'C (가장자리)',clocks.C,'#f59e0b');
}

function drawRotatingDisk(ctx, W, H, vel, t, clocks, pov) {
    const cx=W*0.5,cy=H*0.45,r=160;
    const ang=t*0.001*vel;
    drawStars(ctx, W, H, t);
    ctx.save();
    if(pov==='B'){ctx.translate(cx,cy);}
    else if(pov==='C'){ctx.translate(cx,cy);ctx.rotate(-ang);ctx.translate(-r*0.85,0);ctx.translate(cx,cy);}
    else{ctx.translate(cx,cy);ctx.rotate(ang);}
    const grad=ctx.createRadialGradient(0,0,r*0.8,0,0,r);
    grad.addColorStop(0,'rgba(30,41,59,0.9)'); grad.addColorStop(1,'rgba(71,85,105,0.4)');
    ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth=2; ctx.stroke();
    ctx.beginPath(); ctx.arc(0,0,10,0,Math.PI*2); ctx.fillStyle='#10b981'; ctx.fill();
    ctx.beginPath(); ctx.arc(r*0.85,0,10,0,Math.PI*2); ctx.fillStyle='#f59e0b'; ctx.fill();
    ctx.restore();
    if(pov==='A'){ctx.beginPath();ctx.arc(cx-r-60,cy,10,0,Math.PI*2);ctx.fillStyle='#3b82f6';ctx.fill();}
    else{ctx.save();ctx.translate(cx,cy);ctx.rotate(-ang);ctx.beginPath();ctx.arc(-r-60,0,10,0,Math.PI*2);ctx.fillStyle='#3b82f6';ctx.fill();ctx.restore();}
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
                return { A: prev.A + 0.1*speed, B: prev.B + 0.1*speed, C: prev.C + 0.1*speed*fac };
            });
            frame = requestAnimationFrame(loop);
        };
        frame = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(frame);
    }, []);

    React.useEffect(() => {
        const ctx = canvasRef.current.getContext('2d');
        const W=800, H=500;
        ctx.clearRect(0,0,W,H);
        drawRotatingDisk(ctx, W, H, window.stParams.discVel, t, clocks, window.stParams.pov);
    }, [t, clocks]);

    return (
        <div style={{position:'relative',width:'100%',height:'500px'}}>
            <canvas ref={canvasRef} width={800} height={500}
                style={{width:'100%',height:'500px',borderRadius:'12px',background:'#05070a'}} />
        </div>
    );
};
ReactDOM.render(<Main />, document.getElementById('root'));
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Noto+Sans+KR:wght@400;700&display=swap');
body { font-family:'Inter','Noto Sans KR',sans-serif; background:transparent; margin:0; padding:0; overflow:hidden; color:#fff; }
</style>
"""

# ── 사이드바 ──
st.sidebar.title("🛠️ 아인슈타인 탐구 메뉴")
mode = st.sidebar.radio("탐구 모드 선택",
                        ["🔭 중력 렌즈 탐구", "🎡 등가 원리 학습", "🎬 인터스텔라 스토리"])

render_header_cards()
st.write("---")

if mode == "🔭 중력 렌즈 탐구":
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.success("**🔬 중력 렌즈 현상 탐구 (3D)**")
        case = st.radio("실험 케이스 선택",
                        ["별의 위치 변화 (A/B)", "아인슈타인의 십자가"], index=0)
        mass = st.slider("렌즈 천체(은하단)의 질량", 1.0, 20.0, 5.0, step=0.5)

        st.write("---")
        if case == "별의 위치 변화 (A/B)":
            st.markdown("""
**교과서 탐구 내용**
- 질량이 작을 때 : 별이 원래 위치와 가까운 **B** 부근에 보임.
- 질량이 클 때 : 빛이 더 많이 휘어 별이 더 먼 **A** 위치에 보임.

**3D 조작**
- 🖱️ 왼쪽 드래그 → 시점 회전
- 🖱️ 스크롤 → 줌
- 🖱️ 오른쪽 드래그 → 이동
""")
        else:
            st.markdown("""
**아인슈타인의 십자가**
- 매우 먼 곳의 퀘이사 빛이 중간 은하의 중력으로 4개로 쪼개져 보입니다.
- 우상단 인셋에서 지구 망원경 시야를 확인하세요.

**3D 조작**
- 🖱️ 왼쪽 드래그 → 시점 회전
- 🖱️ 스크롤 → 줌
""")
    with col2:
        case_val = 'shift' if case == "별의 위치 변화 (A/B)" else 'cross'
        components.html(
            f"<script>window.stParams = {{ mode:'lensing', case:'{case_val}', mass:{mass} }};</script>"
            + LENSING_3D_HTML,
            height=580
        )

elif mode == "🎡 등가 원리 학습":
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.success("**🎢 가속도와 중력의 등가성**")
        pov = st.radio("관찰 시점 선택", ["A (지면)", "B (중심)", "C (가장자리)"])
        disc_vel = st.slider("원판 회전 속도 (ω)", 0.5, 10.0, 5.0)
        st.write("---")
        st.markdown("**특징 요약**")
        if "A" in pov:
            st.write("- 정지한 지면에서 회전하는 C의 시간이 느려지는 것을 관찰합니다.")
        elif "B" in pov:
            st.write("- 회전 축에서 주변부가 왜곡되어 보이는 기하학적 효과를 경험합니다.")
        else:
            st.write("- 가속도를 느끼는 C는 자신을 정지했다 생각하나, 관성력이 중력처럼 작용해 시간이 느려집니다.")
    with col2:
        pov_val = pov[0]
        components.html(
            f"<script>window.stParams = {{ mode:'disk', pov:'{pov_val}', discVel:{disc_vel}, speed:1.0 }};</script>"
            + DISK_HTML,
            height=520
        )

else:
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
블랙홀에 가까운 밀러 행성에서는 시간이 매우 느리게 흐르며,
이는 등가 원리에 의해 '강한 중력'이 시간을 느리게 만드는 실제 현상입니다.
""")
    with col_img2:
        st.image(img_reunion, use_container_width=True, caption="시간의 상대성이 만든 재회")
    st.info("💡 **결론**: 아인슈타인의 일반 상대성 이론은 '중력 = 시공간의 휘어짐'임을 증명하며, "
            "이는 중력 렌즈와 시간 지연이라는 놀라운 현상으로 나타납니다.")
