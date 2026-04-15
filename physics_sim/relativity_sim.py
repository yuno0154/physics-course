import streamlit as st
import streamlit.components.v1 as components

# 페이지 제목
st.set_page_config(page_title="가속좌표계 탐구", layout="wide")
st.title("🚌 가속좌표계와 관성력 탐구 시뮬레이션")

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
            const [accel, setAccel] = useState(2); 
            const [view, setView] = useState('external'); 
            const [isMoving, setIsMoving] = useState(false);
            const [showForces, setShowForces] = useState(true);
            
            const posRef = useRef(0);
            const velRef = useRef(0);
            const [renderPos, setRenderPos] = useState(0);

            const g = 9.8; 
            const L = 120; 
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
                        posRef.current += velRef.current * dt * 40; 
                        setRenderPos(posRef.current);
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

            const bgOffset = view === 'internal' ? (-renderPos % 800) : 0;
            const busX = view === 'external' ? ((renderPos % 1000) - 100) : 220;

            const m = 1; 
            const scale = 8; // Force vector scale

            return (
                <div className="p-4 max-w-full mx-auto space-y-4">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        <div className="lg:col-span-3 space-y-4">
                            <div className="glass-card p-6 rounded-[32px] shadow-sm space-y-6">
                                <div className="space-y-4">
                                    <div className="flex bg-slate-100 p-1 rounded-2xl text-[11px] font-bold">
                                        <button onClick={() => setView('external')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'external' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500'}`}>버스 밖 (관성계)</button>
                                        <button onClick={() => setView('internal')} className={`flex-1 py-1.5 rounded-xl transition-all ${view === 'internal' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500'}`}>버스 안 (비관성계)</button>
                                    </div>
                                    
                                    <div className="space-y-3">
                                        <div className="flex justify-between text-[10px] font-black text-slate-400 uppercase tracking-widest">
                                            가속도 (a) <span className="text-blue-600">{accel.toFixed(1)} m/s²</span>
                                        </div>
                                        <input type="range" min="-10" max="10" step="0.5" value={accel} onChange={(e) => setAccel(parseFloat(e.target.value))} className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-blue-600" />
                                    </div>

                                    <div className="flex items-center gap-2 text-xs font-bold text-slate-600">
                                        <input type="checkbox" id="forces" checked={showForces} onChange={(e)=>setShowForces(e.target.checked)} className="w-4 h-4 accent-blue-600" />
                                        <label htmlFor="forces">힘 벡터 표시 (T, mg, F/f)</label>
                                    </div>

                                    <button onClick={() => setIsMoving(!isMoving)} className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-2 ${isMoving ? 'bg-rose-500 text-white' : 'bg-blue-600 text-white shadow-lg'}`}>
                                        <Icon name={isMoving ? "pause" : "play"} /> {isMoving ? "정지" : "운동 시작"}
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div className="lg:col-span-9">
                            <div className="bg-white rounded-[40px] shadow-2xl border border-slate-100 overflow-hidden relative h-[500px]">
                                <div className="absolute top-4 left-4 z-10 flex gap-4 pointer-events-none">
                                    <div className="flex items-center gap-2 px-3 py-1 bg-white/80 rounded-full border border-slate-200 text-[10px] font-bold">
                                        <div className="w-2 h-2 rounded-full bg-blue-500"></div> 장력 (T)
                                    </div>
                                    <div className="flex items-center gap-2 px-3 py-1 bg-white/80 rounded-full border border-slate-200 text-[10px] font-bold">
                                        <div className="w-2 h-2 rounded-full bg-emerald-500"></div> 중력 (mg)
                                    </div>
                                    <div className="flex items-center gap-2 px-3 py-1 bg-white/80 rounded-full border border-slate-200 text-[10px] font-bold">
                                        <div className="w-2 h-2 rounded-full bg-rose-500"></div> {view === 'internal' ? '관성력 (-ma)' : '합력 (F=ma)'}
                                    </div>
                                </div>

                                <div className="relative h-full bg-slate-50 overflow-hidden">
                                    <svg viewBox="0 0 800 500" className="w-full h-full select-none">
                                        <defs>
                                            <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" /></marker>
                                            <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" /></marker>
                                            <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" /></marker>
                                        </defs>

                                        <g transform={`translate(${bgOffset}, 350)`}>
                                            {[...Array(20)].map((_, i) => (
                                                <rect key={i} x={i * 100 - 200} y="0" width="2" height="40" fill="#cbd5e1" />
                                            ))}
                                            <line x1="-1000" y1="0" x2="2000" y2="0" stroke="#cbd5e1" strokeWidth="2" />
                                            {view === 'external' && (
                                                <g transform="translate(100, -50) scale(0.8)">
                                                    <circle cx="0" cy="-40" r="10" fill="#334155" />
                                                    <path d="M -8 -30 Q 0 -32 8 -30 L 12 10 L -12 10 Z" fill="#334155" />
                                                    <rect x="-10" y="10" width="8" height="30" rx="2" fill="#334155" />
                                                    <rect x="2" y="10" width="8" height="30" rx="2" fill="#334155" />
                                                </g>
                                            )}
                                        </g>

                                        <g transform={`translate(${busX}, 140)`}>
                                            <rect x="0" y="0" width="380" height="200" rx="40" fill="#3b82f6" stroke="#1e40af" strokeWidth="4" />
                                            <rect x="50" y="40" width="80" height="70" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            <rect x="150" y="40" width="80" height="70" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            <rect x="250" y="40" width="80" height="70" rx="12" fill="#e0f2fe" opacity="0.9" />
                                            <circle cx="90" cy="200" r="35" fill="#0f172a" /><circle cx="290" cy="200" r="35" fill="#0f172a" />
                                            
                                            {/* Person inside (only if internal) */}
                                            {view === 'internal' && (
                                                <g transform="translate(100, 150) scale(0.7)">
                                                    <circle cx="0" cy="-40" r="10" fill="white" />
                                                    <path d="M -8 -30 Q 0 -32 8 -30 L 12 10 L -12 10 Z" fill="white" />
                                                </g>
                                            )}

                                            <line x1="190" y1="50" x2={bobX+10} y2={bobY} stroke="white" strokeWidth="4" />
                                            <circle cx={bobX+10} cy={bobY} r="15" fill="#f1f5f9" stroke="#1e293b" strokeWidth="3" />

                                            {showForces && (
                                                <g transform={`translate(${bobX+10}, ${bobY})`}>
                                                    {/* Tension T */}
                                                    <line x1="0" y1="0" x2={(180 - bobX)*scale/12} y2={(50 - bobY)*scale/12} stroke="#3b82f6" strokeWidth="3" markerEnd="url(#arrow-blue)" />
                                                    {/* Gravity mg */}
                                                    <line x1="0" y1="0" x2="0" y2={g * scale} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                                    
                                                    {view === 'internal' ? (
                                                        /* Inertial Force -ma */
                                                        <line x1="0" y1="0" x2={-accel * scale} y2="0" stroke="#f43f5e" strokeWidth="3" markerEnd="url(#arrow-red)" />
                                                    ) : (
                                                        /* Net Force F=ma (drawn from end of T or separately) */
                                                        /* Here we draw it horizontally from bob to match conceptual diagrams */
                                                        <line x1="0" y1="0" x2={accel * scale} y2="0" stroke="#f43f5e" strokeWidth="3" markerEnd="url(#arrow-red)" />
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

# 시뮬레이션 삽입
components.html(react_code, height=540, scrolling=False)

# 탐구 표 구성
st.markdown("### 🔍 시점에 따른 운동 및 힘 분석")

with st.expander("👀 시점별 분석 결과 확인하기 (먼저 생각해 보고 클릭하세요!)"):
    # 스타일링된 HTML 테이블
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
            background-color: #1e293b;
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: 800;
            font-size: 14px;
            border: 1px solid #334155;
        }
        .physics-table td {
            padding: 15px;
            border: 1px solid #e2e8f0;
            vertical-align: middle;
            font-size: 14px;
        }
        .physics-table tr:nth-child(even) { background-color: #f8fafc; }
        .label-cell { 
            background-color: #f1f5f9; 
            font-weight: 700; 
            text-align: center; 
            width: 15%;
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
        .tag-blue { background: #dbeafe; color: #1e40af; }
        .tag-green { background: #dcfce7; color: #166534; }
        .tag-red { background: #fee2e2; color: #991b1b; }
    </style>

    <table class="physics-table">
        <thead>
            <tr>
                <th>구분</th>
                <th>🚌 버스 밖에서 관찰한 손잡이</th>
                <th>🙆 버스 안에서 관찰한 손잡이</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="label-cell">관찰한 운동 상태</td>
                <td>버스의 진행 방향과 같게 <b>가속도 운동</b>을 함</td>
                <td>움직이지 않고 한쪽으로 기울어진 채 <b>정지</b>해 있음</td>
            </tr>
            <tr>
                <td class="label-cell">작용한 힘</td>
                <td>
                    <span class="force-tag tag-green">중력 (mg)</span>, 
                    <span class="force-tag tag-blue">장력 (T)</span>, 
                    <span class="force-tag tag-red">합력 (F)</span>
                </td>
                <td>
                    <span class="force-tag tag-green">중력 (mg)</span>, 
                    <span class="force-tag tag-blue">장력 (T)</span>, 
                    <span class="force-tag tag-red">관성력 (fin)</span>
                </td>
            </tr>
            <tr>
                <td class="label-cell">운동 현상의 원인</td>
                <td>실이 당기는 힘(장력)과 중력의 <b>합력이 알짜힘(F=ma)</b>으로 작용하여 버스와 함께 가속됨</td>
                <td>중력, 장력, 그리고 <b>관성력(-ma)</b>이 세 힘의 평형을 이루어 정지한 것으로 보임</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # 탐구 질문
    st.info("💡 **생각해보기**: 버스 안의 관찰자가 느끼는 '관성력'은 실제로 존재하는 힘일까요? 아니면 관찰자의 좌표계가 가속되기 때문에 나타나는 가상의 힘일까요?")
