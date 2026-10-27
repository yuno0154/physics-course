import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정 및 제목
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
            const [scenario, setScenario] = useState('');
            const [stopped, setStopped] = useState(false);

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
                        const vPrev = velRef.current;
                        let vNew = vPrev + accel * dt;
                        if (vPrev !== 0 && Math.sign(vNew) !== Math.sign(vPrev) && accel * vPrev < 0) {
                            // 감속하던 엘리베이터가 멈춤 → 정지, 가속도 0
                            vNew = 0;
                            velRef.current = 0;
                            setIsMoving(false);
                            setAccel(0);
                            setStopped(true);
                        }
                        velRef.current = vNew;
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
                setScenario('');
                setStopped(false);
            };

            // 활동지 '엘리베이터의 운동' 행에 맞춘 상황 버튼 (위쪽을 + 로 둔다)
            const SCEN = {
                upStart:   { label: '올라가며 출발',  v0: 0,  a: 2 },
                upStop:    { label: '올라가다 멈춤',  v0: 6,  a: -2 },
                downStart: { label: '내려가며 출발',  v0: 0,  a: -2 },
                downStop:  { label: '내려가다 멈춤',  v0: -6, a: 2 },
                steady:    { label: '등속 운동',      v0: 3,  a: 0 },
            };
            const runScenario = (key) => {
                const sc = SCEN[key];
                posRef.current = 0; setRenderPos(0);
                velRef.current = sc.v0;
                setAccel(sc.a);
                setScenario(key);
                setStopped(false);
                setIsMoving(true);
            };
            const v = velRef.current;
            const moveText = (() => {
                if (stopped) return '멈춤 (정지)';
                if (!isMoving && Math.abs(v) < 0.01) return accel === 0 ? '정지' : '출발 전';
                const dir = v > 0.01 ? '올라가면서' : (v < -0.01 ? '내려가면서' : '');
                if (Math.abs(accel) < 0.01) return dir ? dir + ' 등속 운동' : '정지';
                if (!dir) return '출발';
                return dir + (accel * v > 0 ? ' 속력 증가' : ' 속력 감소');
            })();
            const gEff = apparentWeight / m;

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
                                        <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest">상황 선택 (가속도 2 m/s²)</div>
                                        <div className="grid grid-cols-2 gap-2">
                                            {['upStart','upStop','downStart','downStop'].map(k => (
                                                <button key={k} onClick={() => runScenario(k)} className={`px-2 py-2 rounded-xl text-[11px] font-bold border transition-all ${scenario === k ? 'bg-sky-600 text-white border-sky-600' : 'bg-white text-slate-500 border-slate-200'}`}>{SCEN[k].label}</button>
                                            ))}
                                            <button onClick={() => runScenario('steady')} className={`col-span-2 px-2 py-2 rounded-xl text-[11px] font-bold border transition-all ${scenario === 'steady' ? 'bg-sky-600 text-white border-sky-600' : 'bg-white text-slate-500 border-slate-200'}`}>{SCEN.steady.label}</button>
                                        </div>
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
                                <div className="mt-4 pt-4 border-t border-slate-700 space-y-2 text-left text-[11px] font-bold text-slate-300">
                                    <div className="flex justify-between"><span>엘리베이터</span><span className="text-sky-300">{moveText}</span></div>
                                    <div className="flex justify-between"><span>관성력 (안에서 본)</span><span className="text-rose-300">{Math.abs(accel) < 0.01 ? '없음' : `${Math.abs(m * accel).toFixed(0)} N, ${accel > 0 ? '아래' : '위'}`}</span></div>
                                    <div className="flex justify-between"><span>같은 눈금이 나오는 중력 가속도</span><span className="text-amber-300">{gEff.toFixed(0)} m/s²</span></div>
                                    <div className="text-[10px] text-slate-500 font-normal">= 저울 눈금 ÷ 질량(65 kg)</div>
                                </div>
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
components.html(react_code, height=760, scrolling=False)

# 탐구 문제 표 (활동지 B와 같은 구조)
st.markdown("### 📋 [탐구 문제] 저울 눈금을 중력과 관성력으로 해석하기")
st.write("몸무게가 **650 N(질량 65 kg)**인 사람이 엘리베이터 안에서 저울에 올라섰다. 위의 **상황 선택** 버튼으로 각 경우를 재현하고, 활동지의 답을 **확인** 버튼으로 점검해 보자. (g = 10 m/s²)")

def _ans(t):
    return f'<details><summary>확인</summary><div class="answer-content"><b>{t}</b></div></details>'

rows = [
    ("엘리베이터의 운동", _ans("위로 가면서 속력 증가<br>아래로 가면서 속력 감소"), "정지해 있을 때<br>등속 운동할 때", _ans("위로 가면서 속력 감소<br>아래로 가면서 속력 증가")),
    ("① 저울 눈금", "<span class='weight-val text-emerald-600'>780 N</span>", "<span class='weight-val'>650 N</span>", "<span class='weight-val text-rose-600'>520 N</span>"),
    ("② 눈금의 해석", _ans("중력 650 N + 관성력 130 N"), "중력 650 N", _ans("중력 650 N − 관성력 130 N")),
    ("③ 관성력의 방향", _ans("아래"), "작용하지 않음", _ans("위")),
    ("④ 엘리베이터의 가속도", _ans("2 m/s², 위 방향"), "0", _ans("2 m/s², 아래 방향")),
    ("⑤ 같은 눈금이 나오는<br>중력 가속도 (눈금 ÷ 질량)", _ans("12 m/s²"), "10 m/s²", _ans("8 m/s²")),
]
body = "".join(f"<tr><td class='label-col'>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>" for r in rows)

st.markdown("""
<style>
    .elevator-table { width: 100%; border-collapse: collapse; margin: 10px 0; font-family: 'Pretendard', sans-serif;
        background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .elevator-table th { background-color: #0f172a; color: white; padding: 12px; text-align: center; font-weight: 800;
        font-size: 13px; border: 1px solid #1e293b; }
    .elevator-table td { padding: 12px; border: 1px solid #e2e8f0; text-align: center; font-size: 14px; vertical-align: middle; }
    .label-col { background-color: #f8fafc; font-weight: 700; width: 25%; }
    .weight-val { font-weight: 800; color: #334155; }
    .text-emerald-600 { color: #059669 !important; } .text-rose-600 { color: #e11d48 !important; }
    summary { cursor: pointer; list-style: none; background-color: #0ea5e9; padding: 4px 10px; border-radius: 6px;
        font-size: 11px; font-weight: 800; display: inline-block; color: white; transition: all 0.2s; }
    summary:hover { background-color: #0284c7; }
    details[open] summary { display: none; }
    .answer-content { animation: fadeIn 0.3s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
<table class="elevator-table">
    <thead><tr><th>가속도</th><th>⬆️ 위쪽으로 일정할 때</th><th>0일 때</th><th>⬇️ 아래쪽으로 일정할 때</th></tr></thead>
    <tbody>""" + body + """</tbody>
</table>
""", unsafe_allow_html=True)

with st.expander("👀 정리하기 및 탐구 포인트"):
    st.success("**정리하기** 엘리베이터 안의 저울 눈금은 사람에게 작용하는 중력과 **관성력**을 합한 힘의 크기와 같고, 관성력의 방향은 엘리베이터 가속도의 방향과 **반대**이다.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **1. 저울 눈금의 변화**
        *   엘리베이터가 **위로 가속**할 때 저울 눈금은 실제 몸무게보다 **크다**: $N = mg + ma$
        *   엘리베이터가 **아래로 가속**할 때 저울 눈금은 실제 몸무게보다 **작다**: $N = mg - ma$
        """)
    with col2:
        st.markdown("""
        **2. 관성력의 방향**
        *   엘리베이터 안의 관찰자는 엘리베이터의 가속도와 **반대 방향**으로 크기 $ma$인 **관성력**이 작용한다고 본다.
        *   위로 2 m/s²로 가속하는 엘리베이터 안의 저울은 중력 가속도가 **12 m/s²**인 곳에 정지해 있을 때와 같은 눈금을 보인다.
        """)
