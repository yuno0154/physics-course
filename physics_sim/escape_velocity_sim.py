import streamlit as st
import streamlit.components.v1 as components

st.sidebar.title("🚀 탈출속도 탐구")
st.sidebar.markdown("천체를 탈출하기 위한 최소 속도를 탐구합니다.")

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
.tab-btn.active{background:#1d4ed8;border-color:#3b82f6;color:#fff;}
.tab-btn:hover:not(.active){border-color:#334155;color:#e2e8f0;}
.card{background:#0d1526;border:1px solid #1e293b;border-radius:14px;padding:18px;margin-bottom:14px;}
.hl-box{background:linear-gradient(135deg,#0c1a3a,#0f2050);border:1px solid #1d4ed8;border-radius:12px;padding:16px;margin-bottom:14px;}
.result-row{display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid #1e293b;font-size:13px;}
.result-row:last-child{border-bottom:none;}
.val{color:#60a5fa;font-family:'Space Mono',monospace;font-weight:700;}
.preset-btn{padding:5px 12px;background:#1e293b;border:1px solid #334155;border-radius:8px;
  color:#94a3b8;cursor:pointer;font-size:12px;font-family:inherit;transition:all 0.2s;font-weight:600;}
.preset-btn:hover,.preset-btn.sel{border-color:#3b82f6;color:#e2e8f0;background:#1e3a5f;}
input[type=range]{-webkit-appearance:none;width:100%;height:5px;background:#1e293b;border-radius:3px;outline:none;margin:4px 0;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;
  background:#3b82f6;cursor:pointer;box-shadow:0 0 8px rgba(59,130,246,0.6);}
input[type=range].orange::-webkit-slider-thumb{background:#f59e0b;box-shadow:0 0 8px rgba(245,158,11,0.6);}
input[type=range].green::-webkit-slider-thumb{background:#22c55e;box-shadow:0 0 8px rgba(34,197,94,0.6);}
.num-input{background:#070b14;border:1px solid #1e293b;border-radius:8px;color:#e2e8f0;
  padding:7px 10px;font-size:13px;font-family:'Space Mono',monospace;outline:none;width:100%;}
.num-input:focus{border-color:#3b82f6;}
.step-btn{width:100%;display:flex;align-items:center;gap:12px;padding:14px 18px;
  background:#0d1526;border:none;cursor:pointer;text-align:left;font-family:inherit;border-radius:12px;}
.step-content{padding:18px 24px;display:flex;flex-direction:column;gap:12px;}
.qa-btn{width:100%;display:flex;align-items:flex-start;gap:12px;padding:14px 18px;
  background:transparent;border:none;cursor:pointer;text-align:left;font-family:inherit;}
.launch-btn{flex:1;padding:12px 0;border:none;border-radius:12px;color:#fff;
  font-weight:800;font-size:14px;font-family:inherit;cursor:pointer;transition:all 0.2s;}
.stop-btn{flex:1;padding:12px 0;background:#7f1d1d;border:1px solid #ef4444;border-radius:12px;color:#fca5a5;
  font-weight:800;font-size:14px;font-family:inherit;cursor:pointer;transition:all 0.2s;}
.stop-btn:hover{background:#991b1b;}
label{font-size:11px;color:#64748b;font-weight:700;display:block;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.05em;}
.sec-title{display:flex;align-items:center;gap:8px;margin-bottom:12px;}
.sec-bar{width:4px;height:18px;border-radius:2px;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

/* ── 실제 물리 상수 ── */
const G_REAL = 6.674e-11;

/* ── 시각 시뮬레이션 상수 (정규화) ── */
const PLANET_R = 90;    // 행성 시각 반지름 (px)
const GM_NORM  = 4050;  // 정규화된 G*M
const V_ESC_NORM = Math.sqrt(2 * GM_NORM / PLANET_R); // ≈ 9.49 (정규화 탈출속도)

/* ── 천체 프리셋 ── */
const PRESETS = [
  { name:'지구',  M:5.972e24, R:6.371e6,  color:'#3b82f6', emoji:'🌍' },
  { name:'달',    M:7.342e22, R:1.737e6,  color:'#94a3b8', emoji:'🌙' },
  { name:'화성',  M:6.390e23, R:3.390e6,  color:'#ef4444', emoji:'🔴' },
  { name:'목성',  M:1.898e27, R:6.991e7,  color:'#f59e0b', emoji:'🟠' },
  { name:'태양',  M:1.989e30, R:6.960e8,  color:'#fbbf24', emoji:'☀️' },
];

const calcEscReal = (M, R) => Math.sqrt(2 * G_REAL * M / R) / 1000; // km/s

const fmtSci = (v) => {
  if (!isFinite(v) || v <= 0) return '—';
  const exp = Math.floor(Math.log10(v));
  const man = v / Math.pow(10, exp);
  return `${man.toFixed(2)} × 10^${exp}`;
};

/* ── KaTeX 수식 ── */
const Eq = ({ f, display=false, color='#93c5fd' }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && window.katex)
      window.katex.render(f, ref.current, { throwOnError:false, displayMode:display });
  }, [f, display]);
  return <span ref={ref} style={{ color }} />;
};

/* ══════════════════════════════════════════
   탭 1: 탈출 시뮬레이션 (전면 재구성)
══════════════════════════════════════════ */
function SimTab() {
  /* ── 천체 설정 상태 ── */
  const [presetIdx, setPresetIdx] = useState(0);
  const [isCustom, setIsCustom]   = useState(false);
  const [logM, setLogM] = useState(Math.log10(PRESETS[0].M)); // log10(kg)
  const [logR, setLogR] = useState(Math.log10(PRESETS[0].R)); // log10(m)

  /* ── 발사 속도 상태 ── */
  const [launchKms, setLaunchKms] = useState(null); // km/s, null = 아직 미설정
  const [sliderVal, setSliderVal] = useState(50);   // 0~100 → 0 ~ 3*vEsc

  /* ── 시뮬레이션 상태 ── */
  const [status, setStatus] = useState('ready'); // ready | running | stopped | escaped | returned
  const canvasRef = useRef(null);
  const animRef   = useRef(null);
  const simRef    = useRef(null);
  const statusRef = useRef('ready');

  /* ── 현재 천체 M, R ── */
  const M = isCustom ? Math.pow(10, logM) : PRESETS[presetIdx].M;
  const R = isCustom ? Math.pow(10, logR) : PRESETS[presetIdx].R;
  const vEsc = calcEscReal(M, R); // km/s

  /* 슬라이더 → km/s 변환 (0~100 → 0~3*vEsc) */
  const sliderToKms = (s) => (s / 100) * 3 * vEsc;
  const kmsToSlider = (v) => Math.min(100, (v / (3 * vEsc)) * 100);

  /* 초기 launchKms 동기화 (천체 변경 시) */
  useEffect(() => {
    setLaunchKms(+(vEsc * 0.85).toFixed(2));
    setSliderVal(+(kmsToSlider(vEsc * 0.85).toFixed(1)));
    setStatus('ready');
    statusRef.current = 'ready';
    cancelAnimationFrame(animRef.current);
  }, [presetIdx, isCustom, logM, logR]);

  /* 프리셋 선택 */
  const selectPreset = (i) => {
    setPresetIdx(i);
    setLogM(Math.log10(PRESETS[i].M));
    setLogR(Math.log10(PRESETS[i].R));
    setIsCustom(false);
  };

  const vFrac = launchKms !== null ? launchKms / vEsc : 0.85;
  const canEscape = launchKms !== null && launchKms >= vEsc;

  /* ── 발사 ── */
  const launch = () => {
    cancelAnimationFrame(animRef.current);
    const v0norm = vFrac * V_ESC_NORM;
    const E0 = 0.5 * v0norm * v0norm - GM_NORM / PLANET_R;
    simRef.current = { r: PLANET_R, v: v0norm, trail: [], willEscape: E0 >= 0, vFrac0: vFrac };
    statusRef.current = 'running';
    setStatus('running');
  };

  /* ── 정지 ── */
  const stop = () => {
    cancelAnimationFrame(animRef.current);
    statusRef.current = 'stopped';
    setStatus('stopped');
  };

  /* ── 다시 ── */
  const reset = () => {
    cancelAnimationFrame(animRef.current);
    statusRef.current = 'ready';
    setStatus('ready');
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0,0,canvas.width,canvas.height);
    }
  };

  /* ── 애니메이션 루프 ── */
  useEffect(() => {
    if (status !== 'running') return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const W = 820, H = 400;
    const CX = W * 0.26, CY = H * 0.5;
    const DT = 0.18, STEPS = 6;
    const color = isCustom ? '#8b5cf6' : PRESETS[presetIdx].color;

    const drawFrame = () => {
      if (statusRef.current !== 'running') return;
      const s = simRef.current;
      let done = false, escaped = false, infinityStop = false;

      for (let i = 0; i < STEPS; i++) {
        const a = -GM_NORM / (s.r * s.r);
        s.v += a * DT;
        s.r += s.v * DT;
        /* 화면 끝 탈출 */
        if (s.r > W - CX + 50) { escaped = true; done = true; break; }
        /* 에너지 기반 탈출: 총 에너지≥0 → 물리적으로 반드시 탈출 */
        if (s.willEscape && s.r > W - CX + 50) {
          escaped = true; done = true; break;
        }
        /* 표면 귀환: 총 에너지 < 0 일 때만 (수치 오류 방지) */
        if (s.r <= PLANET_R) { s.r = PLANET_R; s.v = 0; done = true; break; }
      }

      const objX = CX + s.r;          // r=PLANET_R → 행성 표면(우측 끝)
      const Ek   = Math.max(0, 0.5 * s.v * s.v);
      const Ep   = -GM_NORM / s.r;

      /* 궤적 기록 (탈출·귀환 경로 모두 포함) */
      if (!done) {
        s.trail.push({ x: Math.min(objX, W - 15), y: CY });
        if (s.trail.length > 700) s.trail.shift();
      }

      /* 배경 */
      ctx.fillStyle = '#05070a'; ctx.fillRect(0, 0, W, H);
      for (let i = 0; i < 120; i++) {
        const sx = (i*137.5)%W, sy = (i*97+i*11)%H;
        ctx.beginPath(); ctx.arc(sx, sy, 0.4+(i%3)*0.3, 0, Math.PI*2);
        ctx.fillStyle = `rgba(210,225,255,${0.07+(i%5)*0.05})`; ctx.fill();
      }

      /* 탈출속도 기준선 */
      ctx.save(); ctx.setLineDash([6,5]);
      ctx.strokeStyle = 'rgba(34,197,94,0.35)'; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(CX+PLANET_R+4, CY-26); ctx.lineTo(W-25, CY-26); ctx.stroke();
      ctx.restore();
      ctx.fillStyle = 'rgba(34,197,94,0.6)'; ctx.font = '11px Noto Sans KR'; ctx.textAlign='left';
      ctx.fillText('← 탈출 경로', CX+PLANET_R+8, CY-11);

      /* 행성 */
      const pg = ctx.createRadialGradient(CX-22, CY-22, 8, CX, CY, PLANET_R);
      pg.addColorStop(0, lighten(color)); pg.addColorStop(0.45, color); pg.addColorStop(1, darken(color));
      ctx.beginPath(); ctx.arc(CX, CY, PLANET_R, 0, Math.PI*2); ctx.fillStyle=pg; ctx.fill();
      const ag = ctx.createRadialGradient(CX,CY,PLANET_R,CX,CY,PLANET_R*1.28);
      ag.addColorStop(0,hexA(color,0.3)); ag.addColorStop(1,hexA(color,0));
      ctx.beginPath(); ctx.arc(CX,CY,PLANET_R*1.28,0,Math.PI*2); ctx.fillStyle=ag; ctx.fill();
      ctx.fillStyle='rgba(200,220,255,0.75)'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText(isCustom ? '사용자 천체' : PRESETS[presetIdx].name, CX, CY+PLANET_R+18);

      /* 궤적 */
      s.trail.forEach((pt, i) => {
        const a = 0.08 + (i/s.trail.length)*0.75;
        ctx.beginPath(); ctx.arc(pt.x, pt.y, 2.4, 0, Math.PI*2);
        ctx.fillStyle=`rgba(251,191,36,${a})`; ctx.fill();
      });

      /* 물체 */
      if (!done || escaped) {
        const ox = Math.min(CX + s.r, W-20);
        const og = ctx.createRadialGradient(ox-3,CY-3,1,ox,CY,10);
        og.addColorStop(0,'#fef3c7'); og.addColorStop(1,'#f59e0b');
        ctx.beginPath(); ctx.arc(ox, CY, 10, 0, Math.PI*2); ctx.fillStyle=og; ctx.fill();
        ctx.beginPath(); ctx.arc(ox, CY, 15, 0, Math.PI*2);
        ctx.strokeStyle='rgba(251,191,36,0.4)'; ctx.lineWidth=2; ctx.stroke();
      }

      /* 에너지 막대 */
      const E0 = GM_NORM / PLANET_R;
      const bX=W*0.72, bY=H*0.08, bW=28, bH=H*0.72;
      ctx.fillStyle='rgba(15,23,42,0.92)'; ctx.strokeStyle='rgba(51,65,85,0.8)'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.roundRect(bX-18,bY-36,bW*4+36,bH+56,10); ctx.fill(); ctx.stroke();
      ctx.fillStyle='#cbd5e1'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText('에너지 변화', bX+bW*1.5+18, bY-16);
      const midY = bY + bH*0.45;
      const sc = bH*0.4/E0;
      const Et = Ek + Ep;
      [[0,'#22c55e','Eₖ',Ek],[1,'#ef4444','Eₚ',Ep],[2,'#a78bfa','합계',Et]].forEach(([idx,cl,lb,val])=>{
        const x=bX+idx*(bW+10);
        const bh=Math.min(Math.abs(val)*sc,bH*0.44);
        ctx.fillStyle=cl+'33'; ctx.strokeStyle=cl; ctx.lineWidth=1;
        if(val>=0){ ctx.beginPath(); ctx.roundRect(x,midY-bh,bW,bh,4); }
        else       { ctx.beginPath(); ctx.roundRect(x,midY,bW,bh,4); }
        ctx.fill(); ctx.stroke();
        ctx.fillStyle=cl; ctx.font='bold 11px Space Mono'; ctx.textAlign='center';
        ctx.fillText(lb, x+bW/2, bY+bH+18);
        ctx.fillStyle='#94a3b8'; ctx.font='9px Space Mono';
        ctx.fillText(val.toFixed(0), x+bW/2, val>=0?midY-bh-5:midY+bh+14);
      });
      ctx.strokeStyle='rgba(148,163,184,0.5)'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.moveTo(bX-14,midY); ctx.lineTo(bX+bW*3+22,midY); ctx.stroke();
      ctx.fillStyle='#475569'; ctx.font='10px sans-serif'; ctx.textAlign='left';
      ctx.fillText('E=0', bX-14, midY-4);

      /* 결과 */
      if (done) {
        const isInfinity = escaped && s.willEscape && Math.abs(s.vFrac0 - 1.0) < 0.03;
        const msg = escaped
          ? (isInfinity ? '∞  v → 0 : 무한대에서 정지 (E = 0)' : '🚀 탈출 성공!')
          : '↩ 탈출 실패 — 낙하';
        const col2 = escaped ? (isInfinity ? '#fbbf24' : '#22c55e') : '#ef4444';
        ctx.fillStyle=col2; ctx.font='bold 22px Noto Sans KR'; ctx.textAlign='center';
        ctx.fillText(msg, W*0.42, H*0.13);
        if (isInfinity) {
          ctx.fillStyle='rgba(251,191,36,0.7)'; ctx.font='13px Noto Sans KR';
          ctx.fillText('총 에너지 = 0 → 무한대에서 속도가 0으로 수렴', W*0.42, H*0.13+26);
        }
        ctx.textAlign='left';
        statusRef.current = escaped ? 'escaped' : 'returned';
        setStatus(escaped ? 'escaped' : 'returned');
        return;
      }
      ctx.textAlign='left';
      animRef.current = requestAnimationFrame(drawFrame);
    };

    animRef.current = requestAnimationFrame(drawFrame);
    return () => cancelAnimationFrame(animRef.current);
  }, [status]);

  /* ── 색상 헬퍼 ── */
  const lighten = (hex) => hex + 'cc';
  const darken  = (hex) => hex + '66';
  const hexA    = (hex, a) => hex + Math.round(a*255).toString(16).padStart(2,'0');

  return (
    <div>
      {/* ─── STEP 1: 천체 설정 ─── */}
      <div className="card">
        <div className="sec-title">
          <div className="sec-bar" style={{background:'#3b82f6'}}/>
          <span style={{fontWeight:800,color:'#e2e8f0',fontSize:15}}>STEP 1 — 천체 설정</span>
        </div>

        {/* 프리셋 버튼 */}
        <div style={{display:'flex',gap:6,flexWrap:'wrap',marginBottom:14}}>
          {PRESETS.map((p,i)=>(
            <button key={i} className={`preset-btn ${!isCustom&&presetIdx===i?'sel':''}`}
              onClick={()=>selectPreset(i)}>
              {p.emoji} {p.name}
            </button>
          ))}
          <button className={`preset-btn ${isCustom?'sel':''}`}
            onClick={()=>setIsCustom(true)}>✏️ 직접 입력</button>
        </div>

        {/* 질량·반지름 슬라이더 */}
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:14}}>
          <div>
            <label>질량 (M) — 로그 슬라이더</label>
            <input type="range" className="orange" min={20} max={32} step={0.05}
              value={logM}
              onChange={e=>{ setLogM(parseFloat(e.target.value)); setIsCustom(true); }}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#64748b',marginTop:3}}>
              <span>10²⁰ kg</span>
              <span style={{color:'#f59e0b',fontFamily:'Space Mono',fontWeight:700}}>
                {fmtSci(Math.pow(10,logM))} kg
              </span>
              <span>10³² kg</span>
            </div>
          </div>
          <div>
            <label>반지름 (R) — 로그 슬라이더</label>
            <input type="range" className="green" min={4} max={12} step={0.05}
              value={logR}
              onChange={e=>{ setLogR(parseFloat(e.target.value)); setIsCustom(true); }}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#64748b',marginTop:3}}>
              <span>10⁴ m</span>
              <span style={{color:'#22c55e',fontFamily:'Space Mono',fontWeight:700}}>
                {(Math.pow(10,logR)/1000).toLocaleString('ko-KR',{maximumFractionDigits:0})} km
              </span>
              <span>10¹² m</span>
            </div>
          </div>
        </div>
      </div>

      {/* ─── STEP 2: 탈출속도 표시 ─── */}
      <div style={{
        background:'linear-gradient(135deg,#0a2a0a,#0f400f)',
        border:'2px solid #22c55e',borderRadius:14,padding:'16px 24px',
        marginBottom:14,display:'flex',alignItems:'center',gap:20
      }}>
        <div style={{fontSize:32}}>⚡</div>
        <div style={{flex:1}}>
          <p style={{color:'#4ade80',fontSize:12,fontWeight:700,marginBottom:4,textTransform:'uppercase',letterSpacing:'0.05em'}}>
            계산된 탈출속도 v탈출 = √(2GM/R)
          </p>
          <div style={{display:'flex',alignItems:'baseline',gap:10}}>
            <span style={{color:'#86efac',fontSize:38,fontWeight:800,fontFamily:'Space Mono'}}>
              {vEsc >= 1000 ? (vEsc/1000).toFixed(2) : vEsc.toFixed(2)}
            </span>
            <span style={{color:'#4ade80',fontSize:20,fontWeight:700}}>
              {vEsc >= 1000 ? 'Mm/s' : 'km/s'}
            </span>
            <span style={{color:'#166534',fontSize:14,marginLeft:8}}>
              = {(vEsc*1000).toExponential(3)} m/s
            </span>
          </div>
        </div>
        <div style={{textAlign:'right',fontSize:12,color:'#166534'}}>
          <p>M = {fmtSci(M)} kg</p>
          <p style={{marginTop:4}}>R = {(R/1000).toLocaleString('ko-KR',{maximumFractionDigits:0})} km</p>
          <p style={{marginTop:4}}>g = {(G_REAL*M/R/R).toFixed(2)} m/s²</p>
        </div>
      </div>

      {/* ─── STEP 3: 발사 속도 설정 ─── */}
      <div className="card" style={{marginBottom:14}}>
        <div className="sec-title">
          <div className="sec-bar" style={{background:'#f59e0b'}}/>
          <span style={{fontWeight:800,color:'#e2e8f0',fontSize:15}}>STEP 2 — 발사 속도 설정</span>
          <span style={{
            marginLeft:'auto',padding:'3px 12px',borderRadius:20,fontSize:12,fontWeight:700,
            background: canEscape?'rgba(34,197,94,0.15)':'rgba(239,68,68,0.15)',
            color: canEscape?'#4ade80':'#f87171',
            border: `1px solid ${canEscape?'#22c55e':'#ef4444'}`
          }}>
            {canEscape ? '✅ 탈출 가능' : '❌ 탈출 불가'}
          </span>
        </div>

        {/* 슬라이더 */}
        <div style={{position:'relative',marginBottom:6}}>
          <input type="range" min={0} max={100} step={0.5}
            value={sliderVal}
            onChange={e=>{
              const s=parseFloat(e.target.value);
              setSliderVal(s);
              setLaunchKms(+(sliderToKms(s).toFixed(3)));
              setStatus('ready'); statusRef.current='ready';
            }}
            style={{width:'100%'}}/>
          {/* 탈출속도 마커 */}
          <div style={{
            position:'absolute',top:-18,
            left:`calc(${Math.min(100/3,100)}% - 1px)`,
            pointerEvents:'none'
          }}>
            <div style={{width:2,height:22,background:'#22c55e',opacity:0.8}}/>
            <span style={{position:'absolute',top:24,left:-18,fontSize:10,color:'#22c55e',
              whiteSpace:'nowrap',fontWeight:700}}>v탈출</span>
          </div>
        </div>

        <div style={{display:'flex',alignItems:'flex-end',gap:12,marginTop:14}}>
          <div style={{flex:1}}>
            <label>발사 속도 (km/s) 직접 입력</label>
            <div style={{display:'flex',alignItems:'center',gap:8}}>
              <input type="number" className="num-input"
                value={launchKms ?? ''}
                min={0} step={0.1}
                onChange={e=>{
                  const v=parseFloat(e.target.value);
                  if(!isNaN(v)&&v>=0){
                    setLaunchKms(+v.toFixed(3));
                    setSliderVal(+(kmsToSlider(v).toFixed(1)));
                    setStatus('ready'); statusRef.current='ready';
                  }
                }}
                style={{flex:1}}/>
              <span style={{color:'#64748b',fontSize:13,whiteSpace:'nowrap'}}>km/s</span>
            </div>
          </div>
          {/* 빠른 비율 버튼 */}
          <div style={{display:'flex',gap:6,flexWrap:'wrap'}}>
            {[0.5,0.8,1.0,1.2,1.5].map(frac=>(
              <button key={frac} className={`preset-btn`}
                style={{borderColor:frac===1.0?'#22c55e':undefined,color:frac===1.0?'#4ade80':undefined}}
                onClick={()=>{
                  const v=+(vEsc*frac).toFixed(3);
                  setLaunchKms(v);
                  setSliderVal(+(kmsToSlider(v).toFixed(1)));
                  setStatus('ready'); statusRef.current='ready';
                }}>
                {frac}×v탈출
              </button>
            ))}
          </div>
        </div>

        {/* 비교 정보 */}
        <div style={{marginTop:12,padding:'10px 14px',background:'#070b14',borderRadius:10,border:'1px solid #1e293b',
          display:'flex',gap:24,flexWrap:'wrap',fontSize:12}}>
          <span>v₀ = <strong style={{color:'#fbbf24',fontFamily:'Space Mono'}}>{(launchKms??0).toFixed(3)}</strong> km/s</span>
          <span>v탈출 = <strong style={{color:'#4ade80',fontFamily:'Space Mono'}}>{vEsc.toFixed(3)}</strong> km/s</span>
          <span>비율 v₀/v탈출 = <strong style={{color: canEscape?'#4ade80':'#f87171',fontFamily:'Space Mono'}}>{vFrac.toFixed(3)}</strong></span>
          <span>총 에너지 = <strong style={{color:canEscape?'#4ade80':'#f87171',fontFamily:'Space Mono'}}>
            {(0.5*vFrac*vFrac - 1).toFixed(3)} (정규화)
          </strong></span>
        </div>
      </div>

      {/* ─── 캔버스 + 컨트롤 ─── */}
      <div style={{position:'relative',marginBottom:14}}>
        <canvas ref={canvasRef} width={820} height={400}
          style={{width:'100%',height:'400px',borderRadius:'12px',background:'#05070a',display:'block'}}/>

        {/* 오버레이: ready/stopped 상태일 때 안내 */}
        {(status==='ready'||status==='stopped') && (
          <div style={{
            position:'absolute',top:'50%',left:'50%',transform:'translate(-50%,-50%)',
            textAlign:'center',pointerEvents:'none'
          }}>
            <div style={{fontSize:48,marginBottom:8}}>🚀</div>
            <p style={{color:'rgba(148,163,184,0.8)',fontSize:14}}>
              {status==='stopped' ? '시뮬레이션 정지됨' : '발사 버튼을 눌러 시작'}
            </p>
          </div>
        )}
      </div>

      {/* ─── 발사/정지/초기화 버튼 ─── */}
      <div style={{display:'flex',gap:10,marginBottom:14}}>
        {status !== 'running' ? (
          <button className="launch-btn"
            style={{background: canEscape?'#15803d':'#1d4ed8',
              boxShadow:`0 4px 18px ${canEscape?'rgba(21,128,61,0.5)':'rgba(29,78,216,0.5)'}`}}
            onClick={launch}>
            ▶ {status==='ready' ? '발사 시작' : '다시 발사'}
          </button>
        ) : (
          <button className="stop-btn" onClick={stop}>⏹ 정지</button>
        )}
        <button className="launch-btn"
          style={{background:'#1e293b',boxShadow:'none',border:'1px solid #334155',color:'#94a3b8'}}
          onClick={reset}>↺ 초기화</button>
      </div>

      {/* ─── 탐구 포인트 ─── */}
      <div className="hl-box">
        <p style={{color:'#a78bfa',fontWeight:700,fontSize:13,marginBottom:8}}>📌 탐구 포인트</p>
        <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:10}}>
          {[
            ['v₀ < v탈출 (0.8×)', '총 에너지 < 0 → 중력에 묶여 낙하'],
            ['v₀ = v탈출 (1.0×)', '총 에너지 = 0 → 무한히 먼 곳에 겨우 도달'],
            ['v₀ > v탈출 (1.2×)', '총 에너지 > 0 → 탈출 후 잔여 에너지 보유'],
          ].map(([t,d],i)=>(
            <div key={i} style={{background:'rgba(0,0,0,0.3)',borderRadius:10,padding:12}}>
              <p style={{color:'#fbbf24',fontSize:12,fontWeight:700,marginBottom:4}}>{t}</p>
              <p style={{color:'#94a3b8',fontSize:12,lineHeight:1.7}}>{d}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 2: 탈출속도 계산기
────────────────────────────────────────────── */
function CalcTab() {
  const [sel, setSel] = useState(0);
  const [customM, setCM] = useState(PRESETS[0].M);
  const [customR, setCR] = useState(PRESETS[0].R);
  const [isCustom, setIsCustom] = useState(false);
  const M = isCustom ? customM : PRESETS[sel].M;
  const R = isCustom ? customR : PRESETS[sel].R;
  const v = calcEscReal(M, R);

  return (
    <div>
      <div className="hl-box">
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>🧮 탈출속도 계산기</p>
        <p style={{color:'#cbd5e1',fontSize:14}}>
          탈출속도 공식: <Eq f="v_{\text{탈출}} = \sqrt{\dfrac{2GM}{R}}" />
        </p>
      </div>

      <div style={{display:'flex',gap:8,flexWrap:'wrap',marginBottom:14}}>
        {PRESETS.map((p,i)=>(
          <button key={i} className={`preset-btn ${!isCustom&&sel===i?'sel':''}`}
            onClick={()=>{ setSel(i); setIsCustom(false); }}>
            {p.emoji} {p.name}
          </button>
        ))}
        <button className={`preset-btn ${isCustom?'sel':''}`} onClick={()=>setIsCustom(true)}>
          ✏️ 사용자 입력
        </button>
      </div>

      {isCustom && (
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12,marginBottom:14}}>
          <div className="card">
            <label>천체 질량 (M) [kg]</label>
            <input type="number" className="num-input" value={customM} step="1e22"
              onChange={e=>{ const v=parseFloat(e.target.value); if(v>0) setCM(v); }}/>
          </div>
          <div className="card">
            <label>천체 반지름 (R) [m]</label>
            <input type="number" className="num-input" value={customR} step="1000"
              onChange={e=>{ const v=parseFloat(e.target.value); if(v>0) setCR(v); }}/>
          </div>
        </div>
      )}

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:14,marginBottom:14}}>
        <div className="card">
          <p style={{color:'#64748b',fontSize:11,marginBottom:10,fontWeight:700,textTransform:'uppercase'}}>입력값</p>
          <div className="result-row"><span style={{color:'#94a3b8'}}>질량 (M)</span>
            <span className="val">{M.toExponential(3)} kg</span></div>
          <div className="result-row"><span style={{color:'#94a3b8'}}>반지름 (R)</span>
            <span className="val">{(R/1000).toLocaleString('ko-KR',{maximumFractionDigits:0})} km</span></div>
          <div className="result-row"><span style={{color:'#94a3b8'}}>표면 중력 (g)</span>
            <span className="val">{(G_REAL*M/R/R).toFixed(2)} m/s²</span></div>
        </div>
        <div className="card" style={{background:'linear-gradient(135deg,#0c2a0c,#0a3d0a)',borderColor:'#22c55e'}}>
          <p style={{color:'#22c55e',fontSize:11,marginBottom:10,fontWeight:800,textTransform:'uppercase'}}>탈출속도</p>
          <div style={{textAlign:'center',padding:'12px 0'}}>
            <p style={{color:'#86efac',fontSize:34,fontWeight:800,fontFamily:'Space Mono'}}>{v.toFixed(2)}</p>
            <p style={{color:'#4ade80',fontSize:16}}>km/s</p>
          </div>
          <p style={{color:'#4ade80',fontSize:12,textAlign:'center'}}>= {(v*1000).toFixed(0)} m/s</p>
        </div>
      </div>

      <div className="card">
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>태양계 천체 탈출속도 비교</p>
        <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
          <thead>
            <tr style={{borderBottom:'1px solid #1e293b'}}>
              {['천체','질량 (kg)','반지름 (km)','탈출속도 (km/s)','표면 중력 (m/s²)'].map(h=>(
                <th key={h} style={{padding:'9px 10px',color:'#64748b',fontWeight:700,textAlign:'left'}}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {PRESETS.map((p,i)=>{
              const ve=calcEscReal(p.M,p.R), g=G_REAL*p.M/p.R/p.R;
              return (
                <tr key={i} style={{borderBottom:'1px solid #0f172a',
                  background:!isCustom&&sel===i?'rgba(29,78,216,0.12)':undefined}}>
                  <td style={{padding:'9px 10px',color:p.color,fontWeight:700}}>{p.emoji} {p.name}</td>
                  <td style={{padding:'9px 10px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:11}}>{p.M.toExponential(3)}</td>
                  <td style={{padding:'9px 10px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:11}}>{(p.R/1000).toLocaleString('ko-KR',{maximumFractionDigits:0})}</td>
                  <td style={{padding:'9px 10px',color:'#60a5fa',fontWeight:800,fontFamily:'Space Mono'}}>{ve.toFixed(2)}</td>
                  <td style={{padding:'9px 10px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:11}}>{g.toFixed(2)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 3: 수식 유도
────────────────────────────────────────────── */
const DERIVE_STEPS = [
  { n:1, title:'역학적 에너지 보존 법칙 적용', color:'#3b82f6', bg:'#0d1f3c',
    formula:'E_{\\text{역학}} = E_k + E_p = \\text{일정}',
    note:'외력이 없는 계에서 운동 에너지와 중력 퍼텐셜 에너지의 합은 항상 보존됩니다.' },
  { n:2, title:'출발점 (천체 표면) 에너지', color:'#8b5cf6', bg:'#1a0d3c',
    formula:'E = \\dfrac{1}{2}mv_0^2 - \\dfrac{GMm}{R}',
    note:'R: 천체 반지름. 중력 퍼텐셜 에너지의 기준(Ep=0)은 무한히 먼 곳입니다.' },
  { n:3, title:'탈출 조건: 무한히 먼 곳에서 에너지 ≥ 0', color:'#a855f7', bg:'#1e0d3c',
    formula:'\\dfrac{1}{2}mv_0^2 - \\dfrac{GMm}{R} \\geq 0',
    note:'r→∞ 에서 Ep=0 이므로, 탈출하려면 총 에너지가 0 이상이어야 합니다.' },
  { n:4, title:'등호 조건(최소 탈출속도)으로 정리, m 약분', color:'#10b981', bg:'#0a1f18',
    formula:'\\dfrac{1}{2}v_0^2 = \\dfrac{GM}{R} \\quad (m \\text{ 약분})',
    note:'양변에서 m이 완전히 약분됩니다. 탈출속도는 발사체의 질량과 무관합니다!' },
  { n:5, title:'탈출속도 최종 공식', color:'#fbbf24', bg:'#1f1200',
    formula:'v_{\\text{탈출}} = \\sqrt{\\dfrac{2GM}{R}}',
    note:'G=6.674×10⁻¹¹ N·m²/kg². 질량 M이 클수록, 반지름 R이 작을수록 탈출속도 증가.' },
];

function DerivTab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>📐 탈출속도 수식 유도</p>
        <p style={{color:'#cbd5e1',fontSize:13,lineHeight:1.8}}>역학적 에너지 보존 법칙만으로 탈출속도를 유도합니다. 각 단계를 클릭하세요.</p>
      </div>
      <div style={{display:'flex',flexDirection:'column',gap:10,marginBottom:18}}>
        {DERIVE_STEPS.map((s,i)=>(
          <div key={i} style={{border:`1px solid ${open===i?s.color+'90':'#1e293b'}`,borderRadius:14,overflow:'hidden',transition:'border-color 0.25s'}}>
            <button className="step-btn" onClick={()=>setOpen(open===i?null:i)}>
              <div style={{width:32,height:32,borderRadius:'50%',background:s.color,display:'flex',
                alignItems:'center',justifyContent:'center',color:'#fff',fontWeight:800,fontSize:14,flexShrink:0}}>{s.n}</div>
              <div style={{flex:1}}><p style={{color:'#e2e8f0',fontSize:14,fontWeight:700}}>{s.title}</p></div>
              <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',
                transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
            </button>
            <div style={{maxHeight:open===i?'260px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
              <div className="step-content" style={{background:s.bg}}>
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
      <div style={{background:'linear-gradient(135deg,#064e3b,#065f46)',borderRadius:16,padding:'18px 24px',border:'1px solid #10b981',display:'flex',alignItems:'center',gap:18}}>
        <div style={{fontSize:32}}>✅</div>
        <div>
          <p style={{color:'#34d399',fontWeight:800,fontSize:14,marginBottom:4}}>결론</p>
          <p style={{color:'#6ee7b7',fontSize:13,lineHeight:1.8}}>
            탈출속도는 발사체 질량 m과 무관합니다. 오직 천체의 M과 R에만 의존합니다.<br/>
            STEP 1에서 슬라이더로 M과 R을 바꾸면 탈출속도가 어떻게 변하는지 직접 확인해 보세요.
          </p>
        </div>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 4: 탐구 질문
────────────────────────────────────────────── */
const QA = [
  { q:'탈출속도는 발사 방향과 관계없이 같을까?',
    a:'네. 방향에 무관합니다. 역학적 에너지는 스칼라(크기만 있는 양)이므로 수식에 방향 성분이 없습니다. 수직이든 비스듬히든 같은 속력이 필요합니다. 단, 대기 저항이 있으면 실제로는 달라집니다.' },
  { q:'발사체의 질량이 두 배가 되면 탈출속도도 두 배가 될까?',
    a:'아닙니다. v탈출 = √(2GM/R)에 발사체 질량 m이 없습니다. 수식 유도 Step 4에서 m이 약분되기 때문입니다. 100kg 로켓과 1kg 돌멩이를 같은 속도로 발사해야 탈출할 수 있습니다.' },
  { q:'지구의 질량 그대로, 반지름만 절반으로 줄이면 탈출속도는?',
    a:'v ∝ 1/√R이므로, R이 1/2배가 되면 v탈출은 √2 ≈ 1.41배가 됩니다. 지구 탈출속도 11.2 km/s → 약 15.8 km/s. STEP 1의 슬라이더로 반지름을 줄여서 확인해 보세요.' },
  { q:'탈출속도와 원 궤도 속도의 관계는?',
    a:'원 궤도 속도 v₀ = √(GM/R), 탈출속도 v탈출 = √(2GM/R) = √2 × v₀ ≈ 1.41 × v₀. 탈출속도는 원 궤도 속도의 √2배입니다. ISS의 궤도 속도는 약 7.7 km/s이고 탈출속도는 11.2 km/s입니다.' },
  { q:'탈출속도가 빛의 속도(30만 km/s)가 되려면?',
    a:'v탈출 = c = √(2GM/R_s) → R_s = 2GM/c². 이것이 슈바르츠실트 반지름입니다. 지구의 경우 R_s ≈ 9mm, 태양은 약 3km입니다. 이보다 작게 압축하면 블랙홀이 됩니다. 다음 탐구(블랙홀)에서 이어서 배웁니다.' },
];

function QATab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:4}}>❓ 탐구 질문</p>
        <p style={{color:'#94a3b8',fontSize:13}}>질문을 클릭하면 답변이 펼쳐집니다. 먼저 스스로 생각해 보세요.</p>
      </div>
      <div style={{display:'flex',flexDirection:'column',gap:10}}>
        {QA.map((item,i)=>(
          <div key={i} style={{borderRadius:13,border:`1px solid ${open===i?'#3b82f6':'#1e293b'}`,
            overflow:'hidden',background:'#070b14',transition:'border-color 0.2s'}}>
            <button className="qa-btn" onClick={()=>setOpen(open===i?null:i)}>
              <span style={{color:'#6366f1',fontWeight:800,fontSize:15,flexShrink:0,marginTop:1}}>Q{i+1}.</span>
              <span style={{color:'#cbd5e1',fontSize:14,lineHeight:1.65,flex:1}}>{item.q}</span>
              <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',
                transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
            </button>
            <div style={{maxHeight:open===i?'300px':'0px',overflow:'hidden',transition:'max-height 0.35s ease'}}>
              <div style={{padding:'0 18px 14px 46px',display:'flex',gap:10}}>
                <span style={{color:'#10b981',fontWeight:800,fontSize:13,flexShrink:0,marginTop:1}}>A.</span>
                <span style={{color:'#6ee7b7',fontSize:13,lineHeight:1.8}}>{item.a}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   메인 앱
────────────────────────────────────────────── */
const TABS = [
  { id:'sim',   label:'🔬 탈출 시뮬레이션' },
  { id:'calc',  label:'🧮 탈출속도 계산기' },
  { id:'deriv', label:'📐 수식 유도' },
  { id:'qa',    label:'❓ 탐구 질문' },
];

const App = () => {
  const [tab, setTab] = useState('sim');
  return (
    <div style={{maxWidth:1100,margin:'0 auto'}}>
      <div style={{background:'linear-gradient(135deg,#0f172a,#1e293b)',borderRadius:16,padding:'18px 24px',
        marginBottom:18,border:'1px solid #334155'}}>
        <h2 style={{color:'#60a5fa',margin:0,fontSize:'1.35rem'}}>🚀 학습주제 6-1: 탈출속도 탐구</h2>
        <p style={{color:'#94a3b8',margin:'7px 0 0',fontSize:'0.92rem'}}>
          <strong style={{color:'#fbbf24'}}>핵심 질문:</strong> 천체를 완전히 탈출하기 위한 최소 속도는 어떻게 결정되며, 왜 발사체의 질량과 무관할까?
        </p>
      </div>
      <div className="tab-bar">
        {TABS.map(t=>(
          <button key={t.id} className={`tab-btn ${tab===t.id?'active':''}`}
            onClick={()=>setTab(t.id)}>{t.label}</button>
        ))}
      </div>
      {tab==='sim'   && <SimTab/>}
      {tab==='calc'  && <CalcTab/>}
      {tab==='deriv' && <DerivTab/>}
      {tab==='qa'    && <QATab/>}
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""

components.html(REACT_HTML, height=1200, scrolling=True)
