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
            .axis-line { stroke: #cbd5e1; stroke-width: 1.5; }
            .graph-line { fill: none; stroke-width: 2; vector-effect: non-scaling-stroke; }
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

            const MathSymbol = ({ text, color = "#1e293b", isVector = false }) => (
                <span className="inline-flex flex-col items-center leading-none px-0.5" style={{ color }}>
                    {isVector && <span className="text-[10px] scale-x-125">→</span>}
                    <span className="math-font leading-none">{text}</span>
                </span>
            );

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
                const [isManual, setIsManual] = useState(false);
                const [omega, setOmega] = useState(1.0); 
                const [radius, setRadius] = useState(1.0);
                const [activeId, setActiveId] = useState(null);

                const [showPos, setShowPos] = useState(true);
                const [showVel, setShowVel] = useState(true);
                const [showAcc, setShowAcc] = useState(true);
                const [showComp, setShowComp] = useState(true);
                const [showAccComp, setShowAccComp] = useState(false);

                const [isDragging, setIsDragging] = useState(false);
                const svgRef = useRef(null);

                const maxTime = 12; 
                const samples = 200; 

                useEffect(() => {
                    let frame;
                    if (isPlaying && !isManual) {
                        const tick = () => {
                            setTime(t => (t + 0.05) % maxTime);
                            frame = requestAnimationFrame(tick);
                        };
                        frame = requestAnimationFrame(tick);
                    }
                    return () => cancelAnimationFrame(frame);
                }, [isPlaying, isManual]);

                const wt = (omega * time);
                const pos = { x: radius * Math.cos(wt), y: radius * Math.sin(wt) };
                const vel = { x: -radius * omega * Math.sin(wt), y: radius * omega * Math.cos(wt) };
                const acc = { x: -radius * omega * omega * Math.cos(wt), y: -radius * omega * omega * Math.sin(wt) };

                const graphWidth = 400;
                const graphHeight = 110;

                const handleMouseDown = (e) => {
                    if (!isManual) return;
                    setIsDragging(true);
                    updateTimeFromEvent(e);
                };

                const updateTimeFromEvent = (e) => {
                    if (!svgRef.current) return;
                    const rect = svgRef.current.getBoundingClientRect();
                    const mouseX = e.clientX - rect.left;
                    const dx = (mouseX / rect.width) * 400 - 200;
                    const dy = 200 - (e.clientY - rect.top) / rect.height * 400;
                    let theta = Math.atan2(dy, dx);
                    if (theta < 0) theta += Math.PI * 2;
                    setTime(theta / omega);
                };

                useEffect(() => {
                    const handleMouseMove = (e) => { if (isDragging) updateTimeFromEvent(e); };
                    const handleMouseUp = () => setIsDragging(false);
                    if (isDragging) {
                        window.addEventListener('mousemove', handleMouseMove);
                        window.addEventListener('mouseup', handleMouseUp);
                    }
                    return () => {
                        window.removeEventListener('mousemove', handleMouseMove);
                        window.removeEventListener('mouseup', handleMouseUp);
                    };
                }, [isDragging, omega]);

                const getPath = (func, scale = 1) => {
                    let pts = [];
                    for (let i = 0; i < samples; i++) {
                        const t = (i / samples) * maxTime;
                        const val = func(t);
                        const x = (t / maxTime) * graphWidth;
                        const y = (graphHeight / 2) - val * (graphHeight / 2.5) * scale;
                        pts.push(`${x},${y}`);
                    }
                    return pts.join(" ");
                };

                const GraphPanel = ({ title, xFunc, yFunc, xVal, yVal, xLabel, yLabel, colorX, colorY, scale = 1, yMax="1.0" }) => (
                    <div className="bg-slate-50/50 p-6 rounded-3xl border border-slate-100 space-y-3">
                        <div className="flex justify-between items-center mb-1">
                            <h4 className="text-[11px] font-black text-slate-500 tracking-widest uppercase">{title}</h4>
                            <div className="flex gap-4">
                                <div className="flex items-center gap-1.5 font-bold text-[11px] text-slate-600">
                                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: colorX }}></div> {xLabel}
                                </div>
                                <div className="flex items-center gap-1.5 font-bold text-[11px] text-slate-600">
                                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: colorY }}></div> {yLabel}
                                </div>
                            </div>
                        </div>
                        <div className="relative h-[120px] w-full bg-white rounded-2xl border border-slate-100 overflow-hidden flex">
                            <div className="w-10 border-r border-slate-50 flex flex-col justify-between py-2 text-[9px] font-black text-slate-400 text-center bg-slate-50/30">
                                <span>{yMax}</span><span>0</span><span>-{yMax}</span>
                            </div>
                            <div className="flex-1 relative">
                                <svg viewBox={`0 0 ${graphWidth} ${graphHeight}`} className="w-full h-full" preserveAspectRatio="none">
                                    <line x1="0" y1={graphHeight/2} x2={graphWidth} y2={graphHeight/2} stroke="#f1f5f9" strokeWidth="2" />
                                    <polyline points={getPath(xFunc, scale)} stroke={colorX} fill="none" strokeWidth="2.5" opacity="0.4" />
                                    <polyline points={getPath(yFunc, scale)} stroke={colorY} fill="none" strokeWidth="2.5" opacity="0.4" />
                                    <line x1={(time/maxTime)*graphWidth} y1="0" x2={(time/maxTime)*graphWidth} y2={graphHeight} stroke="#94a3b8" strokeWidth="1.5" strokeDasharray="4,2" />
                                    <circle cx={(time/maxTime)*graphWidth} cy={(graphHeight/2)-xVal*(graphHeight/2.5)*scale} r="5" fill={colorX} stroke="white" strokeWidth="2.5" />
                                    <circle cx={(time/maxTime)*graphWidth} cy={(graphHeight/2)-yVal*(graphHeight/2.5)*scale} r="5" fill={colorY} stroke="white" strokeWidth="2.5" />
                                </svg>
                            </div>
                        </div>
                    </div>
                );

                const handleToggle = (id) => setActiveId(activeId === id ? null : id);

                return (
                    <div className="flex flex-col items-center bg-white rounded-[32px] shadow-2xl overflow-hidden border border-slate-200 font-sans tracking-tight">
                        <div className="w-full flex flex-col md:flex-row items-center justify-between px-10 py-8 bg-slate-900 text-white gap-8 shrink-0">
                            <div className="flex items-center gap-8">
                                <button onClick={() => setIsManual(!isManual)} className={`px-5 py-3 rounded-xl text-xs font-black transition-all border-2 ${isManual ? 'bg-amber-500 border-amber-500 shadow-lg shadow-amber-500/20' : 'border-slate-700 text-slate-400 hover:border-slate-500'}`}>
                                    {isManual ? '수동 조절' : '자동 시뮬레이션'}
                                </button>
                                <button onClick={() => setIsPlaying(!isPlaying)} className={`w-14 h-14 rounded-full flex items-center justify-center transition-all ${isPlaying && !isManual ? 'bg-rose-500 hover:bg-rose-600 shadow-xl' : 'bg-emerald-500 hover:bg-emerald-600 shadow-xl'}`}>
                                    <Icon name={isPlaying && !isManual ? "pause" : "play"} size={28} className="text-white" />
                                </button>
                                <div className="space-y-1">
                                    <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest">실시간 변수</p>
                                    <div className="flex gap-6 italic">
                                        <span className="text-2xl font-black text-sky-400">t = {time.toFixed(2)}s</span>
                                        <span className="text-2xl font-black text-amber-500">θ = {wt.toFixed(2)}rad</span>
                                    </div>
                                </div>
                            </div>
                            <div className="flex gap-10">
                                <div className="w-40 lg:w-56 space-y-2">
                                    <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest flex justify-between">반지름 <span>{radius.toFixed(1)}m</span></p>
                                    <input type="range" min="0.5" max="1.5" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-full h-1 accent-sky-500" />
                                </div>
                                <div className="w-40 lg:w-56 space-y-2">
                                    <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest flex justify-between">각속도(ω) <span>{omega.toFixed(1)} rad/s</span></p>
                                    <input type="range" min="0.5" max="2.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full h-1 accent-amber-500" />
                                </div>
                            </div>
                        </div>

                        <div className="w-full flex flex-col flex-1 divide-y divide-slate-100">
                            {/* Top Section: Simulation & Graphs (50:50) */}
                            <div className="w-full flex flex-col lg:flex-row divide-x divide-slate-100 bg-slate-50/20">
                                {/* Left: Simulation Panel */}
                                <div className="lg:w-1/2 p-8 lg:p-12 flex flex-col items-center bg-slate-50/50 relative overflow-hidden min-h-[650px]">
                                    {/* Control Buttons - Separated from SVG area */}
                                    <div className="w-full mb-10 flex flex-wrap gap-3 justify-center z-20">
                                        <button onClick={()=>setShowPos(!showPos)} className={`px-4 py-2.5 rounded-xl text-[11px] font-black border-2 transition-all ${showPos ? 'bg-blue-600 border-blue-600 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400 hover:border-blue-200'}`}>위치 벡터</button>
                                        <button onClick={()=>setShowVel(!showVel)} className={`px-4 py-2.5 rounded-xl text-[11px] font-black border-2 transition-all ${showVel ? 'bg-emerald-500 border-emerald-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>속도 벡터</button>
                                        <button onClick={()=>setShowComp(!showComp)} className={`px-4 py-2.5 rounded-xl text-[11px] font-black border-2 transition-all ${showComp ? 'bg-teal-500 border-teal-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>속도 성분</button>
                                        <button onClick={()=>setShowAcc(!showAcc)} className={`px-4 py-2.5 rounded-xl text-[11px] font-black border-2 transition-all ${showAcc ? 'bg-rose-500 border-rose-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>가속도 벡터</button>
                                        <button onClick={()=>setShowAccComp(!showAccComp)} className={`px-4 py-2.5 rounded-xl text-[11px] font-black border-2 transition-all ${showAccComp ? 'bg-amber-500 border-amber-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>가속도 성분</button>
                                    </div>
                                    
                                    <div className="flex-1 flex items-center justify-center w-full">
                                        <svg ref={svgRef} viewBox="0 0 400 400" className={`w-full max-w-[420px] select-none ${isManual ? 'cursor-all-scroll' : ''}`} onMouseDown={handleMouseDown}>
                                            <defs>
                                                <marker id="arr-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#3b82f6"/></marker>
                                                <marker id="arr-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#10b981"/></marker>
                                                <marker id="arr-r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#f43f5e"/></marker>
                                            </defs>

                                            {/* Trajectory circle */}
                                            <circle cx="200" cy="200" r={radius*120} fill="none" stroke="#e2e8f0" strokeWidth="4" strokeDasharray="6,4" opacity="0.8" />
                                            <circle cx="200" cy="200" r={radius*120} fill="none" stroke="#cbd5e1" strokeWidth="1.5" />
                                            
                                            <line x1="0" y1="200" x2="400" y2="200" stroke="#f1f5f9" strokeWidth="2" />
                                            <line x1="200" y1="0" x2="200" y2="400" stroke="#f1f5f9" strokeWidth="2" />
                                            
                                            {/* Position Vector & Components */}
                                            {showPos && (
                                                <g>
                                                    <line x1="200" y1="200" x2={200+pos.x*120} y2="200" stroke="#3b82f6" strokeWidth="6" strokeLinecap="round" opacity="0.3" />
                                                    <line x1="200" y1="200" x2="200" y2={200-pos.y*120} stroke="#a855f7" strokeWidth="6" strokeLinecap="round" opacity="0.3" />
                                                    <line x1="200" y1="200" x2={200+pos.x*120} y2={200-pos.y*120} stroke="#3b82f6" strokeWidth="3" markerEnd="url(#arr-b)" />
                                                </g>
                                            )}
                                            
                                            {showVel && <line x1={200+pos.x*120} y1={200-pos.y*120} x2={200+pos.x*120+vel.x*100} y2={200-pos.y*120-vel.y*100} stroke="#10b981" strokeWidth="3" markerEnd="url(#arr-g)" />}
                                            {showAcc && <line x1={200+pos.x*120} y1={200-pos.y*120} x2={200+pos.x*120+acc.x*80} y2={200-pos.y*120-acc.y*80} stroke="#f43f5e" strokeWidth="3" markerEnd="url(#arr-r)" />}
                                            
                                            {showComp && (
                                                <g opacity="0.7">
                                                    <line x1={200+pos.x*120} y1={200-pos.y*120} x2={200+pos.x*120+vel.x*100} y2={200-pos.y*120} stroke="#10b981" strokeWidth="7" strokeLinecap="round" />
                                                    <line x1={200+pos.x*120} y1={200-pos.y*120} x2={200+pos.x*120} y2={200-pos.y*120-vel.y*100} stroke="#f59e0b" strokeWidth="7" strokeLinecap="round" />
                                                </g>
                                            )}
                                            {showAccComp && (
                                                <g opacity="0.7">
                                                    <line x1={200+pos.x*120} y1={200-pos.y*120} x2={200+pos.x*120+acc.x*80} y2={200-pos.y*120} stroke="#f43f5e" strokeWidth="7" strokeLinecap="round" />
                                                    <line x1={200+pos.x*120} y1={200-pos.y*120} x2={200+pos.x*120} y2={200-pos.y*120-acc.y*80} stroke="#06b6d4" strokeWidth="7" strokeLinecap="round" />
                                                </g>
                                            )}
                                            <circle cx={200+pos.x*120} cy={200-pos.y*120} r="12" fill="#0f172a" stroke="white" strokeWidth="3" />
                                        </svg>
                                    </div>
                                    {isManual && <div className="absolute bottom-10 bg-amber-500 text-white px-8 py-3 rounded-full text-[11px] font-black shadow-xl animate-bounce">원을 드래그하여 위치를 조절하세요</div>}
                                </div>
                                
                                {/* Right: Graphs Panel */}
                                <div className="flex-1 lg:w-1/2 p-8 lg:p-12 space-y-6 overflow-y-auto no-scrollbar bg-white">
                                    <div className="space-y-6">
                                        <GraphPanel 
                                            title="위치 성분 분석 (r)" 
                                            xFunc={(t) => radius * Math.cos(omega * t)}
                                            yFunc={(t) => radius * Math.sin(omega * t)}
                                            xVal={pos.x}
                                            yVal={pos.y}
                                            xLabel="x = r cos ωt"
                                            yLabel="y = r sin ωt"
                                            colorX="#3b82f6"
                                            colorY="#a855f7"
                                            scale={1.0}
                                            yMax={radius.toFixed(1)}
                                        />
                                        <GraphPanel 
                                            title="속도 성분 분석 (v)" 
                                            xFunc={(t) => -radius * omega * Math.sin(omega * t)}
                                            yFunc={(t) => radius * omega * Math.cos(omega * t)}
                                            xVal={vel.x}
                                            yVal={vel.y}
                                            xLabel="vx = -v sin ωt"
                                            yLabel="vy = v cos ωt"
                                            colorX="#10b981"
                                            colorY="#f59e0b"
                                            scale={1/omega}
                                            yMax={(radius*omega).toFixed(1)}
                                        />
                                        <GraphPanel 
                                            title="가속도 성분 분석 (a)" 
                                            xFunc={(t) => -radius * omega * omega * Math.cos(omega * t)}
                                            yFunc={(t) => -radius * omega * omega * Math.sin(omega * t)}
                                            xVal={acc.x}
                                            yVal={acc.y}
                                            xLabel="ax = -a cos ωt"
                                            yLabel="ay = -a sin ωt"
                                            colorX="#f43f5e"
                                            colorY="#06b6d4"
                                            scale={1/(omega*omega)}
                                            yMax={(radius*omega*omega).toFixed(1)}
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* Bottom Section: Accordion Steps */}
                            <div className="w-full p-8 lg:p-12 bg-white">
                                <div className="max-w-4xl mx-auto space-y-2 border-t border-slate-100 pt-8">
                                    <h3 className="text-sm font-black text-slate-400 mb-6 uppercase tracking-widest">단계별 물리 개념 분석</h3>
                                    <AccordionItem id="pos" title="1단계: 위치 벡터의 정의" icon="map-pin" activeId={activeId} onToggle={handleToggle}>
                                        <div className="math-block">
                                            <p className="mb-3">원점 <MathSymbol text="O"/>를 기준으로 시간에 <MathSymbol text="t"/>에 따른 위치 벡터 <MathSymbol text="r" isVector={true} color="#2563eb"/>는 다음과 같습니다.</p>
                                            <div className="text-2xl font-black text-center py-4 text-slate-800 font-serif whitespace-nowrap overflow-x-auto no-scrollbar">r(t) = (r cos ωt, r sin ωt)</div>
                                            <p className="text-slate-500 text-[11px] mt-2 italic font-medium">※ 여기서 <MathSymbol text="ω"/>는 각속도이며, 회전각 <MathSymbol text="θ = ωt"/> 임을 이용합니다.</p>
                                        </div>
                                    </AccordionItem>
                                    <AccordionItem id="vel" title="2단계: 속도 벡터 (위치의 미분)" icon="zap" activeId={activeId} onToggle={handleToggle}>
                                        <div className="math-block">
                                            <p className="mb-3">속도 <MathSymbol text="v" isVector={true} color="#10b981"/>는 위치 벡터를 시간 <MathSymbol text="t"/>에 대해 미분하여 구합니다.</p>
                                            <div className="text-xl font-black text-center py-4 space-y-2 overflow-x-auto no-scrollbar">
                                                <div className="text-slate-400 text-sm whitespace-nowrap">v(t) = dr/dt = (d(r cos ωt)/dt, d(r sin ωt)/dt)</div>
                                                <div className="text-emerald-600 text-2xl font-black font-serif italic whitespace-nowrap">= (-rω sin ωt, rω cos ωt)</div>
                                            </div>
                                            <p className="text-slate-400 text-[11px] mt-2 italic font-medium leading-relaxed">결과: 속도의 크기는 v = rω 이며, 방향은 항상 원 궤적의 접선 방향입니다.</p>
                                        </div>
                                    </AccordionItem>
                                    <AccordionItem id="acc" title="3단계: 가속도 벡터 (속도의 미분)" icon="activity" activeId={activeId} onToggle={handleToggle}>
                                        <div className="math-block">
                                            <p className="mb-3">가속도 <MathSymbol text="a" isVector={true} color="#f43f5e"/>는 속도 벡터를 한 번 더 시간 <MathSymbol text="t"/>에 대해 미분합니다.</p>
                                            <div className="text-xl font-black text-center py-4 space-y-2 overflow-x-auto no-scrollbar">
                                                <div className="text-slate-400 text-sm whitespace-nowrap">a(t) = dv/dt = (-rω² cos ωt, -rω² sin ωt)</div>
                                                <div className="text-rose-600 text-2xl font-black font-serif italic whitespace-nowrap">= -ω² (r cos ωt, r sin ωt) = -ω² r(t)</div>
                                            </div>
                                            <p className="text-slate-400 text-[11px] mt-2 italic font-medium leading-relaxed">결과: 가속도의 방향은 위치 벡터와 반대인 **원의 중심**을 향합니다(구심 가속도).</p>
                                        </div>
                                    </AccordionItem>
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

    # Streamlit 컴포넌트로 HTML 삽입 (높이 확대)
    components.html(react_code, height=1800, scrolling=True)

if __name__ == "__main__":
    run_sim()
