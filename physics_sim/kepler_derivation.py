import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 수학적 유도", layout="wide")
    
    st.title("📐 케플러 제3법칙의 수학적 유도")
    st.markdown("""
    뉴턴의 만유인력 법칙과 원운동의 구심력을 결합하여 **조화의 법칙($T^2 \\propto r^3$)**이 도출되는 과정을 단계별로 확인해 보세요.
    각 유도 단계의 핵심 수식을 직접 추측해 본 뒤, [수식 확인] 버튼을 눌러 정답을 맞춰보세요.
    """)

    react_code = r"""
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
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            .accordion-content { 
                max-height: 0; 
                overflow: hidden; 
                transition: max-height 0.4s ease-out, opacity 0.3s ease; 
                opacity: 0;
            }
            .accordion-content.open { 
                max-height: 1000px; 
                opacity: 1;
                padding-bottom: 2rem;
            }
            .math-answer { transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => { if (window.lucide) window.lucide.createIcons(); }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const MathBox = ({ formula, className }) => {
                const ref = useRef(null);
                useEffect(() => {
                    if (ref.current && window.katex) {
                        window.katex.render(formula, ref.current, { throwOnError: false, displayMode: true });
                    }
                }, [formula]);
                return <div ref={ref} className={className} />;
            };

            const StepDiagram = ({ step, color }) => {
                const colors = {
                    blue:    "#3b82f6",
                    indigo:  "#6366f1",
                    purple:  "#a855f7",
                    violet:  "#8b5cf6",
                    emerald: "#10b981"
                };
                const c = colors[color] || "#3b82f6";

                /* ── 공통 SVG 요소 ── */
                const Orbit = ({ dasharray = "6 3", stroke = "#475569", width = 2 }) => (
                    <circle cx="120" cy="95" r="68" fill="none"
                        stroke={stroke} strokeWidth={width} strokeDasharray={dasharray} />
                );
                const Sun = () => (
                    <g>
                        <circle cx="120" cy="95" r="2" fill="rgba(251,191,36,0.3)" />
                        <circle cx="120" cy="95" r="14" fill="#fbbf24" />
                        <circle cx="120" cy="95" r="18" fill="none" stroke="rgba(251,191,36,0.3)" strokeWidth="4" />
                    </g>
                );
                /* 마커 정의 (화살표 끝) */
                const Defs = () => (
                    <defs>
                        <marker id="arr-red"   markerWidth="4" markerHeight="3" refX="3.5" refY="1.5" orient="auto"><polygon points="0 0, 4 1.5, 0 3" fill="#ef4444"/></marker>
                        <marker id="arr-blue"  markerWidth="4" markerHeight="3" refX="3.5" refY="1.5" orient="auto"><polygon points="0 0, 4 1.5, 0 3" fill="#3b82f6"/></marker>
                        <marker id="arr-green" markerWidth="4" markerHeight="3" refX="3.5" refY="1.5" orient="auto"><polygon points="0 0, 4 1.5, 0 3" fill="#10b981"/></marker>
                        <marker id="arr-c"     markerWidth="4" markerHeight="3" refX="3.5" refY="1.5" orient="auto"><polygon points={`0 0, 4 1.5, 0 3`} fill={c}/></marker>
                    </defs>
                );

                /* ── Step 1: F_gravity = F_centripetal ── */
                if (step === 1) return (
                    <div className="w-full h-48 flex items-center justify-center bg-slate-800 rounded-2xl p-3">
                        <svg viewBox="0 0 240 190" className="w-full h-full">
                            <Defs/>
                            <Orbit stroke="#64748b" width="2" dasharray="6 3"/>
                            <Sun/>
                            {/* 행성 (오른쪽) */}
                            <circle cx="188" cy="95" r="9" fill="#3b82f6"/>
                            {/* 중력 화살표 (행성→태양, 빨간) */}
                            <line x1="178" y1="95" x2="142" y2="95" stroke="#ef4444" strokeWidth="3.5" markerEnd="url(#arr-red)"/>
                            {/* 구심력 표시 (같은 방향, 파란 점선 외곽) */}
                            <line x1="178" y1="92" x2="148" y2="92" stroke="#818cf8" strokeWidth="2" strokeDasharray="4 2" markerEnd="url(#arr-blue)"/>
                            {/* 반지름 */}
                            <line x1="120" y1="95" x2="179" y2="95" stroke="#94a3b8" strokeWidth="1" strokeDasharray="4 3"/>
                            {/* 레이블 */}
                            <text x="162" y="85" textAnchor="middle" fontSize="11" fontWeight="800" fill="#ef4444">F중력</text>
                            <text x="163" y="108" textAnchor="middle" fontSize="11" fontWeight="800" fill="#818cf8">F구심</text>
                            <text x="151" y="120" textAnchor="middle" fontSize="10" fill="#64748b">r</text>
                            <text x="188" y="112" textAnchor="middle" fontSize="10" fontWeight="700" fill="#93c5fd">m</text>
                            <text x="120" y="112" textAnchor="middle" fontSize="10" fontWeight="700" fill="#fde68a">M</text>
                        </svg>
                    </div>
                );

                /* ── Step 2: GMm/r² = mv²/r ── */
                if (step === 2) return (
                    <div className="w-full h-48 flex items-center justify-center bg-slate-800 rounded-2xl p-3">
                        <svg viewBox="0 0 240 190" className="w-full h-full">
                            <Defs/>
                            <Orbit stroke="#64748b" width="2" dasharray="6 3"/>
                            <Sun/>
                            {/* 행성 */}
                            <circle cx="188" cy="95" r="9" fill="#6366f1"/>
                            {/* 반지름 선 */}
                            <line x1="120" y1="95" x2="179" y2="95" stroke="#94a3b8" strokeWidth="1.5" strokeDasharray="4 3"/>
                            <text x="150" y="90" textAnchor="middle" fontSize="12" fontWeight="800" fill="#94a3b8">r</text>
                            {/* 중력 화살표 */}
                            <line x1="179" y1="95" x2="142" y2="95" stroke="#ef4444" strokeWidth="3.5" markerEnd="url(#arr-red)"/>
                            <text x="162" y="83" textAnchor="middle" fontSize="10" fontWeight="800" fill="#ef4444">GMm/r²</text>
                            {/* 속도 벡터 (접선, 위쪽) */}
                            <line x1="188" y1="86" x2="188" y2="52" stroke="#10b981" strokeWidth="3.5" markerEnd="url(#arr-green)"/>
                            <text x="205" y="70" textAnchor="middle" fontSize="12" fontWeight="800" fill="#10b981">v</text>
                            {/* 구심가속도 */}
                            <text x="188" y="118" textAnchor="middle" fontSize="10" fontWeight="700" fill="#818cf8">mv²/r</text>
                            <text x="188" y="112" textAnchor="middle" fontSize="10" fontWeight="700" fill="#818cf8"> </text>
                        </svg>
                    </div>
                );

                /* ── Step 3: v = 2πr/T ── */
                if (step === 3) return (
                    <div className="w-full h-48 flex items-center justify-center bg-slate-800 rounded-2xl p-3">
                        <svg viewBox="0 0 240 190" className="w-full h-full">
                            <Defs/>
                            {/* 궤도 강조 */}
                            <Orbit stroke="#a78bfa" width="2.5" dasharray="none"/>
                            <Sun/>
                            {/* 행성 (상단) */}
                            <circle cx="120" cy="27" r="9" fill="#a855f7"/>
                            {/* 반지름 선 */}
                            <line x1="120" y1="81" x2="120" y2="36" stroke="#94a3b8" strokeWidth="1.5" strokeDasharray="4 3"/>
                            <text x="108" y="58" textAnchor="middle" fontSize="12" fontWeight="800" fill="#94a3b8">r</text>
                            {/* 속도 벡터 (접선, 오른쪽) */}
                            <line x1="129" y1="27" x2="165" y2="27" stroke="#10b981" strokeWidth="3.5" markerEnd="url(#arr-green)"/>
                            <text x="150" y="20" textAnchor="middle" fontSize="12" fontWeight="800" fill="#10b981">v</text>
                            {/* 원주 표시 (호) */}
                            <path d="M 120 27 A 68 68 0 0 1 188 95" fill="none" stroke="#a78bfa" strokeWidth="2.5"/>
                            {/* 레이블 */}
                            <text x="175" y="55" textAnchor="start" fontSize="10" fontWeight="700" fill="#c4b5fd">2πr</text>
                            <text x="35" y="155" textAnchor="start" fontSize="11" fontWeight="800" fill="#a78bfa">v = 2πr / T</text>
                        </svg>
                    </div>
                );

                /* ── Step 4: 속력 v 대입 ── */
                if (step === 4) return (
                    <div className="w-full h-48 flex items-center justify-center bg-slate-800 rounded-2xl p-3">
                        <svg viewBox="0 0 240 190" className="w-full h-full">
                            <Defs/>
                            <Orbit stroke="#64748b" width="2" dasharray="6 3"/>
                            <Sun/>
                            <circle cx="188" cy="95" r="9" fill="#8b5cf6"/>
                            {/* 중력 */}
                            <line x1="179" y1="95" x2="142" y2="95" stroke="#ef4444" strokeWidth="3" markerEnd="url(#arr-red)"/>
                            {/* 속도 (접선) */}
                            <line x1="188" y1="86" x2="188" y2="53" stroke="#10b981" strokeWidth="3" markerEnd="url(#arr-green)"/>
                            {/* 반지름 */}
                            <line x1="120" y1="95" x2="179" y2="95" stroke="#94a3b8" strokeWidth="1.5" strokeDasharray="4 3"/>
                            {/* 대입 수식 힌트 */}
                            <rect x="8" y="138" width="224" height="42" rx="8" fill="#1e1b4b" opacity="0.9"/>
                            <text x="120" y="154" textAnchor="middle" fontSize="10" fontWeight="700" fill="#818cf8">v = 2πr/T 대입 →</text>
                            <text x="120" y="170" textAnchor="middle" fontSize="10" fontWeight="800" fill="#c4b5fd">GM/r² = 4π²r / T²</text>
                        </svg>
                    </div>
                );

                /* ── Step 5: 최종 결론 T² = (4π²/GM)r³ ── */
                return (
                    <div className="w-full h-48 flex items-center justify-center bg-slate-800 rounded-2xl p-3">
                        <svg viewBox="0 0 240 190" className="w-full h-full">
                            <Defs/>
                            <Orbit stroke="#34d399" width="2.5" dasharray="none"/>
                            <Sun/>
                            {/* 행성1 가까이 */}
                            <circle cx="155" cy="54" r="7" fill="#34d399"/>
                            <line x1="120" y1="81" x2="149" y2="60" stroke="#94a3b8" strokeWidth="1.5" strokeDasharray="3 3"/>
                            <text x="128" y="64" textAnchor="middle" fontSize="10" fill="#94a3b8">r₁</text>
                            {/* 행성2 멀리 – 교육용 시각화이므로 다른 반지름 원 */}
                            <circle cx="188" cy="95" r="9" fill="#6ee7b7" opacity="0.6"/>
                            {/* T² ∝ r³ 레이블 */}
                            <rect x="8" y="138" width="224" height="44" rx="8" fill="#064e3b" opacity="0.9"/>
                            <text x="120" y="155" textAnchor="middle" fontSize="11" fontWeight="800" fill="#34d399">T² ∝ r³</text>
                            <text x="120" y="172" textAnchor="middle" fontSize="10" fill="#6ee7b7">K = T²/r³ = 4π²/GM (일정)</text>
                        </svg>
                    </div>
                );
            };


            const KeplerDerivation = () => {
                const [expandedIdx, setExpandedIdx] = useState(0);
                const [visibleAnswers, setVisibleAnswers] = useState({}); // { 0: true, 1: false, ... }
                const [isLoaded, setIsLoaded] = useState(false);

                useEffect(() => {
                    const timer = setInterval(() => {
                        if (window.katex && window.lucide) { setIsLoaded(true); clearInterval(timer); }
                    }, 100);
                    return () => clearInterval(timer);
                }, []);

                const toggleAnswer = (idx) => {
                    setVisibleAnswers(prev => ({ ...prev, [idx]: !prev[idx] }));
                };

                if (!isLoaded) return <div className="p-20 text-center font-bold text-slate-400">학습 엔진 로딩 중...</div>;

                const steps = [
                    {
                        title: "1. 행성이 태양 주위를 돌기 위해 필요한 힘",
                        description: "행성이 태양 주위를 공전하기 위해서는 태양이 당기는 '만유인력'이 '구심력'의 역할을 해야 합니다.",
                        formula: "F_{gravity} = F_{centripetal}",
                        color: "blue", accent: "bg-blue-600", bg: "bg-blue-50/50", text: "text-blue-600"
                    },
                    {
                        title: "2. 물리량 대입",
                        description: "만유인력 공식과 원운동의 구심력 공식을 각각 대입합니다.",
                        formula: "G \\frac{Mm}{r^2} = m \\frac{v^2}{r}",
                        color: "indigo", accent: "bg-indigo-600", bg: "bg-indigo-50/50", text: "text-indigo-600"
                    },
                    {
                        title: "3. 공전 속도의 정의",
                        description: "공전 속력 v는 총 이동 거리(원주)를 공전 주기(T)로 나눈 값입니다.",
                        formula: "v = \\frac{2\\pi r}{T}",
                        color: "purple", accent: "bg-purple-600", bg: "bg-purple-50/50", text: "text-purple-600"
                    },
                    {
                        title: "4. 속력을 공식에 대입",
                        description: "2단계 공식의 v 자리에 3단계의 식을 대입하여 방정식을 정리합니다.",
                        formula: "G \\frac{M}{r^2} = \\frac{(2\\pi r / T)^2}{r} = \\frac{4\\pi^2 r}{T^2}",
                        color: "violet", accent: "bg-violet-600", bg: "bg-violet-50/50", text: "text-violet-600"
                    },
                    {
                        title: "5. 최종 관계식 도출",
                        description: "양변을 T²과 r³에 대해 마저 정리하면 케플러 제3법칙이 유도됩니다.",
                        formula: "T^2 = \\left( \\frac{4\\pi^2}{GM} \\right) r^3",
                        color: "emerald", accent: "bg-emerald-600", bg: "bg-emerald-50/50", text: "text-emerald-600"
                    }
                ];

                return (
                    <div className="max-w-6xl mx-auto p-4 space-y-5 pb-20 mt-4">
                        {steps.map((step, idx) => (
                            <div key={idx} className={`bg-white rounded-[2.5rem] border border-slate-200 shadow-xl overflow-hidden ${expandedIdx === idx ? 'ring-2 ring-indigo-200 shadow-2xl' : ''}`}>
                                <button onClick={() => setExpandedIdx(expandedIdx === idx ? -1 : idx)} className="w-full flex items-center justify-between p-7 bg-white hover:bg-slate-50 transition-colors group">
                                    <div className="flex items-center gap-6 text-left">
                                        <div className={`w-12 h-12 rounded-2xl ${step.accent} text-white flex items-center justify-center font-black shadow-lg shadow-indigo-100 group-hover:scale-110 transition-transform`}>{idx + 1}</div>
                                        <h4 className="text-xl font-black text-slate-800 tracking-tight">{step.title}</h4>
                                    </div>
                                    <div className={`transition-transform duration-500 ${expandedIdx === idx ? 'rotate-180 bg-slate-900 text-white' : 'bg-slate-50 text-slate-400'} w-10 h-10 rounded-full flex items-center justify-center`}>
                                        <Icon name="chevron-down" size={20} />
                                    </div>
                                </button>
                                
                                <div className={`accordion-content ${expandedIdx === idx ? 'open' : ''}`}>
                                    <div className="px-10 flex flex-col lg:flex-row gap-10 pb-6 pt-2">
                                        <div className="lg:w-1/3 bg-slate-50 rounded-[2rem] p-6 flex flex-col items-center justify-center border border-slate-100 shadow-inner">
                                            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">Geometric Model</p>
                                            <StepDiagram step={idx + 1} color={step.color} />
                                        </div>
                                        <div className="flex-1 flex flex-col justify-center">
                                            <p className="text-[16px] text-slate-500 font-bold leading-relaxed mb-10 italic border-l-4 border-slate-200 pl-6">{step.description}</p>
                                            
                                            {/* Answer Reveal Section */}
                                            <div className={`p-1 bg-slate-100 rounded-3xl relative overflow-hidden transition-all duration-300 min-h-[140px] flex items-center justify-center`}>
                                                {!visibleAnswers[idx] ? (
                                                    <button 
                                                        onClick={() => toggleAnswer(idx)}
                                                        className="z-10 bg-white hover:bg-indigo-600 hover:text-white text-indigo-600 px-10 py-4 rounded-2xl font-black text-sm shadow-xl transition-all flex items-center gap-3 border border-indigo-100"
                                                    >
                                                        <Icon name="eye" size={18} /> 핵심 수식 확인하기
                                                    </button>
                                                ) : (
                                                    <div className={`w-full h-full p-8 ${step.bg} rounded-[1.4rem] animate-in fade-in zoom-in-95 duration-500 relative`}>
                                                        <button 
                                                            onClick={() => toggleAnswer(idx)}
                                                            className="absolute top-4 right-4 text-slate-300 hover:text-slate-500"
                                                        >
                                                            <Icon name="eye-off" size={16} />
                                                        </button>
                                                        <MathBox formula={step.formula} className={`${step.text} text-3xl font-black text-center`} />
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}

                        <div className="bg-slate-900 p-12 rounded-[4rem] mt-12 text-white shadow-2xl relative border-[10px] border-slate-800">
                            <div className="absolute top-0 right-0 w-80 h-80 bg-indigo-500/10 rounded-full blur-[100px]"></div>
                            <div className="relative z-10 grid lg:grid-cols-2 gap-12 items-center text-center lg:text-left">
                                <div>
                                    <div className="flex items-center justify-center lg:justify-start gap-2 text-indigo-400 mb-6 font-black tracking-widest uppercase text-xs">
                                        <Icon name="award" size={16} /> Final Conclusion
                                    </div>
                                    <h4 className="text-4xl font-black mb-6 leading-tight">뉴턴의 힘으로 완성된 조화의 법칙</h4>
                                    <p className="text-slate-400 text-sm leading-relaxed italic pr-4">
                                        중심 천체의 질량이 일정하다면 모든 행성에 대해 T²/r³은 항상 일정한 값을 가짐을 수식으로 완벽히 증명했습니다.
                                    </p>
                                </div>
                                <div className="bg-white/5 p-10 rounded-[3rem] border border-white/10 backdrop-blur-xl flex items-center justify-center">
                                    <MathBox formula={"T^2 = \\left( \\frac{4\\pi^2}{GM} \\right) r^3"} className="text-3xl text-amber-400 font-black" />
                                </div>
                            </div>
                        </div>

                        {/* ── 탐구 질문 섹션 ── */}
                        <div className="mt-10 space-y-6">
                            <div className="flex items-center gap-3 mb-2">
                                <div className="h-1 flex-1 bg-gradient-to-r from-indigo-500/40 to-transparent rounded-full"/>
                                <span className="text-xs font-black tracking-widest text-indigo-400 uppercase">심화 탐구 질문</span>
                                <div className="h-1 flex-1 bg-gradient-to-l from-indigo-500/40 to-transparent rounded-full"/>
                            </div>

                            {/* 탐구 질문 1 */}
                            <ExploreCard
                                index="01"
                                accentColor="#f59e0b"
                                tag="역학적 탐구"
                                title="태양계의 행성들은 왜 멀어질수록 공전 속도가 느려져야만 할까?"
                                intent="단순히 공전 속도 공식을 암기하는 것을 넘어, 중력(구심력)과 관성(원심적 경향) 사이의 역학적 평형을 이해하기 위한 질문입니다."
                                points={[
                                    "중력이 거리의 제곱에 반비례하여 약해질 때, 궤도를 유지하기 위해 필요한 속도는 어떻게 변해야 할까?",
                                    "만약 해왕성이 수성의 공전 속도(47.9 km/s)로 움직인다면 어떤 일이 벌어질까?",
                                    "반대로 수성이 해왕성의 속도(5.4 km/s)로 느려진다면 궤도를 유지할 수 있을까?"
                                ]}
                                hints={[
                                    { label: "힌트 1 — 궤도를 유지하는 조건",    text: "원 궤도를 유지하려면 구심력 = 중력이어야 합니다. 즉 GMm/r² = mv²/r 가 성립해야 하죠. 이 식에서 v를 r에 대해 정리하면 어떤 관계가 보이나요?" },
                                    { label: "힌트 2 — 너무 빠른 행성",          text: "v²/r (필요 구심력) > GM/r² (실제 중력) 이면 중력이 부족해 행성이 바깥으로 튕겨 나갑니다. 해왕성 궤도에서 수성의 속도는 필요한 v보다 훨씬 클까요, 아닐까요?" },
                                    { label: "힌트 3 — 너무 느린 행성",          text: "반대로 v²/r < GM/r² 이면 중력이 속도에 비해 너무 강해 행성이 안쪽으로 끌려 들어갑니다. 수성 궤도에서 해왕성 속도라면 중력을 이기기에 충분할까요?" }
                                ]}
                            />

                            {/* 탐구 질문 2 */}
                            <ExploreCard
                                index="02"
                                accentColor="#8b5cf6"
                                tag="정량적·비교 탐구"
                                title="중심 천체의 질량이 다른 외계 행성계에서도 케플러 제3법칙의 '조화 상수'는 일정할까?"
                                intent="케플러 제3법칙(T² ∝ a³)의 비례 상수 k = 4π²/GM 이 중심 천체의 질량에 종속적이라는 사실을 탐구하기 위한 질문입니다."
                                points={[
                                    "태양계 데이터로 구한 a³/T² 값과, 질량이 태양의 2배인 항성을 도는 외계 행성계의 a³/T² 값을 비교하면 어떤 차이가 생길까?",
                                    "중심 질량이 커질 때, 동일한 궤도 장반경(a)을 가진 행성의 공전 주기는 어떻게 변할까?",
                                    "이 관계를 통해 보이지 않는 천체(블랙홀 등)의 질량을 역으로 추산하는 방법은 무엇일까?"
                                ]}
                                hints={[
                                    { label: "힌트 1 — 비례 상수의 정체",          text: "T² = (4π²/GM) r³ 에서 비례 상수는 4π²/GM 입니다. 이 상수에서 변하는 것은 오직 중심 천체의 질량 M뿐이에요. 태양의 M과 2M을 대입하면 상수값은 어떻게 달라질까요?" },
                                    { label: "힌트 2 — 같은 궤도, 다른 주기",       text: "동일한 a에서 M이 2배가 되면 T² = (4π²/2GM) a³ 이 됩니다. 원래보다 T는 커지나요 작아지나요? √2 와 관련이 있을 것입니다." },
                                    { label: "힌트 3 — 보이지 않는 천체의 질량",     text: "관측 가능한 행성의 a(궤도 크기)와 T(공전 주기)를 측정하면 M = 4π²a³ / (GT²) 공식으로 중심 천체의 질량을 구할 수 있습니다. 이 원리가 블랙홀 질량 측정에 어떻게 응용될까요?" }
                                ]}
                            />
                        </div>

                    </div>
                );
            };

            /* ── ExploreCard 컴포넌트 ── */
            const ExploreCard = ({ index, accentColor, tag, title, intent, points, hints }) => {
                const [openHint, setOpenHint] = React.useState(null);

                const toggleHint = (i) => setOpenHint(prev => prev === i ? null : i);

                return (
                    <div className="bg-slate-900 rounded-[2.5rem] border border-slate-700 shadow-2xl overflow-hidden">
                        {/* 헤더 */}
                        <div className="flex items-start gap-6 p-8 pb-0">
                            <div className="flex-shrink-0 w-16 h-16 rounded-2xl flex items-center justify-center font-black text-2xl shadow-lg"
                                style={{ background: `${accentColor}22`, color: accentColor, border: `2px solid ${accentColor}55` }}>
                                {index}
                            </div>
                            <div className="flex-1 pt-1">
                                <span className="text-[10px] font-black tracking-widest uppercase px-3 py-1 rounded-full"
                                    style={{ background: `${accentColor}22`, color: accentColor }}>
                                    {tag}
                                </span>
                                <h5 className="text-lg font-black text-white mt-3 leading-snug">{title}</h5>
                                <p className="text-slate-400 text-xs leading-relaxed mt-2 italic border-l-2 pl-3"
                                    style={{ borderColor: `${accentColor}66` }}>{intent}</p>
                            </div>
                        </div>

                        {/* 탐구 포인트 */}
                        <div className="px-8 pt-6 pb-2">
                            <p className="text-[10px] font-black tracking-widest text-slate-500 uppercase mb-3">탐구 포인트</p>
                            <ul className="space-y-2">
                                {points.map((pt, i) => (
                                    <li key={i} className="flex items-start gap-3 text-slate-300 text-sm leading-relaxed">
                                        <span className="mt-1 flex-shrink-0 w-5 h-5 rounded-full text-[10px] font-black flex items-center justify-center"
                                            style={{ background: `${accentColor}33`, color: accentColor }}>
                                            {i + 1}
                                        </span>
                                        {pt}
                                    </li>
                                ))}
                            </ul>
                        </div>

                        {/* 힌트 아코디언 */}
                        <div className="px-8 pt-5 pb-8 space-y-3">
                            <p className="text-[10px] font-black tracking-widest text-slate-500 uppercase mb-3">💡 힌트 (클릭하여 확인)</p>
                            {hints.map((h, i) => (
                                <div key={i} className="rounded-2xl border overflow-hidden transition-all duration-300"
                                    style={{ borderColor: openHint === i ? `${accentColor}66` : '#334155', background: openHint === i ? `${accentColor}11` : '#1e293b' }}>
                                    <button
                                        onClick={() => toggleHint(i)}
                                        className="w-full flex items-center justify-between px-5 py-3 text-left transition-all"
                                    >
                                        <span className="text-sm font-bold" style={{ color: openHint === i ? accentColor : '#94a3b8' }}>{h.label}</span>
                                        <span className="text-slate-500 text-lg font-bold transition-transform duration-300"
                                            style={{ transform: openHint === i ? 'rotate(45deg)' : 'rotate(0deg)' }}>+</span>
                                    </button>
                                    <div className={`accordion-content ${openHint === i ? 'open' : ''} px-5`}>
                                        <p className="text-slate-300 text-sm leading-relaxed pb-4">{h.text}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerDerivation />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=2600, scrolling=True)

if __name__ == "__main__":
    run_sim()
