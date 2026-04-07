import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    # st.set_page_config is removed as it's handled by main_app.py
    
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
            .math-block { background: rgba(15, 23, 42, 0.03); padding: 12px; border-radius: 12px; font-size: 14px; line-height: 1.6; border: 1px solid rgba(15, 23, 42, 0.05); }
            .graph-line { fill: none; stroke-width: 2; vector-effect: non-scaling-stroke; }
            .axis-line { stroke: #cbd5e1; stroke-width: 1.5; }
            .accordion-content { transition: all 0.3s ease-in-out; overflow: hidden; }
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

            const MathSymbol = ({ text, color = "inherit" }) => (
                <span className="math-font font-bold px-0.5" style={{ color }}>{text}</span>
            );

            // AccordionItem을 외부 컴포넌트로 정의
            const AccordionItem = ({ id, title, icon, activeId, onToggle, children }) => {
                const isOpen = activeId === id;
                return (
                    <div className="border-b border-slate-100 bg-white">
                        <button 
                            onClick={() => onToggle(id)}
                            className="w-full flex items-center justify-between py-4 px-8 hover:bg-slate-50 transition-all group"
                        >
                            <div className="flex items-center gap-4">
                                <span className={`p-2 rounded-xl transition-all ${isOpen ? 'bg-blue-600 shadow-lg text-white' : 'bg-slate-100 text-slate-400 group-hover:bg-slate-200'}`}>
                                    <Icon name={icon} size={18} />
                                </span>
                                <span className={`font-black text-sm lg:text-base tracking-tight transition-all ${isOpen ? 'text-slate-900' : 'text-slate-500'}`}>
                                    {title}
                                </span>
                            </div>
                            <span className={`transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}>
                                <Icon name="chevron-down" className="text-slate-300" />
                            </span>
                        </button>
                        <div 
                            className="accordion-content" 
                            style={{ 
                                maxHeight: isOpen ? '500px' : '0px',
                                opacity: isOpen ? 1 : 0,
                                visibility: isOpen ? 'visible' : 'hidden',
                                paddingBottom: isOpen ? '24px' : '0px'
                            }}
                        >
                            <div className="px-20 lg:px-24">
                                {children}
                            </div>
                        </div>
                    </div>
                );
            };

            const ComponentSim = () => {
                const [time, setTime] = useState(0);
                const [isPlaying, setIsPlaying] = useState(true);
                const [omega, setOmega] = useState(1.0); 
                const [radius, setRadius] = useState(1.0);
                const [activeId, setActiveId] = useState(null);

                const [showPos, setShowPos] = useState(true);
                const [showVel, setShowVel] = useState(true);
                const [showAcc, setShowAcc] = useState(true);

                const maxTime = 12; 
                const samples = 200; 

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

                const wt = (omega * time);
                const pos = { x: radius * Math.cos(wt), y: radius * Math.sin(wt) };
                const vel = { x: -radius * omega * Math.sin(wt), y: radius * omega * Math.cos(wt) };
                const acc = { x: -radius * omega * omega * Math.cos(wt), y: -radius * omega * omega * Math.sin(wt) };

                const graphWidth = 400;
                const graphHeight = 110;

                const getPath = (func, scale = 1) => {
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

                const GraphPanel = ({ title, xFunc, yFunc, xVal, yVal, xLabel, yLabel, colorX, colorY, scale = 1, yMax="1.0" }) => (
                    <div className="bg-slate-50/50 p-4 rounded-3xl border border-slate-100 space-y-2">
                        <div className="flex justify-between items-center mb-1">
                            <h4 className="text-[10px] font-black text-slate-400 tracking-widest">{title}</h4>
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
                        <div className="relative h-[120px] w-full bg-white rounded-xl border border-slate-100 overflow-hidden shadow-inner flex">
                            <div className="w-8 h-full border-r border-slate-100 flex flex-col justify-between py-1 text-[9px] font-bold text-slate-400 text-center select-none bg-slate-50/30">
                                <span>{yMax}</span><span>0</span><span>-{yMax}</span>
                            </div>
                            <div className="flex-1 relative overflow-hidden bg-[radial-gradient(#f1f5f9_1px,transparent_1px)] bg-[size:20px_20px]">
                                <svg viewBox={`0 0 ${graphWidth} ${graphHeight}`} className="w-full h-full" preserveAspectRatio="none">
                                    <line x1="0" y1={graphHeight/2} x2={graphWidth} y2={graphHeight/2} className="axis-line" strokeDasharray="4,2" />
                                    <line x1="0" y1="0" x2="0" y2={graphHeight} className="axis-line" stroke="#94a3b8" />
                                    <polyline points={getPath(xFunc, scale)} className="graph-line" stroke={colorX} opacity="0.2" />
                                    <polyline points={getPath(yFunc, scale)} className="graph-line" stroke={colorY} opacity="0.2" />
                                    <line x1={(time/maxTime)*graphWidth} y1="0" x2={(time/maxTime)*graphWidth} y2={graphHeight} stroke="#cbd5e1" strokeWidth="1" strokeDasharray="2,2" />
                                    <circle cx={(time/maxTime)*graphWidth} cy={(graphHeight / 2) - xVal * (graphHeight / 2.5) * scale} r="5" fill={colorX} stroke="white" strokeWidth="2" />
                                    <circle cx={(time/maxTime)*graphWidth} cy={(graphHeight / 2) - yVal * (graphHeight / 2.5) * scale} r="5" fill={colorY} stroke="white" strokeWidth="2" />
                                </svg>
                                <div className="absolute bottom-0 left-0 w-full px-2 flex justify-between text-[9px] font-black text-slate-400">
                                    <span>0s</span><span>시간 (t)</span><span>{maxTime}s</span>
                                </div>
                            </div>
                        </div>
                    </div>
                );

                const handleToggle = (id) => {
                    setActiveId(activeId === id ? null : id);
                };

                return (
                    <div className="flex flex-col items-center bg-transparent min-h-screen p-1 text-slate-800">
                        <div className="w-full max-w-7xl rounded-[32px] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.15)] border border-slate-200 overflow-hidden bg-white mb-8">
                            <div className="flex items-center justify-between px-8 py-4 bg-slate-900 text-white border-b border-slate-800">
                                <div className="flex items-center gap-6">
                                    <button onClick={() => setIsPlaying(!isPlaying)} className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${isPlaying ? 'bg-rose-500 hover:bg-rose-600' : 'bg-emerald-500 hover:bg-emerald-600 shadow-[0_0_15px_rgba(16,185,129,0.3)]'}`}>
                                        <Icon name={isPlaying ? "pause" : "play"} size={24} className="text-white" />
                                    </button>
                                    <div className="space-y-1">
                                        <p className="text-[10px] text-slate-400 font-black uppercase tracking-widest leading-none">물리 변수 제어</p>
                                        <div className="flex gap-4">
                                            <span className="text-xl font-black text-sky-400 italic">t = {time.toFixed(2)}s</span>
                                            <span className="text-xl font-black text-amber-500 italic">ωt = {wt.toFixed(2)}rad</span>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex gap-8">
                                    <div className="w-44 space-y-1">
                                        <p className="text-[10px] text-slate-400 font-black uppercase">반지름 (r)</p>
                                        <input type="range" min="0.5" max="1.5" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-full h-1 accent-sky-500" />
                                    </div>
                                    <div className="w-44 space-y-1">
                                        <p className="text-[10px] text-slate-400 font-black uppercase">각속도 (ω)</p>
                                        <input type="range" min="0.5" max="2.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full h-1 accent-amber-500" />
                                    </div>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row divide-x divide-slate-100 min-h-[640px]">
                                <div className="lg:w-[450px] bg-slate-50 flex flex-col items-center justify-center p-8 relative">
                                    <div className="absolute top-6 left-6 flex flex-col gap-2 z-10 w-[140px]">
                                        <button onClick={()=>setShowPos(!showPos)} className={`w-full py-1.5 rounded-lg text-[10px] font-black border-2 transition-all ${showPos ? 'bg-blue-600 border-blue-600 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>위치(r) 벡터 표시</button>
                                        <button onClick={()=>setShowVel(!showVel)} className={`w-full py-1.5 rounded-lg text-[10px] font-black border-2 transition-all ${showVel ? 'bg-emerald-500 border-emerald-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>속도(v) 벡터 표시</button>
                                        <button onClick={()=>setShowAcc(!showAcc)} className={`w-full py-1.5 rounded-lg text-[10px] font-black border-2 transition-all ${showAcc ? 'bg-amber-500 border-amber-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>가속도(a) 벡터 표시</button>
                                    </div>
                                    <svg viewBox="0 0 400 400" className="w-full h-full max-w-[340px] drop-shadow-2xl">
                                        <line x1="0" y1="200" x2="400" y2="200" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="4,4" />
                                        <line x1="200" y1="0" x2="200" y2="400" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="4,4" />
                                        <circle cx="200" cy="200" r={radius * 120} fill="none" stroke="#e2e8f0" strokeWidth="2" />
                                        {showPos && (
                                            <g><line x1="200" y1="200" x2={200 + pos.x * 120} y2={200 - pos.y * 120} stroke="#3b82f6" strokeWidth="2" />
                                               <line x1="200" y1="200" x2={200 + pos.x * 120} y2="200" stroke="#3b82f6" strokeWidth="4" strokeLinecap="round" opacity="0.4" />
                                               <line x1="200" y1="200" x2="200" y2={200 - pos.y * 120} stroke="#f43f5e" strokeWidth="4" strokeLinecap="round" opacity="0.4" />
                                            </g>
                                        )}
                                        {showAcc && (
                                            <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120 + acc.x * 30} y2={200 - pos.y * 120 - acc.y * 30} stroke="#f59e0b" strokeWidth="3" markerEnd="url(#arrow-amber)" />
                                        )}
                                        {showVel && (
                                            <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120 + vel.x * 40} y2={200 - pos.y * 120 - vel.y * 40} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                        )}
                                        <circle cx={200 + pos.x * 120} cy={200 - pos.y * 120} r="10" fill="#0f172a" stroke="white" strokeWidth="3" />
                                        <defs>
                                            <marker id="arrow-green" markerWidth="6" markerHeight="6" refX="5" refY="3" orientation="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#10b981" /></marker>
                                            <marker id="arrow-amber" markerWidth="6" markerHeight="6" refX="5" refY="3" orientation="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#f59e0b" /></marker>
                                        </defs>
                                    </svg>
                                </div>
                                <div className="flex-1 p-6 space-y-4 max-h-[660px] overflow-y-auto no-scrollbar bg-white">
                                    <GraphPanel title="1. 위치 성분 ($x$, $y$)" xFunc={t => radius * Math.cos(omega*t)} yFunc={t => radius * Math.sin(omega*t)} xVal={pos.x} yVal={pos.y} xLabel="x = r cos ωt" yLabel="y = r sin ωt" colorX="#3b82f6" colorY="#f43f5e" yMax="r" />
                                    <GraphPanel title="2. 속도 성분 ($v_x$, $v_y$)" xFunc={t => -radius * omega * Math.sin(omega*t)} yFunc={t => radius * omega * Math.cos(omega*t)} xVal={vel.x} yVal={vel.y} xLabel="v_x = -v sin ωt" yLabel="v_y = v cos ωt" colorX="#10b981" colorY="#059669" scale={1 / omega} yMax="v" />
                                    <GraphPanel title="3. 가속도 성분 ($a_x$, $a_y$)" xFunc={t => -radius * omega * omega * Math.cos(omega*t)} yFunc={t => -radius * omega * omega * Math.sin(omega*t)} xVal={acc.x} yVal={acc.y} xLabel="a_x = -a cos ωt" yLabel="a_y = -a sin ωt" colorX="#f59e0b" colorY="#d97706" scale={1 / (omega * omega)} yMax="a" />
                                </div>
                            </div>

                            {/* 미분 유도 섹션 아코디언 */}
                            <div className="bg-white border-t border-slate-100">
                                <AccordionItem id="pos" title="1단계: 위치 벡터의 정의" icon="map-pin" activeId={activeId} onToggle={handleToggle}>
                                    <div className="math-block">
                                        <p className="mb-2">원점 <MathSymbol text="O"/>를 기준으로 시간에 <MathSymbol text="t"/>에 따른 위치 벡터 <MathSymbol text="r(t)" color="#2563eb"/>는 다음과 같습니다.</p>
                                        <div className="text-xl font-black text-center py-2">r(t) = (r cos ωt, r sin ωt)</div>
                                        <p className="text-slate-500 text-xs mt-2">※ 여기서 <MathSymbol text="ω"/>는 각속도이며, <MathSymbol text="θ = ωt"/> 임을 이용합니다.</p>
                                    </div>
                                </AccordionItem>
                                <AccordionItem id="vel" title="2단계: 속도 벡터 (위치의 미분)" icon="zap" activeId={activeId} onToggle={handleToggle}>
                                    <div className="math-block">
                                        <p className="mb-2">속도 <MathSymbol text="v(t)" color="#10b981"/>는 위치 벡터를 시간 <MathSymbol text="t"/>에 대해 미분하여 구합니다.</p>
                                        <div className="text-lg font-black text-center py-2 space-y-1">
                                            <div className="text-slate-400 text-sm">v(t) = dr/dt = (d(r cos ωt)/dt, d(r sin ωt)/dt)</div>
                                            <div className="text-emerald-600 text-xl font-black font-serif italic">= (-rω sin ωt, rω cos ωt)</div>
                                        </div>
                                        <p className="text-slate-400 text-[11px] mt-2 italic font-medium leading-relaxed">결과: 속도의 크기는 v = rω 이며, 방향은 항상 궤적의 접선 방향입니다.</p>
                                    </div>
                                </AccordionItem>
                                <AccordionItem id="acc" title="3단계: 가속도 벡터 (속도의 미분)" icon="arrow-down-to-dot" activeId={activeId} onToggle={handleToggle}>
                                    <div className="math-block">
                                        <p className="mb-2">가속도 <MathSymbol text="a(t)" color="#f59e0b"/>는 속도 벡터를 한 번 더 미분하여 얻습니다.</p>
                                        <div className="text-lg font-black text-center py-2 space-y-1">
                                            <div className="text-slate-400 text-sm">a(t) = dv/dt = (-d(rω sin ωt)/dt, d(rω cos ωt)/dt)</div>
                                            <div className="text-amber-600 text-xl font-black font-serif italic">= (-rω² cos ωt, -rω² sin ωt)</div>
                                            <div className="text-rose-500 text-2xl font-black mt-3 font-serif italic">= -ω² r(t)</div>
                                        </div>
                                        <p className="text-slate-400 text-[11px] mt-2 italic font-medium leading-relaxed">결과: 가속도는 위치 벡터와 방향이 반대이며(중심 방향), 그 크기는 a = rω² = v²/r 입니다.</p>
                                    </div>
                                </AccordionItem>
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
    components.html(react_code, height=1150, scrolling=True)

if __name__ == "__main__":
    run_sim()
