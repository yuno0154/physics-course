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
  const [activeTab, setActiveTab] = useState('sim'); // sim | rocket | report

  return (
    <div>
      {/* 탭 네비게이션 */}
      <div className="tab-bar">
        <button className={`tab-btn ${activeTab==='sim'?'active':''}`} onClick={()=>setActiveTab('sim')}>
          🛒 [디지털 해보기] MBL 무선 수레 실험
        </button>
        <button className={`tab-btn ${activeTab==='rocket'?'active':''}`} onClick={()=>setActiveTab('rocket')}>
          🚀 [원리 탐구] 발사체 추진과 운동량 보존
        </button>
        <button className={`tab-btn ${activeTab==='report'?'active':''}`} onClick={()=>setActiveTab('report')}>
          📝 [탐구 보고서] 실험 데이터 & 문제 풀이
        </button>
      </div>

      {activeTab === 'sim' && <CartSimTab />}
      {activeTab === 'rocket' && <RocketPrincipleTab />}
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
  
  const [isFiring, setIsFiring] = useState(false);
  const [vRocket, setVRocket] = useState(0);

  // 로켓 획득 속도: V = (m_gas / M_rocket) * v_gas
  const theoryV = (gasMass / rocketMass) * gasVel;

  const triggerRocketLaunch = () => {
    setIsFiring(true);
    setVRocket(0);
    let progress = 0;
    const interval = setInterval(() => {
      progress += 0.05;
      setVRocket(+(theoryV * Math.min(1, progress)).toFixed(1));
      if (progress >= 1.0) {
        clearInterval(interval);
        setTimeout(() => setIsFiring(false), 800);
      }
    }, 40);
  };

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
            
            {/* SVG 모식도 */}
            <svg width="100%" height="80" viewBox="0 0 320 80">
              {/* 레일 */}
              <line x1="20" y1="65" x2="300" y2="65" stroke="#475569" strokeWidth="3"/>
              {/* 수레 A (배기가스 역할) */}
              <rect x="50" y="25" width="70" height="32" rx="4" fill="#65a30d" stroke="#84cc16"/>
              <text x="85" y="45" fill="#fff" fontSize="11" textAnchor="middle" fontWeight="bold">수레 A (m)</text>
              <circle cx="65" cy="60" r="5" fill="#1e293b"/>
              <circle cx="105" cy="60" r="5" fill="#1e293b"/>
              {/* 수레 B (로켓 본체 역할) */}
              <rect x="180" y="25" width="90" height="32" rx="4" fill="#0284c7" stroke="#0ea5e9"/>
              <text x="225" y="45" fill="#fff" fontSize="11" textAnchor="middle" fontWeight="bold">수레 B (M)</text>
              <circle cx="200" cy="60" r="5" fill="#1e293b"/>
              <circle cx="250" cy="60" r="5" fill="#1e293b"/>
              {/* 용수철 */}
              <path d="M 120 41 Q 128 32, 135 41 T 150 41 T 165 41 T 180 41" fill="none" stroke="#f59e0b" strokeWidth="2.5"/>
              {/* 힘 화살표 */}
              <line x1="110" y1="14" x2="60" y2="14" stroke="#f97316" strokeWidth="2" markerEnd="url(#arrow)"/>
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

            {/* SVG 로켓 모식도 */}
            <svg width="100%" height="80" viewBox="0 0 320 80">
              {/* 배기가스 분출 */}
              <ellipse cx="60" cy="40" rx="35" ry="12" fill="rgba(249,115,22,0.4)"/>
              <polygon points="40,36 20,28 35,40 20,52 40,44" fill="#ef4444"/>
              <text x="60" y="44" fill="#fdba74" fontSize="10" textAnchor="middle" fontWeight="bold">가스 (m, v)</text>
              {/* 로켓 본체 */}
              <rect x="100" y="24" width="110" height="32" rx="4" fill="#334155" stroke="#94a3b8"/>
              <polygon points="210,24 240,40 210,56" fill="#e2e8f0"/>
              <text x="155" y="44" fill="#fff" fontSize="11" textAnchor="middle" fontWeight="bold">로켓 본체 (M, V)</text>
              {/* 추진 방향 화살표 */}
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
        <p style={{fontWeight:800,fontSize:14,color:'#f8fafc',marginBottom:12}}>
          🎛️ 발사체 운동량 보존 시뮬레이터 (질량비와 가스 속도 조절)
        </p>

        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(220px, 1fr))',gap:14,marginBottom:16}}>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>로켓 본체 질량 (M)</label>
            <input type="range" min="400" max="1500" step="50" value={rocketMass} onChange={e=>setRocketMass(+e.target.value)} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#60a5fa',fontFamily:'Space Mono'}}>
              <span>400 kg</span><span>{rocketMass} kg</span><span>1500 kg</span>
            </div>
          </div>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>분출 가스 질량 (m)</label>
            <input type="range" min="50" max="400" step="25" value={gasMass} onChange={e=>setGasMass(+e.target.value)} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#f59e0b',fontFamily:'Space Mono'}}>
              <span>50 kg</span><span>{gasMass} kg</span><span>400 kg</span>
            </div>
          </div>
          <div>
            <label style={{fontSize:11.5,color:'#94a3b8',display:'block',marginBottom:4}}>배기가스 분출 속력 (v)</label>
            <input type="range" min="1000" max="4000" step="200" value={gasVel} onChange={e=>setGasVel(+e.target.value)} style={{width:'100%'}}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#86efac',fontFamily:'Space Mono'}}>
              <span>1,000 m/s</span><span>{gasVel.toLocaleString()} m/s</span><span>4,000 m/s</span>
            </div>
          </div>
        </div>

        {/* 결과 박스 */}
        <div style={{background:'#0a1224',padding:16,borderRadius:12,border:'1px solid #1e3a8a',display:'flex',justifyContent:'space-between',alignItems:'center',flexWrap:'wrap',gap:14}}>
          <div>
            <p style={{fontSize:12,color:'#94a3b8',marginBottom:4}}>로켓이 얻는 속도 증가량 (ΔV):</p>
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

          <div style={{textAlign:'right'}}>
            <button className="btn-success" onClick={triggerRocketLaunch} disabled={isFiring}
              style={{padding:'12px 24px',fontSize:14,boxShadow:'0 0 16px rgba(22,163,74,0.4)'}}>
              {isFiring ? '🔥 가스 분출 가속 중...' : '🚀 연료 분출 발사 시험!'}
            </button>
          </div>
        </div>

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

components.html(REACT_HTML, height=980, scrolling=True)
