import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="원운동의 기초: 라디안과 호의 길이", layout="wide")
    
    # 상단 브랜딩 및 제목
    st.title("📏 원운동의 기초: 라디안(Radian)과 호의 길이")
    st.markdown("""
    이 시뮬레이션은 원운동을 이해하기 위한 가장 기초적인 개념인 **반지름(r), 중심각(θ), 호의 길이(s)** 사이의 관계를 탐구합니다.
    물리학에서 각도의 단위로 왜 **'라디안(rad)'**을 사용하는지 시각적으로 확인해 보세요.
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
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                const iconRef = useRef(null);
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const BasicCircularSim = () => {
                // --- 상태 관리 ---
                const [radius, setRadius] = useState(1.0); 
                const [angleRad, setAngleRad] = useState(1.0); 
                const [activeTab, setActiveTab] = useState('missions');
                const [answerStage, setAnswerStage] = useState(0); // 0: 숨김, 1: 확인질문, 2: 공개
                
                // --- 계산 ---
                const PI = Math.PI;
                const angleDeg = (angleRad * 180) / PI; 
                const arcLength = radius * angleRad;

                const scale = 110; 
                const visualR = radius * scale;
                const viewSize = 500;
                const centerX = viewSize / 2;
                const centerY = viewSize / 2;

                const ballX = centerX + visualR * Math.cos(-angleRad);
                const ballY = centerY + visualR * Math.sin(-angleRad);

                const getSectorPath = () => {
                    const startX = centerX + visualR;
                    const startY = centerY;
                    const largeArcFlag = angleRad > PI ? 1 : 0;
                    return `M ${centerX} ${centerY} L ${startX} ${startY} A ${visualR} ${visualR} 0 ${largeArcFlag} 0 ${ballX} ${ballY} Z`;
                };

                const getArcPath = () => {
                    const startX = centerX + visualR;
                    const startY = centerY;
                    const largeArcFlag = angleRad > PI ? 1 : 0;
                    return `M ${startX} ${startY} A ${visualR} ${visualR} 0 ${largeArcFlag} 0 ${ballX} ${ballY}`;
                };

                const handleRadChange = (val) => {
                    let num = parseFloat(val);
                    if (isNaN(num)) num = 0;
                    if (num > 6.28) num = 6.28;
                    if (num < 0) num = 0;
                    setAngleRad(num);
                };

                return (
                    <div className="flex flex-col items-center bg-transparent min-h-screen p-1 text-slate-800">
                        <div className="w-full max-w-6xl rounded-[32px] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.15)] border border-slate-200 overflow-hidden bg-white">
                            
                            {/* 상단 핵심 데이터 바 */}
                            <div className="grid grid-cols-3 gap-0 bg-slate-900 text-white border-b border-slate-800">
                                <div className="text-center py-4 px-2 border-r border-slate-800/50">
                                    <p className="text-[10px] text-sky-400 font-black uppercase tracking-widest mb-1 leading-none">반지름 (r)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-3xl font-black text-white">{radius.toFixed(1)}</span>
                                        <span className="text-lg font-bold text-slate-500">m</span>
                                    </div>
                                </div>
                                <div className="text-center py-4 px-2 border-r border-slate-800/50">
                                    <p className="text-[10px] text-amber-400 font-black uppercase tracking-widest mb-1 leading-none">중심각 (θ)</p>
                                    <div className="flex flex-col items-center">
                                        <div className="flex items-center justify-center gap-1">
                                            <span className="text-3xl font-black text-white">{angleRad.toFixed(2)}</span>
                                            <span className="text-lg font-bold text-slate-500">rad</span>
                                        </div>
                                    </div>
                                </div>
                                <div className="text-center py-4 px-2">
                                    <p className="text-[10px] text-rose-500 font-black uppercase tracking-widest mb-1 leading-none">호의 길이 (s)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-3xl font-black text-white">{arcLength.toFixed(2)}</span>
                                        <span className="text-lg font-bold text-slate-500">m</span>
                                    </div>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row min-h-[580px]">
                                {/* 1. 시각화 영역 */}
                                <div className="flex-1 bg-slate-50 relative flex items-center justify-center p-4 border-b lg:border-b-0 lg:border-r-2 border-slate-100">
                                    <svg viewBox={`0 0 ${viewSize} ${viewSize}`} className="w-full h-full max-w-[440px] filter drop-shadow-xl">
                                        <circle cx={centerX} cy={centerY} r={50} fill="none" stroke="#e2e8f0" strokeWidth="1" />
                                        <circle cx={centerX} cy={centerY} r={100} fill="none" stroke="#e2e8f0" strokeWidth="1" />
                                        <circle cx={centerX} cy={centerY} r={150} fill="none" stroke="#e2e8f0" strokeWidth="1" />
                                        <circle cx={centerX} cy={centerY} r={200} fill="none" stroke="#e2e8f0" strokeWidth="2" strokeOpacity="0.5" />
                                        
                                        <circle cx={centerX} cy={centerY} r={visualR} fill="none" stroke="#cbd5e1" strokeWidth="2" strokeDasharray="6,6" />
                                        <path d={getSectorPath()} fill="rgba(56, 189, 248, 0.12)" stroke="none" />
                                        <line x1={centerX} y1={centerY} x2={centerX + visualR} y2={centerY} stroke="#334155" strokeWidth="4" strokeLinecap="round" />
                                        <line x1={centerX} y1={centerY} x2={ballX} y2={ballY} stroke="#334155" strokeWidth="4" strokeLinecap="round" />
                                        <path d={getArcPath()} fill="none" stroke="#f43f5e" strokeWidth="8" strokeLinecap="round" />
                                        <circle cx={centerX} cy={centerY} r="8" fill="#0f172a" stroke="white" strokeWidth="3" />
                                        <circle cx={ballX} cy={ballY} r="10" fill="#f43f5e" stroke="white" strokeWidth="3" />
                                        
                                        <text x={centerX + visualR/2} y={centerY + 25} textAnchor="middle" fill="#1e293b" className="text-base italic font-black">r = {radius}m</text>
                                        <g>
                                            <path d={`M ${centerX + 40} ${centerY} A 40 40 0 ${angleRad > PI ? 1 : 0} 0 ${centerX + 40 * Math.cos(-angleRad)} ${centerY + 40 * Math.sin(-angleRad)}`} fill="none" stroke="#f59e0b" strokeWidth="3" />
                                            <text x={centerX + 65 * Math.cos(-angleRad/2)} y={centerY + 65 * Math.sin(-angleRad/2)} textAnchor="middle" dominantBaseline="middle" fill="#b45309" className="text-sm font-black">θ = {angleRad.toFixed(2)}</text>
                                        </g>
                                        <text x={centerX + (visualR + 35) * Math.cos(-angleRad/2)} y={centerY + (visualR + 35) * Math.sin(-angleRad/2)} textAnchor="middle" dominantBaseline="middle" fill="#e11d48" className="text-xl italic font-black text-rose-600">s = {arcLength.toFixed(2)}m</text>
                                    </svg>
                                </div>

                                {/* 2. 컨트롤 영역 */}
                                <div className="w-full lg:w-[420px] bg-white flex flex-col">
                                    <div className="flex bg-slate-50 p-1 border-b border-slate-100">
                                        <button 
                                            onClick={() => setActiveTab('missions')} 
                                            className={`flex-1 py-3 text-[13px] font-black rounded-xl transition-all duration-300 ${activeTab === 'missions' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}
                                        >
                                            탐구 미션
                                        </button>
                                        <button 
                                            onClick={() => setActiveTab('settings')} 
                                            className={`flex-1 py-3 text-[13px] font-black rounded-xl transition-all duration-300 ${activeTab === 'settings' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}
                                        >
                                            조절 및 수식
                                        </button>
                                    </div>

                                    <div className="p-5 flex-1 overflow-y-auto no-scrollbar space-y-4">
                                        {activeTab === 'missions' ? (
                                            <div className="space-y-3 animate-in fade-in slide-in-from-right-10 duration-500">
                                                <h4 className="text-[11px] font-black text-slate-400 uppercase tracking-widest px-1">질문에 의한 탐구 실험</h4>
                                                
                                                <div className="p-4 bg-slate-50 rounded-[20px] border-2 border-transparent hover:bg-blue-50/30 transition-all group">
                                                    <div className="flex gap-3">
                                                        <span className="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center text-sm font-black shadow-lg shadow-blue-100 group-hover:scale-110 transition-transform">1</span>
                                                        <p className="text-[15px] leading-relaxed text-slate-700 font-bold">
                                                            반지름(<span className="math-font text-xl text-blue-600">r</span>)을 <span className="text-blue-600 font-black text-xl">1.0m</span>로 고정하고 라디안(<span className="math-font text-xl text-amber-600">θ</span>)을 조절해 보세요. <span className="text-rose-600 font-black underline decoration-2">호의 길이(s)</span>는 각도에 따라 어떻게 변하나요?
                                                        </p>
                                                    </div>
                                                </div>

                                                <div className="p-4 bg-slate-50 rounded-[20px] border-2 border-transparent hover:bg-emerald-50/30 transition-all group">
                                                    <div className="flex gap-3">
                                                        <span className="flex-shrink-0 w-8 h-8 rounded-lg bg-emerald-500 text-white flex items-center justify-center text-sm font-black shadow-lg shadow-emerald-100 group-hover:scale-110 transition-transform">2</span>
                                                        <p className="text-[15px] leading-relaxed text-slate-700 font-bold">
                                                            라디안(<span className="math-font text-xl text-amber-600">θ</span>)을 <span className="text-amber-600 font-black text-xl">1.00rad</span>로 고정하고 반지름을 바꿔보세요. <span className="text-rose-600 font-black underline decoration-2">호의 길이(s)</span>와 반지름은 어떤 관계인가요?
                                                        </p>
                                                    </div>
                                                </div>

                                                <div 
                                                    onClick={() => setAnswerStage(prev => prev < 2 ? prev + 1 : 2)}
                                                    className={`p-5 rounded-[24px] shadow-lg mt-1 relative overflow-hidden group cursor-pointer transition-all duration-500 ${answerStage === 2 ? 'bg-slate-900 ring-2 ring-emerald-500/20' : 'bg-slate-800 hover:bg-slate-700'}`}
                                                >
                                                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                                                        <Icon name="lightbulb" size={50} className="text-white" />
                                                    </div>
                                                    
                                                    <p className="text-amber-400 text-[12px] font-black mb-2 flex items-center gap-2">
                                                        <Icon name="sparkles" size={16} /> 탐구 정리
                                                    </p>

                                                    {answerStage === 0 && (
                                                        <div className="flex flex-col items-center py-2 animate-in zoom-in-95 duration-300">
                                                            <p className="text-slate-300 text-[14px] font-bold mb-2 italic">답을 정리한 후 클릭해서 비교해 보세요!</p>
                                                            <div className="bg-blue-600 hover:bg-blue-500 text-white px-5 py-2 rounded-full font-black text-[13px] shadow-lg transition-transform active:scale-95">
                                                                결론 비교하기
                                                            </div>
                                                        </div>
                                                    )}

                                                    {answerStage === 1 && (
                                                        <div className="flex flex-col items-center py-2 animate-in slide-in-from-bottom-2 duration-300 text-center">
                                                            <p className="text-sky-300 text-[15px] font-black mb-2 italic">스스로 정리해 보셨나요?</p>
                                                            <div className="bg-amber-500 hover:bg-amber-400 text-white px-5 py-2 rounded-full font-black text-[13px] shadow-xl animate-pulse">
                                                                확인을 위해 다시 클릭
                                                            </div>
                                                        </div>
                                                    )}

                                                    {answerStage === 2 && (
                                                        <div className="animate-in fade-in zoom-in-95 duration-700">
                                                            <p className="text-white text-[17px] leading-relaxed font-black italic tracking-tight">
                                                                "호의 길이 <span className="text-rose-400 text-xl font-black">s</span>는 반지름 <span className="text-sky-400 text-xl font-black">r</span>과 라디안각 <span className="text-amber-400 text-xl font-black">θ</span>에 각각 <span className="text-emerald-400 text-xl font-black underline decoration-2 underline-offset-4">비례</span>합니다."
                                                            </p>
                                                            <div className="mt-2 flex justify-end">
                                                                <button onClick={(e) => { e.stopPropagation(); setAnswerStage(0); }} className="text-slate-500 hover:text-slate-300 text-[10px] font-bold underline">다시 숨기기</button>
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="space-y-4 animate-in fade-in slide-in-from-left-10 duration-500">
                                                <div className="space-y-4 p-1">
                                                    <div className="space-y-2">
                                                        <div className="flex justify-between items-end">
                                                            <span className="text-[13px] font-black text-slate-500 tracking-tight uppercase px-2 border-l-4 border-sky-400 leading-none">반지름 (r)</span>
                                                            <div className="flex items-center gap-2">
                                                                <input type="number" step="0.1" min="0.1" max="2.0" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-20 h-8 text-lg font-black text-center bg-sky-50 text-sky-700 border-2 border-sky-200 rounded-lg outline-none focus:border-sky-500" />
                                                                <span className="text-xl font-black text-sky-600">m</span>
                                                            </div>
                                                        </div>
                                                        <input type="range" min="0.1" max="2.0" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-full h-2 bg-slate-100 rounded-full appearance-none cursor-pointer accent-sky-600" />
                                                    </div>
                                                    
                                                    <div className="space-y-2 pt-4 border-t-2 border-slate-50">
                                                        <div className="flex justify-between items-start">
                                                            <div className="flex flex-col">
                                                                <span className="text-[13px] font-black text-slate-500 tracking-tight uppercase px-2 border-l-4 border-amber-400 leading-none mb-1">중심각 (θ)</span>
                                                                <span className="text-[12px] text-slate-400 font-bold bg-slate-50 px-2 py-0.5 rounded-full w-fit">≈ {angleDeg.toFixed(1)}°</span>
                                                            </div>
                                                            <div className="flex items-center gap-2">
                                                                <input type="number" step="0.01" min="0" max="6.28" value={angleRad} onChange={e=>handleRadChange(e.target.value)} className="w-24 h-8 text-lg font-black text-center bg-amber-50 text-amber-700 border-2 border-amber-200 rounded-lg outline-none focus:border-amber-500" />
                                                                <span className="text-xl font-black text-amber-600">rad</span>
                                                            </div>
                                                        </div>
                                                        <input type="range" min="0" max="6.28" step="0.01" value={angleRad} onChange={e=>setAngleRad(parseFloat(e.target.value))} className="w-full h-2 bg-slate-100 rounded-full appearance-none cursor-pointer accent-amber-500" />
                                                    </div>
                                                </div>

                                                <div className="bg-white p-4 rounded-[28px] border-2 border-slate-100 shadow-md relative overflow-hidden group">
                                                    <div className="absolute top-0 left-0 w-2 h-full bg-rose-500"></div>
                                                    <h4 className="text-[10px] font-black text-slate-400 uppercase mb-2 tracking-widest">실시간 물리 관계식</h4>
                                                    <div className="flex flex-col items-center py-4 bg-slate-50 rounded-[20px] mb-4 group-hover:bg-rose-50 transition-colors">
                                                        <p className="text-4xl font-black text-slate-900 italic tracking-tighter">s = rθ</p>
                                                    </div>
                                                    <div className="text-[16px] font-black text-slate-700 text-center flex flex-wrap justify-center gap-2 items-center leading-none">
                                                        <span className="text-sky-600 px-2 py-1 bg-sky-50 rounded-lg">{radius.toFixed(1)}m</span> 
                                                        <span className="text-slate-300">×</span> 
                                                        <span className="text-amber-600 px-2 py-1 bg-amber-50 rounded-lg">{angleRad.toFixed(2)}rad</span> 
                                                        <span className="text-slate-300">=</span> 
                                                        <span className="text-rose-500 text-2xl">{arcLength.toFixed(2)}m</span>
                                                    </div>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<BasicCircularSim />);
        </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트로 HTML 삽입
    components.html(react_code, height=820, scrolling=False)

if __name__ == "__main__":
    run_sim()
