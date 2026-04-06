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
                                        {/* 그리드 */}
                                        <circle cx={centerX} cy={centerY} r={50} fill="none" stroke="#e2e8f0" strokeWidth="1" />
                                        <circle cx={centerX} cy={centerY} r={100} fill="none" stroke="#e2e8f0" strokeWidth="1" />
                                        <circle cx={centerX} cy={centerY} r={150} fill="none" stroke="#e2e8f0" strokeWidth="1" />
                                        <circle cx={centerX} cy={centerY} r={200} fill="none" stroke="#e2e8f0" strokeWidth="2" strokeOpacity="0.5" />
                                        
                                        {/* 궤도 */}
                                        <circle cx={centerX} cy={centerY} r={visualR} fill="none" stroke="#cbd5e1" strokeWidth="2" strokeDasharray="6,6" />
                                        
                                        {/* 반지름 벡터 */}
                                        <line x1={centerX} y1={centerY} x2={ballX} y2={ballY} stroke="#0ea5e9" strokeWidth="3" strokeLinecap="round" />
                                        
                                        {/* 속도 벡터 (v) */}
                                        {showVectors && (
                                            <g>
                                                <line x1={ballX} y1={ballY} x2={vEndX} y2={vEndY} stroke="#e11d48" strokeWidth="5" strokeLinecap="round" markerEnd="url(#arrow-v)" />
                                                <text x={vEndX + 10} y={vEndY} fill="#e11d48" className="text-lg font-black italic">v</text>
                                            </g>
                                        )}

                                        {/* 물체 */}
                                        <circle cx={centerX} cy={centerY} r="6" fill="#0f172a" />
                                        <circle cx={ballX} cy={ballY} r="12" fill="#0f172a" stroke="#fff" strokeWidth="3" className="shadow-lg" />
                                        
                                        {/* 화살표 마커 정의 */}
                                        <defs>
                                            <marker id="arrow-v" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="3" markerHeight="3" orient="auto-start-reverse">
                                                <path d="M 0 0 L 10 5 L 0 10 z" fill="#e11d48" />
                                            </marker>
                                        </defs>
                                    </svg>
                                    
                                    {/* 컨트롤 플로팅 버튼 */}
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
                                                <h4 className="text-[11px] font-black text-slate-400 uppercase tracking-widest px-1">원운동을 어떻게 표현할까?</h4>
                                                
                                                {/* 질문 1: 각변위 */}
                                                <div 
                                                    className={`p-5 rounded-3xl border-2 transition-all cursor-pointer ${ans1 === 2 ? 'bg-blue-900 border-blue-500 text-white' : 'bg-slate-50 border-transparent'}`}
                                                    onClick={() => setAns1(p => p < 2 ? p + 1 : 2)}
                                                >
                                                    <p className="text-sm font-bold text-blue-400 mb-2 uppercase">Q1. 회전한 회전각(Δθ) ?</p>
                                                    {ans1 === 0 ? (
                                                        <p className="text-[16px] font-black">원운동에서 위치 변화량의 표현을 무엇이라 할까요?</p>
                                                    ) : ans1 === 1 ? (
                                                        <p className="text-amber-400 font-black animate-pulse text-[16px]">"생각해 보았나요? 다시 눌러보세요."</p>
                                                    ) : (
                                                        <p className="text-[20px] font-black text-white">정답: <span className="text-sky-300 underline underline-offset-4 decoration-4">각변위(Angular Displacement)</span></p>
                                                    )}
                                                </div>

                                                {/* 질문 2: 각속도 */}
                                                <div 
                                                    className={`p-5 rounded-3xl border-2 transition-all cursor-pointer ${ans2 === 2 ? 'bg-amber-900 border-amber-500 text-white' : 'bg-slate-50 border-transparent'}`}
                                                    onClick={() => setAns2(p => p < 2 ? p + 1 : 2)}
                                                >
                                                    <p className="text-sm font-bold text-amber-500 mb-2 uppercase">Q2. 단위 시간 동안 회전하는 각도(ω) ?</p>
                                                    {ans2 === 0 ? (
                                                        <p className="text-[16px] font-black">이 물리량의 이름과 정의식(ω=?)은 무엇일까요?</p>
                                                    ) : ans2 === 1 ? (
                                                        <p className="text-sky-400 font-black animate-pulse text-[16px]">"어떤 기호를 사용할까요? 다시 클릭!"</p>
                                                    ) : (
                                                        <div className="space-y-2">
                                                            <p className="text-[19px] font-black">정답: 각속도 (Angular Velocity)</p>
                                                            <p className="text-[22px] font-black font-serif italic text-amber-300">ω = Δθ / Δt [rad/s]</p>
                                                        </div>
                                                    )}
                                                </div>

                                                {/* 질문 3: 선속도와 주기의 관계 */}
                                                <div 
                                                    className={`p-5 rounded-3xl border-2 transition-all cursor-pointer ${ans3 === 2 ? 'bg-rose-900 border-rose-500 text-white' : 'bg-slate-50 border-transparent shadow-sm'}`}
                                                    onClick={() => setAns3(p => p < 2 ? p + 1 : 2)}
                                                >
                                                    <p className="text-sm font-bold text-rose-500 mb-2 uppercase">Q3. 선속도(v)와 반지름(r)의 관계 ?</p>
                                                    {ans3 === 0 ? (
                                                        <p className="text-[16px] font-black">선속도 v를 반지름 r과 각속도 ω로 나타내면?</p>
                                                    ) : ans3 === 1 ? (
                                                        <p className="text-emerald-400 font-black animate-pulse text-[16px]">"거의 다 왔어요! 한 번만 더."</p>
                                                    ) : (
                                                        <div className="space-y-3">
                                                            <p className="text-[19px] font-black text-rose-100 italic tracking-tighter">"속도의 방향은 원의 <span className="text-rose-300 underline underline-offset-4 decoration-2">접선 방향</span>!"</p>
                                                            <p className="text-[26px] font-black font-serif text-white">v = rω</p>
                                                            <p className="text-[22px] font-bold text-emerald-300 leading-tight">T = 2πr / v = 2π / ω</p>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="space-y-5 animate-in fade-in slide-in-from-left-10 duration-500">
                                                {/* 조절 슬라이더 */}
                                                <div className="space-y-5 p-1">
                                                    <div className="space-y-2">
                                                        <div className="flex justify-between items-end">
                                                            <span className="text-[13px] font-black text-slate-500 tracking-tight uppercase px-2 border-l-4 border-sky-400 leading-none">반지름 (r)</span>
                                                            <input type="number" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-20 h-8 text-lg font-black text-center bg-sky-50 text-sky-700 border-2 border-sky-200 rounded-lg outline-none" />
                                                        </div>
                                                        <input type="range" min="0.1" max="2.0" step="0.1" value={radius} onChange={e=>setRadius(parseFloat(e.target.value))} className="w-full h-2 bg-slate-100 rounded-full appearance-none cursor-pointer accent-sky-600" />
                                                    </div>
                                                    
                                                    <div className="space-y-2">
                                                        <div className="flex justify-between items-end">
                                                            <span className="text-[13px] font-black text-slate-500 tracking-tight uppercase px-2 border-l-4 border-amber-400 leading-none">각속도 (ω)</span>
                                                            <input type="number" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-20 h-8 text-lg font-black text-center bg-amber-50 text-amber-700 border-2 border-amber-200 rounded-lg outline-none" />
                                                        </div>
                                                        <input type="range" min="0.1" max="10.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full h-2 bg-slate-100 rounded-full appearance-none cursor-pointer accent-amber-500" />
                                                    </div>
                                                </div>

                                                {/* 실시간 데이터 카드 */}
                                                <div className="bg-slate-900 p-6 rounded-[32px] text-white space-y-4">
                                                    <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Real-time Dynamics</h4>
                                                    <div className="grid grid-cols-2 gap-4">
                                                        <div className="bg-slate-800 p-4 rounded-3xl border border-slate-700">
                                                            <p className="text-[11px] text-rose-400 font-black mb-1">선속도 (v)</p>
                                                            <p className="text-3xl font-black italic">{(radius * omega).toFixed(2)}<span className="text-xs text-slate-500 ml-1">m/s</span></p>
                                                        </div>
                                                        <div className="bg-slate-800 p-4 rounded-3xl border border-slate-700">
                                                            <p className="text-[11px] text-emerald-400 font-black mb-1">주기 (T)</p>
                                                            <p className="text-3xl font-black italic">{(2 * Math.PI / omega).toFixed(2)}<span className="text-xs text-slate-500 ml-1">s</span></p>
                                                        </div>
                                                    </div>
                                                </div>

                                                {/* 팁 박스 */}
                                                <div className="p-4 bg-blue-50/50 rounded-[28px] border border-blue-100 flex gap-4">
                                                    <Icon name="info" className="text-blue-500 shrink-0" size={24} />
                                                    <p className="text-[13px] font-bold text-blue-700 leading-relaxed">
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
