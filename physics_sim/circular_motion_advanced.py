import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="등속 원운동 심화 탐구", layout="wide")
    
    st.title("🏀 [수행평가 1-3] 등속 원운동 심화 탐구 (Advanced Study)")
    st.markdown("""
    이 시뮬레이션은 등속 원운동의 상급 개념인 **라디안의 정의, 반경에 따른 속도 관계, 그리고 가속도 벡터의 증명**을 위해 제작되었습니다. 
    상단의 탭을 통해 3단계 학습 모드를 탐구해 보세요.
    """)

    react_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
            body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; overflow: hidden; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                const iconRef = useRef(null);
                useEffect(() => { if (window.lucide) window.lucide.createIcons(); }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const CircularMotionAdvanced = () => {
                const [mode, setMode] = useState(1);
                const [isPaused, setIsPaused] = useState(false);
                const [isCut, setIsCut] = useState(false);
                const [radius, setRadius] = useState(120);
                const [theta, setTheta] = useState(1.0);
                const [omega, setOmega] = useState(1.5);
                const [angle, setAngle] = useState(0);
                const [elapsedTimeAfterCut, setElapsedTimeAfterCut] = useState(0);
                const [cutState, setCutState] = useState({ pos: { x: 0, y: 0 }, vel: { x: 0, y: 0 } });
                const [savedVectors, setSavedVectors] = useState([]);
                
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
                    setIsCut(false); setAngle(0); setElapsedTimeAfterCut(0); setSavedVectors([]); setIsPaused(false);
                };

                const handleCut = () => {
                    const x = radius * Math.cos(angle); const y = radius * Math.sin(angle);
                    const v = radius * omega; const vx = -v * Math.sin(angle); const vy = v * Math.cos(angle);
                    setCutState({ pos: { x, y }, vel: { x: vx, y: vy } });
                    setIsCut(true);
                };

                const saveVector = () => {
                    if (savedVectors.length >= 2) setSavedVectors([]);
                    const v = radius * omega;
                    setSavedVectors(prev => [...prev, {
                        pos: { x: radius * Math.cos(angle), y: radius * Math.sin(angle) },
                        vel: { x: -v * Math.sin(angle), y: v * Math.cos(angle) }
                    }]);
                };

                const CX = 250; const CY = 180;

                return (
                    <div className="flex flex-col bg-white min-h-screen p-2 text-slate-800">
                        <div className="w-full flex bg-slate-100 p-1.5 gap-1.5 border border-slate-200 rounded-2xl mb-4 shadow-sm">
                            {[
                                { id: 1, label: 'Mode 1: 라디안 정의', icon: 'layers' },
                                { id: 2, label: 'Mode 2: v = rω 탐구', icon: 'zap' },
                                { id: 3, label: 'Mode 3: 가속도 증명', icon: 'scissors' }
                            ].map(m => (
                                <button key={m.id} onClick={() => { setMode(m.id); handleReset(); }} className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-xs font-black transition-all ${mode === m.id ? 'bg-white shadow text-blue-600' : 'text-slate-400 hover:bg-slate-200'}`}>
                                    <Icon name={m.icon} size={14}/> {m.label}
                                </button>
                            ))}
                        </div>

                        <div className="flex flex-col lg:flex-row gap-4 h-[550px]">
                            <div className="flex-1 bg-slate-50 border border-slate-100 rounded-3xl relative overflow-hidden flex items-center justify-center">
                                <svg viewBox="0 0 500 400" className="w-full h-full">
                                    <circle cx={CX} cy={CY} r="2" fill="#94a3b8" />
                                    {mode === 1 && (
                                        <g>
                                            <circle cx={CX} cy={CY} r={radius} fill="none" stroke="#e2e8f0" strokeWidth="2" strokeDasharray="4,4" />
                                            <path d={`M ${CX} ${CY} L ${CX + radius} ${CY} A ${radius} ${radius} 0 ${theta > Math.PI ? 1 : 0} 1 ${CX + radius * Math.cos(theta)} ${CY + radius * Math.sin(theta)} Z`} fill="rgba(59, 130, 246, 0.1)" stroke="#3b82f6" strokeWidth="2" />
                                            <path d={`M ${CX + radius} ${CY} A ${radius} ${radius} 0 ${theta > Math.PI ? 1 : 0} 1 ${CX + radius * Math.cos(theta)} ${CY + radius * Math.sin(theta)}`} fill="none" stroke="#ef4444" strokeWidth="5" strokeLinecap="round" />
                                            {Math.abs(theta - 1) < 0.05 && <text x={CX + radius + 10} y={CY + 50} className="text-[12px] font-black fill-rose-600 italic animate-pulse">s = r (1 rad)</text>}
                                        </g>
                                    )}
                                    {mode === 2 && (
                                        <g>
                                            {[radius, radius * 0.6].map((r, i) => {
                                                const x = CX + r * Math.cos(angle); const y = CY + r * Math.sin(angle);
                                                const v_sc = -Math.sin(angle) * (r * omega * 0.4); const vy_sc = Math.cos(angle) * (r * omega * 0.4);
                                                return (
                                                    <g key={i}>
                                                        <circle cx={CX} cy={CY} r={r} fill="none" stroke="#e2e8f0" strokeWidth="1" />
                                                        <line x1={CX} y1={CY} x2={x} y2={y} stroke="#cbd5e1" strokeWidth="1.5" />
                                                        <line x1={x} y1={y} x2={x + v_sc} y2={y + vy_sc} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                                        <circle cx={x} cy={y} r="8" fill={i === 0 ? "#0f172a" : "#64748b"} />
                                                    </g>
                                                );
                                            })}
                                        </g>
                                    )}
                                    {mode === 3 && (
                                        <g>
                                           <circle cx={CX} cy={CY} r={radius} fill="none" stroke="#e2e8f0" strokeWidth="1" strokeDasharray="5,5" />
                                           {!isCut ? (
                                             <g>
                                                <line x1={CX} y1={CY} x2={CX + radius * Math.cos(angle)} y2={CY + radius * Math.sin(angle)} stroke="#cbd5e1" strokeWidth="2" />
                                                <line x1={CX + radius * Math.cos(angle)} y1={CY + radius * Math.sin(angle)} x2={CX + radius * Math.cos(angle) - (radius * omega * 0.4) * Math.sin(angle)} y2={CY + radius * Math.sin(angle) + (radius * omega * 0.4) * Math.cos(angle)} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                                <line x1={CX + radius * Math.cos(angle)} y1={CY + radius * Math.sin(angle)} x2={CX + radius * Math.cos(angle) * 0.7} y2={CY + radius * Math.sin(angle) * 0.7} stroke="#ef4444" strokeWidth="3" markerEnd="url(#arrow-red)" />
                                                <circle cx={CX + radius * Math.cos(angle)} cy={CY + radius * Math.sin(angle)} r="10" fill="#0f172a" />
                                             </g>
                                           ) : (
                                             <circle cx={CX + cutState.pos.x + cutState.vel.x * elapsedTimeAfterCut} cy={CY + cutState.pos.y + cutState.vel.y * elapsedTimeAfterCut} r="10" fill="#64748b" />
                                           )}
                                           {savedVectors.length > 0 && (
                                             <g transform={`translate(${CX + 140}, ${CY + 80}) scale(0.8)`}>
                                                <rect x="-60" y="-60" width="120" height="120" fill="white/80" stroke="#e2e8f0" rx="10" />
                                                <circle cx="0" cy="0" r="2" fill="black" />
                                                {savedVectors.map((sv, idx) => (
                                                   <line key={idx} x1="0" y1="0" x2={sv.vel.x*0.4} y2={sv.vel.y*0.4} stroke="#10b981" strokeWidth="2" opacity={idx===0 ? 0.3 : 1} markerEnd="url(#arrow-green)" />
                                                ))}
                                                {savedVectors.length === 2 && (
                                                  <line x1={savedVectors[0].vel.x*0.4} y1={savedVectors[0].vel.y*0.4} x2={savedVectors[1].vel.x*0.4} y2={savedVectors[1].vel.y*0.4} stroke="#ef4444" strokeWidth="4" markerEnd="url(#arrow-red)" />
                                                )}
                                                <text x="0" y="55" textAnchor="middle" className="text-[10px] font-black fill-slate-400">Δv Direction</text>
                                             </g>
                                           )}
                                        </g>
                                    )}
                                    <defs>
                                        <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L0,10 L10,5 Z" fill="#10b981"/></marker>
                                        <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L0,10 L10,5 Z" fill="#ef4444"/></marker>
                                    </defs>
                                </svg>
                                <div className="absolute top-4 left-4 bg-white/70 backdrop-blur-md p-4 rounded-3xl border border-white/50 shadow-sm pointer-events-none space-y-2">
                                    <p className="text-[14px] font-black italic underline leading-none">
                                        {mode === 1 ? `s = rθ = ${(radius*theta).toFixed(1)}` : mode === 2 ? `v = rω = ${(radius*omega).toFixed(1)}` : 'a = v²/r'}
                                    </p>
                                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">Physics Study Dashboard</p>
                                </div>
                            </div>

                            <div className="w-full lg:w-80 bg-slate-50 border border-slate-100 rounded-3xl p-6 flex flex-col gap-6 overflow-y-auto no-scrollbar shadow-inner">
                                <div className="space-y-4">
                                    <div className="flex justify-between items-center"><span className="text-[11px] font-bold text-slate-400">반지름 (r)</span><span className="text-xs font-mono font-black">{radius}px</span></div>
                                    <input type="range" min="50" max="200" value={radius} onChange={e=>setRadius(parseInt(e.target.value))} className="w-full h-1 bg-slate-200 rounded-lg appearance-none accent-slate-900" />
                                    {mode === 1 ? (
                                        <div className="space-y-4">
                                            <div className="flex justify-between items-center"><span className="text-[11px] font-bold text-slate-400">중심각 (θ)</span><span className="text-xs font-mono font-black text-rose-500">{theta.toFixed(2)} rad</span></div>
                                            <input type="range" min="0" max="6.28" step="0.01" value={theta} onChange={e=>setTheta(parseFloat(e.target.value))} className="w-full h-1 bg-slate-200 rounded-lg appearance-none accent-rose-500" />
                                        </div>
                                    ) : (
                                        <div className="space-y-4">
                                            <div className="flex justify-between items-center"><span className="text-[11px] font-bold text-slate-400">각속도 (ω)</span><span className="text-xs font-mono font-black text-emerald-500">{omega.toFixed(1)} rad/s</span></div>
                                            <input type="range" min="0.5" max="5.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full h-1 bg-slate-200 rounded-lg appearance-none accent-emerald-500" />
                                        </div>
                                    )}
                                </div>

                                <div className="space-y-3">
                                    <button onClick={()=>setIsPaused(!isPaused)} className="w-full flex items-center justify-center gap-2 py-3 bg-white border border-slate-200 rounded-2xl text-xs font-black hover:bg-slate-50 transition-all">
                                        <Icon name={isPaused ? "play" : "pause"} size={14}/> {isPaused ? "재개" : "일시정지"}
                                    </button>
                                    {mode === 3 && (
                                        <>
                                            <button onClick={saveVector} className="w-full flex items-center justify-center gap-2 py-3 bg-blue-600 text-white rounded-2xl text-xs font-black shadow-lg shadow-blue-100 hover:bg-blue-700 transition-all">
                                                <Icon name="plus" size={14}/> 벡터 자취 기록 ({savedVectors.length}/2)
                                            </button>
                                            <button onClick={handleCut} className="w-full py-3 bg-rose-500 text-white rounded-2xl text-xs font-black hover:bg-rose-600 transition-all">실 끊기 (관성 확인)</button>
                                        </>
                                    )}
                                    <button onClick={handleReset} className="w-full py-3 text-slate-400 text-xs font-bold hover:text-slate-600">초기화 (Reset)</button>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<CircularMotionAdvanced />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=720, scrolling=False)

if __name__ == "__main__":
    run_sim()
