import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="원운동의 표현: 각속도와 선속도", layout="wide")
    
    st.title("🔄 원운동의 표현: 각속도(ω), 선속도(v), 주기(T)")
    st.markdown("""
    등속 원운동하는 물체의 빠르기를 어떻게 나타낼까요? 
    **각속도(ω)**와 **선속도(v)**의 관계, 그리고 한 바퀴 도는 데 걸리는 시간인 **주기(T)**를 탐구해 봅시다.
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
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; overflow: hidden; }
            .no-scrollbar::-webkit-scrollbar { display: none; }
            .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
            .math-font { font-family: 'Times New Roman', serif; font-style: italic; }
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef, useMemo } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) window.lucide.createIcons();
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const CircularMotionAdv = () => {
                const [radius, setRadius] = useState(1.0); 
                const [omega, setOmega] = useState(1.0); // rad/s
                const [activeTab, setActiveTab] = useState('missions');
                const [time, setTime] = useState(0);
                const [showVectors, setShowVectors] = useState(true);
                const [isPaused, setIsPaused] = useState(false);
                
                // 정답 확인 상태 (0: 질문, 1: 정리 확인, 2: 정답 공개)
                const [ans1, setAns1] = useState(0);
                const [ans2, setAns2] = useState(0);
                const [ans3, setAns3] = useState(0);
                const [ans4, setAns4] = useState(0);
                const [ans5, setAns5] = useState(0);

                const requestRef = useRef();

                // 애니메이션 루프
                const animate = (t) => {
                    if (!isPaused) {
                        setTime(prevTime => prevTime + 0.016); // 약 60fps
                    }
                    requestRef.current = requestAnimationFrame(animate);
                };

                useEffect(() => {
                    requestRef.current = requestAnimationFrame(animate);
                    return () => cancelAnimationFrame(requestRef.current);
                }, [isPaused]);

                // 계산
                const angle = time * omega;
                const v = radius * omega; 
                const period = (2 * Math.PI) / omega;
                
                const viewSize = 500;
                const centerX = viewSize / 2;
                const centerY = viewSize / 2;
                const scale = 100;
                const visualR = radius * scale;

                const ballX = centerX + visualR * Math.cos(-angle);
                const ballY = centerY + visualR * Math.sin(-angle);

                // 속도 벡터 끝점
                const vVecLen = v * 30; // 시각화를 위한 속도 벡터 길이
                const vEndX = ballX + vVecLen * Math.cos(-angle - Math.PI/2);
                const vEndY = ballY + vVecLen * Math.sin(-angle - Math.PI/2);

                return (
                    <div className="flex flex-col items-center bg-transparent p-1 text-slate-800">
                        <div className="w-full max-w-6xl rounded-[32px] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.15)] border border-slate-200 overflow-hidden bg-white">
                            
                            {/* 상단 스탯 바 */}
                            <div className="grid grid-cols-4 gap-0 bg-slate-900 text-white border-b border-slate-800">
                                <div className="text-center py-4 border-r border-slate-800/50">
                                    <p className="text-[10px] text-sky-400 font-black uppercase tracking-widest mb-1 leading-none">반지름 (r)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-3xl font-black text-white">{radius.toFixed(1)}</span>
                                        <span className="text-lg font-bold text-slate-500">m</span>
                                    </div>
                                </div>
                                <div className="text-center py-4 border-r border-slate-800/50">
                                    <p className="text-[10px] text-amber-400 font-black uppercase tracking-widest mb-1 leading-none">각속도 (ω)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-3xl font-black text-white">{omega.toFixed(1)}</span>
                                        <span className="text-lg font-bold text-slate-500">rad/s</span>
                                    </div>
                                </div>
                                <div className="text-center py-4 border-r border-slate-800/50">
                                    <p className="text-[10px] text-rose-400 font-black uppercase tracking-widest mb-1 leading-none">선속도 (v)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-3xl font-black text-white">{v.toFixed(2)}</span>
                                        <span className="text-lg font-bold text-slate-500">m/s</span>
                                    </div>
                                </div>
                                <div className="text-center py-4">
                                    <p className="text-[10px] text-emerald-400 font-black uppercase tracking-widest mb-1 leading-none">주기 (T)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-3xl font-black text-white">{period.toFixed(2)}</span>
                                        <span className="text-lg font-bold text-slate-500">s</span>
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
                                        
                                        <line x1={centerX} y1={centerY} x2={ballX} y2={ballY} stroke="#0ea5e9" strokeWidth="3" strokeLinecap="round" />
                                        
                                        {showVectors && (
                                            <g>
                                                <line x1={ballX} y1={ballY} x2={vEndX} y2={vEndY} stroke="#e11d48" strokeWidth="5" strokeLinecap="round" markerEnd="url(#arrow-v)" />
                                                <text x={vEndX + 10} y={vEndY} fill="#e11d48" className="text-lg font-black italic shadow-sm">v</text>
                                            </g>
                                        )}

                                        <circle cx={centerX} cy={centerY} r="6" fill="#0f172a" />
                                        <circle cx={ballX} cy={ballY} r="12" fill="#0f172a" stroke="#fff" strokeWidth="3" className="shadow-lg" />
                                        
                                        <defs>
                                            <marker id="arrow-v" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="3" markerHeight="3" orient="auto-start-reverse">
                                                <path d="M 0 0 L 10 5 L 0 10 z" fill="#e11d48" />
                                            </marker>
                                        </defs>
                                    </svg>
                                    
                                    <div className="absolute bottom-6 flex gap-3">
                                        <button onClick={()=>setIsPaused(!isPaused)} className="bg-slate-900 text-white p-3 rounded-2xl shadow-xl hover:scale-105 transition-all">
                                            <Icon name={isPaused ? "play" : "pause"} size={24} fill="currentColor" />
                                        </button>
                                        <button onClick={()=>setShowVectors(!showVectors)} className={`p-3 rounded-2xl shadow-xl transition-all ${showVectors ? 'bg-rose-500 text-white' : 'bg-slate-200 text-slate-500'}`}>
                                            <Icon name="arrow-up-right" size={24} />
                                        </button>
                                    </div>
                                </div>

                                {/* 2. 컨트롤/활동지 영역 */}
                                <div className="w-full lg:w-[440px] bg-white flex flex-col">
                                    <div className="flex bg-slate-50 p-1 border-b border-slate-100">
                                        <button onClick={() => setActiveTab('missions')} className={`flex-1 py-3 text-[13px] font-black rounded-xl transition-all ${activeTab === 'missions' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}>활동지 (개념 탐구)</button>
                                        <button onClick={() => setActiveTab('settings')} className={`flex-1 py-3 text-[13px] font-black rounded-xl transition-all ${activeTab === 'settings' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}>조절 및 데이터</button>
                                    </div>

                                    <div className="p-5 flex-1 overflow-y-auto no-scrollbar space-y-5">
                                        {activeTab === 'missions' ? (
                                            <div className="space-y-4 animate-in fade-in slide-in-from-right-10 duration-500">
                                                <h4 className="text-[20px] font-black text-slate-900 border-l-4 border-blue-600 pl-3 mb-6 leading-tight">원운동을 어떻게 표현할까?</h4>
                                                
                                                {/* 질문 1: 각변위 */}
                                                <div 
                                                    className={`p-4 rounded-3xl border-2 transition-all cursor-pointer ${ans1 === 2 ? 'bg-blue-900 border-blue-500 text-white shadow-xl' : 'bg-slate-50 border-transparent hover:bg-slate-100'}`}
                                                    onClick={() => setAns1(p => p < 2 ? p + 1 : 2)}
                                                >
                                                    <p className={`text-[12px] font-black mb-1 uppercase ${ans1 === 2 ? 'text-blue-300' : 'text-blue-500'}`}>Q1. 위치 변화량의 표현</p>
                                                    {ans1 === 0 ? (
                                                        <p className="text-[15px] font-bold">기준선으로부터 돌아간 회전각(<span className="math-font italic text-xl">Δθ</span>)을 무엇이라 할까요?</p>
                                                    ) : ans1 === 1 ? (
                                                        <p className="text-amber-500 font-black animate-pulse text-[15px]">"스스로 답해 보셨나요? 한 번 더!"</p>
                                                    ) : (
                                                        <p className="text-[18px] font-black text-white">정답: <span className="text-sky-300">각변위(Angular Displacement)</span></p>
                                                    )}
                                                </div>

                                                {/* 질문 2: 각속도 */}
                                                <div 
                                                    className={`p-4 rounded-3xl border-2 transition-all cursor-pointer ${ans2 === 2 ? 'bg-amber-900 border-amber-500 text-white shadow-xl' : 'bg-slate-50 border-transparent hover:bg-slate-100'}`}
                                                    onClick={() => setAns2(p => p < 2 ? p + 1 : 2)}
                                                >
                                                    <p className={`text-[12px] font-black mb-1 uppercase ${ans2 === 2 ? 'text-amber-200' : 'text-amber-600'}`}>Q2. 단위 시간 동안 회전하는 각도</p>
                                                    {ans2 === 0 ? (
                                                        <p className="text-[15px] font-bold">회전하는 각도의 빠르기를 나타내는 물리량의 이름과 기호는?</p>
                                                    ) : ans2 === 1 ? (
                                                        <p className="text-sky-400 font-black animate-pulse text-[15px]">"정의식도 떠올려 보세요. 다시 클릭!"</p>
                                                    ) : (
                                                        <div className="space-y-1">
                                                            <p className="text-[18px] font-black">정답: <span className="text-amber-300 underline decoration-2">각속도(ω)</span></p>
                                                            <p className="text-[16px] font-bold font-serif italic text-amber-100">ω = Δθ / Δt [rad/s]</p>
                                                        </div>
                                                    )}
                                                </div>

                                                {/* 질문 3: 선속도 정의 */}
                                                <div 
                                                    className={`p-4 rounded-3xl border-2 transition-all cursor-pointer ${ans3 === 2 ? 'bg-rose-900 border-rose-500 text-white shadow-xl' : 'bg-slate-50 border-transparent hover:bg-slate-100'}`}
                                                    onClick={() => setAns3(p => p < 2 ? p + 1 : 2)}
                                                >
                                                    <p className={`text-[12px] font-black mb-1 uppercase ${ans3 === 2 ? 'text-rose-200' : 'text-rose-500'}`}>Q3. 호의 길이를 시간으로 나누면?</p>
                                                    {ans3 === 0 ? (
                                                        <p className="text-[15px] font-bold text-slate-700 leading-tight">회전하는 원궤도상의 호의 길이(<span className="math-font italic text-xl">Δs</span>)를 시간으로 나누면 무엇일까?</p>
                                                    ) : ans3 === 1 ? (
                                                        <p className="text-emerald-400 font-black animate-pulse text-[15px]">"방향은 원의 접선 방향입니다. 다시 클릭!"</p>
                                                    ) : (
                                                        <div className="space-y-1">
                                                            <p className="text-[18px] font-black">정답: <span className="text-rose-300 underline decoration-2">선속도(v)</span></p>
                                                            <p className="text-[16px] font-bold font-serif italic text-rose-100">v = Δs / Δt [m/s]</p>
                                                        </div>
                                                    )}
                                                </div>

                                                {/* 질문 4: 관계식 */}
                                                <div 
                                                    className={`p-4 rounded-3xl border-2 transition-all cursor-pointer ${ans4 === 2 ? 'bg-emerald-900 border-emerald-500 shadow-xl' : 'bg-slate-50 border-transparent hover:bg-slate-100'}`}
                                                    onClick={() => setAns4(p => p < 2 ? p + 1 : 2)}
                                                >
                                                    <p className={`text-[12px] font-black mb-1 uppercase ${ans4 === 2 ? 'text-emerald-200' : 'text-emerald-600'}`}>Q4. 각속도와 선속도의 관계</p>
                                                    {ans4 === 0 ? (
                                                        <p className="text-[15px] font-bold text-slate-700">각속도(<span className="math-font italic text-amber-600 text-xl">ω</span>)와 선속도(<span className="math-font italic text-rose-600 text-xl">v</span>)는 어떤 관계일까?</p>
                                                    ) : ans4 === 1 ? (
                                                        <p className="text-white font-black animate-pulse text-[15px]">"반지름과의 상관관계를 생각해 보세요!"</p>
                                                    ) : (
                                                        <p className="text-[24px] font-black text-white italic tracking-widest text-center py-1">v = rω</p>
                                                    )}
                                                </div>

                                                {/* 질문 5: 주기 */}
                                                <div 
                                                    className={`p-4 rounded-3xl border-2 transition-all cursor-pointer ${ans5 === 2 ? 'bg-slate-900 border-slate-700 shadow-xl' : 'bg-slate-50 border-transparent hover:bg-slate-100'}`}
                                                    onClick={() => setAns5(p => p < 2 ? p + 1 : 2)}
                                                >
                                                    <p className={`text-[12px] font-black mb-1 uppercase ${ans5 === 2 ? 'text-slate-400' : 'text-slate-50'}`}>Q5. 원둘레를 한 바퀴 도는 시간</p>
                                                    {ans5 === 0 ? (
                                                        <p className="text-[15px] font-bold text-slate-700">이 시간을 무엇이라 하며, 선속도 v와 관계는?</p>
                                                    ) : ans5 === 1 ? (
                                                        <p className="text-sky-400 font-black animate-pulse text-[15px]">"한 바퀴의 길이(2πr)를 속도로 나누면?"</p>
                                                    ) : (
                                                        <div className="space-y-1 text-center">
                                                            <p className="text-[18px] font-black text-white">정답: <span className="text-emerald-400 underline underline-offset-4 decoration-2">주기 (T)</span></p>
                                                            <p className="text-[17px] font-black text-white py-1 italic tracking-tighter">T = 2πr / v = 2π / ω</p>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="space-y-5 animate-in fade-in slide-in-from-left-10 duration-500">
                                                <div className="space-y-4 p-1">
                                                    <div className="space-y-1">
                                                        <div className="flex justify-between items-end">
                                                            <span className="text-[12px] font-black text-slate-500 uppercase px-2 border-l-4 border-sky-400">반지름 (r)</span>
                                                            <div className="flex items-center gap-1">
                                                                <input type="number" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-16 h-7 text-sm font-black text-center bg-sky-50 text-sky-700 border-2 border-sky-100 rounded-md outline-none" />
                                                                <span className="text-[10px] font-bold text-slate-400 font-serif">m</span>
                                                            </div>
                                                        </div>
                                                        <input type="range" min="0.1" max="2.0" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-full h-1.5 bg-slate-100 rounded-full appearance-none cursor-pointer accent-sky-600" />
                                                    </div>
                                                    
                                                    <div className="space-y-1">
                                                        <div className="flex justify-between items-end">
                                                            <span className="text-[12px] font-black text-slate-500 uppercase px-2 border-l-4 border-amber-400">각속도 (ω)</span>
                                                            <div className="flex items-center gap-1">
                                                                <input type="number" step="0.1" value={omega.toFixed(1)} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-16 h-7 text-sm font-black text-center bg-amber-50 text-amber-700 border-2 border-amber-100 rounded-md outline-none" />
                                                                <span className="text-[10px] font-bold text-slate-400 font-serif">rad/s</span>
                                                            </div>
                                                        </div>
                                                        <input type="range" min="0.1" max="10.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full h-1.5 bg-slate-100 rounded-full appearance-none cursor-pointer accent-amber-500" />
                                                    </div>

                                                    <div className="space-y-1 pt-1">
                                                        <div className="flex justify-between items-end">
                                                            <span className="text-[12px] font-black text-slate-500 uppercase px-2 border-l-4 border-emerald-400">주기 (T)</span>
                                                            <div className="flex items-center gap-1">
                                                                <input 
                                                                    type="number" 
                                                                    step="0.1" 
                                                                    value={period.toFixed(2)} 
                                                                    onChange={e => {
                                                                        const t = parseFloat(e.target.value);
                                                                        if(t > 0) setOmega((2 * Math.PI) / t);
                                                                    }} 
                                                                    className="w-16 h-7 text-sm font-black text-center bg-emerald-50 text-emerald-700 border-2 border-emerald-100 rounded-md outline-none" 
                                                                />
                                                                <span className="text-[10px] font-bold text-slate-400 font-serif">s</span>
                                                            </div>
                                                        </div>
                                                        <input 
                                                            type="range" 
                                                            min="0.6" 
                                                            max="10.0" 
                                                            step="0.1" 
                                                            value={period} 
                                                            onChange={e => {
                                                                const t = parseFloat(e.target.value);
                                                                setOmega((2 * Math.PI) / t);
                                                            }} 
                                                            className="w-full h-1.5 bg-slate-100 rounded-full appearance-none cursor-pointer accent-emerald-500" 
                                                        />
                                                    </div>
                                                </div>

                                                <div className="bg-slate-900 p-6 rounded-[32px] text-white space-y-4">
                                                    <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest leading-none">Real-time Dynamics</h4>
                                                    <div className="grid grid-cols-2 gap-4">
                                                        <div className="bg-slate-800 p-4 rounded-3xl border border-slate-700 shadow-inner">
                                                            <p className="text-[10px] text-rose-400 font-black mb-1">선속도 (v)</p>
                                                            <p className="text-2xl font-black italic">{(radius * omega).toFixed(2)}<span className="text-[10px] text-slate-500 ml-1 font-serif">m/s</span></p>
                                                        </div>
                                                        <div className="bg-slate-800 p-4 rounded-3xl border border-slate-700 shadow-inner">
                                                            <p className="text-[10px] text-emerald-400 font-black mb-1">주기 (T)</p>
                                                            <p className="text-2xl font-black italic">{(2 * Math.PI / omega).toFixed(2)}<span className="text-[10px] text-slate-500 ml-1 font-serif">s</span></p>
                                                        </div>
                                                    </div>
                                                </div>

                                                <div className="p-4 bg-blue-50/50 rounded-[28px] border border-blue-100 flex gap-4">
                                                    <Icon name="info" className="text-blue-500 shrink-0" size={24} />
                                                    <p className="text-[13px] font-bold text-blue-700 leading-relaxed italic">
                                                        각속도(ω)가 일정할 때, 반지름(r)이 커질수록 물체의 선속도(v)는 어떻게 변하나요? 직접 확인해 보세요!
                                                    </p>
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
            root.render(<CircularMotionAdv />);
        </script>
    </body>
    </html>
    """

    components.html(react_code, height=840, scrolling=False)

if __name__ == "__main__":
    run_sim()
