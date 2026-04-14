import streamlit as st
import streamlit.components.v1 as components

# React 컴포넌트를 위한 HTML/JS 소스
react_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>가속좌표계 시뮬레이션</title>
    <!-- Stable CDN -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
        body { 
            font-family: 'Pretendard', sans-serif; 
            margin: 0; 
            padding: 0; 
            background-color: transparent; 
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }
    </style>
</head>
<body>
    <div id="root">
        <div style="padding: 50px; text-align: center; color: #64748b; font-family: sans-serif;">
            시뮬레이션을 초기화하고 있습니다...
        </div>
    </div>

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
            const [showVectors, setShowVectors] = useState(true);
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
                        posRef.current += velRef.current * dt * 30; 
                        if (posRef.current > 600) posRef.current = -400;
                        if (posRef.current < -400) posRef.current = 600;
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

            return (
                <div className="p-4 max-w-7xl mx-auto space-y-6">
                    <div className="flex items-center gap-4">
                        <div className="bg-indigo-600 p-3 rounded-2xl shadow-lg">
                            <Icon name="rocket" size={24} className="text-white" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-black text-slate-900 tracking-tight">가속좌표계와 관성력 실시간 탐구</h1>
                            <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mt-1">General Relativity: Inertial Force Simulation</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-4 space-y-4">
                            <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-6">
                                <div className="space-y-4">
                                    <div className="space-y-3">
                                        <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Observer View</label>
                                        <div className="flex bg-slate-100 p-1 rounded-2xl">
                                            <button onClick={() => setView('external')} className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all ${view === 'external' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500'}`}>외부 (관성계)</button>
                                            <button onClick={() => setView('internal')} className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all ${view === 'internal' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500'}`}>내부 (비관성계)</button>
                                        </div>
                                    </div>
                                    <div className="space-y-3">
                                        <div className="flex justify-between items-center text-[10px] font-black text-slate-400 uppercase tracking-widest">
                                            <span>Acceleration (a)</span>
                                            <span className="text-indigo-600 font-black">{accel.toFixed(1)} m/s²</span>
                                        </div>
                                        <input type="range" min="-10" max="10" step="0.5" value={accel} onChange={(e) => setAccel(parseFloat(e.target.value))} className="w-full" />
                                    </div>
                                    <div className="flex flex-col gap-2">
                                        <button onClick={() => setIsMoving(!isMoving)} className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-2 ${isMoving ? 'bg-rose-500 text-white' : 'bg-indigo-600 text-white shadow-lg shadow-indigo-100'}`}>
                                            <Icon name={isMoving ? "pause" : "play"} /> {isMoving ? "실험 중지" : "운동 시작"}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div className="glass-card p-5 rounded-[32px] shadow-sm">
                                <h3 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">Live Values</h3>
                                <div className="space-y-2">
                                    <div className="bg-slate-50 p-3 rounded-2xl flex justify-between items-center text-xs font-bold">
                                        <span className="text-slate-500">각도</span>
                                        <span className="text-slate-900">{((currentTheta * 180) / Math.PI).toFixed(1)}°</span>
                                    </div>
                                    <div className="bg-slate-50 p-3 rounded-2xl flex justify-between items-center text-xs font-bold">
                                        <span className="text-slate-500">버스 속도</span>
                                        <span className="text-slate-900">{renderVel.toFixed(1)} m/s</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="lg:col-span-8">
                            <div className="bg-white rounded-[40px] shadow-2xl border border-slate-100 overflow-hidden relative h-[550px]">
                                <div className="p-4 bg-slate-900 flex justify-between text-white/50 text-[10px] font-black uppercase tracking-widest">
                                    <span>{view === 'internal' ? 'Non-Inertial Perspective' : 'Inertial Perspective'}</span>
                                    <div className="flex gap-4">
                                        <span>● Gravity</span><span>● Tension</span>{view==='internal' && <span className="text-rose-400">● Inertial</span>}
                                    </div>
                                </div>
                                <div className="relative h-full bg-slate-50">
                                    <svg viewBox="0 0 800 500" className="w-full h-full select-none">
                                        <defs>
                                            <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" /></marker>
                                            <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" /></marker>
                                            <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" /></marker>
                                        </defs>

                                        <g transform={`translate(${view === 'external' ? renderPos + 100 : 220}, 140)`}>
                                            <rect x="0" y="0" width="360" height="180" rx="24" fill="#3b82f6" stroke="#1e40af" strokeWidth="4" />
                                            <rect x="40" y="40" width="70" height="60" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            <rect x="140" y="40" width="80" height="70" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            <rect x="250" y="40" width="70" height="60" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            <circle cx="80" cy="180" r="30" fill="#0f172a" /><circle cx="280" cy="180" r="30" fill="#0f172a" />
                                            
                                            <line x1="180" y1="50" x2={bobX} y2={bobY} stroke="white" strokeWidth="4" />
                                            <circle cx={bobX} cy={bobY} r="18" fill="white" stroke="#1e293b" strokeWidth="3" />

                                            {showVectors && (
                                                <g transform={`translate(${bobX}, ${bobY})`}>
                                                    <line x1="0" y1="0" x2="0" y2="70" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrow-green)" />
                                                    <line x1="0" y1="0" x2={(180 - bobX)*0.8} y2={(50 - bobY)*0.8} stroke="#3b82f6" strokeWidth="4" markerEnd="url(#arrow-blue)" />
                                                    {view === 'internal' && Math.abs(accel) > 0.1 && (
                                                        <line x1="0" y1="0" x2={-accel * 10} y2="0" stroke="#f43f5e" strokeWidth="4" markerEnd="url(#arrow-red)" />
                                                    )}
                                                </g>
                                            )}
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

# Streamlit 컴포넌트로 HTML 삽입
components.html(react_code, height=900, scrolling=True)
