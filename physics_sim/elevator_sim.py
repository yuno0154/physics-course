import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정 및 제목
st.set_page_config(page_title="엘리베이터 관성력 탐구", layout="wide")
st.title("🛗 엘리베이터 시뮬레이션: 겉보기 무게와 관성력")

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
            const [selectedForces, setSelectedForces] = useState({ N: false, mg: false, F: false });
            
            const posRef = useRef(0);
            const velRef = useRef(0);
            const [renderPos, setRenderPos] = useState(0);

            const g = 10; 
            const m = 65; 
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

            const handleReset = () => {
                setIsMoving(false);
                posRef.current = 0;
                velRef.current = 0;
                setRenderPos(0);
            };

            const shaftOffset = view === 'internal' ? (renderPos % 200) : 0;
            const elevatorY = view === 'internal' ? 80 : (100 + (renderPos % 400 + 400) % 400 - 100);

            const toggleForce = (f) => {
                setSelectedForces(prev => ({ ...prev, [f]: !prev[f] }));
            };

            return (
                <div className="p-4 max-w-full mx-auto space-y-4">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-3 space-y-4">
                            <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-6">
                                <div className="space-y-4 text-center">
                                    <div className="flex bg-slate-100 p-1 rounded-2xl text-[11px] font-bold">
                                        <button onClick={() => setView('external')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'external' ? 'bg-white text-sky-600 shadow-sm' : 'text-slate-500'}`}>외부 (관성계)</button>
                                        <button onClick={() => setView('internal')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'internal' ? 'bg-white text-sky-600 shadow-sm' : 'text-slate-500'}`}>내부 (비관성계)</button>
                                    </div>
                                    <div className="p-4 bg-slate-50 rounded-2xl text-left">
                                        <div className="flex justify-between text-[10px] font-black text-slate-400 mb-2 uppercase tracking-widest">가속도 <span className="text-sky-600">{accel.toFixed(1)} m/s²</span></div>
                                        <input type="range" min="-10" max="10" step="1" value={accel} onChange={(e)=>setAccel(parseFloat(e.target.value))} className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-sky-600" />
                                        <div className="flex justify-between text-[9px] mt-1 text-slate-400 font-bold"><span>하강 가속</span><span>정지/등속</span><span>상승 가속</span></div>
                                    </div>
                                    
                                    <div className="space-y-2 text-left">
                                        <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest">힘 벡터 선택</div>
                                        <div className="grid grid-cols-1 gap-2">
                                            <button onClick={() => toggleForce('N')} className={`px-3 py-2 rounded-xl text-[11px] font-bold transition-all border ${selectedForces.N ? 'bg-blue-50 text-blue-600 border-blue-200' : 'bg-white text-slate-400 border-slate-100'}`}>
                                                수직항력 (N)
                                            </button>
                                            <button onClick={() => toggleForce('mg')} className={`px-3 py-2 rounded-xl text-[11px] font-bold transition-all border ${selectedForces.mg ? 'bg-emerald-50 text-emerald-600 border-emerald-200' : 'bg-white text-slate-400 border-slate-100'}`}>
                                                중력 (mg)
                                            </button>
                                            <button onClick={() => toggleForce('F')} className={`px-3 py-2 rounded-xl text-[11px] font-bold transition-all border ${selectedForces.F ? 'bg-rose-50 text-rose-600 border-rose-200' : 'bg-white text-slate-400 border-slate-100'}`}>
                                                {view === 'internal' ? '관성력 (f)' : '합력 (F=ma)'}
                                            </button>
                                        </div>
                                    </div>

                                    <div className="flex flex-col gap-2">
                                        <button onClick={()=>setIsMoving(!isMoving)} className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-2 ${isMoving ? 'bg-rose-500 text-white' : 'bg-sky-600 text-white shadow-lg'}`}>
                                            <Icon name={isMoving ? "pause" : "play"} /> {isMoving ? "운행 중지" : "운동 시작"}
                                        </button>
                                        <button onClick={handleReset} className="w-full py-3 rounded-2xl font-black text-sm flex items-center justify-center gap-2 bg-slate-200 text-slate-600 hover:bg-slate-300 transition-all">
                                            <Icon name="refresh-cw" size={16} /> 초기화 (Reset)
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-slate-900 p-6 rounded-[32px] text-center shadow-xl border-t-4 border-sky-400">
                                <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">저울 측정 체중 (N)</div>
                                <div className={`text-4xl font-black ${Math.abs(accel) < 0.1 ? 'text-white' : (accel > 0 ? 'text-emerald-400' : 'text-rose-400')}`}>
                                    {apparentWeight.toFixed(0)} <span className="text-lg">N</span>
                                </div>
                                <div className="text-[10px] text-slate-500 mt-2 font-bold">(실제 체중: 650 N)</div>
                            </div>
                        </div>

                        <div className="lg:col-span-9">
                            <div className="bg-white rounded-[40px] shadow-2xl border border-slate-100 overflow-hidden relative h-[500px]">
                                <div className="p-4 bg-slate-900 flex justify-between text-white/50 text-[10px] font-black uppercase tracking-widest">
                                    <span>{view === 'internal' ? '엘리베이터 안의 관찰자 (비관성 좌표계)' : '엘리베이터 밖의 관찰자 (관성 좌표계)'}</span>
                                    <div className="flex gap-4">
                                        <span className={`transition-opacity ${selectedForces.N ? 'text-blue-400 opacity-100' : 'opacity-20'}`}>● 수직항력 (N)</span>
                                        <span className={`transition-opacity ${selectedForces.mg ? 'text-emerald-400 opacity-100' : 'opacity-20'}`}>● 중력 (mg)</span>
                                        <span className={`transition-opacity ${selectedForces.F ? 'text-rose-400 opacity-100' : 'opacity-20'}`}>● {view==='internal' ? '관성력 (f)' : '합력 (F)'}</span>
                                    </div>
                                </div>
                                <div className="relative h-full bg-slate-50 overflow-hidden">
                                    <svg viewBox="0 0 600 450" className="w-full h-full select-none">
                                        <defs>
                                            <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" /></marker>
                                            <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" /></marker>
                                            <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" /></marker>
                                        </defs>

                                        <g transform={`translate(0, ${shaftOffset})`}>
                                            {[...Array(10)].map((_, i) => (
                                                <g key={i}>
                                                    <line x1="280" y1={i * 100 - 200} x2="260" y2={i * 100 - 200} stroke="#cbd5e1" strokeWidth="2" />
                                                    <text x="240" y={i * 100 - 195} className="text-[10px] fill-slate-300 font-bold">{10 - i}F</text>
                                                </g>
                                            ))}
                                            {[...Array(10)].map((_, i) => (
                                                <line key={i} x1="520" y1={i * 100 - 200} x2="540" y2={i * 100 - 200} stroke="#cbd5e1" strokeWidth="2" />
                                            ))}
                                        </g>
                                        <line x1="280" y1="0" x2="280" y2="450" stroke="#e2e8f0" strokeWidth="1" />
                                        <line x1="520" y1="0" x2="520" y2="450" stroke="#e2e8f0" strokeWidth="1" />

                                        <g transform="translate(100, 225)">
                                            <rect x="-80" y="-120" width="160" height="240" rx="16" fill="#f8fafc" stroke="#e2e8f0" strokeWidth="2" />
                                            <text x="0" y="-100" textAnchor="middle" className="text-[11px] font-black fill-slate-400 italic">힘의 자유체도 (FBD)</text>
                                            <circle cx="0" cy="0" r="10" fill="#475569" />
                                            
                                            {selectedForces.mg && (
                                                <g>
                                                    <line x1="0" y1="0" x2="0" y2="70" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrow-green)" />
                                                    <text x="15" y="60" className="text-[10px] font-bold fill-emerald-600">mg</text>
                                                </g>
                                            )}
                                            {selectedForces.N && (
                                                <g>
                                                    <line x1="0" y1="0" x2="0" y2={-apparentWeight/10} stroke="#3b82f6" strokeWidth="4" markerEnd="url(#arrow-blue)" />
                                                    <text x="15" y="-60" className="text-[10px] font-bold fill-blue-600">N</text>
                                                </g>
                                            )}
                                            {selectedForces.F && Math.abs(accel) > 0.1 && (
                                                <g>
                                                    {view === 'internal' ? (
                                                        <>
                                                            <line x1="0" y1="0" x2="0" y2={inertialForce/10} stroke="#f43f5e" strokeWidth="4" markerEnd="url(#arrow-red)" />
                                                            <text x="-35" y={inertialForce > 0 ? 30 : -30} className="text-[10px] font-bold fill-rose-600">f (관성력)</text>
                                                        </>
                                                    ) : (
                                                        <>
                                                            <line x1="-20" y1="0" x2="-20" y2={-accel * 5} stroke="#f43f5e" strokeWidth="4" markerEnd="url(#arrow-red)" />
                                                            <text x="-55" y={accel > 0 ? -30 : 30} className="text-[10px] font-bold fill-rose-600">F (합력)</text>
                                                        </>
                                                    )}
                                                </g>
                                            )}
                                        </g>

                                        <g transform={`translate(300, ${elevatorY})`}>
                                            <rect x="0" y="0" width="200" height="280" rx="20" fill="white" stroke="#94a3b8" strokeWidth="4" />
                                            <rect x="30" y="240" width="140" height="15" rx="4" fill="#334155" />
                                            <g transform="translate(100, 240) scale(0.9)">
                                                <circle cx="0" cy="-140" r="20" fill="#334155" />
                                                <path d="M -15 -120 Q 0 -125 15 -120 L 22 -60 L -22 -60 Z" fill="#334155" />
                                                <rect x="-20" y="-60" width="15" height="60" rx="4" fill="#334155" />
                                                <rect x="5" y="-60" width="15" height="60" rx="4" fill="#334155" />
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
components.html(react_code, height=540, scrolling=False)

# 탐구 문제 표
st.markdown("### 📋 [탐구 문제] 엘리베이터 운동에 따른 몸무게 변화 분석")
st.write("표는 엘리베이터가 정지해 있을 때 몸무게가 **650N**인 사람이 엘리베이터의 움직임에 따라 몸무게의 변화를 측정한 것이다.")

# 스타일링된 HTML 테이블 (각 셀마다 정답 확인 버튼 적용)
st.markdown("""
<style>
    .elevator-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-family: 'Pretendard', sans-serif;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .elevator-table th {
        background-color: #0f172a;
        color: white;
        padding: 12px;
        text-align: center;
        font-weight: 800;
        font-size: 13px;
        border: 1px solid #1e293b;
    }
    .elevator-table td {
        padding: 15px;
        border: 1px solid #e2e8f0;
        text-align: center;
        font-size: 14px;
        vertical-align: middle;
    }
    .label-col {
        background-color: #f8fafc;
        font-weight: 700;
        width: 25%;
    }
    .weight-val { font-weight: 800; color: #334155; }
    
    /* 각 셀 정답 확인 버튼 스타일 */
    summary {
        cursor: pointer;
        list-style: none;
        background-color: #0ea5e9;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 800;
        display: inline-block;
        color: white;
        transition: all 0.2s;
    }
    summary:hover { background-color: #0284c7; }
    details[open] summary { display: none; }
    .answer-content { animation: fadeIn 0.3s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>

<table class="elevator-table">
    <thead>
        <tr>
            <th>구분</th>
            <th>🚀 출발 직후</th>
            <th>↔ 등속 운동</th>
            <th>🛑 멈추기 직전</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="label-col">⬆️ 올라갈 때 (몸무게)</td>
            <td class="weight-val text-emerald-600">780 N</td>
            <td class="weight-val">650 N</td>
            <td class="weight-val text-rose-600">520 N</td>
        </tr>
        <tr>
            <td class="label-col">⬇️ 내려갈 때 (몸무게)</td>
            <td class="weight-val text-rose-600">520 N</td>
            <td class="weight-val">650 N</td>
            <td class="weight-val text-emerald-600">780 N</td>
        </tr>
        <tr>
            <td class="label-col">관성력의 크기와 방향</td>
            <td><details><summary>확인</summary><div class="answer-content"><b>130 N (아래)</b></div></details></td>
            <td><details><summary>확인</summary><div class="answer-content"><b>0</b></div></details></td>
            <td><details><summary>확인</summary><div class="answer-content"><b>130 N (위)</b></div></details></td>
        </tr>
        <tr>
            <td class="label-col">엘리베이터의 가속도</td>
            <td><details><summary>확인</summary><div class="answer-content"><b>2 m/s² (위)</b></div></details></td>
            <td><details><summary>확인</summary><div class="answer-content"><b>0</b></div></details></td>
            <td><details><summary>확인</summary><div class="answer-content"><b>2 m/s² (아래)</b></div></details></td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

with st.expander("👀 엘리베이터 운동 분석 및 정답 확인하기"):
    st.success("### 💡 탐구 포인트")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **1. 겉보기 무게의 변화**
        *   엘리베이터가 **위로 가속**될 때($a>0$) 몸무게는 실제보다 **더 무겁게** 측정됩니다.
        *   엘리베이터가 **아래로 가속**될 때($a<0$) 몸무게는 실제보다 **더 가볍게** 측정됩니다.
        """)
    with col2:
        st.markdown("""
        **2. 관성력의 방향**
        *   내부 관찰자는 엘리베이터의 가속도와 **반대 방향**으로 작용하는 **관성력($f = -ma$)**을 느낍니다.
        *   저울의 눈금은 **수직항력($N$)**의 크기와 같으며, $N = mg - f$ (방향 고려)로 계산됩니다.
        """)
