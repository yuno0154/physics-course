import streamlit as st
import streamlit.components.v1 as components

try:
    st.set_page_config(
        page_title="누리호 5차 발사와 다단·페어링 분리 3D 가상실험",
        page_icon="🚀",
        layout="wide"
    )
except Exception:
    pass


st.sidebar.title("🚀 누리호 다단·페어링 분리 3D 탐구")
st.sidebar.markdown(r"""
**2022 개정 교육과정 역학과 에너지**  
[12역학01-02] 운동량 보존 법칙 및 [12역학01-05] 로켓 추진과 다단 분리 원리

**누리호 5차 발사(KSLV-II)** 사례를 바탕으로:
1. **페어링(위성 보호 덮개) 분리 이유** (대기권을 나간 후 불필요한 무거운 짐 버리기)
2. **1단·2단 로켓 분리 이유** (다 탄 빈 연료 탱크를 버려 속도 $\Delta v$ 크게 올리기)
3. **운동량 보존 법칙과 찌올콥스키 로켓 방정식**의 쉬운 물리 원리
를 3D 생생한 비행 시뮬레이션으로 탐구합니다.

---
🎬 **[실제 발사 영상]**  
• [누리호 5차 발사 영상 (YouTube)](https://youtu.be/YeM0G_BEBzY)
""")

# 유튜브 영상 플레이어 상단 배치 (펼치기 가능)
with st.expander("📺 🎬 [실황 영상] 누리호 5차 발사 및 다단·페어링 분리 생중계 영상 (YouTube)", expanded=False):
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        st.video("https://youtu.be/YeM0G_BEBzY")
    with col_v2:
        st.markdown("""
        ### 📌 영상 관전 포인트 (쉬운 설명)
        * **125초 경과 (고도 59km)**: 다 탄 1단 로켓 분리 및 2단 엔진 점화
        * **204초 경과 (고도 191km)**: 위성 보호 덮개(페어링) 2개 분리
        * **255초 경과 (고도 258km)**: 2단 로켓 분리 및 3단 엔진 점화
        * **755초 경과 (고도 700km)**: 초속 7.5 km 궤도 속도 달성 후 위성 분리
        """)

REACT_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#050914;color:#e2e8f0;padding:14px;overflow-x:hidden;}
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
.table-custom th{background:#080e1e;color:#94a3b8;padding:10px 12px;border:1px solid #1e293b;text-align:center;font-weight:700;}
.table-custom td{padding:10px 12px;border:1px solid #1e293b;text-align:center;}
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
  const [activeTab, setActiveTab] = useState('sim3d'); // sim3d | dataTable | math | report

  return (
    <div>
      {/* 상단 타이틀 배너 */}
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:14,flexWrap:'wrap',gap:10}}>
        <div>
          <div style={{display:'flex',alignItems:'center',gap:8}}>
            <span style={{fontSize:24}}>🚀</span>
            <h2 style={{fontSize:19,fontWeight:800,color:'#f8fafc'}}>
              누리호 5차 발사 기반 3D/2D 로켓 비행 & 분리 가상실험실
            </h2>
            <span className="badge badge-lime">역학과 에너지 [쉬운 해설]</span>
          </div>
          <p style={{fontSize:12.5,color:'#94a3b8',marginTop:4}}>
            지상 발사대에서 700km 우주 궤도 진입까지, <b>'왜 다 탄 빈 로켓과 위성 덮개를 제때 버려야 하는지'</b> 비행으로 확인하세요!
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
        <button className={`tab-btn ${activeTab==='sim3d'?'active':''}`} onClick={()=>setActiveTab('sim3d')}>
          🌌 [가상 시뮬레이션] 지상 발사 ~ 700km 궤도 비행 & 3가지 조건 비교
        </button>
        <button className={`tab-btn ${activeTab==='dataTable'?'active':''}`} onClick={()=>setActiveTab('dataTable')}>
          📊 [데이터 비교 표] 3가지 발사 조건 정량적 최종 속도/질량 데이터 비교표
        </button>
        <button className={`tab-btn ${activeTab==='math'?'active':''}`} onClick={()=>setActiveTab('math')}>
          📐 [쉬운 물리 원리] 운동량 보존 & 질량 감축 공식 해설
        </button>
        <button className={`tab-btn ${activeTab==='report'?'active':''}`} onClick={()=>setActiveTab('report')}>
          📝 [수행평가] 탐구 보고서 & 학생 형성평가 Quiz
        </button>
      </div>

      {activeTab === 'sim3d' && <NuriSimTab />}
      {activeTab === 'dataTable' && <DataTableTab />}
      {activeTab === 'math' && <MathTab />}
      {activeTab === 'report' && <ReportTab />}
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 1: 누리호 지상 발사 ~ 700km 궤도 시뮬레이션
══════════════════════════════════════════════════ */
function NuriSimTab() {
  const [mode, setMode] = useState('normal'); // 'normal' | 'no_fairing_sep' | 'no_stage_sep'
  const [speedMult, setSpeedMult] = useState(2); // 배속
  const [viewMode, setViewMode] = useState('2d'); // '2d' | '3d'
  const [cameraView, setCameraView] = useState('follow'); // 'follow' | 'orbit' | 'ground'
  
  const [simState, setSimState] = useState('ready'); // ready | launching | completed | failed
  const [telemetry, setTelemetry] = useState({
    time: 0, altKm: 0, velKms: 0, accelG: 0, massTon: 200.0,
    phaseText: '발사대 대기 중', fairingText: '위성 덮개 닫힘 (공기 저항 방어)', resultText: '발사 버튼을 눌러보세요!'
  });

  const containerRef = useRef(null);
  const canvas2dRef = useRef(null);
  const animRef = useRef(null);
  const modeRef = useRef(mode);
  const speedRef = useRef(speedMult);
  const viewModeRef = useRef(viewMode);
  const camRef = useRef(cameraView);

  useEffect(() => { modeRef.current = mode; }, [mode]);
  useEffect(() => { speedRef.current = speedMult; }, [speedMult]);
  useEffect(() => { viewModeRef.current = viewMode; }, [viewMode]);
  useEffect(() => { camRef.current = cameraView; }, [cameraView]);

  // 물리 파라미터 및 3D 참조
  const simRef = useRef({
    t: 0, alt: 0, vel: 0, accel: 0, mass: 200.0, downrange: 0,
    stagePhase: 1,
    stage1Sep: false, fairingSep: false, stage2Sep: false, satDeployed: false,
    status: 'ready',
    path: [],
    debris: [],
    events: [],
    
    // 3D 객체
    scene: null, camera: null, renderer: null, rocketGroup: null,
    stage1Mesh: null, stage2Mesh: null, stage3Mesh: null,
    fairingLeft: null, fairingRight: null, solarPanelL: null, solarPanelR: null,
    is3DInited: false
  });

  const SPECS = {
    stage1: { fuel: 125.0, dry: 20.0, burnDur: 125, thrustKn: 2940 },
    fairing: { mass: 1.5, sepTime: 204 },
    stage2: { fuel: 35.0, dry: 4.5, burnDur: 130, thrustKn: 735 },
    stage3: { fuel: 11.0, dry: 1.5, burnDur: 500, thrustKn: 68.6 },
    payload: 1.5
  };

  // 고도(km), 수평거리(km) -> 2D 캔버스 좌표 변환
  const to2D = (downKm, altKm, W, H) => {
    const safeDown = Number.isFinite(downKm) ? downKm : 0;
    const safeAlt = Number.isFinite(altKm) ? altKm : 0;
    const x = 68 + (safeDown / 920) * (W - 120);
    const y = (H - 42) - (safeAlt / 780) * (H - 86);
    return { x, y };
  };

  /* 물리 업데이트 루프 (3가지 발사 조건별 정밀 궤적 및 분리 이벤트) */
  const updatePhysics = (dt) => {
    const s = simRef.current;
    const mMode = modeRef.current;
    const safeDt = Number.isFinite(dt) && dt > 0 ? dt : 0.016;

    const prevT = s.t;
    s.t = Math.max(0, s.t + safeDt);
    const t = s.t;

    let totalM = SPECS.payload;
    let phaseMsg = '';
    let fairingMsg = '';
    let targetAlt = 0;
    let targetVel = 0;
    let targetDown = 0;
    let accelGVal = 0;

    // 1) 구간별 질량 및 분리 상태 업데이트
    if (t <= 125) {
      s.stagePhase = 1;
      const p = Math.max(0, Math.min(1, t / 125));
      const fuelRem1 = SPECS.stage1.fuel * (1 - p);
      totalM = fuelRem1 + SPECS.stage1.dry + SPECS.stage2.fuel + SPECS.stage2.dry + SPECS.stage3.fuel + SPECS.stage3.dry + SPECS.fairing.mass + SPECS.payload;
      targetAlt = 59.0 * Math.pow(p, 1.35);
      targetVel = 1.80 * Math.pow(p, 1.1);
      targetDown = 75.0 * Math.pow(p, 1.4);
      accelGVal = 1.5 + 1.8 * p;
      phaseMsg = '🔥 1단 엔진 연소 중 (300톤급 추력 · 대기권 돌파)';
      fairingMsg = '🛡️ 위성 보호 덮개(페어링) 닫힘';
    } else if (t <= 255) {
      s.stagePhase = 2;
      // 125초: 1단 분리 이벤트
      if (mMode !== 'no_stage_sep') {
        if (!s.stage1Sep) {
          s.stage1Sep = true;
          s.debris.push({ type: 'stage1', down: s.downrange, alt: s.alt, vx: 0.4, vy: 0.1, rot: 0, label: '1단 분리 (20t)' });
          s.events.push({ down: s.downrange, alt: s.alt, text: '1단 분리 (125s, 59km)', col: '#38bdf8' });
        }
      } else {
        if (prevT <= 125) s.events.push({ down: s.downrange, alt: s.alt, text: '❌ 1단 미분리 (20t 짐 잔류)', col: '#ef4444' });
      }

      // 204초: 페어링 분리 이벤트
      if (t >= 204) {
        if (mMode === 'normal') {
          if (!s.fairingSep) {
            s.fairingSep = true;
            s.debris.push({ type: 'fairingL', down: s.downrange, alt: s.alt, vx: 0.3, vy: 0.35, rot: -0.2, label: '페어링 좌측' });
            s.debris.push({ type: 'fairingR', down: s.downrange, alt: s.alt, vx: 0.5, vy: -0.15, rot: 0.2, label: '페어링 우측' });
            s.events.push({ down: s.downrange, alt: s.alt, text: '✨ 페어링 분리 (204s, 191km)', col: '#a3e635' });
          }
          fairingMsg = '✨ 페어링(1.5t) 분리 완료! (위성 노출)';
        } else {
          if (prevT < 204) {
            s.events.push({ down: s.downrange, alt: s.alt, text: '⚠️ 페어링 미분리 고착! (204s)', col: '#f59e0b' });
          }
          fairingMsg = '⚠️ 페어링 미분리 (1.5t 덮개 고착 → 가속 저하!)';
        }
      } else {
        fairingMsg = '🛡️ 대기권 탈출 상승 중';
      }

      const p2 = Math.max(0, Math.min(1, (t - 125) / 130));
      const fuelRem2 = Math.max(0, SPECS.stage2.fuel * (1 - p2));
      totalM = fuelRem2 + SPECS.stage2.dry + SPECS.stage3.fuel + SPECS.stage3.dry + SPECS.payload
               + (s.stage1Sep ? 0 : SPECS.stage1.dry)
               + (s.fairingSep ? 0 : SPECS.fairing.mass);

      if (mMode === 'normal') {
        targetAlt = 59.0 + 199.0 * Math.pow(p2, 0.92); // 255s -> 258 km
        targetVel = 1.80 + 2.00 * p2;                  // 255s -> 3.80 km/s
        targetDown = 75.0 + 165.0 * p2;                // 255s -> 240 km
        accelGVal = 1.6 + 1.1 * p2;
        phaseMsg = '🚀 2단 엔진 연소 중 (75톤급 추력)';
      } else if (mMode === 'no_fairing_sep') {
        targetAlt = 59.0 + 186.0 * Math.pow(p2, 0.92); // 255s -> 245 km
        targetVel = 1.80 + 1.75 * p2;                  // 255s -> 3.55 km/s
        targetDown = 75.0 + 155.0 * p2;
        accelGVal = 1.4 + 0.9 * p2;
        phaseMsg = '⚠️ 2단 연소 중 (204초 이후 1.5t 덮개 짐 끌고 비행)';
      } else {
        // 단분리 미실시: 무거운 1단 20t 때문에 고도 180km 부근까지만 겨우 상승
        targetAlt = 59.0 + 115.0 * Math.sin(p2 * Math.PI * 0.55); // ~174 km
        targetVel = 1.80 + 0.30 * Math.sin(p2 * Math.PI * 0.6);   // 최고 2.10 km/s
        targetDown = 75.0 + 110.0 * p2;
        accelGVal = 0.3;
        phaseMsg = '❌ 2단 연소 (다 탄 1단 20톤 껍데기 때문에 가속 불능!)';
      }
    } else if (t <= 755) {
      s.stagePhase = 3;
      const p3 = Math.max(0, Math.min(1, (t - 255) / 500));
      const fuelRem3 = Math.max(0, SPECS.stage3.fuel * (1 - p3));

      if (mMode !== 'no_stage_sep') {
        if (!s.stage2Sep) {
          s.stage2Sep = true;
          s.debris.push({ type: 'stage2', down: s.downrange, alt: s.alt, vx: 0.5, vy: 0.05, rot: 0, label: '2단 분리 (4.5t)' });
          s.events.push({ down: s.downrange, alt: s.alt, text: '2단 분리 (255s)', col: '#38bdf8' });
        }
      }

      if (mMode === 'normal') {
        s.fairingSep = true;
        // 3단 연소 종료 시 3단 껍데기(1.5t)도 분리되어 최종 위성 질량 1.5t 달성
        totalM = SPECS.payload + fuelRem3 + (p3 < 0.98 ? SPECS.stage3.dry : 0);
        // 258 km -> 700.0 km 매끄러운 궤도 진입 곡선
        targetAlt = 258.0 + 442.0 * (1 - Math.pow(Math.max(0, 1 - p3), 1.85));
        targetVel = 3.80 + 3.70 * Math.pow(p3, 0.88); // 755s -> 7.50 km/s
        targetDown = 240.0 + 500.0 * p3;
        accelGVal = 0.8 + 1.6 * p3;
        phaseMsg = '🌌 3단 정밀 엔진 가속 중 (700km 궤도 진입 속도 7.5 km/s 향해 가속!)';
        fairingMsg = '✨ 페어링 분리 상태 (가벼운 위성체만 가속)';
      } else if (mMode === 'no_fairing_sep') {
        s.fairingSep = false;
        totalM = SPECS.payload + SPECS.fairing.mass + fuelRem3; // 종료 시 3.0 톤 (위성 1.5t + 덮개 1.5t)
        // 1.5t 덮개 무게 때문에 620 km에서 정점 찍고 속도 6.40 km/s에 그침
        targetAlt = 245.0 + 375.0 * Math.sin(p3 * Math.PI * 0.56); // 755s 부근 최고 620 km 후 완만히 처짐
        targetVel = 3.55 + 2.85 * Math.pow(p3, 0.9);               // 755s -> 6.40 km/s
        targetDown = 230.0 + 430.0 * p3;
        accelGVal = 0.5 + 0.7 * p3;
        phaseMsg = '⚠️ 3단 연소 중 (1.5t 덮개 무게 때문에 가속도 크게 저하!)';
        fairingMsg = '❌ 페어링 덮개 고착 (위성 분리 불가 + 속도 1.1 km/s 부족)';
      } else {
        // 단분리 미실시: 최고 고도 180 km 찍고 바다(고도 0 km)로 추락!
        totalM = 26.0 + fuelRem3;
        const fallP = Math.max(0, Math.min(1, (t - 255) / 260));
        targetAlt = Math.max(0, 180.0 * (1 - Math.pow(fallP, 1.65)));
        targetVel = 2.10 * (1 - 0.35 * fallP);
        targetDown = 185.0 + 190.0 * fallP;
        accelGVal = -0.8;
        phaseMsg = '❌ 추락 중 (다 탄 1·2단 24.5t 무게를 이기지 못하고 해상 추락!)';
        fairingMsg = '❌ 전 단 미분리 (총 26.0t 무거운 짐)';
        if (targetAlt <= 0.2) {
          s.alt = 0;
          s.vel = 2.10;
          s.mass = 26.0;
          s.events.push({ down: targetDown, alt: 0, text: '💥 해상 추락 (속도 부족 2.1 km/s)', col: '#ef4444' });
          s.status = 'failed';
        }
      }
    } else {
      // 755초 이후: 궤도 순항(normal) vs 궤도 미달 강하(no_fairing_sep)
      s.stagePhase = 4;
      const postT = Math.max(0, t - 755);
      if (mMode === 'normal') {
        s.satDeployed = true;
        totalM = 1.5;
        targetAlt = 700.0;
        targetVel = 7.50;
        targetDown = 740.0 + postT * 2.2;
        accelGVal = 0;
        phaseMsg = '🛰️ 목표 고도 700km 원궤도 안착 & 위성 사출 성공!';
        fairingMsg = '✨ 태양전지판 전개 및 지상국 교신 성공';
        if (prevT <= 755) {
          s.events.push({ down: 740.0, alt: 700.0, text: '🎉 700km 궤도 진입 & 위성 사출 (7.5 km/s)', col: '#a3e635' });
        }
        if (postT >= 60) s.status = 'completed';
      } else if (mMode === 'no_fairing_sep') {
        totalM = 3.0;
        // 6.4 km/s는 700km 원궤도 속도(7.5 km/s)보다 느려 원심력 부족으로 고도가 점점 강하함!
        targetAlt = Math.max(420, 614.0 - postT * 1.8);
        targetVel = 6.40;
        targetDown = 660.0 + postT * 1.8;
        accelGVal = -0.35;
        phaseMsg = '⚠️ 3단 연소 종료 — 속도 부족(6.4 km/s)으로 700km 궤도 진입 실패 (고도 강하 중)';
        fairingMsg = '❌ 1.5t 페어링 덮개 안에 위성 갇힘 (임무 실패)';
        if (prevT <= 755) {
          s.events.push({ down: 660.0, alt: 614.0, text: '⚠️ 속도 부족(6.4 km/s) → 궤도 미달 강하', col: '#f59e0b' });
        }
        if (postT >= 60) s.status = 'failed';
      }
    }

    if (s.status === 'launching') {
      s.alt = Number.isFinite(targetAlt) ? targetAlt : 0;
      s.vel = Number.isFinite(targetVel) ? targetVel : 0;
      s.downrange = Number.isFinite(targetDown) ? targetDown : 0;
      s.mass = Number.isFinite(totalM) ? totalM : 200.0;
      s.accel = accelGVal * 9.81;
    }

    // 분리된 낙하물(1단, 페어링, 2단) 물리 업데이트
    s.debris.forEach(d => {
      d.down += d.vx * safeDt;
      d.vy -= 0.012 * safeDt;
      d.alt = Math.max(0, d.alt + d.vy * safeDt * 8);
      d.rot += 0.04 * safeDt;
    });

    // 비행 궤적 기록
    if (s.path.length === 0 || Math.hypot(s.downrange - s.path[s.path.length - 1].down, s.alt - s.path[s.path.length - 1].alt) > 4) {
      s.path.push({ down: s.downrange, alt: s.alt });
    }

    let resultStr = '🚀 누리호 비행 진행 중...';
    if (s.status === 'completed') {
      resultStr = '🎉 [성공] 700km 우주 궤도 진입 및 위성 분리 성공! (최종 속도 7.5 km/s, 최종 질량 1.5t)';
    } else if (s.status === 'failed') {
      if (mMode === 'no_fairing_sep') {
        resultStr = '⚠️ [실패] 페어링 덮개(1.5t) 미분리 → 최종 속도 부족(6.4 km/s)으로 700km 궤도 안착 실패 및 고도 강하!';
      } else {
        resultStr = '❌ [실패] 다 탄 1·2단(24.5t) 미분리 → 최종 속도 2.1 km/s에 그쳐 고도 180km에서 해상 추락!';
      }
    }

    setTelemetry({
      time: Math.min(755, Math.round(t)),
      altKm: Math.max(0, +s.alt.toFixed(1)),
      velKms: Math.max(0, +s.vel.toFixed(2)),
      accelG: +accelGVal.toFixed(2),
      massTon: +s.mass.toFixed(1),
      phaseText: phaseMsg,
      fairingText: fairingMsg,
      resultText: resultStr
    });
  };

  /* 2D Canvas 렌더링 */
  const render2D = () => {
    const cvs = canvas2dRef.current;
    if (!cvs) return;
    const ctx = cvs.getContext('2d');
    const W = cvs.width, H = cvs.height;
    const s = simRef.current;
    const mMode = modeRef.current;

    // 1) 우주/대기권 배경
    const skyFactor = Math.max(0, 1 - s.alt / 150);
    const bgGrad = ctx.createLinearGradient(0, H, 0, 0);
    bgGrad.addColorStop(0, `rgb(${Math.round(14 + 70*skyFactor)}, ${Math.round(25 + 100*skyFactor)}, ${Math.round(52 + 150*skyFactor)})`);
    bgGrad.addColorStop(0.55, '#071026');
    bgGrad.addColorStop(1, '#020617');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // 2) 별 배경
    ctx.fillStyle = 'rgba(255,255,255,0.75)';
    for (let i = 0; i < 45; i++) {
      ctx.beginPath();
      ctx.arc((i * 53 + 17) % W, (i * 29 + 11) % (H * 0.72), (i % 3 === 0 ? 1.5 : 1), 0, Math.PI * 2);
      ctx.fill();
    }

    // 3) 고도 기준선: 목표 700 km 우주 궤도선 & 대기권 경계(100 km 카르만 라인)
    const y700 = to2D(0, 700, W, H).y;
    const y100 = to2D(0, 100, W, H).y;

    ctx.strokeStyle = 'rgba(163, 230, 53, 0.55)';
    ctx.lineWidth = 1.8;
    ctx.setLineDash([7, 5]);
    ctx.beginPath(); ctx.moveTo(40, y700); ctx.lineTo(W - 20, y700); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#a3e635';
    ctx.font = 'bold 11.5px Noto Sans KR';
    ctx.fillText('🎯 목표 우주 궤도 (고도 700 km · 필요 궤도 속도 7.5 km/s)', W - 335, y700 - 7);

    ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(40, y100); ctx.lineTo(W - 20, y100); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = 'rgba(148, 163, 184, 0.75)';
    ctx.font = '10.5px Noto Sans KR';
    ctx.fillText('대기권 경계 (고도 100 km)', W - 165, y100 - 5);

    // 4) 하단 지구 표면 및 바다 곡선
    ctx.fillStyle = '#0284c7';
    ctx.beginPath();
    ctx.arc(W / 2, H + 860, 900, 0, Math.PI * 2);
    ctx.fill();
    // 나로 우주센터 발사대
    ctx.fillStyle = '#334155';
    ctx.fillRect(54, H - 52, 28, 12);
    ctx.fillStyle = '#94a3b8';
    ctx.fillRect(58, H - 82, 4, 30);

    // 5) 다른 조건 비교용 기준 궤적 안내선 (연한 점선으로 정상 700km 궤적 표시)
    if (mMode !== 'normal') {
      ctx.strokeStyle = 'rgba(163, 230, 53, 0.22)';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      const p0 = to2D(0, 0, W, H);
      const p1 = to2D(240, 258, W, H);
      const p2 = to2D(740, 700, W, H);
      const p3 = to2D(860, 700, W, H);
      ctx.moveTo(p0.x, p0.y);
      ctx.quadraticCurveTo(p1.x, p1.y, p2.x, p2.y);
      ctx.lineTo(p3.x, p3.y);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // 6) 실제 비행 궤적 실선 그리기
    if (s.path.length > 1) {
      ctx.strokeStyle = mMode === 'normal' ? '#38bdf8' : (mMode === 'no_fairing_sep' ? '#f59e0b' : '#ef4444');
      ctx.lineWidth = 3;
      ctx.beginPath();
      s.path.forEach((pt, idx) => {
        const p = to2D(pt.down, pt.alt, W, H);
        if (idx === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      });
      ctx.stroke();
    }

    // 7) 주요 분리·이벤트 마커 표시
    s.events.forEach(ev => {
      const p = to2D(ev.down, ev.alt, W, H);
      ctx.fillStyle = ev.col;
      ctx.beginPath(); ctx.arc(p.x, p.y, 4.5, 0, Math.PI * 2); ctx.fill();
      ctx.font = 'bold 11px Noto Sans KR';
      ctx.fillText(ev.text, Math.min(W - 185, Math.max(15, p.x - 20)), Math.max(24, p.y - 10));
    });

    // 8) 분리되어 낙하하는 부품(1단, 페어링 좌·우, 2단) 렌더링
    s.debris.forEach(d => {
      if (d.alt <= 0) return;
      const p = to2D(d.down, d.alt, W, H);
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(d.rot);
      if (d.type === 'stage1') {
        ctx.fillStyle = '#e2e8f0'; ctx.fillRect(-5, -9, 10, 18);
        ctx.fillStyle = '#dc2626'; ctx.fillRect(-5, -3, 10, 3);
      } else if (d.type === 'stage2') {
        ctx.fillStyle = '#94a3b8'; ctx.fillRect(-4, -6, 8, 12);
      } else {
        ctx.fillStyle = '#ffffff';
        ctx.beginPath(); ctx.moveTo(-3, -6); ctx.lineTo(3, 0); ctx.lineTo(-3, 6); ctx.closePath(); ctx.fill();
      }
      ctx.restore();
    });

    // 9) 현재 로켓 / 위성 본체 렌더링
    const curP = to2D(s.downrange, s.alt, W, H);
    const rx = Math.max(60, Math.min(W - 45, curP.x));
    const ry = Math.max(28, Math.min(H - 35, curP.y));

    let pitchAngle = Math.max(0.02, (Math.PI / 2) * Math.exp(-s.downrange / 240));
    if (mMode === 'normal' && s.t >= 755) pitchAngle = 0; // 700km 원궤도 수평 비행
    if (mMode === 'no_fairing_sep' && s.t > 680) pitchAngle = -0.22; // 궤도 미달 하강 기울기
    if (mMode === 'no_stage_sep' && s.t > 240) pitchAngle = -0.65;   // 해상 추락 기울기

    ctx.save();
    ctx.translate(rx, ry);
    ctx.rotate(Math.PI / 2 - pitchAngle);

    // 엔진 화염
    if (s.t > 0 && s.t < 755 && s.status === 'launching') {
      const flameY = !s.stage1Sep ? 22 : (!s.stage2Sep ? 4 : -12);
      const flameGrad = ctx.createLinearGradient(0, flameY, 0, flameY + 26);
      flameGrad.addColorStop(0, '#ffffff');
      flameGrad.addColorStop(0.35, '#38bdf8');
      flameGrad.addColorStop(1, 'rgba(239,68,68,0)');
      ctx.fillStyle = flameGrad;
      ctx.beginPath();
      ctx.moveTo(-5, flameY);
      ctx.lineTo(0, flameY + 22 + Math.random() * 6);
      ctx.lineTo(5, flameY);
      ctx.closePath();
      ctx.fill();
    }

    // 1단
    if (!s.stage1Sep) {
      ctx.fillStyle = '#f8fafc'; ctx.fillRect(-8, 2, 16, 20);
      ctx.fillStyle = '#dc2626'; ctx.fillRect(-8, 6, 16, 3);
    }
    // 2단
    if (!s.stage2Sep) {
      ctx.fillStyle = '#cbd5e1'; ctx.fillRect(-6, -14, 12, 16);
    }
    // 3단 (위성 단독 사출 전까지 표시)
    if (!s.satDeployed) {
      ctx.fillStyle = '#64748b'; ctx.fillRect(-5, -26, 10, 12);
    }

    // 페어링 또는 위성
    if (!s.fairingSep) {
      ctx.fillStyle = mMode !== 'normal' && s.t >= 204 ? '#fca5a5' : '#ffffff';
      ctx.strokeStyle = mMode !== 'normal' && s.t >= 204 ? '#ef4444' : '#cbd5e1';
      ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(-6, -26); ctx.quadraticCurveTo(0, -44, 6, -26); ctx.closePath();
      ctx.fill(); ctx.stroke();
    } else {
      // 황금색 인공위성 본체
      ctx.fillStyle = '#fbbf24'; ctx.fillRect(-5, -35, 10, 9);
      if (s.satDeployed) {
        // 태양전지판 전개!
        ctx.fillStyle = '#0284c7';
        ctx.strokeStyle = '#bae6fd';
        ctx.lineWidth = 1;
        ctx.fillRect(-20, -34, 13, 7); ctx.strokeRect(-20, -34, 13, 7);
        ctx.fillRect(7, -34, 13, 7);   ctx.strokeRect(7, -34, 13, 7);
      }
    }
    ctx.restore();

    // 페어링 미분리 경고 말풍선 (로켓 위)
    if (mMode === 'no_fairing_sep' && s.t >= 204) {
      ctx.fillStyle = '#fbbf24';
      ctx.font = 'bold 11.5px Noto Sans KR';
      ctx.fillText('⚠️ 1.5t 덮개 고착! (속도 부족)', Math.min(W - 170, rx - 30), Math.max(22, ry - 26));
    }

    // 좌측 상단 HUD
    ctx.fillStyle = 'rgba(11, 19, 43, 0.88)';
    ctx.strokeStyle = mMode === 'normal' ? '#2563eb' : (mMode === 'no_fairing_sep' ? '#d97706' : '#dc2626');
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.roundRect(12, 12, 315, 86, 8); ctx.fill(); ctx.stroke();

    ctx.fillStyle = '#60a5fa'; ctx.font = 'bold 11.5px Noto Sans KR';
    const modeTitle = mMode === 'normal' ? '🟢 정상 다단·덮개 분리' : (mMode === 'no_fairing_sep' ? '⚠️ 페어링(덮개) 미분리' : '❌ 단분리 미실시');
    ctx.fillText(`${modeTitle} (t = ${Math.min(755, Math.round(s.t))}초)`, 20, 30);
    ctx.fillStyle = '#e2e8f0'; ctx.font = 'bold 11.5px Space Mono';
    ctx.fillText(`고도(h): ${s.alt.toFixed(1)} km / 700 km | 속도: ${s.vel.toFixed(2)} km/s`, 20, 50);
    ctx.fillStyle = '#fbbf24';
    ctx.fillText(`현재 총 질량(m): ${s.mass.toFixed(1)} 톤`, 20, 70);
    ctx.fillStyle = s.status === 'completed' ? '#a3e635' : (s.status === 'failed' ? '#fca5a5' : '#93c5fd');
    ctx.font = 'bold 11px Noto Sans KR';
    ctx.fillText(s.status === 'completed' ? '✅ 700km 원궤도 진입 & 위성 사출 성공!' : (s.status === 'failed' ? '❌ 궤도 진입 실패 (속도·고도 미달)' : `현재 상태: ${s.fairingSep ? '페어링 분리됨' : '페어링 닫힘'}`), 20, 88);
  };

  /* Three.js 3D 씬 초기화 (폴링 및 세이프티 로드) */
  useEffect(() => {
    if (viewMode !== '3d') return;
    const container = containerRef.current;
    if (!container) return;

    let timerId = null;

    const init3D = () => {
      const THREE = window.THREE;
      if (!THREE) {
        timerId = setTimeout(init3D, 150);
        return;
      }

      const W = container.clientWidth || 800;
      const H = 400;

      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x040814);

      const camera = new THREE.PerspectiveCamera(45, W / H, 0.1, 5000);
      camera.position.set(0, 15, 60);

      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(W, H);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      container.innerHTML = '';
      container.appendChild(renderer.domElement);

      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);

      const sunLight = new THREE.DirectionalLight(0xffffff, 1.2);
      sunLight.position.set(200, 150, 100);
      scene.add(sunLight);

      // 지구
      const earthGeo = new THREE.SphereGeometry(120, 48, 48);
      const earthMat = new THREE.MeshPhongMaterial({ color: 0x1d4ed8, emissive: 0x06112d, specular: 0x38bdf8, shininess: 20 });
      const earthMesh = new THREE.Mesh(earthGeo, earthMat);
      earthMesh.position.set(0, -120, 0);
      scene.add(earthMesh);

      // 로켓 그룹
      const rocketGroup = new THREE.Group();
      rocketGroup.position.set(0, 0.5, 0);

      const stage1Mesh = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.5, 14, 20), new THREE.MeshStandardMaterial({ color: 0xf8fafc }));
      stage1Mesh.position.set(0, 7, 0); rocketGroup.add(stage1Mesh);

      const stage2Mesh = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.3, 8, 20), new THREE.MeshStandardMaterial({ color: 0xcbd5e1, metalness: 0.5 }));
      stage2Mesh.position.set(0, 18, 0); rocketGroup.add(stage2Mesh);

      const stage3Mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 1.0, 5, 20), new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.7 }));
      stage3Mesh.position.set(0, 24.5, 0); rocketGroup.add(stage3Mesh);

      const fMat = new THREE.MeshStandardMaterial({ color: 0xffffff });
      const fairingLeft = new THREE.Mesh(new THREE.ConeGeometry(0.9, 4.5, 20, 1, false, 0, Math.PI), fMat);
      fairingLeft.position.set(0, 29.25, 0); rocketGroup.add(fairingLeft);

      const fairingRight = new THREE.Mesh(new THREE.ConeGeometry(0.9, 4.5, 20, 1, false, Math.PI, Math.PI), fMat);
      fairingRight.position.set(0, 29.25, 0); rocketGroup.add(fairingRight);

      scene.add(rocketGroup);

      const s = simRef.current;
      s.scene = scene; s.camera = camera; s.renderer = renderer;
      s.rocketGroup = rocketGroup; s.stage1Mesh = stage1Mesh; s.stage2Mesh = stage2Mesh;
      s.fairingLeft = fairingLeft; s.fairingRight = fairingRight;
      s.is3DInited = true;
    };

    init3D();

    return () => {
      if (timerId) clearTimeout(timerId);
      const s = simRef.current;
      s.is3DInited = false;
    };
  }, [viewMode]);

  /* 3D 위치 및 카메라 연동 */
  const render3D = () => {
    const s = simRef.current;
    if (!s.is3DInited || !s.renderer || !s.scene || !s.camera) return;

    const scaleAlt = (s.alt / 700) * 180;
    const scaleX = (s.downrange / 800) * 220;

    s.rocketGroup.position.set(scaleX, scaleAlt + 0.5, 0);
    const pitch = Math.max(0, (Math.PI / 2) * Math.exp(-s.alt / 220));
    s.rocketGroup.rotation.z = -((Math.PI / 2) - pitch);

    if (s.stage1Sep && s.stage1Mesh) {
      s.stage1Mesh.position.y -= 0.4;
      s.stage1Mesh.rotation.z += 0.02;
    }
    if (s.fairingSep && s.fairingLeft && s.fairingRight) {
      s.fairingLeft.position.x -= 0.2; s.fairingLeft.rotation.z += 0.03;
      s.fairingRight.position.x += 0.2; s.fairingRight.rotation.z -= 0.03;
    }

    if (camRef.current === 'follow') {
      s.camera.position.set(scaleX - 25, scaleAlt + 18, 45);
      s.camera.lookAt(scaleX, scaleAlt + 5, 0);
    } else if (camRef.current === 'orbit') {
      s.camera.position.set(120, 150, 260);
      s.camera.lookAt(0, 50, 0);
    } else {
      s.camera.position.set(12, 6, 25);
      s.camera.lookAt(0, 10, 0);
    }

    s.renderer.render(s.scene, s.camera);
  };

  /* 비행 시뮬레이션 애니메이션 루프 */
  const startLaunch = () => {
    cancelAnimationFrame(animRef.current);
    const s = simRef.current;
    s.t = 0; s.alt = 0; s.vel = 0; s.mass = 200.0; s.downrange = 0;
    s.stage1Sep = false; s.fairingSep = false; s.stage2Sep = false; s.satDeployed = false;
    s.path = [{ down: 0, alt: 0 }]; s.debris = []; s.events = [];
    s.status = 'launching';

    if (s.rocketGroup) {
      s.rocketGroup.position.set(0, 0.5, 0);
      s.rocketGroup.rotation.set(0, 0, 0);
    }
    if (s.stage1Mesh) { s.stage1Mesh.position.set(0, 7, 0); s.stage1Mesh.rotation.set(0, 0, 0); }
    if (s.fairingLeft) { s.fairingLeft.position.set(0, 29.25, 0); s.fairingLeft.rotation.set(0, 0, 0); }
    if (s.fairingRight) { s.fairingRight.position.set(0, 29.25, 0); s.fairingRight.rotation.set(0, 0, 0); }

    setSimState('launching');

    let lastNow = null;
    const step = (now) => {
      if (lastNow === null) lastNow = now;
      const dtReal = Math.max(0.001, Math.min(0.05, (now - lastNow) / 1000));
      lastNow = now;
      const dtSim = dtReal * speedRef.current * 14.0;

      if (s.status === 'launching') {
        updatePhysics(dtSim);
        if (viewModeRef.current === '3d' && s.is3DInited) render3D();
        else render2D();

        animRef.current = requestAnimationFrame(step);
      } else {
        if (viewModeRef.current === '3d' && s.is3DInited) render3D();
        else render2D();
        setSimState(s.status);
      }
    };
    animRef.current = requestAnimationFrame(step);
  };

  const resetSim = () => {
    cancelAnimationFrame(animRef.current);
    const s = simRef.current;
    s.t = 0; s.alt = 0; s.vel = 0; s.mass = 200.0; s.downrange = 0;
    s.stage1Sep = false; s.fairingSep = false; s.stage2Sep = false; s.satDeployed = false;
    s.path = []; s.debris = []; s.events = [];
    s.status = 'ready';

    if (s.rocketGroup) {
      s.rocketGroup.position.set(0, 0.5, 0);
      s.rocketGroup.rotation.set(0, 0, 0);
    }
    if (s.stage1Mesh) { s.stage1Mesh.position.set(0, 7, 0); s.stage1Mesh.rotation.set(0, 0, 0); }
    if (s.fairingLeft) { s.fairingLeft.position.set(0, 29.25, 0); s.fairingLeft.rotation.set(0, 0, 0); }
    if (s.fairingRight) { s.fairingRight.position.set(0, 29.25, 0); s.fairingRight.rotation.set(0, 0, 0); }

    setSimState('ready');
    setTelemetry({
      time: 0, altKm: 0, velKms: 0, accelG: 0, massTon: 200.0,
      phaseText: '발사대 대기 중', fairingText: '위성 덮개 닫힘 (공기 저항 방어)', resultText: '발사 버튼을 눌러보세요!'
    });

    if (viewModeRef.current === '3d' && s.is3DInited) render3D();
    else render2D();
  };

  useEffect(() => {
    resetSim();
  }, [mode, viewMode]);

  return (
    <div>
      {/* 카드 1 */}
      <div className="card">
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',flexWrap:'wrap',gap:12}}>
          <div>
            <span className="badge badge-lime">2D 궤도 뷰 & 3D 입체 뷰 모두 지원</span>
            <h3 style={{fontSize:16,fontWeight:800,color:'#f8fafc',marginTop:4}}>
              지상 발사대 ~ 700km 우주 궤도 진입 비행 가상실험
            </h3>
            <p style={{fontSize:13,color:'#94a3b8',lineHeight:1.6,marginTop:4}}>
              나로 우주센터 지상 발사대에서 시속 27,000km(초속 7.5km) 우주 궤도로 올라가는 누리호의 비행 과정을 관찰하고, 
              <b>'왜 다 탄 1단·2단과 위성 덮개를 제때 버려야만 궤도에 들어갈 수 있는지'</b> 3가지 조건으로 비교해 보세요.
            </p>
          </div>
          
          <div style={{display:'flex',gap:12,alignItems:'center',flexWrap:'wrap'}}>
            <div>
              <span style={{fontSize:11.5,color:'#cbd5e1',fontWeight:700,marginRight:6}}>🖼️ 화면 뷰 전환:</span>
              <button className="btn-secondary" style={{padding:'5px 12px',fontSize:12,background:viewMode==='2d'?'#2563eb':undefined,color:viewMode==='2d'?'#fff':undefined}} onClick={()=>setViewMode('2d')}>
                🚀 2D 궤도 뷰 (추천)
              </button>
              <button className="btn-secondary" style={{padding:'5px 12px',fontSize:12,background:viewMode==='3d'?'#2563eb':undefined,color:viewMode==='3d'?'#fff':undefined,marginLeft:4}} onClick={()=>setViewMode('3d')}>
                🌌 3D 입체 뷰
              </button>
            </div>

            {viewMode==='3d' && (
              <div>
                <span style={{fontSize:11.5,color:'#cbd5e1',fontWeight:700,marginRight:6}}>🎥 3D 시점:</span>
                <button className="btn-secondary" style={{padding:'4px 8px',fontSize:11,background:cameraView==='follow'?'#2563eb':undefined}} onClick={()=>setCameraView('follow')}>
                  로켓 추적
                </button>
                <button className="btn-secondary" style={{padding:'4px 8px',fontSize:11,background:cameraView==='orbit'?'#2563eb':undefined,marginLeft:3}} onClick={()=>setCameraView('orbit')}>
                  지구 전체
                </button>
              </div>
            )}

            <div>
              <span style={{fontSize:11.5,color:'#cbd5e1',fontWeight:700,marginRight:6}}>⚡ 배속:</span>
              {[1, 2, 5, 10].map(sp => (
                <button key={sp} className="btn-secondary"
                  style={{padding:'4px 8px',fontSize:11,background:speedMult===sp?'#2563eb':undefined,color:speedMult===sp?'#fff':undefined}}
                  onClick={()=>setSpeedMult(sp)}>
                  {sp}x
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 3가지 실험 모드 버튼 */}
      <div className="card" style={{background:'#080e20',borderColor:'#1e3a8a'}}>
        <span style={{fontSize:13,fontWeight:800,color:'#38bdf8',display:'block',marginBottom:10}}>
          🎛️ 발사 조건 선택 (위성 덮개 & 다단 로켓 분리 설정)
        </span>
        
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(280px, 1fr))',gap:12}}>
          <div style={{
            background: mode==='normal' ? 'rgba(37,99,235,0.18)' : '#0f172a',
            border: `2px solid ${mode==='normal'?'#3b82f6':'#1e293b'}`,
            borderRadius:10, padding:12, cursor:'pointer'
          }} onClick={()=>setMode('normal')}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:4}}>
              <span style={{fontWeight:800,color:'#60a5fa',fontSize:13.5}}>🟢 정상 다단 & 덮개 분리</span>
              <span className="badge badge-lime">정상 궤도 진입</span>
            </div>
            <p style={{fontSize:11.5,color:'#cbd5e1',lineHeight:1.5}}>
              • 125초: 1단 분리 (20톤 무거운 짐 제거)<br/>
              • 204초: 페어링 덮개 분리 (1.5톤 제거)<br/>
              • 255초: 2단 분리 (4.5톤 제거)<br/>
              <b>👉 최종속도 7.5 km/s (700km 궤도 안착 성공)</b>
            </p>
          </div>

          <div style={{
            background: mode==='no_fairing_sep' ? 'rgba(245,158,11,0.18)' : '#0f172a',
            border: `2px solid ${mode==='no_fairing_sep'?'#f59e0b':'#1e293b'}`,
            borderRadius:10, padding:12, cursor:'pointer'
          }} onClick={()=>setMode('no_fairing_sep')}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:4}}>
              <span style={{fontWeight:800,color:'#fbbf24',fontSize:13.5}}>⚠️ 페어링 미분리 (덮개 고장)</span>
              <span className="badge badge-amber">속도 부족 궤도 실패</span>
            </div>
            <p style={{fontSize:11.5,color:'#cbd5e1',lineHeight:1.5}}>
              • 1단/2단은 버렸으나,<br/>
              • 대기권 밖(204초)에서 <b>1.5톤 덮개 안 열림!</b><br/>
              <b>👉 최종속도 6.4 km/s (무게 때문에 속도 부족)</b>
            </p>
          </div>

          <div style={{
            background: mode==='no_stage_sep' ? 'rgba(239,68,68,0.18)' : '#0f172a',
            border: `2px solid ${mode==='no_stage_sep'?'#ef4444':'#1e293b'}`,
            borderRadius:10, padding:12, cursor:'pointer'
          }} onClick={()=>setMode('no_stage_sep')}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:4}}>
              <span style={{fontWeight:800,color:'#fca5a5',fontSize:13.5}}>❌ 단분리 미실시 (다 탄 껍데기 짐)</span>
              <span className="badge badge-red">해상 추락 진입 실패</span>
            </div>
            <p style={{fontSize:11.5,color:'#cbd5e1',lineHeight:1.5}}>
              • 다 탄 빈 1단(20t) & 2단(4.5t) 껍데기를<br/>
              • 버리지 않고 끝까지 끌고 올라감!<br/>
              <b>👉 최종속도 2.1 km/s (무게에 눌려 추락)</b>
            </p>
          </div>
        </div>
      </div>

      {/* 캔버스 뷰 디스플레이 */}
      <div className="card" style={{padding:6,position:'relative'}}>
        {viewMode === '3d' ? (
          <div ref={containerRef} style={{width:'100%',height:'400px',borderRadius:10,overflow:'hidden',background:'#040814'}}/>
        ) : (
          <canvas ref={canvas2dRef} width={800} height={360} style={{width:'100%',height:'360px',borderRadius:10,background:'#030712',display:'block'}}/>
        )}

        {/* 컨트롤 버튼 바 */}
        <div style={{display:'flex',justifyContent:'center',gap:14,marginTop:12,flexWrap:'wrap'}}>
          <button className="btn-success" onClick={startLaunch} disabled={simState==='launching'}
            style={{padding:'10px 30px',fontSize:14.5,boxShadow:'0 0 16px rgba(22,163,74,0.4)'}}>
            🚀 {simState==='launching'?'누리호 비행 가속 중...':'누리호 비행 발사 개시!'}
          </button>
          <button className="btn-secondary" onClick={resetSim}
            style={{padding:'10px 20px',fontSize:13}}>
            🔄 발사대 리셋 (초기화)
          </button>
        </div>
      </div>

      {/* 실시간 텔레메트리 계측 HUD */}
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(200px, 1fr))',gap:12,marginBottom:14}}>
        <div style={{background:'#0a1224',padding:12,borderRadius:10,border:'1px solid #1e293b'}}>
          <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>⏱️ 발사 후 경과 시간</span>
          <span className="num-mono" style={{fontSize:22,fontWeight:800,color:'#60a5fa'}}>
            {telemetry.time} <span style={{fontSize:13,color:'#94a3b8'}}>초</span>
          </span>
        </div>

        <div style={{background:'#0a1224',padding:12,borderRadius:10,border:'1px solid #1e293b'}}>
          <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>🚀 현재 비행 속도</span>
          <span className="num-mono" style={{fontSize:22,fontWeight:800,color:'#38bdf8'}}>
            {telemetry.velKms} <span style={{fontSize:13,color:'#94a3b8'}}>km/s</span>
          </span>
        </div>

        <div style={{background:'#0a1224',padding:12,borderRadius:10,border:'1px solid #1e293b'}}>
          <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>🛰️ 비행 고도</span>
          <span className="num-mono" style={{fontSize:22,fontWeight:800,color:'#a3e635'}}>
            {telemetry.altKm} <span style={{fontSize:13,color:'#94a3b8'}}>km</span>
          </span>
        </div>

        <div style={{background:'#0a1224',padding:12,borderRadius:10,border:'1px solid #1e293b'}}>
          <span style={{fontSize:11,color:'#94a3b8',display:'block'}}>⚖️ 발사체 전체 남은 무게</span>
          <span className="num-mono" style={{fontSize:22,fontWeight:800,color:'#fbbf24'}}>
            {telemetry.massTon} <span style={{fontSize:13,color:'#94a3b8'}}>톤</span>
          </span>
        </div>
      </div>

      {/* 상태 안내 배너 */}
      <div className="card" style={{background:'#0a1020',border:'1px solid #2563eb'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',flexWrap:'wrap',gap:10}}>
          <div>
            <span style={{fontSize:12,color:'#94a3b8'}}>비행 단계: </span>
            <span style={{fontSize:13.5,fontWeight:700,color:'#f8fafc',marginLeft:4}}>{telemetry.phaseText}</span>
            <span style={{fontSize:12,color:'#38bdf8',marginLeft:12}}>{telemetry.fairingText}</span>
          </div>
          <div style={{fontWeight:800,fontSize:14,color:telemetry.resultText.includes('성공')?'#a3e635':'#fca5a5'}}>
            {telemetry.resultText}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 2: 3가지 발사 조건 정량적 데이터 비교 표 & 그래프
══════════════════════════════════════════════════ */
function DataTableTab() {
  return (
    <div>
      <div className="card">
        <h3 style={{fontSize:16,fontWeight:800,color:'#f8fafc',marginBottom:8}}>
          📊 3가지 발사 조건 정량적 최종 속도/질량 데이터 비교표
        </h3>
        <p style={{fontSize:13,color:'#94a3b8',lineHeight:1.6}}>
          세 가지 발사 조건에서 <b>'최종 남아있는 무게(m_f)'</b>가 속도에 얼마나 결정적인 영향을 주는지 수치 데이터로 직접 비교합니다.
        </p>
      </div>

      <div className="card" style={{background:'#080e1e',borderColor:'#2563eb'}}>
        <span style={{fontSize:14,fontWeight:800,color:'#60a5fa',display:'block',marginBottom:12}}>
          📋 3가지 경우의 최종 속도 및 궤도 진입 결과 정량 비교표
        </span>

        <table className="table-custom">
          <thead>
            <tr>
              <th style={{width:'22%'}}>발사 조건 구분</th>
              <th style={{width:'15%'}}>최종 남은 무게 (m_f)</th>
              <th style={{width:'18%'}}>최종 달성 최고 속도 (v_최종)</th>
              <th style={{width:'15%'}}>목표 고도 도달</th>
              <th style={{width:'15%'}}>우주 궤도 안착</th>
              <th style={{width:'15%'}}>쉬운 결과 원인 분석</th>
            </tr>
          </thead>
          <tbody>
            <tr style={{background:'rgba(16,185,129,0.08)'}}>
              <td style={{textAlign:'left',fontWeight:800,color:'#a3e635'}}>
                🟢 1) 정상 다단 & 덮개 분리
              </td>
              <td className="num-mono" style={{fontWeight:800,color:'#a3e635'}}>
                1.5 톤<br/><span style={{fontSize:10,color:'#94a3b8'}}>(위성 짐만 남음)</span>
              </td>
              <td className="num-mono" style={{fontSize:16,fontWeight:800,color:'#38bdf8'}}>
                7.5 km/s<br/><span style={{fontSize:10,color:'#64748b'}}>(약 27,000 km/h)</span>
              </td>
              <td style={{fontWeight:700,color:'#a3e635'}}>700 km 성공</td>
              <td><span className="badge badge-lime">🎉 성공</span></td>
              <td style={{fontSize:11.5,textAlign:'left',color:'#cbd5e1'}}>
                다 탄 1단/2단과 덮개를 다 버려서 무게가 1.5t으로 가벼워져 최고 속도에 도달함!
              </td>
            </tr>

            <tr style={{background:'rgba(245,158,11,0.08)'}}>
              <td style={{textAlign:'left',fontWeight:800,color:'#fbbf24'}}>
                ⚠️ 2) 페어링 미분리 (덮개 고장)
              </td>
              <td className="num-mono" style={{fontWeight:800,color:'#fbbf24'}}>
                3.0 톤<br/><span style={{fontSize:10,color:'#94a3b8'}}>(위성 1.5t + 덮개 1.5t)</span>
              </td>
              <td className="num-mono" style={{fontSize:16,fontWeight:800,color:'#f59e0b'}}>
                6.4 km/s<br/><span style={{fontSize:10,color:'#64748b'}}>(속도 1.1 km/s 부족!)</span>
              </td>
              <td style={{fontWeight:700,color:'#fbbf24'}}>620 km 저하</td>
              <td><span className="badge badge-amber">⚠️ 실패</span></td>
              <td style={{fontSize:11.5,textAlign:'left',color:'#cbd5e1'}}>
                대기권 밖에서 쓸데없는 1.5t 덮개 무게를 끌고 가느라 속도가 모자람!
              </td>
            </tr>

            <tr style={{background:'rgba(239,68,68,0.08)'}}>
              <td style={{textAlign:'left',fontWeight:800,color:'#fca5a5'}}>
                ❌ 3) 단분리 미실시 (다 탄 껍데기)
              </td>
              <td className="num-mono" style={{fontWeight:800,color:'#fca5a5'}}>
                26.0 톤<br/><span style={{fontSize:10,color:'#94a3b8'}}>(다 탄 1/2단 24.5t 포함)</span>
              </td>
              <td className="num-mono" style={{fontSize:16,fontWeight:800,color:'#ef4444'}}>
                2.1 km/s<br/><span style={{fontSize:10,color:'#64748b'}}>(속도 5.4 km/s 부족!)</span>
              </td>
              <td style={{fontWeight:700,color:'#fca5a5'}}>180 km 불과</td>
              <td><span className="badge badge-red">❌ 추락</span></td>
              <td style={{fontSize:11.5,textAlign:'left',color:'#cbd5e1'}}>
                다 탄 빈 로켓 24.5t 무거운 짐에 눌려 가속을 못 하고 바다로 추락함!
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(340px, 1fr))',gap:14,marginTop:14}}>
        <div className="card">
          <span style={{fontSize:13.5,fontWeight:700,color:'#38bdf8',display:'block',marginBottom:8}}>
            🚀 1. 속도-시간 변화 그래프 (v-t)
          </span>
          <svg width="100%" height="190" viewBox="0 0 320 190">
            <rect x="0" y="0" width="320" height="190" fill="#070c18" rx="8"/>
            <line x1="40" y1="20" x2="40" y2="160" stroke="#1e293b"/>
            <line x1="40" y1="160" x2="300" y2="160" stroke="#1e293b"/>
            <text x="35" y="25" fill="#64748b" fontSize="9" textAnchor="end">7.5 km/s</text>
            <text x="35" y="164" fill="#64748b" fontSize="9" textAnchor="end">0</text>
            <path d="M 40 160 Q 75 135, 100 120 T 170 80 T 300 25" fill="none" stroke="#38bdf8" strokeWidth="2.5"/>
            <path d="M 40 160 Q 75 135, 100 120 T 170 90 T 300 55" fill="none" stroke="#f59e0b" strokeWidth="2" strokeDasharray="4,2"/>
            <path d="M 40 160 Q 75 135, 100 120 T 170 140 T 300 150" fill="none" stroke="#ef4444" strokeWidth="2" strokeDasharray="2,2"/>
          </svg>
        </div>

        <div className="card">
          <span style={{fontSize:13.5,fontWeight:700,color:'#a3e635',display:'block',marginBottom:8}}>
            ⚖️ 2. 발사체 무게 변화 그래프 (m-t)
          </span>
          <svg width="100%" height="190" viewBox="0 0 320 190">
            <rect x="0" y="0" width="320" height="190" fill="#070c18" rx="8"/>
            <line x1="40" y1="20" x2="40" y2="160" stroke="#1e293b"/>
            <line x1="40" y1="160" x2="300" y2="160" stroke="#1e293b"/>
            <text x="35" y="25" fill="#64748b" fontSize="9" textAnchor="end">200톤</text>
            <text x="35" y="164" fill="#64748b" fontSize="9" textAnchor="end">0</text>
            <path d="M 40 25 L 85 95 L 85 120 L 115 145 L 115 147 L 140 158 L 300 160" fill="none" stroke="#a3e635" strokeWidth="2.5"/>
          </svg>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 3: 쉬운 설명으로 풀어쓴 물리 공식 해설
══════════════════════════════════════════════════ */
function MathTab() {
  return (
    <div>
      <div className="hl-box">
        <h3 style={{fontSize:16,fontWeight:800,color:'#93c5fd',marginBottom:8}}>
          📐 1. 쉬운 공식 해설: 로켓 속도 증가량 공식 (찌올콥스키 공식)
        </h3>
        <p style={{fontSize:13.5,color:'#e2e8f0',lineHeight:1.8}}>
          로켓이 엔진을 태워 늘릴 수 있는 속도량 <Eq f="\Delta v"/>는 아래 공식으로 계산됩니다.
        </p>
        <div style={{background:'rgba(15,23,42,0.6)',padding:12,borderRadius:8,marginTop:10,textAlign:'center'}}>
          <Eq f="\Delta v = v_e \cdot \ln \left( \frac{\text{초기 전체 무게 } m_0}{\text{마지막 남은 무게 } m_f} \right)" display={true}/>
        </div>
        <p style={{fontSize:12.5,color:'#cbd5e1',marginTop:10,lineHeight:1.6}}>
          💡 <b>쉽게 이해하기:</b> 마지막에 남은 무게 <Eq f="m_f"/>가 <b>가벼우면 가벼울수록(분모가 작을수록)</b> 
          로켓이 얻는 속도 <Eq f="\Delta v"/>가 훨씬 더 폭발적으로 커집니다! 이것이 다 탄 1단/2단 로켓과 위성 덮개를 버리는 이유입니다.
        </p>
      </div>

      <div className="card">
        <h3 style={{fontSize:15,fontWeight:800,color:'#fbbf24',marginBottom:10}}>
          🛡️ 2. 페어링(위성 보호 덮개)을 버려야만 하는 이유
        </h3>
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(280px, 1fr))',gap:14}}>
          <div style={{background:'#0a1020',padding:14,borderRadius:10,border:'1px solid #1e293b'}}>
            <span style={{fontSize:13,fontWeight:700,color:'#38bdf8'}}>1단계: 지상 ~ 고도 100km 대기권 통과</span>
            <p style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.7,marginTop:6}}>
              • 공기가 빽빽해서 1,000℃ 넘는 뜨거운 공기 마찰과 센 바람 압력이 밀려옴.<br/>
              • <b>위성을 안전하게 보호하기 위해 덮개(페어링)가 필수!</b>
            </p>
          </div>

          <div style={{background:'#0a1020',padding:14,borderRadius:10,border:'1px solid #1e293b'}}>
            <span style={{fontSize:13,fontWeight:700,color:'#a3e635'}}>2단계: 고도 190km 이상 우주 진공</span>
            <p style={{fontSize:12.5,color:'#cbd5e1',lineHeight:1.7,marginTop:6}}>
              • 공기가 거의 없어 마찰열 방어 필요성이 완전히 사라짐.<br/>
              • 이때 1.5톤 덮개를 버리지 않으면 <b>쓸데없는 무거운 짐</b>이 되어 로켓 가속을 방해함.<br/>
              • <b>누리호는 204초(고도 191km)에 덮개 2개를 즉시 툭 버림!</b>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════
   탭 4: 탐구 보고서 & 학생 퀴즈
══════════════════════════════════════════════════ */
function ReportTab() {
  const [answers, setAnswers] = useState({ q1: '', q2: '' });
  const [submitted, setSubmitted] = useState(false);

  return (
    <div>
      <div className="card">
        <h3 style={{fontSize:15,fontWeight:800,color:'#f8fafc',marginBottom:8}}>
          📝 쉬운 개념 확인 퀴즈 (학생용)
        </h3>
        <p style={{fontSize:13,color:'#94a3b8'}}>
          시뮬레이터에서 관찰한 내용을 떠올리며 문제의 정답을 골라보세요.
        </p>
      </div>

      <div className="card">
        <p style={{fontWeight:700,fontSize:13.5,color:'#38bdf8',marginBottom:8}}>
          Q1. 누리호가 고도 191km(발사 후 204초) 우주 공간에 도달했을 때 페어링(위성 덮개)을 떨어뜨려 버리는 가장 큰 이유는?
        </p>
        <div style={{display:'flex',flexDirection:'column',gap:6,fontSize:12.5}}>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q1" value="1" onChange={e=>setAnswers({...answers, q1:e.target.value})}/> 1) 덮개 속에 들어있는 연료를 태우기 위해
          </label>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q1" value="2" onChange={e=>setAnswers({...answers, q1:e.target.value})}/> 2) 대기권을 나가 공기 마찰 방어가 불필요해졌으므로 1.5톤의 쓸데없는 무게를 버려 로켓 속도를 더 올리기 위해
          </label>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q1" value="3" onChange={e=>setAnswers({...answers, q1:e.target.value})}/> 3) 지구 중력을 끄기 위해
          </label>
        </div>
        {submitted && (
          <p style={{fontSize:12,marginTop:8,color:answers.q1==='2'?'#a3e635':'#fca5a5',fontWeight:700}}>
            {answers.q1==='2' ? '정답입니다! 👏 공기가 없는 우주에서는 덮개가 불필요한 무거운 짐이 되므로 버려야 초속 7.5km에 도달할 수 있습니다.' : '❌ 오답입니다. 정답은 2번입니다.'}
          </p>
        )}
      </div>

      <div className="card">
        <p style={{fontWeight:700,fontSize:13.5,color:'#38bdf8',marginBottom:8}}>
          Q2. 다 탄 1단, 2단 로켓 껍데기를 버리지 않고 끝까지 끌고 올라가면 어떤 일이 일어날까요?
        </p>
        <div style={{display:'flex',flexDirection:'column',gap:6,fontSize:12.5}}>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q2" value="1" onChange={e=>setAnswers({...answers, q2:e.target.value})}/> 1) 발사체가 무거운 짐에 눌려 가속을 못 하고 속도가 부족해 바다로 추락한다.
          </label>
          <label style={{cursor:'pointer'}}>
            <input type="radio" name="q2" value="2" onChange={e=>setAnswers({...answers, q2:e.target.value})}/> 2) 무거울수록 더 빠른 속도를 내서 우주 멀리 나아간다.
          </label>
        </div>
        {submitted && (
          <p style={{fontSize:12,marginTop:8,color:answers.q2==='1'?'#a3e635':'#fca5a5',fontWeight:700}}>
            {answers.q2==='1' ? '정답입니다! 👏 다 탄 껍데기 24.5톤을 끌고 가면 무게에 눌려 속도를 못 냅니다.' : '❌ 오답입니다. 정답은 1번입니다.'}
          </p>
        )}
      </div>

      <div style={{textAlign:'center',marginTop:14}}>
        <button className="btn-primary" onClick={()=>setSubmitted(true)} style={{padding:'10px 24px',fontSize:14}}>
          📊 정답 제출하기
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

components.html(REACT_HTML, height=960, scrolling=True)
