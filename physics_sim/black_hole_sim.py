import streamlit as st
import streamlit.components.v1 as components
import base64, os

st.sidebar.title("🌑 블랙홀 탐구")
st.sidebar.markdown("탈출속도가 빛의 속도를 넘는 천체를 탐구합니다.")

# 블랙홀 구조 이미지 (bh_structure.png 우선, 없으면 blackhole.png 사용)
_assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_struct_path = os.path.join(_assets, "bh_structure.png")
_fallback_path = os.path.join(_assets, "blackhole.png")
_img_path = _struct_path if os.path.exists(_struct_path) else _fallback_path
_img_b64 = ""
if os.path.exists(_img_path):
    with open(_img_path, "rb") as _f:
        _img_b64 = base64.b64encode(_f.read()).decode("utf-8")
    _img_mime = "image/png"

REACT_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#070c18;color:#e2e8f0;padding:16px;}
.tab-bar{display:flex;gap:6px;margin-bottom:20px;flex-wrap:wrap;}
.tab-btn{padding:9px 18px;border-radius:10px;border:1px solid #1e293b;background:#0d1526;
  color:#64748b;cursor:pointer;font-size:13px;font-weight:700;font-family:inherit;transition:all 0.2s;}
.tab-btn.active{background:#7c3aed;border-color:#8b5cf6;color:#fff;}
.tab-btn:hover:not(.active){border-color:#334155;color:#e2e8f0;}
.card{background:#0d1526;border:1px solid #1e293b;border-radius:14px;padding:20px;margin-bottom:16px;}
.hl-box{background:linear-gradient(135deg,#1a0a2e,#2e1060);border:1px solid #7c3aed;border-radius:12px;padding:16px;margin-bottom:14px;}
.result-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #1e293b;font-size:13px;}
.result-row:last-child{border-bottom:none;}
.val{color:#a78bfa;font-family:'Space Mono',monospace;font-weight:700;}
.preset-btn{padding:6px 14px;background:#1e293b;border:1px solid #334155;border-radius:8px;
  color:#94a3b8;cursor:pointer;font-size:12px;font-family:inherit;transition:all 0.2s;font-weight:600;}
.preset-btn:hover,.preset-btn.sel{border-color:#8b5cf6;color:#e2e8f0;background:#2d1060;}
input[type=range]{-webkit-appearance:none;width:100%;height:5px;background:#1e293b;border-radius:3px;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;
  background:#8b5cf6;cursor:pointer;box-shadow:0 0 8px rgba(139,92,246,0.6);}
.qa-btn{width:100%;display:flex;align-items:flex-start;gap:12px;padding:14px 18px;
  background:transparent;border:none;cursor:pointer;text-align:left;font-family:inherit;}
.step-btn{width:100%;display:flex;align-items:center;gap:12px;padding:14px 18px;
  background:#0d1526;border:none;cursor:pointer;text-align:left;font-family:inherit;border-radius:12px;}
.detect-card{border-radius:14px;border:1px solid #1e293b;padding:18px;
  background:#0d1526;transition:border-color 0.2s;}
.detect-card:hover{border-color:#7c3aed;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

const G_REAL = 6.674e-11;
const C_LIGHT = 3e8; // m/s

const calcRs = (M) => 2 * G_REAL * M / (C_LIGHT * C_LIGHT); // Schwarzschild radius (m)

const PRESETS_BH = [
  { name:'지구',    M:5.972e24,  R_real:6.371e6,   emoji:'🌍', color:'#3b82f6' },
  { name:'태양',    M:1.989e30,  R_real:6.960e8,   emoji:'☀️', color:'#fbbf24' },
  { name:'백색왜성',M:1.989e30*1.4, R_real:7e6,   emoji:'⚪', color:'#e2e8f0' },
  { name:'중성자별',M:1.989e30*2.0, R_real:12000,  emoji:'💫', color:'#60a5fa' },
  { name:'M87* BH', M:6.5e9*1.989e30, R_real:0,   emoji:'🌑', color:'#a78bfa' },
];

/* ── KaTeX 수식 렌더링 ── */
const Eq = ({ f, display=false, color='#c4b5fd' }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && window.katex)
      window.katex.render(f, ref.current, { throwOnError:false, displayMode:display });
  }, [f, display]);
  return <span ref={ref} style={{ color }} />;
};

/* ──────────────────────────────────────────────
   탭 1: 블랙홀이란? (개념 + 슈바르츠실트 유도)
────────────────────────────────────────────── */
const CONCEPT_STEPS = [
  { n:1, title:'탈출속도 공식 출발', color:'#3b82f6', bg:'#0d1f3c',
    formula:'v_{\\text{탈출}} = \\sqrt{\\dfrac{2GM}{R}}',
    note:'역학적 에너지 보존으로 유도한 탈출속도 공식입니다.' },
  { n:2, title:'탈출속도 = 빛의 속도 조건 설정', color:'#8b5cf6', bg:'#1a0d3c',
    formula:'c = \\sqrt{\\dfrac{2GM}{R_s}}',
    note:'탈출속도가 빛의 속도(c)와 같아지는 반지름 Rs를 구합니다.' },
  { n:3, title:'Rs에 대해 정리', color:'#a855f7', bg:'#1e0d3c',
    formula:'c^2 = \\dfrac{2GM}{R_s} \\implies R_s = \\dfrac{2GM}{c^2}',
    note:'양변에 Rs/c²를 곱하면 슈바르츠실트 반지름이 나옵니다.' },
  { n:4, title:'슈바르츠실트 반지름 (사건 지평선)', color:'#ec4899', bg:'#1f0014',
    formula:'R_s = \\dfrac{2GM}{c^2}',
    note:'이 반지름 안쪽에서는 탈출속도 > c이므로 빛도 탈출할 수 없습니다. 이 경계를 사건 지평선(Event Horizon)이라 합니다.' },
];

/* ──────────────────────────────────────────────
   시공간 구조 캔버스 (Flamm's Paraboloid)
────────────────────────────────────────────── */
function SpacetimeCanvas() {
  const ref    = useRef(null);
  const animRef = useRef(null);

  useEffect(() => {
    const canvas = ref.current; if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = 820, H = 500;
    canvas.width = W; canvas.height = H;
    let t = 0;

    /* ── 레이아웃 상수 ── */
    const CX     = W / 2;    // 중심 X
    const FY     = 148;      // 평평한 시공간 경계 Y
    const RS     = 68;       // 1Rₛ = 68px
    const K      = 52;       // 퍼널 깊이 계수
    const SING_Y = 462;      // 특이점 Y
    const MAX_D  = SING_Y - FY;
    const R_MAX  = 5.6;      // 표시 최대 반지름 (Rₛ 단위)

    const fX   = r => CX + r * RS;
    const fYat = r => Math.min(MAX_D, K / Math.sqrt(Math.max(r - 1, 0) + 5e-4));

    /* ── 빛 굴절 경로 계산 ── (별이 오른쪽에서 왼쪽으로 이동) */
    const STAR_TRACK_LEN = W + 120;
    const STAR_SPD = 38;  // px/s 정도
    const LIGHT_BASE_Y = FY - 52;  // 빛이 이동하는 기준 Y

    const loop = () => {
      t += 0.013;
      ctx.fillStyle = '#04060d'; ctx.fillRect(0, 0, W, H);

      /* ── 배경 별 (상단 평탄 영역) ── */
      for (let i = 0; i < 130; i++) {
        const sx = (i * 139.7 + 30) % W;
        const sy = (i * 83.3 + i * 17) % (FY - 20) + 6;
        const a  = 0.06 + (i % 5) * 0.05;
        ctx.beginPath(); ctx.arc(sx, sy, 0.3 + (i % 3) * 0.25, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(210,225,255,${a})`; ctx.fill();
      }

      /* ── 격자 (평탄 영역) ── */
      ctx.save(); ctx.globalAlpha = 0.18;
      for (let row = 1; row <= 5; row++) {
        const gy = 12 + (FY - 22) * row / 5;
        ctx.beginPath(); ctx.moveTo(10, gy); ctx.lineTo(W - 10, gy);
        ctx.strokeStyle = '#4f6ec5'; ctx.lineWidth = 0.8; ctx.stroke();
      }
      for (let col = 0; col <= 20; col++) {
        const gx = 10 + (W - 20) * col / 20;
        ctx.beginPath(); ctx.moveTo(gx, 10); ctx.lineTo(gx, FY);
        ctx.strokeStyle = '#4f6ec5'; ctx.lineWidth = 0.8; ctx.stroke();
      }
      ctx.restore();

      /* ── 퍼널 프로파일 계산 ── */
      const N = 280, profile = [];
      for (let i = 0; i <= N; i++) {
        const r = 1 + (R_MAX - 1) * i / N;
        const x = fX(r), y = FY + fYat(r);
        if (x <= W - 8) profile.push({ x, y });
      }
      const mirX = p => CX - (p.x - CX);

      /* 퍼널 내부 채우기 (검정) */
      ctx.fillStyle = '#000';
      ctx.fillRect(CX - RS, FY, RS * 2, MAX_D + 16);

      /* 퍼널 내부 보라 그라디언트 */
      const ig = ctx.createRadialGradient(CX, SING_Y, 0, CX, SING_Y, RS * 3);
      ig.addColorStop(0, 'rgba(110,0,200,0.22)');
      ig.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.beginPath(); ctx.arc(CX, SING_Y, RS * 3, 0, Math.PI * 2);
      ctx.fillStyle = ig; ctx.fill();

      /* 퍼널 면 채우기 */
      const fillSide = flip => {
        if (!profile.length) return;
        ctx.beginPath();
        ctx.moveTo(CX + (flip ? -RS : RS), FY);
        profile.forEach(p => ctx.lineTo(flip ? mirX(p) : p.x, p.y));
        const last = profile[profile.length - 1];
        ctx.lineTo(flip ? mirX(last) : last.x, FY);
        ctx.closePath();
        const g = ctx.createLinearGradient(CX, FY, CX, FY + MAX_D);
        g.addColorStop(0, 'rgba(139,92,246,0.11)');
        g.addColorStop(0.5, 'rgba(139,92,246,0.05)');
        g.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = g; ctx.fill();
      };
      fillSide(false); fillSide(true);

      /* 퍼널 수평 그리드선 */
      [1.5, 2, 2.5, 3, 4, 5].forEach(r => {
        const x = fX(r), y = FY + fYat(r), mx = CX - (x - CX);
        ctx.beginPath(); ctx.moveTo(mx, y); ctx.lineTo(x, y);
        ctx.strokeStyle = 'rgba(80,105,185,0.10)'; ctx.lineWidth = 0.7; ctx.stroke();
      });

      /* 퍼널 프로파일 선 */
      const drawProfile = flip => {
        if (!profile.length) return;
        ctx.beginPath();
        ctx.moveTo(CX + (flip ? -RS : RS), FY);
        profile.forEach(p => ctx.lineTo(flip ? mirX(p) : p.x, p.y));
        const g = ctx.createLinearGradient(CX, FY, CX, FY + MAX_D * 0.6);
        g.addColorStop(0, 'rgba(167,139,250,0.95)');
        g.addColorStop(0.6, 'rgba(139,92,246,0.55)');
        g.addColorStop(1, 'rgba(109,40,217,0.2)');
        ctx.strokeStyle = g; ctx.lineWidth = 2.4; ctx.stroke();
      };
      drawProfile(false); drawProfile(true);

      /* ── 사건 지평선 수직 글로우 선 ── */
      [-RS, RS].forEach(dx => {
        const ehX = CX + dx;
        const gEH = ctx.createLinearGradient(ehX - 12, 0, ehX + 12, 0);
        gEH.addColorStop(0, 'rgba(139,92,246,0)');
        gEH.addColorStop(0.5, 'rgba(167,139,250,0.5)');
        gEH.addColorStop(1, 'rgba(139,92,246,0)');
        ctx.fillStyle = gEH; ctx.fillRect(ehX - 12, FY - 36, 24, MAX_D * 0.82);
        ctx.beginPath(); ctx.moveTo(ehX, FY - 36); ctx.lineTo(ehX, FY + MAX_D * 0.80);
        ctx.strokeStyle = 'rgba(167,139,250,0.98)'; ctx.lineWidth = 2.2; ctx.stroke();
      });

      /* ── 평평한 시공간 기준선 ── */
      ctx.beginPath(); ctx.moveTo(10, FY); ctx.lineTo(W - 10, FY);
      ctx.strokeStyle = 'rgba(70,90,170,0.38)'; ctx.lineWidth = 1.2; ctx.stroke();

      /* ── 광자 구 점선 (r=1.5Rs) ── */
      const psXr = fX(1.5), psY = FY + fYat(1.5), psXl = CX - (psXr - CX);
      ctx.save(); ctx.setLineDash([6, 6]);
      ctx.strokeStyle = 'rgba(251,191,36,0.65)'; ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.moveTo(psXl, psY); ctx.lineTo(psXr, psY); ctx.stroke();
      ctx.restore();

      /* ── ISCO 점선 (r=3Rs) ── */
      const iscoXr = fX(3), iscoY = FY + fYat(3), iscoXl = CX - (iscoXr - CX);
      ctx.save(); ctx.setLineDash([3, 8]);
      ctx.strokeStyle = 'rgba(34,197,94,0.45)'; ctx.lineWidth = 1.4;
      ctx.beginPath(); ctx.moveTo(iscoXl, iscoY); ctx.lineTo(iscoXr, iscoY); ctx.stroke();
      ctx.restore();

      /* ── 특이점 ── */
      const sg = ctx.createRadialGradient(CX, SING_Y, 0, CX, SING_Y, 28);
      sg.addColorStop(0, '#fff');
      sg.addColorStop(0.18, '#fef3c7');
      sg.addColorStop(0.55, 'rgba(255,80,10,0.5)');
      sg.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.beginPath(); ctx.arc(CX, SING_Y, 28, 0, Math.PI * 2);
      ctx.fillStyle = sg; ctx.fill();
      ctx.beginPath(); ctx.arc(CX, SING_Y, 6, 0, Math.PI * 2);
      ctx.fillStyle = '#fff'; ctx.fill();

      /* ── 애니메이션: 중력 굴절 빛 ── */
      /* 별(광원)이 오른쪽 위에 고정, 빛이 왼쪽으로 진행하며 굴절 */
      const STAR_X = W - 60, STAR_Y = LIGHT_BASE_Y - 18;
      /* 별 그리기 */
      const stG = ctx.createRadialGradient(STAR_X, STAR_Y, 1, STAR_X, STAR_Y, 14);
      stG.addColorStop(0, '#fffde7'); stG.addColorStop(0.4, '#fde047');
      stG.addColorStop(1, 'rgba(253,224,71,0)');
      ctx.beginPath(); ctx.arc(STAR_X, STAR_Y, 14, 0, Math.PI * 2);
      ctx.fillStyle = stG; ctx.fill();
      ctx.beginPath(); ctx.arc(STAR_X, STAR_Y, 5.5, 0, Math.PI * 2);
      ctx.fillStyle = '#fef9c3'; ctx.fill();

      /* 빛의 굴절 경로: 정적 곡선 (별 → 중력 굴절 → 왼쪽 관측자) */
      ctx.beginPath();
      const bendPts = [];
      for (let px = STAR_X; px >= 10; px -= 4) {
        const dist = Math.abs(px - CX) / RS;
        const bend = dist < 6 ? 22 * Math.exp(-dist * dist * 0.12) : 0;
        const py   = LIGHT_BASE_Y + bend;
        bendPts.push({ x: px, y: py });
      }
      if (bendPts.length > 0) {
        ctx.moveTo(bendPts[0].x, bendPts[0].y);
        bendPts.slice(1).forEach(p => ctx.lineTo(p.x, p.y));
      }
      ctx.strokeStyle = 'rgba(253,224,71,0.32)'; ctx.lineWidth = 1.8; ctx.stroke();

      /* 빛 입자 (경로 위를 이동) */
      const prog = (t * STAR_SPD) % (STAR_X - 10);
      const lpX  = STAR_X - prog;
      const ldist = Math.abs(lpX - CX) / RS;
      const lbend = ldist < 6 ? 22 * Math.exp(-ldist * ldist * 0.12) : 0;
      const lpY   = LIGHT_BASE_Y + lbend;
      const lpG   = ctx.createRadialGradient(lpX, lpY, 1, lpX, lpY, 9);
      lpG.addColorStop(0, '#fffde7'); lpG.addColorStop(1, 'rgba(253,224,71,0)');
      ctx.beginPath(); ctx.arc(lpX, lpY, 9, 0, Math.PI * 2); ctx.fillStyle = lpG; ctx.fill();
      ctx.beginPath(); ctx.arc(lpX, lpY, 4, 0, Math.PI * 2);
      ctx.fillStyle = '#fde047'; ctx.fill();

      /* ── 애니메이션: 광자 구 궤도 광자 ── */
      const psOrb = psXl + (psXr - psXl) * ((Math.cos(t * 1.05) + 1) / 2);
      ctx.beginPath(); ctx.arc(psOrb, psY, 4.2, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(251,191,36,0.88)'; ctx.fill();
      ctx.beginPath(); ctx.arc(psOrb, psY, 8, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(251,191,36,0.2)'; ctx.lineWidth = 1; ctx.stroke();

      /* ── 애니메이션: 사건 지평선 근처 포획 광자 ── */
      const capAngle = t * 1.5;
      const capRn    = 1.12 + (Math.sin(t * 0.35) + 1) * 0.12;
      const capRpx   = capRn * RS;
      const capX     = CX + capRpx * Math.cos(capAngle);
      const capYraw  = FY + fYat(capRn) * 0.38 * Math.abs(Math.cos(capAngle * 0.5));
      if (capRpx >= RS + 2) {
        ctx.beginPath(); ctx.arc(capX, capYraw, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(252,110,20,0.9)'; ctx.fill();
        ctx.beginPath(); ctx.arc(capX, capYraw, 7, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(252,110,20,0.2)'; ctx.lineWidth = 1; ctx.stroke();
      }

      /* ══ 레이블 ══ */
      ctx.save();

      /* 특이점 */
      ctx.textAlign = 'left'; ctx.fillStyle = '#fbbf24';
      ctx.font = 'bold 13px Noto Sans KR';
      ctx.fillText('특이점', CX + 16, SING_Y - 14);
      ctx.font = '11px Noto Sans KR'; ctx.fillStyle = 'rgba(251,191,36,0.65)';
      ctx.fillText('(Singularity)', CX + 16, SING_Y + 1);
      ctx.fillText('밀도 → ∞, 물리법칙의 한계', CX + 16, SING_Y + 16);
      ctx.strokeStyle = 'rgba(251,191,36,0.55)'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(CX + 13, SING_Y - 4); ctx.lineTo(CX + 7, SING_Y); ctx.stroke();

      /* 사건 지평선 왼쪽 */
      ctx.textAlign = 'right'; ctx.fillStyle = '#a78bfa';
      ctx.font = 'bold 12px Noto Sans KR';
      ctx.fillText('사건 지평선', CX - RS - 14, FY + 46);
      ctx.font = '10px Noto Sans KR'; ctx.fillStyle = 'rgba(167,139,250,0.72)';
      ctx.fillText('(Event Horizon)', CX - RS - 14, FY + 60);
      ctx.fillText('← 포획되는 빛', CX - RS - 14, FY + 74);
      ctx.strokeStyle = 'rgba(167,139,250,0.45)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(CX - RS - 12, FY + 52); ctx.lineTo(CX - RS - 2, FY + 52); ctx.stroke();

      /* 사건 지평선 오른쪽 */
      ctx.textAlign = 'left'; ctx.fillStyle = '#a78bfa';
      ctx.font = 'bold 12px Noto Sans KR';
      ctx.fillText('사건 지평선', CX + RS + 14, FY + 46);
      ctx.font = '10px Noto Sans KR'; ctx.fillStyle = 'rgba(167,139,250,0.72)';
      ctx.fillText('(Event Horizon = Rₛ)', CX + RS + 14, FY + 60);
      ctx.fillText('빛도 탈출 불가 경계', CX + RS + 14, FY + 74);
      ctx.strokeStyle = 'rgba(167,139,250,0.45)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(CX + RS + 12, FY + 52); ctx.lineTo(CX + RS + 2, FY + 52); ctx.stroke();

      /* 광자 구 */
      ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(251,191,36,0.95)';
      ctx.font = 'bold 11px Noto Sans KR';
      ctx.fillText('광자 구 (r = 1.5 Rₛ)', psXr + 12, psY + 4);
      ctx.font = '10px Noto Sans KR'; ctx.fillStyle = 'rgba(251,191,36,0.58)';
      ctx.fillText('빛도 달을 경도로 원형 궤도', psXr + 12, psY + 17);
      ctx.strokeStyle = 'rgba(251,191,36,0.38)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(psXr + 10, psY + 1); ctx.lineTo(psXr + 2, psY + 1); ctx.stroke();

      /* ISCO */
      ctx.textAlign = 'left'; ctx.fillStyle = 'rgba(34,197,94,0.85)';
      ctx.font = 'bold 11px Noto Sans KR';
      ctx.fillText('ISCO (r = 3 Rₛ)', iscoXr + 12, iscoY + 4);
      ctx.font = '10px Noto Sans KR'; ctx.fillStyle = 'rgba(34,197,94,0.55)';
      ctx.fillText('최내각 안정 원형 궤도', iscoXr + 12, iscoY + 17);

      /* 평평한 시공간 */
      ctx.textAlign = 'center'; ctx.font = '11px Noto Sans KR';
      ctx.fillStyle = 'rgba(90,120,200,0.75)';
      ctx.fillText('평평한 시공간 — 사건 지평선 외부 (탈출 가능)', CX, FY - 18);

      /* 내부 */
      ctx.font = 'bold 11px Noto Sans KR'; ctx.fillStyle = 'rgba(139,92,246,0.38)';
      ctx.fillText('내부 — 탈출 불가', CX, FY + MAX_D * 0.33);

      /* 빛 경로 레이블 */
      ctx.textAlign = 'center'; ctx.font = '11px Noto Sans KR';
      ctx.fillStyle = 'rgba(253,224,71,0.72)';
      ctx.fillText('중력에 의해 휘어진 빛', CX, LIGHT_BASE_Y - 12);

      ctx.restore();

      animRef.current = requestAnimationFrame(loop);
    };

    animRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animRef.current);
  }, []);

  return (
    <div style={{marginBottom:16}}>
      <div style={{background:'linear-gradient(135deg,#08031a,#120830)',borderRadius:'14px 14px 0 0',
        padding:'13px 20px',border:'1px solid #4c1d95',borderBottom:'none',
        display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          <p style={{color:'#c4b5fd',fontWeight:800,fontSize:14}}>
            🌀 블랙홀 주변 시공간 구조 — 플람 파라볼로이드 (Flamm's Paraboloid)
          </p>
          <p style={{color:'#6d28d9',fontSize:12,marginTop:3}}>
            시공간의 공간적 곡률을 단면(Cross-section)으로 표현합니다. 깊이는 시공간 곡률의 세기를 나타냅니다.
          </p>
        </div>
        <div style={{display:'flex',flexDirection:'column',gap:5,fontSize:11,flexShrink:0,marginLeft:20}}>
          {[
            ['──','rgba(167,139,250,0.85)','사건 지평선 (EH)'],
            ['╌╌','rgba(251,191,36,0.8)','광자 구 (r=1.5Rₛ)'],
            ['╌ ','rgba(34,197,94,0.8)','ISCO (r=3Rₛ)'],
            ['●','#fbbf24','특이점'],
            ['●','rgba(253,224,71,0.9)','굴절되는 빛'],
          ].map(([sym,col,lbl],i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:col,fontFamily:'monospace',fontWeight:700,minWidth:22,fontSize:13}}>{sym}</span>
              <span style={{color:'#64748b'}}>{lbl}</span>
            </div>
          ))}
        </div>
      </div>
      <canvas ref={ref} width={820} height={500}
        style={{width:'100%',height:'500px',borderRadius:'0 0 14px 14px',
          background:'#04060d',display:'block',border:'1px solid #4c1d95',borderTop:'none'}}/>
    </div>
  );
}

function ConceptTab() {
  const [open, setOpen] = useState(null);
  const [animT, setAnimT] = useState(0);
  const canvasRef = useRef(null);
  const animRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current; if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let t = 0;
    const loop = () => {
      t += 0.015;
      const W = canvas.width, H = canvas.height;
      ctx.fillStyle = '#05070a'; ctx.fillRect(0,0,W,H);

      // 별
      for (let i=0;i<80;i++){
        const sx=(i*137.5)%W, sy=(i*97+i*11)%H;
        ctx.beginPath(); ctx.arc(sx,sy,0.4+(i%3)*0.3,0,Math.PI*2);
        ctx.fillStyle=`rgba(210,225,255,${0.1+(i%5)*0.06})`; ctx.fill();
      }

      const CX=W*0.5, CY=H*0.5;
      const BH_R=55;

      // 강착 원반 (Accretion Disk)
      for (let layer=0; layer<3; layer++){
        const rx = BH_R*(2.0+layer*0.7);
        const ry = rx*0.22;
        const col = ['rgba(255,100,20,', 'rgba(255,160,40,', 'rgba(255,200,80,'][layer];
        const alpha = [0.55, 0.35, 0.2][layer];
        ctx.save();
        ctx.translate(CX, CY);
        ctx.beginPath(); ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI*2);
        const grad = ctx.createRadialGradient(0,0,BH_R,0,0,rx);
        grad.addColorStop(0, col+alpha+')');
        grad.addColorStop(1, col+'0)');
        ctx.fillStyle = grad; ctx.fill();
        ctx.restore();
      }

      // 제트 (Relativistic Jets)
      [[-1,1],[1,-1]].forEach(([sign, dir])=>{
        const jetLen = 100;
        const spread = 14;
        const jetGrad = ctx.createLinearGradient(CX, CY, CX, CY+sign*jetLen);
        jetGrad.addColorStop(0, 'rgba(139,92,246,0.8)');
        jetGrad.addColorStop(1, 'rgba(139,92,246,0)');
        ctx.beginPath();
        ctx.moveTo(CX-spread*0.3, CY+sign*BH_R*0.8);
        ctx.lineTo(CX-spread, CY+sign*(BH_R+jetLen));
        ctx.lineTo(CX+spread, CY+sign*(BH_R+jetLen));
        ctx.lineTo(CX+spread*0.3, CY+sign*BH_R*0.8);
        ctx.fillStyle = jetGrad; ctx.fill();
      });

      // 블랙홀 본체
      const bhGrad = ctx.createRadialGradient(CX-10,CY-10,5,CX,CY,BH_R);
      bhGrad.addColorStop(0,'#1a0a30'); bhGrad.addColorStop(0.5,'#08040f'); bhGrad.addColorStop(1,'#000');
      ctx.beginPath(); ctx.arc(CX,CY,BH_R,0,Math.PI*2); ctx.fillStyle=bhGrad; ctx.fill();

      // 사건 지평선 글로우
      const ehGrad = ctx.createRadialGradient(CX,CY,BH_R,CX,CY,BH_R+20);
      ehGrad.addColorStop(0,'rgba(139,92,246,0.6)'); ehGrad.addColorStop(1,'rgba(139,92,246,0)');
      ctx.beginPath(); ctx.arc(CX,CY,BH_R+20,0,Math.PI*2); ctx.fillStyle=ehGrad; ctx.fill();
      ctx.beginPath(); ctx.arc(CX,CY,BH_R,0,Math.PI*2);
      ctx.strokeStyle='rgba(139,92,246,0.9)'; ctx.lineWidth=2; ctx.stroke();

      // 빛의 나선 (포획되는 광자)
      const photons = [0, 1.2, 2.4, 3.8, 5.0];
      photons.forEach((ph, pi) => {
        const angle = t * 1.8 + ph;
        const decayFac = Math.min(1, (t % (Math.PI*2)) / (Math.PI*2));
        const r = BH_R * 2.8 - (t * 6 + pi * 25) % (BH_R * 1.8);
        if (r < BH_R) return;
        const px2 = CX + r * Math.cos(angle);
        const py2 = CY + r * Math.sin(angle) * 0.4;
        ctx.beginPath(); ctx.arc(px2,py2,2.5,0,Math.PI*2);
        ctx.fillStyle=`rgba(253,224,71,0.85)`; ctx.fill();
        ctx.beginPath(); ctx.arc(px2,py2,5,0,Math.PI*2);
        ctx.strokeStyle='rgba(253,224,71,0.2)'; ctx.lineWidth=1; ctx.stroke();
      });

      // 라벨
      ctx.fillStyle='rgba(167,139,250,0.9)'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText('사건 지평선', CX, CY-BH_R-12);
      ctx.fillStyle='rgba(252,211,77,0.7)'; ctx.font='11px Noto Sans KR';
      ctx.fillText('강착 원반', CX+BH_R*2.2, CY+BH_R*0.2);
      ctx.fillStyle='rgba(139,92,246,0.7)';
      ctx.fillText('상대론적 제트', CX+35, CY-BH_R-45);

      ctx.textAlign='left';
      animRef.current = requestAnimationFrame(loop);
    };
    animRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animRef.current);
  }, []);

  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>🌑 핵심 질문</p>
        <p style={{color:'#cbd5e1',fontSize:14,lineHeight:1.8}}>
          탈출속도 공식 <Eq f="v_{\text{탈출}}=\sqrt{2GM/R}"/> 에서,
          만약 천체의 반지름을 충분히 작게 만들어 <strong style={{color:'#a78bfa'}}>탈출속도 = 빛의 속도(c)</strong>가 되면 어떻게 될까?
          빛조차 탈출하지 못하는 이 천체를 <strong style={{color:'#c4b5fd'}}>블랙홀</strong>이라 한다.
        </p>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginBottom:16}}>
        <canvas ref={canvasRef} width={480} height={300}
          style={{width:'100%',height:'300px',borderRadius:'12px',background:'#05070a'}}/>
        <div style={{display:'flex',flexDirection:'column',gap:12}}>
          <div className="card" style={{flex:1}}>
            <p style={{color:'#a78bfa',fontWeight:700,fontSize:14,marginBottom:10}}>📌 블랙홀의 핵심 특성</p>
            {[
              ['사건 지평선','빛도 탈출 불가능한 경계면. 반지름 = 슈바르츠실트 반지름 Rs'],
              ['특이점','중심부. 밀도가 무한대로 발산하는 점. 현재 물리학의 한계'],
              ['강착 원반','블랙홀로 빨려드는 물질이 이루는 뜨거운 원반. X선 방출'],
              ['상대론적 제트','블랙홀의 자기장에 의해 수직 방향으로 뿜어지는 물질'],
            ].map(([t,d],i)=>(
              <div key={i} style={{borderBottom:'1px solid #1e293b',padding:'8px 0',display:'flex',gap:10}}>
                <span style={{color:'#8b5cf6',fontWeight:800,fontSize:12,flexShrink:0,paddingTop:2}}>▪</span>
                <div>
                  <p style={{color:'#e2e8f0',fontSize:13,fontWeight:700}}>{t}</p>
                  <p style={{color:'#64748b',fontSize:12,lineHeight:1.6,marginTop:2}}>{d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card" style={{marginBottom:16}}>
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>📐 슈바르츠실트 반지름 유도</p>
        <div style={{display:'flex',flexDirection:'column',gap:10}}>
          {CONCEPT_STEPS.map((s,i)=>(
            <div key={i} style={{border:`1px solid ${open===i?s.color+'90':'#1e293b'}`,borderRadius:14,overflow:'hidden',transition:'border-color 0.25s'}}>
              <button className="step-btn" onClick={()=>setOpen(open===i?null:i)}>
                <div style={{width:32,height:32,borderRadius:'50%',background:s.color,display:'flex',
                  alignItems:'center',justifyContent:'center',color:'#fff',fontWeight:800,fontSize:14,flexShrink:0}}>{s.n}</div>
                <div style={{flex:1}}>
                  <p style={{color:'#e2e8f0',fontSize:14,fontWeight:700}}>{s.title}</p>
                </div>
                <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',
                  transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
              </button>
              <div style={{maxHeight:open===i?'250px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
                <div style={{padding:'18px 24px',background:s.bg,display:'flex',flexDirection:'column',gap:12}}>
                  <div style={{background:'rgba(0,0,0,0.3)',borderRadius:12,padding:'16px 24px',
                    display:'flex',justifyContent:'center',border:`1px solid ${s.color}30`}}>
                    <Eq f={s.formula} display={true} color={s.color}/>
                  </div>
                  <div style={{display:'flex',gap:10,alignItems:'flex-start'}}>
                    <span style={{fontSize:15,flexShrink:0}}>💡</span>
                    <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.75}}>{s.note}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── 블랙홀 구조 이미지 + 설명 ── */}
      <SpacetimeCanvas/>

      <div className="card" style={{marginBottom:16}}>
        <p style={{fontWeight:800,color:'#e2e8f0',fontSize:15,marginBottom:14}}>
          🖼️ 블랙홀의 구조 — 단면도
        </p>
        <div style={{display:'grid',gridTemplateColumns:'220px 1fr',gap:20,alignItems:'flex-start'}}>
          {/* 이미지 */}
          <div style={{borderRadius:12,overflow:'hidden',border:'1px solid #3b1e7c',
            background:'#000',display:'flex',alignItems:'center',justifyContent:'center'}}>
            {"__BH_IMG_B64__" !== "" ? (
              <img src={"data:image/png;base64,__BH_IMG_B64__"}
                style={{width:'100%',display:'block',borderRadius:11}}
                alt="블랙홀 구조 단면도"/>
            ) : (
              <div style={{padding:24,color:'#475569',fontSize:12,textAlign:'center'}}>
                이미지를 assets/bh_structure.png로 저장해 주세요.
              </div>
            )}
          </div>
          {/* 구조 설명 */}
          <div style={{display:'flex',flexDirection:'column',gap:10}}>
            <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.8,marginBottom:6}}>
              블랙홀을 수직으로 잘라 본 단면도입니다. 시공간의 곡률이 심할수록 "깊이"가 깊어집니다.
            </p>
            {[
              ['#a78bfa','사건 지평선 (Event Horizon)',
                `반지름 Rₛ = 2GM/c²인 구면. 이 경계 안쪽에서는 탈출속도 > c 이므로 빛도 탈출 불가. 외부 관측자는 이 경계 너머를 볼 수 없습니다.`],
              ['#fbbf24','특이점 (Singularity)',
                `블랙홀의 중심. 밀도 → ∞, 부피 → 0. 현재 물리학(일반 상대성 이론)이 적용되지 않는 지점으로, 양자 중력 이론이 필요합니다.`],
              ['rgba(251,191,36,0.8)','광자 구 (Photon Sphere)',
                `r = 1.5 Rₛ인 구면. 빛이 원형 궤도를 그릴 수 있는 경계이지만, 불안정합니다. 약간의 교란만 있어도 빛은 탈출하거나 포획됩니다.`],
              ['rgba(34,197,94,0.8)','ISCO (최내각 안정 원형 궤도)',
                `r = 3 Rₛ. 물질이 안정적으로 원 궤도를 유지할 수 있는 가장 안쪽 경계. 이보다 안쪽의 물질은 빠르게 블랙홀로 나선형으로 떨어집니다.`],
            ].map(([col,title,desc],i)=>(
              <div key={i} style={{display:'flex',gap:10,padding:'8px 0',
                borderBottom:'1px solid #1e293b'}}>
                <div style={{width:4,flexShrink:0,borderRadius:2,background:col,marginTop:3,alignSelf:'stretch'}}/>
                <div>
                  <p style={{color:col,fontWeight:700,fontSize:13,marginBottom:3}}>{title}</p>
                  <p style={{color:'#64748b',fontSize:12,lineHeight:1.7}}>{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{background:'linear-gradient(135deg,#2e0a4e,#1a0030)',borderRadius:16,padding:'20px 28px',border:'1px solid #8b5cf6'}}>
        <p style={{color:'#c4b5fd',fontWeight:800,fontSize:15,marginBottom:8}}>✅ 결론</p>
        <p style={{color:'#ddd6fe',fontSize:13,lineHeight:1.85}}>
          슈바르츠실트 반지름 <Eq f="R_s = \dfrac{2GM}{c^2}"/> 안쪽에서는 탈출속도가 빛의 속도를 초과하므로,
          어떤 물체도, 심지어 빛조차도 탈출할 수 없습니다.<br/>
          <strong style={{color:'#a78bfa'}}>블랙홀이 되는 조건</strong>: 천체의 반지름 ≤ Rs = 2GM/c²<br/>
          지구가 블랙홀이 되려면 반지름을 약 <strong style={{color:'#fbbf24'}}>9 mm</strong>로 압축해야 합니다.
        </p>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 2: 슈바르츠실트 반지름 계산기
────────────────────────────────────────────── */
function SchwarzschildTab() {
  const [sel, setSel]    = useState(0);
  const [massScale, setMassScale] = useState(1); // solar mass multiplier
  const [isCustom, setIsCustom]   = useState(false);
  const canvasRef = useRef(null);

  const preset = PRESETS_BH[sel];
  const M_use  = isCustom ? massScale * 1.989e30 : preset.M;
  const Rs = calcRs(M_use);
  const R_real = isCustom ? preset.R_real : preset.R_real;
  const isBH_now = !isCustom && (R_real === 0 || R_real < Rs);

  // 시각화: 반지름 비교 다이어그램
  useEffect(() => {
    const canvas = canvasRef.current; if(!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.fillStyle='#05070a'; ctx.fillRect(0,0,W,H);

    // 별
    for (let i=0;i<60;i++){
      const sx=(i*137)%W, sy=(i*97)%H;
      ctx.beginPath(); ctx.arc(sx,sy,0.4+(i%3)*0.25,0,Math.PI*2);
      ctx.fillStyle=`rgba(200,220,255,${0.08+(i%5)*0.05})`; ctx.fill();
    }

    const M = M_use;
    const Rs_v = Rs;
    const R_v = R_real;

    // 중앙 위치
    const CX = W*0.5, CY = H*0.5;

    // 반지름 스케일 계산 (시각화)
    const maxR = Math.max(Rs_v, R_v);
    const scale = Math.min(H*0.35, W*0.35) / Math.max(maxR, 1);
    const Rs_px = Math.max(Math.min(Rs_v * scale, 120), 8);
    const R_px  = R_v > 0 ? Math.max(Math.min(R_v * scale, 120), 8) : 0;

    // 슈바르츠실트 반지름 (사건 지평선)
    const ehGrad = ctx.createRadialGradient(CX,CY,0,CX,CY,Rs_px);
    ehGrad.addColorStop(0,'#000'); ehGrad.addColorStop(0.7,'#0d0518'); ehGrad.addColorStop(1,'#1a0030');
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px,0,Math.PI*2); ctx.fillStyle=ehGrad; ctx.fill();
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px,0,Math.PI*2);
    ctx.strokeStyle='rgba(139,92,246,0.9)'; ctx.lineWidth=2.5; ctx.stroke();

    // 글로우
    const gGrad = ctx.createRadialGradient(CX,CY,Rs_px,CX,CY,Rs_px+20);
    gGrad.addColorStop(0,'rgba(139,92,246,0.4)'); gGrad.addColorStop(1,'rgba(139,92,246,0)');
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px+20,0,Math.PI*2); ctx.fillStyle=gGrad; ctx.fill();

    // 실제 천체 반지름 (있는 경우)
    if (R_v > 0) {
      const bodyGrad = ctx.createRadialGradient(CX-R_px*0.2,CY-R_px*0.2,R_px*0.1,CX,CY,R_px);
      const col = preset.color;
      bodyGrad.addColorStop(0, col+'ff'); bodyGrad.addColorStop(1, col+'66');
      ctx.save(); ctx.globalAlpha=0.5;
      ctx.beginPath(); ctx.arc(CX,CY,R_px,0,Math.PI*2);
      ctx.fillStyle = bodyGrad; ctx.fill();
      ctx.restore();
      ctx.beginPath(); ctx.arc(CX,CY,R_px,0,Math.PI*2);
      ctx.strokeStyle=col+'99'; ctx.lineWidth=1.5; ctx.stroke();
    }

    // 라벨 - Rs
    ctx.fillStyle='#a78bfa'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
    ctx.fillText('사건 지평선 (Rs)', CX, CY - Rs_px - 12);

    const fmtR = (r) => {
      if (r >= 1e9) return (r/1e9).toFixed(2) + ' Gm';
      if (r >= 1e6) return (r/1e6).toFixed(2) + ' Mm';
      if (r >= 1e3) return (r/1e3).toFixed(2) + ' km';
      if (r >= 1)   return r.toFixed(2) + ' m';
      return (r*1000).toFixed(2) + ' mm';
    };

    ctx.fillStyle='#ddd6fe'; ctx.font='11px Space Mono'; ctx.textAlign='center';
    ctx.fillText(fmtR(Rs_v), CX, CY - Rs_px - 28);

    if (R_v > 0) {
      ctx.fillStyle='rgba(200,200,255,0.7)'; ctx.font='bold 11px Noto Sans KR';
      ctx.fillText('실제 반지름', CX + R_px + 15, CY);
      ctx.fillStyle='rgba(200,200,255,0.55)'; ctx.font='10px Space Mono';
      ctx.fillText(fmtR(R_v), CX + R_px + 15, CY + 15);
    }

    // 비교 표시
    if (R_v > 0) {
      const ratio = R_v / Rs_v;
      ctx.fillStyle='rgba(148,163,184,0.8)'; ctx.font='11px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText(`실제 반지름 = Rs × ${ratio.toExponential(2)}`, CX, H-14);
    }

    ctx.textAlign='left';
  }, [sel, massScale, isCustom]);

  const fmtNum = (r) => {
    if (r >= 1e12) return (r/1e12).toFixed(3) + ' Tm (테라미터)';
    if (r >= 1e9)  return (r/1e9).toFixed(3) + ' Gm (기가미터)';
    if (r >= 1e6)  return (r/1e6).toFixed(3) + ' Mm → ' + (r/1e3).toFixed(0) + ' km';
    if (r >= 1e3)  return (r/1e3).toFixed(3) + ' km';
    if (r >= 1)    return r.toFixed(4) + ' m';
    return (r*1000).toFixed(4) + ' mm';
  };

  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>🔭 슈바르츠실트 반지름 계산기</p>
        <p style={{color:'#cbd5e1',fontSize:14}}>
          공식: <Eq f="R_s = \dfrac{2GM}{c^2}"/> &nbsp;
          지구 Rs ≈ 8.9 mm | 태양 Rs ≈ 3.0 km
        </p>
      </div>

      <div style={{display:'flex',gap:8,flexWrap:'wrap',marginBottom:16}}>
        {PRESETS_BH.map((p,i)=>(
          <button key={i} className={`preset-btn ${!isCustom&&sel===i?'sel':''}`}
            onClick={()=>{ setSel(i); setIsCustom(false); }}>
            {p.emoji} {p.name}
          </button>
        ))}
        <button className={`preset-btn ${isCustom?'sel':''}`} onClick={()=>setIsCustom(true)}>
          ✏️ 태양질량 배수
        </button>
      </div>

      {isCustom && (
        <div className="card" style={{marginBottom:14}}>
          <label>태양 질량의 배수: {massScale.toLocaleString('ko-KR')} M☉</label>
          <input type="range" min={0.1} max={1e10} step={0.1}
            value={massScale} onChange={e=>setMassScale(parseFloat(e.target.value))}/>
          <p style={{textAlign:'center',fontSize:12,color:'#64748b',marginTop:6}}>
            M = {M_use.toExponential(3)} kg
          </p>
        </div>
      )}

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginBottom:16}}>
        <canvas ref={canvasRef} width={440} height={280}
          style={{width:'100%',height:'280px',borderRadius:'12px',background:'#05070a'}}/>

        <div style={{display:'flex',flexDirection:'column',gap:12}}>
          <div className="card">
            <p style={{color:'#64748b',fontSize:12,marginBottom:10,fontWeight:700}}>계산 결과</p>
            <div className="result-row">
              <span style={{color:'#94a3b8'}}>질량 (M)</span>
              <span className="val">{M_use.toExponential(3)} kg</span>
            </div>
            <div className="result-row">
              <span style={{color:'#94a3b8'}}>슈바르츠실트 반지름 (Rs)</span>
              <span className="val">{fmtNum(Rs)}</span>
            </div>
            {!isCustom && PRESETS_BH[sel].R_real > 0 && (
              <div className="result-row">
                <span style={{color:'#94a3b8'}}>실제 반지름</span>
                <span className="val" style={{color:'#60a5fa'}}>{fmtNum(PRESETS_BH[sel].R_real)}</span>
              </div>
            )}
            {!isCustom && PRESETS_BH[sel].R_real > 0 && (
              <div className="result-row">
                <span style={{color:'#94a3b8'}}>실제 / Rs 비율</span>
                <span className="val" style={{color: isBH_now?'#ef4444':'#22c55e'}}>
                  {(PRESETS_BH[sel].R_real / Rs).toExponential(2)}
                </span>
              </div>
            )}
          </div>

          <div className={`card`} style={{
            background: isBH_now ? 'linear-gradient(135deg,#1a0030,#2e0050)' : 'linear-gradient(135deg,#0a1f0a,#0f300f)',
            borderColor: isBH_now ? '#8b5cf6' : '#22c55e'
          }}>
            <p style={{color: isBH_now?'#c4b5fd':'#4ade80', fontWeight:800, fontSize:16, marginBottom:8}}>
              {isBH_now ? '🌑 블랙홀 상태' : '✅ 일반 천체 상태'}
            </p>
            <p style={{color: isBH_now?'#ddd6fe':'#86efac', fontSize:13, lineHeight:1.75}}>
              {isBH_now
                ? '실제 반지름이 슈바르츠실트 반지름보다 작거나 같습니다. 이 천체는 블랙홀입니다. 사건 지평선 내부로 들어간 물체는 탈출 불가능합니다.'
                : `실제 반지름이 Rs보다 ${(PRESETS_BH[sel].R_real/Rs).toExponential(2)}배 큽니다. 블랙홀이 되려면 이 천체를 ${fmtNum(Rs)}까지 압축해야 합니다.`}
            </p>
          </div>
        </div>
      </div>

      <div className="card">
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>주요 천체의 슈바르츠실트 반지름 비교</p>
        <div style={{overflowX:'auto'}}>
          <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
            <thead>
              <tr style={{borderBottom:'1px solid #1e293b'}}>
                {['천체','질량','실제 반지름','슈바르츠실트 반지름 Rs','상태'].map(h=>(
                  <th key={h} style={{padding:'10px 12px',color:'#64748b',fontWeight:700,textAlign:'left'}}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                ['🌍 지구',  '5.97×10²⁴ kg', '6,371 km', '8.9 mm',   false],
                ['☀️ 태양',  '1.99×10³⁰ kg', '696,000 km','3.0 km',  false],
                ['⚪ 백색왜성','1.4 M☉',       '~7,000 km', '4.1 km',  false],
                ['💫 중성자별','2.0 M☉',       '~12 km',    '5.9 km',  true ],
                ['🌑 M87*',  '6.5×10⁹ M☉',  '–',         '~192 AU', true ],
              ].map(([nm,m,r,rs,isBH],i)=>(
                <tr key={i} style={{borderBottom:'1px solid #0f172a',background:isBH?'rgba(139,92,246,0.08)':undefined}}>
                  <td style={{padding:'10px 12px',fontWeight:700,color:'#e2e8f0'}}>{nm}</td>
                  <td style={{padding:'10px 12px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:12}}>{m}</td>
                  <td style={{padding:'10px 12px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:12}}>{r}</td>
                  <td style={{padding:'10px 12px',color:'#a78bfa',fontWeight:800,fontFamily:'Space Mono'}}>{rs}</td>
                  <td style={{padding:'10px 12px'}}>
                    <span style={{
                      padding:'3px 10px',borderRadius:20,fontSize:11,fontWeight:700,
                      background: isBH?'rgba(139,92,246,0.2)':'rgba(34,197,94,0.15)',
                      color: isBH?'#c4b5fd':'#4ade80',
                      border: `1px solid ${isBH?'#8b5cf6':'#22c55e'}`
                    }}>
                      {isBH ? '블랙홀' : '일반 천체'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 3: 블랙홀 탐지 방법
────────────────────────────────────────────── */
const DETECT_METHODS = [
  {
    icon:'🌡️', title:'X선 쌍성계 (X-ray Binaries)',
    color:'#ef4444',
    summary:'블랙홀이 동반성의 물질을 강착 원반으로 흡수할 때 방출되는 X선을 관측',
    how:'동반 별에서 흘러나온 가스가 블랙홀 주변 강착 원반을 형성하며 수백만℃로 가열되어 강한 X선을 방출합니다.',
    example:'백조자리 X-1 (1964년 최초 발견), 궤도 운동으로 블랙홀 질량 추정 가능',
    evidence:'보이지 않는 동반체 + X선 + 궤도 운동 = 블랙홀'
  },
  {
    icon:'🌊', title:'중력파 (Gravitational Waves)',
    color:'#3b82f6',
    summary:'두 블랙홀이 합병할 때 시공간의 파동을 LIGO/Virgo 간섭계로 검출',
    how:'두 블랙홀이 나선운동하며 합쳐질 때 엄청난 에너지가 중력파로 방출됩니다. 이 파동이 지구를 통과하면 공간이 수소 원자 크기의 1/1000만큼 신축합니다.',
    example:'GW150914 (2015년): 36M☉ + 29M☉ → 62M☉ 블랙홀. 3M☉에 해당하는 에너지가 중력파로 방출.',
    evidence:'중력파 파형 분석으로 병합 전후 질량 정확 계산 가능'
  },
  {
    icon:'🔭', title:'중력 렌즈 (Gravitational Lensing)',
    color:'#8b5cf6',
    summary:'블랙홀의 강한 중력이 배경 별빛을 휘게 만드는 현상 관측',
    how:'블랙홀이 배경 별과 지구 사이를 통과할 때, 별빛이 블랙홀 중력에 의해 휘어 밝기가 증가합니다(미시 중력 렌즈). 초대질량 블랙홀은 퀘이사 상을 여러 개로 분리시킵니다.',
    example:'허블 망원경의 아인슈타인 링 관측, M87* 사건 지평선 망원경(EHT) 촬영',
    evidence:'아인슈타인 십자가, 링 등 특유의 광학 현상'
  },
  {
    icon:'⭐', title:'별의 궤도 운동 (Stellar Orbits)',
    color:'#fbbf24',
    summary:'초대질량 블랙홀 주변 별들의 궤도를 수십 년간 추적하여 블랙홀 질량과 위치 결정',
    how:'우리 은하 중심(궁수자리 A*) 주변 S2별을 16년간 추적한 결과, 보이지 않는 질량이 태양의 400만 배임을 확인. 이것이 블랙홀의 결정적 증거.',
    example:'S2별: 16.0년 주기, 근접점에서 빛의 2.87%의 속도. 2020년 노벨 물리학상.',
    evidence:'케플러 법칙으로 중심 질량 계산 → 블랙홀 확인'
  },
  {
    icon:'📡', title:'사건 지평선 망원경 (Event Horizon Telescope)',
    color:'#10b981',
    summary:'전 지구 규모의 전파망원경 네트워크로 블랙홀 그림자를 직접 촬영',
    how:'지구 크기의 가상 망원경(VLBI 기술)으로 M87 은하 중심의 초대질량 블랙홀을 촬영. 블랙홀 그림자(shadow)와 강착 원반의 고리 구조를 확인.',
    example:'2019년 M87* 블랙홀 최초 직접 촬영 (질량: 태양의 65억배). 2022년 우리 은하 중심 궁수자리 A* 촬영.',
    evidence:'빛 고리(Photon Ring)와 중앙의 어두운 그림자 = 사건 지평선의 직접 증거'
  },
];

function DetectTab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:18}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>📡 블랙홀을 발견하는 방법</p>
        <p style={{color:'#cbd5e1',fontSize:14,lineHeight:1.8}}>
          블랙홀은 빛을 방출하지 않으므로 <strong style={{color:'#a78bfa'}}>간접적인 방법</strong>으로만 탐지합니다.
          주변 물질과의 상호작용, 중력 효과, 시공간 왜곡이 증거가 됩니다.
        </p>
      </div>

      <div style={{display:'flex',flexDirection:'column',gap:12}}>
        {DETECT_METHODS.map((m,i)=>(
          <div key={i} className="detect-card"
            style={{borderColor:open===i?m.color+'80':'#1e293b',transition:'border-color 0.2s'}}>
            <div style={{display:'flex',gap:14,alignItems:'flex-start',cursor:'pointer'}}
              onClick={()=>setOpen(open===i?null:i)}>
              <div style={{width:46,height:46,borderRadius:12,background:`${m.color}22`,
                border:`1px solid ${m.color}44`,display:'flex',alignItems:'center',justifyContent:'center',
                fontSize:22,flexShrink:0}}>
                {m.icon}
              </div>
              <div style={{flex:1}}>
                <p style={{color:m.color,fontWeight:800,fontSize:15}}>{m.title}</p>
                <p style={{color:'#94a3b8',fontSize:13,marginTop:4,lineHeight:1.6}}>{m.summary}</p>
              </div>
              <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',marginTop:4,
                transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
            </div>
            <div style={{maxHeight:open===i?'400px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
              <div style={{marginTop:14,paddingTop:14,borderTop:'1px solid #1e293b',display:'flex',flexDirection:'column',gap:10}}>
                <div style={{display:'flex',gap:10}}>
                  <span style={{color:m.color,fontWeight:800,fontSize:12,flexShrink:0,paddingTop:2}}>원리</span>
                  <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.75}}>{m.how}</p>
                </div>
                <div style={{display:'flex',gap:10}}>
                  <span style={{color:'#fbbf24',fontWeight:800,fontSize:12,flexShrink:0,paddingTop:2}}>사례</span>
                  <p style={{color:'#fcd34d',fontSize:13,lineHeight:1.75}}>{m.example}</p>
                </div>
                <div style={{display:'flex',gap:10,background:`${m.color}11`,padding:'10px 14px',borderRadius:10,border:`1px solid ${m.color}33`}}>
                  <span style={{fontSize:14,flexShrink:0}}>🔑</span>
                  <p style={{color:m.color,fontSize:13,lineHeight:1.7,fontWeight:600}}>{m.evidence}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card" style={{marginTop:16,background:'linear-gradient(135deg,#0c1a0c,#0a2a0a)',borderColor:'#22c55e'}}>
        <p style={{color:'#4ade80',fontWeight:800,fontSize:14,marginBottom:10}}>💡 공통 원리</p>
        <p style={{color:'#86efac',fontSize:13,lineHeight:1.85}}>
          모든 탐지 방법은 <strong>블랙홀 주변의 물리적 효과</strong>를 관측합니다.
          블랙홀 자체는 보이지 않지만, 뉴턴의 중력 법칙과 일반 상대성 이론으로 예측한 현상들이
          정확히 관측되어 블랙홀의 존재를 증명합니다.
          2020년 노벨 물리학상은 우리 은하 중심 블랙홀 연구에 수여되었습니다.
        </p>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 4: 탐구 질문
────────────────────────────────────────────── */
const QA_BH = [
  { q:'블랙홀은 "모든 것을 빨아들인다"는 말이 맞을까?',
    a:'반은 맞고 반은 틀립니다. 사건 지평선 내부에서는 탈출이 불가능하지만, 사건 지평선 바깥에서는 블랙홀도 같은 질량의 별과 동일하게 중력을 작용합니다. 태양이 같은 질량의 블랙홀로 바뀌어도 지구 궤도는 변하지 않습니다. 블랙홀은 "가까이 가면 위험하지만" 멀리서는 평범한 중력체입니다.' },
  { q:'태양이 블랙홀이 될 수 있을까?',
    a:'아닙니다. 블랙홀이 되려면 초신성 폭발이 필요하고, 이를 위해서는 태양 질량의 약 8배 이상이 필요합니다. 태양은 약 50억 년 후 적색 거성을 거쳐 백색 왜성으로 생을 마감합니다. 태양을 블랙홀로 만들려면 반지름을 약 3 km로 압축해야 하는데, 자연적인 과정으로는 불가능합니다.' },
  { q:'블랙홀에서 나오는 정보는 없을까? (호킹 복사)',
    a:'스티븐 호킹은 1974년 양자 역학 효과로 블랙홀이 열복사를 방출한다고 예측했습니다(호킹 복사). 블랙홀 주변에서 가상 입자-반입자 쌍이 생성될 때, 한 입자가 사건 지평선 안으로 들어가고 다른 입자가 탈출하면 블랙홀은 질량을 잃습니다. 매우 작은 블랙홀은 빠르게 증발할 수 있지만, 거대 블랙홀의 호킹 온도는 우주 배경 복사보다도 낮아 현실적으로 측정이 불가능합니다.' },
  { q:'블랙홀 내부에 들어가면 어떻게 될까?',
    a:'멀리서 보면: 시간 팽창(중력 적색 편이) 때문에 진입자가 사건 지평선에 영원히 접근하는 것처럼 보이며 점점 흐릿해집니다. 진입자 입장: 질량이 크지 않은 블랙홀이라면 사건 지평선을 통과할 때 특별한 변화를 느끼지 못할 수 있습니다. 하지만 특이점에 가까워질수록 조석력(tidal force)이 극단적으로 커져 "스파게티화(spaghettification)"됩니다. 특이점에서는 현재의 물리 법칙이 적용되지 않습니다.' },
  { q:'우리 은하 중심에도 블랙홀이 있을까?',
    a:'네. 궁수자리 A*(Sgr A*)라는 초대질량 블랙홀이 있으며, 질량은 태양의 약 400만 배입니다. 지구에서 약 26,000광년 떨어져 있습니다. 2022년 사건 지평선 망원경(EHT)이 Sgr A*의 이미지를 직접 촬영했으며, 2020년 노벨 물리학상은 S2별 궤도 추적을 통한 Sgr A* 연구에 수여되었습니다.' },
];

function QATab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:18}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:4}}>❓ 탐구 질문</p>
        <p style={{color:'#94a3b8',fontSize:13}}>질문을 클릭하여 답변을 확인하세요. 먼저 스스로 생각해 보세요.</p>
      </div>
      <div style={{display:'flex',flexDirection:'column',gap:10}}>
        {QA_BH.map((item,i)=>(
          <div key={i} style={{borderRadius:13,border:`1px solid ${open===i?'#8b5cf6':'#1e293b'}`,
            overflow:'hidden',background:'#070b14',transition:'border-color 0.2s'}}>
            <button className="qa-btn" onClick={()=>setOpen(open===i?null:i)}>
              <span style={{color:'#8b5cf6',fontWeight:800,fontSize:15,flexShrink:0,marginTop:1}}>Q{i+1}.</span>
              <span style={{color:'#cbd5e1',fontSize:14,lineHeight:1.65,flex:1}}>{item.q}</span>
              <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',
                transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
            </button>
            <div style={{maxHeight:open===i?'350px':'0px',overflow:'hidden',transition:'max-height 0.35s ease'}}>
              <div style={{padding:'0 18px 14px 46px',display:'flex',gap:10}}>
                <span style={{color:'#10b981',fontWeight:800,fontSize:13,flexShrink:0,marginTop:1}}>A.</span>
                <span style={{color:'#6ee7b7',fontSize:13,lineHeight:1.85}}>{item.a}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card" style={{marginTop:16,background:'linear-gradient(135deg,#0f172a,#1a1040)',borderColor:'#8b5cf6'}}>
        <p style={{color:'#c4b5fd',fontWeight:800,marginBottom:10}}>🌌 연결 개념</p>
        <p style={{color:'#a78bfa',fontSize:13,lineHeight:1.9}}>
          블랙홀 탐구는 뉴턴의 중력 법칙 → 탈출속도 → 슈바르츠실트 반지름 → 아인슈타인의 일반 상대성 이론으로 이어지는 개념의 연결입니다.
          고전 역학으로 예측한 "빛도 탈출 못하는 천체"가 실제로 관측으로 확인되었다는 것은
          물리학의 예측력과 아름다움을 보여주는 대표적 사례입니다.
        </p>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   메인 앱
────────────────────────────────────────────── */
const TABS = [
  { id:'concept',  label:'🌑 블랙홀이란?' },
  { id:'calc',     label:'🔭 슈바르츠실트 계산기' },
  { id:'detect',   label:'📡 블랙홀 탐지' },
  { id:'qa',       label:'❓ 탐구 질문' },
];

const App = () => {
  const [tab, setTab] = useState('concept');
  return (
    <div style={{maxWidth:1100,margin:'0 auto'}}>
      <div style={{background:'linear-gradient(135deg,#0f0520,#1a0a3e)',borderRadius:16,padding:'20px 24px',
        marginBottom:20,border:'1px solid #5b21b6'}}>
        <h2 style={{color:'#c4b5fd',margin:0,fontSize:'1.4rem'}}>🌑 학습주제 6-2: 블랙홀 탐구</h2>
        <p style={{color:'#94a3b8',margin:'8px 0 0',fontSize:'0.95rem'}}>
          <strong style={{color:'#fbbf24'}}>핵심 질문:</strong> 탈출속도가 빛의 속도보다 큰 천체가 존재할 수 있을까? 그 천체를 어떻게 발견할 수 있을까?
        </p>
      </div>
      <div className="tab-bar">
        {TABS.map(t=>(
          <button key={t.id} className={`tab-btn ${tab===t.id?'active':''}`}
            onClick={()=>setTab(t.id)}>{t.label}</button>
        ))}
      </div>
      {tab==='concept' && <ConceptTab/>}
      {tab==='calc'    && <SchwarzschildTab/>}
      {tab==='detect'  && <DetectTab/>}
      {tab==='qa'      && <QATab/>}
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""

REACT_HTML_FINAL = REACT_HTML.replace("__BH_IMG_B64__", _img_b64)
components.html(REACT_HTML_FINAL, height=1500, scrolling=True)
