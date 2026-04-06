import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Scissors, Settings2, Info, Activity, Layers, ArrowRight, MousePointer2, HelpCircle } from 'lucide-react';

/**
 * 물리학Ⅱ 등속 원운동 심화 탐구 (3단계 학습 모드)
 * @author Antigravity
 */
const CircularMotionAdvanced = () => {
  const [mode, setMode] = useState(1); // 1: Radian, 2: v=rw, 3: Delta v
  const [isPaused, setIsPaused] = useState(false);
  const [isCut, setIsCut] = useState(false);
  const [activeTab, setActiveTab] = useState('settings'); // 'settings' or 'activity'
  
  // 공통 물리 파라미터
  const [radius, setRadius] = useState(120);
  const [theta, setTheta] = useState(1); // Mode 1용 (radian)
  const [omega, setOmega] = useState(1.5); // Mode 2, 3용 (rad/s)
  const [mass, setMass] = useState(2.0);
  
  // 애니메이션 상태
  const [angle, setAngle] = useState(0); 
  const [elapsedTimeAfterCut, setElapsedTimeAfterCut] = useState(0);
  const [cutState, setCutState] = useState({ pos: { x: 0, y: 0 }, vel: { x: 0, y: 0 } });
  
  // Mode 3 특화 상태 (벡터 자취)
  const [savedVectors, setSavedVectors] = useState([]); // [{ angle, pos, vel }]
  
  const requestRef = useRef();
  const lastTimeRef = useRef();

  const animate = (time) => {
    if (lastTimeRef.current !== undefined && !isPaused) {
      const deltaTime = (time - lastTimeRef.current) / 1000;
      
      if (!isCut) {
        setAngle((prev) => (prev + (mode === 1 ? 0 : omega) * deltaTime) % (Math.PI * 2));
      } else {
        setElapsedTimeAfterCut((prev) => prev + deltaTime);
      }
    }
    lastTimeRef.current = time;
    requestRef.current = requestAnimationFrame(animate);
  };

  useEffect(() => {
    requestRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(requestRef.current);
  }, [isPaused, isCut, mode, omega]);

  const handleReset = () => {
    setIsCut(false);
    setAngle(0);
    setElapsedTimeAfterCut(0);
    setSavedVectors([]);
    setIsPaused(false);
  };

  const handleCut = () => {
    if (isCut || mode !== 3) return;
    const x = radius * Math.cos(angle);
    const y = radius * Math.sin(angle);
    const v = radius * omega;
    const vx = -v * Math.sin(angle);
    const vy = v * Math.cos(angle);
    setCutState({ pos: { x, y }, vel: { x: vx, y: vy } });
    setIsCut(true);
  };

  const saveVector = () => {
    if (savedVectors.length >= 2) setSavedVectors([]);
    const v = radius * omega;
    setSavedVectors(prev => [...prev, {
      angle: angle,
      pos: { x: radius * Math.cos(angle), y: radius * Math.sin(angle) },
      vel: { x: -v * Math.sin(angle), y: v * Math.cos(angle) }
    }]);
  };

  // --- 렌더링 상수 ---
  const CX = 250;
  const CY = 250;

  return (
    <div className="flex flex-col items-center min-h-screen bg-slate-50 p-6 text-slate-800 font-sans">
      <div className="w-full max-w-6xl bg-white rounded-[2rem] shadow-2xl border border-slate-200 overflow-hidden flex flex-col">
        
        {/* 모드 선택 탭 */}
        <div className="flex bg-slate-100 p-2 gap-2 border-b border-slate-200">
          {[
            { id: 1, label: 'Mode 1: 호와 반지름 (Radian)', icon: <Layers size={16}/> },
            { id: 2, label: 'Mode 2: 선속도와 각속도 (v=rω)', icon: <Activity size={16}/> },
            { id: 3, label: 'Mode 3: 구심 가속도와 Δv', icon: <Scissors size={16}/> }
          ].map(m => (
            <button
              key={m.id}
              onClick={() => { setMode(m.id); handleReset(); }}
              className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-bold transition-all ${mode === m.id ? 'bg-white shadow-md text-blue-600 scale-[1.02]' : 'text-slate-500 hover:bg-slate-200'}`}
            >
              {m.icon} {m.label}
            </button>
          ))}
        </div>

                <div className="flex flex-col lg:flex-row h-[650px]">
                  {/* 오버레이 팁 (수정본) */}
                  <div className="absolute top-4 left-4 bg-white/80 backdrop-blur-sm p-3 rounded-2xl border border-slate-100 text-[10px] space-y-1 shadow-sm z-10">
                    <div className="flex items-center gap-2 font-bold"><div className="w-2 h-2 bg-emerald-500 rounded-full"></div><span>속도 (v, Green)</span></div>
                    <div className="flex items-center gap-2 font-bold"><div className="w-2 h-2 bg-rose-500 rounded-full"></div><span>가속도 (a, Red)</span></div>
                    <div className="flex items-center gap-2 font-bold"><div className="w-2 h-2 bg-blue-500 rounded-full"></div><span>구심력 (F, Blue)</span></div>
                  </div>
          {/* 시뮬레이션 영역 */}
          <div className="flex-1 bg-white relative overflow-hidden flex items-center justify-center border-r border-slate-100">
            <svg viewBox="0 0 500 500" className="w-full h-full max-w-[500px]">
              {/* 공통 격자 */}
              <circle cx={CX} cy={CY} r="2" fill="#94a3b8" />
              <line x1="0" y1={CY} x2="500" y2={CY} stroke="#f1f5f9" strokeWidth="1" />
              <line x1={CX} y1="0" x2={CX} y2="500" stroke="#f1f5f9" strokeWidth="1" />

              {/* Mode 1: Radian 학습 */}
              {mode === 1 && (
                <g>
                  <circle cx={CX} cy={CY} r={radius} fill="none" stroke="#334155" strokeWidth="2.5" strokeDasharray="4,4" />
                  {/* 부채꼴 영역 */}
                  <path 
                    d={`M ${CX} ${CY} L ${CX + radius} ${CY} A ${radius} ${radius} 0 ${theta > Math.PI ? 1 : 0} 1 ${CX + radius * Math.cos(theta)} ${CY + radius * Math.sin(theta)} Z`} 
                    fill="rgba(59, 130, 246, 0.1)" 
                    stroke="#3b82f6" 
                    strokeWidth="2"
                  />
                  {/* 호(s) 강조 */}
                  <path 
                    d={`M ${CX + radius} ${CY} A ${radius} ${radius} 0 ${theta > Math.PI ? 1 : 0} 1 ${CX + radius * Math.cos(theta)} ${CY + radius * Math.sin(theta)}`} 
                    fill="none" 
                    stroke="#ef4444" 
                    strokeWidth="5" 
                    strokeLinecap="round"
                  />
                  {/* 1 Radian 강조 효과 */}
                  {Math.abs(theta - 1) < 0.05 && (
                    <g className="animate-pulse">
                      <text x={CX + radius/2} y={CY - 10} textAnchor="middle" className="text-xs font-bold fill-blue-600">r</text>
                      <text x={CX + radius + 10} y={CY + 50} className="text-xs font-bold fill-red-600 italic">s = r (1 rad)</text>
                    </g>
                  )}
                </g>
              )}

              {/* Mode 2: r1, r2 비교 */}
              {mode === 2 && (
                <g>
                  {[radius, radius * 0.6].map((r, i) => {
                    const x = CX + r * Math.cos(angle);
                    const y = CY + r * Math.sin(angle);
                    const v = r * omega;
                    const vx = -Math.sin(angle) * (v * 0.5);
                    const vy = Math.cos(angle) * (v * 0.5);
                    return (
                      <g key={i}>
                        <circle cx={CX} cy={CY} r={r} fill="none" stroke="#334155" strokeWidth="2.5" strokeDasharray="4,4" />
                        <line x1={CX} y1={CY} x2={x} y2={y} stroke="#94a3b8" strokeWidth="2" />
                        {/* Velocity Arrow */}
                        <line x1={x} y1={y} x2={x + vx} y2={y + vy} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                        <circle cx={x} cy={y} r="8" fill={i === 0 ? "#1e293b" : "#64748b"} />
                      </g>
                    );
                  })}
                </g>
              )}

              {/* Mode 3: Delta v 증명 */}
              {mode === 3 && (
                <g>
                   <circle cx={CX} cy={CY} r={radius} fill="none" stroke="#334155" strokeWidth="2.5" strokeDasharray="4,4" />
                   
                   {!isCut ? (
                     <>
                        <line x1={CX} y1={CY} x2={CX + radius * Math.cos(angle)} y2={CY + radius * Math.sin(angle)} stroke="#94a3b8" strokeWidth="2" />
                        {/* Velocity Vector */}
                        <line 
                          x1={CX + radius * Math.cos(angle)} y1={CY + radius * Math.sin(angle)} 
                          x2={CX + radius * Math.cos(angle) - (radius * omega * 0.5) * Math.sin(angle)} 
                          y2={CY + radius * Math.sin(angle) + (radius * omega * 0.5) * Math.cos(angle)} 
                          stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" 
                        />
                        {/* Acceleration Vector (Red) */}
                        <line 
                          x1={CX + radius * Math.cos(angle)} y1={CY + radius * Math.sin(angle)} 
                          x2={CX + radius * Math.cos(angle) + (radius * omega * 0.3) * -Math.cos(angle)} 
                          y2={CY + radius * Math.sin(angle) + (radius * omega * 0.3) * -Math.sin(angle)} 
                          stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrow-red)" 
                        />
                        {/* Centripetal Force Vector (Blue) - Slightly longer to differentiate */}
                        <line 
                          x1={CX + radius * Math.cos(angle)} y1={CY + radius * Math.sin(angle)} 
                          x2={CX + radius * Math.cos(angle) + (radius * omega * 0.45) * -Math.cos(angle)} 
                          y2={CY + radius * Math.sin(angle) + (radius * omega * 0.45) * -Math.sin(angle)} 
                          stroke="#3b82f6" strokeWidth="3" opacity="0.7" markerEnd="url(#arrow-blue)" 
                        />
                        <circle cx={CX + radius * Math.cos(angle)} cy={CY + radius * Math.sin(angle)} r="10" fill="#0f172a" />
                     </>
                   ) : (
                     <g>
                        <circle 
                          cx={CX + cutState.pos.x + cutState.vel.x * elapsedTimeAfterCut} 
                          cy={CY + cutState.pos.y + cutState.vel.y * elapsedTimeAfterCut} 
                          r="10" fill="#475569" 
                        />
                        <line 
                          x1={CX + cutState.pos.x} y1={CY + cutState.pos.y} 
                          x2={CX + cutState.pos.x + cutState.vel.x * 2} y2={CY + cutState.pos.y + cutState.vel.y * 2} 
                          stroke="#cbd5e1" strokeWidth="1" strokeDasharray="2,2" 
                        />
                     </g>
                   )}

                   {/* 벡터 자취 시각화 (서브 다이어그램 역할을 캔버스 우측 하단에 소형으로 표시 가능하지만, 여기서는 공간 활용) */}
                   {savedVectors.length > 0 && (
                     <g transform={`translate(${CX + 120}, ${CY + 120}) scale(0.8)`}>
                        <rect x="-60" y="-60" width="120" height="120" fill="white" stroke="#e2e8f0" rx="10" />
                        <line x1="-50" y1="0" x2="50" y2="0" stroke="#f1f5f9" />
                        <line x1="0" y1="-50" x2="0" y2="50" stroke="#f1f5f9" />
                        <circle cx="0" cy="0" r="2" fill="black" />
                        
                        {savedVectors.map((sv, idx) => (
                           <line key={idx} x1="0" y1="0" x2={sv.vel.x*0.5} y2={sv.vel.y*0.5} stroke={idx===0 ? "#10b981" : "#10b981"} strokeWidth="3" opacity={idx===0 ? 0.4 : 1} markerEnd="url(#arrow-green)" />
                        ))}

                        {savedVectors.length === 2 && (
                          <line 
                            x1={savedVectors[0].vel.x*0.5} y1={savedVectors[0].vel.y*0.5} 
                            x2={savedVectors[1].vel.x*0.5} y2={savedVectors[1].vel.y*0.5} 
                            stroke="#ef4444" strokeWidth="4" markerEnd="url(#arrow-red)" 
                          />
                        )}
                        <text x="0" y="55" textAnchor="middle" className="text-[10px] font-bold fill-slate-400 font-mono">Δv Direction</text>
                     </g>
                   )}
                </g>
              )}

              {/* 벡터 화살표 정의 */}
              <defs>
                <marker id="arrow-green" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#10b981"/></marker>
                <marker id="arrow-red" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#ef4444"/></marker>
                <marker id="arrow-blue" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#3b82f6"/></marker>
              </defs>
            </svg>

            {/* 수식 표시 오버레이 */}
            <div className="absolute top-8 left-8 bg-white/90 backdrop-blur shadow-sm p-4 rounded-2xl border border-slate-100 flex flex-col gap-2 pointer-events-none">
              {mode === 1 && (
                <>
                  <div className="flex items-center gap-4">
                    <span className="text-xl font-mono font-black italic text-blue-600 underline">s = r θ</span>
                    <span className="text-sm font-semibold text-slate-400">Relationship of Arc</span>
                  </div>
                  <div className="text-sm space-y-1">
                    <p>호의 길이 (s) = {radius} × {theta.toFixed(2)} = {(radius * theta).toFixed(1)} px</p>
                    <p className="text-blue-500 font-bold">1 Radian: s와 r이 같아질 때의 각도</p>
                  </div>
                </>
              )}
              {mode === 2 && (
                <>
                  <div className="flex items-center gap-4">
                    <span className="text-xl font-mono font-black italic text-emerald-600 underline">v = r ω</span>
                    <span className="text-sm font-semibold text-slate-400">Velocity Proportionality</span>
                  </div>
                  <div className="text-sm space-y-1">
                    <p>Outer v = {radius} × {omega.toFixed(1)} = {(radius * omega).toFixed(1)} px/s</p>
                    <p>Inner v = {(radius * 0.6).toFixed(0)} × {omega.toFixed(1)} = {(radius * 0.6 * omega).toFixed(1)} px/s</p>
                  </div>
                </>
              )}
              {mode === 3 && (
                <>
                  <div className="flex items-center gap-4 text-rose-600">
                    <span className="text-xl font-mono font-black italic underline">Δv → Center</span>
                    <span className="text-sm font-semibold text-slate-400">Direction of Force</span>
                  </div>
                  <div className="text-sm">
                    <p>구심 가속도 a = v²/r = {((radius * omega)**2/radius).toFixed(1)} px/s²</p>
                    <p className="text-rose-500">벡터 자취 차이(Δv)는 항상 중심을 향합니다.</p>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* 컨트롤 및 활동지 패널 */}
          <div className="w-full lg:w-96 bg-slate-50 flex flex-col overflow-hidden border-l border-slate-100">
            {/* 탭 헤더 */}
            <div className="flex border-b border-slate-200">
              <button 
                onClick={() => setActiveTab('settings')}
                className={`flex-1 py-4 flex items-center justify-center gap-2 font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'settings' ? 'bg-white text-blue-600 border-b-2 border-blue-600' : 'text-slate-400 hover:text-slate-600'}`}
              >
                <Settings2 size={16} /> 조작 설정
              </button>
              <button 
                onClick={() => setActiveTab('activity')}
                className={`flex-1 py-4 flex items-center justify-center gap-2 font-bold text-xs uppercase tracking-wider transition-all ${activeTab === 'activity' ? 'bg-white text-emerald-600 border-b-2 border-emerald-600' : 'text-slate-400 hover:text-slate-600'}`}
              >
                <HelpCircle size={16} /> 학습 활동지
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-8 space-y-8">
              {activeTab === 'settings' ? (
                <>
                  <section className="space-y-4">
                    <div className="flex items-center gap-2 text-blue-600">
                      <Settings2 size={20} />
                      <h3 className="font-black text-sm uppercase tracking-widest">환경 설정</h3>
                    </div>
                    
                    <div className="space-y-6">
                      {/* 반지름 슬라이더 */}
                      <div className="space-y-2">
                        <div className="flex justify-between font-mono text-sm"><span>Radius (r)</span><span className="text-blue-600 font-bold">{radius} px</span></div>
                        <input type="range" min="50" max="200" step="1" value={radius} onChange={e=>setRadius(parseInt(e.target.value))} className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600" />
                      </div>

                      {mode === 1 ? (
                        <div className="space-y-2">
                          <div className="flex justify-between font-mono text-sm"><span>Angle (θ)</span><span className="text-red-500 font-bold">{theta.toFixed(2)} rad</span></div>
                          <input type="range" min="0" max={Math.PI * 2} step="0.01" value={theta} onChange={e=>setTheta(parseFloat(e.target.value))} className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-red-500" />
                        </div>
                      ) : (
                        <div className="space-y-2">
                          <div className="flex justify-between font-mono text-sm"><span>Angular Vel (ω)</span><span className="text-emerald-500 font-bold">{omega.toFixed(1)} rad/s</span></div>
                          <input type="range" min="0.5" max="5.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-500" />
                        </div>
                      )}
                    </div>
                  </section>

                  <section className="space-y-4">
                    <div className="flex items-center gap-2 text-slate-500">
                      <Activity size={20} />
                      <h3 className="font-black text-sm uppercase tracking-widest">인터랙션</h3>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-3">
                      <button onClick={() => setIsPaused(!isPaused)} className="flex items-center justify-center gap-2 py-4 bg-white border border-slate-200 rounded-2xl shadow-sm font-bold text-sm hover:bg-slate-100 transition-all">
                        {isPaused ? <Play size={18} fill="currentColor"/> : <Pause size={18} fill="currentColor"/>}
                        {isPaused ? '시작' : '일시 정지'}
                      </button>
                      <button onClick={handleReset} className="flex items-center justify-center gap-2 py-4 bg-white border border-slate-200 rounded-2xl shadow-sm font-bold text-sm hover:bg-slate-100 transition-all">
                        <RotateCcw size={18} /> 초기화
                      </button>

                      {mode === 3 && (
                        <>
                          <button onClick={saveVector} className="col-span-2 flex items-center justify-center gap-2 py-4 bg-blue-600 text-white rounded-2xl shadow-lg shadow-blue-100 font-bold text-sm hover:bg-blue-700 transition-all">
                             <MousePointer2 size={18} /> 벡터 자취 저장 {savedVectors.length}/2
                          </button>
                          <button onClick={handleCut} disabled={isCut} className={`col-span-2 flex items-center justify-center gap-2 py-4 rounded-2xl font-bold text-sm transition-all shadow-md ${isCut ? 'bg-slate-100 text-slate-300' : 'bg-rose-500 text-white hover:bg-rose-600'}`}>
                             <Scissors size={18} /> 실 끊기 (관성 관찰)
                          </button>
                        </>
                      )}
                    </div>
                  </section>
                </>
              ) : (
                /* 활동지 내용 */
                <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-300">
                  {mode === 1 && (
                    <section className="space-y-4">
                      <div className="bg-blue-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold inline-block">Step 1. 수학적 기초</div>
                      <h4 className="font-bold text-slate-800 italic">"왜 굳이 라디안(rad)인가?"</h4>
                      <div className="bg-white p-4 rounded-2xl border border-slate-200 space-y-4 text-sm leading-relaxed">
                        <div className="space-y-2">
                          <p className="font-bold text-blue-600 flex items-center gap-2"><ArrowRight size={14}/> 탐구 미션</p>
                          <p className="text-slate-600">반지름을 100px로 설정하고, 호의 길이(s)가 100px이 될 때까지 각도를 조절해보세요.</p>
                        </div>
                        <div className="p-3 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                          <p className="font-bold text-xs text-slate-400 uppercase mb-2">인출 질문 (Retrieval)</p>
                          <p className="font-semibold text-slate-700">"호의 길이(s)가 반지름(r)과 정확히 같아지는 순간의 각도는 약 몇 도인가요? 이때의 rad 값은?"</p>
                          <div className="mt-3 h-8 bg-white border border-slate-200 rounded-lg flex items-center px-3 text-slate-300 italic text-xs">직접 인출하여 답변해보세요...</div>
                        </div>
                        <p className="text-xs text-slate-500 italic bg-blue-50 p-2 rounded-lg border border-blue-100">
                          <strong>핵심 정리:</strong> s = rθ 관계에서 θ = 1(rad)일 때 비로소 호의 길이와 반지름이 같아집니다.
                        </p>
                      </div>
                    </section>
                  )}

                  {mode === 2 && (
                    <section className="space-y-4">
                      <div className="bg-emerald-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold inline-block">Step 2. 운동의 기술</div>
                      <h4 className="font-bold text-slate-800 italic">"바깥쪽 개미가 더 빠른가요?"</h4>
                      <div className="bg-white p-4 rounded-2xl border border-slate-200 space-y-4 text-sm leading-relaxed">
                        <div className="space-y-2">
                          <p className="font-bold text-emerald-600 flex items-center gap-2"><ArrowRight size={14}/> 탐구 미션</p>
                          <p className="text-slate-600">반지름이 다른 두 물체를 동시에 회전시키며 각 속도 벡터를 관찰하세요.</p>
                        </div>
                        <div className="p-3 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                          <p className="font-bold text-xs text-slate-400 uppercase mb-2">인출 질문 (Retrieval)</p>
                          <p className="font-semibold text-slate-700">"두 물체의 각속도(ω)는 똑같지만, 접선 속도(v) 화살표 길이는 누가 더 긴가요? 그 물리적 이유는?"</p>
                          <div className="mt-3 h-8 bg-white border border-slate-200 rounded-lg flex items-center px-3 text-slate-300 italic text-xs">두 반지름의 비와 속도의 비를 비교해보세요...</div>
                        </div>
                        <p className="text-xs text-slate-500 italic bg-emerald-50 p-2 rounded-lg border border-emerald-100">
                          <strong>명시적 지도:</strong> v = Δs/Δt = r(Δθ/Δt) = rω 임을 수치 대조를 통해 확인합니다.
                        </p>
                      </div>
                    </section>
                  )}

                  {mode === 3 && (
                    <section className="space-y-4">
                      <div className="bg-rose-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold inline-block">Step 3. 역학의 본질</div>
                      <h4 className="font-bold text-slate-800 italic">"속력이 일정한데 왜 힘이 필요한가?"</h4>
                      <div className="bg-white p-4 rounded-2xl border border-slate-200 space-y-4 text-sm leading-relaxed">
                        <div className="space-y-2">
                          <p className="font-bold text-rose-600 flex items-center gap-2"><ArrowRight size={14}/> 탐구 미션</p>
                          <p className="text-slate-600">'벡터 자취' 기능을 켜서 서로 다른 두 지점의 속도 벡터를 기록하고 차이를 확인하세요.</p>
                        </div>
                        <div className="p-3 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                          <p className="font-bold text-xs text-slate-400 uppercase mb-2">인출 질문 (Retrieval)</p>
                          <p className="font-semibold text-slate-700">"두 속도 벡터의 차이(Δv)는 원의 어느 방향으로 나타나나요? 실이 갑자기 사라진다면 물체는?"</p>
                          <div className="mt-3 h-8 bg-white border border-slate-200 rounded-lg flex items-center px-3 text-slate-300 italic text-xs">'실 끊기' 버튼을 눌러 관성 방향을 관찰하세요...</div>
                        </div>
                        <p className="text-xs text-slate-500 italic bg-rose-50 p-2 rounded-lg border border-rose-100">
                          <strong>교정 포인트:</strong> '원심력'은 가상적인 힘이며, 본질은 관성과 중심을 향하는 구심력입니다.
                        </p>
                      </div>
                    </section>
                  )}

                  {/* 공통 평가 섹션 */}
                  <section className="space-y-4 border-t border-slate-200 pt-6">
                    <div className="bg-slate-800 text-white px-3 py-1.5 rounded-lg text-xs font-bold inline-block">Step 4. 평가 및 전이</div>
                    <h4 className="font-bold text-slate-800 italic">"도로 설계자 미션: 안전한 곡선"</h4>
                    <div className="bg-slate-100 p-4 rounded-2xl border border-slate-200 space-y-4 text-sm leading-relaxed">
                      <p className="text-slate-600 font-medium">문제: "비가 와서 마찰력이 줄어들면 구심력이 부족해집니다. 이때 사고를 막으려면 자동차는 어떻게 해야 할까요?"</p>
                      <ul className="text-xs space-y-2 text-slate-500">
                        <li>(1) 속력을 줄여야 한다 ($v \downarrow$)</li>
                        <li>(2) 회전 반경을 키워야 한다 ($r \uparrow$)</li>
                      </ul>
                      <p className="text-xs font-bold text-slate-700 bg-white p-2 rounded border border-slate-200 inline-block">
                        근거: F = m v²/r 수식을 바탕으로 설명해보세요.
                      </p>
                    </div>
                  </section>
                </div>
              )}
            </div>

            <div className="p-8 border-t border-slate-100 bg-white">
               <div className="flex items-center gap-2 text-blue-800 font-black text-[10px] uppercase tracking-tighter mb-2">
                 <Info size={14} /> 학습 가이드 요약
               </div>
               <p className="text-[10px] leading-relaxed text-blue-700/60 font-medium">
                 {mode === 1 && "라디안은 호의 길이와 반지름의 비로 각도를 정의한 것으로, 물리 공식의 단순화에 필수적입니다."}
                 {mode === 2 && "동일한 회전축에서 반지름이 커지면 더 긴 궤적을 돌아야 하므로 선속도가 빨라집니다."}
                 {mode === 3 && "속도 방향의 변화가 바로 가속도이며, 이 가속도를 만드는 근원이 중심을 향하는 구심력입니다."}
               </p>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 py-4 px-8 flex justify-between items-center text-white/50 text-[10px] font-mono tracking-wider">
           <span>PHYSICS II - UNIFORM CIRCULAR MOTION ADVANCED SIMULATION</span>
           <span className="flex items-center gap-2 text-emerald-400 font-bold"><Activity size={12}/> 60 FPS STABLE</span>
        </div>
      </div>
    </div>
  );
};

export default CircularMotionAdvanced;
