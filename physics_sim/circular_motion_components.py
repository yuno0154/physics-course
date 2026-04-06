import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="원운동의 성분 분석: 삼각함수와 조화 운동", layout="wide")
    
    # 상단 브랜딩 및 제목
    st.title("📊 원운동의 성분 분석: 삼각함수와 조화 운동")
    st.markdown("""
    이 시뮬레이션은 등속 원운동을 **x축**과 **y축** 성분으로 분해하여 분석합니다.
    위치, 속도, 가속도의 각 성분이 시간에 따라 어떻게 **사인(sin)**과 **코사인(cos)** 파형을 그리는지 확인해 보세요.
    """)

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
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            .no-scrollbar::-webkit-scrollbar { display: none; }
            .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
            .math-font { font-family: 'Times New Roman', serif; font-style: italic; }
            .graph-line { fill: none; stroke-width: 2; vector-effect: non-scaling-stroke; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef, useMemo } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                const iconRef = useRef(null);
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const ComponentSim = () => {
                const [time, setTime] = useState(0);
                const [isPlaying, setIsPlaying] = useState(true);
                const [omega, setOmega] = useState(1.0); // 각속력 (rad/s)
                const [radius, setRadius] = useState(1.0); // 반지름 (m)

                const maxTime = 12; // 총 시간 (s)
                const samples = 200; // 그래프 샘플 수

                useEffect(() => {
                    let frame;
                    if (isPlaying) {
                        const tick = () => {
                            setTime(t => (t + 0.05) % maxTime);
                            frame = requestAnimationFrame(tick);
                        };
                        frame = requestAnimationFrame(tick);
                    }
                    return () => cancelAnimationFrame(frame);
                }, [isPlaying]);

                const angle = (omega * time);
                const pos = { x: radius * Math.cos(angle), y: radius * Math.sin(angle) };
                const vel = { x: -radius * omega * Math.sin(angle), y: radius * omega * Math.cos(angle) };
                const acc = { x: -radius * omega * omega * Math.cos(angle), y: -radius * omega * omega * Math.sin(angle) };

                // 시각화 스케일
                const circleSize = 180;
                const graphWidth = 400;
                const graphHeight = 110;

                const getPath = (func, scale = 1, offset = 0) => {
                    let points = [];
                    for (let i = 0; i < samples; i++) {
                        const t = (i / samples) * maxTime;
                        const val = func(t);
                        const x = (t / maxTime) * graphWidth;
                        const y = (graphHeight / 2) - val * (graphHeight / 2.5) * scale;
                        points.push(`${x},${y}`);
                    }
                    return points.join(" ");
                };

                const GraphPanel = ({ title, xFunc, yFunc, xVal, yVal, xLabel, yLabel, colorX, colorY, scale = 1 }) => (
                    <div className="bg-slate-50/50 p-4 rounded-3xl border border-slate-100 space-y-2">
                        <div className="flex justify-between items-center mb-1">
                            <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{title}</h4>
                            <div className="flex gap-4">
                                <div className="flex items-center gap-1">
                                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: colorX }}></div>
                                    <span className="text-[11px] font-bold text-slate-600">{xLabel}</span>
                                </div>
                                <div className="flex items-center gap-1">
                                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: colorY }}></div>
                                    <span className="text-[11px] font-bold text-slate-600">{yLabel}</span>
                                </div>
                            </div>
                        </div>
                        <div className="relative h-[110px] w-full bg-white rounded-xl border border-slate-100 overflow-hidden shadow-inner">
                            {/* 격자선 */}
                            <line x1="0" y1={graphHeight/2} x2={graphWidth} y2={graphHeight/2} stroke="#f1f5f9" strokeWidth="1" />
                            {/* 현재 시간 수직선 */}
                            <line x1={(time/maxTime)*graphWidth} y1="0" x2={(time/maxTime)*graphWidth} y2={graphHeight} stroke="#e2e8f0" strokeWidth="2" />
                            
                            <svg viewBox={`0 0 ${graphWidth} ${graphHeight}`} className="w-full h-full" preserveAspectRatio="none">
                                <polyline points={getPath(xFunc, scale)} className="graph-line" stroke={colorX} opacity="0.3" />
                                <polyline points={getPath(yFunc, scale)} className="graph-line" stroke={colorY} opacity="0.3" />
                                <circle cx={(time/maxTime)*graphWidth} cy={(graphHeight/2) - xVal * (graphHeight / 2.5) * scale} r="4" fill={colorX} />
                                <circle cx={(time/maxTime)*graphWidth} cy={(graphHeight/2) - yVal * (graphHeight / 2.5) * scale} r="4" fill={colorY} />
                            </svg>
                        </div>
                    </div>
                );

                return (
                    <div className="flex flex-col items-center bg-transparent min-h-screen p-1 text-slate-800">
                        <div className="w-full max-w-7xl rounded-[32px] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.15)] border border-slate-200 overflow-hidden bg-white">
                            
                            {/* 상단 컨트롤 바 */}
                            <div className="flex items-center justify-between px-8 py-4 bg-slate-900 text-white border-b border-slate-800">
                                <div className="flex items-center gap-6">
                                    <button 
                                        onClick={() => setIsPlaying(!isPlaying)}
                                        className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${isPlaying ? 'bg-rose-500 hover:bg-rose-600' : 'bg-emerald-500 hover:bg-emerald-600'}`}
                                    >
                                        <Icon name={isPlaying ? "pause" : "play"} size={24} className="text-white" />
                                    </button>
                                    <div className="space-y-1">
                                        <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest leading-none">실시간 데이터</p>
                                        <div className="flex gap-4">
                                            <span className="text-xl font-black text-sky-400 italic">t = {time.toFixed(2)}s</span>
                                            <span className="text-xl font-black text-amber-500 italic">θ = {angle.toFixed(2)}rad</span>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex gap-8">
                                    <div className="w-48 space-y-1">
                                        <div className="flex justify-between"><span className="text-[10px] text-slate-400 font-black uppercase tracking-widest">반지름 (r)</span><span className="text-[11px] font-bold text-white">{radius.toFixed(1)}m</span></div>
                                        <input type="range" min="0.5" max="1.5" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-full accent-emerald-500 h-1" />
                                    </div>
                                    <div className="w-48 space-y-1">
                                        <div className="flex justify-between"><span className="text-[10px] text-slate-400 font-black uppercase tracking-widest">각속도 (ω)</span><span className="text-[11px] font-bold text-white">{omega.toFixed(1)} rad/s</span></div>
                                        <input type="range" min="0.5" max="2.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full accent-amber-500 h-1" />
                                    </div>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row divide-x divide-slate-100">
                                {/* 1. 원운동 시각화 */}
                                <div className="lg:w-[450px] bg-slate-50 flex items-center justify-center p-12 relative overflow-hidden">
                                    <div className="absolute top-8 left-8">
                                        <h3 className="text-sm font-black text-slate-900 border-l-4 border-slate-900 pl-3">2D 궤적 및 벡터</h3>
                                    </div>
                                    <svg viewBox="0 0 400 400" className="w-full h-full max-w-[340px] drop-shadow-2xl">
                                        {/* 좌표축 */}
                                        <line x1="0" y1="200" x2="400" y2="200" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="4,4" />
                                        <line x1="200" y1="0" x2="200" y2="400" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="4,4" />
                                        
                                        {/* 궤도 */}
                                        <circle cx="200" cy="200" r={radius * 120} fill="none" stroke="#e2e8f0" strokeWidth="2" />
                                        
                                        {/* 위치 벡터 및 성분 */}
                                        <line x1="200" y1="200" x2={200 + pos.x * 120} y2={200 - pos.y * 120} stroke="#cbd5e1" strokeWidth="2" />
                                        <line x1="200" y1="200" x2={200 + pos.x * 120} y2="200" stroke="#3b82f6" strokeWidth="4" strokeLinecap="round" opacity="0.6" />
                                        <line x1="200" y1="200" x2="200" y2={200 - pos.y * 120} stroke="#f43f5e" strokeWidth="4" strokeLinecap="round" opacity="0.6" />
                                        
                                        {/* 가속도 벡터 (중심 방향) */}
                                        <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120 + acc.x * 30} y2={200 - pos.y * 120 - acc.y * 30} stroke="#f59e0b" strokeWidth="3" markerEnd="url(#arrow-amber)" />

                                        {/* 속도 벡터 (접선 방향) */}
                                        <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120 + vel.x * 40} y2={200 - pos.y * 120 - vel.y * 40} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />

                                        {/* 물체 */}
                                        <circle cx={200 + pos.x * 120} cy={200 - pos.y * 120} r="10" fill="#0f172a" stroke="white" strokeWidth="3" />
                                        
                                        <defs>
                                            <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="5" orientation="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#10b981" /></marker>
                                            <marker id="arrow-amber" markerWidth="10" markerHeight="10" refX="9" refY="5" orientation="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#f59e0b" /></marker>
                                        </defs>
                                    </svg>
                                </div>

                                {/* 2. 성분 그래프들 */}
                                <div className="flex-1 p-6 space-y-4 max-h-[680px] overflow-y-auto no-scrollbar bg-white">
                                    <GraphPanel 
                                        title="1. 위치 성분 ($x$, $y$)" 
                                        xFunc={t => radius * Math.cos(omega*t)}
                                        yFunc={t => radius * Math.sin(omega*t)}
                                        xVal={pos.x} yVal={pos.y}
                                        xLabel="x = r cos θ" yLabel="y = r sin θ"
                                        colorX="#3b82f6" colorY="#f43f5e"
                                    />
                                    <GraphPanel 
                                        title="2. 속도 성분 ($v_x$, $v_y$)" 
                                        xFunc={t => -radius * omega * Math.sin(omega*t)}
                                        yFunc={t => radius * omega * Math.cos(omega*t)}
                                        xVal={vel.x} yVal={vel.y}
                                        xLabel="v_x = -v sin θ" yLabel="v_y = v cos θ"
                                        colorX="#10b981" colorY="#059669"
                                        scale={1 / omega}
                                    />
                                    <GraphPanel 
                                        title="3. 가속도 성분 ($a_x$, $a_y$)" 
                                        xFunc={t => -radius * omega * omega * Math.cos(omega*t)}
                                        yFunc={t => -radius * omega * omega * Math.sin(omega*t)}
                                        xVal={acc.x} yVal={acc.y}
                                        xLabel="a_x = -a cos θ" yLabel="a_y = -a sin θ"
                                        colorX="#f59e0b" colorY="#d97706"
                                        scale={1 / (omega * omega)}
                                    />

                                    <div className="p-5 bg-slate-900 rounded-[28px] mt-2 border-t border-slate-700">
                                        <div className="flex gap-4 items-start">
                                            <div className="p-3 bg-white/5 rounded-2xl">
                                                <Icon name="info" size={24} className="text-sky-400" />
                                            </div>
                                            <div>
                                                <h5 className="text-white font-black text-sm mb-1 uppercase tracking-wider">물리학적 통찰</h5>
                                                <p className="text-slate-400 text-xs leading-relaxed">
                                                    각 그래프의 파형을 비교해 보세요. 속도 성분은 위치보다 <span className="text-emerald-400 font-bold">π/2</span>만큼 위상이 빠르고, 가속도 성분은 위치와 <span className="text-amber-400 font-bold">반대 방향(π 차이)</span>임을 시각적으로 확인할 수 있습니다.
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<ComponentSim />);
        </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트로 HTML 삽입
    components.html(react_code, height=820, scrolling=False)

if __name__ == "__main__":
    run_sim()
