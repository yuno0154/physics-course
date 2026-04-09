import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙의 수학적 유도", layout="wide")
    
    st.title("🪐 케플러 제3법칙(조화의 법칙)의 수학적 유도")
    st.markdown("""
    뉴턴의 **만유인력 법칙**과 **원운동의 구심력** 개념을 결합하여 케플러 제3법칙을 수학적으로 전개해 봅시다.
    왼쪽의 그림과 오른쪽의 식을 함께 보며 과정을 이해해 보세요.
    """)

    # raw string (r""")을 사용하여 백슬래시 기호가 파이썬 이스케이프 문자로 해석되는 것을 방지합니다.
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
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            .step-card { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
            .step-card:hover { transform: scale(1.01); border-color: #3b82f6; }
            .math-container { min-height: 2.5rem; display: flex; align-items: center; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) window.lucide.createIcons();
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const MathBox = ({ formula, className = "" }) => {
                const containerRef = useRef(null);
                useEffect(() => {
                    if (containerRef.current && window.katex) {
                        window.katex.render(formula, containerRef.current, {
                            throwOnError: false,
                            displayMode: true
                        });
                    }
                }, [formula]);
                return <div ref={containerRef} className={`math-container ${className}`}></div>;
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
                            {/* Base Orbit */}
                            <circle cx="100" cy="80" r="65" fill="none" stroke="#f1f5f9" strokeWidth="2" strokeDasharray="4,4" />
                            <circle cx="100" cy="80" r="14" fill="#fbbf24" className="animate-pulse" /> {/* Sun */}
                            
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
                const steps = [
                    {
                        title: "1. 힘의 평형 설정",
                        description: "행성이 태양 주위를 원운동하기 위해서는 태양이 당기는 '만유인력'이 '구심력'의 역할을 해야 합니다.",
                        formula: "F_{gravity} = F_{centripetal}",
                        color: "blue"
                    },
                    {
                        title: "2. 물리량 대입",
                        description: "만유인력 공식과 원운동의 구심력 공식을 각각 대입합니다.",
                        formula: "G \\frac{Mm}{r^2} = m \\frac{v^2}{r}",
                        color: "indigo"
                    },
                    {
                        title: "3. 공전 속도의 정의",
                        description: "공전 속력 v는 총 이동 거리(원주)를 공전 주기(T)로 나눈 값입니다.",
                        formula: "v = \\frac{2\\pi r}{T}",
                        color: "purple"
                    },
                    {
                        title: "4. 속력을 공식에 대입",
                        description: "2단계 공식의 v 자리에 3단계의 식을 대입하여 방정식을 정리합니다.",
                        formula: "G \\frac{M}{r^2} = \\frac{(2\\pi r / T)^2}{r} = \\frac{4\\pi^2 r}{T^2}",
                        color: "violet"
                    },
                    {
                        title: "5. 최종 관계식 도출",
                        description: "양변을 T²과 r³에 대해 마저 정리하면 케플러 제3법칙이 유도됩니다.",
                        formula: "T^2 = \\left( \\frac{4\\pi^2}{GM} \\right) r^3",
                        color: "emerald"
                    }
                ];

                return (
                    <div className="max-w-6xl mx-auto p-4 space-y-6 pb-20 mt-4">
                        <div className="flex flex-col gap-6">
                            {steps.map((step, idx) => (
                                <div key={idx} className="step-card bg-white rounded-3xl border border-slate-200 shadow-lg flex flex-col md:flex-row overflow-hidden group">
                                    {/* Left: Diagram */}
                                    <div className="w-full md:w-1/3 p-4 bg-slate-50 border-r border-slate-100 flex items-center justify-center">
                                        <StepDiagram step={idx + 1} color={step.color} />
                                    </div>
                                    
                                    {/* Right: Text & Math */}
                                    <div className="flex-1 p-8 relative">
                                        <div className={`absolute top-0 left-0 w-2 h-full bg-${step.color}-500 opacity-20 group-hover:opacity-100 transition-opacity`}></div>
                                        <div className="flex items-start gap-4 mb-4">
                                            <div className={`w-8 h-8 rounded-lg bg-${step.color}-100 text-${step.color}-600 flex items-center justify-center font-black text-sm shrink-0`}>
                                                {idx + 1}
                                            </div>
                                            <h4 className="text-xl font-black text-slate-800">{step.title}</h4>
                                        </div>
                                        <p className="text-[14px] text-slate-500 mb-6 leading-relaxed font-semibold pr-4">{step.description}</p>
                                        <div className={`p-6 bg-${step.color}-50/30 rounded-2xl border border-${step.color}-100/50`}>
                                            <MathBox formula={step.formula} className={`text-${step.color}-700 font-bold`} />
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Summary Section */}
                        <div className="bg-slate-900 p-10 rounded-[3rem] text-white shadow-2xl relative overflow-hidden mt-12 border-4 border-slate-800">
                             <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/10 rounded-full blur-[80px]"></div>
                             <div className="relative z-10 flex flex-col lg:flex-row items-center gap-10">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 text-blue-400 mb-4 font-black tracking-widest uppercase text-xs">
                                        <Icon name="award" size={16} /> Conclusion
                                    </div>
                                    <h4 className="text-3xl font-black mb-6">증명 완료: $T^2 \propto r^3$</h4>
                                    <p className="text-slate-400 text-sm leading-relaxed mb-0 font-medium italic">
                                        태양의 질량 $M$이 일정하다면, 괄호 안의 모든 항은 상수가 됩니다.<br/>
                                        따라서 공전 주기의 제곱($T^2$)은 궤도 반지름의 세제곱($r^3$)에 비례함을 알 수 있습니다.
                                    </p>
                                </div>
                                <div className="w-full lg:w-fit p-8 bg-white/5 rounded-3xl border border-white/10 backdrop-blur-sm self-stretch flex items-center justify-center">
                                    <MathBox formula="T^2 = K \cdot r^3 \quad \left(K = \frac{4\pi^2}{GM}\right)" className="text-2xl text-amber-400 font-black" />
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
    components.html(react_code, height=1250, scrolling=False)

if __name__ == "__main__":
    run_sim()
