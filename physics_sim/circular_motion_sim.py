import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="등속 원운동 시뮬레이션", layout="wide")
    
    # 상단 안내 문구 (Streamlit 스타일)
    st.title("🎡 등속 원운동 (Uniform Circular Motion) 탐구")
    st.markdown("""
    이 시뮬레이션은 등속 원운동의 물리적 원리를 시각적으로 학습하기 위해 제작되었습니다. 
    **속도 벡터(접선 방향)**와 **가속도 벡터(중심 방향)**의 관계를 관찰하고, 
    '실 끊기' 기능을 통해 구심력이 사라질 때의 관성 운동을 확인해 보세요.
    """)

    # React 컴포넌트를 위한 HTML/JS 소스
    # 주요 라이브러리: React, ReactDOM, Babel (JSX 변환), Tailwind CSS, Lucide Icons
    react_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; }
            .no-scrollbar::-webkit-scrollbar { display: none; }
            .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            // Lucide 아이콘 컴포넌트 래퍼 (CDN 환경 대응)
            const Icon = ({ name, size = 18, className = "" }) => {
                const iconRef = useRef(null);
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const CircularMotionSimulation = () => {
                // --- 상태 관리 ---
                const [mass, setMass] = useState(2.5);
                const [radius, setRadius] = useState(120);
                const [linearVelocity, setLinearVelocity] = useState(150);
                const [isPaused, setIsPaused] = useState(false);
                const [isCut, setIsCut] = useState(false);
                
                const [angle, setAngle] = useState(0);
                const [startAngle, setStartAngle] = useState(0);
                const [cutPosition, setCutPosition] = useState({ x: 0, y: 0 });
                const [cutVelocity, setCutVelocity] = useState({ x: 0, y: 0 });
                const [elapsedTimeAfterCut, setElapsedTimeAfterCut] = useState(0);

                const requestRef = useRef();
                const lastTimeRef = useRef();

                // --- 물리량 계산 ---
                const r = radius;
                const v = linearVelocity;
                const omega = v / r;
                const centripetalAcc = (v * v) / r;
                const centripetalForce = mass * centripetalAcc;

                const animate = (time) => {
                    if (lastTimeRef.current !== undefined && !isPaused) {
                        const deltaTime = (time - lastTimeRef.current) / 1000;
                        if (!isCut) {
                            setAngle((prev) => (prev + omega * deltaTime) % (Math.PI * 2));
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
                }, [isPaused, isCut, omega]);

                const handleCut = () => {
                    if (isCut) return;
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
                    setElapsedTimeAfterCut(0);
                    setIsPaused(false);
                };

                const centerX = 250;
                const centerY = 250;
                let ballX, ballY, velX, velY, accX, accY;

                if (!isCut) {
                    ballX = centerX + r * Math.cos(angle);
                    ballY = centerY + r * Math.sin(angle);
                    velX = -Math.sin(angle) * (v / 2);
                    velY = Math.cos(angle) * (v / 2);
                    accX = -Math.cos(angle) * (centripetalAcc / 5);
                    accY = -Math.sin(angle) * (centripetalAcc / 5);
                } else {
                    ballX = centerX + cutPosition.x + cutVelocity.x * elapsedTimeAfterCut;
                    ballY = centerY + cutPosition.y + cutVelocity.y * elapsedTimeAfterCut;
                    velX = cutVelocity.x / 2;
                    velY = cutVelocity.y / 2;
                    accX = 0; accY = 0;
                }

                const getArcPath = () => {
                    if (isCut) return null;
                    const startX = centerX + r;
                    const startY = centerY;
                    let diff = angle;
                    const largeArcFlag = diff > Math.PI ? 1 : 0;
                    return `M ${centerX} ${centerY} L ${startX} ${startY} A ${r} ${r} 0 ${largeArcFlag} 1 ${ballX} ${ballY} Z`;
                };

                return (
                    <div className="flex flex-col items-center bg-white min-h-screen p-2 text-slate-800">
                        <div className="w-full max-w-5xl rounded-2xl shadow-2xl border border-slate-200 overflow-hidden bg-white">
                            {/* 헤더 데이터 */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-slate-900 text-white">
                                <div className="space-y-1">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase">선속도 (v)</p>
                                    <p className="text-xl font-mono text-emerald-400">{v.toFixed(0)} <small className="text-[10px]">px/s</small></p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase">각속도 (ω)</p>
                                    <p className="text-xl font-mono text-amber-400">{omega.toFixed(3)} <small className="text-[10px]">rad/s</small></p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase">구심 가속도 (a)</p>
                                    <p className="text-xl font-mono text-rose-400">{centripetalAcc.toFixed(1)}</p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase">구심력 (F)</p>
                                    <p className="text-xl font-mono text-sky-400">{centripetalForce.toFixed(1)} <small className="text-[10px]">N</small></p>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row h-[550px]">
                                {/* 캔버스 */}
                                <div className="flex-1 bg-slate-50 relative overflow-hidden flex items-center justify-center p-4">
                                    <svg viewBox="0 0 500 500" className="w-full h-full max-w-[450px]">
                                        <circle cx={centerX} cy={centerY} r="3" fill="#64748b" />
                                        {!isCut && <circle cx={centerX} cy={centerY} r={r} fill="none" stroke="#e2e8f0" strokeWidth="1.5" strokeDasharray="5,5" />}
                                        {!isCut && <path d={getArcPath()} fill="rgba(245, 158, 11, 0.15)" />}
                                        {!isCut && <line x1={centerX} y1={centerY} x2={ballX} y2={ballY} stroke="#94a3b8" strokeWidth="1.5" />}
                                        
                                        {/* Velocity Vector */}
                                        <g>
                                            <line x1={ballX} y1={ballY} x2={ballX + velX} y2={ballY + velY} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                            <text x={ballX + velX + 5} y={ballY + velY} fill="#059669" className="text-[12px] font-bold font-mono">v</text>
                                        </g>
                                        
                                        {/* Acceleration Vector */}
                                        {!isCut && (
                                            <g>
                                                <line x1={ballX} y1={ballY} x2={ballX + accX} y2={ballY + accY} stroke="#ef4444" strokeWidth="3" markerEnd="url(#arrow-red)" />
                                                <text x={ballX + accX - 15} y={ballY + accY - 5} fill="#dc2626" className="text-[12px] font-bold font-mono">a</text>
                                            </g>
                                        )}

                                        <circle cx={ballX} cy={ballY} r={10 + mass * 2} fill="url(#grad)" stroke="#1e293b" strokeWidth="1" />
                                        
                                        <defs>
                                            <radialGradient id="grad">
                                                <stop offset="0%" stopColor="#475569" />
                                                <stop offset="100%" stopColor="#0f172a" />
                                            </radialGradient>
                                            <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L0,10 L10,5 Z" fill="#10b981"/></marker>
                                            <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L0,10 L10,5 Z" fill="#ef4444"/></marker>
                                        </defs>
                                    </svg>
                                    
                                    <div className="absolute top-4 left-4 bg-white/70 backdrop-blur-sm p-2 rounded-lg border border-slate-200 text-[10px] space-y-1 shadow-sm">
                                        <div className="flex items-center gap-1.5"><div className="w-2 h-2 bg-emerald-500 rounded-full"></div><span>속도</span></div>
                                        <div className="flex items-center gap-1.5"><div className="w-2 h-2 bg-rose-500 rounded-full"></div><span>가속도</span></div>
                                    </div>
                                </div>

                                {/* 컨트롤러 */}
                                <div className="w-full lg:w-72 bg-slate-50 border-l border-slate-200 p-5 flex flex-col gap-6 overflow-y-auto no-scrollbar">
                                    <div className="space-y-4">
                                        <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                            <Icon name="settings-2" size={14} /> 설정 (Parameters)
                                        </h4>
                                        <div className="space-y-5">
                                            <div className="space-y-2">
                                                <div className="flex justify-between text-xs font-semibold"><span>질량 (m)</span><span>{mass.toFixed(1)} kg</span></div>
                                                <input type="range" min="0.5" max="5.0" step="0.1" value={mass} onChange={e=>setMass(parseFloat(e.target.value))} className="w-full h-1 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-900" />
                                            </div>
                                            <div className="space-y-2">
                                                <div className="flex justify-between text-xs font-semibold"><span>반지름 (r)</span><span>{radius} px</span></div>
                                                <input type="range" min="50" max="200" step="1" value={radius} onChange={e=>{setRadius(parseInt(e.target.value)); if(isCut) handleReset();}} className="w-full h-1 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-900" />
                                            </div>
                                            <div className="space-y-2">
                                                <div className="flex justify-between text-xs font-semibold"><span>선속도 (v)</span><span>{linearVelocity} px/s</span></div>
                                                <input type="range" min="50" max="400" step="5" value={linearVelocity} onChange={e=>{setLinearVelocity(parseInt(e.target.value)); if(isCut) handleReset();}} className="w-full h-1 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-900" />
                                            </div>
                                        </div>
                                    </div>

                                    <div className="space-y-3 pt-2">
                                        <div className="grid grid-cols-2 gap-2">
                                            <button onClick={()=>setIsPaused(!isPaused)} className="flex items-center justify-center gap-2 py-2.5 bg-slate-200 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-300 transition-colors">
                                                <Icon name={isPaused ? "play" : "pause"} size={14} /> {isPaused ? "시작" : "정지"}
                                            </button>
                                            <button onClick={handleReset} className="flex items-center justify-center gap-2 py-2.5 bg-slate-200 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-300 transition-colors">
                                                <Icon name="rotate-ccw" size={14} /> 초기화
                                            </button>
                                        </div>
                                        <button onClick={handleCut} disabled={isCut} className={`w-full py-3 flex items-center justify-center gap-2 rounded-xl text-xs font-black shadow-lg transition-all ${isCut ? 'bg-slate-100 text-slate-300' : 'bg-rose-500 text-white hover:bg-rose-600 active:scale-95'}`}>
                                            <Icon name="scissors" size={16} /> 실 끊기 (관성 확인)
                                        </button>
                                    </div>

                                    <div className="mt-auto bg-white p-3 rounded-xl border border-slate-200 space-y-2">
                                        <p className="text-[10px] font-bold text-slate-400">학습 포인트</p>
                                        <div className="text-[11px] leading-relaxed text-slate-600 space-y-1">
                                            <p>• <b>v = rω</b>: 반지름과 선속도의 비례</p>
                                            <p>• <b>a = v²/r</b>: 구심 가속도의 크기</p>
                                            <p>• 실을 끊으면 물체는 <b>접선 방향</b>으로 운동합니다.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<CircularMotionSimulation />);
        </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트로 HTML 삽입 (높이를 충분히 확보)
    components.html(react_code, height=700, scrolling=False)

if __name__ == "__main__":
    run_sim()
