import streamlit as st
import streamlit.components.v1 as components

# 페이지 제목
st.title("🚀 가속좌표계와 관성력 실시간 탐구")

# React 컴포넌트를 위한 HTML/JS 소스
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
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
        body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background-color: transparent; overflow: hidden; }
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(224, 231, 255, 0.5); }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        const Icon = ({ name, size = 18, className = "" }) => {
            useEffect(() => {
                if (window.lucide) window.lucide.createIcons();
            }, [name]);
            return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
        };

        const App = () => {
            const [accel, setAccel] = useState(0); 
            const [view, setView] = useState('external'); 
            const [isMoving, setIsMoving] = useState(false);
            
            const posRef = useRef(0);
            const velRef = useRef(0);
            const [renderPos, setRenderPos] = useState(0);
            const [renderVel, setRenderVel] = useState(0);

            const g = 9.8; 
            const L = 130; 
            const targetTheta = Math.atan(accel / g);
            const [currentTheta, setCurrentTheta] = useState(0);

            useEffect(() => {
                let animationId;
                let lastTime = performance.now();

                const animate = (time) => {
                    const dt = Math.min((time - lastTime) / 1000, 0.05);
                    lastTime = time;

                    if (isMoving) {
                        velRef.current += accel * dt;
                        posRef.current += velRef.current * dt * 40; // Scale movement
                        setRenderPos(posRef.current);
                        setRenderVel(velRef.current);
                    }

                    setCurrentTheta(prev => {
                        const diff = targetTheta - prev;
                        return prev + diff * 0.1;
                    });
                    animationId = requestAnimationFrame(animate);
                };
                animationId = requestAnimationFrame(animate);
                return () => cancelAnimationFrame(animationId);
            }, [accel, isMoving, targetTheta]);

            const pivotX = 180; 
            const pivotY = 50;
            const bobX = pivotX - L * Math.sin(currentTheta);
            const bobY = pivotY + L * Math.cos(currentTheta);

            // Calculate background movement
            // External view: background is fixed (offset 0), bus moves by x
            // Internal view: bus is fixed, background moves by -x
            const bgOffset = view === 'internal' ? (-renderPos % 800) : 0;
            const busX = view === 'external' ? ((renderPos % 1000) - 100) : 220;

            return (
                <div className="p-4 max-w-7xl mx-auto space-y-6">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-4 space-y-4">
                            <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-6">
                                <div className="space-y-4">
                                    <div className="space-y-4">
                                        <div className="flex bg-slate-100 p-1 rounded-2xl text-[11px] font-bold">
                                            <button onClick={() => setView('external')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'external' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500'}`}>외부 시점</button>
                                            <button onClick={() => setView('internal')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'internal' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500'}`}>내부 시점</button>
                                        </div>
                                        <div className="space-y-3">
                                            <div className="flex justify-between text-[10px] font-black text-slate-400 uppercase tracking-widest">
                                                버스 가속도 (a)
                                                <span className="text-indigo-600 font-black">{accel.toFixed(1)} m/s²</span>
                                            </div>
                                            <input type="range" min="-10" max="10" step="0.5" value={accel} onChange={(e) => setAccel(parseFloat(e.target.value))} className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-indigo-600" />
                                        </div>
                                        <button onClick={() => setIsMoving(!isMoving)} className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-2 ${isMoving ? 'bg-rose-500 text-white' : 'bg-indigo-600 text-white shadow-lg'}`}>
                                            <Icon name={isMoving ? "pause" : "play"} /> {isMoving ? "실험 중지" : "운동 시작"}
                                        </button>
                                        <button onClick={() => {posRef.current=0; velRef.current=0; setRenderPos(0); setRenderVel(0);}} className="w-full py-2 bg-slate-100 text-slate-500 rounded-xl text-xs font-bold hover:bg-slate-200">초기화</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="lg:col-span-8">
                            <div className="bg-white rounded-[40px] shadow-2xl border border-slate-100 overflow-hidden relative h-[500px]">
                                <div className="p-4 bg-slate-900 flex justify-between text-white/50 text-[10px] font-black tracking-widest">
                                    <span>{view === 'internal' ? 'INTERNAL: BUS IS STATIONARY' : 'EXTERNAL: WORLD IS STATIONARY'}</span>
                                    <div className="flex gap-4">
                                        <span className="text-blue-400">● Tension</span>
                                        {view==='internal' && <span className="text-rose-400">● Inertial Force</span>}
                                    </div>
                                </div>
                                <div className="relative h-full bg-slate-50 overflow-hidden">
                                    {/* Road and Background Scenery */}
                                    <svg viewBox="0 0 800 500" className="w-full h-full select-none">
                                        <defs>
                                            <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" /></marker>
                                            <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" /></marker>
                                        </defs>

                                        {/* Road Marks (Moving if internal) */}
                                        <g transform={`translate(${bgOffset}, 320)`}>
                                            {[...Array(20)].map((_, i) => (
                                                <rect key={i} x={i * 100 - 200} y="0" width="2" height="40" fill="#e2e8f0" />
                                            ))}
                                            <line x1="-1000" y1="0" x2="2000" y2="0" stroke="#cbd5e1" strokeWidth="2" />
                                        </g>

                                        {/* Bus */}
                                        <g transform={`translate(${busX}, 140)`}>
                                            <rect x="0" y="0" width="360" height="180" rx="32" fill="#3b82f6" stroke="#1e40af" strokeWidth="4" />
                                            {/* Windows */}
                                            <rect x="40" y="40" width="70" height="60" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            <rect x="140" y="40" width="80" height="70" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            <rect x="250" y="40" width="70" height="60" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            
                                            {/* Wheels */}
                                            <circle cx="80" cy="180" r="30" fill="#0f172a" /><circle cx="280" cy="180" r="30" fill="#0f172a" />
                                            
                                            {/* Bob */}
                                            <line x1="180" y1="50" x2={bobX} y2={bobY} stroke="white" strokeWidth="4" />
                                            <circle cx={bobX} cy={bobY} r="18" fill="white" stroke="#1e293b" strokeWidth="3" />

                                            {/* Forces */}
                                            <g transform={`translate(${bobX}, ${bobY})`}>
                                                <line x1="0" y1="0" x2={(180 - bobX)*0.8} y2={(50 - bobY)*0.8} stroke="#3b82f6" strokeWidth="4" markerEnd="url(#arrow-blue)" />
                                                <text x="10" y="-10" className="text-[10px] font-black fill-blue-600">T</text>
                                                {view === 'internal' && Math.abs(accel) > 0.1 && (
                                                    <g>
                                                        <line x1="0" y1="0" x2={-accel * 10} y2="0" stroke="#f43f5e" strokeWidth="4" markerEnd="url(#arrow-red)" />
                                                        <text x={-accel * 10} y="-10" textAnchor="middle" className="text-[10px] font-black fill-rose-600">-ma</text>
                                                    </g>
                                                )}
                                            </g>
                                        </g>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# 시뮬레이션 삽입
components.html(react_code, height=600, scrolling=True)

# 탐구 내용 추가
st.divider()
st.info("**가상 실험 가이드**: 내부 시점에서는 버스가 멈춰 있는 것처럼 보이며, 대신 **바깥 세상이 뒤로 빠르게 지나가는 것**으로 처리했습니다. 이것이 바로 가속 좌표계에서의 관찰자 시점입니다.")
