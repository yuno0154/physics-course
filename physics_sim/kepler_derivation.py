import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 수학적 유도", layout="wide")
    
    st.title("📐 케플러 제3법칙의 수학적 유도")
    st.markdown("""
    뉴턴의 만유인력 법칙과 원운동의 구심력을 결합하여 **조화의 법칙($T^2 \propto r^3$)**이 도출되는 과정을 단계별로 확인해 보세요.
    각 단계를 클릭하여 상세한 수식과 다이어그램을 펼쳐볼 수 있습니다.
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
        <!-- KaTeX for Math -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            .step-card { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
            .math-font { font-family: 'Times New Roman', serif; }
            .accordion-content { 
                max-height: 0; 
                overflow: hidden; 
                transition: max-height 0.4s ease-out, padding 0.4s ease; 
                opacity: 0;
            }
            .accordion-content.open { 
                max-height: 800px; 
                opacity: 1;
                padding-bottom: 2rem;
            }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                const ref = useRef(null);
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const MathBox = ({ formula, className }) => {
                const ref = useRef(null);
                useEffect(() => {
                    if (ref.current && window.katex) {
                        window.katex.render(formula, ref.current, {
                            throwOnError: false,
                            displayMode: true
                        });
                    }
                }, [formula]);
                return <div ref={ref} className={className} />;
            };

            const StepDiagram = ({ step, color }) => {
                const colors = {
                    blue: "#3b82f6",
                    indigo: "#6366f1",
                    purple: "#a855f7",
                    violet: "#8b5cf6",
                    emerald: "#10b981"
                };
                const c = colors[color] || "#3b82f6";

                return (
                    <div className="w-full h-full min-h-[180px] flex items-center justify-center bg-white rounded-3xl p-4">
                        <svg viewBox="0 0 200 160" className="w-full h-full drop-shadow-sm">
                            <circle cx="100" cy="80" r="65" fill="none" stroke="#f1f5f9" strokeWidth="2" strokeDasharray="4,4" />
                            <circle cx="100" cy="80" r="14" fill="#fbbf24" className="animate-pulse" />
                            
                            {step === 1 && (
                                <g>
                                    <circle cx="165" cy="80" r="7" fill="#3b82f6" />
                                    <line x1="165" y1="80" x2="125" y2="80" stroke={c} strokeWidth="5" markerEnd="url(#arrow)" />
                                    <text x="145" y="70" textAnchor="middle" fontSize="14" fontWeight="900" fill={c}>F</text>
                                </g>
                            )}
                            {step === 2 && (
                                <g>
                                    <circle cx="165" cy="80" r="7" fill="#6366f1" />
                                    <line x1="165" y1="80" x2="130" y2="80" stroke={c} strokeWidth="5" markerEnd="url(#arrow)" />
                                    <line x1="100" y1="80" x2="165" y2="80" stroke="#94a3b8" strokeWidth="2" strokeDasharray="3,3" />
                                    <text x="132" y="105" textAnchor="middle" fontSize="12" fontWeight="bold" fill="#64748b">r</text>
                                </g>
                            )}
                            {step === 3 && (
                                <g>
                                    <circle cx="100" cy="80" r="65" fill="none" stroke={c} strokeWidth="4" strokeDasharray="12,6" opacity="0.6" />
                                    <circle cx="165" cy="80" r="7" fill={c} />
                                    <line x1="165" y1="80" x2="165" y2="30" stroke={c} strokeWidth="4" markerEnd="url(#arrow)" />
                                    <text x="180" y="55" textAnchor="middle" fontSize="14" fontWeight="900" fill={c}>v</text>
                                    <text x="100" y="30" textAnchor="middle" fontSize="13" fontWeight="bold" fill={c}>2πr</text>
                                </g>
                            )}
                            {step === 4 && (
                                <g>
                                    <rect x="60" y="45" width="80" height="70" fill={`${c}10`} stroke={c} strokeWidth="3" rx="10" strokeDasharray="6,3" />
                                    <text x="100" y="85" textAnchor="middle" fontSize="16" fontWeight="900" fill={c}>v → ΣF</text>
                                </g>
                            )}
                             {step === 5 && (
                                <g>
                                    <circle cx="100" cy="80" r="65" fill="none" stroke={c} strokeWidth="4" />
                                    <circle cx="165" cy="80" r="9" fill="#10b981" />
                                    <text x="100" y="155" textAnchor="middle" fontSize="18" fontWeight="900" fill={c}>T² ∝ r³</text>
                                </g>
                            )}

                            <defs>
                                <marker id="arrow" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
                                    <path d="M0,0 L0,8 L7,4 Z" fill="currentColor" />
                                </marker>
                            </defs>
                        </svg>
                    </div>
                );
            };

            const KeplerDerivation = () => {
                const [expandedIdx, setExpandedIdx] = useState(0); // 첫 번째 단계만 열림

                const steps = [
                    {
                        title: "1. 행성이 태양 주위를 돌기 위해 필요한 힘",
                        description: "행성이 태양 주위를 원운동하기 위해서는 태양이 당기는 '만유인력'이 '구심력'의 역할을 해야 합니다.",
                        formula: "F_{gravity} = F_{centripetal}",
                        color: "blue",
                        bg: "bg-blue-50/50",
                        text: "text-blue-600",
                        accent: "bg-blue-600"
                    },
                    {
                        title: "2. 물리량 대입",
                        description: "만유인력 공식과 원운동의 구심력 공식을 각각 대입합니다.",
                        formula: "G \\frac{Mm}{r^2} = m \\frac{v^2}{r}",
                        color: "indigo",
                        bg: "bg-indigo-50/50",
                        text: "text-indigo-600",
                        accent: "bg-indigo-600"
                    },
                    {
                        title: "3. 공전 속도의 정의",
                        description: "공전 속력 v는 총 이동 거리(원주)를 공전 주기(T)로 나눈 값입니다.",
                        formula: "v = \\frac{2\\pi r}{T}",
                        color: "purple",
                        bg: "bg-purple-50/50",
                        text: "text-purple-600",
                        accent: "bg-purple-600"
                    },
                    {
                        title: "4. 속력을 공식에 대입",
                        description: "2단계 공식의 v 자리에 3단계의 식을 대입하여 방정식을 정리합니다.",
                        formula: "G \\frac{M}{r^2} = \\frac{(2\\pi r / T)^2}{r} = \\frac{4\\pi^2 r}{T^2}",
                        color: "violet",
                        bg: "bg-violet-50/50",
                        text: "text-violet-600",
                        accent: "bg-violet-600"
                    },
                    {
                        title: "5. 최종 관계식 도출",
                        description: "양변을 T²과 r³에 대해 마저 정리하면 케플러 제3법칙이 유도됩니다.",
                        formula: "T^2 = \\left( \\frac{4\\pi^2}{GM} \\right) r^3",
                        color: "emerald",
                        bg: "bg-emerald-50/50",
                        text: "text-emerald-600",
                        accent: "bg-emerald-600"
                    }
                ];

                return (
                    <div className="max-w-6xl mx-auto p-4 space-y-4 pb-20 mt-4">
                        <div className="flex flex-col gap-4">
                            {steps.map((step, idx) => (
                                <div key={idx} className={`step-card bg-white rounded-[2.5rem] border border-slate-200 shadow-xl overflow-hidden ${expandedIdx === idx ? 'ring-4 ring-slate-100 shadow-2xl' : 'hover:border-slate-300'}`}>
                                    {/* Accordion Header */}
                                    <button 
                                        onClick={() => setExpandedIdx(expandedIdx === idx ? -1 : idx)}
                                        className="w-full flex items-center justify-between p-8 text-left bg-white"
                                    >
                                        <div className="flex items-center gap-6">
                                            <div className={`w-12 h-12 rounded-2xl ${step.accent} text-white flex items-center justify-center font-black text-lg shadow-lg`}>
                                                {idx + 1}
                                            </div>
                                            <h4 className={`text-xl font-black ${expandedIdx === idx ? 'text-slate-900' : 'text-slate-500 hover:text-slate-700'}`}>{step.title}</h4>
                                        </div>
                                        <div className={`w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center transition-transform duration-500 ${expandedIdx === idx ? 'rotate-180 bg-slate-900 text-white' : 'text-slate-400'}`}>
                                            <Icon name="chevron-down" size={20} />
                                        </div>
                                    </button>

                                    {/* Accordion Content */}
                                    <div className={`accordion-content ${expandedIdx === idx ? 'open' : ''}`}>
                                        <div className="px-8 flex flex-col md:flex-row gap-8 items-stretch pt-2">
                                            <div className="w-full md:w-2/5 p-6 bg-slate-50 rounded-3xl border border-slate-100 flex items-center justify-center shadow-inner">
                                                <StepDiagram step={idx + 1} color={step.color} />
                                            </div>
                                            <div className="flex-1 p-4 flex flex-col justify-center">
                                                <p className="text-[15px] text-slate-500 mb-8 leading-relaxed font-bold pr-4 max-w-lg italic border-l-4 border-slate-200 pl-6">
                                                    {step.description}
                                                </p>
                                                <div className={`p-10 ${step.bg} rounded-[2rem] border-2 border-dashed border-slate-100 shadow-sm relative overflow-hidden`}>
                                                    <div className="absolute -top-6 -right-6 w-24 h-24 bg-white/50 rounded-full blur-2xl"></div>
                                                    <MathBox formula={step.formula} className={`${step.text} text-2xl font-black text-center`} />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Summary Section */}
                        <div className="bg-slate-900 p-12 rounded-[4rem] text-white shadow-2xl relative overflow-hidden mt-16 border-[12px] border-slate-800">
                             <div className="absolute top-0 right-0 w-80 h-80 bg-blue-600/10 rounded-full blur-[100px]"></div>
                             <div className="relative z-10 flex flex-col lg:flex-row items-center gap-12">
                                <div className="flex-1 text-center lg:text-left">
                                    <div className="flex items-center justify-center lg:justify-start gap-2 text-indigo-400 mb-6 font-black tracking-widest uppercase text-xs">
                                        <Icon name="award" size={16} /> Mathematical Conclusion
                                    </div>
                                    <h4 className="text-4xl font-black mb-8 leading-tight">증명 완료: $T^2 \propto r^3$</h4>
                                    <p className="text-slate-400 text-sm leading-relaxed max-w-xl mx-auto lg:mx-0 font-medium italic">
                                        "태양의 질량 $M$이 일정하다면, 비례상수 $K(=\frac{4\pi^2}{GM})$는 태양계 내의 모든 행성에서 동일한 값을 가집니다. 따라서 공전 주기의 제곱은 궤도 반지름의 세제곱에 비례함이 증명되었습니다."
                                    </p>
                                </div>
                                <div className="w-full lg:w-fit p-10 bg-white/5 rounded-[3rem] border border-white/10 backdrop-blur-xl self-stretch flex items-center justify-center shadow-2xl">
                                    <MathBox formula="T^2 = K \cdot r^3 \quad \left(K = \frac{4\pi^2}{GM}\right)" className="text-3xl text-amber-400 font-black px-4" />
                                </div>
                             </div>
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
    components.html(react_code, height=1800, scrolling=True)

if __name__ == "__main__":
    run_sim()
