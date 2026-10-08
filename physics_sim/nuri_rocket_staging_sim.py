import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="누리호 5차 발사와 다단·페어링 분리 시뮬레이션",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 누리호 다단·페어링 분리 탐구")
st.sidebar.markdown(r"""
**2022 개정 교육과정 역학과 에너지**  
[12역학01-02] 운동량 보존 법칙 및 [12역학01-05] 로켓 추진과 다단 분리 원리

**누리호 5차 발사(KSLV-II)** 사례를 바탕으로:
1. **페어링(Fairing) 분리 이유** (대기권 탈출 후 사중량 제거)
2. **1단·2단 로켓 분리 이유** (빈 연료탱크 질량 감축과 $\Delta v$ 증대)
3. **운동량 보존 법칙과 찌올콥스키 로켓 방정식**의 정량적 연결
을 가상 시뮬레이션으로 비교 체험합니다.

---
🎬 **[관련 영상]**  
• [누리호 5차 발사 영상 (YouTube)](https://youtu.be/YeM0G_BEBzY)
""")

# 유튜브 영상 플레이어 상단 배치 (펼치기 가능)
with st.expander("📺 🎬 [실황 영상] 누리호 5차 발사 및 다단·페어링 분리 생중계 영상 (YouTube)", expanded=False):
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        st.video("https://youtu.be/YeM0G_BEBzY")
    with col_v2:
        st.markdown("""
        ### 📌 영상 관전 포인트
        * **125초 경과 (고도 59km)**: 1단 로켓 분리 및 2단 엔진 점화
        * **204초 경과 (고도 191km)**: 페어링(위성 보호 커버) 2개 분리
        * **255초 경과 (고도 258km)**: 2단 로켓 분리 및 3단 엔진 점화
        * **755초 경과 (고도 700km)**: 7.5 km/s 궤도 속도 달성 후 위성 분리
        """)

REACT_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#070b14;color:#e2e8f0;padding:14px;overflow-x:hidden;}
.tab-bar{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;}
.tab-btn{padding:10px 18px;border-radius:10px;border:1px solid #1e293b;background:#0f172a;
  color:#94a3b8;cursor:pointer;font-size:13.5px;font-weight:700;font-family:inherit;transition:all 0.2s;}
.tab-btn.active{background:#2563eb;border-color:#3b82f6;color:#fff;box-shadow:0 0 14px rgba(37,99,235,0.4);}
.tab-btn:hover:not(.active){border-color:#475569;color:#e2e8f0;}
.card{background:#0b132b;border:1px solid #1e293b;border-radius:14px;padding:18px;margin-bottom:14px;}
.hl-box{background:linear-gradient(135deg,#0c1d4a,#0e2660);border:1px solid #2563eb;border-radius:12px;padding:16px;margin-bottom:14px;}
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
.badge-red{background:rgba(239,68,68,0.15);color:#fca5a5;border:1px solid rgba(239,68,68,0.4);}
.table-custom{width:100%;border-collapse:collapse;font-size:12.5px;}
.table-custom th{background:#080e1e;color:#94a3b8;padding:8px 10px;border:1px solid #1e293b;text-align:center;font-weight:700;}
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
  const [activeTab, setActiveTab] = useState('sim'); // sim | graph | math | report

  return (
    <div>
      {/* 상단 타이틀 배너 */}
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:14,flexWrap:'wrap',gap:10}}>
        <div>
          <div style={{display:'flex',alignItems:'center',gap:8}}>
            <span style={{fontSize:22}}>🚀</span>
            <h2 style={{fontSize:19,fontWeight:800,color:'#f8fafc'}}>
              누리호 5차 발사 기반 다단 로켓 & 페어링 분리 가상실험
            </h2>
            <span className="badge badge-lime">역학과 에너지 [12역학01-02/05]</span>
          </div>
          <p style={{fontSize:12.5,color:'#94a3b8',marginTop:4}}>
            운동량 보존 법칙과 질량 감축($\Delta v = v_e \ln(m_0/m_f)$) 원리로 왜 페어링과 1단·2단을 분리해야 하는지 탐구합니다.
          </p>
        </div>

        <div style={{display:'flex',gap:8,alignItems:'center'}}>
          <a href="https://youtu.be/YeM0G_BEBzY" target="_blank" rel="noreferrer" style={{textDecoration:'none'}}>
            <button className="btn-danger" style={{display:'flex',alignItems:'center',gap:6,boxShadow:'0 0 12px rgba(220,38,38,0.4)',padding:'9px 15px',fontSize:12.5}}>
              <span>▶️</span> 누리호 5차 발사 영상 (YouTube)
            </button>
          </a>
        </div>
      </div>

      {/* 탭 네비게이션 */}
      <div className="tab-bar">
        <button className={`tab-btn ${activeTab==='sim'?'active':''}`} onClick={()=>setActiveTab('sim')}>
          🎬 [시뮬레이션] 누리호 5차 발사 & 3가지 모드 비교
        </button>
        <button className={`tab-btn ${activeTab==='graph'?'active':''}`} onClick={()=>setActiveTab('graph')}>
          📊 [정량 분석] 속도·고도·질량 텔레메트리 그래프
        </button>
        <button className={`tab-btn ${activeTab==='math'?'active':''}`} onClick={()=>setActiveTab('math')}>
          📐 [원리 탐구] 운동량 보존 & 페어링 분리 물리 수식
        </button>
        <button className={`tab-btn ${activeTab==='report'?'active':''}`} onClick={()=>setActiveTab('report')}>
          📝 [수행평가] 탐구 보고서 & 문제 풀이 Quiz
        </button>
      </div>

      {activeTab === 'sim' && <NuriSimTab />}
      {activeTab === 'graph' && <GraphTab />}
      {activeTab === 'math' && <MathTab />}
      {activeTab === 'report' && <ReportTab />}
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 1: 누리호 발사 & 다단/페어링 분리 실시간 캔버스 시뮬레이션
══════════════════════════════════════════════════ */
function NuriSimTab() {
  /* 발사 모드:
     'normal': 정상 다단 분리 + 페어링 분리 (목표 700km 궤도, 7.5km/s 성공)
     'no_fairing_sep': 페어링 미분리 (페어링 1.5t 사중량 유지 -> 궤도속도 미달 6.4km/s)
     'no_stage_sep': 단분리 미실시 (빈 1단/2단 30t 사중량 유지 -> 궤도 진입 실패 2.1km/s, 해상 추락)
  */
  const [mode, setMode] = useState('normal');
  const [speedMultiplier, setSpeedMultiplier] = useState(2); // 1x, 2x, 5x, 10x 배속
  
  /* 시뮬레이션 상태 */
  const [simStatus, setSimStatus] = useState('ready'); // ready | launching | paused | completed | failed
  const [telemetry, setTelemetry] = useState({
    time: 0,
    altKm: 0,
    velKms: 0,
    accelG: 0,
    massTon: 200.0,
    stage: '1단 연소 중 (4 engines)',
    fairingStatus: '보호 중 (대기권 내)',
    orbitStatus: '발사대 대기'
  });

  const canvasRef = useRef(null);
  const animRef = useRef(null);
  const stateRef = useRef({
    t: 0,
    mode: 'normal',
    status: 'ready',
    alt: 0, // km
    vel: 0, // km/s
    accel: 0, // m/s^2
    mass: 200.0, // tons
    downrange: 0, // km
    stagePhase: 1, // 1: 1단연소, 2: 2단연소, 3: 3단연소, 4: 궤도선회
    fairingDetached: false,
    stage1Detached: false,
    stage2Detached: false,
    satDeployed: false,
    
    // 이격 파티클 애니메이션 좌표
    stage1SepPos: null, // { x, y, vx, vy, rot }
    stage2SepPos: null,
    fairingLeftPos: null,
    fairingRightPos: null,
    particles: []
  });

  /* 누리호 물리 파라미터 (실제 Nuri KSLV-II 규격 준수) */
  const NURI_SPECS = {
    liftoffMass: 200.0, // 총 이륙 질량 200톤
    stage1: { fuel: 130.0, dry: 20.0, burnDur: 125, thrustKn: 2940 }, // 1단: 75t x 4 = 300t 힘
    fairing: { mass: 1.5, sepTime: 204, sepAlt: 191 }, // 페어링: 1.5톤, 204초, 191km
    stage2: { fuel: 35.0, dry: 4.5, burnDur: 130, thrustKn: 735 }, // 2단: 75t x 1
    stage3: { fuel: 11.0, dry: 1.5, burnDur: 500, thrustKn: 68.6 }, // 3단: 7t x 1
    payload: 1.5 // 위성 체 1.5톤
  };

  /* 시뮬레이션 프레임 계산 (물리 모델링) */
  const updatePhysics = (dt) => {
    const s = stateRef.current;
    const mMode = s.mode;
    
    s.t += dt;
    const t = s.t;

    let totalM = NURI_SPECS.payload; // 기본 위성 질량 1.5t

    /* 1. 스테이지 및 질량 상태 계산 */
    let thrust = 0; // kN
    let stageName = '';
    let fairingStateStr = '';

    // (A) 0 ~ 125s: 1단 엔진 연소 구간
    if (t <= 125) {
      s.stagePhase = 1;
      const fuelRem1 = Math.max(0, NURI_SPECS.stage1.fuel * (1 - t / 125));
      totalM += fuelRem1 + NURI_SPECS.stage1.dry;
      totalM += NURI_SPECS.stage2.fuel + NURI_SPECS.stage2.dry;
      totalM += NURI_SPECS.stage3.fuel + NURI_SPECS.stage3.dry;
      totalM += NURI_SPECS.fairing.mass;
      thrust = NURI_SPECS.stage1.thrustKn;
      stageName = '🔥 1단 연소 중 (75톤x4 300톤 추진력)';
      fairingStateStr = '🛡️ 페어링 밀폐 (대기 마찰 보호)';
    }
    // (B) 125 ~ 255s: 2단 연소 구간 (t=125s 시 1단 분리)
    else if (t > 125 && t <= 255) {
      s.stagePhase = 2;
      // 1단 분리 체크
      if (mMode !== 'no_stage_sep') {
        s.stage1Detached = true;
      } else {
        // 미분리 시 빈 1단 20톤 계속 적재!
        totalM += NURI_SPECS.stage1.dry;
      }

      // 페어링 분리 체크 (t >= 204s)
      if (t >= 204) {
        if (mMode === 'normal') {
          s.fairingDetached = true;
        } else {
          // 페어링 미분리 시 1.5톤 사중량 추가 적재!
          totalM += NURI_SPECS.fairing.mass;
        }
        fairingStateStr = s.fairingDetached ? '✨ 페어링 분리 완료 (우주 진공)' : '⚠️ 페어링 미분리 (1.5t 사중량 탑재)';
      } else {
        totalM += NURI_SPECS.fairing.mass;
        fairingStateStr = '🛡️ 대기권 탈출 단계';
      }

      const dt2 = t - 125;
      const fuelRem2 = Math.max(0, NURI_SPECS.stage2.fuel * (1 - dt2 / 130));
      totalM += fuelRem2 + NURI_SPECS.stage2.dry;
      totalM += NURI_SPECS.stage3.fuel + NURI_SPECS.stage3.dry;
      thrust = NURI_SPECS.stage2.thrustKn;
      stageName = s.stage1Detached ? '🚀 2단 연소 중 (75톤 엔진)' : '⚠️ 2단 연소 중 (1단 20t 미분리 사중량 탑재!)';
    }
    // (C) 255 ~ 755s: 3단 연소 구간 (t=255s 시 2단 분리)
    else if (t > 255 && t <= 755) {
      s.stagePhase = 3;
      // 2단 분리 체크
      if (mMode !== 'no_stage_sep') {
        s.stage2Detached = true;
      } else {
        totalM += NURI_SPECS.stage1.dry + NURI_SPECS.stage2.dry; // 24.5톤 사중량!
      }

      if (mMode !== 'normal') {
        totalM += NURI_SPECS.fairing.mass; // 페어링 사중량 1.5t
      }
      s.fairingDetached = (mMode === 'normal');

      const dt3 = t - 255;
      const fuelRem3 = Math.max(0, NURI_SPECS.stage3.fuel * (1 - dt3 / 500));
      totalM += fuelRem3 + NURI_SPECS.stage3.dry;
      thrust = NURI_SPECS.stage3.thrustKn;
      stageName = s.stage2Detached ? '🌌 3단 연소 중 (7톤 고효율 엔진)' : '⚠️ 3단 연소 (24.5t 빈 껍데기 사중량 견인!)';
      fairingStateStr = s.fairingDetached ? '✨ 페어링 분리 상태' : '❌ 페어링 사중량 가속 방해';
    }
    // (D) t > 755s: 연소 종료 및 위성 분리 / 궤도 평가
    else {
      s.stagePhase = 4;
      thrust = 0;
      stageName = '🏁 추진 연소 완료 (관성 궤도 비행)';
      if (mMode === 'normal') {
        s.satDeployed = true;
      }
    }

    s.mass = totalM;

    /* 2. 가속도 및 속도, 고도 계산 (뉴턴 운동 방정식 F_net = F_thrust - m*g - F_drag) */
    const g = 9.81 * Math.pow(6371 / (6371 + s.alt), 2); // 고도별 중력가속도 감축
    // 대기 저항 (고도 100km 이상에서는 0에 수렴)
    const airDensity = 1.225 * Math.exp(-s.alt / 8.5); // kg/m^3
    const dragForceKn = 0.5 * airDensity * Math.pow(s.vel * 1000, 2) * 12.0 * 0.3 / 1000; // kN

    // 순 가속도 (m/s^2)
    const netForceKn = thrust - (s.t < 30 ? totalM * g : totalM * g * 0.35) - dragForceKn;
    const accelMss = Math.max(-g, netForceKn / totalM);
    s.accel = accelMss;

    // 속도 (km/s) 및 고도 (km) 적분
    s.vel += (accelMss / 1000) * dt;
    if (s.vel < 0 && s.alt <= 0) s.vel = 0;

    s.alt += s.vel * dt;
    s.downrange += (s.vel * 0.85) * dt;

    /* 3. 궤도 진입 성공 여부 판단 */
    let orbitStr = '🚀 상승 중...';
    if (t > 755 || s.alt >= 700) {
      if (mMode === 'normal' && s.vel >= 7.4) {
        orbitStr = '🎉 [성공] 700km 원 궤도 안착! (7.5 km/s)';
        s.status = 'completed';
      } else if (mMode === 'no_fairing_sep') {
        orbitStr = '⚠️ [원인: 페어링 미분리] 1.5t 사중량으로 최종속도 부족(6.3 km/s) -> 타원 궤도 저하';
        s.status = 'failed';
      } else {
        orbitStr = '❌ [원인: 단분리 미실시] 빈 로켓 24.5t 사중량 견인 실패 -> 궤도진입 불가, 해상 추락!';
        s.status = 'failed';
      }
    }

    /* 텔레메트리 업데이트 */
    setTelemetry({
      time: Math.round(t),
      altKm: Math.max(0, +s.alt.toFixed(1)),
      velKms: Math.max(0, +s.vel.toFixed(2)),
      accelG: +(accelMss / 9.81).toFixed(2),
      massTon: +s.mass.toFixed(1),
      stage: stageName,
      fairingStatus: fairingStateStr,
      orbitStatus: orbitStr
    });
  };

  /* 캔버스 그래픽 드로잉 루프 */
  const renderCanvas = () => {
    const cvs = canvasRef.current;
    if (!cvs) return;
    const ctx = cvs.getContext('2d');
    const W = cvs.width, H = cvs.height;
    const s = stateRef.current;

    // 1. 우주/대기권 배경 (고도에 따른 파란 하늘 -> 흑색 우주 전환)
    const skyFactor = Math.max(0, 1 - s.alt / 100); // 고도 100km에서 우주진입
    const bgGrad = ctx.createLinearGradient(0, H, 0, 0);
    bgGrad.addColorStop(0, `rgb(${Math.round(14 + 100*skyFactor)}, ${Math.round(23 + 140*skyFactor)}, ${Math.round(42 + 200*skyFactor)})`);
    bgGrad.addColorStop(1, '#030712');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // 우주 공간 별무리 (skyFactor 낮을 때만 부각)
    if (skyFactor < 0.8) {
      ctx.fillStyle = `rgba(255,255,255,${(1 - skyFactor)*0.8})`;
      for (let i = 0; i < 50; i++) {
        const sx = (i * 47 + 13) % W;
        const sy = (i * 31 + 7) % (H * 0.7);
        ctx.beginPath(); ctx.arc(sx, sy, (i % 3 === 0 ? 1.5 : 1), 0, Math.PI * 2); ctx.fill();
      }
    }

    // 지구 곡률 (하단 커브)
    const earthY = H + 600 - (s.alt / 700) * 450;
    const earthGrad = ctx.createRadialGradient(W / 2, earthY, 500, W / 2, earthY, 650);
    earthGrad.addColorStop(0, '#1e3a8a');
    earthGrad.addColorStop(0.7, '#0ea5e9');
    earthGrad.addColorStop(1, '#030712');
    ctx.fillStyle = earthGrad;
    ctx.beginPath();
    ctx.arc(W / 2, earthY, 650, 0, Math.PI * 2);
    ctx.fill();

    // 2. 누리호 발사체 궤적 (Trajectory Line)
    const trajX = 80 + (s.downrange / 800) * (W - 160);
    const trajY = H - 50 - (s.alt / 750) * (H - 100);

    ctx.strokeStyle = 'rgba(56,189,248,0.4)';
    ctx.lineWidth = 2;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(80, H - 50);
    ctx.quadraticCurveTo(W * 0.3, H - 180, trajX, trajY);
    ctx.stroke();
    ctx.setLineDash([]);

    /* 3. 누리호 로켓 본체 및 이격체 렌더링 */
    const rx = Math.max(80, Math.min(W - 80, trajX));
    const ry = Math.max(40, Math.min(H - 40, trajY));
    
    // 로켓 기울기 각도 (발사 직립 90도 -> 궤도 수평 0도)
    const pitchRad = Math.max(0.1, (Math.PI / 2) * Math.exp(-s.alt / 220));

    ctx.save();
    ctx.translate(rx, ry);
    ctx.rotate(Math.PI / 2 - pitchRad); // 궤도 방향 회전

    // (A) 추진 엔진 제트 화염
    if (s.t < 755 && s.status === 'launching') {
      const flameLen = s.stagePhase === 1 ? 45 : (s.stagePhase === 2 ? 30 : 18);
      const fGrad = ctx.createLinearGradient(0, 30, 0, 30 + flameLen);
      fGrad.addColorStop(0, '#ffffff');
      fGrad.addColorStop(0.2, '#38bdf8');
      fGrad.addColorStop(0.5, '#f59e0b');
      fGrad.addColorStop(1, 'rgba(239, 68, 68, 0)');
      ctx.fillStyle = fGrad;
      ctx.beginPath();
      ctx.moveTo(-8, 30);
      ctx.lineTo(0, 30 + flameLen + Math.random() * 8);
      ctx.lineTo(8, 30);
      ctx.closePath();
      ctx.fill();
    }

    // (B) 1단 로켓 (t < 125s 동안 결합, 125s 분리 시 아래로 낙하)
    if (!s.stage1Detached) {
      // 1단 본체
      const g1 = ctx.createLinearGradient(-10, 0, 10, 0);
      g1.addColorStop(0, '#e2e8f0'); g1.addColorStop(0.5, '#ffffff'); g1.addColorStop(1, '#94a3b8');
      ctx.fillStyle = g1;
      ctx.fillRect(-10, 5, 20, 26);
      // 대한민국 태극기 데칼 / NURI 로고
      ctx.fillStyle = '#052c65'; ctx.fillRect(-10, 8, 20, 3);
      ctx.fillStyle = '#dc2626'; ctx.fillRect(-10, 11, 20, 2);
    }

    // (C) 2단 로켓 (t < 255s 동안 결합)
    if (!s.stage2Detached) {
      const g2 = ctx.createLinearGradient(-8, 0, 8, 0);
      g2.addColorStop(0, '#cbd5e1'); g2.addColorStop(0.5, '#f8fafc'); g2.addColorStop(1, '#64748b');
      ctx.fillStyle = g2;
      ctx.fillRect(-8, -15, 16, 20);
    }

    // (D) 3단 로켓 및 위성 페이로드
    const g3 = ctx.createLinearGradient(-6, 0, 6, 0);
    g3.addColorStop(0, '#94a3b8'); g3.addColorStop(0.5, '#e2e8f0'); g3.addColorStop(1, '#475569');
    ctx.fillStyle = g3;
    ctx.fillRect(-6, -30, 12, 15);

    // (E) 페어링 (Fairing Nosecone)
    if (!s.fairingDetached) {
      // 페어링 조립 캡슐 (흰색 타원 원뿔)
      const gF = ctx.createLinearGradient(-7, 0, 7, 0);
      gF.addColorStop(0, '#ffffff'); gF.addColorStop(0.7, '#e2e8f0'); gF.addColorStop(1, '#cbd5e1');
      ctx.fillStyle = gF;
      ctx.beginPath();
      ctx.moveTo(-7, -30);
      ctx.quadraticCurveTo(0, -48, 7, -30);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#2563eb';
      ctx.lineWidth = 1;
      ctx.stroke();
    } else {
      // 페어링 분리 후 위성 본체 노출 (차세대 소형위성 2호 태양전지판)
      ctx.fillStyle = '#fbbf24';
      ctx.fillRect(-5, -40, 10, 10);
      if (s.satDeployed) {
        // 좌우 태양광 날개 펼침
        ctx.fillStyle = '#0284c7';
        ctx.fillRect(-14, -37, 8, 4);
        ctx.fillRect(6, -37, 8, 4);
      }
    }

    ctx.restore();

    // 4. 이격체(분리된 1단, 2단, 페어링 껍데기) 표류 연출
    if (s.stage1Detached) {
      ctx.fillStyle = 'rgba(148,163,184,0.6)';
      ctx.font = '10px Space Mono';
      ctx.fillText('🗑️ 1단 분리체 (20t 낙하)', rx - 60, ry + 50);
    }
    if (s.fairingDetached) {
      ctx.fillStyle = '#38bdf8';
      ctx.font = '10px Space Mono';
      ctx.fillText('✨ 페어링 분리 (1.5t)', rx + 25, ry - 35);
    }

    // 5. 캔버스 HUD 계기판 배너
    ctx.fillStyle = 'rgba(11, 19, 43, 0.85)';
    ctx.strokeStyle = '#1e3a8a';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.roundRect(14, 14, 310, 95, 8); ctx.fill(); ctx.stroke();

    ctx.fillStyle = '#60a5fa'; ctx.font = 'bold 11px Noto Sans KR';
    ctx.fillText(`🚀 누리호 비행 텔레메트리 (t = ${Math.round(s.t)}초)`, 24, 32);

    ctx.fillStyle = '#cbd5e1'; ctx.font = '10.5px Space Mono';
    ctx.fillText(`고도 (h): ${s.alt.toFixed(1)} km`, 24, 50);
    ctx.fillText(`속도 (v): ${s.vel.toFixed(2)} km/s (${(s.vel*3600).toFixed(0)} km/h)`, 24, 66);
    ctx.fillText(`총 질량 (m): ${s.mass.toFixed(1)} 톤`, 24, 82);

    ctx.fillStyle = s.fairingDetached ? '#a3e635' : '#fca5a5';
    ctx.font = 'bold 10px Noto Sans KR';
    ctx.fillText(s.fairingDetached ? '✓ 페어링 분리 완료' : '⚠️ 페어링 탑재 중', 200, 82);
  };

  /* 시뮬레이션 루프 실행 */
  const startLaunch = () => {
    cancelAnimationFrame(animRef.current);
    const s = stateRef.current;
    s.t = 0;
    s.mode = mode;
    s.status = 'launching';
    s.alt = 0;
    s.vel = 0;
    s.accel = 0;
    s.mass = 200.0;
    s.downrange = 0;
    s.stagePhase = 1;
    s.fairingDetached = false;
    s.stage1Detached = false;
    s.stage2Detached = false;
    s.satDeployed = false;

    setSimStatus('launching');

    let lastTime = performance.now();
    const loop = (now) => {
      const dtReal = (now - lastTime) / 1000;
      lastTime = now;

      // 배속 적용
      const dtSim = Math.min(0.2, dtReal * speedMultiplier * 2.5);

      if (s.status === 'launching') {
        updatePhysics(dtSim);
        renderCanvas();
        animRef.current = requestAnimationFrame(loop);
      } else {
        renderCanvas();
        setSimStatus(s.status);
      }
    };

    animRef.current = requestAnimationFrame(loop);
  };

  /* 리셋 */
  const resetSim = () => {
    cancelAnimationFrame(animRef.current);
    const s = stateRef.current;
    s.t = 0;
    s.status = 'ready';
    s.alt = 0;
    s.vel = 0;
    s.mass = 200.0;
    s.fairingDetached = false;
    s.stage1Detached = false;
    s.stage2Detached = false;

    setSimStatus('ready');
    setTelemetry({
      time: 0,
      altKm: 0,
      velKms: 0,
      accelG: 0,
      massTon: 200.0,
      stage: '발사 준비 완료',
      fairingStatus: '보호 커버 장착됨',
      orbitStatus: '대기 중'
    });

    renderCanvas();
  };

  useEffect(() => {
    resetSim();
  }, [mode]);

  return (
    <div>
      {/* ── 탐구 개요 카드 ── */}
      <div className="card">
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',flexWrap:'wrap',gap:12}}>
          <div>
            <span className="badge badge-lime" style={{marginBottom:6}}>실제 누리호 5차 발사 시퀀스 기반</span>
            <h3 style={{fontSize:16,fontWeight:800,color:'#f8fafc',marginTop:4}}>
              왜 페어링과 1단·2단 로켓을 분리할까? (3가지 조건 실험 비교)
            </h3>
            <p style={{fontSize:13,color:'#94a3b8',lineHeight:1.6,marginTop:4}}>
              우주 발사체는 연료 소비에 따라 <b>빈 껍데기가 되는 연료 탱크와 보호 덮개(페어링)를 제때 버리지 않으면 사중량(Dead Mass)</b>이 되어 
              최종 궤도 속도(7.5 km/s)에 도달하지 못합니다. 3가지 발사 조건의 결과를 직접 비교해 보세요.
            </p>
          </div>
          
          <div style={{display:'flex',gap:8,alignItems:'center'}}>
            <span style={{fontSize:12,color:'#cbd5e1',fontWeight:700}}>⚡ 재생 배속:</span>
            {[1, 2, 5, 10].map(sp => (
              <button key={sp} className="btn-secondary" 
                style={{padding:'4px 10px',fontSize:12,background:speedMultiplier===sp?'#2563eb':undefined,color:speedMultiplier===sp?'#fff':undefined}}
                onClick={()=>setSpeedMultiplier(sp)}>
                {sp}x
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* ── 3가지 실험 모드 선택 라디오 박스 ── */}
      <div className="card" style={{background:'#080e20',borderColor:'#1e3a8a'}}>
        <span style={{fontSize:13,fontWeight:800,color:'#38bdf8',display:'block',marginBottom:10}}>
          🎛️ 발사 시뮬레이션 모드 선택 (페어링 & 다단 분리 조건 설정)
        </span>
        
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(280px, 1fr))',gap:12}}>
          {/* 정상 모드 */}
          <div style={{
            background: mode==='normal' ? 'rgba(37,99,235,0.18)' : '#0f172a',
            border: `2px solid ${mode==='normal'?'#3b82f6':'#1e293b'}`,
            borderRadius:10, padding:12, cursor:'pointer'
          }} onClick={()=>setMode('normal')}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:4}}>
              <span style={{fontWeight:800,color:'#60a5fa',fontSize:13.5}}>🟢 정상 다단 & 페어링 분리</span>
              <span className="badge badge-lime">정상 궤도 진입</span>
            </div>
            <p style={{fontSize:11.5,color:'#cbd5e1',lineHeight:1.5}}>
              • 125초: 1단 분리 (20t 사중량 제거)<br/>
              • 204초: 페어링 분리 (1.5t 제거)<br/>
              • 255초: 2단 분리 (4.5t 제거)<br/>
              <b>👉 최종속도 7.5 km/s (700km 궤도 안착)</b>
            </p>
          </div>

          {/* 페어링 미분리 모드 */}
          <div style={{
            background: mode==='no_fairing_sep' ? 'rgba(245,158,11,0.18)' : '#0f172a',
            border: `2px solid ${mode==='no_fairing_sep'?'#f59e0b':'#1e293b'}`,
            borderRadius:10, padding:12, cursor:'pointer'
          }} onClick={()=>setMode('no_fairing_sep')}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:4}}>
              <span style={{fontWeight:800,color:'#fbbf24',fontSize:13.5}}>⚠️ 페어링 미분리 (고장 모사)</span>
              <span className="badge badge-amber">속도 저하 궤도 미달</span>
            </div>
            <p style={{fontSize:11.5,color:'#cbd5e1',lineHeight:1.5}}>
              • 1단/2단은 정상 분리되나,<br/>
              • 대기권 밖(204초)에서 <b>1.5t 페어링 안 열림!</b><br/>
              <b>👉 최종속도 6.4 km/s (속도 부족, 궤도 타락)</b>
            </p>
          </div>

          {/* 단분리 미실시 모드 */}
          <div style={{
            background: mode==='no_stage_sep' ? 'rgba(239,68,68,0.18)' : '#0f172a',
            border: `2px solid ${mode==='no_stage_sep'?'#ef4444':'#1e293b'}`,
            borderRadius:10, padding:12, cursor:'pointer'
          }} onClick={()=>setMode('no_stage_sep')}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:4}}>
              <span style={{fontWeight:800,color:'#fca5a5',fontSize:13.5}}>❌ 단분리 미실시 (1/2단 견인)</span>
              <span className="badge badge-red">해상 추락 진입 실패</span>
            </div>
            <p style={{fontSize:11.5,color:'#cbd5e1',lineHeight:1.5}}>
              • 빈 1단(20t) & 2단(4.5t) 껍데기를<br/>
              • 분리하지 않고 끝까지 끌고 올라감!<br/>
              <b>👉 최종속도 2.1 km/s (무게 압사, 궤도 실패)</b>
            </p>
          </div>
        </div>
      </div>

      {/* ── 캔버스 발사 디스플레이 ── */}
      <div className="card" style={{padding:10,position:'relative'}}>
        <canvas ref={canvasRef} width={800} height={320}
          style={{width:'100%',height:'320px',borderRadius:10,background:'#030712',display:'block'}}/>
        
        {/* 컨트롤 오버레이 버튼 바 */}
        <div style={{display:'flex',justifyContent:'center',gap:14,marginTop:12,flexWrap:'wrap'}}>
          <button className="btn-success" onClick={startLaunch} disabled={simStatus==='launching'}
            style={{padding:'10px 28px',fontSize:14,boxShadow:'0 0 16px rgba(22,163,74,0.4)'}}>
            🚀 {simStatus==='launching'?'누리호 발사 비행 중...':'누리호 5차 발사 개시!'}
          </button>
          <button className="btn-secondary" onClick={resetSim} disabled={simStatus==='launching'}
            style={{padding:'10px 20px',fontSize:13}}>
            🔄 발사대 리셋 (초기화)
          </button>
        </div>
      </div>

      {/* ── 실시간 비행 HUD 계측기 카드 ── */}
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(200px, 1fr))',gap:12,marginBottom:14}}>
        
        <div style={{background:'#0a1224',padding:12,borderRadius:10,border:'1px solid #1e293b'}}>
          <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>⏱️ 발사 후 경과 시간 (t)</span>
          <span className="num-mono" style={{fontSize:22,fontWeight:800,color:'#60a5fa'}}>
            {telemetry.time} <span style={{fontSize:13,color:'#94a3b8'}}>초</span>
          </span>
        </div>

        <div style={{background:'#0a1224',padding:12,borderRadius:10,border:'1px solid #1e293b'}}>
          <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>🚀 현재 속도 (v)</span>
          <span className="num-mono" style={{fontSize:22,fontWeight:800,color:'#38bdf8'}}>
            {telemetry.velKms} <span style={{fontSize:13,color:'#94a3b8'}}>km/s</span>
          </span>
        </div>

        <div style={{background:'#0a1224',padding:12,borderRadius:10,border:'1px solid #1e293b'}}>
          <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>🛰️ 비행 고도 (h)</span>
          <span className="num-mono" style={{fontSize:22,fontWeight:800,color:'#a3e635'}}>
            {telemetry.altKm} <span style={{fontSize:13,color:'#94a3b8'}}>km</span>
          </span>
        </div>

        <div style={{background:'#0a1224',padding:12,borderRadius:10,border:'1px solid #1e293b'}}>
          <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>⚖️ 발사체 총 질량 (m)</span>
          <span className="num-mono" style={{fontSize:22,fontWeight:800,color:'#fbbf24'}}>
            {telemetry.massTon} <span style={{fontSize:13,color:'#94a3b8'}}>톤</span>
          </span>
        </div>

      </div>

      {/* 상태 알림 바 */}
      <div className="card" style={{background:'#0a1020',border:'1px solid #2563eb'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',flexWrap:'wrap',gap:10}}>
          <div>
            <span style={{fontSize:12,color:'#94a3b8'}}>진행 상태: </span>
            <span style={{fontSize:13.5,fontWeight:700,color:'#f8fafc',marginLeft:4}}>{telemetry.stage}</span>
            <span style={{fontSize:12,color:'#38bdf8',marginLeft:12}}>{telemetry.fairingStatus}</span>
          </div>
          <div style={{fontWeight:800,fontSize:13.5,color:telemetry.orbitStatus.includes('성공')?'#a3e635':'#fca5a5'}}>
            {telemetry.orbitStatus}
          </div>
        </div>
      </div>

    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 2: 텔레메트리 그래프 (속도, 고도, 질량 변화)
══════════════════════════════════════════════════ */
function GraphTab() {
  return (
    <div>
      <div className="card">
        <h3 style={{fontSize:15,fontWeight:800,color:'#f8fafc',marginBottom:8}}>
          📊 텔레메트리 데이터 그래프: 분리 여부에 따른 속도·질량 궤적 비교
        </h3>
        <p style={{fontSize:13,color:'#94a3b8',lineHeight:1.6}}>
          다단 분리 및 페어링 분리가 일어날 때 로켓의 <b>질량(m)이 급격히 계단식으로 감소</b>하며, 
          이에 따라 <b>속도 기울기(가속도 $a = F/m$)가 폭증</b>하는 현상을 확인합니다.
        </p>
      </div>

      {/* 3가지 비교 그래프 컴포넌트 */}
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(340px, 1fr))',gap:14}}>
        
        {/* 그래프 1: 속도-시간 (v-t) */}
        <div className="card">
          <span style={{fontSize:13.5,fontWeight:700,color:'#38bdf8',display:'block',marginBottom:8}}>
            🚀 1. 속도-시간 그래프 (v-t Graph)
          </span>
          <svg width="100%" height="200" viewBox="0 0 320 200">
            <rect x="0" y="0" width="320" height="200" fill="#070c18" rx="8"/>
            {/* 그리드 */}
            <line x1="40" y1="20" x2="40" y2="170" stroke="#1e293b"/>
            <line x1="40" y1="170" x2="300" y2="170" stroke="#1e293b"/>
            <text x="35" y="25" fill="#64748b" fontSize="9" textAnchor="end">7.5 km/s</text>
            <text x="35" y="174" fill="#64748b" fontSize="9" textAnchor="end">0</text>
            <text x="295" y="186" fill="#64748b" fontSize="9" textAnchor="end">750초</text>
            <line x1="40" y1="30" x2="300" y2="30" stroke="#334155" strokeDasharray="3,3"/>

            {/* 정상 분리 커브 (청색) */}
            <path d="M 40 170 Q 75 145, 100 130 T 170 85 T 300 30" fill="none" stroke="#38bdf8" strokeWidth="2.5"/>
            
            {/* 페어링 미분리 커브 (황색) */}
            <path d="M 40 170 Q 75 145, 100 130 T 170 95 T 300 60" fill="none" stroke="#f59e0b" strokeWidth="2" strokeDasharray="4,2"/>

            {/* 단분리 미실시 커브 (적색) */}
            <path d="M 40 170 Q 75 145, 100 130 T 170 145 T 300 160" fill="none" stroke="#ef4444" strokeWidth="2" strokeDasharray="2,2"/>

            {/* 범례 */}
            <circle cx="50" cy="188" r="4" fill="#38bdf8"/>
            <text x="58" y="191" fill="#cbd5e1" fontSize="9">정상 분리 (7.5km/s 궤도달성)</text>
            <circle cx="180" cy="188" r="4" fill="#f59e0b"/>
            <text x="188" y="191" fill="#cbd5e1" fontSize="9">페어링 미분리 (6.4km/s)</text>
          </svg>
          <p style={{fontSize:11.5,color:'#94a3b8',marginTop:8}}>
            💡 1단/2단 분리 시점(125초, 255초) 및 페어링 분리 시점(204초)에서 질량이 줄어들며 속도 곡선의 기울기(가속도)가 꺾여 급격히 커집니다.
          </p>
        </div>

        {/* 그래프 2: 발사체 질량-시간 (m-t) */}
        <div className="card">
          <span style={{fontSize:13.5,fontWeight:700,color:'#a3e635',display:'block',marginBottom:8}}>
            ⚖️ 2. 발사체 질량-시간 그래프 (m-t Graph)
          </span>
          <svg width="100%" height="200" viewBox="0 0 320 200">
            <rect x="0" y="0" width="320" height="200" fill="#070c18" rx="8"/>
            <line x1="40" y1="20" x2="40" y2="170" stroke="#1e293b"/>
            <line x1="40" y1="170" x2="300" y2="170" stroke="#1e293b"/>
            <text x="35" y="25" fill="#64748b" fontSize="9" textAnchor="end">200톤</text>
            <text x="35" y="174" fill="#64748b" fontSize="9" textAnchor="end">0</text>

            {/* 정상 분리 질량 커브 (계단식 급감!) */}
            <path d="M 40 25 L 85 105 L 85 130 L 115 155 L 115 157 L 140 170 L 300 172" fill="none" stroke="#a3e635" strokeWidth="2.5"/>
            
            {/* 계단식 분리 지점 표시 */}
            <circle cx="85" cy="117" r="3" fill="#f59e0b"/>
            <text x="92" y="115" fill="#f59e0b" fontSize="8">1단 분리 (-20t)</text>
            <circle cx="115" cy="156" r="3" fill="#38bdf8"/>
            <text x="122" y="152" fill="#38bdf8" fontSize="8">페어링 분리 (-1.5t)</text>

            <circle cx="140" cy="170" r="3" fill="#c084fc"/>
            <text x="148" y="168" fill="#c084fc" fontSize="8">2단 분리 (-4.5t)</text>
          </svg>
          <p style={{fontSize:11.5,color:'#94a3b8',marginTop:8}}>
            💡 불필요해진 빈 1단(20t), 페어링(1.5t), 빈 2단(4.5t)을 수직으로 툭 떨어뜨려 버림으로써 3단 로켓이 1.5t 위성만 가볍게 가속합니다!
          </p>
        </div>

      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 3: 운동량 보존 & 페어링 분리 물리 수식 탐구
══════════════════════════════════════════════════ */
function MathTab() {
  return (
    <div>
      {/* 핵심 이론 박스 1 */}
      <div className="hl-box">
        <h3 style={{fontSize:16,fontWeight:800,color:'#93c5fd',marginBottom:8}}>
          📐 1. 운동량 보존 법칙과 다단 로켓 추진 방정식 (Tsiolkovsky Rocket Equation)
        </h3>
        <p style={{fontSize:13.5,color:'#e2e8f0',lineHeight:1.8}}>
          외력이 무시되는 계에서 배기가스를 분출하여 얻는 로켓의 속도 증가량 <Eq f="\Delta v"/>는 찌올콥스키 방정식에 의해 결정됩니다.
        </p>
        <div style={{background:'rgba(15,23,42,0.6)',padding:12,borderRadius:8,marginTop:10,textAlign:'center'}}>
          <Eq f="\Delta v = v_e \cdot \ln \left( \frac{m_0}{m_f} \right)" display={true}/>
          <p style={{fontSize:12,color:'#94a3b8',marginTop:6}}>
            여기서 <Eq f="v_e"/>: 가스 분출 속력, <Eq f="m_0"/>: 발사 시 초기 질량, <Eq f="m_f"/>: 연소 후 최종 남아있는 질량
          </p>
        </div>
      </div>

      {/* 핵심 이론 박스 2: 페어링 분리의 이유 */}
      <div className="card">
        <h3 style={{fontSize:15,fontWeight:800,color:'#fbbf24',marginBottom:10}}>
          🛡️ 2. 페어링(Payload Fairing) 분리의 물리적 이유
        </h3>
        
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(280px, 1fr))',gap:14}}>
          <div style={{background:'#0a1020',padding:14,borderRadius:10,border:'1px solid #1e293b'}}>
            <span style={{fontSize:13,fontWeight:700,color:'#38bdf8'}}>1단계: 대기권 통과 (고도 0 ~ 100km)</span>
            <p style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.7,marginTop:6}}>
              • 대기 마찰열(1,000℃ 이상)과 공기 저항 둔두압으로부터 정밀 인공위성을 물리적으로 방어해야 함.<br/>
              • <b>페어링 필수 탑재!</b>
            </p>
          </div>

          <div style={{background:'#0a1020',padding:14,borderRadius:10,border:'1px solid #1e293b'}}>
            <span style={{fontSize:13,fontWeight:700,color:'#a3e635'}}>2단계: 우주 진공 진입 (고도 190km 이상)</span>
            <p style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.7,marginTop:6}}>
              • 공기가 거의 없어 마찰열 방어 필요성 소멸.<br/>
              • 이때 1.5톤 페어링을 분리하지 않으면 <b>무거운 불필요 사중량(Dead Weight)</b>이 되어 로켓 가속을 방해함.<br/>
              • <b>누리호는 204초(고도 191km)에 페어링 반통 2개를 즉시 분리!</b>
            </p>
          </div>
        </div>
      </div>

      {/* 누리호 5차 발사 타임라인 표 */}
      <div className="card">
        <span style={{fontSize:14,fontWeight:800,color:'#f8fafc',display:'block',marginBottom:10}}>
          📋 누리호(KSLV-II) 실제 발사 시퀀스 타임라인 (Timeline)
        </span>

        <table className="table-custom">
          <thead>
            <tr>
              <th>시각 (t)</th>
              <th>비행 고도 (h)</th>
              <th>주요 이벤트 (Event)</th>
              <th>물리적 의미 및 질량 변화</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="num-mono">t = 0초</td>
              <td className="num-mono">0 km</td>
              <td>🚀 이륙 (Liftoff)</td>
              <td>1단 75t 엔진 4기 점화 (총 300톤 추진력)</td>
            </tr>
            <tr>
              <td className="num-mono" style={{color:'#60a5fa'}}>t = 125초</td>
              <td className="num-mono">59 km</td>
              <td style={{color:'#60a5fa',fontWeight:700}}>💥 1단 로켓 분리</td>
              <td>연료 소진된 빈 1단 껍데기(20톤) 분리 낙하</td>
            </tr>
            <tr>
              <td className="num-mono" style={{color:'#fbbf24'}}>t = 204초</td>
              <td className="num-mono">191 km</td>
              <td style={{color:'#fbbf24',fontWeight:700}}>✨ 페어링(Fairing) 분리</td>
              <td>대기권 밖 진입, 1.5톤 사중량 분리 제거</td>
            </tr>
            <tr>
              <td className="num-mono" style={{color:'#c084fc'}}>t = 255초</td>
              <td className="num-mono">258 km</td>
              <td style={{color:'#c084fc',fontWeight:700}}>💥 2단 로켓 분리</td>
              <td>빈 2단 껍데기(4.5톤) 분리, 3단 엔진 점화</td>
            </tr>
            <tr>
              <td className="num-mono" style={{color:'#a3e635'}}>t = 755초</td>
              <td className="num-mono">700 km</td>
              <td style={{color:'#a3e635',fontWeight:700}}>🛰️ 위성 궤도 투입 완료</td>
              <td>목표 원 궤도 속도 7.5 km/s 달성 성공</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 4: 탐구 보고서 & 형성평가 Quiz
══════════════════════════════════════════════════ */
function ReportTab() {
  const [answers, setAnswers] = useState({ q1: '', q2: '', q3: '' });
  const [submitted, setSubmitted] = useState(false);

  const checkAnswers = () => {
    setSubmitted(true);
  };

  return (
    <div>
      <div className="card">
        <h3 style={{fontSize:15,fontWeight:800,color:'#f8fafc',marginBottom:8}}>
          📝 형성평가 및 탐구 보고서 문제 풀이
        </h3>
        <p style={{fontSize:13,color:'#94a3b8'}}>
          시뮬레이션으로 관찰한 내용을 바탕으로 질문에 답해 보세요.
        </p>
      </div>

      {/* Q1 */}
      <div className="card">
        <p style={{fontWeight:700,fontSize:13.5,color:'#38bdf8',marginBottom:8}}>
          Q1. 누리호가 고도 191km(발사 후 204초)에서 페어링(Fairing)을 분리하는 주요 물리적 이유는 무엇인가요?
        </p>
        <div style={{display:'flex',flexDirection:'column',gap:6,fontSize:12.5}}>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q1" value="1" onChange={e=>setAnswers({...answers, q1:e.target.value})}/> 1) 페어링 속의 가스를 연소시켜 추가 추진력을 얻기 위해
          </label>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q1" value="2" onChange={e=>setAnswers({...answers, q1:e.target.value})}/> 2) 대기권을 벗어난 후 공기 마찰 보호가 불필요해지므로 1.5톤의 사중량(Dead weight)을 버려 가속도를 높이기 위해
          </label>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q1" value="3" onChange={e=>setAnswers({...answers, q1:e.target.value})}/> 3) 지구 중력을 차단하기 위해
          </label>
        </div>
        {submitted && (
          <p style={{fontSize:12,marginTop:8,color:answers.q1==='2'?'#a3e635':'#fca5a5',fontWeight:700}}>
            {answers.q1==='2' ? '정답입니다! 👏 대기권 밖 진공에서는 1.5톤 페어링이 사중량이 되므로 분리해야 final velocity가 증가합니다.' : '❌ 오답입니다. 정답은 2번입니다.'}
          </p>
        )}
      </div>

      {/* Q2 */}
      <div className="card">
        <p style={{fontWeight:700,fontSize:13.5,color:'#38bdf8',marginBottom:8}}>
          Q2. 로켓이 배기가스를 분출할 때 앞으로 추진력을 얻는 원리를 서술한 것 중 옳지 않은 것은?
        </p>
        <div style={{display:'flex',flexDirection:'column',gap:6,fontSize:12.5}}>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q2" value="1" onChange={e=>setAnswers({...answers, q2:e.target.value})}/> 1) 로켓이 가스를 밀어내는 힘과 가스가 로켓을 밀어내는 힘은 작용-반작용 관계이다.
          </label>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q2" value="2" onChange={e=>setAnswers({...answers, q2:e.target.value})}/> 2) 외력이 없는 경우 (로켓+배기가스) 전체 계의 운동량의 총합은 보존된다.
          </label>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q2" value="3" onChange={e=>setAnswers({...answers, q2:e.target.value})}/> 3) 로켓은 주변 공기를 밀어내며 받침대 역할을 해야만 나아갈 수 있으므로 우주 진공에서는 추진할 수 없다.
          </label>
        </div>
        {submitted && (
          <p style={{fontSize:12,marginTop:8,color:answers.q2==='3'?'#a3e635':'#fca5a5',fontWeight:700}}>
            {answers.q2==='3' ? '정답입니다! 👏 로켓은 공기를 미는 것이 아니라 자기가 뿜어내는 가스와의 작용-반작용으로 우주 진공에서도 잘 나아갑니다.' : '❌ 오답입니다. 정답은 3번입니다.'}
          </p>
        )}
      </div>

      <div style={{textAlign:'center',marginTop:14}}>
        <button className="btn-primary" onClick={checkAnswers} style={{padding:'10px 24px',fontSize:14}}>
          📊 정답 제출 및 채점하기
        </button>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>
"""

components.html(REACT_HTML, height=920, scrolling=True)
