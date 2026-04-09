import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙의 수학적 유도", layout="wide")
    
    st.title("🪐 케플러 제3법칙(조화의 법칙)의 수학적 유도")
    st.markdown("""
    케플러는 관측을 통해 제3법칙을 발견했지만, 뉴턴은 자신의 **만유인력 법칙**과 **원운동의 역학**을 결합하여 이를 수학적으로 완벽히 증명했습니다.
    아래의 단계별 과정을 통해 중력과 공전 주기의 관계를 이해해 보세요.
    """)

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
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            .step-card { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
            .step-card:hover { transform: translateY(-5px); }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const MathBox = ({ formula, className = "" }) => {
                const containerRef = React.useRef(null);
                useEffect(() => {
                    if (containerRef.current && window.katex) {
                        window.katex.render(formula, containerRef.current, {
                            throwOnError: false,
                            displayMode: true
                        });
                    }
                }, [formula]);
                return <div ref={containerRef} className={`my-2 ${className}`}></div>;
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
                        description: "2단계 공식의 v 자리에 3단계의 식을 대입하여 정리합니다.",
                        formula: "G \\frac{M}{r^2} = \\frac{(2\\pi r / T)^2}{r} = \\frac{4\\pi^2 r}{T^2}",
                        color: "violet"
                    },
                    {
                        title: "5. 최종 관계식 도출",
                        description: "양변을 T²과 r³에 대해 정리하면 케플러 제3법칙이 유도됩니다.",
                        formula: "T^2 = \\left( \\frac{4\\pi^2}{GM} \\right) r^3",
                        color: "emerald"
                    }
                ];

                return (
                    <div className="max-w-4xl mx-auto p-4 space-y-8 pb-12">
                        <div className="grid grid-cols-1 gap-6">
                            {steps.map((step, idx) => (
                                <div key={idx} className="step-card bg-white p-6 rounded-3xl border border-slate-200 shadow-xl flex gap-6 items-start relative overflow-hidden group">
                                    <div className={`absolute top-0 left-0 w-2 h-full bg-${step.color}-500`}></div>
                                    <div className={`w-12 h-12 bg-${step.color}-50 rounded-2xl flex items-center justify-center text-${step.color}-600 font-black text-xl shrink-0`}>
                                        {idx + 1}
                                    </div>
                                    <div className="flex-1">
                                        <h4 className="text-lg font-black text-slate-800 mb-2">{step.title}</h4>
                                        <p className="text-[14px] text-slate-500 mb-4 leading-relaxed font-medium">{step.description}</p>
                                        <div className={`p-4 bg-${step.color}-50/50 rounded-2xl border border-${step.color}-100 animate-in fade-in slide-in-from-left-4 duration-700`}>
                                            <MathBox formula={step.formula} className={`text-${step.color}-700 font-bold`} />
                                        </div>
                                    </div>
                                    {idx < steps.length - 1 && (
                                        <div className="absolute -bottom-6 left-10 text-slate-200 hidden md:block">
                                            <Icon name="arrow-down" size={30} />
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>

                        <div className="bg-slate-900 p-8 rounded-[40px] text-white shadow-2xl relative overflow-hidden">
                             <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl"></div>
                             <h4 className="text-xl font-black text-blue-400 mb-4 flex items-center gap-2">
                                <Icon name="check-circle" /> 유도 결과의 물리적 의미
                             </h4>
                             <p className="text-slate-300 text-sm leading-relaxed mb-6">
                                괄호 안의 값 <span className="font-mono text-emerald-400 font-bold">4π²/GM</span>은 태양의 질량이 일정하다면 변하지 않는 **상수(K)**입니다. 
                                따라서 행성의 종류에 상관없이 주기의 제곱과 궤도 반지름(장반경)의 세제곱의 비는 항상 일정하다는 것을 증명할 수 있습니다.
                             </p>
                             <div className="p-5 bg-white/5 rounded-2xl border border-white/10 flex items-center justify-center">
                                <MathBox formula="\\frac{T^2}{r^3} = \\frac{4\\pi^2}{GM} = Constant" className="text-2xl text-amber-400" />
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
    components.html(react_code, height=1100, scrolling=False)

if __name__ == "__main__":
    run_sim()
