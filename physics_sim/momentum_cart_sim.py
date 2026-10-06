import streamlit as st
import streamlit.components.v1 as components
import json

st.sidebar.title("🛒 운동량 보존 법칙 실험")
st.sidebar.markdown("""
2022 개정 교육과정 역학과 에너지 [12역학01-02] 성취기준 연계
디지털 MBL 무선 수레와 용수철 분리 실험을 통해 운동량 보존 법칙을 정량적으로 탐구하고, 
발사체(우주 로켓)의 추진 원리를 분석합니다.
""")

REACT_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#090d16;color:#e2e8f0;padding:16px;}
.tab-bar{display:flex;gap:8px;margin-bottom:18px;flex-wrap:wrap;}
.tab-btn{padding:10px 18px;border-radius:10px;border:1px solid #1e293b;background:#0f172a;
  color:#94a3b8;cursor:pointer;font-size:13.5px;font-weight:700;font-family:inherit;transition:all 0.2s;}
.tab-btn.active{background:#2563eb;border-color:#3b82f6;color:#fff;box-shadow:0 0 14px rgba(37,99,235,0.4);}
.tab-btn:hover:not(.active){border-color:#475569;color:#e2e8f0;}
.card{background:#0d1526;border:1px solid #1e293b;border-radius:14px;padding:18px;margin-bottom:14px;}
.hl-box{background:linear-gradient(135deg,#0c1a3a,#0f2050);border:1px solid #1d4ed8;border-radius:12px;padding:16px;margin-bottom:14px;}
.btn-primary{background:#2563eb;color:#fff;border:none;border-radius:10px;padding:10px 18px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.2s;}
.btn-primary:hover{background:#1d4ed8;}
.btn-success{background:#16a34a;color:#fff;border:none;border-radius:10px;padding:10px 18px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.2s;}
.btn-success:hover{background:#15803d;}
.btn-danger{background:#dc2626;color:#fff;border:none;border-radius:10px;padding:10px 18px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.2s;}
.btn-danger:hover{background:#b91c1c;}
.btn-secondary{background:#1e293b;color:#cbd5e1;border:1px solid #334155;border-radius:10px;padding:8px 14px;font-size:12.5px;font-weight:600;cursor:pointer;transition:all 0.2s;}
.btn-secondary:hover{background:#334155;color:#fff;}
.badge{display:inline-block;padding:3px 8px;border-radius:6px;font-size:11px;font-weight:700;}
.badge-lime{background:rgba(132,204,22,0.15);color:#a3e635;border:1px solid rgba(132,204,22,0.4);}
.badge-blue{background:rgba(14,165,233,0.15);color:#38bdf8;border:1px solid rgba(14,165,233,0.4);}
.badge-purple{background:rgba(168,85,247,0.15);color:#c084fc;border:1px solid rgba(168,85,247,0.4);}
.badge-amber{background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.4);}
.table-custom{width:100%;border-collapse:collapse;font-size:12.5px;}
.table-custom th{background:#0a101f;color:#94a3b8;padding:8px 10px;border:1px solid #1e293b;text-align:center;font-weight:700;}
.table-custom td{padding:8px 10px;border:1px solid #1e293b;text-align:center;}
.num-mono{font-family:'Space Mono',monospace;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

/* KaTeX 수식 컴포넌트 */
const Eq = ({ f, display=false, color='#93c5fd' }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && window.katex)
      window.katex.render(f, ref.current, { throwOnError:false, displayMode:display });
  }, [f, display]);
  return <span ref={ref} style={{ color }} />;
};

/* ══════════════════════════════════════════════════
   메인 애플리케이션 컴포넌트
══════════════════════════════════════════════════ */
function App() {
  const [activeTab, setActiveTab] = useState('sim'); // sim | rocket | rocket2 | report

  return (
    <div>
      {/* 탭 네비게이션 */}
      <div className="tab-bar">
        <button className={`tab-btn ${activeTab==='sim'?'active':''}`} onClick={()=>setActiveTab('sim')}>
          🛒 [디지털 해보기] MBL 무선 수레 실험
        </button>
        <button className={`tab-btn ${activeTab==='rocket'?'active':''}`} onClick={()=>setActiveTab('rocket')}>
          🚀 [원리 탐구 1] 그림 I-23 정지계 발사체 추진
        </button>
        <button className={`tab-btn ${activeTab==='rocket2'?'active':''}`} onClick={()=>setActiveTab('rocket2')}>
          🌌 [원리 탐구 2] 그림 I-24 질량감소 & 속도증가
        </button>
        <button className={`tab-btn ${activeTab==='report'?'active':''}`} onClick={()=>setActiveTab('report')}>
          📝 [탐구 보고서] 실험 데이터 & 문제 풀이
        </button>
      </div>

      {activeTab === 'sim' && <CartSimTab />}
      {activeTab === 'rocket' && <RocketPrincipleTab />}
      {activeTab === 'rocket2' && <RocketMotionPrincipleTab />}
      {activeTab === 'report' && <ReportTab />}
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 1: MBL 무선 수레 가상 실험실
══════════════════════════════════════════════════ */
function CartSimTab() {
  /* 수레 A (좌측) 설정: 기본 0.50kg + 추가 추 (개당 0.25kg) */
  const [weightsA, setWeightsA] = useState(0); // 0개 (빈 수레 0.50 kg)
  /* 수레 B (우측) 설정: 기본 0.50kg + 추가 추 (개당 0.25kg, 교과서 기본: 2개 = 1.00 kg) */
  const [weightsB, setWeightsB] = useState(2); // 2개 (추 올린 수레 1.00 kg)
  
  /* 용수철 압축 강도: 1(약 0.20J), 2(중 0.45J), 3(강 0.80J) */
  const [springStrength, setSpringStrength] = useState(2);
  
  /* 물리 벡터 표시 옵션 */
  const [showForceVec, setShowForceVec] = useState(true);
  const [showVelVec, setShowVelVec] = useState(true);
  const [showMomVec, setShowMomVec] = useState(true);

  /* 질량 계산 */
  const massA = 0.50 + weightsA * 0.25; // kg
  const massB = 0.50 + weightsB * 0.25; // kg
  
  /* 용수철 탄성 에너지 (J) */
  const springEnergies = { 1: 0.22, 2: 0.48, 3: 0.85 };
  const Espring = springEnergies[springStrength];

  /* 이론 분리 속도 계산 (운동량 보존 & 에너지 보존)
     mA*vA = mB*vB  =>  vA = (mB/mA)*vB
     E = 0.5*mA*vA^2 + 0.5*mB*vB^2 = 0.5*mB*vB^2 * (1 + mB/mA)
     => vB = sqrt( 2*E / (mB * (1 + mB/mA)) )
  */
  const vB_theory = Math.sqrt((2 * Espring) / (massB * (1 + massB / massA)));
  const vA_theory = (massB / massA) * vB_theory;

  /* 이론 운동량 (kg·m/s) */
  const pA_theory = -massA * vA_theory; // 음의 방향 (왼쪽)
  const pB_theory = +massB * vB_theory; // 양의 방향 (오른쪽)

  /* 시뮬레이션 상태 */
  const [simState, setSimState] = useState('ready'); // ready(압축대기) | compressed(장전됨) | running(분리운동) | stopped(정지)
  const [measData, setMeasData] = useState(null); // 분리 후 측정된 실제 센서값
  const [logList, setLogList] = useState([
    { id: 1, nameA: '빈 수레 (추 0개)', mA: 0.50, vA: -0.98, pA: -0.490, nameB: '추 2개 올린 수레', mB: 1.00, vB: 0.49, pB: 0.490, pTot: 0.000 },
    { id: 2, nameA: '빈 수레 (추 0개)', mA: 0.50, vA: -0.69, pA: -0.345, nameB: '빈 수레 (추 0개)', mB: 0.50, vB: 0.69, pB: 0.345, pTot: 0.000 }
  ]);

  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const simRef = useRef({
    xA: 330, xB: 430, // 수레 중심 X 좌표 (px)
    vA: 0, vB: 0,
    springW: 30, // 용수철 길이
    t: 0,
    trailA: [], trailB: [],
    pushProgress: 0 // 용수철 팽창 진행도 (0~1)
  });

  /* 시뮬레이션 리셋 / 장전 */
  const armSpring = () => {
    cancelAnimationFrame(animRef.current);
    simRef.current = {
      xA: 370, xB: 410, // 맞닿은 위치
      vA: 0, vB: 0,
      springW: 10,
      t: 0,
      trailA: [], trailB: [],
      pushProgress: 0
    };
    setSimState('compressed');
    setMeasData(null);
    drawScene(370, 410, 0, 0, 0, true);
  };

  /* 초기화 (트랙 상 적당한 대기 위치) */
  const resetToReady = () => {
    cancelAnimationFrame(animRef.current);
    simRef.current = {
      xA: 310, xB: 470,
      vA: 0, vB: 0,
      springW: 28,
      t: 0,
      trailA: [], trailB: [],
      pushProgress: 0
    };
    setSimState('ready');
    setMeasData(null);
    drawScene(310, 470, 0, 0, 0, false);
  };

  /* 🚀 분리 버튼 클릭 (데이터 수집 시작 및 릴리즈) */
  const triggerRelease = () => {
    if (simState !== 'compressed') {
      armSpring();
    }
    setSimState('running');
    
    // 센서 데이터 확정 (약간의 현실적인 마이크로 노이즈 0.5% 반영)
    const noise = 1.0; 
    const vA_meas = -(vA_theory * noise);
    const vB_meas = +(vB_theory * noise);
    const pA_meas = +(massA * vA_meas).toFixed(3);
    const pB_meas = +(massB * vB_meas).toFixed(3);
    const pTot_meas = +(pA_meas + pB_meas).toFixed(3);

    setMeasData({
      mA: massA,
      mB: massB,
      vA: +vA_meas.toFixed(3),
      vB: +vB_meas.toFixed(3),
      pA: pA_meas,
      pB: pB_meas,
      pTot: pTot_meas
    });

    let startTime = null;
    const TRACK_MIN_X = 65;  // 왼쪽 범퍼 위치
    const TRACK_MAX_X = 735; // 오른쪽 범퍼 위치
    const PIXEL_SCALE = 180; // 1 m = 180 px

    const stepAnim = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const elapsed = (timestamp - startTime) / 1000; // 초
      
      const s = simRef.current;
      s.t = elapsed;

      // 0.06초 동안 용수철 팽창 가속, 이후 등속 운동
      const PUSH_DUR = 0.08;
      if (elapsed <= PUSH_DUR) {
        const prog = elapsed / PUSH_DUR;
        s.pushProgress = prog;
        s.vA = -vA_theory * prog;
        s.vB = +vB_theory * prog;
        s.xA = 370 + (s.vA * PIXEL_SCALE * elapsed * 0.5);
        s.xB = 410 + (s.vB * PIXEL_SCALE * elapsed * 0.5);
      } else {
        s.pushProgress = 1;
        s.vA = -vA_theory;
        s.vB = +vB_theory;
        const dtMove = elapsed - PUSH_DUR;
        s.xA = 370 - (vA_theory * PIXEL_SCALE * (PUSH_DUR * 0.5 + dtMove));
        s.xB = 410 + (vB_theory * PIXEL_SCALE * (PUSH_DUR * 0.5 + dtMove));
      }

      // 궤적 기록
      if (s.trailA.length < 180) {
        s.trailA.push({ x: s.xA, t: elapsed, v: s.vA });
        s.trailB.push({ x: s.xB, t: elapsed, v: s.vB });
      }

      // 범퍼 충돌 검사
      let hit = false;
      if (s.xA <= TRACK_MIN_X + 40) {
        s.xA = TRACK_MIN_X + 40;
        hit = true;
      }
      if (s.xB >= TRACK_MAX_X - 40) {
        s.xB = TRACK_MAX_X - 40;
        hit = true;
      }

      drawScene(s.xA, s.xB, s.vA, s.vB, s.pushProgress, false);

      if (hit || elapsed > 3.0) {
        setSimState('stopped');
        return;
      }

      animRef.current = requestAnimationFrame(stepAnim);
    };

    animRef.current = requestAnimationFrame(stepAnim);
  };

  /* 캔버스 그리기 함수 */
  const drawScene = (xA, xB, curVA, curVB, pushProg, isComp) => {
    const cvs = canvasRef.current;
    if (!cvs) return;
    const ctx = cvs.getContext('2d');
    const W = cvs.width, H = cvs.height;

    // 배경 클리어
    ctx.fillStyle = '#080d1a';
    ctx.fillRect(0, 0, W, H);

    // 상단 실험실 조명 가이드
    const gradLight = ctx.createLinearGradient(0, 0, 0, 80);
    gradLight.addColorStop(0, 'rgba(30,58,138,0.25)');
    gradLight.addColorStop(1, 'rgba(8,13,26,0)');
    ctx.fillStyle = gradLight;
    ctx.fillRect(0, 0, W, 80);

    /* ── 1. 다이내믹스 트랙 (알루미늄 레일) ── */
    const trackY = 175;
    const trackX1 = 40, trackX2 = 760;

    // 레일 다리 (수평 지지대)
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(trackX1 + 30, trackY + 22, 14, 25);
    ctx.fillRect(trackX2 - 44, trackY + 22, 14, 25);
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(trackX1 + 22, trackY + 44, 30, 6);
    ctx.fillRect(trackX2 - 52, trackY + 44, 30, 6);

    // 알루미늄 레일 바디
    const railG = ctx.createLinearGradient(0, trackY, 0, trackY + 22);
    railG.addColorStop(0, '#64748b');
    railG.addColorStop(0.3, '#94a3b8');
    railG.addColorStop(0.7, '#475569');
    railG.addColorStop(1, '#1e293b');
    ctx.fillStyle = railG;
    ctx.fillRect(trackX1, trackY, trackX2 - trackX1, 22);
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(trackX1, trackY, trackX2 - trackX1, 22);

    // 양쪽 끝 범퍼 (충격 흡수대)
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(trackX1 - 8, trackY - 14, 12, 36);
    ctx.fillRect(trackX2 - 4, trackY - 14, 12, 36);
    ctx.fillStyle = '#dc2626';
    ctx.fillRect(trackX1 + 4, trackY - 8, 5, 20);
    ctx.fillRect(trackX2 - 9, trackY - 8, 5, 20);

    // 레일 눈금자 (밀리미터 각인)
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 0.8;
    for (let cm = 0; cm <= 120; cm += 2) {
      const rx = trackX1 + 10 + (cm / 120) * (trackX2 - trackX1 - 20);
      const tickH = (cm % 10 === 0) ? 7 : (cm % 5 === 0 ? 5 : 3);
      ctx.beginPath();
      ctx.moveTo(rx, trackY + 2);
      ctx.lineTo(rx, trackY + 2 + tickH);
      ctx.stroke();
      if (cm % 20 === 0) {
        ctx.fillStyle = '#e2e8f0';
        ctx.font = '8px Space Mono';
        ctx.textAlign = 'center';
        ctx.fillText(`${cm}`, rx, trackY + 16);
      }
    }

    // 중앙 원점 표시 (60 cm)
    const midTrackX = trackX1 + 10 + 0.5 * (trackX2 - trackX1 - 20);
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(midTrackX, trackY - 4);
    ctx.lineTo(midTrackX, trackY + 22);
    ctx.stroke();
    ctx.fillStyle = '#fbbf24';
    ctx.font = 'bold 9px Space Mono';
    ctx.fillText('중앙(원점)', midTrackX, trackY + 34);

    /* ── 2. 용수철 플런저 (중앙 또는 수레 사이) ── */
    const cartW = 82, cartH = 34;
    const cartAy = trackY - cartH - 4;
    const cartBy = trackY - cartH - 4;

    const springLeft = xA + cartW/2;
    const springRight = xB - cartW/2;
    const currentSpringLen = Math.max(2, springRight - springLeft);

    if (currentSpringLen < 60) {
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      const coils = 6;
      ctx.moveTo(springLeft, cartAy + cartH/2);
      for (let c = 1; c <= coils; c++) {
        const cx = springLeft + (currentSpringLen / (coils + 1)) * c;
        const cy = cartAy + cartH/2 + (c % 2 === 1 ? -7 : 7);
        ctx.lineTo(cx, cy);
      }
      ctx.lineTo(springRight, cartBy + cartH/2);
      ctx.stroke();
    }

    /* ── 3. 수레 A 그리기 (라임/녹색 MBL 스마트카트) ── */
    drawCartBody(ctx, xA, cartAy, cartW, cartH, '#65a30d', '#84cc16', '#a3e635', '수레 A (빈 수레)', weightsA, '#ecfccb');

    /* ── 4. 수레 B 그리기 (스카이블루 MBL 스마트카트) ── */
    drawCartBody(ctx, xB, cartBy, cartW, cartH, '#0284c7', '#0ea5e9', '#38bdf8', '수레 B (추 올린 수레)', weightsB, '#e0f2fe');

    /* ── 5. 물리 벡터 화살표 오버레이 ── */
    // (1) 작용-반작용 힘 벡터 (분리 순간 pushProgress < 0.95 시 표시)
    if (showForceVec && pushProg > 0 && pushProg < 0.95) {
      const forceMag = (Math.abs(pA_theory) / 0.08) * 1.5; // 화살표 스케일
      // FAB (A가 B를 오른쪽으로 미는 힘)
      drawArrow(ctx, xB - cartW/2, cartBy + 12, xB - cartW/2 + forceMag, cartBy + 12, '#f97316', 'F_AB (작용)');
      // FBA (B가 A를 왼쪽으로 미는 힘)
      drawArrow(ctx, xA + cartW/2, cartAy + 12, xA + cartW/2 - forceMag, cartAy + 12, '#f97316', 'F_BA (반작용)');
    }

    // (2) 속도 벡터
    if (showVelVec && (Math.abs(curVA) > 0.02 || Math.abs(curVB) > 0.02)) {
      const vScale = 65;
      drawArrow(ctx, xA, cartAy - 10, xA + curVA * vScale, cartAy - 10, '#22c55e', `v_A = ${curVA.toFixed(2)} m/s`);
      drawArrow(ctx, xB, cartBy - 10, xB + curVB * vScale, cartBy - 10, '#06b6d4', `v_B = ${curVB.toFixed(2)} m/s`);
    }

    // (3) 운동량 벡터
    if (showMomVec && (Math.abs(curVA) > 0.02 || Math.abs(curVB) > 0.02)) {
      const momScale = 120;
      const curPA = massA * curVA;
      const curPB = massB * curVB;
      drawArrow(ctx, xA, cartAy - 26, xA + curPA * momScale, cartAy - 26, '#a855f7', `p_A = ${curPA.toFixed(2)}`);
      drawArrow(ctx, xB, cartBy - 26, xB + curPB * momScale, cartBy - 26, '#a855f7', `p_B = +${curPB.toFixed(2)}`);
    }
  };

  /* 수레 본체 렌더링 함수 */
  const drawCartBody = (ctx, cx, cy, w, h, colDark, colMain, colLight, label, numWeights, textColor) => {
    const rx = cx - w/2;
    
    // 그림자
    ctx.fillStyle = 'rgba(0,0,0,0.35)';
    ctx.beginPath();
    ctx.roundRect(rx - 2, cy + h + 2, w + 4, 4, 3);
    ctx.fill();

    // 바퀴 (2개)
    ctx.fillStyle = '#0f172a';
    ctx.beginPath(); ctx.arc(rx + 16, cy + h + 2, 6.5, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(rx + w - 16, cy + h + 2, 6.5, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = '#94a3b8';
    ctx.beginPath(); ctx.arc(rx + 16, cy + h + 2, 2.5, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(rx + w - 16, cy + h + 2, 2.5, 0, Math.PI*2); ctx.fill();

    // 수레 본체 그라데이션
    const bgCart = ctx.createLinearGradient(rx, cy, rx, cy + h);
    bgCart.addColorStop(0, colLight);
    bgCart.addColorStop(0.4, colMain);
    bgCart.addColorStop(1, colDark);
    ctx.fillStyle = bgCart;
    ctx.beginPath();
    ctx.roundRect(rx, cy, w, h, 6);
    ctx.fill();
    ctx.strokeStyle = colDark;
    ctx.lineWidth = 1.2;
    ctx.stroke();

    // 스마트카트 내부 센서 창 / 데칼
    ctx.fillStyle = 'rgba(15,23,42,0.6)';
    ctx.beginPath();
    ctx.roundRect(rx + 8, cy + 6, w - 16, 12, 4);
    ctx.fill();

    // 블루투스 MBL LED
    ctx.fillStyle = '#38bdf8';
    ctx.beginPath();
    ctx.arc(rx + 14, cy + 12, 2.5, 0, Math.PI*2);
    ctx.fill();

    // 수레 질량 라벨
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 9px Space Mono';
    ctx.textAlign = 'center';
    const totalM = (0.50 + numWeights * 0.25).toFixed(2);
    ctx.fillText(`${totalM} kg`, cx + 6, cy + 15);

    // 수레 상단에 적재된 추 블록 그리기
    for (let i = 0; i < numWeights; i++) {
      const weightW = 28;
      const weightH = 9;
      const wy = cy - (i + 1) * (weightH + 1);
      const wx = cx - weightW / 2;

      const gradW = ctx.createLinearGradient(wx, wy, wx, wy + weightH);
      gradW.addColorStop(0, '#f1f5f9');
      gradW.addColorStop(0.5, '#cbd5e1');
      gradW.addColorStop(1, '#64748b');
      ctx.fillStyle = gradW;
      ctx.beginPath();
      ctx.roundRect(wx, wy, weightW, weightH, 2);
      ctx.fill();
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 0.8;
      ctx.stroke();

      ctx.fillStyle = '#0f172a';
      ctx.font = '7.5px Space Mono';
      ctx.fillText('+250g', cx, wy + 7);
    }

    // 하단 수레 설명 텍스트
    ctx.fillStyle = textColor;
    ctx.font = 'bold 10px Noto Sans KR';
    ctx.textAlign = 'center';
    ctx.fillText(label, cx, cy + h + 22);
  };

  /* 화살표 벡터 그리기 헬퍼 */
  const drawArrow = (ctx, fromX, fromY, toX, toY, color, labelText) => {
    if (Math.abs(toX - fromX) < 3) return;
    const headLen = 7;
    const dx = toX - fromX;
    const dy = toY - fromY;
    const angle = Math.atan2(dy, dx);

    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2.5;

    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(toX, toY);
    ctx.lineTo(toX - headLen * Math.cos(angle - Math.PI / 6), toY - headLen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(toX - headLen * Math.cos(angle + Math.PI / 6), toY - headLen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fill();

    if (labelText) {
      ctx.font = 'bold 9px Space Mono';
      ctx.textAlign = 'center';
      ctx.fillText(labelText, (fromX + toX) / 2, fromY - 5);
    }
  };

  /* 초기 렌더링 */
  useEffect(() => {
    resetToReady();
  }, [massA, massB, springStrength]);

  /* 현재 데이터 기록 */
  const logCurrentData = () => {
    if (!measData) return;
    const newEntry = {
      id: logList.length + 1,
      nameA: `수레 A (추 ${weightsA}개)`,
      mA: measData.mA,
      vA: measData.vA,
      pA: measData.pA,
      nameB: `수레 B (추 ${weightsB}개)`,
      mB: measData.mB,
      vB: measData.vB,
      pB: measData.pB,
      pTot: measData.pTot
    };
    setLogList([newEntry, ...logList]);
  };

  /* 교과서 표준 실험 데이터 세트 불러오기 */
  const loadTextbookPreset = () => {
    setLogList([
      { id: 1, nameA: '빈 수레 (추 0개)', mA: 0.50, vA: -0.98, pA: -0.490, nameB: '추 2개 올린 수레', mB: 1.00, vB: 0.49, pB: 0.490, pTot: 0.000 },
      { id: 2, nameA: '빈 수레 (추 0개)', mA: 0.50, vA: -0.70, pA: -0.350, nameB: '빈 수레 (추 0개)', mB: 0.50, vB: 0.70, pB: 0.350, pTot: 0.000 },
      { id: 3, nameA: '빈 수레 (추 0개)', mA: 0.50, vA: -1.20, pA: -0.600, nameB: '추 4개 올린 수레', mB: 1.50, vB: 0.40, pB: 0.600, pTot: 0.000 },
      { id: 4, nameA: '추 1개 올린 수레', mA: 0.75, vA: -0.80, pA: -0.600, nameB: '추 2개 올린 수레', mB: 1.00, vB: 0.60, pB: 0.600, pTot: 0.000 }
    ]);
  };

  return (
    <div>
      {/* ── 탐구 개요 카드 ── */}
      <div className="card">
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',flexWrap:'wrap',gap:12}}>
          <div>
            <div style={{display:'flex',gap:8,alignItems:'center',marginBottom:6}}>
              <span className="badge badge-lime">교과서 탐구 활동</span>
              <span className="badge badge-blue">디지털 해보기</span>
              <span style={{fontSize:16,fontWeight:800,color:'#f8fafc'}}>발사체에 적용된 운동량 보존 원리 알아보기</span>
            </div>
            <p style={{fontSize:13,color:'#94a3b8',lineHeight:1.6}}>
              한 수레에만 추를 2개 올리고, 압축된 용수철을 분리하여 두 수레의 속도와 운동량을 디지털 MBL 센서로 측정합니다.<br/>
              외력이 작용하지 않는 계에서 <b>m·v + M·V = 0</b> 관계가 성립함을 실험 데이터로 정량 검증합니다.
            </p>
          </div>
          <div style={{display:'flex',gap:6}}>
            <button className="btn-secondary" onClick={loadTextbookPreset}>
              📚 교과서 표준 데이터 세트 불러오기
            </button>
          </div>
        </div>
      </div>

      {/* ── 실험 파라미터 조작부 ── */}
      <div className="card" style={{background:'#0c1424',borderColor:'#1e3a8a'}}>
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(220px, 1fr))',gap:16}}>
          
          {/* 수레 A (좌측) */}
          <div style={{background:'rgba(101,163,13,0.08)',padding:12,borderRadius:10,border:'1px solid rgba(132,204,22,0.3)'}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:6}}>
              <span style={{fontSize:13,fontWeight:700,color:'#a3e635'}}>🛒 수레 A (좌측)</span>
              <span className="num-mono" style={{fontWeight:800,color:'#ecfccb',fontSize:14}}>{massA.toFixed(2)} kg</span>
            </div>
            <p style={{fontSize:11.5,color:'#94a3b8',marginBottom:8}}>빈 수레 0.50kg + 추가 추 ({weightsA}개)</p>
            <div style={{display:'flex',gap:4}}>
              {[0, 1, 2, 3].map(w => (
                <button key={w} 
                  className={`btn-secondary`}
                  style={{flex:1,padding:'5px 0',fontSize:11,background:weightsA===w?'#65a30d':undefined,color:weightsA===w?'#fff':undefined}}
                  onClick={()=>setWeightsA(w)}>
                  추 {w}개
                </button>
              ))}
            </div>
          </div>

          {/* 수레 B (우측, 교과서: 추 2개 올림) */}
          <div style={{background:'rgba(2,132,199,0.08)',padding:12,borderRadius:10,border:'1px solid rgba(14,165,233,0.3)'}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:6}}>
              <span style={{fontSize:13,fontWeight:700,color:'#38bdf8'}}>🛒 수레 B (우측)</span>
              <span className="num-mono" style={{fontWeight:800,color:'#e0f2fe',fontSize:14}}>{massB.toFixed(2)} kg</span>
            </div>
            <p style={{fontSize:11.5,color:'#94a3b8',marginBottom:8}}>빈 수레 0.50kg + 추가 추 ({weightsB}개)</p>
            <div style={{display:'flex',gap:4}}>
              {[0, 1, 2, 3].map(w => (
                <button key={w} 
                  className={`btn-secondary`}
                  style={{flex:1,padding:'5px 0',fontSize:11,background:weightsB===w?'#0284c7':undefined,color:weightsB===w?'#fff':undefined}}
                  onClick={()=>setWeightsB(w)}>
                  추 {w}개
                </button>
              ))}
            </div>
          </div>

          {/* 용수철 압축 강도 */}
          <div style={{background:'rgba(245,158,11,0.08)',padding:12,borderRadius:10,border:'1px solid rgba(245,158,11,0.3)'}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:6}}>
              <span style={{fontSize:13,fontWeight:700,color:'#fbbf24'}}>⚡ 용수철 플런저 압축 강도</span>
              <span className="num-mono" style={{fontWeight:700,color:'#fef3c7',fontSize:12.5}}>{Espring.toFixed(2)} J</span>
            </div>
            <p style={{fontSize:11.5,color:'#94a3b8',marginBottom:8}}>압축 핀을 누르는 단계 설정</p>
            <div style={{display:'flex',gap:4}}>
              {[1, 2, 3].map(s => (
                <button key={s} 
                  className={`btn-secondary`}
                  style={{flex:1,padding:'5px 0',fontSize:11,background:springStrength===s?'#d97706':undefined,color:springStrength===s?'#fff':undefined}}
                  onClick={()=>setSpringStrength(s)}>
                  {s}단계 {s===1?'(약)':s===2?'(중)':'(강)'}
                </button>
              ))}
            </div>
          </div>

          {/* 벡터 시각화 토글 */}
          <div style={{background:'rgba(148,163,184,0.06)',padding:12,borderRadius:10,border:'1px solid #334155'}}>
            <span style={{fontSize:12.5,fontWeight:700,color:'#cbd5e1',display:'block',marginBottom:8}}>👁️ 물리 벡터 표시</span>
            <div style={{display:'flex',gap:6,flexWrap:'wrap'}}>
              <label style={{fontSize:11,display:'flex',alignItems:'center',gap:4,cursor:'pointer',color:'#f97316'}}>
                <input type="checkbox" checked={showForceVec} onChange={e=>setShowForceVec(e.target.checked)}/> 작용·반작용력(F)
              </label>
              <label style={{fontSize:11,display:'flex',alignItems:'center',gap:4,cursor:'pointer',color:'#22c55e'}}>
                <input type="checkbox" checked={showVelVec} onChange={e=>setShowVelVec(e.target.checked)}/> 속도(v)
              </label>
              <label style={{fontSize:11,display:'flex',alignItems:'center',gap:4,cursor:'pointer',color:'#c084fc'}}>
                <input type="checkbox" checked={showMomVec} onChange={e=>setShowMomVec(e.target.checked)}/> 운동량(p)
              </label>
            </div>
          </div>

        </div>
      </div>

      {/* ── 캔버스 시뮬레이터 ── */}
      <div className="card" style={{padding:12,position:'relative'}}>
        <canvas ref={canvasRef} width={800} height={250} 
          style={{width:'100%',height:'250px',background:'#070c18',borderRadius:10,display:'block'}}/>
        
        {/* 컨트롤 오버레이 버튼 바 */}
        <div style={{display:'flex',justifyContent:'center',gap:12,marginTop:12,flexWrap:'wrap'}}>
          <button className="btn-secondary" onClick={armSpring} disabled={simState==='running'}>
            🔒 1. 용수철 압축 장전
          </button>
          <button className="btn-success" onClick={triggerRelease} disabled={simState==='running'}
            style={{padding:'10px 24px',fontSize:14,boxShadow:'0 0 15px rgba(22,163,74,0.4)'}}>
            🚀 2. 분리 단추 누르기 (MBL 데이터 수집)
          </button>
          <button className="btn-secondary" onClick={resetToReady}>
            ↺ 3. 트랙 정렬 (초기화)
          </button>
          {measData && (
            <button className="btn-primary" onClick={logCurrentData}>
              📋 현재 실험 데이터 표에 추가
            </button>
          )}
        </div>
      </div>

      {/* ── 디지털 MBL 스마트 태블릿 실시간 계측 화면 ── */}
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(350px, 1fr))',gap:14,marginBottom:14}}>
        
        {/* 좌측: 실시간 계측 HUD */}
        <div className="card" style={{border:'1px solid #1e3a8a',background:'linear-gradient(145deg,#0a1329,#090e1c)'}}>
          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:12,borderBottom:'1px solid #1e293b',paddingBottom:8}}>
            <div style={{display:'flex',alignItems:'center',gap:8}}>
              <span style={{width:8,height:8,borderRadius:'50%',background:'#22c55e',display:'inline-block'}}></span>
              <span style={{fontWeight:800,color:'#60a5fa',fontSize:13.5}}>📱 디지털 MBL 애플리케이션 실시간 센서값</span>
            </div>
            <span className="badge badge-blue">무선 블루투스 연결됨</span>
          </div>

          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12}}>
            
            {/* 수레 A 센서 데이터 */}
            <div style={{background:'rgba(101,163,13,0.1)',padding:10,borderRadius:8,border:'1px solid rgba(132,204,22,0.3)'}}>
              <p style={{fontSize:11.5,fontWeight:700,color:'#a3e635',marginBottom:6}}>수레 A (좌측 / 빈 수레)</p>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:12,marginBottom:4}}>
                <span style={{color:'#94a3b8'}}>질량 (m_A):</span>
                <span className="num-mono" style={{fontWeight:700,color:'#ecfccb'}}>{massA.toFixed(2)} kg</span>
              </div>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:12,marginBottom:4}}>
                <span style={{color:'#94a3b8'}}>측정 속도 (v_A):</span>
                <span className="num-mono" style={{fontWeight:700,color:'#86efac'}}>
                  {measData ? `${measData.vA > 0 ? '+' : ''}${measData.vA.toFixed(2)} m/s` : '0.00 m/s'}
                </span>
              </div>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:12,borderTop:'1px dashed #334155',paddingTop:4}}>
                <span style={{color:'#cbd5e1',fontWeight:700}}>운동량 (p_A):</span>
                <span className="num-mono" style={{fontWeight:800,color:'#a3e635'}}>
                  {measData ? `${measData.pA > 0 ? '+' : ''}${measData.pA.toFixed(3)}` : '0.000'} kg·m/s
                </span>
              </div>
            </div>

            {/* 수레 B 센서 데이터 */}
            <div style={{background:'rgba(2,132,199,0.1)',padding:10,borderRadius:8,border:'1px solid rgba(14,165,233,0.3)'}}>
              <p style={{fontSize:11.5,fontWeight:700,color:'#38bdf8',marginBottom:6}}>수레 B (우측 / 추 2개)</p>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:12,marginBottom:4}}>
                <span style={{color:'#94a3b8'}}>질량 (m_B):</span>
                <span className="num-mono" style={{fontWeight:700,color:'#e0f2fe'}}>{massB.toFixed(2)} kg</span>
              </div>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:12,marginBottom:4}}>
                <span style={{color:'#94a3b8'}}>측정 속도 (v_B):</span>
                <span className="num-mono" style={{fontWeight:700,color:'#38bdf8'}}>
                  {measData ? `${measData.vB > 0 ? '+' : ''}${measData.vB.toFixed(2)} m/s` : '0.00 m/s'}
                </span>
              </div>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:12,borderTop:'1px dashed #334155',paddingTop:4}}>
                <span style={{color:'#cbd5e1',fontWeight:700}}>운동량 (p_B):</span>
                <span className="num-mono" style={{fontWeight:800,color:'#38bdf8'}}>
                  {measData ? `+${measData.pB.toFixed(3)}` : '0.000'} kg·m/s
                </span>
              </div>
            </div>

          </div>

          {/* 전체 운동량 합계 바 */}
          <div style={{marginTop:12,background:'#0f172a',padding:'10px 14px',borderRadius:8,display:'flex',justifyContent:'space-between',alignItems:'center',border:'1px solid #1e293b'}}>
            <div>
              <span style={{fontSize:12.5,fontWeight:700,color:'#f8fafc'}}>전체 운동량 합계 (p_A + p_B):</span>
              <span style={{fontSize:11,color:'#94a3b8',marginLeft:6}}>분리 전 정지 상태 = 0 kg·m/s</span>
            </div>
            <span className="num-mono" style={{fontSize:16,fontWeight:800,color:'#22c55e'}}>
              {measData ? `${measData.pTot >= 0 ? '+' : ''}${measData.pTot.toFixed(3)} kg·m/s` : '0.000 kg·m/s'}
            </span>
          </div>

          <div style={{marginTop:10,fontSize:11.5,color:'#94a3b8',lineHeight:1.6}}>
            💡 <b>실험 결과 해석:</b> 질량이 2배 큰 수레 B는 속도가 정확히 절반(<Eq f="v_B = \frac{1}{2} v_A"/>)으로 튀어나가며,
            두 수레의 운동량 크기는 정확히 같고 부호만 반대(<Eq f="p_A = -p_B"/>)이므로 <b>운동량 보존 법칙</b>이 완벽히 성립합니다.
          </div>
        </div>

        {/* 우측: 교과서 결과 기록 표 */}
        <div className="card">
          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:10}}>
            <span style={{fontWeight:800,fontSize:13.5,color:'#f8fafc'}}>📊 교과서 실험 결과 기록 표</span>
            <span style={{fontSize:11,color:'#64748b'}}>누적 {logList.length}회 측정</span>
          </div>

          <div style={{overflowX:'auto'}}>
            <table className="table-custom">
              <thead>
                <tr>
                  <th>회차</th>
                  <th>수레 구분</th>
                  <th>질량 (kg)</th>
                  <th>속도 (m/s)</th>
                  <th>운동량 (kg·m/s)</th>
                  <th>전체 합 (kg·m/s)</th>
                </tr>
              </thead>
              <tbody>
                {logList.map(item => (
                  <React.Fragment key={item.id}>
                    <tr>
                      <td rowSpan={2} style={{fontWeight:700,background:'#0a0f1d'}}>{item.id}</td>
                      <td style={{color:'#a3e635',textAlign:'left',paddingLeft:10}}>{item.nameA}</td>
                      <td className="num-mono">{item.mA.toFixed(2)}</td>
                      <td className="num-mono" style={{color:'#86efac'}}>{item.vA.toFixed(2)}</td>
                      <td className="num-mono" style={{fontWeight:700,color:'#a3e635'}}>{item.pA.toFixed(3)}</td>
                      <td rowSpan={2} className="num-mono" style={{fontWeight:800,color:'#22c55e',background:'#0a0f1d'}}>
                        {item.pTot.toFixed(3)}
                      </td>
                    </tr>
                    <tr>
                      <td style={{color:'#38bdf8',textAlign:'left',paddingLeft:10}}>{item.nameB}</td>
                      <td className="num-mono">{item.mB.toFixed(2)}</td>
                      <td className="num-mono" style={{color:'#38bdf8'}}>+{item.vB.toFixed(2)}</td>
                      <td className="num-mono" style={{fontWeight:700,color:'#38bdf8'}}>+{item.pB.toFixed(3)}</td>
                    </tr>
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{marginTop:10,display:'flex',justifyContent:'flex-end',gap:8}}>
            <button className="btn-secondary" onClick={()=>setLogList([])} style={{fontSize:11}}>
              🗑️ 기록 비우기
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 2: 발사체 추진 원리 연계 (그림 I-23)
══════════════════════════════════════════════════ */
function RocketPrincipleTab() {
  const [gasMass, setGasMass] = useState(150); // 분출 가스 질량 (kg)
  const [rocketMass, setRocketMass] = useState(850); // 로켓 본체 질량 (kg)
  const [gasVel, setGasVel] = useState(2400); // 가스 분출 속도 (m/s)
  
  // 물리 벡터 오버레이 토글
  const [showForceVec, setShowForceVec] = useState(true);
  const [showVelVec, setShowVelVec] = useState(true);
  const [showMomVec, setShowMomVec] = useState(true);

  // 시뮬레이션 상태: 'ready'(발사대기) | 'firing'(가스 분출 가속 중) | 'cruising'(분출 완료 후 등속 순항)
  const [simStatus, setSimStatus] = useState('ready');
  const [curV, setCurV] = useState(0);
  const [curFuelPct, setCurFuelPct] = useState(100);
  const [launchSummary, setLaunchSummary] = useState(null);

  // 이론값 계산
  const theoryV = (gasMass / rocketMass) * gasVel;
  const theoryP_gas = gasMass * gasVel;
  const theoryP_rocket = rocketMass * theoryV;

  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const simRef = useRef({
    x: 220, // 로켓 중심 X 좌표 (px)
    y: 120, // 로켓 중심 Y 좌표 (px)
    v: 0,
    progress: 0,
    fuelPct: 100,
    burnTime: 2.2, // 총 분출 소요 시간 (초)
    distKm: 0,
    bgOffset: 0,
    particles: [],
    stars: Array.from({ length: 65 }, (_, i) => ({
      x: (i * 39 + 17) % 800,
      y: (i * 23 + 7) % 230 + 5,
      r: (i % 4 === 0 ? 1.8 : (i % 2 === 0 ? 1.2 : 0.8)),
      brightness: 0.35 + ((i * 19) % 65) / 100
    }))
  });

  // 화살표 그리기 헬퍼 함수
  const drawArrow = (ctx, fromX, fromY, toX, toY, color, labelText, offsetLabelY = -6) => {
    if (Math.abs(toX - fromX) < 4 && Math.abs(toY - fromY) < 4) return;
    const headLen = 7;
    const dx = toX - fromX;
    const dy = toY - fromY;
    const angle = Math.atan2(dy, dx);

    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2.4;

    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(toX, toY);
    ctx.lineTo(toX - headLen * Math.cos(angle - Math.PI / 6), toY - headLen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(toX - headLen * Math.cos(angle + Math.PI / 6), toY - headLen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fill();

    if (labelText) {
      ctx.font = 'bold 9px Space Mono, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(labelText, (fromX + toX) / 2, fromY + offsetLabelY);
    }
  };

  // 캔버스 프레임 렌더링 함수
  const renderCanvas = () => {
    const cvs = canvasRef.current;
    if (!cvs) return;
    const ctx = cvs.getContext('2d');
    const W = cvs.width, H = cvs.height;
    const s = simRef.current;

    // 1. 깊은 우주 배경 클리어
    const bgGrad = ctx.createLinearGradient(0, 0, W, H);
    bgGrad.addColorStop(0, '#040714');
    bgGrad.addColorStop(0.5, '#080d22');
    bgGrad.addColorStop(1, '#050a18');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // 2. 우주 성운 글로우 효과
    const neb1 = ctx.createRadialGradient(W * 0.75, 40, 10, W * 0.75, 40, 180);
    neb1.addColorStop(0, 'rgba(14, 165, 233, 0.15)');
    neb1.addColorStop(1, 'rgba(14, 165, 233, 0)');
    ctx.fillStyle = neb1;
    ctx.fillRect(0, 0, W, H);

    const neb2 = ctx.createRadialGradient(W * 0.2, H * 0.75, 10, W * 0.2, H * 0.75, 160);
    neb2.addColorStop(0, 'rgba(168, 85, 247, 0.12)');
    neb2.addColorStop(1, 'rgba(168, 85, 247, 0)');
    ctx.fillStyle = neb2;
    ctx.fillRect(0, 0, W, H);

    // 3. 우주 배경 별무리 (패럴랙스 이동)
    s.stars.forEach(st => {
      const curStarX = (st.x - s.bgOffset * 0.4) % W;
      const finalX = curStarX < 0 ? curStarX + W : curStarX;
      ctx.fillStyle = `rgba(226, 232, 240, ${st.brightness})`;
      ctx.beginPath();
      ctx.arc(finalX, st.y, st.r, 0, Math.PI * 2);
      ctx.fill();
    });

    // 4. 하단 우주 공간 기준선 및 거리 눈금자 (스크롤 연동)
    const axisY = 215;
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(20, axisY);
    ctx.lineTo(W - 20, axisY);
    ctx.stroke();

    const tickSpacing = 80;
    const offsetMod = (s.bgOffset * 1.2) % tickSpacing;
    for (let tx = 20 - offsetMod; tx <= W - 20; tx += tickSpacing) {
      if (tx >= 20) {
        ctx.strokeStyle = '#334155';
        ctx.beginPath();
        ctx.moveTo(tx, axisY - 4);
        ctx.lineTo(tx, axisY + 4);
        ctx.stroke();
      }
    }
    ctx.fillStyle = '#64748b';
    ctx.font = '8px Space Mono';
    ctx.textAlign = 'left';
    ctx.fillText('우주 기준 좌표계 (정지계 관측)', 25, axisY - 8);
    ctx.textAlign = 'right';
    ctx.fillText(`누적 항행 거리: ${(s.distKm).toFixed(2)} km`, W - 25, axisY - 8);

    // 5. 배기가스 분출 파티클 렌더링
    s.particles.forEach(p => {
      ctx.save();
      ctx.globalAlpha = Math.max(0, p.life);
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    // 6. 로켓 본체 렌더링
    const rx = s.x;
    // 분출 가속 중일 때 미세한 추진 엔진 진동(rumble)
    const ry = s.y + (s.progress > 0 && s.progress < 1.0 ? (Math.random() - 0.5) * 2.2 : 0);

    const bodyW = 90;
    const bodyH = 26;
    const nozzleX = rx - bodyW / 2;
    const noseX = rx + bodyW / 2;

    // (1) 엔진 화염 제트 (가스 분출 중일 때)
    if (s.progress > 0 && s.progress < 1.0) {
      const flameLen = 45 + (gasVel / 4000) * 45 + Math.random() * 14;
      const flameH = 14 + (gasMass / 400) * 10;

      // 외부 오렌지/옐로 화염
      const flameGrad = ctx.createLinearGradient(nozzleX, ry, nozzleX - flameLen, ry);
      flameGrad.addColorStop(0, '#ffffff');
      flameGrad.addColorStop(0.2, '#38bdf8');
      flameGrad.addColorStop(0.45, '#f59e0b');
      flameGrad.addColorStop(0.8, '#ef4444');
      flameGrad.addColorStop(1, 'rgba(239,68,68,0)');

      ctx.fillStyle = flameGrad;
      ctx.beginPath();
      ctx.moveTo(nozzleX - 4, ry - flameH / 2);
      ctx.quadraticCurveTo(nozzleX - flameLen * 0.6, ry - flameH * 0.8, nozzleX - flameLen, ry);
      ctx.quadraticCurveTo(nozzleX - flameLen * 0.6, ry + flameH * 0.8, nozzleX - 4, ry + flameH / 2);
      ctx.closePath();
      ctx.fill();

      // 내부 초고온 청색 마하 다이아몬드 코어
      const coreLen = flameLen * 0.45;
      const coreGrad = ctx.createLinearGradient(nozzleX, ry, nozzleX - coreLen, ry);
      coreGrad.addColorStop(0, '#ffffff');
      coreGrad.addColorStop(0.6, '#38bdf8');
      coreGrad.addColorStop(1, 'rgba(56,189,248,0)');
      ctx.fillStyle = coreGrad;
      ctx.beginPath();
      ctx.moveTo(nozzleX - 4, ry - flameH * 0.3);
      ctx.lineTo(nozzleX - coreLen, ry);
      ctx.lineTo(nozzleX - 4, ry + flameH * 0.3);
      ctx.closePath();
      ctx.fill();
    }

    // (2) 로켓 날개 핀 (위/아래)
    ctx.fillStyle = '#1e293b';
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 1;
    // 상단 핀
    ctx.beginPath();
    ctx.moveTo(nozzleX + 4, ry - bodyH / 2);
    ctx.lineTo(nozzleX - 10, ry - bodyH / 2 - 12);
    ctx.lineTo(nozzleX + 22, ry - bodyH / 2);
    ctx.closePath();
    ctx.fill(); ctx.stroke();
    // 하단 핀
    ctx.beginPath();
    ctx.moveTo(nozzleX + 4, ry + bodyH / 2);
    ctx.lineTo(nozzleX - 10, ry + bodyH / 2 + 12);
    ctx.lineTo(nozzleX + 22, ry + bodyH / 2);
    ctx.closePath();
    ctx.fill(); ctx.stroke();

    // (3) 로켓 엔진 노즐 벨 (원뿔대)
    const nozGrad = ctx.createLinearGradient(nozzleX - 12, ry, nozzleX, ry);
    nozGrad.addColorStop(0, '#334155');
    nozGrad.addColorStop(0.7, '#64748b');
    nozGrad.addColorStop(1, '#94a3b8');
    ctx.fillStyle = nozGrad;
    ctx.beginPath();
    ctx.moveTo(nozzleX, ry - bodyH * 0.36);
    ctx.lineTo(nozzleX - 12, ry - bodyH * 0.52);
    ctx.lineTo(nozzleX - 12, ry + bodyH * 0.52);
    ctx.lineTo(nozzleX, ry + bodyH * 0.36);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#475569';
    ctx.stroke();

    // (4) 로켓 원통형 본체
    const bGrad = ctx.createLinearGradient(0, ry - bodyH / 2, 0, ry + bodyH / 2);
    bGrad.addColorStop(0, '#f8fafc');
    bGrad.addColorStop(0.35, '#cbd5e1');
    bGrad.addColorStop(0.85, '#475569');
    bGrad.addColorStop(1, '#1e293b');
    ctx.fillStyle = bGrad;
    ctx.beginPath();
    ctx.roundRect(nozzleX, ry - bodyH / 2, bodyW - 20, bodyH, [2, 0, 0, 2]);
    ctx.fill();
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1.2;
    ctx.strokeRect(nozzleX, ry - bodyH / 2, bodyW - 20, bodyH);

    // 단 분리 밴드 데칼 (1단/2단 분리선)
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(nozzleX + (bodyW - 20) * 0.55, ry - bodyH / 2, 4, bodyH);
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(nozzleX + (bodyW - 20) * 0.57, ry - bodyH / 2, 2, bodyH);

    // (5) 로켓 전방 노즈콘 (유선형 페어링)
    const noseStart = nozzleX + bodyW - 20;
    const noseGrad = ctx.createLinearGradient(noseStart, ry - bodyH / 2, noseX, ry);
    noseGrad.addColorStop(0, '#cbd5e1');
    noseGrad.addColorStop(0.7, '#f8fafc');
    noseGrad.addColorStop(1, '#38bdf8');
    ctx.fillStyle = noseGrad;
    ctx.beginPath();
    ctx.moveTo(noseStart, ry - bodyH / 2);
    ctx.quadraticCurveTo(noseStart + 16, ry - bodyH / 2 + 2, noseX, ry);
    ctx.quadraticCurveTo(noseStart + 16, ry + bodyH / 2 - 2, noseStart, ry + bodyH / 2);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#334155';
    ctx.stroke();

    // (6) 본체 텍스트 각인
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 8.5px Space Mono';
    ctx.textAlign = 'center';
    ctx.fillText(`M=${rocketMass}kg`, nozzleX + (bodyW - 20) * 0.28, ry + 3);

    // 7. 물리 벡터 화살표 오버레이
    // (1) 작용-반작용 힘 벡터 (F_gas, F_thrust) - 분출 중에만 가동
    if (showForceVec && s.progress > 0 && s.progress < 1.0) {
      const fScale = 55;
      // 노즐에서 가스를 뒤로 밀어내는 힘 F_gas (← 주황색)
      drawArrow(ctx, nozzleX - 14, ry - 22, nozzleX - 14 - fScale, ry - 22, '#f97316', 'F_작용(가스 ←)', -6);
      // 로켓을 앞으로 미는 추진력 F_thrust (→ 주황색)
      drawArrow(ctx, rx + 15, ry - 22, rx + 15 + fScale, ry - 22, '#f97316', 'F_추진(로켓 →)', -6);
    }

    // (2) 속도 벡터 (v_gas, V_rocket)
    if (showVelVec && s.progress > 0) {
      // 로켓 속도 V (→ 하늘색)
      const vScale = Math.min(100, Math.max(12, (s.v / theoryV) * 75));
      drawArrow(ctx, noseX + 4, ry, noseX + 4 + vScale, ry, '#38bdf8', `V = +${s.v.toFixed(1)} m/s`, -7);

      // 가스 분출 속도 v (← 연두색) - 분출 중일 때
      if (s.progress < 1.0) {
        const gasVScale = Math.min(85, (gasVel / 4000) * 75);
        drawArrow(ctx, nozzleX - 18, ry + 22, nozzleX - 18 - gasVScale, ry + 22, '#86efac', `v = -${gasVel.toLocaleString()} m/s`, 14);
      }
    }

    // (3) 운동량 벡터 (p_gas, P_rocket) - 핵심 원리!
    if (showMomVec && s.progress > 0) {
      const curProg = Math.min(1.0, s.progress);
      const curMomRocket = rocketMass * s.v;
      const curMomGas = gasMass * curProg * gasVel;
      const momScale = Math.min(95, (curMomRocket / Math.max(1, theoryP_rocket)) * 85);

      if (momScale > 8) {
        // 로켓 운동량 P_rocket (→ 보라색)
        drawArrow(ctx, rx + 20, ry + 28, rx + 20 + momScale, ry + 28, '#c084fc', `P_로켓=+${Math.round(curMomRocket).toLocaleString()}`, 14);
        // 가스 총 운동량 p_gas (← 보라색)
        drawArrow(ctx, nozzleX - 22, ry + 28, nozzleX - 22 - momScale, ry + 28, '#c084fc', `p_가스=-${Math.round(curMomGas).toLocaleString()}`, 14);
      }
    }

    // 8. 캔버스 내부 상단 실시간 HUD 배너
    // 좌측: 상태 뱃지
    let statusText = '⚪ [발사 대기] 연료 완충 상태';
    let statusBg = 'rgba(15, 23, 42, 0.75)';
    let statusBorder = '#334155';
    let statusCol = '#94a3b8';

    if (s.progress > 0 && s.progress < 1.0) {
      statusText = '🔥 [주엔진 연소 가속 중...] 고온 가스 초음속 분출';
      statusBg = 'rgba(180, 83, 9, 0.35)';
      statusBorder = '#f59e0b';
      statusCol = '#fef08a';
    } else if (s.progress >= 1.0) {
      statusText = '🛸 [목표 속도 달성] 관성 등속 순항 중 (외력 0, 운동량 보존)';
      statusBg = 'rgba(12, 74, 110, 0.35)';
      statusBorder = '#0ea5e9';
      statusCol = '#7dd3fc';
    }

    // 상태 배지 그리기
    ctx.fillStyle = statusBg;
    ctx.strokeStyle = statusBorder;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(14, 12, 330, 26, 6);
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = statusCol;
    ctx.font = 'bold 10px Noto Sans KR, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(statusText, 24, 28);

    // 우측: 실시간 속도계 및 연료 잔량
    const fuelPct = Math.max(0, 100 * (1 - Math.min(1, s.progress)));
    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.strokeStyle = '#1e3a8a';
    ctx.beginPath();
    ctx.roundRect(W - 250, 12, 236, 42, 6);
    ctx.fill(); ctx.stroke();

    ctx.fillStyle = '#94a3b8';
    ctx.font = '9px Noto Sans KR';
    ctx.fillText('현재 로켓 속도 V:', W - 240, 27);
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 15px Space Mono';
    ctx.fillText(`+${s.v.toFixed(1)} m/s`, W - 145, 27);

    // 연료 게이지 바
    ctx.fillStyle = '#64748b';
    ctx.font = '8px Space Mono';
    ctx.fillText(`연료 ${fuelPct.toFixed(0)}%`, W - 240, 44);
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(W - 180, 37, 155, 7);
    const fuelGrad = ctx.createLinearGradient(W - 180, 0, W - 25, 0);
    fuelGrad.addColorStop(0, '#f59e0b');
    fuelGrad.addColorStop(1, '#ef4444');
    ctx.fillStyle = fuelGrad;
    ctx.fillRect(W - 180, 37, (fuelPct / 100) * 155, 7);

    // 중앙 하단: 운동량 보존 인디케이터 배너
    if (s.progress > 0) {
      const curProg = Math.min(1.0, s.progress);
      const pR = Math.round(rocketMass * s.v);
      const pG = Math.round(gasMass * curProg * gasVel);
      ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
      ctx.strokeStyle = '#a855f7';
      ctx.beginPath();
      ctx.roundRect(W / 2 - 190, H - 36, 380, 24, 6);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#e9d5ff';
      ctx.font = 'bold 9.5px Space Mono, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`⚖️ 운동량 보존: P_로켓(+${pR.toLocaleString()}) + p_가스(-${pG.toLocaleString()}) = 0 kg·m/s`, W / 2, H - 21);
    }
  };

  // 🚀 연료 분출 발사 시험 트리거
  const triggerRocketLaunch = () => {
    cancelAnimationFrame(animRef.current);
    const s = simRef.current;
    s.x = 220;
    s.v = 0;
    s.distKm = 0;
    s.progress = 0;
    s.fuelPct = 100;
    s.bgOffset = 0;
    s.particles = [];

    setSimStatus('firing');
    setCurV(0);
    setCurFuelPct(100);
    setLaunchSummary(null);

    let startTime = null;
    const BURN_DUR = 2.4; // 2.4초간 가스 분출 가속
    const finalV = theoryV;

    const step = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const elapsed = (timestamp - startTime) / 1000;
      const prog = Math.min(1.0, elapsed / BURN_DUR);

      s.progress = prog;
      s.fuelPct = Math.max(0, 100 * (1 - prog));

      // 가속 단계
      if (prog < 1.0) {
        s.v = finalV * prog;
        // 로켓 위치 전진 (캔버스 안에서 시각적으로 전진)
        s.x = 220 + prog * 160;
        // 가스 분출 파티클 생성
        const numParticles = Math.floor(4 + (gasMass / 80));
        for (let i = 0; i < numParticles; i++) {
          s.particles.push({
            x: s.x - 45,
            y: s.y + (Math.random() - 0.5) * 8,
            vx: -(gasVel / 320) * (0.7 + Math.random() * 0.6),
            vy: (Math.random() - 0.5) * 2.8,
            life: 1.0,
            decay: 0.035 + Math.random() * 0.03,
            size: 3.5 + Math.random() * 5.0,
            color: Math.random() > 0.4 ? '#f97316' : (Math.random() > 0.5 ? '#facc15' : '#67e8f9')
          });
        }
      } else {
        // 분출 완료 후 등속 순항 단계 (뉴턴 관성 운동)
        s.v = finalV;
        s.x = 380;
        if (simStatus !== 'cruising') {
          setSimStatus('cruising');
          setLaunchSummary({
            rocketMass,
            gasMass,
            gasVel,
            finalV,
            pGas: theoryP_gas,
            pRocket: theoryP_rocket
          });
        }
      }

      // 파티클 업데이트
      s.particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.life -= p.decay;
        p.size *= 1.03;
      });
      s.particles = s.particles.filter(p => p.life > 0);

      // 배경 패럴랙스 및 비행 거리 누적
      const dtSec = 1 / 60;
      s.distKm += (s.v * dtSec) / 1000;
      s.bgOffset += Math.max(0.8, s.v * 0.015);

      setCurV(s.v);
      setCurFuelPct(s.fuelPct);

      renderCanvas();

      // 분출 종료 후 4초간 순항 모습을 보여준 뒤 종료 대기
      if (elapsed < BURN_DUR + 4.0) {
        animRef.current = requestAnimationFrame(step);
      } else {
        // 애니메이션 지속 루프 유지 (배경과 별만 은은히 흐름)
        const cruiseLoop = () => {
          s.bgOffset += Math.max(0.8, s.v * 0.015);
          s.distKm += (s.v * dtSec) / 1000;
          renderCanvas();
          animRef.current = requestAnimationFrame(cruiseLoop);
        };
        animRef.current = requestAnimationFrame(cruiseLoop);
      }
    };

    animRef.current = requestAnimationFrame(step);
  };

  // 🔄 발사대 초기화 (리셋)
  const resetRocketLaunch = () => {
    cancelAnimationFrame(animRef.current);
    const s = simRef.current;
    s.x = 220;
    s.y = 120;
    s.v = 0;
    s.distKm = 0;
    s.progress = 0;
    s.fuelPct = 100;
    s.bgOffset = 0;
    s.particles = [];

    setSimStatus('ready');
    setCurV(0);
    setCurFuelPct(100);
    setLaunchSummary(null);

    renderCanvas();
  };

  // 초기 렌더링 및 슬라이더 변경 시 반영
  useEffect(() => {
    resetRocketLaunch();
  }, [rocketMass, gasMass, gasVel]);

  return (
    <div>
      {/* ── 교과서 본문 텍스트 연계 ── */}
      <div className="hl-box">
        <h3 style={{color:'#93c5fd',fontSize:15,fontWeight:800,marginBottom:8}}>
          🚀 교과서 단원 연계: 그림 I-23 용수철을 사이에 둔 두 수레와 발사체 추진 원리
        </h3>
        <p style={{fontSize:13.5,lineHeight:1.8,color:'#e2e8f0'}}>
          발사체는 배기가스를 분출해 추진력을 얻어 날아갑니다. 이것은 <b>질량 M인 수레 B의 용수철이 압축 상태에서 펴지면서 질량 m인 수레 A를 밀면, 
          B와 A가 각각 속도 V, v로 반대 방향으로 운동하는 것과 완벽히 같은 원리</b>입니다.
        </p>
      </div>

      {/* ── 1:1 대응 원리 다이어그램 ── */}
      <div className="card">
        <p style={{fontWeight:800,fontSize:14,color:'#fbbf24',marginBottom:14}}>
          🔍 수레 분리 실험 ↔ 우주 발사체(로켓) 추진의 1:1 물리적 대응 관계
        </p>
        
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(300px, 1fr))',gap:16}}>
          {/* 수레 실험 모델 */}
          <div style={{background:'#0a1020',padding:16,borderRadius:12,border:'1px solid #1e293b'}}>
            <div style={{display:'flex',justifyContent:'space-between',marginBottom:10}}>
              <span style={{fontWeight:700,color:'#86efac'}}>🛒 [실험실] 용수철 두 수레</span>
              <span className="badge badge-lime">정지계</span>
            </div>
            
            <svg width="100%" height="80" viewBox="0 0 320 80">
              <line x1="20" y1="65" x2="300" y2="65" stroke="#475569" strokeWidth="3"/>
              <rect x="50" y="25" width="70" height="32" rx="4" fill="#65a30d" stroke="#84cc16"/>
              <text x="85" y="45" fill="#fff" fontSize="11" textAnchor="middle" fontWeight="bold">수레 A (m)</text>
              <circle cx="65" cy="60" r="5" fill="#1e293b"/>
              <circle cx="105" cy="60" r="5" fill="#1e293b"/>
              <rect x="180" y="25" width="90" height="32" rx="4" fill="#0284c7" stroke="#0ea5e9"/>
              <text x="225" y="45" fill="#fff" fontSize="11" textAnchor="middle" fontWeight="bold">수레 B (M)</text>
              <circle cx="200" cy="60" r="5" fill="#1e293b"/>
              <circle cx="250" cy="60" r="5" fill="#1e293b"/>
              <path d="M 120 41 Q 128 32, 135 41 T 150 41 T 165 41 T 180 41" fill="none" stroke="#f59e0b" strokeWidth="2.5"/>
              <line x1="110" y1="14" x2="60" y2="14" stroke="#f97316" strokeWidth="2"/>
              <text x="85" y="10" fill="#f97316" fontSize="9" textAnchor="middle">F_BA (←)</text>
              <line x1="190" y1="14" x2="240" y2="14" stroke="#f97316" strokeWidth="2"/>
              <text x="215" y="10" fill="#f97316" fontSize="9" textAnchor="middle">F_AB (→)</text>
            </svg>

            <ul style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.8,marginTop:10,paddingLeft:16}}>
              <li><b>수레 A (질량 m):</b> 로켓에서 뒤로 뿜어져 나가는 <b>배기가스</b>에 대응</li>
              <li><b>수레 B (질량 M):</b> 앞으로 추진되는 <b>발사체(로켓) 본체</b>에 대응</li>
              <li><b>압축 용수철:</b> 연료 연소 시 팽창하는 <b>고온·고압 가스 압력</b>에 대응</li>
            </ul>
          </div>

          {/* 실제 로켓 추진 모델 */}
          <div style={{background:'#0a1020',padding:16,borderRadius:12,border:'1px solid #1e293b'}}>
            <div style={{display:'flex',justifyContent:'space-between',marginBottom:10}}>
              <span style={{fontWeight:700,color:'#38bdf8'}}>🚀 [우주 공간] 발사체 추진</span>
              <span className="badge badge-blue">무중력 진공</span>
            </div>

            <svg width="100%" height="80" viewBox="0 0 320 80">
              <ellipse cx="60" cy="40" rx="35" ry="12" fill="rgba(249,115,22,0.4)"/>
              <polygon points="40,36 20,28 35,40 20,52 40,44" fill="#ef4444"/>
              <text x="60" y="44" fill="#fdba74" fontSize="10" textAnchor="middle" fontWeight="bold">가스 (m, v)</text>
              <rect x="100" y="24" width="110" height="32" rx="4" fill="#334155" stroke="#94a3b8"/>
              <polygon points="210,24 240,40 210,56" fill="#e2e8f0"/>
              <text x="155" y="44" fill="#fff" fontSize="11" textAnchor="middle" fontWeight="bold">로켓 본체 (M, V)</text>
              <line x1="245" y1="40" x2="295" y2="40" stroke="#38bdf8" strokeWidth="2.5"/>
              <text x="270" y="32" fill="#38bdf8" fontSize="10" textAnchor="middle" fontWeight="bold">전진 (→ V)</text>
            </svg>

            <ul style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.8,marginTop:10,paddingLeft:16}}>
              <li>뉴턴 제3법칙 작용-반작용: <Eq f="\vec{F}_{\text{가스}} = -\vec{F}_{\text{로켓}}"/></li>
              <li>양변에 분출 시간 <Eq f="\Delta t"/>를 곱하면 충격량이 같음: <Eq f="\Delta \vec{p}_{\text{가스}} = -\Delta \vec{p}_{\text{로켓}}"/></li>
              <li>전체 운동량 보존: <Eq f="m\vec{v} + M\vec{V} = 0 \implies \vec{V} = -\frac{m}{M}\vec{v}"/></li>
            </ul>
          </div>
        </div>
      </div>

      {/* ── 인터랙티브 로켓 가속 시뮬레이터 ── */}
      <div className="card">
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:12,flexWrap:'wrap',gap:8}}>
          <div>
            <span style={{fontWeight:800,fontSize:15,color:'#f8fafc'}}>
              🌌 [실시간 시뮬레이션] 우주 발사체 가스 분출 가속 실험실
            </span>
            <span style={{fontSize:12,color:'#94a3b8',marginLeft:8}}>
              (가스 분출 시 작용-반작용과 운동량 보존을 시각적으로 관찰합니다)
            </span>
          </div>

          {/* 물리 벡터 토글 체크박스 */}
          <div style={{display:'flex',gap:12,fontSize:12}}>
            <label style={{display:'flex',alignItems:'center',gap:4,cursor:'pointer',color:'#fb923c'}}>
              <input type="checkbox" checked={showForceVec} onChange={e=>setShowForceVec(e.target.checked)}/>
              작용·반작용 힘 (<span style={{fontFamily:'Space Mono'}}>F</span>)
            </label>
            <label style={{display:'flex',alignItems:'center',gap:4,cursor:'pointer',color:'#38bdf8'}}>
              <input type="checkbox" checked={showVelVec} onChange={e=>setShowVelVec(e.target.checked)}/>
              속도 벡터 (<span style={{fontFamily:'Space Mono'}}>v, V</span>)
            </label>
            <label style={{display:'flex',alignItems:'center',gap:4,cursor:'pointer',color:'#c084fc'}}>
              <input type="checkbox" checked={showMomVec} onChange={e=>setShowMomVec(e.target.checked)}/>
              운동량 벡터 (<span style={{fontFamily:'Space Mono'}}>p, P</span>)
            </label>
          </div>
        </div>

        {/* ── 캔버스 디스플레이 ── */}
        <canvas ref={canvasRef} width={800} height={235}
          style={{width:'100%',borderRadius:12,border:'1px solid #1e293b',background:'#040714',display:'block',boxShadow:'0 4px 20px rgba(0,0,0,0.6)',marginBottom:16}} />

        {/* ── 조절 슬라이더 ── */}
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(220px, 1fr))',gap:14,marginBottom:16}}>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>로켓 본체 질량 (M)</label>
            <input type="range" min="400" max="1500" step="50" value={rocketMass} onChange={e=>setRocketMass(+e.target.value)} disabled={simStatus==='firing'} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#60a5fa',fontFamily:'Space Mono'}}>
              <span>400 kg</span><span>{rocketMass} kg</span><span>1500 kg</span>
            </div>
          </div>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>분출 가스 질량 (m)</label>
            <input type="range" min="50" max="400" step="25" value={gasMass} onChange={e=>setGasMass(+e.target.value)} disabled={simStatus==='firing'} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#f59e0b',fontFamily:'Space Mono'}}>
              <span>50 kg</span><span>{gasMass} kg</span><span>400 kg</span>
            </div>
          </div>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>배기가스 분출 속력 (v)</label>
            <input type="range" min="1000" max="4000" step="200" value={gasVel} onChange={e=>setGasVel(+e.target.value)} disabled={simStatus==='firing'} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#86efac',fontFamily:'Space Mono'}}>
              <span>1,000 m/s</span><span>{gasVel.toLocaleString()} m/s</span><span>4,000 m/s</span>
            </div>
          </div>
        </div>

        {/* ── 결과 박스 & 발사 버튼 ── */}
        <div style={{background:'#0a1224',padding:16,borderRadius:12,border:'1px solid #1e3a8a',display:'flex',justifyContent:'space-between',alignItems:'center',flexWrap:'wrap',gap:14}}>
          <div>
            <p style={{fontSize:12,color:'#94a3b8',marginBottom:4}}>
              로켓이 얻는 이론 속도 증가량 (ΔV = <Eq f="\frac{m}{M}v"/>):
            </p>
            <div style={{display:'flex',alignItems:'baseline',gap:8}}>
              <span className="num-mono" style={{fontSize:28,fontWeight:800,color:'#38bdf8'}}>
                +{theoryV.toFixed(1)}
              </span>
              <span style={{fontSize:14,color:'#93c5fd',fontWeight:700}}>m/s</span>
              <span style={{fontSize:12,color:'#64748b'}}>
                = ({theoryV * 3.6 >= 1000 ? (theoryV*3.6/1000).toFixed(1) + 'k' : (theoryV*3.6).toFixed(0)} km/h)
              </span>
            </div>
          </div>

          <div style={{display:'flex',gap:10,alignItems:'center'}}>
            <button className="btn-secondary" onClick={resetRocketLaunch} disabled={simStatus==='firing'}
              style={{padding:'12px 18px',fontSize:13}}>
              🔄 발사대 초기화
            </button>
            <button className="btn-success" onClick={triggerRocketLaunch} disabled={simStatus==='firing'}
              style={{padding:'12px 26px',fontSize:14,boxShadow:'0 0 18px rgba(22,163,74,0.45)'}}>
              {simStatus==='firing' ? '🔥 가스 분출 가속 중...' : '🚀 연료 분출 발사 시험!'}
            </button>
          </div>
        </div>

        {/* ── 시험 완료 후 정량적 운동량 보존 결과 브리핑 카드 ── */}
        {launchSummary && (
          <div style={{marginTop:14,background:'rgba(15,23,42,0.9)',padding:16,borderRadius:12,border:'1px solid #38bdf8'}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:10}}>
              <span style={{fontWeight:800,color:'#38bdf8',fontSize:14}}>
                📊 [시험 결과 분석] 발사체-배기가스 운동량 보존 정량 검증
              </span>
              <span className="badge badge-blue">실험 완료</span>
            </div>

            <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(180px, 1fr))',gap:10,marginBottom:12}}>
              <div style={{background:'#090d16',padding:10,borderRadius:8,border:'1px solid #1e293b'}}>
                <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>배기가스 총 운동량 (p_gas)</span>
                <span className="num-mono" style={{fontSize:15,fontWeight:700,color:'#f97316'}}>
                  -{(launchSummary.pGas).toLocaleString()} kg·m/s
                </span>
              </div>
              <div style={{background:'#090d16',padding:10,borderRadius:8,border:'1px solid #1e293b'}}>
                <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>로켓 본체 운동량 (P_rocket)</span>
                <span className="num-mono" style={{fontSize:15,fontWeight:700,color:'#38bdf8'}}>
                  +{(launchSummary.pRocket).toLocaleString()} kg·m/s
                </span>
              </div>
              <div style={{background:'#090d16',padding:10,borderRadius:8,border:'1px solid #1e293b'}}>
                <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>전체 운동량 합 (p_total)</span>
                <span className="num-mono" style={{fontSize:15,fontWeight:700,color:'#a3e635'}}>
                  0.000 kg·m/s (100% 보존)
                </span>
              </div>
              <div style={{background:'#090d16',padding:10,borderRadius:8,border:'1px solid #1e293b'}}>
                <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>최종 달성 속도 (V_final)</span>
                <span className="num-mono" style={{fontSize:15,fontWeight:700,color:'#fbbf24'}}>
                  +{(launchSummary.finalV).toFixed(1)} m/s
                </span>
              </div>
            </div>

            <p style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.7}}>
              💡 <b>정량적 결론:</b> 배기가스가 뒤로 가져간 운동량 <Eq f="p = m \cdot (-v)"/>와 로켓이 앞으로 얻은 운동량 <Eq f="P = M \cdot V"/>의 
              크기는 정확히 일치하며 방향이 반대입니다. 따라서 외력이 없는 우주 공간에서 <b>전체 계의 운동량의 총합은 정확히 0으로 완벽하게 보존</b>됩니다!
            </p>
          </div>
        )}

        {/* 다단계 로켓의 필요성 설명 박스 */}
        <div style={{marginTop:14,background:'rgba(30,41,59,0.5)',padding:14,borderRadius:10,border:'1px solid #334155',fontSize:12.5,color:'#cbd5e1',lineHeight:1.8}}>
          💡 <b>다단계 로켓(1단, 2단 분리)이 필수적인 물리적 이유:</b><br/>
          위 공식 <Eq f="V = \frac{m}{M} v"/>에서 알 수 있듯이, 로켓의 속도 증가량은 <b>본체 질량 M에 반비례</b>합니다.<br/>
          연료를 모두 소모한 빈 연료탱크는 불필요한 질량 M이 되어 추가 가속을 방해합니다. 따라서 빈 1단 로켓을 분리하여 버림으로써 본체 질량 M을 대폭 가볍게 만들어야만 최종 궤도 속도(약 7.9 km/s)에 도달할 수 있습니다.
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 2-2: [원리 탐구 2] 발사체 질량 감소와 속도 증가 (그림 I-24)
══════════════════════════════════════════════════ */
function RocketMotionPrincipleTab() {
  // 슬라이더 상태 변수
  const [initMass, setInitMass] = useState(1000);   // 초기 전체 질량 M (kg)
  const [initVel, setInitVel] = useState(400);      // 초기 비행 속력 V (m/s)
  const [deltaM, setDeltaM] = useState(100);        // 방출 배기가스 질량 Δm (kg)
  const [relU, setRelU] = useState(2000);           // 상대 분사 속력 u (m/s)

  // 관측 기준계: 'ground'(외부 정지계: 배경 고정, 로켓 상승) | 'rocket'(로켓계: 로켓 고정, 배경 흐름)
  const [frameView, setFrameView] = useState('ground');

  // 물리 벡터 토글
  const [showVelVec, setShowVelVec] = useState(true);
  const [showMomVec, setShowMomVec] = useState(true);

  // 시뮬레이션 상태: 'before'(방출 전) | 'ejecting'(방출 중) | 'after'(방출 후 가속)
  const [simState, setSimState] = useState('before');
  const [curV, setCurV] = useState(initVel);
  const [curM, setCurM] = useState(initMass);

  // 물리 이론값 정밀 계산
  const exactDeltaV = (relU * deltaM) / (initMass - deltaM);
  const approxDeltaV = (relU * deltaM) / initMass;
  const finalVel = initVel + exactDeltaV;
  const gasGroundVel = initVel - relU; // 지상 관측계 배기가스 속도 (V - u)

  // 운동량 계산 (kg·m/s)
  const P_initial = initMass * initVel;
  const P_rocket_after = (initMass - deltaM) * finalVel;
  const P_gas_after = deltaM * gasGroundVel;
  const P_total_after = P_rocket_after + P_gas_after;

  // 2차 미소량 분석 (Δm * Δv)
  const term_dmdv = deltaM * exactDeltaV;
  const term_udm = relU * deltaM;
  const term_Mdv = initMass * exactDeltaV;

  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const simRef = useRef({
    rocketY: 170, // 정지계에서는 아래쪽 시작, 로켓계에서는 135 중앙 고정
    rocketX: 400,
    vel: initVel,
    mass: initMass,
    state: 'before',
    altKm: 120.0,
    gasPosY: 0,
    gasAlpha: 0,
    ejectProgress: 0,
    ejectStartTime: null,
    stars: Array.from({ length: 65 }, (_, i) => ({
      x: (i * 37 + 19) % 800,
      y: (i * 29 + 11) % 260,
      r: (i % 3 === 0 ? 1.7 : 1.0),
      speedMult: 0.6 + ((i * 13) % 9) / 10
    })),
    particles: []
  });

  // 화살표 그리기 헬퍼 함수
  const drawVecArrow = (ctx, fromX, fromY, toX, toY, color, labelText, offsetLabelX = 0, offsetLabelY = -6) => {
    if (Math.abs(toX - fromX) < 3 && Math.abs(toY - fromY) < 3) return;
    const headLen = 7;
    const dx = toX - fromX;
    const dy = toY - fromY;
    const angle = Math.atan2(dy, dx);

    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2.4;

    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(toX, toY);
    ctx.lineTo(toX - headLen * Math.cos(angle - Math.PI / 6), toY - headLen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(toX - headLen * Math.cos(angle + Math.PI / 6), toY - headLen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fill();

    if (labelText) {
      ctx.font = 'bold 9px Space Mono, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(labelText, (fromX + toX) / 2 + offsetLabelX, (fromY + toY) / 2 + offsetLabelY);
    }
  };

  // 캔버스 그리기 함수
  const drawScene = (ctx, W, H, s) => {
    // 1. 심우주 배경
    const bgGrad = ctx.createLinearGradient(0, 0, 0, H);
    bgGrad.addColorStop(0, '#020617');
    bgGrad.addColorStop(0.5, '#070f26');
    bgGrad.addColorStop(1, '#030712');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // 은은한 성운 글로우
    const radG = ctx.createRadialGradient(W / 2, H / 2, 20, W / 2, H / 2, 220);
    radG.addColorStop(0, 'rgba(30, 58, 138, 0.18)');
    radG.addColorStop(1, 'rgba(2, 6, 23, 0)');
    ctx.fillStyle = radG;
    ctx.fillRect(0, 0, W, H);

    // 2. 배경 별무리 렌더링
    // (정지계: 별 위치 완전 고정! / 로켓계: 별이 아래로 흘러내림)
    s.stars.forEach(st => {
      ctx.fillStyle = '#e2e8f0';
      ctx.beginPath();
      ctx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
      ctx.fill();
    });

    // 3. 고도 및 기준 좌표계 축 (좌측)
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(40, 10);
    ctx.lineTo(40, H - 10);
    ctx.stroke();

    if (frameView === 'ground') {
      // 정지계: 고정된 지표면 기준 격자 눈금자 (화면에 고정!)
      const groundTicks = [
        { y: 35, label: '200 km' },
        { y: 85, label: '160 km' },
        { y: 135, label: '120 km' },
        { y: 185, label: '80 km' },
        { y: 235, label: '40 km' }
      ];
      groundTicks.forEach(gt => {
        ctx.strokeStyle = '#334155';
        ctx.beginPath(); ctx.moveTo(35, gt.y); ctx.lineTo(45, gt.y); ctx.stroke();
        ctx.fillStyle = '#64748b';
        ctx.font = '8px Space Mono';
        ctx.textAlign = 'left';
        ctx.fillText(gt.label, 50, gt.y + 3);
      });
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 8.5px Noto Sans KR';
      ctx.textAlign = 'left';
      ctx.fillText('🏛️ 고정 좌표계', 48, 16);
    } else {
      // 로켓계: 로켓 기준 동적 고도 표시
      for (let y = 20; y <= H - 20; y += 45) {
        ctx.strokeStyle = '#334155';
        ctx.beginPath(); ctx.moveTo(35, y); ctx.lineTo(45, y); ctx.stroke();
      }
      ctx.fillStyle = '#64748b';
      ctx.font = '8px Space Mono';
      ctx.textAlign = 'left';
      ctx.fillText(`고도 ${(s.altKm).toFixed(1)} km`, 50, H - 15);
      ctx.fillText('상승 방향 (↑)', 50, 25);
    }

    // 4. 배기가스 방출 덩어리 및 파티클
    s.particles.forEach(p => {
      ctx.save();
      ctx.globalAlpha = Math.max(0, p.life);
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

    if (s.gasAlpha > 0) {
      const gx = s.rocketX;
      const gy = s.gasPosY;

      ctx.save();
      ctx.globalAlpha = s.gasAlpha;

      // 가스 덩어리 외부 구름
      const gasGrad = ctx.createRadialGradient(gx, gy, 4, gx, gy, 22);
      gasGrad.addColorStop(0, '#f97316');
      gasGrad.addColorStop(0.5, '#ea580c');
      gasGrad.addColorStop(1, 'rgba(194, 65, 12, 0)');
      ctx.fillStyle = gasGrad;
      ctx.beginPath();
      ctx.arc(gx, gy, 22, 0, Math.PI * 2);
      ctx.fill();

      // 가스 본체 원 (교과서 갈색 원 Δm)
      ctx.fillStyle = '#c2410c';
      ctx.strokeStyle = '#fdba74';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(gx, gy, 9.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#fed7aa';
      ctx.font = 'bold 9.5px Space Mono';
      ctx.textAlign = 'left';
      ctx.fillText(`Δm = ${deltaM}kg`, gx + 15, gy + 3);

      // 배기가스 속도 벡터 화살표
      if (showVelVec) {
        if (frameView === 'ground') {
          // 외부 정지 관측자 시점: 속도 V - u
          const gvLen = Math.max(14, Math.min(65, Math.abs(gasGroundVel) / 35));
          if (gasGroundVel < 0) {
            // 아래쪽 방향 (배기가스가 지표면 기준 후진)
            drawVecArrow(ctx, gx - 14, gy, gx - 14, gy + gvLen, '#fb923c', `V - u = ${gasGroundVel.toFixed(0)}m/s (↓)`, -68, 4);
          } else {
            // 위쪽 방향 (로켓 초기속도가 너무 커서 가스도 앞으로 전진하지만 로켓보다 느림)
            drawVecArrow(ctx, gx - 14, gy, gx - 14, gy - gvLen, '#fb923c', `V - u = +${gasGroundVel.toFixed(0)}m/s (↑)`, -68, -4);
          }
        } else {
          // 로켓 탑승자 시점: 속도 -u (항상 아래쪽 ↓)
          const uLen = Math.min(70, relU / 35);
          drawVecArrow(ctx, gx - 14, gy, gx - 14, gy + uLen, '#fb923c', `-u = -${relU.toLocaleString()}m/s (↓)`, -68, 4);
        }
      }

      ctx.restore();
    }

    // 5. 로켓 본체 그리기
    const rx = s.rocketX;
    const ry = s.rocketY;
    const rw = 40;
    const rh = 72;

    // (1) 추진 화염 (방출 중일 때)
    if (s.state === 'ejecting') {
      const fH = 35 + Math.random() * 18;
      const fGrad = ctx.createLinearGradient(rx, ry + rh / 2, rx, ry + rh / 2 + fH);
      fGrad.addColorStop(0, '#ffffff');
      fGrad.addColorStop(0.3, '#38bdf8');
      fGrad.addColorStop(0.6, '#f97316');
      fGrad.addColorStop(1, 'rgba(239, 68, 68, 0)');
      ctx.fillStyle = fGrad;
      ctx.beginPath();
      ctx.moveTo(rx - 10, ry + rh / 2 + 4);
      ctx.quadraticCurveTo(rx, ry + rh / 2 + fH, rx + 10, ry + rh / 2 + 4);
      ctx.closePath();
      ctx.fill();
    }

    // (2) 로켓 측면 핀 (붉은 날개)
    ctx.fillStyle = '#dc2626';
    ctx.strokeStyle = '#991b1b';
    ctx.lineWidth = 1;
    // 좌측 핀
    ctx.beginPath();
    ctx.moveTo(rx - rw / 2, ry + 10);
    ctx.quadraticCurveTo(rx - rw / 2 - 18, ry + rh / 2 + 4, rx - rw / 2 - 14, ry + rh / 2 + 10);
    ctx.lineTo(rx - rw / 2 + 4, ry + rh / 2);
    ctx.closePath();
    ctx.fill(); ctx.stroke();
    // 우측 핀
    ctx.beginPath();
    ctx.moveTo(rx + rw / 2, ry + 10);
    ctx.quadraticCurveTo(rx + rw / 2 + 18, ry + rh / 2 + 4, rx + rw / 2 + 14, ry + rh / 2 + 10);
    ctx.lineTo(rx + rw / 2 - 4, ry + rh / 2);
    ctx.closePath();
    ctx.fill(); ctx.stroke();

    // (3) 로켓 엔진 노즐
    ctx.fillStyle = '#334155';
    ctx.fillRect(rx - 10, ry + rh / 2, 20, 6);
    ctx.fillStyle = '#1e293b';
    ctx.beginPath();
    ctx.moveTo(rx - 12, ry + rh / 2 + 6);
    ctx.lineTo(rx + 12, ry + rh / 2 + 6);
    ctx.lineTo(rx + 8, ry + rh / 2);
    ctx.lineTo(rx - 8, ry + rh / 2);
    ctx.closePath();
    ctx.fill();

    // (4) 로켓 원통 몸체 (메탈릭 그레이)
    const bGrad = ctx.createLinearGradient(rx - rw / 2, 0, rx + rw / 2, 0);
    bGrad.addColorStop(0, '#94a3b8');
    bGrad.addColorStop(0.35, '#e2e8f0');
    bGrad.addColorStop(0.7, '#cbd5e1');
    bGrad.addColorStop(1, '#64748b');
    ctx.fillStyle = bGrad;
    ctx.beginPath();
    ctx.roundRect(rx - rw / 2, ry - 14, rw, rh * 0.72, 4);
    ctx.fill();
    ctx.strokeStyle = '#475569';
    ctx.stroke();

    // (5) 노즈콘 (상단 붉은 원뿔)
    const noseGrad = ctx.createLinearGradient(rx - rw / 2, 0, rx + rw / 2, 0);
    noseGrad.addColorStop(0, '#b91c1c');
    noseGrad.addColorStop(0.4, '#ef4444');
    noseGrad.addColorStop(1, '#991b1b');
    ctx.fillStyle = noseGrad;
    ctx.beginPath();
    ctx.moveTo(rx - rw / 2, ry - 14);
    ctx.quadraticCurveTo(rx, ry - rh / 2 - 14, rx + rw / 2, ry - 14);
    ctx.closePath();
    ctx.fill();

    // (6) 원형 포트홀 (블루 렌즈 창)
    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    ctx.arc(rx, ry + 2, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#0284c7';
    ctx.beginPath();
    ctx.arc(rx, ry + 2, 7.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#7dd3fc';
    ctx.beginPath();
    ctx.arc(rx - 2.5, ry - 0.5, 2.5, 0, Math.PI * 2);
    ctx.fill();

    // (7) 동체 질량 텍스트 (실시간 질량 감소 반영)
    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 9px Space Mono';
    ctx.textAlign = 'center';
    const displayMass = Math.round(s.mass);
    ctx.fillText(`${displayMass}kg`, rx, ry + 26);

    // 6. 로켓 속도 및 운동량 벡터 오버레이
    if (showVelVec) {
      const vLen = Math.min(85, Math.max(16, (s.vel / 1200) * 75));
      const vLabel = s.state === 'after' ? `V + Δv = +${s.vel.toFixed(1)}m/s` : `V = +${s.vel.toFixed(1)}m/s`;
      drawVecArrow(ctx, rx + rw / 2 + 8, ry, rx + rw / 2 + 8, ry - vLen, '#38bdf8', vLabel, 60, -4);
    }

    if (showMomVec) {
      const curMom = s.mass * s.vel;
      const pLen = Math.min(85, Math.max(16, (curMom / Math.max(1, P_initial * 1.5)) * 65));
      const pLabel = `P_로켓 = +${Math.round(curMom).toLocaleString()}`;
      drawVecArrow(ctx, rx + rw / 2 + 40, ry, rx + rw / 2 + 40, ry - pLen, '#c084fc', pLabel, 60, -4);
    }

    // 7. 상단 HUD 배너
    let hudText = '';
    let hudColor = '#94a3b8';

    if (frameView === 'ground') {
      if (s.state === 'before') {
        hudText = '🌐 [외부 정지계 관측] 배경: 정지(지표면 고정) | 로켓: 초기 속도 V 로 위로 상승 이동 중';
        hudColor = '#94a3b8';
      } else if (s.state === 'ejecting') {
        hudText = `🔥 [가스 방출 중] 로켓 가속(V+Δv) 솟구침 | 가스: V - u (${gasGroundVel.toFixed(0)}m/s) 로 분리 이동`;
        hudColor = '#fbbf24';
      } else {
        hudText = `🚀 [방출 완료] 배경 고정 | 로켓: +${s.vel.toFixed(1)}m/s 고속 상승 | 가스: ${gasGroundVel.toFixed(0)}m/s 분리 이동`;
        hudColor = '#38bdf8';
      }
    } else {
      if (s.state === 'before') {
        hudText = '🚀 [로켓계 관측] 로켓: 화면 중앙 정지(내 우주선) | 배경: 속도 -V 로 뒤로 스쳐 흐름';
        hudColor = '#94a3b8';
      } else if (s.state === 'ejecting') {
        hudText = `🔥 [가스 방출 중] 배경 흐름 가속 | 배기가스: 로켓 기준 속도 -u (-${relU.toLocaleString()}m/s) 로 후방 분출`;
        hudColor = '#fbbf24';
      } else {
        hudText = `🛸 [가속 순항 중] 로켓: 중앙 정지 | 배경: -(V+Δv) 초고속 하강 | 가스: -u 로 후방 분출 완료`;
        hudColor = '#38bdf8';
      }
    }

    ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
    ctx.strokeStyle = frameView === 'ground' ? '#0ea5e9' : '#a855f7';
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.roundRect(14, 10, 480, 26, 6);
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = hudColor;
    ctx.font = 'bold 9.5px Noto Sans KR';
    ctx.textAlign = 'left';
    ctx.fillText(hudText, 22, 26);

    // 우측: 속도 및 질량 대형 디스플레이
    ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
    ctx.strokeStyle = '#1e3a8a';
    ctx.beginPath();
    ctx.roundRect(W - 250, 10, 236, 44, 6);
    ctx.fill(); ctx.stroke();

    ctx.fillStyle = '#94a3b8';
    ctx.font = '9px Noto Sans KR';
    ctx.fillText('발사체 현재 속도:', W - 240, 25);
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 14px Space Mono';
    ctx.fillText(`+${s.vel.toFixed(1)} m/s`, W - 145, 25);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '9px Noto Sans KR';
    ctx.fillText('발사체 현재 질량:', W - 240, 45);
    ctx.fillStyle = '#f59e0b';
    ctx.font = 'bold 13px Space Mono';
    ctx.fillText(`${s.mass} kg`, W - 145, 45);
  };

  // 🚀 연속 애니메이션 루프 (상시 실행되어 정지계와 로켓계의 배경/로켓 움직임을 실시간 렌더링)
  useEffect(() => {
    const s = simRef.current;
    s.mass = simState === 'after' ? (initMass - deltaM) : initMass;
    s.vel = simState === 'after' ? finalVel : initVel;
    setCurV(s.vel);
    setCurM(s.mass);

    if (frameView === 'rocket') {
      s.rocketY = 135; // 로켓계는 화면 중앙에 고정
    }

    let isRunning = true;

    const mainLoop = (timestamp) => {
      if (!isRunning) return;
      const cvs = canvasRef.current;
      if (!cvs) {
        animRef.current = requestAnimationFrame(mainLoop);
        return;
      }
      const ctx = cvs.getContext('2d');
      const W = cvs.width, H = cvs.height;

      // 1. 방출 단계 애니메이션 진행
      if (s.state === 'ejecting') {
        if (!s.ejectStartTime) s.ejectStartTime = timestamp;
        const elapsed = (timestamp - s.ejectStartTime) / 1000;
        const prog = Math.min(1.0, elapsed / 1.6);
        s.ejectProgress = prog;

        s.mass = +(initMass - deltaM * prog).toFixed(1);
        s.vel = +(initVel + exactDeltaV * prog).toFixed(1);
        setCurV(s.vel);
        setCurM(s.mass);

        // 분출 파티클 생성
        if (prog < 0.9) {
          for (let i = 0; i < 4; i++) {
            s.particles.push({
              x: s.rocketX + (Math.random() - 0.5) * 12,
              y: s.rocketY + 40,
              vx: (Math.random() - 0.5) * 2.5,
              vy: 3 + Math.random() * 5,
              life: 1.0,
              decay: 0.05,
              size: 3 + Math.random() * 4,
              color: Math.random() > 0.4 ? '#f97316' : '#ef4444'
            });
          }
        }

        if (prog >= 1.0) {
          s.state = 'after';
          setSimState('after');
        }
      }

      // 파티클 업데이트
      s.particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.life -= p.decay;
      });
      s.particles = s.particles.filter(p => p.life > 0);

      // 2. 관측 기준계(frameView)에 따른 물리적 위치 계산 (핵심!)
      s.altKm += (s.vel * (1 / 60)) / 1000;

      if (frameView === 'ground') {
        // [외부 정지계 (지표면 관측)]
        // (1) 배경 별들은 완전히 멈춤! (st.y 변경 없음)
        // (2) 로켓이 실제로 위로 물리적 상승!
        const rSpeed = (s.vel / 220);
        s.rocketY -= rSpeed;
        if (s.rocketY < -45) {
          s.rocketY = H + 40; // 화면 위를 벗어나면 아래에서 다시 상승
        }

        // (3) 방출된 배기가스는 지표면 기준 속도 V - u 로 이동!
        if (s.gasAlpha > 0) {
          const gSpeed = (gasGroundVel / 220);
          s.gasPosY -= gSpeed; // gasGroundVel < 0 이면 아래로(Y 증가), > 0 이면 위로
        }
      } else {
        // [로켓계 (우주선 조종사 관측)]
        // (1) 로켓은 화면 중앙에 완벽히 정지!
        s.rocketY = 135;

        // (2) 배경 별들이 로켓의 속도에 비례해 아래로 쏟아져 내림!
        const starSpeed = (s.vel / 110);
        s.stars.forEach(st => {
          st.y = (st.y + starSpeed * st.speedMult) % H;
        });

        // (3) 방출된 배기가스는 로켓에 대해 항상 -u 속도로 아래로 뿜어져 나감!
        if (s.gasAlpha > 0) {
          const uSpeed = (relU / 180);
          s.gasPosY += uSpeed;
        }
      }

      // 3. 렌더링
      drawScene(ctx, W, H, s);

      animRef.current = requestAnimationFrame(mainLoop);
    };

    animRef.current = requestAnimationFrame(mainLoop);
    return () => {
      isRunning = false;
      cancelAnimationFrame(animRef.current);
    };
  }, [initMass, initVel, deltaM, relU, frameView, simState]);

  // 🚀 배기가스 방출 및 가속 트리거
  const triggerEjection = () => {
    const s = simRef.current;
    s.state = 'ejecting';
    s.ejectStartTime = null;
    s.ejectProgress = 0;
    s.mass = initMass;
    s.vel = initVel;
    s.gasPosY = s.rocketY + 45;
    s.gasAlpha = 1.0;
    s.particles = [];
    setSimState('ejecting');
  };

  // 🔄 초기 상태(가)로 리셋
  const resetToBefore = () => {
    const s = simRef.current;
    s.state = 'before';
    s.ejectStartTime = null;
    s.ejectProgress = 0;
    s.mass = initMass;
    s.vel = initVel;
    s.gasAlpha = 0;
    s.particles = [];
    if (frameView === 'ground') {
      s.rocketY = 175; // 정지계는 아래쪽에서 다시 출발
    } else {
      s.rocketY = 135; // 로켓계는 중앙 고정
    }
    setSimState('before');
    setCurV(initVel);
    setCurM(initMass);
  };

  // 관측계 전환 핸들러
  const handleFrameChange = (newFrame) => {
    setFrameView(newFrame);
    const s = simRef.current;
    if (newFrame === 'ground') {
      s.rocketY = 175; // 정지계는 아래쪽에서 출발
    } else {
      s.rocketY = 135; // 로켓계는 중앙 고정
    }
  };

  return (
    <div>
      {/* ── 교과서 단원 연계 배너 ── */}
      <div className="hl-box">
        <h3 style={{color:'#93c5fd',fontSize:15,fontWeight:800,marginBottom:8}}>
          🌌 교과서 단원 연계: 그림 I-24 발사체에서의 운동량 보존 (초기 속도와 질량 감소 모델)
        </h3>
        <p style={{fontSize:13.5,lineHeight:1.8,color:'#e2e8f0'}}>
          발사체가 이미 <b>초기 속도 <Eq f="V"/></b>로 운동하고 있을 때, 배기가스 <Eq f="\Delta m"/>을 상대 속력 <Eq f="u"/>로 분사하면 
          발사체의 질량은 <b><Eq f="M \to M - \Delta m"/></b>으로 감소하고, 속도는 <b><Eq f="V \to V + \Delta v"/></b>로 증가합니다.
          외부 정지계 관측에서 배기가스의 속도가 <b><Eq f="V - u"/></b>가 되는 상대 속도 원리와 <b><Eq f="M\Delta v = u\Delta m"/></b> 유도 과정을 탐구합니다.
        </p>
      </div>

      {/* ── 교과서 그림 I-24 완벽 재현 비교 카드 ── */}
      <div className="card">
        <p style={{fontWeight:800,fontSize:14,color:'#fbbf24',marginBottom:14}}>
          🔍 교과서 그림 I-24 발사체에서의 운동량 보존 상태 비교
        </p>

        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(320px, 1fr))',gap:16}}>
          {/* (가) 방출 전 */}
          <div style={{background:'#0a1020',padding:16,borderRadius:12,border:'1px solid #1e293b'}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:10}}>
              <span style={{fontWeight:700,color:'#38bdf8'}}>🚀 (가) 배기가스 방출 전</span>
              <span className="badge badge-blue">초기 상태</span>
            </div>

            <div style={{display:'flex',alignItems:'center',gap:16,padding:'10px 0'}}>
              <div style={{width:55,height:85,background:'#1e293b',borderRadius:'16px 16px 4px 4px',border:'2px solid #ef4444',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',position:'relative'}}>
                <div style={{width:16,height:16,borderRadius:'50%',background:'#0284c7',marginBottom:4}}/>
                <span style={{fontSize:11,fontWeight:800,color:'#f8fafc',fontFamily:'Space Mono'}}>M</span>
                <span style={{position:'absolute',top:-18,color:'#38bdf8',fontSize:12,fontWeight:800}}>↑ V</span>
              </div>

              <div style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.8}}>
                • <b>발사체 질량:</b> <Eq f="M"/> = {initMass} kg<br/>
                • <b>발사체 속도:</b> <Eq f="V"/> = +{initVel} m/s (위쪽)<br/>
                • <b>전체 초기 운동량:</b><br/>
                <span className="num-mono" style={{color:'#38bdf8',fontWeight:700}}>
                  P_초기 = M · V = +{(P_initial).toLocaleString()} kg·m/s
                </span>
              </div>
            </div>
          </div>

          {/* (나) 방출 후 */}
          <div style={{background:'#0a1020',padding:16,borderRadius:12,border:'1px solid #f97316'}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:10}}>
              <span style={{fontWeight:700,color:'#fb923c'}}>🔥 (나) 배기가스 방출 후</span>
              <span className="badge badge-amber">분출 완료</span>
            </div>

            <div style={{display:'flex',alignItems:'center',gap:16,padding:'10px 0'}}>
              <div style={{display:'flex',flexDirection:'column',alignItems:'center'}}>
                <div style={{width:55,height:85,background:'#1e293b',borderRadius:'16px 16px 4px 4px',border:'2px solid #f97316',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',position:'relative'}}>
                  <div style={{width:16,height:16,borderRadius:'50%',background:'#0284c7',marginBottom:4}}/>
                  <span style={{fontSize:10,fontWeight:800,color:'#f8fafc',fontFamily:'Space Mono'}}>M-Δm</span>
                  <span style={{position:'absolute',top:-18,color:'#38bdf8',fontSize:12,fontWeight:800}}>↑ V+Δv</span>
                </div>
                <div style={{width:18,height:18,borderRadius:'50%',background:'#c2410c',marginTop:6,display:'flex',alignItems:'center',justifyContent:'center',fontSize:8,fontWeight:800,color:'#fed7aa'}}>
                  Δm
                </div>
                <span style={{fontSize:10,color:'#fb923c',fontWeight:700}}>↓ V-u</span>
              </div>

              <div style={{fontSize:12,color:'#cbd5e1',lineHeight:1.7}}>
                • <b>가벼워진 발사체:</b> 질량 <Eq f="M - \Delta m"/> ({initMass - deltaM} kg), 속도 <Eq f="V + \Delta v"/> (+{finalVel.toFixed(1)} m/s)<br/>
                • <b>방출된 배기가스:</b> 질량 <Eq f="\Delta m"/> ({deltaM} kg), 속도 <Eq f="V - u"/> ({gasGroundVel.toFixed(1)} m/s)<br/>
                • <b>전체 나중 운동량 합:</b><br/>
                <span className="num-mono" style={{color:'#a3e635',fontWeight:700}}>
                  P_나중 = (M-Δm)(V+Δv) + Δm(V-u) = +{(Math.round(P_total_after)).toLocaleString()} kg·m/s
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ── 인터랙티브 수직 상승 시뮬레이터 ── */}
      <div className="card">
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:12,flexWrap:'wrap',gap:8}}>
          <div>
            <span style={{fontWeight:800,fontSize:15,color:'#f8fafc'}}>
              🚀 [수직 비행 시뮬레이터] 초기 속도 상태에서의 가스 방출 및 속도 증가
            </span>
          </div>

          {/* 관측계 및 벡터 토글 */}
          <div style={{display:'flex',gap:14,fontSize:12,flexWrap:'wrap',alignItems:'center'}}>
            <div style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:'#94a3b8',fontWeight:700}}>관측 기준계:</span>
              <button className={`btn-secondary ${frameView==='ground'?'active':''}`} onClick={()=>handleFrameChange('ground')}
                style={{padding:'5px 12px',fontSize:12,fontWeight:700,background:frameView==='ground'?'#0284c7':'#1e293b',color:frameView==='ground'?'#fff':'#94a3b8',border:frameView==='ground'?'1px solid #38bdf8':'1px solid #334155'}}>
                🌐 정지계 (배경 정지, 로켓 상승)
              </button>
              <button className={`btn-secondary ${frameView==='rocket'?'active':''}`} onClick={()=>handleFrameChange('rocket')}
                style={{padding:'5px 12px',fontSize:12,fontWeight:700,background:frameView==='rocket'?'#7c3aed':'#1e293b',color:frameView==='rocket'?'#fff':'#94a3b8',border:frameView==='rocket'?'1px solid #c084fc':'1px solid #334155'}}>
                🚀 로켓계 (로켓 정지, 배경 흐름)
              </button>
            </div>

            <label style={{display:'flex',alignItems:'center',gap:4,cursor:'pointer',color:'#38bdf8'}}>
              <input type="checkbox" checked={showVelVec} onChange={e=>setShowVelVec(e.target.checked)}/>
              속도 벡터 (<span style={{fontFamily:'Space Mono'}}>v, V</span>)
            </label>
            <label style={{display:'flex',alignItems:'center',gap:4,cursor:'pointer',color:'#c084fc'}}>
              <input type="checkbox" checked={showMomVec} onChange={e=>setShowMomVec(e.target.checked)}/>
              운동량 벡터 (<span style={{fontFamily:'Space Mono'}}>P</span>)
            </label>
          </div>
        </div>

        {/* 관측계 모드 친절 안내 박스 */}
        <div style={{marginBottom:10,padding:'8px 14px',borderRadius:8,fontSize:12,background:frameView==='ground'?'rgba(2,132,199,0.12)':'rgba(124,58,237,0.12)',border:frameView==='ground'?'1px solid rgba(2,132,199,0.35)':'1px solid rgba(124,58,237,0.35)',color:frameView==='ground'?'#7dd3fc':'#d8b4fe'}}>
          {frameView === 'ground' ? (
            <span>💡 <b>외부 정지계 (지표면 관측):</b> 관측자가 멈춰 있으므로 <b>배경(별·좌표계)은 정지</b>해 있고, <b>로켓이 실제로 화면 위로 상승</b>하며, 분출된 가스는 지표면 기준 속도 <b>V - u</b>로 분리 이동합니다.</span>
          ) : (
            <span>💡 <b>로켓계 (우주선 조종사 관측):</b> 관측자가 로켓에 타고 있으므로 <b>로켓은 화면 중앙에 정지(내 우주선)</b>해 있고, <b>배경 별들이 뒤로 스쳐 지나가며</b>, 가스는 로켓 기준 상대 속도 <b>-u</b>로 후방 분출됩니다.</span>
          )}
        </div>

        {/* ── 캔버스 ── */}
        <canvas ref={canvasRef} width={800} height={250}
          style={{width:'100%',borderRadius:12,border:'1px solid #1e293b',background:'#020617',display:'block',boxShadow:'0 4px 20px rgba(0,0,0,0.6)',marginBottom:16}} />

        {/* ── 조절 슬라이더 ── */}
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(220px, 1fr))',gap:14,marginBottom:16}}>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>초기 전체 질량 (M)</label>
            <input type="range" min="600" max="2000" step="50" value={initMass} onChange={e=>setInitMass(+e.target.value)} disabled={simState==='ejecting'} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#60a5fa',fontFamily:'Space Mono'}}>
              <span>600 kg</span><span>{initMass} kg</span><span>2000 kg</span>
            </div>
          </div>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>초기 비행 속력 (V)</label>
            <input type="range" min="100" max="1000" step="50" value={initVel} onChange={e=>setInitVel(+e.target.value)} disabled={simState==='ejecting'} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#38bdf8',fontFamily:'Space Mono'}}>
              <span>100 m/s</span><span>{initVel} m/s</span><span>1,000 m/s</span>
            </div>
          </div>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>방출 가스 질량 (Δm)</label>
            <input type="range" min="20" max="250" step="10" value={deltaM} onChange={e=>setDeltaM(+e.target.value)} disabled={simState==='ejecting'} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#f59e0b',fontFamily:'Space Mono'}}>
              <span>20 kg</span><span>{deltaM} kg</span><span>250 kg</span>
            </div>
          </div>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>상대 분사 속력 (u)</label>
            <input type="range" min="1000" max="3500" step="100" value={relU} onChange={e=>setRelU(+e.target.value)} disabled={simState==='ejecting'} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#86efac',fontFamily:'Space Mono'}}>
              <span>1,000 m/s</span><span>{relU.toLocaleString()} m/s</span><span>3,500 m/s</span>
            </div>
          </div>
        </div>

        {/* ── 결과 박스 & 제어 버튼 ── */}
        <div style={{background:'#0a1224',padding:16,borderRadius:12,border:'1px solid #1e3a8a',display:'flex',justifyContent:'space-between',alignItems:'center',flexWrap:'wrap',gap:14}}>
          <div>
            <p style={{fontSize:12,color:'#94a3b8',marginBottom:4}}>
              속도 증가량 (교과서 근사 <Eq f="\Delta v \approx u\frac{\Delta m}{M}"/>):
            </p>
            <div style={{display:'flex',alignItems:'baseline',gap:8}}>
              <span className="num-mono" style={{fontSize:28,fontWeight:800,color:'#38bdf8'}}>
                +{exactDeltaV.toFixed(1)}
              </span>
              <span style={{fontSize:14,color:'#93c5fd',fontWeight:700}}>m/s</span>
              <span style={{fontSize:12,color:'#64748b'}}>
                (근사값: +{approxDeltaV.toFixed(1)} m/s, 오차 {((Math.abs(exactDeltaV - approxDeltaV)/exactDeltaV)*100).toFixed(1)}%)
              </span>
            </div>
            <p style={{fontSize:11.5,color:'#94a3b8',marginTop:4}}>
              최종 속도: {initVel} m/s → <b style={{color:'#a3e635'}}>+{finalVel.toFixed(1)} m/s</b> | 배기가스 속도(정지계): <b style={{color:'#f97316'}}>{gasGroundVel.toFixed(1)} m/s</b>
            </p>
          </div>

          <div style={{display:'flex',gap:10,alignItems:'center'}}>
            <button className="btn-secondary" onClick={resetToBefore} disabled={simState==='ejecting'}
              style={{padding:'12px 18px',fontSize:13}}>
              🔄 (가) 상태로 리셋
            </button>
            <button className="btn-success" onClick={triggerEjection} disabled={simState==='ejecting'}
              style={{padding:'12px 26px',fontSize:14,boxShadow:'0 0 18px rgba(22,163,74,0.45)'}}>
              {simState==='ejecting' ? '🔥 가스 방출 가속 중...' : '🚀 배기가스 방출 시험! (가 → 나)'}
            </button>
          </div>
        </div>

        {/* ── 교과서 수식 증명 및 유도 전개 카드 ── */}
        <div style={{marginTop:16,background:'rgba(15,23,42,0.85)',padding:16,borderRadius:12,border:'1px solid #334155'}}>
          <p style={{fontWeight:800,fontSize:14,color:'#fbbf24',marginBottom:10}}>
            📐 교과서 그림 I-24 수식 증명 및 <Eq f="M \Delta v = u \Delta m"/>의 물리적 의미
          </p>

          <div style={{fontSize:12.8,color:'#e2e8f0',lineHeight:1.9,background:'#0a1020',padding:14,borderRadius:10,border:'1px solid #1e293b',marginBottom:12}}>
            <p><b>1. 운동량 보존 법칙 적용:</b></p>
            <p style={{paddingLeft:16}}>
              <Eq f="M V = (M - \Delta m)(V + \Delta v) + \Delta m (V - u)" display={true}/>
            </p>
            <p style={{marginTop:6}}><b>2. 우변 전개:</b></p>
            <p style={{paddingLeft:16}}>
              <Eq f="M V = M V + M \Delta v - \Delta m V - \Delta m \Delta v + \Delta m V - u \Delta m" display={true}/>
            </p>
            <p style={{marginTop:6}}><b>3. 양변의 <Eq f="M V"/> 및 <Eq f="\Delta m V"/> 상쇄:</b></p>
            <p style={{paddingLeft:16}}>
              <Eq f="0 = M \Delta v - \Delta m \Delta v - u \Delta m \implies M \Delta v = u \Delta m + \Delta m \Delta v" display={true}/>
            </p>
            <p style={{marginTop:6}}><b>4. 교과서의 핵심 근사 (<Eq f="\Delta m \Delta v \approx 0"/>):</b></p>
            <p style={{paddingLeft:16}}>
              <Eq f="\Delta m \Delta v"/>는 두 미소 변화량의 곱이므로 다른 항들에 비해 매우 작아 무시할 수 있습니다.<br/>
              현재 실험값에서: <Eq f="u \Delta m"/> = {(term_udm).toLocaleString()} N·s vs <Eq f="\Delta m \Delta v"/> = {(term_dmdv).toFixed(0)} N·s (비율: {((term_dmdv/term_udm)*100).toFixed(1)}%)<br/>
              따라서 최종적으로 다음 관계가 성립합니다:
            </p>
            <p style={{paddingLeft:16,fontSize:15,fontWeight:800,color:'#38bdf8',marginTop:4}}>
              <Eq f="M \Delta v = u \Delta m \iff \Delta v = u \frac{\Delta m}{M}" display={true}/>
            </p>
          </div>

          <p style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.8}}>
            💡 <b>교과서 결론:</b> 발사체에서 분사하는 <b>배기가스의 질량 <Eq f="\Delta m"/>이 크고 그 속력 <Eq f="u"/>가 빠를수록</b> 발사체의 
            속도 증가량 <Eq f="\Delta v"/>가 더 커집니다. 또한 이를 미소 시간 <Eq f="dt"/>에 대해 연속적으로 적분하면 현대 우주 로켓의 근간인 
            <b>치올콥스키 로켓 방정식</b> <Eq f="\Delta V = u \ln\left(\frac{M_{\text{초기}}}{M_{\text{최종}}}\right)"/>으로 자연스럽게 확장됩니다!
          </p>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 3: 교과서 탐구 보고서 & 문제 풀이
══════════════════════════════════════════════════ */
function ReportTab() {
  const [ans1, setAns1] = useState('');
  const [ans2, setAns2] = useState('');
  const [showModelAns, setShowModelAns] = useState(false);

  return (
    <div>
      {/* ── 타이틀 카드 ── */}
      <div className="card">
        <h3 style={{fontSize:16,fontWeight:800,color:'#f8fafc',marginBottom:6}}>
          📝 교과서 탐구 활동 보고서 및 생각하기 문제 풀이
        </h3>
        <p style={{fontSize:13,color:'#94a3b8',lineHeight:1.7}}>
          교과서 [디지털 해보기] 학습지의 탐구 결과 질문에 대해 고등학교 물리학 및 역학과 에너지 성취기준에 맞춘 체계적인 풀이와 모범 답안을 확인합니다.
        </p>
      </div>

      {/* ── 탐구 질문 1 ── */}
      <div className="card" style={{borderLeft:'4px solid #84cc16'}}>
        <div style={{display:'flex',gap:8,alignItems:'center',marginBottom:8}}>
          <span className="badge badge-lime">탐구 질문 1</span>
          <span style={{fontWeight:800,color:'#f8fafc',fontSize:14}}>
            두 수레가 분리된 뒤 각 수레의 운동량을 비교해 보자.
          </span>
        </div>

        <div style={{background:'#0a1020',padding:14,borderRadius:10,border:'1px solid #1e293b',marginBottom:12}}>
          <p style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.8}}>
            • <b>실험 조건:</b> 빈 수레 A (질량 m = 0.50 kg), 추를 2개 올린 수레 B (질량 M = 1.00 kg)<br/>
            • <b>실험 측정값 예시:</b> 수레 A 속도 v_A = -0.98 m/s, 수레 B 속도 v_B = +0.49 m/s
          </p>
        </div>

        {/* 모범 답안 박스 */}
        <div style={{background:'rgba(132,204,22,0.08)',padding:16,borderRadius:10,border:'1px solid rgba(132,204,22,0.3)',lineHeight:1.8,fontSize:13}}>
          <p style={{fontWeight:800,color:'#a3e635',marginBottom:6}}>💡 고등학교 수준 단계별 모범 답안</p>
          
          <p>
            <b>1. 각 수레의 운동량 계산:</b><br/>
            - 수레 A (빈 수레): <Eq f="p_A = m_A \cdot v_A = 0.50\,\text{kg} \times (-0.98\,\text{m/s}) = -0.49\,\text{kg}\cdot\text{m/s}"/><br/>
            - 수레 B (추 2개): <Eq f="p_B = m_B \cdot v_B = 1.00\,\text{kg} \times (+0.49\,\text{m/s}) = +0.49\,\text{kg}\cdot\text{m/s}"/>
          </p>
          <p style={{marginTop:8}}>
            <b>2. 운동량의 크기와 방향 비교:</b><br/>
            - <b>크기:</b> 두 수레의 운동량의 크기는 <Eq f="|p_A| = |p_B| = 0.49\,\text{kg}\cdot\text{m/s}"/>로 서로 <b>같습니다</b>.<br/>
            - <b>방향:</b> 두 수레는 서로 <b>반대 방향</b>으로 운동합니다.
          </p>
          <p style={{marginTop:8}}>
            <b>3. 결론 (운동량 보존 법칙):</b><br/>
            두 수레의 운동량의 합은 <Eq f="p_A + p_B = -0.49 + 0.49 = 0"/>입니다. 이는 두 수레가 분리되기 전 정지해 있을 때의 전체 운동량(0)과 동일하며, 
            외력이 작용하지 않는 계에서 <b>전체 운동량이 일정하게 보존됨</b>을 증명합니다.
          </p>
        </div>
      </div>

      {/* ── 탐구 질문 2 ── */}
      <div className="card" style={{borderLeft:'4px solid #0ea5e9'}}>
        <div style={{display:'flex',gap:8,alignItems:'center',marginBottom:8}}>
          <span className="badge badge-blue">탐구 질문 2</span>
          <span style={{fontWeight:800,color:'#f8fafc',fontSize:14}}>
            위 실험 결과를 통해 발사체에 운동량 보존 원리를 어떻게 적용해 발사체를 목표 궤도까지 올릴 수 있을지 설명해 보자.
          </span>
        </div>

        {/* 모범 답안 박스 */}
        <div style={{background:'rgba(14,165,233,0.08)',padding:16,borderRadius:10,border:'1px solid rgba(14,165,233,0.3)',lineHeight:1.8,fontSize:13}}>
          <p style={{fontWeight:800,color:'#38bdf8',marginBottom:6}}>💡 고등학교 수준 단계별 모범 답안</p>

          <p>
            <b>1. 발사체(로켓)의 추진 메커니즘과 운동량 보존:</b><br/>
            발사체는 연료가 연소하면서 발생한 고온·고압의 배기가스를 고속으로 뒤쪽(- 방향)으로 분출합니다. 
            외력이 없는 계에서 발사체와 배기가스로 이루어진 전체 계의 운동량은 보존되므로, 배기가스가 얻은 운동량만큼 발사체 본체는 반대 방향(+ 방향, 앞쪽)으로 동일한 크기의 운동량을 얻어 가속됩니다 (<Eq f="M\vec{V} + m\vec{v} = 0 \implies \vec{V} = -\frac{m}{M}\vec{v}"/>).
          </p>

          <p style={{marginTop:8}}>
            <b>2. 목표 궤도 진입을 위한 구체적인 적용 방안:</b><br/>
            지구 주위를 도는 원 궤도에 진입하려면 제1우주속도인 <b>약 7.9 km/s 이상의 초고속</b>이 필요합니다. 이를 달성하기 위해 다음 두 가지 원리를 적용합니다.
          </p>

          <ul style={{paddingLeft:20,marginTop:4}}>
            <li>
              <b>방안 1: 배기가스의 분출 속도(v) 극대화</b><br/>
              공식에서 분출 속도 v가 클수록 발사체가 얻는 추진 속도 V가 비례하여 증가합니다. 따라서 초고효율 로켓 엔진(터보 펌프와 노즐)을 설계하여 가스를 초음속으로 뿜어냅니다.
            </li>
            <li>
              <b>방안 2: 다단계 로켓 분리를 통한 본체 질량(M)의 극적인 감소</b><br/>
              발사체의 가속도 및 속도 증가는 본체 질량 M에 반비례합니다. 
              수레 실험에서 가벼운 수레가 훨씬 더 빠른 속도로 튀어나가듯, 로켓도 연료를 다 쓴 1단과 2단의 무거운 빈 탱크를 차례로 분리하여 버림으로써 본체 질량 M을 대폭 줄여야 목표 궤도까지 충분한 가속도를 얻을 수 있습니다.
            </li>
          </ul>

          <p style={{marginTop:8,color:'#94a3b8',fontSize:12}}>
            * 연계 개념: 러시아의 과학자 콘스탄틴 치올콥스키의 로켓 방정식 <Eq f="\Delta V = v_{\text{배기}} \ln\left(\frac{M_{\text{초기}}}{M_{\text{최종}}}\right)"/>
          </p>
        </div>
      </div>

    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
</script>
</body>
</html>"""

components.html(REACT_HTML, height=1150, scrolling=True)
