import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    # 상단 브랜딩 및 제목
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; shadow: 0 4px 12px rgba(99, 102, 241, 0.3);">
                🚀
            </div>
            <div>
                <h1 style="margin: 0; font-size: 28px; font-weight: 800; color: #1e293b; letter-spacing: -0.5px;">가속좌표계와 관성력 실시간 탐구</h1>
                <p style="margin: 0; color: #64748b; font-size: 14px; font-weight: 500;">일반 상대성 이론의 기초: 가속되는 버스 안에서의 물리 현상</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

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
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; overflow: hidden; }
            .glass { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.3); }
            .bus-body { fill: #3b82f6; stroke: #1e40af; stroke-width: 4; }
            .bus-window { fill: #e0f2fe; stroke: #1e40af; stroke-width: 2; }
            .vector-label { font-weight: 800; font-style: italic; font-size: 14px; }
            .control-card { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
            .control-card:hover { transform: translateY(-2px); shadow: 0 12px 24px -10px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const InertialForceSim = () => {
                const [accel, setAccel] = useState(0); // m/s^2
                const [view, setView] = useState('external'); // 'external' or 'internal'
                const [showVectors, setShowVectors] = useState(true);
                const [isMoving, setIsMoving] = useState(false);
                const [busPos, setBusPos] = useState(0);
                const [busVelocity, setBusVelocity] = useState(0);
                
                const g = 9.8; // Gravity
                const L = 120; // Length of pendulum string
                const mass = 1; // kg
                
                // Pendulum angle (theta) from vertical
                // In equilibrium in non-inertial frame: tan(theta) = a/g
                const targetTheta = Math.atan(accel / g);
                const [currentTheta, setCurrentTheta] = useState(0);

                // Animation loop
                useEffect(() => {
                    let animationId;
                    let lastTime = performance.now();

                    const animate = (time) => {
                        const dt = (time - lastTime) / 1000;
                        lastTime = time;

                        if (isMoving) {
                            setBusVelocity(v => v + accel * dt);
                            setBusPos(p => {
                                let newP = p + busVelocity * dt * 20; // Scale position
                                if (newP > 600) return -200; // Reset if out of bounds
                                if (newP < -200) return 600;
                                return newP;
                            });
                        }

                        // Smoothly adjust pendulum angle towards target
                        setCurrentTheta(prev => {
                            const diff = targetTheta - prev;
                            return prev + diff * 0.1;
                        });

                        animationId = requestAnimationFrame(animate);
                    };

                    animationId = requestAnimationFrame(animate);
                    return () => cancelAnimationFrame(animationId);
                }, [accel, isMoving, busVelocity, targetTheta]);

                const reset = () => {
                    setBusPos(0);
                    setBusVelocity(0);
                    setIsMoving(false);
                    setAccel(0);
                };

                // Coordinates
                const busWidth = 300;
                const busHeight = 160;
                const pivotX = 150; // Relative to bus center
                const pivotY = 50;

                // Pendulum bob position
                const bobX = pivotX - L * Math.sin(currentTheta);
                const bobY = pivotY + L * Math.cos(currentTheta);

                return (
                    <div className="flex flex-col items-center p-4 bg-slate-50 min-h-screen">
                        <div className="w-full max-w-6xl flex flex-col lg:flex-row gap-6">
                            
                            {/* Control Panel */}
                            <div className="w-full lg:w-80 space-y-4">
                                <div className="glass p-6 rounded-[24px] shadow-sm space-y-6 control-card">
                                    <div className="space-y-4">
                                        <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                            <Icon name="settings" className="text-indigo-600" /> 가상실험 설정
                                        </h3>
                                        
                                        <div className="space-y-4">
                                            <div className="p-4 bg-white rounded-2xl border border-slate-100 shadow-sm">
                                                <label className="block text-xs font-bold text-slate-500 mb-2">관찰자 시점 선택</label>
                                                <div className="grid grid-cols-2 gap-2">
                                                    <button 
                                                        onClick={() => setView('internal')}
                                                        className={`py-2 px-1 rounded-xl text-[11px] font-black transition-all ${view === 'internal' ? 'bg-indigo-600 text-white shadow-md' : 'bg-slate-50 text-slate-400 hover:bg-slate-100'}`}
                                                    >
                                                        버스 내부 (비관성계)
                                                    </button>
                                                    <button 
                                                        onClick={() => setView('external')}
                                                        className={`py-2 px-1 rounded-xl text-[11px] font-black transition-all ${view === 'external' ? 'bg-indigo-600 text-white shadow-md' : 'bg-slate-50 text-slate-400 hover:bg-slate-100'}`}
                                                    >
                                                        버스 외부 (관성계)
                                                    </button>
                                                </div>
                                            </div>

                                            <div className="p-4 bg-white rounded-2xl border border-slate-100 shadow-sm">
                                                <div className="flex justify-between items-center mb-2">
                                                    <label className="text-xs font-bold text-slate-500">버스 가속도 (a)</label>
                                                    <span className="text-sm font-black text-indigo-600">{accel.toFixed(1)} m/s²</span>
                                                </div>
                                                <input 
                                                    type="range" min="-10" max="10" step="0.5" value={accel} 
                                                    onChange={(e) => setAccel(parseFloat(e.target.value))}
                                                    className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                                />
                                                <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                                                    <span>급브레이크</span>
                                                    <span>정속</span>
                                                    <span>급가속</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex flex-col gap-2 pt-2">
                                            <button 
                                                onClick={() => setIsMoving(!isMoving)}
                                                className={`w-full py-3 rounded-2xl font-black text-sm flex items-center justify-center gap-2 transition-all ${isMoving ? 'bg-rose-500 text-white shadow-lg shadow-rose-200' : 'bg-indigo-600 text-white shadow-lg shadow-indigo-200'}`}
                                            >
                                                <Icon name={isMoving ? "pause" : "play"} />
                                                {isMoving ? "실험 일시정지" : "실험 시작"}
                                            </button>
                                            <button 
                                                onClick={reset}
                                                className="w-full py-3 rounded-2xl bg-white border border-slate-200 text-slate-600 font-black text-sm hover:bg-slate-50 transition-all flex items-center justify-center gap-2"
                                            >
                                                <Icon name="refresh-ccw" /> 초기화
                                            </button>
                                            <button 
                                                onClick={() => setShowVectors(!showVectors)}
                                                className={`w-full py-3 rounded-2xl font-black text-sm flex items-center justify-center gap-2 transition-all ${showVectors ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-400'}`}
                                            >
                                                <Icon name={showVectors ? "eye" : "eye-off"} />
                                                {showVectors ? "힘의 벡터 숨기기" : "힘의 벡터 보기"}
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <div className="glass p-5 rounded-[24px] shadow-sm space-y-3">
                                    <h4 className="text-[11px] font-black text-slate-400 uppercase tracking-widest pl-1 border-l-4 border-indigo-500">물리 분석 정보</h4>
                                    <div className="space-y-2">
                                        <div className="p-3 bg-indigo-50/50 rounded-xl border border-indigo-100 flex justify-between items-center">
                                            <span className="text-[11px] font-bold text-indigo-700">기울어진 각도</span>
                                            <span className="text-sm font-black text-indigo-900">{((currentTheta * 180) / Math.PI).toFixed(1)}°</span>
                                        </div>
                                        <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100 flex justify-between items-center">
                                            <span className="text-[11px] font-bold text-emerald-700">버스 속도</span>
                                            <span className="text-sm font-black text-emerald-900">{busVelocity.toFixed(1)} m/s</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Simulation Canvas */}
                            <div className="flex-1 bg-white rounded-[32px] shadow-xl border border-slate-100 overflow-hidden relative flex flex-col">
                                <div className="p-4 bg-slate-900 flex justify-between items-center text-white">
                                    <div className="flex items-center gap-3">
                                        <div className={`w-3 h-3 rounded-full ${isMoving ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'}`}></div>
                                        <span className="text-xs font-black uppercase tracking-tight">Perspective: {view === 'internal' ? 'Non-Inertial Frame (Inside)' : 'Inertial Frame (Outside)'}</span>
                                    </div>
                                    <div className="flex gap-4 text-[10px] font-bold">
                                        <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500"></span> 장력 (T)</div>
                                        <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500"></span> 중력 (mg)</div>
                                        {view === 'internal' && <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-rose-500"></span> 관성력 (-ma)</div>}
                                    </div>
                                </div>

                                <div className="flex-1 min-h-[500px] relative bg-slate-50 overflow-hidden">
                                    {/* Road lines */}
                                    {view === 'external' && (
                                        <div className="absolute bottom-10 w-full h-[2px] bg-slate-200">
                                            {[...Array(20)].map((_, i) => (
                                                <div key={i} className="absolute h-10 w-[2px] bg-slate-200" style={{ left: `${(i * 100 + (busPos % 100)) % 1000}px` }}></div>
                                            ))}
                                        </div>
                                    )}

                                    <svg viewBox="0 0 800 500" className="w-full h-full select-none">
                                        <defs>
                                            <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                                                <path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" />
                                            </marker>
                                            <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                                                <path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" />
                                            </marker>
                                            <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                                                <path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" />
                                            </marker>
                                            <linearGradient id="busGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                                                <stop offset="0%" stopColor="#3b82f6" />
                                                <stop offset="100%" stopColor="#1e40af" />
                                            </linearGradient>
                                        </defs>

                                        {/* Bus Rendering */}
                                        <g transform={`translate(${view === 'external' ? busPos + 100 : 250}, 150)`}>
                                            {/* Bus Body */}
                                            <rect x="0" y="0" width={busWidth} height={busHeight} rx="20" fill="url(#busGrad)" stroke="#1e3a8a" strokeWidth="2" className="shadow-lg" />
                                            
                                            {/* Windows */}
                                            <rect x="20" y="20" width="60" height="50" rx="8" className="bus-window" />
                                            <rect x="100" y="20" width="100" height="70" rx="8" className="bus-window" />
                                            <rect x="220" y="20" width="60" height="50" rx="8" className="bus-window" />
                                            
                                            {/* Wheels */}
                                            <circle cx="60" cy={busHeight} r="25" fill="#1e293b" />
                                            <circle cx="240" cy={busHeight} r="25" fill="#1e293b" />
                                            <circle cx="60" cy={busHeight} r="10" fill="#64748b" />
                                            <circle cx="240" cy={busHeight} r="10" fill="#64748b" />

                                            {/* Pendulum */}
                                            <line x1={pivotX} y1={pivotY} x2={bobX} y2={bobY} stroke="#f1f5f9" strokeWidth="3" />
                                            <circle cx={pivotX} cy={pivotY} r="4" fill="#f1f5f9" />
                                            <circle cx={bobX} cy={bobY} r="15" fill="#f8fafc" stroke="#334155" strokeWidth="3" className="shadow-md" />

                                            {/* Vectors */}
                                            {showVectors && (
                                                <g transform={`translate(${bobX}, ${bobY})`}>
                                                    {/* Gravity (mg) - Green */}
                                                    <line x1="0" y1="0" x2="0" y2="60" stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                                    <text x="5" y="75" className="vector-label fill-emerald-600">mg</text>

                                                    {/* Tension (T) - Blue */}
                                                    <line x1="0" y1="0" x2={(pivotX - bobX) * 0.7} y2={(pivotY - bobY) * 0.7} stroke="#3b82f6" strokeWidth="3" markerEnd="url(#arrow-blue)" />
                                                    <text x={(pivotX - bobX) * 0.8} y={(pivotY - bobY) * 0.8} className="vector-label fill-blue-600">T</text>

                                                    {/* Inertial Force (-ma) - Red (Shown only in Internal View) */}
                                                    {view === 'internal' && Math.abs(accel) > 0.1 && (
                                                        <g>
                                                            <line x1="0" y1="0" x2={-accel * 8} y2="0" stroke="#f43f5e" strokeWidth="3" markerEnd="url(#arrow-red)" />
                                                            <text x={-accel * 10} y="-10" textAnchor="middle" className="vector-label fill-rose-600">-ma</text>
                                                        </g>
                                                    )}
                                                </g>
                                            )}
                                        </g>

                                        {/* External Observer (Only in external view) */}
                                        {view === 'external' && (
                                            <g transform="translate(50, 310)">
                                                <circle cx="0" cy="-20" r="10" fill="#475569" />
                                                <line x1="0" y1="-10" x2="0" y2="20" stroke="#475569" strokeWidth="3" />
                                                <line x1="0" y1="0" x2="-10" y2="10" stroke="#475569" strokeWidth="3" />
                                                <line x1="0" y1="0" x2="10" y2="10" stroke="#475569" strokeWidth="3" />
                                                <line x1="0" y1="20" x2="-10" y2="40" stroke="#475569" strokeWidth="3" />
                                                <line x1="0" y1="20" x2="10" y2="40" stroke="#475569" strokeWidth="3" />
                                                <text x="0" y="60" textAnchor="middle" className="text-[10px] font-bold fill-slate-500">외부 관찰자</text>
                                            </g>
                                        )}
                                    </svg>

                                    {/* Overlay Labels */}
                                    <div className="absolute top-4 right-4 flex flex-col items-end gap-2">
                                        <div className="px-3 py-1 bg-slate-900 border border-slate-700 rounded-full text-[10px] font-black text-white">
                                            {view === 'internal' ? '내부 관찰자: 물체는 정지해 보임' : '외부 관찰자: 물체는 버스와 함께 가속됨'}
                                        </div>
                                        {Math.abs(accel) > 0 && (
                                          <div className="px-3 py-1 bg-indigo-600 rounded-full text-[10px] font-black text-white shadow-lg">
                                            가속도: {accel > 0 ? '→' : '←'} {Math.abs(accel)} m/s²
                                          </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Inquiry Questions */}
                        <div className="w-full max-w-6xl mt-8 grid grid-cols-1 md:grid-cols-2 gap-6 pb-20">
                            <div className="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm space-y-4">
                                <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                                    <Icon name="search" className="text-indigo-600" />
                                    관찰 시점의 차이 탐구
                                </h3>
                                <div className="space-y-3">
                                    <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                                        <p className="text-xs font-black text-slate-400 mb-1 uppercase tracking-tighter italic">Question 1</p>
                                        <p className="text-[14px] font-bold text-slate-700 leading-relaxed">
                                            **버스 외부**의 관찰자가 볼 때, 손잡이가 비스듬히 기울어진 상태로 가속되는 원인은 무엇입니까?
                                        </p>
                                        <p className="text-[12px] text-slate-500 mt-2">
                                            (힌트: 장력의 수평 성분이 알짜힘이 되어 손잡이를 가속시킵니다.)
                                        </p>
                                    </div>
                                    <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                                        <p className="text-xs font-black text-slate-400 mb-1 uppercase tracking-tighter italic">Question 2</p>
                                        <p className="text-[14px] font-bold text-slate-700 leading-relaxed">
                                            **버스 내부**의 관찰자가 볼 때, 손잡이가 기울어진 채 정지해 있는 이유는 무엇입니까?
                                        </p>
                                        <p className="text-[12px] text-slate-500 mt-2">
                                          (힌트: 실제로 존재하지 않지만 가속 좌표계에서 도입되는 **관성력**이 장력, 중력과 평형을 이룹니다.)
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm space-y-4">
                                <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                                    <Icon name="info" className="text-emerald-600" />
                                    물리 개념 핵심 요약
                                </h3>
                                <div className="space-y-4">
                                    <div className="flex gap-4">
                                        <div className="w-10 h-10 rounded-full bg-amber-500 text-white flex items-center justify-center shrink-0 font-black">!</div>
                                        <div>
                                            <p className="font-black text-slate-800 text-sm">관성력 (Inertial Force)</p>
                                            <p className="text-[12px] text-slate-500 leading-relaxed">가속되는 좌표계 안에서 관찰되는 가상의 힘으로, 좌표계의 가속도와 반대 방향으로 작용합니다. ($F_{inertial} = -ma$)</p>
                                        </div>
                                    </div>
                                    <div className="flex gap-4">
                                        <div className="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center shrink-0 font-black">?</div>
                                        <div>
                                            <p className="font-black text-slate-800 text-sm">등가 원리 (Equivalence Principle)</p>
                                            <p className="text-[12px] text-slate-500 leading-relaxed">아인슈타인은 가속도에 의한 관성력과 중력을 구별할 수 없다는 점에서 일반 상대성 이론을 이끌어냈습니다.</p>
                                        </div>
                                    </div>
                                    <div className="p-4 bg-slate-900 rounded-2xl border border-slate-800">
                                        <p className="text-rose-400 font-bold text-xs uppercase mb-2 tracking-widest">Physics Focus</p>
                                        <p className="text-white font-black text-sm italic">"관성력은 실제 힘이 아니라, 관찰자가 가속되고 있기 때문에 나타나는 겉보기 힘(Apparent Force)입니다."</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<InertialForceSim />);
        </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트로 HTML 삽입
    components.html(react_code, height=950, scrolling=True)

if __name__ == "__main__":
    run_sim()
