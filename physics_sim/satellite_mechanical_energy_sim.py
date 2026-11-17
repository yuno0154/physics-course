import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """지구 주위를 공전하는 인공위성의 역학적 에너지 보존 시뮬레이션.
    교과서 'E. 지구 주위를 도는 인공 위성의 역학적 에너지' 유도 및
    원궤도·타원궤도에서의 역학적 에너지 보존, 탈출속도와의 관계를 탐구한다.
    """
    st.title("🛰️ 지구 주위를 공전하는 인공위성의 역학적 에너지 보존")
    st.caption("2022 개정 역학과 에너지 · 중력장 내 인공위성의 운동 에너지, 중력 퍼텐셜 에너지, 역학적 에너지 보존")
    components.html(HTML, height=980, scrolling=True)


HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
  :root {
    --ink: #0f172a;
    --sub: #475569;
    --line: #cbd5e1;
    --bg: #f8fafc;
    --card: #ffffff;
    --key: #1d4ed8;
    --k-col: #2563eb;
    --u-col: #e11d48;
    --e-col: #7c3aed;
    --f-col: #059669;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: "Pretendard", "Malgun Gothic", "Apple SD Gothic Neo", sans-serif;
    color: var(--ink);
    background: transparent;
  }
  #app {
    max-width: 1140px;
    margin: 0 auto;
    padding: 4px 6px 24px;
  }
  .tabs {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin: 6px 0 10px;
  }
  .tab {
    border: 1px solid var(--line);
    background: #fff;
    border-radius: 999px;
    padding: 8px 15px;
    font-size: 13.5px;
    font-weight: 700;
    color: var(--sub);
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s;
  }
  .tab.on {
    background: var(--key);
    border-color: var(--key);
    color: #fff;
    box-shadow: 0 3px 10px rgba(29, 78, 216, 0.22);
  }
  .ctrl {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 16px;
    align-items: center;
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 9px 14px;
    margin-bottom: 10px;
  }
  .speed-bar {
    background: #fffbeb;
    border-color: #fde68a;
  }
  .grp {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 13px;
    font-weight: 600;
  }
  input[type=range] {
    width: 135px;
    accent-color: var(--key);
    cursor: pointer;
  }
  .val {
    min-width: 78px;
    color: var(--key);
    font-weight: 800;
    font-variant-numeric: tabular-nums;
  }
  .btn {
    border: 1px solid var(--line);
    background: #fff;
    border-radius: 9px;
    padding: 6px 11px;
    font-size: 12.5px;
    font-weight: 700;
    cursor: pointer;
    font-family: inherit;
    color: var(--ink);
  }
  .btn:hover { background: #f1f5f9; }
  .btn.on {
    background: #eff6ff;
    border-color: #93c5fd;
    color: #1e3a8a;
  }
  .btn.primary {
    background: #0f172a;
    color: #fff;
    border-color: #0f172a;
  }
  .grid-2 {
    display: grid;
    grid-template-columns: 1.08fr 1fr;
    gap: 12px;
    align-items: stretch;
  }
  @media (max-width: 900px) {
    .grid-2 { grid-template-columns: 1fr; }
  }
  .card {
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 12px;
  }
  canvas {
    display: block;
    width: 100%;
    height: auto;
    border-radius: 10px;
  }
  .view { display: none; }
  .view.show { display: block; }
  .ctrl.view.show { display: flex; }

  /* 교과서 유도 박스 스타일 */
  .textbook-box {
    border: 2px solid #334155;
    border-radius: 12px;
    padding: 14px 16px;
    background: #ffffff;
    font-size: 14px;
    line-height: 1.85;
  }
  .textbook-title {
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 2px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .eq-step {
    padding: 6px 10px;
    border-radius: 8px;
    margin-bottom: 6px;
    background: #f8fafc;
    border-left: 4px solid #cbd5e1;
  }
  .eq-step.hl-k { border-left-color: var(--k-col); background: #eff6ff; }
  .eq-step.hl-u { border-left-color: var(--u-col); background: #fff1f2; }
  .eq-step.hl-e { border-left-color: var(--e-col); background: #f5f3ff; }

  .metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 10px;
  }
  .metric-card {
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 9px 10px;
    text-align: center;
  }
  .metric-card .lbl { font-size: 12px; font-weight: 700; color: var(--sub); }
  .metric-card .num { font-size: 15.5px; font-weight: 800; margin-top: 3px; font-variant-numeric: tabular-nums; }

  .step-box {
    margin-top: 10px;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    padding: 11px 14px;
    font-size: 14px;
    line-height: 1.65;
  }
  .step-box b { color: #1d4ed8; }
  .note-box {
    margin-top: 8px;
    background: #f1f5f9;
    border-radius: 12px;
    padding: 9px 14px;
    font-size: 13px;
    line-height: 1.6;
    color: #334155;
  }
  .ws-tag {
    display: inline-block;
    background: #dbeafe;
    color: #1e3a8a;
    border-radius: 6px;
    padding: 1px 7px;
    font-size: 12px;
    font-weight: 800;
    margin-right: 6px;
  }
  .mvar{font-family:KaTeX_Math,"Times New Roman",serif;font-style:italic;font-size:1.08em;padding:0 1px}
</style>
</head>
<body>
<div id="app">

  <!-- 재생 컨트롤 바 -->
  <div class="ctrl speed-bar">
    <div class="grp">⏱ 재생 속도</div>
    <button class="btn" data-sp="0.25">0.25×</button>
    <button class="btn on" data-sp="0.5">0.5×</button>
    <button class="btn" data-sp="1">1×</button>
    <button class="btn" data-sp="2">2×</button>
    <button class="btn primary" id="pp">⏸ 일시정지</button>
    <button class="btn" id="rs">↺ 위치 초기화</button>
  </div>

  <!-- 상단 탭 -->
  <div class="tabs" id="tabs"></div>

  <!-- 탭 0 컨트롤: 원궤도 인공위성의 역학적 에너지 -->
  <div id="c0" class="ctrl view show">
    <div class="grp">궤도 반지름 <i>r</i>
      <input type="range" id="r0" min="1.05" max="5.00" step="0.05" value="1.50">
      <span class="val" id="vr0">1.50 R_E</span>
    </div>
    <div class="grp">위성 질량 <i>m</i>
      <input type="range" id="m0" min="200" max="2000" step="100" value="1000">
      <span class="val" id="vm0">1000 kg</span>
    </div>
    <button class="btn" data-orb="1.06">저궤도(ISS, 1.06R_E)</button>
    <button class="btn on" data-orb="1.50">기본 궤도(1.50R_E)</button>
    <button class="btn" data-orb="3.17">GPS 궤도(3.17R_E)</button>
    <button class="btn" data-orb="4.50">고궤도(4.50R_E)</button>
  </div>

  <!-- 탭 1 컨트롤: 궤도 반지름에 따른 K, U, E 그래프 -->
  <div id="c1" class="ctrl view">
    <div class="grp">탐색 궤도 반지름 <i>r</i>
      <input type="range" id="r1" min="1.00" max="5.50" step="0.05" value="2.00">
      <span class="val" id="vr1">2.00 R_E</span>
    </div>
    <button class="btn" data-r1="1.00">지표면 근처 (1.0 R_E)</button>
    <button class="btn on" data-r1="2.00">r = 2.0 R_E</button>
    <button class="btn" data-r1="3.00">r = 3.0 R_E</button>
    <button class="btn" data-r1="4.00">r = 4.0 R_E</button>
  </div>

  <!-- 탭 2 컨트롤: 타원 궤도에서의 역학적 에너지 보존 -->
  <div id="c2" class="ctrl view">
    <div class="grp">타원 궤도 이심률 <i>e</i>
      <input type="range" id="ec2" min="0.00" max="0.60" step="0.05" value="0.45">
      <span class="val" id="vec2">0.45</span>
    </div>
    <button class="btn" data-ec="0.00">원궤도 (e = 0)</button>
    <button class="btn on" data-ec="0.45">타원궤도 (e = 0.45)</button>
    <button class="btn" data-ec="0.60">큰 타원궤도 (e = 0.60)</button>
    <button class="btn" id="toPerigee">📍 근지점(속력 최대)</button>
    <button class="btn" id="toApogee">📍 원지점(속력 최소)</button>
  </div>

  <!-- 탭 3 컨트롤: 원궤도 속력 vs 탈출속도 -->
  <div id="c3" class="ctrl view">
    <div class="grp">발사 속력 배율 (<i>v</i> / <i>v</i><sub>원</sub>)
      <input type="range" id="vf3" min="1.00" max="1.60" step="0.01" value="1.00">
      <span class="val" id="vvf3">1.00 v_원</span>
    </div>
    <button class="btn on" data-vf="1.00">① 원궤도 (v = v_원, E &lt; 0)</button>
    <button class="btn" data-vf="1.20">② 타원궤도 (v = 1.2v_원, E &lt; 0)</button>
    <button class="btn" data-vf="1.414">③ 포물선 탈출 (v = √2 v_원, E = 0)</button>
    <button class="btn" data-vf="1.55">④ 쌍곡선 탈출 (v &gt; √2 v_원, E &gt; 0)</button>
  </div>

  <!-- 탭 0 화면: 왼쪽 원운동 캔버스 + 오른쪽 교과서 수식 유도 & 실시간 에너지 막대 -->
  <div id="v0" class="view show">
    <div class="grid-2">
      <div class="card">
        <canvas id="cv0" width="540" height="470"></canvas>
      </div>
      <div class="card textbook-box">
        <div class="textbook-title">
          <span>📘 E. 지구 주위를 도는 인공 위성의 역학적 에너지</span>
          <span style="font-size:12px; color:#2563eb; font-weight:700;">교과서 핵심 유도</span>
        </div>

        <div class="eq-step">
          <div><b>① 역학적 에너지의 정의</b> (운동 에너지 <i class="mvar">K</i> + 중력 퍼텐셜 에너지 <i class="mvar">U</i>)</div>
          <div id="k_eq1" style="margin-top:3px;"></div>
        </div>

        <div class="eq-step">
          <div><b>② 중력이 구심력 역할</b>을 하므로 궤도 속력 <i class="mvar">v</i>는</div>
          <div id="k_eq2" style="margin-top:3px;"></div>
        </div>

        <div class="eq-step hl-k">
          <div><b>③ 원운동하는 인공위성의 운동 에너지 <i class="mvar">K</i></b></div>
          <div id="k_eq3" style="margin-top:3px;"></div>
        </div>

        <div class="eq-step hl-e">
          <div><b>④ 따라서 인공위성의 역학적 에너지 <i class="mvar">E</i>는</b></div>
          <div id="k_eq4" style="margin-top:3px;"></div>
        </div>

        <div class="metric-grid">
          <div class="metric-card" style="background:#eff6ff; border-color:#93c5fd;">
            <div class="lbl" style="color:#1d4ed8;">운동 에너지 K (+GMm/2r)</div>
            <div class="num" style="color:#2563eb;" id="m0_k">+20.8 GJ</div>
          </div>
          <div class="metric-card" style="background:#fff1f2; border-color:#fecdd3;">
            <div class="lbl" style="color:#be123c;">퍼텐셜 에너지 U (−GMm/r)</div>
            <div class="num" style="color:#e11d48;" id="m0_u">−41.7 GJ</div>
          </div>
          <div class="metric-card" style="background:#f5f3ff; border-color:#ddd6fe;">
            <div class="lbl" style="color:#6d28d9;">역학적 에너지 E (= U/2 = −K)</div>
            <div class="num" style="color:#7c3aed;" id="m0_e">−20.8 GJ</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 탭 1, 2, 3 공용 전체폭 캔버스 -->
  <div id="vCanvas" class="card view">
    <canvas id="cvMain" width="1000" height="460"></canvas>
  </div>

  <div class="step-box" id="step"></div>
  <div class="note-box" id="note"></div>
</div>

<script>
const $ = id => document.getElementById(id);
const BL = '#2563eb', RD = '#e11d48', GN = '#059669', PU = '#7c3aed', INK = '#0f172a', SUB = '#64748b', OR = '#ea580c';

// 실제 물리 상수 (지구 기준)
const G = 6.674e-11;
const M_E = 5.972e24;
const R_E = 6.371e6; // m
const GM = G * M_E;  // 3.986e14 m^3/s^2
// 지표면(r = R_E)에서 m = 1000 kg 위성의 GMm/R_E ≈ 62.56 GJ
const U0_PER_KG = GM / R_E / 1e9; // GJ per 1000 kg unit: 0.06256 GJ/kg

const TABS = [
  ['① 원궤도 인공위성의 역학적 에너지 (교과서 E)', 'E①', '중력이 구심력 역할을 하므로 K = GMm/(2r)이 되고, 역학적 에너지 E = K + U = −GMm/(2r) = U/2 로 음(−)의 일정한 값을 가집니다.'],
  ['② 궤도 반지름(r)과 에너지 그래프', 'E②', '궤도 반지름 r이 커질수록 속력은 느려져 운동 에너지 K는 감소하지만, 퍼텐셜 에너지 U와 역학적 에너지 E = −GMm/(2r)는 모두 증가(0에 가까워짐)합니다.'],
  ['③ 타원 궤도에서의 역학적 에너지 보존', 'E③', '타원 궤도를 돌 때 근지점에서는 K가 최대·U가 최소이고 원지점에서는 K가 최소·U가 최대이지만, 두 에너지의 합인 역학적 에너지 E = K + U는 모든 위치에서 일정하게 보존됩니다.'],
  ['④ 원궤도 속력 vs 탈출속도 비교', 'E④', '원궤도 속력 v_원 = √(GM/r)일 때 E = −GMm/(2r) < 0 (속박 궤도)이고, 속력이 √2배인 v_탈출 = √(2GM/r)이 되면 K = |U|가 되어 E = 0으로 지구 중력장을 탈출합니다.']
];

let tab = 0, paused = false, speed = 0.5, last = performance.now(), T = 0;

TABS.forEach((t, i) => {
  const b = document.createElement('button');
  b.className = 'tab';
  b.textContent = t[0];
  b.onclick = () => go(i);
  $('tabs').appendChild(b);
});

document.querySelectorAll('[data-sp]').forEach(b => {
  b.onclick = () => {
    speed = +b.dataset.sp;
    document.querySelectorAll('[data-sp]').forEach(x => x.classList.toggle('on', x === b));
  };
});
$('pp').onclick = () => {
  paused = !paused;
  $('pp').textContent = paused ? '▶ 재생' : '⏸ 일시정지';
};
$('rs').onclick = () => { T = 0; };

// KaTeX 렌더링
function renderFormulas() {
  if (!window.katex) return;
  katex.render(String.raw`E = K + U = \frac{1}{2}mv_0^2 - \frac{GMm}{r}`, $('k_eq1'), { throwOnError: false, displayMode: true });
  katex.render(String.raw`m\frac{v_0^2}{r} = G\frac{Mm}{r^2} \;\;\longrightarrow\;\; v_0^2 = \frac{GM}{r}`, $('k_eq2'), { throwOnError: false, displayMode: true });
  katex.render(String.raw`K = \frac{1}{2}mv_0^2 = +\frac{GMm}{2r} = -\frac{U}{2}`, $('k_eq3'), { throwOnError: false, displayMode: true });
  katex.render(String.raw`E = \frac{GMm}{2r} - \frac{GMm}{r} = -\frac{GMm}{2r} = \frac{U}{2} = -K < 0`, $('k_eq4'), { throwOnError: false, displayMode: true });
}
window.addEventListener('load', renderFormulas);
setTimeout(renderFormulas, 250);

// 캔버스 드로잉 헬퍼
function txt(ctx, s, x, y, o) {
  o = o || {};
  ctx.font = (o.b ? '700 ' : '500 ') + (o.s || 13.5) + 'px "Malgun Gothic", sans-serif';
  ctx.fillStyle = o.c || INK;
  ctx.textAlign = o.a || 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(s, x, y);
}
function ln(ctx, x0, y0, x1, y1, c, w, d) {
  ctx.beginPath();
  ctx.setLineDash(d || []);
  ctx.strokeStyle = c;
  ctx.lineWidth = w || 1.5;
  ctx.moveTo(x0, y0);
  ctx.lineTo(x1, y1);
  ctx.stroke();
  ctx.setLineDash([]);
}
function head(ctx, x, y, dx, dy, c, s) {
  s = s || 9;
  const a = Math.atan2(dy, dx);
  ctx.beginPath();
  ctx.fillStyle = c;
  ctx.moveTo(x, y);
  ctx.lineTo(x - s * Math.cos(a - 0.4), y - s * Math.sin(a - 0.4));
  ctx.lineTo(x - s * Math.cos(a + 0.4), y - s * Math.sin(a + 0.4));
  ctx.fill();
}
function arr(ctx, x0, y0, x1, y1, c, w) {
  ln(ctx, x0, y0, x1, y1, c, w || 2.5);
  head(ctx, x1, y1, x1 - x0, y1 - y0, c, 9);
}
function dbl(ctx, x0, y0, x1, y1, c, w) {
  ln(ctx, x0, y0, x1, y1, c, w || 1.8);
  head(ctx, x1, y1, x1 - x0, y1 - y0, c, 7);
  head(ctx, x0, y0, x0 - x1, y0 - y1, c, 7);
}
function dot(ctx, x, y, r, c) {
  ctx.beginPath();
  ctx.fillStyle = c;
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}
function drawEarth(ctx, cx, cy, Rpx) {
  const grd = ctx.createRadialGradient(cx - Rpx * 0.25, cy - Rpx * 0.25, Rpx * 0.1, cx, cy, Rpx);
  grd.addColorStop(0, '#60a5fa');
  grd.addColorStop(0.65, '#2563eb');
  grd.addColorStop(1, '#1e3a8a');
  ctx.beginPath();
  ctx.fillStyle = grd;
  ctx.arc(cx, cy, Rpx, 0, Math.PI * 2);
  ctx.fill();
  // 대륙 모형
  ctx.fillStyle = 'rgba(74, 222, 128, 0.75)';
  ctx.beginPath();
  ctx.arc(cx - Rpx * 0.28, cy - Rpx * 0.18, Rpx * 0.32, 0, Math.PI * 2);
  ctx.arc(cx + Rpx * 0.25, cy + Rpx * 0.22, Rpx * 0.26, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = '#93c5fd';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.arc(cx, cy, Rpx, 0, Math.PI * 2);
  ctx.stroke();
}
function drawSatellite(ctx, x, y, radAng) {
  ctx.save();
  ctx.translate(x, y);
  // radAng = 중심에서 위성을 향하는 반지름 방향 각도 -> 접선 방향은 radAng + Math.PI/2
  ctx.rotate(radAng);
  // 태양전지판 (반지름 방향과 나란하게 배치하여 접선 속도 화살표와 간섭하지 않음)
  ctx.fillStyle = '#1e3a8a';
  ctx.strokeStyle = '#93c5fd';
  ctx.lineWidth = 1.2;
  ctx.fillRect(-24, -4, 15, 8);
  ctx.strokeRect(-24, -4, 15, 8);
  ctx.fillRect(9, -4, 15, 8);
  ctx.strokeRect(9, -4, 15, 8);
  // 본체
  ctx.fillStyle = '#cbd5e1';
  ctx.strokeStyle = '#0f172a';
  ctx.fillRect(-6, -6, 12, 12);
  ctx.strokeRect(-6, -6, 12, 12);
  ctx.restore();
}

// ============================================================================
// [TAB 0] 원궤도 인공위성의 역학적 에너지 (교과서 그림 E 재현 + 실시간 에너지 바)
// ============================================================================
function scene0() {
  const cv = $('cv0'), ctx = cv.getContext('2d'), W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);

  const rRatio = +$('r0').value; // r / R_E
  const mass = +$('m0').value;   // kg
  $('vr0').textContent = rRatio.toFixed(2) + ' R_E';
  $('vm0').textContent = mass + ' kg';

  // 실제 물리량 계산
  const rReal = rRatio * R_E;
  const vReal = Math.sqrt(GM / rReal) / 1000; // km/s
  const U_GJ = -(GM * mass / rReal) / 1e9;    // GJ
  const K_GJ = -U_GJ / 2;                     // +GMm/(2r) in GJ
  const E_GJ = U_GJ / 2;                      // -GMm/(2r) in GJ

  $('m0_k').textContent = '+' + K_GJ.toFixed(1) + ' GJ';
  $('m0_u').textContent = '−' + Math.abs(U_GJ).toFixed(1) + ' GJ';
  $('m0_e').textContent = '−' + Math.abs(E_GJ).toFixed(1) + ' GJ';

  // 왼쪽 궤도 캔버스 (원궤도가 시원하게 보이도록 반지름 스케일 조정)
  const cx = 190, cy = 225, RePx = 42;
  const rPx = 78 + (rRatio - 1.05) * 24; // 78 px ~ 173 px

  // 원궤도 점선
  ctx.beginPath();
  ctx.setLineDash([6, 4]);
  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 1.8;
  ctx.arc(cx, cy, rPx, 0, Math.PI * 2);
  ctx.stroke();
  ctx.setLineDash([]);

  // 지구 그리기
  drawEarth(ctx, cx, cy, RePx);
  txt(ctx, 'M', cx - 10, cy + 4, { c: '#fff', b: 1, s: 13 });

  // 지구 반지름 R 화살표
  const rAng = 0.85;
  arr(ctx, cx, cy, cx + RePx * Math.cos(rAng), cy + RePx * Math.sin(rAng), '#f8fafc', 1.8);
  txt(ctx, 'R', cx + RePx * 0.52 * Math.cos(rAng) + 9, cy + RePx * 0.52 * Math.sin(rAng) - 4, { c: '#fff', b: 1, s: 12 });

  // 인공위성 공전 각속도 (케플러 제3법칙 ω ∝ r^(-3/2))
  const omega = 1.2 / Math.pow(rRatio, 1.5);
  const th = T * omega; // 시계방향 공전
  const ux = Math.cos(th), uy = Math.sin(th);   // 바깥쪽 반지름 단위벡터
  const tx = -Math.sin(th), ty = Math.cos(th);  // 시계방향 접선 단위벡터 (반지름과 정확히 90° 수직!)
  const sx = cx + rPx * ux, sy = cy + rPx * uy;

  // 궤도 반지름 r 양방향 화살표 (위성 반대쪽 각도에 배치하여 위성과 절대 겹치지 않게 함)
  const orbAng = th + Math.PI * 0.65;
  dbl(ctx, cx, cy, cx + rPx * Math.cos(orbAng), cy + rPx * Math.sin(orbAng), '#475569', 1.6);
  txt(ctx, 'r = ' + rRatio.toFixed(2) + ' R', cx + rPx * 0.58 * Math.cos(orbAng), cy + rPx * 0.58 * Math.sin(orbAng) - 12, { c: '#0f172a', b: 1, s: 12 });

  // 중심-위성 반지름 보조선 (점선) 및 접선-반지름 수직(∟) 기호 표시
  ln(ctx, cx, cy, sx, sy, '#cbd5e1', 1.2, [3, 3]);
  const sq = 9;
  ctx.beginPath();
  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 1.3;
  ctx.moveTo(sx - ux * sq, sy - uy * sq);
  ctx.lineTo(sx - ux * sq + tx * sq, sy - uy * sq + ty * sq);
  ctx.lineTo(sx + tx * sq, sy + ty * sq);
  ctx.stroke();

  // 구심력(만유인력 F_g) 벡터 (지구 중심 방향 초록 화살표)
  const fLen = Math.min(rPx - RePx - 6, Math.max(26, 48 / Math.pow(rRatio, 0.8)));
  arr(ctx, sx, sy, sx - ux * fLen, sy - uy * fLen, GN, 2.6);
  txt(ctx, '중력 F', sx - ux * (fLen * 0.55) - tx * 24, sy - uy * (fLen * 0.55) - ty * 24, { c: GN, b: 1, s: 11.5 });

  // 접선 속도 벡터 v0 (원궤도 접선 방향 파란 화살표)
  const vLen = 54 / Math.pow(rRatio, 0.35);
  arr(ctx, sx, sy, sx + tx * vLen, sy + ty * vLen, BL, 3.2);
  txt(ctx, 'v₀ = ' + vReal.toFixed(2) + ' km/s', sx + tx * (vLen + 18) + ux * 14, sy + ty * (vLen + 18) + uy * 14, { c: BL, b: 1, s: 12.5 });

  // 위성 본체 (접선 방향과 정확히 정렬)
  drawSatellite(ctx, sx, sy, th);
  txt(ctx, 'm', sx + ux * 28, sy + uy * 28, { c: INK, b: 1, s: 13 });

  // 우측 에너지 막대 그래프 (x = 400 .. 525)
  const bx0 = 395, by0 = 230, maxH = 155;
  const maxGJ = U0_PER_KG * 2000; // 기준 스케일 (m=2000, r=1 -> 125 GJ)
  const scE = maxH / Math.max(45, U0_PER_KG * mass);

  ln(ctx, bx0 - 10, by0, 530, by0, '#334155', 1.8);
  txt(ctx, '0', bx0 - 18, by0, { c: SUB, b: 1, s: 12 });
  txt(ctx, '에너지 비교 (단위: GJ)', 460, 42, { c: INK, b: 1, s: 13 });

  const bars = [
    { x: 418, v: K_GJ,  lab: 'K', col: BL, sub: '+GMm/2r' },
    { x: 460, v: U_GJ,  lab: 'U', col: RD, sub: '−GMm/r' },
    { x: 502, v: E_GJ,  lab: 'E', col: PU, sub: '−GMm/2r' }
  ];
  bars.forEach(b => {
    const h = b.v * scE;
    ctx.fillStyle = b.col;
    if (h >= 0) {
      ctx.fillRect(b.x - 13, by0 - h, 26, h);
      txt(ctx, '+' + b.v.toFixed(1), b.x, by0 - h - 12, { c: b.col, b: 1, s: 11.5 });
    } else {
      ctx.fillRect(b.x - 13, by0, 26, -h);
      txt(ctx, '−' + Math.abs(b.v).toFixed(1), b.x, by0 - h + 13, { c: b.col, b: 1, s: 11.5 });
    }
    txt(ctx, b.lab, b.x, by0 + (h >= 0 ? 15 : -14), { c: b.col, b: 1, s: 13 });
  });

  txt(ctx, '원궤도에서는 항상  K = |E| = |U|/2  이므로  E = K + U = −GMm/(2r) = U/2  가 성립합니다.', W / 2, 442, { c: PU, b: 1, s: 12.5 });

  $('step').innerHTML =
    `현재 궤도 반지름 <b>r = ${rRatio.toFixed(2)} R<sub>E</sub></b>에서 원운동 속력은 <b>v₀ = ${vReal.toFixed(2)} km/s</b>입니다. ` +
    `중력이 구심력 역할을 하므로 <b>운동 에너지 K = +${K_GJ.toFixed(1)} GJ</b>는 퍼텐셜 에너지 <b>U = −${Math.abs(U_GJ).toFixed(1)} GJ</b> 크기의 정확히 절반이며, ` +
    `따라서 <b>역학적 에너지 E = K + U = −${Math.abs(E_GJ).toFixed(1)} GJ (= U/2 = −K)</b>로 일정하게 보존됩니다.`;
}

document.querySelectorAll('[data-orb]').forEach(b => {
  b.onclick = () => {
    $('r0').value = b.dataset.orb;
    document.querySelectorAll('[data-orb]').forEach(x => x.classList.toggle('on', x === b));
  };
});

// ============================================================================
// [TAB 1] 궤도 반지름 r에 따른 K(r), U(r), E(r) 그래프
// ============================================================================
function scene1() {
  const cv = $('cvMain'), ctx = cv.getContext('2d'), W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);

  const rSel = +$('r1').value;
  $('vr1').textContent = rSel.toFixed(2) + ' R_E';

  const gx0 = 90, gx1 = 640, gy0 = 205, gH = 175;
  const rMin = 1.0, rMax = 5.5;
  const X = r => gx0 + (r - rMin) / (rMax - rMin) * (gx1 - gx0);
  // 정규화 에너지: r=1일 때 U = -1.0, K = +0.5, E = -0.5
  const Y = eNorm => gy0 - eNorm * gH;

  // 축 및 격자
  ln(ctx, gx0, gy0 - gH - 15, gx0, gy0 + gH + 20, INK, 1.8);
  ln(ctx, gx0, gy0, gx1 + 15, gy0, INK, 1.8);
  txt(ctx, '궤도 반지름 r (R_E)', gx1 + 10, gy0 + 22, { a: 'right', b: 1, s: 13 });
  txt(ctx, '에너지', gx0 - 10, gy0 - gH - 22, { a: 'center', b: 1, s: 13 });
  txt(ctx, '0 (무한원 기준)', gx0 - 10, gy0, { a: 'right', c: SUB, s: 12 });
  txt(ctx, '+GMm/2R', gx0 - 10, Y(0.5), { a: 'right', c: BL, b: 1, s: 11.5 });
  txt(ctx, '−GMm/2R', gx0 - 10, Y(-0.5), { a: 'right', c: PU, b: 1, s: 11.5 });
  txt(ctx, '−GMm/R', gx0 - 10, Y(-1.0), { a: 'right', c: RD, b: 1, s: 11.5 });

  for (let r = 1; r <= 5; r++) {
    const x = X(r);
    ln(ctx, x, gy0 - gH, x, gy0 + gH, '#f1f5f9', 1);
    ln(ctx, x, gy0 - 4, x, gy0 + 4, INK, 1.5);
    txt(ctx, r + ' R_E', x, gy0 + 18, { c: SUB, s: 12, b: 1 });
  }

  // 곡선 1: K(r) = +1/(2r)
  ctx.beginPath(); ctx.strokeStyle = BL; ctx.lineWidth = 3;
  for (let r = 1.0; r <= rMax; r += 0.03) {
    const x = X(r), y = Y(0.5 / r);
    r === 1.0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.stroke();
  txt(ctx, '운동 에너지 K = +GMm/(2r)', X(2.3), Y(0.5 / 2.3) - 18, { c: BL, b: 1, s: 13, a: 'left' });

  // 곡선 2: E(r) = -1/(2r)
  ctx.beginPath(); ctx.strokeStyle = PU; ctx.lineWidth = 3.5;
  for (let r = 1.0; r <= rMax; r += 0.03) {
    const x = X(r), y = Y(-0.5 / r);
    r === 1.0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.stroke();
  txt(ctx, '역학적 에너지 E = −GMm/(2r) = U/2', X(2.2), Y(-0.5 / 2.2) - 16, { c: PU, b: 1, s: 13, a: 'left' });

  // 곡선 3: U(r) = -1/r
  ctx.beginPath(); ctx.strokeStyle = RD; ctx.lineWidth = 3;
  for (let r = 1.0; r <= rMax; r += 0.03) {
    const x = X(r), y = Y(-1.0 / r);
    r === 1.0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.stroke();
  txt(ctx, '중력 퍼텐셜 에너지 U = −GMm/r', X(2.1), Y(-1.0 / 2.1) + 20, { c: RD, b: 1, s: 13, a: 'left' });

  // 현재 선택한 r에서의 점 및 대칭 화살표
  const xs = X(rSel), yK = Y(0.5 / rSel), yE = Y(-0.5 / rSel), yU = Y(-1.0 / rSel);
  ln(ctx, xs, yK, xs, yU, '#94a3b8', 1.5, [4, 4]);
  dbl(ctx, xs - 12, gy0, xs - 12, yK, BL, 1.8);
  dbl(ctx, xs + 12, gy0, xs + 12, yE, PU, 1.8);
  dot(ctx, xs, yK, 6.5, BL);
  dot(ctx, xs, yE, 7, PU);
  dot(ctx, xs, yU, 6.5, RD);

  // 우측 설명 카드 영역 (x = 680 .. 980)
  const rx = 685;
  ctx.fillStyle = '#f8fafc';
  ctx.strokeStyle = '#cbd5e1';
  ctx.lineWidth = 1.5;
  ctx.fillRect(rx, 35, 290, 385);
  ctx.strokeRect(rx, 35, 290, 385);

  const U0 = 62.56; // m=1000kg 기준 지표면 GMm/R (GJ)
  const curK = (0.5 * U0 / rSel).toFixed(1);
  const curU = (-U0 / rSel).toFixed(1);
  const curE = (-0.5 * U0 / rSel).toFixed(1);
  const curV = (7.91 / Math.sqrt(rSel)).toFixed(2);

  txt(ctx, '📊 r = ' + rSel.toFixed(2) + ' R_E 에서의 값', rx + 145, 65, { b: 1, s: 15, c: INK });
  txt(ctx, '(위성 질량 m = 1,000 kg 기준)', rx + 145, 86, { s: 12, c: SUB });

  const info = [
    ['원궤도 속력 v', curV + ' km/s', INK],
    ['운동 에너지 K', '+' + curK + ' GJ', BL],
    ['퍼텐셜 에너지 U', curU + ' GJ', RD],
    ['역학적 에너지 E', curE + ' GJ', PU]
  ];
  info.forEach((row, i) => {
    const yy = 128 + i * 42;
    ctx.fillStyle = '#fff';
    ctx.fillRect(rx + 16, yy - 16, 258, 34);
    txt(ctx, row[0], rx + 28, yy, { a: 'left', b: 1, s: 13, c: SUB });
    txt(ctx, row[1], rx + 262, yy, { a: 'right', b: 1, s: 14, c: row[2] });
  });

  txt(ctx, '💡 핵심 질문: 높은 궤도로 올라가면?', rx + 145, 310, { b: 1, s: 13.5, c: INK });
  txt(ctx, '· 궤도 반지름 r이 커지면:', rx + 24, 336, { a: 'left', s: 12.5, c: INK });
  txt(ctx, '  ① 속력 v와 운동 에너지 K는 감소!', rx + 24, 358, { a: 'left', b: 1, s: 12.5, c: BL });
  txt(ctx, '  ② 퍼텐셜 에너지 U는 더 크게 증가!', rx + 24, 380, { a: 'left', b: 1, s: 12.5, c: RD });
  txt(ctx, '  ③ 총 역학적 에너지 E는 증가!', rx + 24, 402, { a: 'left', b: 1, s: 12.5, c: PU });

  $('step').innerHTML =
    `그래프에서 <b>운동 에너지 K 곡선(파랑, +GMm/2r)</b>과 <b>역학적 에너지 E 곡선(보라, −GMm/2r)</b>은 시간축(0)에 대해 완벽한 <b>위아래 대칭(K = −E)</b>입니다. ` +
    `더 높은 원궤도(r 증가)로 위성을 올리려면 속력은 느려지지만 퍼텐셜 에너지가 2배 더 많이 증가하므로 <b>로켓을 점화해 역학적 에너지 E를 공급</b>해야 합니다.`;
}

document.querySelectorAll('[data-r1]').forEach(b => {
  b.onclick = () => {
    $('r1').value = b.dataset.r1;
    document.querySelectorAll('[data-r1]').forEach(x => x.classList.toggle('on', x === b));
  };
});

// ============================================================================
// [TAB 2] 타원 궤도에서의 역학적 에너지 보존 (근지점 ↔ 원지점)
// ============================================================================
let ellAngle = 0; // 평균 근점 이각 M
function scene2(dt) {
  const cv = $('cvMain'), ctx = cv.getContext('2d'), W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);

  const e = +$('ec2').value;
  $('vec2').textContent = e.toFixed(2);

  // 긴반지름 a = 2.5 R_E 고정
  const aRatio = 2.5, RePx = 32;
  const aPx = aRatio * RePx * 1.75; // 140 px
  const bPx = aPx * Math.sqrt(1 - e * e);
  const cPx = aPx * e; // 초점(지구) 이동 거리

  // 케플러 방정식 근사 풀이로 실제 면적속도 일정(근지점 빠름, 원지점 느림) 구현
  const rNowNorm = (1 - e * e) / (1 + e * Math.cos(ellAngle)); // r / a
  if (!paused) {
    const dTheta = (1.1 / Math.pow(rNowNorm, 2)) * dt;
    ellAngle = (ellAngle + dTheta) % (Math.PI * 2);
  }

  // 왼쪽 타원 궤도 영역 (지구 초점 = (focusX, cy))
  const focusX = 275, cy = 225;
  const centerX = focusX - cPx; // 근지점이 오른쪽(focusX + aPx*(1-e)), 원지점이 왼쪽(focusX - aPx*(1+e))

  // 타원 궤도 점선
  ctx.beginPath();
  ctx.setLineDash([5, 4]);
  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 2;
  ctx.ellipse(centerX, cy, aPx, bPx, 0, 0, Math.PI * 2);
  ctx.stroke();
  ctx.setLineDash([]);

  // 근지점·원지점 표시
  const periX = focusX + aPx * (1 - e), apoX = focusX - aPx * (1 + e);
  dot(ctx, periX, cy, 4.5, BL);
  txt(ctx, '근지점 (속력 최대)', periX + 8, cy + 20, { c: BL, b: 1, s: 12, a: 'left' });
  dot(ctx, apoX, cy, 4.5, OR);
  txt(ctx, '원지점 (속력 최소)', apoX - 8, cy + 20, { c: OR, b: 1, s: 12, a: 'right' });

  // 지구 (초점 위치)
  drawEarth(ctx, focusX, cy, RePx);
  txt(ctx, '지구', focusX, cy + RePx + 15, { c: INK, b: 1, s: 12 });

  // 현재 위성 위치 (극좌표 r = a(1-e^2)/(1+e cos θ))
  const rPx = aPx * (1 - e * e) / (1 + e * Math.cos(ellAngle));
  const sx = focusX + rPx * Math.cos(ellAngle);
  const sy = cy - rPx * Math.sin(ellAngle);

  ln(ctx, focusX, cy, sx, sy, '#94a3b8', 1.5, [3, 3]);

  // 활력 방정식(Vis-viva equation): v^2 = GM(2/r - 1/a)
  const rRealRatio = aRatio * (1 - e * e) / (1 + e * Math.cos(ellAngle)); // in R_E
  const U0 = 62.56; // GJ (m=1000 kg, r=1 R_E)
  const E_tot = -U0 / (2 * aRatio);         // 총 역학적 에너지 = -GMm/(2a) (상수!)
  const U_now = -U0 / rRealRatio;           // 현재 퍼텐셜 에너지 = -GMm/r
  const K_now = E_tot - U_now;              // 현재 운동 에너지 = GMm(1/r - 1/(2a))
  const v_now = 7.91 * Math.sqrt(2 / rRealRatio - 1 / aRatio);

  // 타원 궤도의 정확한 접선 방향 속도 벡터 (극좌표 r(θ) = p/(1+e cos θ) 미분)
  const dx = -Math.sin(ellAngle), dy = -(e + Math.cos(ellAngle));
  const dNorm = Math.hypot(dx, dy);
  const vScale = 6.5 * v_now;
  arr(ctx, sx, sy, sx + (dx / dNorm) * vScale, sy + (dy / dNorm) * vScale, BL, 2.8);
  drawSatellite(ctx, sx, sy, Math.atan2(dy, dx) - Math.PI / 2);

  // 우측 에너지 보존 실시간 막대 및 위상 그래프 (x = 520 .. 970)
  const bx0 = 545, by0 = 215, scBar = 3.2;
  ln(ctx, bx0 - 15, by0, 725, by0, '#334155', 1.8);
  txt(ctx, '0', bx0 - 22, by0, { c: SUB, b: 1, s: 12 });
  txt(ctx, '실시간 에너지 변환과 보존 (GJ)', 630, 36, { c: INK, b: 1, s: 13.5 });

  [
    { x: 575, v: K_now, lab: 'K (운동)', col: BL },
    { x: 630, v: U_now, lab: 'U (퍼텐셜)', col: RD },
    { x: 685, v: E_tot, lab: 'E = K+U (보존!)', col: PU }
  ].forEach(b => {
    const h = b.v * scBar;
    ctx.fillStyle = b.col;
    if (h >= 0) {
      ctx.fillRect(b.x - 16, by0 - h, 32, h);
      txt(ctx, '+' + b.v.toFixed(1), b.x, by0 - h - 12, { c: b.col, b: 1, s: 12 });
    } else {
      ctx.fillRect(b.x - 16, by0, 32, -h);
      txt(ctx, '−' + Math.abs(b.v).toFixed(1), b.x, by0 - h + 14, { c: b.col, b: 1, s: 12 });
    }
    txt(ctx, b.lab, b.x, by0 + (h >= 0 ? 16 : -14), { c: b.col, b: 1, s: 12 });
  });

  // 우측 끝 공전 위치별 K, U, E 그래프 (x = 755 .. 970)
  const gx0 = 760, gx1 = 965, gy0 = 215;
  ln(ctx, gx0, gy0 - 140, gx0, gy0 + 165, INK, 1.5);
  ln(ctx, gx0, gy0, gx1, gy0, INK, 1.5);
  txt(ctx, '공전 각도 θ (근지점→원지점→근지점)', (gx0 + gx1) / 2, gy0 + 185, { c: SUB, b: 1, s: 11.5 });

  // K(θ), U(θ), E(θ) 곡선
  [
    { fn: th => { const r = aRatio * (1 - e * e) / (1 + e * Math.cos(th)); return (-U0 / (2 * aRatio)) - (-U0 / r); }, col: BL, w: 2.5 },
    { fn: th => { const r = aRatio * (1 - e * e) / (1 + e * Math.cos(th)); return -U0 / r; }, col: RD, w: 2.5 },
    { fn: th => -U0 / (2 * aRatio), col: PU, w: 3.5 }
  ].forEach(curve => {
    ctx.beginPath(); ctx.strokeStyle = curve.col; ctx.lineWidth = curve.w;
    for (let a = 0; a <= Math.PI * 2; a += 0.05) {
      const x = gx0 + (a / (Math.PI * 2)) * (gx1 - gx0);
      const y = gy0 - curve.fn(a) * scBar;
      a === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();
  });
  const curX = gx0 + (ellAngle / (Math.PI * 2)) * (gx1 - gx0);
  ln(ctx, curX, gy0 - 130, curX, gy0 + 150, '#94a3b8', 1.2, [3, 3]);
  dot(ctx, curX, gy0 - K_now * scBar, 5, BL);
  dot(ctx, curX, gy0 - U_now * scBar, 5, RD);
  dot(ctx, curX, gy0 - E_tot * scBar, 6, PU);
  txt(ctx, 'E = 일정 (보존)', gx1 - 8, gy0 - E_tot * scBar - 12, { a: 'right', c: PU, b: 1, s: 12 });

  txt(ctx, `현재 거리 r = ${rRealRatio.toFixed(2)} R_E  |  속력 v = ${v_now.toFixed(2)} km/s  |  K(${K_now.toFixed(1)}) + U(${U_now.toFixed(1)}) = E(${E_tot.toFixed(1)} GJ 일정!)`, W / 2, 438, { c: INK, b: 1, s: 13.5 });

  $('step').innerHTML =
    `인공위성이 타원 궤도를 돌 때 만유인력(보존력)만 일을 하므로 <b>역학적 에너지 E = K + U = −GMm/(2a) = ${E_tot.toFixed(1)} GJ로 항상 일정하게 보존</b>됩니다. ` +
    `<b>근지점 → 원지점</b>으로 갈 때는 속력이 줄어들며 <b>운동 에너지 K가 감소한 만큼 퍼텐셜 에너지 U가 똑같이 증가(ΔK = −ΔU)</b>합니다.`;
}

document.querySelectorAll('[data-ec]').forEach(b => {
  b.onclick = () => {
    $('ec2').value = b.dataset.ec;
    document.querySelectorAll('[data-ec]').forEach(x => x.classList.toggle('on', x === b));
  };
});
$('toPerigee').onclick = () => { ellAngle = 0; paused = true; $('pp').textContent = '▶ 재생'; };
$('toApogee').onclick = () => { ellAngle = Math.PI; paused = true; $('pp').textContent = '▶ 재생'; };

// ============================================================================
// [TAB 3] 원궤도 속력 vs 탈출속도 비교 (v_원 vs √2 v_원)
// ============================================================================
function scene3() {
  const cv = $('cvMain'), ctx = cv.getContext('2d'), W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);

  const mul = +$('vf3').value; // v / v_원
  $('vvf3').textContent = mul.toFixed(2) + ' v_원';

  const fx = 220, cy = 225, r0Px = 72;
  drawEarth(ctx, fx, cy, 34);

  // 4가지 기준 궤도 배경 표시 + 현재 선택된 궤도 강조
  const cases = [
    { m: 1.00,  col: '#2563eb', lab: '① v = v_원 (원궤도, E = −GMm/2r < 0)' },
    { m: 1.20,  col: '#059669', lab: '② v = 1.2 v_원 (타원궤도, E < 0)' },
    { m: 1.414, col: '#ea580c', lab: '③ v = √2 v_원 = v_탈출 (포물선 탈출, E = 0)' },
    { m: 1.55,  col: '#e11d48', lab: '④ v > √2 v_원 (쌍곡선 탈출, E > 0)' }
  ];

  // 궤적 그리기: 극좌표 r(θ) = r0 * mul^2 / (1 + (mul^2 - 1) cos θ)
  function drawOrbitCurve(mVal, col, isMain) {
    const e = mVal * mVal - 1;
    const p = r0Px * mVal * mVal;
    ctx.beginPath();
    ctx.strokeStyle = col;
    ctx.lineWidth = isMain ? 3.5 : 1.4;
    if (!isMain) ctx.setLineDash([4, 4]);
    let first = true;
    const maxTh = e >= 1 ? Math.acos(-1 / e) - 0.08 : Math.PI;
    for (let th = -maxTh; th <= maxTh; th += 0.02) {
      const r = p / (1 + e * Math.cos(th));
      if (r > 480 || r < 0) continue;
      const x = fx + r * Math.cos(th), y = cy - r * Math.sin(th);
      if (first) { ctx.moveTo(x, y); first = false; } else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.setLineDash([]);
  }

  cases.forEach(c => drawOrbitCurve(c.m, c.col, false));
  const curCol = mul < 1.02 ? BL : (mul < 1.40 ? GN : (mul < 1.43 ? OR : RD));
  drawOrbitCurve(mul, curCol, true);

  // 현재 배율 위성 애니메이션
  const eNow = mul * mul - 1;
  const pNow = r0Px * mul * mul;
  let thNow;
  if (eNow < 0.99) {
    thNow = (T * 1.4) % (Math.PI * 2);
  } else {
    const lim = Math.acos(-1 / eNow) - 0.12;
    thNow = ((T * 0.7) % 1) * lim;
  }
  const rNow = Math.min(440, pNow / (1 + eNow * Math.cos(thNow)));
  const sx = fx + rNow * Math.cos(thNow), sy = cy - rNow * Math.sin(thNow);
  dot(ctx, sx, sy, 7, curCol);

  // 발사 지점 표시
  dot(ctx, fx + r0Px, cy, 5, INK);
  txt(ctx, '발사점 (거리 r)', fx + r0Px + 8, cy + 16, { a: 'left', b: 1, s: 12 });

  // 우측 비교 표 & 에너지 분석 (x = 560 .. 975)
  const rx = 555;
  ctx.fillStyle = '#f8fafc';
  ctx.strokeStyle = '#cbd5e1';
  ctx.lineWidth = 1.5;
  ctx.fillRect(rx, 28, 420, 395);
  ctx.strokeRect(rx, 28, 420, 395);

  txt(ctx, '🚀 초기 속력에 따른 에너지와 궤도 비교', rx + 210, 56, { b: 1, s: 15, c: INK });

  // 정규화 에너지: U = -1.00 (단위: GMm/r), K = 0.5 * mul^2 * (GMm/r), E = (0.5*mul^2 - 1) GMm/r
  const kNorm = 0.5 * mul * mul;
  const uNorm = -1.0;
  const eNorm = kNorm + uNorm;

  const rows = [
    ['초기 속력 v', `${mul.toFixed(2)} √(GM/r) = ${(7.91 * mul).toFixed(2)} km/s`, curCol],
    ['운동 에너지 K', `+${kNorm.toFixed(2)} GMm/r`, BL],
    ['퍼텐셜 에너지 U', `−1.00 GMm/r`, RD],
    ['총 역학적 에너지 E', `${eNorm >= -0.005 && eNorm <= 0.005 ? '0.00' : (eNorm > 0 ? '+' : '−') + Math.abs(eNorm).toFixed(2)} GMm/r`, PU],
    ['궤도 형태', mul < 1.02 ? '원궤도 (속박, E = −GMm/2r)' : (mul < 1.405 ? '타원궤도 (속박, E < 0)' : (mul < 1.425 ? '포물선 궤도 (탈출, E = 0)' : '쌍곡선 궤도 (탈출, E > 0)')), curCol]
  ];
  rows.forEach((r, i) => {
    const yy = 102 + i * 44;
    ctx.fillStyle = '#fff';
    ctx.fillRect(rx + 16, yy - 17, 388, 34);
    txt(ctx, r[0], rx + 28, yy, { a: 'left', b: 1, s: 13, c: SUB });
    txt(ctx, r[1], rx + 392, yy, { a: 'right', b: 1, s: 13.5, c: r[2] });
  });

  txt(ctx, '핵심 비교: v_탈출 = √(2GM/r) = √2 × v_원궤도 (운동 에너지 K가 2배!)', rx + 210, 340, { b: 1, s: 13, c: INK });
  txt(ctx, '· 원궤도: K = +½(GMm/r), U = −GMm/r  →  E = −½(GMm/r) < 0', rx + 24, 368, { a: 'left', s: 12.5, c: BL });
  txt(ctx, '· 탈출속도: K = +GMm/r,   U = −GMm/r  →  E = 0 (무한원까지 탈출)', rx + 24, 394, { a: 'left', s: 12.5, c: OR });

  $('step').innerHTML =
    `반지름 r인 원궤도를 도는 인공위성의 운동 에너지는 <b>K = +GMm/(2r)</b>이고 역학적 에너지는 <b>E = −GMm/(2r)</b>입니다. ` +
    `이 위성이 지구 중력장을 탈출(<b>E = 0</b>)하려면 <b>운동 에너지를 2배(+GMm/r)</b>로 만들어야 하므로, 속력을 <b>√2배(약 1.414배, v<sub>탈출</sub> = √(2GM/r))</b>로 높여야 합니다.`;
}

document.querySelectorAll('[data-vf]').forEach(b => {
  b.onclick = () => {
    $('vf3').value = b.dataset.vf;
    T = 0;
    document.querySelectorAll('[data-vf]').forEach(x => x.classList.toggle('on', x === b));
  };
});

function go(i) {
  tab = i;
  [...$('tabs').children].forEach((b, k) => b.classList.toggle('on', k === i));
  for (let k = 0; k < 4; k++) $('c' + k).classList.toggle('show', k === i);
  $('v0').classList.toggle('show', i === 0);
  $('vCanvas').classList.toggle('show', i !== 0);
  $('note').innerHTML = '<span class="ws-tag">교과서 ' + TABS[i][1] + '</span>' + TABS[i][2];
}

function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000) * speed;
  last = now;
  if (!paused) T += dt;
  if (tab === 0) scene0();
  else if (tab === 1) scene1();
  else if (tab === 2) scene2(dt);
  else if (tab === 3) scene3();
  requestAnimationFrame(frame);
}

go(0);
requestAnimationFrame(frame);
</script>
</body>
</html>
"""


if __name__ == "__main__":
    run_sim()
