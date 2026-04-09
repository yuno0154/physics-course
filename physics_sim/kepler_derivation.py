import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 수학적 유도", layout="wide")
    
    st.title("📐 케플러 제3법칙의 수학적 유도")
    st.markdown("""
    뉴턴의 만유인력 법칙과 원운동의 구심력을 결합하여 **조화의 법칙($T^2 \\propto r^3$)**이 도출되는 과정을 단계별로 확인해 보세요.
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

            const MathBox = ({ formula, className }) => {
                const ref = useRef(null);
                useEffect(() => {
                    if (ref.current && window.katex) {
                        try {
                            window.katex.render(formula, ref.current, {
                                throwOnError: false,
                                displayMode: true
                            });
                        } catch (e) {
                            console.error("Katex error:", e);
                        }
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
                    <div className="w-full h-48 flex items-center justify-center bg-white rounded-3xl p-4">
                        <svg viewBox="0 0 200 160" className="w-full h-full">
                            <circle cx="100" cy="80" r="65" fill="none" stroke="#f1f5f9" strokeWidth="2" strokeDasharray="4,4" />
                            <circle cx="100" cy="80" r="14" fill="#fbbf24" />
                            {step === 1 && (
                                <g>
                                    <circle cx="165" cy="80" r="7" fill="#3b82f6" />
                                    <line x1="164" y1="80" x2="125" y2="80" stroke={c} strokeWidth="5" />
                                    <text x="145" y="70" textAnchor="middle" fontSize="14" fontWeight="900" fill={c}>F</text>
                                </g>
                            )}
                            {step === 2 && (
                                <g>
                                    <circle cx="165" cy="80" r="7" fill="#6366f1" />
                                    <line x1="165" y1="80" x2="130" y2="80" stroke={c} strokeWidth="5" />
                                    <text x="132" y="105" textAnchor="middle" fontSize="12" fontWeight="bold" fill="#64748b">r</text>
                                </g>
                            )}
                            {step === 3 && (
                                <g>
                                    <circle cx="165" cy="80" r="7" fill={c} />
                                    <line x1="165" y1="80" x2="165" y2="35" stroke={c} strokeWidth="4" />
                                    <text x="180" y="55" textAnchor="middle" fontSize="14" fontWeight="900" fill={c}>v</text>
                                </g>
                            )}
                            {step === 4 && (
                                <g>
                                    <rect x="65" y="50" width="70" height="60" fill={`${c}15`} stroke={c} strokeWidth="2" rx="8" />
                                    <text x="100" y="85" textAnchor="middle" fontSize="14" fontWeight="900" fill={c}>Algebra</text>
                                </g>
                            )}
                            {step === 5 && (
                                <g>
                                    <text x="100" y="85" textAnchor="middle" fontSize="22" fontWeight="900" fill={c}>Q.E.D</text>
                                </g>
                            )}
                        </svg>
                    </div>
                );
            };

            const KeplerDerivation = () => {
                const [expandedIdx, setExpandedIdx] = useState(0);
                const [isLoaded, setIsLoaded] = useState(false);

                useEffect(() => {
                    const timer = setInterval(() => {
                        if (window.katex && window.lucide) {
                            setIsLoaded(true);
                            clearInterval(timer);
                        }
                    }, 100);
                    return () => clearInterval(timer);
                }, []);

                if (!isLoaded) return <div className="p-20 text-center font-bold text-slate-400">엔진 로딩 중...</div>;

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
                    <div className="max-w-6xl mx-auto p-4 space-y-4 pb-20 mt-4">
                        {steps.map((step, idx) => (
                            <div key={idx} className={`bg-white rounded-[2rem] border border-slate-200 shadow-xl overflow-hidden ${expandedIdx === idx ? 'ring-2 ring-indigo-100' : ''}`}>
                                <button 
                                    onClick={() => setExpandedIdx(expandedIdx === idx ? -1 : idx)}
                                    className="w-full flex items-center justify-between p-7 bg-white hover:bg-slate-50 transition-colors"
                                >
                                    <div className="flex items-center gap-5 text-left">
                                        <div className={`w-10 h-10 rounded-xl ${step.accent} text-white flex items-center justify-center font-black shadow-md`}>{idx + 1}</div>
                                        <h4 className="text-lg font-black text-slate-800">{step.title}</h4>
                                    </div>
                                    <div className={`transition-transform duration-300 ${expandedIdx === idx ? 'rotate-180' : ''}`}>
                                        <Icon name="chevron-down" size={24} className="text-slate-400" />
                                    </div>
                                </button>
                                <div className={`accordion-content ${expandedIdx === idx ? 'open' : ''}`}>
                                    <div className="px-8 flex flex-col md:flex-row gap-8 pb-4">
                                        <div className="md:w-1/3 bg-slate-50 rounded-2xl p-4 flex items-center justify-center">
                                            <StepDiagram step={idx + 1} color={step.color} />
                                        </div>
                                        <div className="flex-1 flex flex-col justify-center gap-6">
                                            <p className="text-sm text-slate-500 font-bold leading-relaxed">{step.description}</p>
                                            <div className={`p-8 ${step.bg} rounded-2xl border border-slate-100`}>
                                                <MathBox formula={step.formula} className={`${step.text} text-xl font-bold`} />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                        <div className="bg-slate-900 p-12 rounded-[3.5rem] mt-10 text-white shadow-2xl relative overflow-hidden">
                            <div className="grid lg:grid-cols-2 gap-10 items-center">
                                <div>
                                    <h5 className="text-indigo-400 font-black mb-4 uppercase tracking-widest text-xs">Conclusion</h5>
                                    <h4 className="text-3xl font-black mb-6">최종 결과: 조화의 법칙</h4>
                                    <p className="text-slate-400 text-sm leading-relaxed italic font-medium">
                                        "비례 상수 K는 중심 천체(태양)의 질량에만 의존하므로, 태양 주위의 모든 행성에 동일하게 적용됩니다."
                                    </p>
                                </div>
                                <div className="bg-white/5 p-8 rounded-3xl border border-white/10 flex items-center justify-center">
                                    <MathBox formula={"T^2 = \\left( \\frac{4\\pi^2}{GM} \\right) r^3"} className="text-2xl text-amber-400 font-black" />
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
    components.html(react_code, height=1500, scrolling=True)

if __name__ == "__main__":
    run_sim()
