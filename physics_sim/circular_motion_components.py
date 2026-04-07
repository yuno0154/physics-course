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
                const [activeView, setActiveView] = useState('sim'); // 'sim', 'practice'

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
                    const mouseY = e.clientY - rect.top;
                    
                    const dx = (mouseX / rect.width) * 400 - 200;
                    const dy = 200 - (mouseY / rect.height) * 400; // SVG y is down, math y is up
                    
                    let theta = Math.atan2(dy, dx);
                    if (theta < 0) theta += Math.PI * 2;
                    
                    // t = theta / omega
                    setTime(theta / omega);
                };

                useEffect(() => {
                    const handleMouseMove = (e) => { if (isDragging) updateTimeFromEvent(e); };
                    const handleMouseUp = () => { setIsDragging(false); };
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
                                    <polyline points={getPath(xFunc, scale)} className="graph-line" stroke={colorX} opacity="0.2" />
                                    <polyline points={getPath(yFunc, scale)} className="graph-line" stroke={colorY} opacity="0.2" />
                                    <line x1={(time/maxTime)*graphWidth} y1="0" x2={(time/maxTime)*graphWidth} y2={graphHeight} stroke="#cbd5e1" strokeWidth="1" strokeDasharray="2,2" />
                                    <circle cx={(time/maxTime)*graphWidth} cy={(graphHeight / 2) - xVal * (graphHeight / 2.5) * scale} r="5" fill={colorX} stroke="white" strokeWidth="2" />
                                    <circle cx={(time/maxTime)*graphWidth} cy={(graphHeight / 2) - yVal * (graphHeight / 2.5) * scale} r="5" fill={colorY} stroke="white" strokeWidth="2" />
                                </svg>
                            </div>
                        </div>
                    </div>
                );

                const PracticeSection = () => {
                    const [answers, setAnswers] = useState({ 
                        ox: Array(7).fill(null),
                        q1: '', q2_a: '', q2_f: '', q3: ''
                    });
                    const [submitted, setSubmitted] = useState(false);

                    const oxQuestions = [
                        "(1) 속도가 일정하다.",
                        "(2) 가속도가 일정하다.",
                        "(3) 등가속도 운동이다.",
                        "(4) 가속도의 크기는 일정하다.",
                        "(5) 가속도의 방향은 원의 중심 방향을 향하고 매순간 방향이 변한다.",
                        "(6) 구심력의 크기는 일정하다.",
                        "(7) 구심력의 방향은 일정하다."
                    ];
                    const oxCorrect = [false, false, false, true, true, true, false];

                    const handleSubmit = () => {
                        setSubmitted(true);
                    };

                    const getScore = () => {
                        let score = 0;
                        answers.ox.forEach((ans, i) => { if(ans === oxCorrect[i]) score++; });
                        if(answers.q1 === '40') score++;
                        if(answers.q2_a.includes('2.5') || answers.q2_a.includes('25')) score++; // Simplified
                        if(answers.q3 === '14') score++;
                        return score;
                    };

                    if (submitted) {
                        return (
                            <div className="space-y-6 animate-in fade-in zoom-in-95 duration-500">
                                <div className="bg-slate-900 rounded-[2rem] p-8 text-white shadow-2xl relative overflow-hidden">
                                    <div className="absolute top-0 right-0 p-8 opacity-10">
                                        <Icon name="award" size={120} />
                                    </div>
                                    <h3 className="text-3xl font-black mb-2 italic">학습 결과 리포트</h3>
                                    <p className="text-slate-400 font-bold mb-6 italic">제출이 완료되었습니다. 아래에서 상세 피드백을 확인하세요.</p>
                                    
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                                        <div className="bg-white/10 p-4 rounded-2xl border border-white/10 text-center">
                                            <p className="text-[10px] text-sky-400 font-black uppercase mb-1">최종 점수</p>
                                            <p className="text-4xl font-black">{getScore()} / 10</p>
                                        </div>
                                        <div className="bg-white/10 p-4 rounded-2xl border border-white/10 text-center">
                                            <p className="text-[10px] text-emerald-400 font-black uppercase mb-1">학습 상태</p>
                                            <p className="text-2xl font-black">{getScore() > 7 ? '우수함' : '복습 필요'}</p>
                                        </div>
                                        <button className="bg-blue-600 hover:bg-blue-500 p-4 rounded-2xl font-black transition-all flex flex-col items-center justify-center gap-1 shadow-lg shadow-blue-500/20">
                                            <Icon name="download" size={20} />
                                            <span className="text-xs">리포트(DOCX) 다운로드</span>
                                        </button>
                                    </div>

                                    <div className="space-y-4">
                                        <div className="bg-slate-800/50 p-6 rounded-3xl border border-white/5">
                                            <h4 className="font-black text-amber-400 mb-3 flex items-center gap-2">
                                                <Icon name="message-square" size={18} /> 정답 및 피드백
                                            </h4>
                                            <div className="space-y-4 text-sm text-slate-300 leading-relaxed">
                                                <div className="border-l-2 border-slate-700 pl-4 py-1">
                                                    <p className="text-white font-bold mb-1">1. OX 퀴즈 핵심 피드백</p>
                                                    <p>등속 원운동에서 **속력**은 일정하지만 **속도**는 방향이 계속 변하므로 일정하지 않습니다. 이로 인해 가속도의 '크기'는 일정하지만 '방향'은 항상 중심을 향하며 변하는 가속도 운동입니다.</p>
                                                </div>
                                                <div className="border-l-2 border-slate-700 pl-4 py-1">
                                                    <p className="text-white font-bold mb-1">2. 계산 문제 풀이 가이드</p>
                                                    <p>- 문제 1: $a_c = v^2/r = 20^2/10 = 40 m/s^2$</p>
                                                    <p>- 문제 2: $a_c = v^2/r = (5\pi)^2/10 \approx 2.5\pi^2$, $F = ma_c = 5\pi^2 N$</p>
                                                    <p>- 문제 3: $F = mr\omega^2 \rightarrow 196 = 1 \cdot 1 \cdot \omega^2 \rightarrow \omega = 14 rad/s$</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <button 
                                        onClick={() => setSubmitted(false)}
                                        className="mt-8 text-slate-500 hover:text-white text-xs font-bold underline transition-colors"
                                    >
                                        다시 풀기
                                    </button>
                                </div>
                            </div>
                        );
                    }

                    return (
                        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                            {/* OX 퀴즈 섹션 */}
                            <div className="bg-white rounded-[2.5rem] p-8 border-2 border-slate-100 shadow-xl overflow-hidden relative">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-sky-50 rounded-full -mr-16 -mt-16 opacity-50"></div>
                                <div className="flex items-center gap-4 mb-8">
                                    <div className="w-12 h-12 bg-sky-600 rounded-2xl flex items-center justify-center text-white shadow-lg">
                                        <Icon name="check-square" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-black text-slate-800">Part 1. 핵심 개념 OX 퀴즈</h3>
                                        <p className="text-xs text-slate-400 font-bold italic tracking-tight">등속 원운동의 성질을 정확히 이해하고 있는지 확인하세요.</p>
                                    </div>
                                </div>
                                <div className="grid grid-cols-1 gap-3">
                                    {oxQuestions.map((q, i) => (
                                        <div key={i} className="flex flex-col md:flex-row md:items-center justify-between p-4 bg-slate-50 rounded-2xl border border-transparent hover:border-sky-200 transition-all group">
                                            <span className="text-sm font-bold text-slate-700 group-hover:text-sky-700 transition-colors">{q}</span>
                                            <div className="flex gap-2 mt-3 md:mt-0">
                                                <button 
                                                    onClick={() => setAnswers(prev => {
                                                        const next = [...prev.ox];
                                                        next[i] = true;
                                                        return { ...prev, ox: next };
                                                    })}
                                                    className={`px-6 py-2 rounded-xl text-sm font-black transition-all ${answers.ox[i] === true ? 'bg-emerald-500 text-white shadow-lg' : 'bg-white text-slate-400 border border-slate-200 hover:bg-slate-100'}`}
                                                >O</button>
                                                <button 
                                                    onClick={() => setAnswers(prev => {
                                                        const next = [...prev.ox];
                                                        next[i] = false;
                                                        return { ...prev, ox: next };
                                                    })}
                                                    className={`px-6 py-2 rounded-xl text-sm font-black transition-all ${answers.ox[i] === false ? 'bg-rose-500 text-white shadow-lg' : 'bg-white text-slate-400 border border-slate-200 hover:bg-slate-100'}`}
                                                >X</button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* 계산 문제 섹션 */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="bg-white p-8 rounded-[2.5rem] border-2 border-slate-100 shadow-xl space-y-6">
                                    <div className="flex items-center gap-3">
                                        <span className="w-8 h-8 rounded-xl bg-blue-600 text-white flex items-center justify-center text-xs font-black">P1</span>
                                        <h4 className="font-bold text-slate-800">구심 가속도 계산</h4>
                                    </div>
                                    <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100 italic text-[13px] leading-relaxed text-slate-600 font-medium">
                                        반지름이 <span className="text-blue-600 font-black">10.0m</span>인 원 궤도를 따라 <span className="text-blue-600 font-black">20.0m/s</span>의 일정한 속력으로 운동하는 물체의 구심 가속도는 몇 $m/s^2$인가?
                                    </div>
                                    <div className="relative">
                                        <input 
                                            type="text" 
                                            value={answers.q1}
                                            onChange={e => setAnswers(prev => ({ ...prev, q1: e.target.value }))}
                                            className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-6 py-4 text-lg font-black text-blue-700 outline-none focus:border-blue-400 transition-all placeholder:text-slate-300"
                                            placeholder="값 입력..."
                                        />
                                        <span className="absolute right-6 top-1/2 -translate-y-1/2 text-slate-400 font-black">$m/s^2$</span>
                                    </div>
                                </div>

                                <div className="bg-white p-8 rounded-[2.5rem] border-2 border-slate-100 shadow-xl space-y-6">
                                    <div className="flex items-center gap-3">
                                        <span className="w-8 h-8 rounded-xl bg-emerald-500 text-white flex items-center justify-center text-xs font-black">P2</span>
                                        <h4 className="font-bold text-slate-800">구심력과 질량</h4>
                                    </div>
                                    <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100 italic text-[13px] leading-relaxed text-slate-600 font-medium">
                                        길이가 <span className="text-emerald-500 font-black">1m</span>인 줄 끝에 질량이 <span className="text-emerald-500 font-black">1kg</span>인 추를 매달고 줄에 <span className="text-rose-500 font-black">196N</span>의 힘을 작용하여 등속 원운동을 시킬 때, 각속도는 몇 $rad/s$인가?
                                    </div>
                                    <div className="relative">
                                        <input 
                                            type="text" 
                                            value={answers.q3}
                                            onChange={e => setAnswers(prev => ({ ...prev, q3: e.target.value }))}
                                            className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-6 py-4 text-lg font-black text-emerald-700 outline-none focus:border-emerald-400 transition-all placeholder:text-slate-300"
                                            placeholder="값 입력..."
                                        />
                                        <span className="absolute right-6 top-1/2 -translate-y-1/2 text-slate-400 font-black">$rad/s$</span>
                                    </div>
                                </div>
                            </div>

                            <button 
                                onClick={handleSubmit}
                                className="w-full py-6 bg-slate-900 hover:bg-slate-800 text-white rounded-[2rem] text-xl font-black shadow-2xl transition-all active:scale-[0.98] flex items-center justify-center gap-3"
                            >
                                <Icon name="send" size={24} />
                                학습 활동 결과 제출하기
                            </button>
                        </div>
                    );
                };

                const handleToggle = (id) => {
                    setActiveId(activeId === id ? null : id);
                };

                return (
                    <div className="flex flex-col items-center bg-transparent min-h-screen p-1 text-slate-800">
                        <div className="w-full max-w-7xl min-h-[850px] rounded-[32px] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.15)] border border-slate-200 overflow-hidden bg-white mb-8 transition-all flex">
                            
                            <div className="w-[100px] flex-shrink-0 bg-slate-900 flex flex-col items-center py-10 gap-8 border-r border-white/5">
                                <button 
                                    onClick={() => setActiveView('sim')}
                                    className={`flex flex-col items-center justify-center p-4 rounded-2xl transition-all duration-300 ${activeView === 'sim' ? 'bg-blue-600 text-white shadow-xl shadow-blue-500/20' : 'text-slate-500 hover:text-slate-400'}`}
                                >
                                    <Icon name="activity" size={24} />
                                    <span className="text-[10px] font-black uppercase mt-2 tracking-tighter">주제 분석 2</span>
                                </button>
                                <button 
                                    onClick={() => setActiveView('practice')}
                                    className={`flex flex-col items-center justify-center p-4 rounded-2xl transition-all duration-300 ${activeView === 'practice' ? 'bg-amber-500 text-white shadow-xl shadow-amber-500/20' : 'text-slate-500 hover:text-slate-400'}`}
                                >
                                    <Icon name="clipboard-list" size={24} />
                                    <span className="text-[10px] font-black uppercase mt-2 tracking-tighter">연습 문제</span>
                                </button>
                                <div className="mt-auto pb-6">
                                    <Icon name="cpu" size={20} className="text-slate-700" />
                                </div>
                            </div>

                            <div className="flex-1 flex flex-col bg-slate-50/30 overflow-hidden">
                                {activeView === 'sim' ? (
                                    <>
                                        <div className="flex items-center justify-between px-8 py-4 bg-slate-900 text-white border-b border-slate-800">
                                            <div className="flex items-center gap-6">
                                                <button onClick={() => setIsManual(!isManual)} className={`px-4 py-2 rounded-xl text-[10px] font-black transition-all border-2 ${isManual ? 'bg-amber-500 border-amber-500 text-white shadow-lg shadow-amber-200' : 'bg-transparent border-slate-700 text-slate-400 hover:border-slate-500'}`}>
                                                    {isManual ? 'MANUAL' : 'AUTO'}
                                                </button>
                                                <button onClick={() => setIsPlaying(!isPlaying)} className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${isPlaying && !isManual ? 'bg-rose-500 hover:bg-rose-600' : 'bg-emerald-500 hover:bg-emerald-600'}`}>
                                                    <Icon name={isPlaying && !isManual ? "pause" : "play"} size={24} className="text-white" />
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
                                                    <input type="range" min="0.5" max="1.5" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-full h-1 accent-sky-500 text-slate-900" />
                                                </div>
                                                <div className="w-44 space-y-1">
                                                    <p className="text-[10px] text-slate-400 font-black uppercase">각속도 (ω)</p>
                                                    <input type="range" min="0.5" max="2.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full h-1 accent-amber-500" />
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex flex-col lg:flex-row divide-x divide-slate-100 min-h-[640px] bg-white">
                                            <div className="lg:w-[450px] bg-slate-50 flex flex-col items-center justify-center p-8 relative border-r">
                                                <div className="absolute top-6 left-6 flex flex-col gap-2 z-10 w-[140px]">
                                                    <button onClick={()=>setShowPos(!showPos)} className={`w-full py-1.5 rounded-lg text-[10px] font-black border-2 transition-all ${showPos ? 'bg-blue-600 border-blue-600 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>위치(r) 벡터 표시</button>
                                                    <button onClick={()=>setShowVel(!showVel)} className={`w-full py-1.5 rounded-lg text-[10px] font-black border-2 transition-all ${showVel ? 'bg-emerald-500 border-emerald-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>속도(v) 벡터 표시</button>
                                                    <button onClick={()=>setShowComp(!showComp)} className={`w-full py-1.5 rounded-lg text-[10px] font-black border-2 transition-all ${showComp ? 'bg-teal-500 border-teal-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>속도 성분 (vx, vy)</button>
                                                    <button onClick={()=>setShowAcc(!showAcc)} className={`w-full py-1.5 rounded-lg text-[10px] font-black border-2 transition-all ${showAcc ? 'bg-rose-500 border-rose-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>가속도(a) 벡터 표시</button>
                                                    <button onClick={()=>setShowAccComp(!showAccComp)} className={`w-full py-1.5 rounded-lg text-[10px] font-black border-2 transition-all ${showAccComp ? 'bg-amber-500 border-amber-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>가속도 성분 (ax, ay)</button>
                                                </div>
                                                <svg ref={svgRef} viewBox="0 0 400 400" className={`w-full h-full max-w-[340px] select-none ${isManual ? 'cursor-move' : ''}`} onMouseDown={handleMouseDown}>
                                                    <defs>
                                                        <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto" markerUnits="userSpaceOnUse">
                                                            <path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" />
                                                        </marker>
                                                        <marker id="arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto" markerUnits="userSpaceOnUse">
                                                            <path d="M 0 2 L 10 5 L 0 8 Z" fill="#f59e0b" />
                                                        </marker>
                                                        <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto" markerUnits="userSpaceOnUse">
                                                            <path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" />
                                                        </marker>
                                                        <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto" markerUnits="userSpaceOnUse">
                                                            <path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" />
                                                        </marker>
                                                    </defs>

                                                    <line x1="0" y1="200" x2="400" y2="200" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="4,4" />
                                                    <line x1="200" y1="0" x2="200" y2="400" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="4,4" />
                                                    <circle cx="200" cy="200" r={radius * 120} fill="none" stroke="#e2e8f0" strokeWidth="2" />

                                                    {showPos && (
                                                        <g>
                                                            <line x1="200" y1="200" x2={200 + pos.x * 120} y2={200 - pos.y * 120} stroke="#3b82f6" strokeWidth="3" markerEnd="url(#arrow-blue)" />
                                                            <line x1="200" y1="200" x2={200 + pos.x * 120} y2={200} stroke="#3b82f6" strokeWidth="4" strokeLinecap="round" opacity="0.3" />
                                                            <line x1="200" y1="200" x2="200" y2={200 - pos.y * 120} stroke="#f43f5e" strokeWidth="4" strokeLinecap="round" opacity="0.3" />
                                                        </g>
                                                    )}
                                                    {showAcc && (
                                                        <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120 + acc.x * 80} y2={200 - pos.y * 120 - acc.y * 80} stroke="#f43f5e" strokeWidth="4" markerEnd="url(#arrow-red)" />
                                                    )}
                                                    {showAccComp && (
                                                        <g opacity="0.8">
                                                            <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120 + acc.x * 80} y2={200 - pos.y * 120} stroke="#f59e0b" strokeWidth="6" strokeLinecap="round" />
                                                            <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120} y2={200 - pos.y * 120 - acc.y * 80} stroke="#d97706" strokeWidth="6" strokeLinecap="round" />
                                                            <text x={200 + pos.x * 120 + acc.x * 80} y={200 - pos.y * 120 - 10} className="fill-amber-600 text-[11px] font-black italic">ax</text>
                                                            <text x={200 + pos.x * 120 + 10} y={200 - pos.y * 120 - acc.y * 80} className="fill-amber-800 text-[11px] font-black italic">ay</text>
                                                        </g>
                                                    )}
                                                    {showComp && (
                                                        <g opacity="0.9">
                                                            <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120 + vel.x * 110} y2={200 - pos.y * 120} stroke="#10b981" strokeWidth="7" strokeLinecap="round" />
                                                            <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120} y2={200 - pos.y * 120 - vel.y * 110} stroke="#059669" strokeWidth="7" strokeLinecap="round" />
                                                            <text x={200 + pos.x * 120 + vel.x * 110} y={200 - pos.y * 120 - 12} className="fill-emerald-600 text-[12px] font-black italic">vx</text>
                                                            <text x={200 + pos.x * 120 + 12} y={200 - pos.y * 120 - vel.y * 110} className="fill-emerald-800 text-[12px] font-black italic">vy</text>
                                                        </g>
                                                    )}
                                                    {showVel && (
                                                        <line x1={200 + pos.x * 120} y1={200 - pos.y * 120} x2={200 + pos.x * 120 + vel.x * 110} y2={200 - pos.y * 120 - vel.y * 110} stroke="#10b981" strokeWidth="4" markerEnd="url(#arrow-green)" />
                                                    )}
                                                    <circle cx={200 + pos.x * 120} cy={200 - pos.y * 120} r="10" fill="#0f172a" stroke="white" strokeWidth="4" />
                                                </svg>
                                                {isManual && <div className="absolute bottom-8 bg-amber-500 text-white px-6 py-2 rounded-full text-xs font-black animate-pulse shadow-xl">드래그하여 직접 조작하세요!</div>}
                                            </div>
                                            <div className="flex-1 p-6 space-y-4 max-h-[700px] overflow-y-auto no-scrollbar bg-white shadow-inner">
                                                <GraphPanel title="1. 위치 성분 ($x$, $y$)" xFunc={t => radius * Math.cos(omega*t)} yFunc={t => radius * Math.sin(omega*t)} xVal={pos.x} yVal={pos.y} xLabel="x = r cos ωt" yLabel="y = r sin ωt" colorX="#3b82f6" colorY="#f43f5e" yMax="r" />
                                                <div className="space-y-4 pt-4 pb-4">
                                                    <div className="flex items-center gap-2 border-l-4 border-emerald-500 pl-3">
                                                        <h3 className="font-black text-slate-800 text-sm italic">2: 속도 성분 ($v_x, v_y$)</h3>
                                                    </div>
                                                    <GraphPanel title="2. 속도 성분 ($v_x$, $v_y$)" xFunc={t => -radius * omega * Math.sin(omega*t)} yFunc={t => radius * omega * Math.cos(omega*t)} xVal={vel.x} yVal={vel.y} xLabel="vx = -rω sin ωt" yLabel="vy = rω cos ωt" colorX="#10b981" colorY="#059669" scale={1/omega} yMax="rω" />
                                                </div>
                                                <GraphPanel title="3. 가속도 성분 ($a_x$, $a_y$)" xFunc={t => -radius * omega * omega * Math.cos(omega*t)} yFunc={t => -radius * omega * omega * Math.sin(omega*t)} xVal={acc.x} yVal={acc.y} xLabel="ax = -rω² cos ωt" yLabel="ay = -rω² sin ωt" colorX="#f59e0b" colorY="#d97706" scale={1/(omega*omega)} yMax="rω²" />
                                            </div>
                                        </div>

                                        <div className="bg-white border-t border-slate-100 mt-0">
                                            <AccordionItem id="pos" title="1단계: 위치 벡터의 정의" icon="map-pin" activeId={activeId} onToggle={handleToggle}>
                                                <div className="math-block">
                                                    <p className="mb-2">원점 <MathSymbol text="O"/>를 기준으로 시간에 <MathSymbol text="t"/>에 따른 위치 벡터 <MathSymbol text="r" isVector={true} color="#2563eb"/>는 다음과 같습니다.</p>
                                                    <div className="text-xl font-black text-center py-2 text-slate-800 font-serif">r(t) = (r cos ωt, r sin ωt)</div>
                                                    <p className="text-slate-500 text-xs mt-2 italic">※ 여기서 <MathSymbol text="ω"/>는 각속도이며, <MathSymbol text="θ = ωt"/> 임을 이용합니다.</p>
                                                </div>
                                            </AccordionItem>
                                            <AccordionItem id="vel" title="2단계: 속도 벡터 (위치의 미분)" icon="zap" activeId={activeId} onToggle={handleToggle}>
                                                <div className="math-block">
                                                    <p className="mb-2">속도 <MathSymbol text="v" isVector={true} color="#10b981"/>는 위치 벡터를 시간 <MathSymbol text="t"/>에 대해 미분하여 구합니다.</p>
                                                    <div className="text-lg font-black text-center py-2 space-y-1">
                                                        <div className="text-slate-400 text-sm">v(t) = dr/dt = (d(r cos ωt)/dt, d(r sin ωt)/dt)</div>
                                                        <div className="text-emerald-600 text-xl font-black font-serif italic">= (-rω sin ωt, rω cos ωt)</div>
                                                    </div>
                                                    <p className="text-slate-400 text-[11px] mt-2 italic font-medium leading-relaxed">결과: 속도의 크기는 v = rω 이며, 방향은 항상 궤적의 접선 방향입니다.</p>
                                                </div>
                                            </AccordionItem>
                                            <AccordionItem id="acc" title="3단계: 가속도 벡터 (속도의 미분)" icon="arrow-down-to-dot" activeId={activeId} onToggle={handleToggle}>
                                                <div className="math-block">
                                                    <p className="mb-2">가속도 <MathSymbol text="a" isVector={true} color="#f59e0b"/>는 속도 벡터를 한 번 더 미분하여 얻습니다.</p>
                                                    <div className="text-lg font-black text-center py-2 space-y-1 text-slate-800">
                                                        <div className="text-slate-400 text-sm italic underline">a(t) = dv/dt = (-d(rω sin ωt)/dt, d(rω cos ωt)/dt)</div>
                                                        <div className="text-amber-600 text-xl font-black font-serif italic">= (-rω² cos ωt, -rω² sin ωt)</div>
                                                        <div className="text-rose-500 text-2xl font-black mt-3 font-serif italic tracking-tighter">= -ω² r(t)</div>
                                                    </div>
                                                    <p className="text-slate-400 text-[11px] mt-2 italic font-medium leading-relaxed">결과: 가속도는 위치 벡터와 방향이 반대이며(중심 방향), 그 크기는 a = rω² = v²/r 입니다.</p>
                                                </div>
                                            </AccordionItem>
                                        </div>
                                    </>
                                ) : (
                                    <div className="flex-1 bg-slate-50 p-12 overflow-y-auto no-scrollbar">
                                        <div className="max-w-4xl mx-auto space-y-12">
                                            <div className="flex items-center justify-between">
                                                <div className="flex items-center gap-6">
                                                    <div className="w-16 h-16 bg-slate-900 rounded-[1.5rem] flex items-center justify-center text-white shadow-2xl">
                                                        <Icon name="clipboard-list" size={32} />
                                                    </div>
                                                    <div>
                                                        <h2 className="text-4xl font-black text-slate-800 tracking-tighter">실전 연습 문제 (Physics Lab)</h2>
                                                        <p className="text-slate-400 font-bold italic text-sm">등속 원운동의 성분 분석과 관련된 핵심 문제들을 해결해 보세요.</p>
                                                    </div>
                                                </div>
                                                <div className="px-6 py-2 bg-white rounded-full border border-slate-200 shadow-sm text-xs font-black text-slate-400 tracking-widest uppercase">
                                                    Assessment Mode
                                                </div>
                                            </div>
                                            <PracticeSection />
                                        </div>
                                    </div>
                                )}
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
