import streamlit as st
import streamlit.components.v1 as components

# 페이지 제목
st.title("🛗 엘리베이터 시뮬레이션: 관성력 탐구")

# React 컴포넌트
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

            const g = 9.8;
            const m = 60;
            const apparentWeight = m * (g + accel);
            const inertialForce = -m * accel;

            useEffect(() => {
                let animationId;
                let lastTime = performance.now();

                const animate = (time) => {
                    const dt = Math.min((time - lastTime) / 1000, 0.05);
                    lastTime = time;

                    if (isMoving) {
                        velRef.current += accel * dt;
                        posRef.current -= velRef.current * dt * 50; 
                        setRenderPos(posRef.current);
                    }
                    animationId = requestAnimationFrame(animate);
                };
                animationId = requestAnimationFrame(animate);
                return () => cancelAnimationFrame(animationId);
            }, [isMoving, accel]);

            // Background Shaft Lines
            // If internal: elevator y is fixed, shaft lines move at -y
            // If external: elevator y moves, shaft lines are fixed
            const shaftOffset = view === 'internal' ? (renderPos % 200) : 0;
            const elevatorY = view === 'internal' ? 80 : (100 + (renderPos % 400 + 400) % 400 - 100);

            return (
                <div className="p-4 max-w-7xl mx-auto space-y-4">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-4 space-y-4">
                            <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-6 text-center">
                                <div className="space-y-4">
                                    <div className="flex bg-slate-100 p-1 rounded-2xl text-[11px] font-bold">
                                        <button onClick={() => setView('external')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'external' ? 'bg-white text-sky-600 shadow-sm' : 'text-slate-500'}`}>외부에서 보기</button>
                                        <button onClick={() => setView('internal')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'internal' ? 'bg-white text-sky-600 shadow-sm' : 'text-slate-500'}`}>내부에서 보기</button>
                                    </div>
                                    <div className="p-4 bg-slate-50 rounded-2xl">
                                        <div className="flex justify-between text-[10px] font-black text-slate-400 mb-2">가속도 (m/s²) <span className="text-sky-600">{accel.toFixed(1)}</span></div>
                                        <input type="range" min="-9.8" max="10" step="0.2" value={accel} onChange={(e)=>setAccel(parseFloat(e.target.value))} className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-sky-600" />
                                    </div>
                                    <button onClick={()=>setIsMoving(!isMoving)} className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-2 ${isMoving ? 'bg-rose-500 text-white' : 'bg-sky-600 text-white shadow-lg'}`}>
                                        <Icon name={isMoving ? "pause" : "play"} /> {isMoving ? "운동 멈춤" : "운동 시뮬레이션 시작"}
                                    </button>
                                </div>
                            </div>

                            <div className="bg-slate-900 p-6 rounded-[32px] text-center shadow-xl">
                                <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">저울 눈금 (N)</div>
                                <div className={`text-4xl font-black ${Math.abs(accel) < 0.1 ? 'text-white' : (accel > 0 ? 'text-emerald-400' : 'text-rose-400')}`}>
                                    {apparentWeight.toFixed(1)}
                                </div>
                            </div>
                        </div>

                        <div className="lg:col-span-8">
                            <div className="bg-white rounded-[40px] shadow-xl border border-slate-100 overflow-hidden relative h-[500px]">
                                <div className="p-4 bg-slate-900 flex justify-between text-white/50 text-[10px] font-black uppercase tracking-widest">
                                    <span>{view === 'internal' ? 'Non-Inertial Frame (Moving Wall)' : 'Inertial Frame (Moving Box)'}</span>
                                </div>
                                <div className="relative h-full bg-slate-50 overflow-hidden">
                                    <svg viewBox="0 0 600 450" className="w-full h-full select-none">
                                        <defs>
                                            <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" /></marker>
                                            <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" /></marker>
                                            <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" /></marker>
                                        </defs>

                                        {/* Shaft Lines */}
                                        <g transform={`translate(0, ${shaftOffset})`}>
                                            {[...Array(10)].map((_, i) => (
                                                <line key={i} x1="180" y1={i * 100 - 200} x2="160" y2={i * 100 - 200} stroke="#cbd5e1" strokeWidth="2" />
                                            ))}
                                            {[...Array(10)].map((_, i) => (
                                                <line key={i} x1="420" y1={i * 100 - 200} x2="440" y2={i * 100 - 200} stroke="#cbd5e1" strokeWidth="2" />
                                            ))}
                                        </g>
                                        <line x1="180" y1="0" x2="180" y2="450" stroke="#e2e8f0" strokeWidth="1" />
                                        <line x1="420" y1="0" x2="420" y2="450" stroke="#e2e8f0" strokeWidth="1" />

                                        <g transform={`translate(200, ${elevatorY})`}>
                                            <rect x="0" y="0" width="200" height="280" rx="16" fill="white" stroke="#94a3b8" strokeWidth="4" />
                                            <rect x="30" y="240" width="140" height="15" rx="4" fill="#f1f5f9" stroke="#cbd5e1" />
                                            <g transform="translate(100, 240) scale(0.9)">
                                                <circle cx="0" cy="-140" r="20" fill="#334155" />
                                                <path d="M -15 -120 Q 0 -125 15 -120 L 22 -60 L -22 -60 Z" fill="#334155" />
                                                <rect x="-20" y="-60" width="15" height="60" rx="4" fill="#334155" />
                                                <rect x="5" y="-60" width="15" height="60" rx="4" fill="#334155" />
                                            </g>

                                            <g transform="translate(100, 160)">
                                                <line x1="0" y1="0" x2="0" y2="70" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrow-green)" />
                                                <line x1="0" y1="0" x2="0" y2={-apparentWeight/15} stroke="#3b82f6" strokeWidth="4" markerEnd="url(#arrow-blue)" />
                                                {view === 'internal' && Math.abs(accel) > 0.1 && (
                                                    <line x1="0" y1="0" x2="0" y2={inertialForce/15} stroke="#f43f5e" strokeWidth="3" markerEnd="url(#arrow-red)" />
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

# 질문 섹션 (이전 컨셉 유지)
st.divider()
st.subheader("🔍 시점별 물리 현상 탐구")
col1, col2 = st.columns(2)
with col1:
    st.info("### 🌎 외부 시점 (관성계)")
    st.write("엘리베이터가 위로 가속될 때 사람도 함께 가속됩니다. 저울이 사람을 밀어주는 힘(수직항력)이 중력보다 커야 하므로 측정값이 늘어납니다.")
with col2:
    st.success("### 🚠 내부 시점 (비관성계)")
    st.write("내부에서는 자신이 가속되고 있다는 것을 주변 환경(엘리베이터 벽)과의 상대적인 정지 상태로 느끼기 어렵습니다. 대신 **바깥 환경(층수 표시 등)이 반대로 움직이는 것**으로 이 운동을 시각화합니다.")
