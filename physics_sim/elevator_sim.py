import streamlit as st
import streamlit.components.v1 as components

# 제목 표시 (스크립트 실행 여부 확인용)
st.title("🛗 엘리베이터 시뮬레이션")

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
        body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background-color: transparent; }
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(224, 231, 255, 0.5); }
    </style>
</head>
<body>
    <div id="root">
        <div style="padding: 40px; text-align: center; color: #64748b;">준비 중...</div>
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
            const [mass, setMass] = useState(60);
            const [view, setView] = useState('external'); 
            const [isMoving, setIsMoving] = useState(false);
            const [history, setHistory] = useState([]);
            
            const posRef = useRef(0);
            const velRef = useRef(0);
            const [renderPos, setRenderPos] = useState(0);

            const g = 9.8;
            const apparentWeight = mass * (g + accel);
            const inertialForce = -mass * accel;

            useEffect(() => {
                let animationId;
                let lastTime = performance.now();

                const animate = (time) => {
                    const dt = Math.min((time - lastTime) / 1000, 0.05);
                    lastTime = time;

                    if (isMoving) {
                        velRef.current += accel * dt;
                        posRef.current -= velRef.current * dt * 25; 
                        if (posRef.current > 120) posRef.current = -120;
                        if (posRef.current < -120) posRef.current = 120;
                        setRenderPos(posRef.current);
                    }
                    animationId = requestAnimationFrame(animate);
                };
                animationId = requestAnimationFrame(animate);
                return () => cancelAnimationFrame(animationId);
            }, [isMoving, accel]);

            return (
                <div className="p-4 max-w-7xl mx-auto space-y-6">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-4 space-y-4">
                            <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-4">
                                <div className="space-y-4">
                                    <div className="flex bg-slate-100 p-1 rounded-2xl text-[10px] font-bold">
                                        <button onClick={() => setView('external')} className={`flex-1 py-1.5 rounded-xl ${view === 'external' ? 'bg-white text-sky-600 shadow-sm' : 'text-slate-500'}`}>외부</button>
                                        <button onClick={() => setView('internal')} className={`flex-1 py-1.5 rounded-xl ${view === 'internal' ? 'bg-white text-sky-600 shadow-sm' : 'text-slate-500'}`}>내부</button>
                                    </div>
                                    <div className="space-y-3">
                                        <div className="flex justify-between text-[10px] font-black text-slate-400 uppercase">가속도 <span className="text-sky-600">{accel.toFixed(1)}</span></div>
                                        <input type="range" min="-9.8" max="10" step="0.2" value={accel} onChange={(e)=>setAccel(parseFloat(e.target.value))} className="w-full" />
                                    </div>
                                    <button onClick={()=>setIsMoving(!isMoving)} className={`w-full py-3 rounded-2xl font-black text-sm ${isMoving ? 'bg-rose-500 text-white' : 'bg-sky-600 text-white shadow-lg shadow-sky-100'}`}>
                                        <Icon name={isMoving ? "pause" : "play"} /> {isMoving ? "정지" : "운동 시작"}
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div className="lg:col-span-8">
                            <div className="bg-white rounded-[40px] shadow-xl border border-slate-100 overflow-hidden h-[450px]">
                                <div className="relative h-full bg-slate-50">
                                    <svg viewBox="0 0 600 450" className="w-full h-full select-none">
                                        <defs>
                                            <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" /></marker>
                                            <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" /></marker>
                                        </defs>
                                        <g transform={`translate(200, ${view === 'external' ? renderPos + 100 : 80})`}>
                                            <rect x="0" y="0" width="200" height="280" rx="12" fill="white" stroke="#64748b" strokeWidth="4" />
                                            <rect x="30" y="240" width="140" height="15" rx="4" fill="#f1f5f9" stroke="#cbd5e1" />
                                            <g transform="translate(100, 240) scale(0.9)">
                                                <circle cx="0" cy="-140" r="20" fill="#334155" />
                                                <rect x="-15" y="-120" width="30" height="60" rx="4" fill="#334155" />
                                                <rect x="-18" y="-60" width="15" height="60" rx="4" fill="#334155" />
                                                <rect x="3" y="-60" width="15" height="60" rx="4" fill="#334155" />
                                            </g>
                                            <g transform="translate(100, 160)">
                                                <line x1="0" y1="0" x2="0" y2="60" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrow-green)" />
                                                <line x1="0" y1="0" x2="0" y2={-apparentWeight/15} stroke="#3b82f6" strokeWidth="4" markerEnd="url(#arrow-blue)" />
                                            </g>
                                        </g>
                                    </svg>
                                    <div className="absolute top-4 right-4 bg-slate-900 border border-white/10 p-4 rounded-2xl text-center shadow-2xl">
                                        <div className="text-[10px] font-black text-slate-400 mb-1 uppercase tracking-widest">Scale Reading</div>
                                        <div className="text-2xl font-black text-white">{apparentWeight.toFixed(1)} <span className="text-xs text-slate-500">N</span></div>
                                    </div>
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
components.html(react_code, height=600, scrolling=True)
