import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    # React 컴포넌트를 위한 HTML/JS 소스
    react_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>가속좌표계 시뮬레이션</title>
        <!-- CDN Loaders -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.5/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { 
                font-family: 'Pretendard', sans-serif; 
                margin: 0; 
                padding: 0; 
                background-color: #f8fafc; 
                min-height: 100vh;
            }
            #root { min-height: 100vh; }
            .glass-card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(226, 232, 240, 1);
            }
        </style>
    </head>
    <body>
        <div id="root">
            <div style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; color: #64748b;">
                시뮬레이션을 불러오는 중입니다...
            </div>
        </div>

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
                            const step = diff * 0.1;
                            return prev + step;
                        });

                        animationId = requestAnimationFrame(animate);
                    };

                    animationId = requestAnimationFrame(animate);
                    return () => cancelAnimationFrame(animationId);
                }, [accel, isMoving, targetTheta]);

                const pivotX = 160; 
                const pivotY = 50;
                const bobX = pivotX - L * Math.sin(currentTheta);
                const bobY = pivotY + L * Math.cos(currentTheta);

                return (
                    <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-8">
                        {/* Header */}
                        <div className="flex items-center gap-4 mb-8">
                            <div className="bg-indigo-600 p-3 rounded-2xl shadow-lg shadow-indigo-200">
                                <Icon name="rocket" size={28} className="text-white" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-black text-slate-900 tracking-tight">가속좌표계와 관성력 실시간 탐구</h1>
                                <p className="text-slate-500 font-medium">일반 상대성 이론 학습: 관찰자의 운동 상태에 따른 물리 현상 분석</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                            {/* Left: Controls */}
                            <div className="lg:col-span-4 space-y-6">
                                <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-6">
                                    <div className="flex items-center gap-2 border-b border-slate-100 pb-4">
                                        <Icon name="settings-2" className="text-indigo-600" />
                                        <h2 className="text-sm font-black text-slate-400 p-2 uppercase tracking-widest">Simulation Setup</h2>
                                    </div>
                                    
                                    <div className="space-y-6">
                                        <div className="space-y-3">
                                            <label className="text-xs font-black text-slate-400 uppercase tracking-tighter">관찰 시점 선택</label>
                                            <div className="flex bg-slate-100 p-1 rounded-2xl">
                                                <button onClick={() => setView('external')} className={`flex-1 py-2.5 rounded-xl text-xs font-bold transition-all ${view === 'external' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-700'}`}>외부 (관성계)</button>
                                                <button onClick={() => setView('internal')} className={`flex-1 py-2.5 rounded-xl text-xs font-bold transition-all ${view === 'internal' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-700'}`}>내부 (비관성계)</button>
                                            </div>
                                        </div>

                                        <div className="space-y-3">
                                            <div className="flex justify-between items-center">
                                                <label className="text-xs font-black text-slate-400 uppercase tracking-tighter">가속도 (a)</label>
                                                <span className="text-sm font-black text-indigo-600 px-2 py-0.5 bg-indigo-50 rounded-lg">{accel.toFixed(1)} m/s²</span>
                                            </div>
                                            <input type="range" min="-10" max="10" step="0.5" value={accel} onChange={(e) => setAccel(parseFloat(e.target.value))} className="w-full" />
                                        </div>

                                        <div className="flex flex-col gap-3">
                                            <button onClick={() => setIsMoving(!isMoving)} className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-3 transition-all ${isMoving ? 'bg-rose-500 text-white shadow-lg shadow-rose-100' : 'bg-indigo-600 text-white shadow-lg shadow-indigo-100'}`}>
                                                <Icon name={isMoving ? "pause-circle" : "play-circle"} />
                                                {isMoving ? "실험 중지" : "운동 시작"}
                                            </button>
                                            <button onClick={() => {posRef.current=0; velRef.current=0; setRenderPos(0); setRenderVel(0);}} className="w-full py-4 rounded-2xl bg-white border border-slate-200 text-slate-600 font-bold text-sm hover:bg-slate-50 flex items-center justify-center gap-2">
                                                <Icon name="rotate-ccw" size={16} /> 초기화
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-4">
                                    <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest pl-2 border-l-4 border-emerald-500">Live Feedback</h3>
                                    <div className="space-y-2">
                                        <div className="bg-emerald-50 p-4 rounded-2xl flex justify-between items-center">
                                            <span className="text-xs font-bold text-emerald-700">기울어진 각도</span>
                                            <span className="text-lg font-black text-emerald-900">{((currentTheta * 180) / Math.PI).toFixed(1)}°</span>
                                        </div>
                                        <div className="bg-slate-50 p-4 rounded-2xl flex justify-between items-center">
                                            <span className="text-xs font-bold text-slate-600">현재 버스 속도</span>
                                            <span className="text-lg font-black text-slate-900">{renderVel.toFixed(1)} m/s</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Right: Simulation */}
                            <div className="lg:col-span-8 flex flex-col gap-6">
                                <div className="bg-white rounded-[40px] shadow-xl border border-slate-100 overflow-hidden relative h-[600px]">
                                    <div className="p-5 bg-slate-900 flex justify-between items-center">
                                        <div className="flex items-center gap-3">
                                            <div className={`w-3 h-3 rounded-full ${isMoving ? 'bg-emerald-400 shadow-lg shadow-emerald-400' : 'bg-slate-600'}`}></div>
                                            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">SYSTEM: {view === 'internal' ? 'Non-Inertial Frame' : 'Inertial Frame'}</span>
                                        </div>
                                        <div className="flex gap-4">
                                            <div className="flex items-center gap-1.5 text-[10px] font-black text-white/60"><div className="w-2 h-2 rounded-full bg-blue-500"></div> 장력</div>
                                            <div className="flex items-center gap-1.5 text-[10px] font-black text-white/60"><div className="w-2 h-2 rounded-full bg-emerald-500"></div> 중력</div>
                                            {view==='internal' && <div className="flex items-center gap-1.5 text-[10px] font-black text-white/60"><div className="w-2 h-2 rounded-full bg-rose-500"></div> 관성력</div>}
                                        </div>
                                    </div>

                                    <div className="relative h-full bg-slate-50">
                                        {/* Road Marks */}
                                        {view === 'external' && (
                                            <div className="absolute bottom-16 w-full h-1 bg-slate-200">
                                                {[...Array(12)].map((_, i) => (
                                                    <div key={i} className="absolute h-12 w-0.5 bg-slate-200" style={{ left: `${(i * 100 + (renderPos % 100 + 100) % 100) % 1000}px` }}></div>
                                                ))}
                                            </div>
                                        )}

                                        <svg viewBox="0 0 800 500" className="w-full h-full select-none">
                                            <defs>
                                                <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" /></marker>
                                                <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" /></marker>
                                                <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" /></marker>
                                            </defs>

                                            <g transform={`translate(${view === 'external' ? renderPos + 100 : 220}, 120)`}>
                                                <rect x="0" y="0" width="360" height="180" rx="32" fill="#3b82f6" stroke="#1e40af" strokeWidth="4" className="shadow-2xl" />
                                                <rect x="30" y="30" width="60" height="60" rx="12" fill="#e0f2fe" opacity="0.8" />
                                                <rect x="130" y="30" width="100" height="80" rx="12" fill="#e0f2fe" opacity="0.8" />
                                                <rect x="270" y="30" width="60" height="60" rx="12" fill="#e0f2fe" opacity="0.8" />
                                                
                                                <circle cx="80" cy="180" r="30" fill="#0f172a" />
                                                <circle cx="280" cy="180" r="30" fill="#0f172a" />
                                                <circle cx="80" cy="180" r="12" fill="#64748b" />
                                                <circle cx="280" cy="180" r="12" fill="#64748b" />

                                                <line x1="180" y1="50" x2={bobX} y2={bobY} stroke="white" strokeWidth="4" strokeLinecap="round" />
                                                <circle cx="180" cy="50" r="6" fill="white" />
                                                <circle cx={bobX} cy={bobY} r="18" fill="white" stroke="#1e293b" strokeWidth="4" />

                                                {showVectors && (
                                                    <g transform={`translate(${bobX}, ${bobY})`}>
                                                        {/* Gravity */}
                                                        <line x1="0" y1="0" x2="0" y2="70" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrow-green)" />
                                                        <text x="8" y="85" className="vector-label fill-emerald-600 font-black italic">mg</text>
                                                        {/* Tension */}
                                                        <line x1="0" y1="0" x2={(180 - bobX)*0.8} y2={(50 - bobY)*0.8} stroke="#3b82f6" strokeWidth="4" markerEnd="url(#arrow-blue)" />
                                                        <text x={(180 - bobX)*1} y={(50 - bobY)*1 - 5} className="vector-label fill-blue-600 font-black italic">T</text>
                                                        {/* Inertial */}
                                                        {view === 'internal' && Math.abs(accel) > 0.1 && (
                                                            <g>
                                                                <line x1="0" y1="0" x2={-accel * 10} y2="0" stroke="#f43f5e" strokeWidth="4" markerEnd="url(#arrow-red)" />
                                                                <text x={-accel * 13} y="-10" textAnchor="middle" className="vector-label fill-rose-600 font-black italic">-ma</text>
                                                            </g>
                                                        )}
                                                    </g>
                                                )}
                                            </g>

                                            {view === 'external' && (
                                                <g transform="translate(60, 320)">
                                                    <circle cx="0" cy="-20" r="10" fill="#475569" />
                                                    <line x1="0" y1="-10" x2="0" y2="20" stroke="#475569" strokeWidth="3" />
                                                    <text x="0" y="50" textAnchor="middle" className="text-[10px] font-black fill-slate-400">외부인</text>
                                                </g>
                                            )}
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Analysis Questions */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pb-32">
                            <div className="glass-card p-8 rounded-[40px] space-y-6">
                                <h3 className="text-xl font-black text-slate-900 flex items-center gap-3">
                                    <Icon name="help-circle" className="text-indigo-600" />
                                    관찰자 시점 탐구
                                </h3>
                                <div className="space-y-4">
                                    <div className="p-5 bg-slate-50 rounded-3xl">
                                        <p className="font-bold text-slate-800 leading-relaxed mb-2">1. 외부 관찰자 시점</p>
                                        <p className="text-sm text-slate-500 leading-relaxed italic">버스가 가속될 때, 진자가 뒤로 처지면서 버스와 같은 가속도로 운동하는 이유는 장력의 수평 성분이 알짜힘으로 작용하기 때문입니다.</p>
                                    </div>
                                    <div className="p-5 bg-slate-50 rounded-3xl">
                                        <p className="font-bold text-slate-800 leading-relaxed mb-2">2. 내부 관찰자 시점</p>
                                        <p className="text-sm text-slate-500 leading-relaxed italic">가속되는 버스 안에서 진자가 정지해 보이는 이유는, 버스의 가속과 반대 방향으로 작용하는 **관성력**이 장력 및 중력과 평형을 이루기 때문입니다.</p>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-slate-900 p-8 rounded-[40px] text-white space-y-6 shadow-2xl">
                                <h3 className="text-xl font-black flex items-center gap-3">
                                    <Icon name="activity" className="text-emerald-400" />
                                    핵심 물리 개념
                                </h3>
                                <div className="space-y-4">
                                    <div className="p-6 bg-white/5 rounded-3xl border border-white/10">
                                        <div className="flex justify-between items-center mb-4">
                                            <span className="text-xs font-black text-rose-400 uppercase tracking-widest">Inertial Force</span>
                                            <span className="text-lg font-black text-white">$F_{inertial} = -ma$</span>
                                        </div>
                                        <p className="text-sm text-slate-400 leading-relaxed">
                                            관성력은 가속 좌표계에서만 나타나는 **가상의 힘(Apparent Force)**으로, 관찰자가 가속되는 좌표계에 속해 있기 때문에 느끼게 됩니다.
                                        </p>
                                    </div>
                                    <div className="p-6 bg-emerald-500/10 rounded-3xl border border-emerald-500/20">
                                        <p className="text-sm text-emerald-100 italic leading-relaxed font-bold">
                                            "관성력의 존재 덕분에 가속 좌표계 안에서도 뉴턴의 제2법칙($F=ma$)이 성립하는 것처럼 기술할 수 있게 됩니다."
                                        </p>
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
    components.html(react_code, height=1300, scrolling=True)

if __name__ == "__main__":
    run_sim()
