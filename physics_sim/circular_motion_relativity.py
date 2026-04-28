import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.title("🎡 회전 원판 시뮬레이션: 원심력과 관성력")

# React 컴포넌트 코드
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
            const [omega, setOmega] = useState(2); // rad/s
            const [view, setView] = useState('external'); 
            const [isRunning, setIsRunning] = useState(false);
            const [showForces, setShowForces] = useState(true);
            
            const angleRef = useRef(0);
            const [renderAngle, setRenderAngle] = useState(0);

            const r = 100; // Radius in px
            const m = 1; // Mass
            const centripetalForce = m * r * omega * omega / 500; // Simplified for visual
            const springReading = (omega * omega * 2).toFixed(1);

            useEffect(() => {
                let animationId;
                let lastTime = performance.now();

                const animate = (time) => {
                    const dt = Math.min((time - lastTime) / 1000, 0.05);
                    lastTime = time;

                    if (isRunning) {
                        angleRef.current += omega * dt;
                        setRenderAngle(angleRef.current);
                    }
                    animationId = requestAnimationFrame(animate);
                };
                animationId = requestAnimationFrame(animate);
                return () => cancelAnimationFrame(animationId);
            }, [isRunning, omega]);

            // External: Disk at angle, observer fixed.
            // Internal: Disk at 0 (fixed), Background/Stars rotate at -angle, observer on disk.
            const diskRotation = view === 'external' ? (renderAngle * 180 / Math.PI) : 0;
            const backgroundRotation = view === 'internal' ? (-renderAngle * 180 / Math.PI) : 0;

            return (
                <div className="p-4 max-w-full mx-auto space-y-4">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-3 space-y-4">
                            <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-6">
                                <div className="space-y-4 text-center">
                                    <div className="flex bg-slate-100 p-1 rounded-2xl text-[11px] font-bold">
                                        <button onClick={() => setView('external')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'external' ? 'bg-white text-emerald-600 shadow-sm' : 'text-slate-500'}`}>외부 (관성계)</button>
                                        <button onClick={() => setView('internal')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'internal' ? 'bg-white text-emerald-600 shadow-sm' : 'text-slate-500'}`}>내부 (비관성계)</button>
                                    </div>

                                    <div className="p-4 bg-slate-50 rounded-2xl">
                                        <div className="flex justify-between text-[10px] font-black text-slate-400 mb-2 uppercase tracking-widest">각속도 ω <span className="text-emerald-600">{(omega).toFixed(1)} rad/s</span></div>
                                        <input type="range" min="0" max="10" step="0.5" value={omega} onChange={(e)=>setOmega(parseFloat(e.target.value))} className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600" />
                                    </div>
                                    
                                    <div className="flex items-center gap-2 text-xs font-bold text-slate-600">
                                        <input type="checkbox" id="forces" checked={showForces} onChange={(e)=>setShowForces(e.target.checked)} className="w-4 h-4 accent-emerald-600" />
                                        <label htmlFor="forces">힘 벡터 표시</label>
                                    </div>

                                    <button onClick={()=>setIsRunning(!isRunning)} className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-2 ${isRunning ? 'bg-rose-500 text-white' : 'bg-emerald-600 text-white shadow-lg'}`}>
                                        <Icon name={isRunning ? "pause" : "play"} /> {isRunning ? "정지" : "시작"}
                                    </button>
                                </div>
                            </div>

                            <div className="bg-slate-900 p-6 rounded-[32px] text-center shadow-xl border-t-4 border-emerald-400">
                                <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">용수철 저울 눈금 (F)</div>
                                <div className="text-4xl font-black text-white">
                                    {springReading} <span className="text-lg text-emerald-400">N</span>
                                </div>
                                <div className="text-[10px] text-slate-500 mt-2 font-bold">(탄성력 = m r ω²)</div>
                            </div>
                        </div>

                        <div className="lg:col-span-9">
                            <div className="bg-slate-100 rounded-[40px] shadow-2xl border border-slate-200 overflow-hidden relative h-[500px]">
                                <div className="p-4 bg-slate-900 flex justify-between text-white/50 text-[10px] font-black uppercase tracking-widest">
                                    <span>{view === 'internal' ? '원판 위의 관찰자 (회전 좌표계)' : '원판 밖의 관찰자 (관성 좌표계)'}</span>
                                    <div className="flex gap-4">
                                        <span className="text-emerald-500">● 탄성력 (F)</span>
                                        {view==='internal' && <span className="text-rose-400">● 원심력 (Fc)</span>}
                                    </div>
                                </div>
                                <div className="relative h-full overflow-hidden bg-[radial-gradient(circle_at_center,_#eff6ff_0%,_#dbeafe_100%)]">
                                    {/* Stars/Background for internal view rotation */}
                                    <div className="absolute inset-0 pointer-events-none" style={{ transform: `rotate(${backgroundRotation}deg)` }}>
                                        {[...Array(40)].map((_, i) => (
                                            <div key={i} className="absolute w-1 h-1 bg-slate-300 rounded-full" style={{ left: `${Math.random()*100}%`, top: `${Math.random()*100}%` }}></div>
                                        ))}
                                        <div className="absolute inset-0 border-[40px] border-slate-200/20 rounded-full scale-110"></div>
                                    </div>

                                    <svg viewBox="0 0 600 450" className="w-full h-full select-none relative z-10">
                                        <defs>
                                            <marker id="arrow-emerald" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" /></marker>
                                            <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" /></marker>
                                        </defs>

                                        {/* Disk Container */}
                                        <g transform={`translate(300, 225) rotate(${diskRotation})`}>
                                            <circle cx="0" cy="0" r="150" fill="white" stroke="#94a3b8" strokeWidth="8" shadow="0 10px 20px rgba(0,0,0,0.1)" />
                                            <circle cx="0" cy="0" r="10" fill="#334155" />
                                            
                                            {/* Spring Scale */}
                                            <line x1="0" y1="0" x2={r} y2="0" stroke="#cbd5e1" strokeWidth="6" strokeDasharray="4 2" />
                                            <rect x="20" y="-12" width="60" height="24" rx="4" fill="#f8fafc" stroke="#94a3b8" strokeWidth="2" />
                                            <text x="50" y="4" textAnchor="middle" className="text-[10px] font-black fill-slate-500">용수철 저울</text>

                                            {/* Mass m */}
                                            <circle cx={r} cy="0" r="15" fill="#1e293b" />
                                            <text x={r} y="-20" textAnchor="middle" className="text-[12px] font-black fill-slate-800 italic">m</text>

                                            {showForces && (
                                                <g transform={`translate(${r}, 0)`}>
                                                    {/* Centripetal Force (Elastic) */}
                                                    <line x1="0" y1="0" x2="-60" y2="0" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrow-emerald)" />
                                                    <text x="-40" y="-10" textAnchor="middle" className="text-[10px] font-bold fill-emerald-600">F (탄성력)</text>
                                                    
                                                    {/* Centrifugal Force (only in internal) */}
                                                    {view === 'internal' && omega > 0.1 && (
                                                        <>
                                                            <line x1="0" y1="0" x2="60" y2="0" stroke="#f43f5e" strokeWidth="4" markerEnd="url(#arrow-red)" />
                                                            <text x="40" y="-10" textAnchor="middle" className="text-[10px] font-bold fill-rose-600">Fc (원심력)</text>
                                                        </>
                                                    )}
                                                </g>
                                            )}

                                            {/* Observer on disk (only if internal) */}
                                            {view === 'internal' && (
                                                <g transform="translate(0, -60) scale(0.6)">
                                                    <circle cx="0" cy="-30" r="15" fill="#0284c7" />
                                                    <path d="M -10 -15 L 10 -15 L 15 20 L -15 20 Z" fill="#0284c7" />
                                                </g>
                                            )}
                                        </g>

                                        {/* External Observer (only if external) */}
                                        {view === 'external' && (
                                            <g transform="translate(500, 150) scale(0.8)">
                                                <circle cx="0" cy="-30" r="15" fill="#475569" />
                                                <path d="M -10 -15 L 10 -15 L 15 40 L -15 40 Z" fill="#475569" />
                                            </g>
                                        )}
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
components.html(react_code, height=540, scrolling=False)

# 탐구 표 구성
st.markdown("### 🔍 회전하는 원판에서의 운동 분석")

# 스타일링된 HTML 테이블 (각 셀마다 정답 확인 버튼 적용)
st.markdown("""
<style>
    .physics-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-family: 'Pretendard', sans-serif;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .physics-table th {
        background-color: #0f172a;
        color: white;
        padding: 15px;
        text-align: center;
        font-weight: 800;
        font-size: 14px;
        border: 1px solid #1e293b;
    }
    .physics-table td {
        padding: 15px;
        border: 1px solid #e2e8f0;
        vertical-align: middle;
        font-size: 14px;
        text-align: center;
    }
    .label-cell { 
        background-color: #f1f5f9; 
        font-weight: 700; 
        text-align: center; 
        width: 20%;
        color: #475569;
    }
    .force-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        margin: 2px;
    }
    .tag-emerald { background: #d1fae5; color: #065f46; }
    .tag-rose { background: #ffe4e6; color: #9f1239; }
    
    summary {
        cursor: pointer;
        list-style: none;
        background-color: #10b981;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 800;
        display: inline-block;
        color: white;
        transition: all 0.2s;
    }
    summary:hover { background-color: #059669; transform: translateY(-1px); }
    details[open] summary { display: none; }
    .answer-content { animation: fadeIn 0.3s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
</style>

<table class="physics-table">
    <thead>
        <tr>
            <th>구분</th>
            <th>🌍 지면에 정지한 관찰자 (외부)</th>
            <th>🙆 회전 원판 위의 관찰자 (내부)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="label-cell">추의 운동 상태</td>
            <td>
                <details>
                    <summary>정답 확인</summary>
                    <div class="answer-content">일정한 속력으로 원을 그리는 <b>등속 원운동</b>을 함</div>
                </details>
            </td>
            <td>
                <details>
                    <summary>정답 확인</summary>
                    <div class="answer-content">관찰자와 함께 회전하므로 <b>정지</b>한 것으로 보임</div>
                </details>
            </td>
        </tr>
        <tr>
            <td class="label-cell">작용한 힘</td>
            <td>
                <details>
                    <summary>정답 확인</summary>
                    <div class="answer-content">
                        <span class="force-tag tag-emerald">탄성력 (구심력 역할)</span>만 작용
                    </div>
                </details>
            </td>
            <td>
                <details>
                    <summary>정답 확인</summary>
                    <div class="answer-content">
                        <span class="force-tag tag-emerald">탄성력</span>과 
                        <span class="force-tag tag-rose">원심력 (관성력)</span>이 모두 작용
                    </div>
                </details>
            </td>
        </tr>
        <tr>
            <td class="label-cell">운동 법칙의 해석</td>
            <td>
                <details>
                    <summary>정답 확인</summary>
                    <div class="answer-content">탄성력이 <b>구심력</b>으로 작용하여 <b>가속도 운동(원운동)</b>을 일으킴</div>
                </details>
            </td>
            <td>
                <details>
                    <summary>정답 확인</summary>
                    <div class="answer-content">탄성력과 원심력이 <b>평형</b>을 이루어 <b>정지 상태</b>를 유지함</div>
                </details>
            </td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# 탐구 질문
st.info("💡 **생각해보기**: 원심력은 실제로 추를 밖으로 밀어내는 힘일까요? 아니면 관찰자가 회전(가속)하기 때문에 나타나는 가상의 힘일까요?")
