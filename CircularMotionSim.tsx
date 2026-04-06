import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Scissors, Settings2, Info, Activity } from 'lucide-react';

/**
 * 물리학Ⅱ 등속 원운동 시뮬레이션 컴포넌트
 * @author Antigravity
 * @goal 고등학교 물리학Ⅱ 교과과정에 따른 등속 원운동의 시각적 이해 지원
 */
const CircularMotionSimulation = () => {
  // --- 상태 관리 ---
  const [mass, setMass] = useState(2.0); // 질량 m (kg)
  const [radius, setRadius] = useState(120); // 반지름 r (px)
  const [linearVelocity, setLinearVelocity] = useState(150); // 선속도 v (px/s)
  const [isPaused, setIsPaused] = useState(false);
  const [isCut, setIsCut] = useState(false);
  
  // 가상 물리 상태
  const [angle, setAngle] = useState(0); // 현재 각도 theta (rad)
  const [startAngle, setStartAngle] = useState(0); // 누적 각도 추적용 (부채꼴)
  const [cutPosition, setCutPosition] = useState({ x: 0, y: 0 });
  const [cutVelocity, setCutVelocity] = useState({ x: 0, y: 0 });
  const [elapsedTimeAfterCut, setElapsedTimeAfterCut] = useState(0);

  const requestRef = useRef<number>(null);
  const lastTimeRef = useRef<number>(null);

  // --- 물리량 계산 ---
  const r = radius;
  const v = linearVelocity;
  const omega = v / r; // 각속도 w = v/r
  const centripetalAcc = (v * v) / r; // 구심 가속도 a = v^2/r
  const centripetalForce = mass * centripetalAcc; // 구심력 F = ma

  // --- 애니메이션 루프 ---
  const animate = (time: number) => {
    if (lastTimeRef.current !== null && !isPaused) {
      const deltaTime = (time - lastTimeRef.current) / 1000;

      if (!isCut) {
        setAngle((prevAngle) => (prevAngle + omega * deltaTime) % (Math.PI * 2));
      } else {
        setElapsedTimeAfterCut((prev) => prev + deltaTime);
      }
    }
    lastTimeRef.current = time;
    requestRef.current = requestAnimationFrame(animate);
  };

  useEffect(() => {
    requestRef.current = requestAnimationFrame(animate);
    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, [isPaused, isCut, omega]);

  // --- 상호작용 함수 ---
  const handleCut = () => {
    if (isCut) return;
    
    // 현재 위치 및 접선 속도 계산
    const x = r * Math.cos(angle);
    const y = r * Math.sin(angle);
    const vx = -v * Math.sin(angle);
    const vy = v * Math.cos(angle);

    setCutPosition({ x, y });
    setCutVelocity({ x: vx, y: vy });
    setIsCut(true);
    setElapsedTimeAfterCut(0);
  };

  const handleReset = () => {
    setIsCut(false);
    setAngle(0);
    setStartAngle(0);
    setElapsedTimeAfterCut(0);
    setIsPaused(false);
  };

  const handleTogglePause = () => {
    setIsPaused(!isPaused);
  };

  // --- 렌더링 좌표 계산 ---
  const centerX = 250;
  const centerY = 250;
  
  let ballX, ballY, velX, velY, accX, accY;

  if (!isCut) {
    ballX = centerX + r * Math.cos(angle);
    ballY = centerY + r * Math.sin(angle);
    
    // 속도 벡터 (접선 방향 - 초록색)
    velX = -Math.sin(angle) * (v / 2); // 길이는 시각적 편의를 위해 절반
    velY = Math.cos(angle) * (v / 2);
    
    // 가속도 벡터 (중심 방향 - 빨간색)
    accX = -Math.cos(angle) * (centripetalAcc / 5); // 스케일 조정
    accY = -Math.sin(angle) * (centripetalAcc / 5);
  } else {
    ballX = centerX + cutPosition.x + cutVelocity.x * elapsedTimeAfterCut;
    ballY = centerY + cutPosition.y + cutVelocity.y * elapsedTimeAfterCut;
    velX = cutVelocity.x / 2;
    velY = cutVelocity.y / 2;
    accX = 0;
    accY = 0;
  }

  // --- 부채꼴(각변위) 경로 계산 ---
  const getArcPath = () => {
    if (isCut) return null;
    const startX = centerX + r * Math.cos(startAngle);
    const startY = centerY + r * Math.sin(startAngle);
    const endX = ballX;
    const endY = ballY;
    
    // 델타 각도 계산
    let diff = angle - startAngle;
    if (diff < 0) diff += Math.PI * 2;
    
    const largeArcFlag = diff > Math.PI ? 1 : 0;
    
    return `M ${centerX} ${centerY} L ${startX} ${startY} A ${r} ${r} 0 ${largeArcFlag} 1 ${endX} ${endY} Z`;
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-50 p-4 font-sans text-slate-800">
      <div className="w-full max-w-5xl bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">
        {/* 상단 데이터 헤더 */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-6 bg-slate-900 text-white">
          <div className="flex flex-col">
            <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider">선속도 (v)</span>
            <span className="text-2xl font-mono text-emerald-400">{v.toFixed(1)} <small className="text-xs">px/s</small></span>
          </div>
          <div className="flex flex-col">
            <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider">각속도 (ω)</span>
            <span className="text-2xl font-mono text-amber-400">{omega.toFixed(3)} <small className="text-xs">rad/s</small></span>
          </div>
          <div className="flex flex-col">
            <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider">구심 가속도 (a)</span>
            <span className="text-2xl font-mono text-rose-400">{centripetalAcc.toFixed(1)} <small className="text-xs">px/s²</small></span>
          </div>
          <div className="flex flex-col">
            <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider">구심력 (F)</span>
            <span className="text-2xl font-mono text-blue-400">{centripetalForce.toFixed(1)} <small className="text-xs">N</small></span>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row h-[600px]">
          {/* 메인 시뮬레이션 캔버스 영역 */}
          <div className="relative flex-1 bg-slate-100 overflow-hidden flex items-center justify-center">
            <svg width="500" height="500" viewBox="0 0 500 500" className="drop-shadow-sm">
              {/* 중심점 및 격자 */}
              <circle cx={centerX} cy={centerY} r="3" fill="#64748b" />
              <line x1="0" y1={centerY} x2="500" y2={centerY} stroke="#e2e8f0" strokeDasharray="4" />
              <line x1={centerX} y1="0" x2={centerX} y2="500" stroke="#e2e8f0" strokeDasharray="4" />

              {/* 궤도 (실 끊기 전) */}
              {!isCut && (
                <circle
                  cx={centerX}
                  cy={centerY}
                  r={r}
                  fill="none"
                  stroke="#cbd5e1"
                  strokeWidth="1.5"
                  strokeDasharray="5,5"
                />
              )}

              {/* 각변위 영역 (부채꼴) */}
              {!isCut && (
                <path d={getArcPath() || ''} fill="rgba(245, 158, 11, 0.2)" />
              )}

              {/* 실 (중심에서 물체까지) */}
              {!isCut && (
                <line
                  x1={centerX}
                  y1={centerY}
                  x2={ballX}
                  y2={ballY}
                  stroke="#94a3b8"
                  strokeWidth="2"
                />
              )}

              {/* 속도 벡터 (접선 방향, 초록색) */}
              <g>
                <line
                  x1={ballX}
                  y1={ballY}
                  x2={ballX + velX}
                  y2={ballY + velY}
                  stroke="#10b981"
                  strokeWidth="3"
                  markerEnd="url(#arrow-green)"
                />
                <text x={ballX + velX + 5} y={ballY + velY} fill="#059669" className="text-[10px] font-bold font-mono">v</text>
              </g>

              {/* 가속도 벡터 (중심 방향, 빨간색) */}
              {!isCut && (
                <g>
                  <line
                    x1={ballX}
                    y1={ballY}
                    x2={ballX + accX}
                    y2={ballY + accY}
                    stroke="#ef4444"
                    strokeWidth="3"
                    markerEnd="url(#arrow-red)"
                  />
                  <text x={ballX + accX - 15} y={ballY + accY - 5} fill="#dc2626" className="text-[10px] font-bold font-mono">a</text>
                </g>
              )}

              {/* 물체 (공) */}
              <circle
                cx={ballX}
                cy={ballY}
                r={10 + mass * 2}
                className="transition-all duration-300"
                fill="url(#ball-gradient)"
                stroke="#1e293b"
                strokeWidth="1"
              />

              {/* 화살표 정의 */}
              <defs>
                <linearGradient id="ball-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#475569" />
                  <stop offset="100%" stopColor="#0f172a" />
                </linearGradient>
                <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                  <path d="M0,0 L0,10 L10,5 Z" fill="#10b981" />
                </marker>
                <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
                  <path d="M0,0 L0,10 L10,5 Z" fill="#ef4444" />
                </marker>
              </defs>
            </svg>

            {/* 오버레이 팁 */}
            <div className="absolute top-4 left-4 bg-white/80 backdrop-blur-sm p-3 rounded-xl border border-slate-200 text-xs shadow-sm">
              <div className="flex items-center gap-2 mb-1">
                <div className="w-3 h-3 bg-emerald-500 rounded-full"></div>
                <span>속도 벡터 (접선 방향)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-rose-500 rounded-full"></div>
                <span>가속도 벡터 (중심 방향)</span>
              </div>
            </div>
          </div>

          {/* 우측 컨트롤 패널 */}
          <div className="w-full lg:w-80 bg-slate-50 border-l border-slate-200 p-6 space-y-8 overflow-y-auto">
            <section className="space-y-4">
              <div className="flex items-center gap-2 text-slate-500">
                <Settings2 size={18} />
                <h3 className="font-bold text-sm tracking-wide uppercase">물리량 설정</h3>
              </div>

              <div className="space-y-6">
                {/* 질량 m */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-sm">
                    <label className="text-slate-600">질량 (m)</label>
                    <span className="font-mono font-bold text-slate-900">{mass.toFixed(1)} kg</span>
                  </div>
                  <input
                    type="range"
                    min="0.5"
                    max="5.0"
                    step="0.1"
                    value={mass}
                    onChange={(e) => setMass(parseFloat(e.target.value))}
                    className="w-full h-1.5 bg-slate-300 rounded-lg appearance-none cursor-pointer accent-slate-900"
                  />
                </div>

                {/* 반지름 r */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-sm">
                    <label className="text-slate-600">반지름 (r)</label>
                    <span className="font-mono font-bold text-slate-900">{radius} px</span>
                  </div>
                  <input
                    type="range"
                    min="50"
                    max="200"
                    step="1"
                    value={radius}
                    onChange={(e) => {
                      setRadius(parseInt(e.target.value));
                      if (isCut) handleReset();
                    }}
                    className="w-full h-1.5 bg-slate-300 rounded-lg appearance-none cursor-pointer accent-slate-900"
                  />
                </div>

                {/* 선속도 v */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-sm">
                    <label className="text-slate-600">선속도 (v)</label>
                    <span className="font-mono font-bold text-slate-900">{linearVelocity} px/s</span>
                  </div>
                  <input
                    type="range"
                    min="50"
                    max="400"
                    step="5"
                    value={linearVelocity}
                    onChange={(e) => {
                      setLinearVelocity(parseInt(e.target.value));
                      if (isCut) handleReset();
                    }}
                    className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-900"
                  />
                </div>
              </div>
            </section>

            <section className="space-y-4">
              <div className="flex items-center gap-2 text-slate-500">
                <Activity size={18} />
                <h3 className="font-bold text-sm tracking-wide uppercase">제어 시스템</h3>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={handleTogglePause}
                  className={`flex items-center justify-center gap-2 px-4 py-3 rounded-xl transition-all font-semibold ${
                    isPaused ? 'bg-emerald-500 text-white hover:bg-emerald-600' : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
                  }`}
                >
                  {isPaused ? <Play size={16} fill="currentColor" /> : <Pause size={16} fill="currentColor" />}
                  {isPaused ? '재개' : '일시정지'}
                </button>
                <button
                  onClick={handleReset}
                  className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-slate-200 text-slate-700 hover:bg-slate-300 transition-all font-semibold"
                >
                  <RotateCcw size={16} />
                  초기화
                </button>
                <button
                  onClick={handleCut}
                  disabled={isCut}
                  className={`flex items-center justify-center col-span-2 gap-2 px-4 py-3 rounded-xl transition-all font-bold tracking-tight shadow-md ${
                    isCut 
                    ? 'bg-slate-100 text-slate-400 cursor-not-allowed border-slate-200' 
                    : 'bg-rose-500 text-white hover:bg-rose-600 hover:translate-y-[-2px] active:translate-y-[0px]'
                  }`}
                >
                  <Scissors size={18} />
                  실 끊기 (구심력 제거)
                </button>
              </div>
            </section>

            {/* 수식 및 관계식 정보 */}
            <div className="mt-8 p-5 rounded-2xl bg-white border border-slate-200 space-y-3 shadow-inner">
              <div className="flex items-center gap-2 text-slate-400 mb-1">
                <Info size={16} />
                <h4 className="text-xs font-bold uppercase tracking-wider">주요 관계식</h4>
              </div>
              <div className="space-y-2.5 font-mono text-[13px]">
                <div className="flex justify-between items-center text-slate-500">
                  <span className="bg-slate-100 px-1 rounded italic text-xs">v = rω</span>
                  <span className="text-slate-900">{linearVelocity} = {radius} × {omega.toFixed(3)}</span>
                </div>
                <div className="flex justify-between items-center text-slate-500">
                  <span className="bg-slate-100 px-1 rounded italic text-xs">a = v²/r</span>
                  <span className="text-slate-900">{centripetalAcc.toFixed(1)} = {linearVelocity}² / {radius}</span>
                </div>
                <div className="flex justify-between items-center text-slate-500 border-t border-slate-100 pt-2">
                  <span className="font-bold text-slate-700 italic text-xs">F = ma</span>
                  <span className="text-slate-900">{centripetalForce.toFixed(1)} = {mass.toFixed(1)} × {centripetalAcc.toFixed(1)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 푸터 안내 */}
        <div className="bg-slate-50 py-3 px-6 border-t border-slate-200 flex justify-between items-center">
          <p className="text-xs text-slate-500">
            <strong>실 끊기 효과:</strong> 등속 원운동을 하던 물체는 구심력이 사라지는 순간, 
            <span className="text-rose-600 font-bold ml-1 italic underline decoration-rose-200 underline-offset-4">접선 방향으로 등속 직선 이동</span>합니다 (관성의 법칙).
          </p>
          <span className="text-[10px] text-slate-400 font-mono">Physics Simulation V1.0</span>
        </div>
      </div>
    </div>
  );
};

export default CircularMotionSimulation;
