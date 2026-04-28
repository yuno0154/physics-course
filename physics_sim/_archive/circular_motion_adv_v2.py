import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    
    st.title("🏀 [수행평가 1-3] 등속 원운동 심화 탐구 (Advanced Study)")
    st.markdown("""
    이 시뮬레이션은 등속 원운동의 상급 개념인 **라디안의 정의, 반경에 따른 속도 관계, 그리고 가속도 벡터의 증명**을 위해 제작되었습니다. 
    우측 상단의 **'학습 활동지'** 탭을 클릭하여 각 탐구 단계의 미션을 확인하세요.
    """)

    react_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
            body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; overflow: hidden; }
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

            const CircularMotionAdvanced = () => {
                const [mode, setMode] = useState(1);
                const [isPaused, setIsPaused] = useState(false);
                const [isCut, setIsCut] = useState(false);
                const [activeTab, setActiveTab] = useState('settings');
                const [radius, setRadius] = useState(120);
                const [theta, setTheta] = useState(1.0);
                const [omega, setOmega] = useState(1.5);
                const [angle, setAngle] = useState(0);
                const [elapsedTimeAfterCut, setElapsedTimeAfterCut] = useState(0);
                const [cutState, setCutState] = useState({ pos: { x: 0, y: 0 }, vel: { x: 0, y: 0 } });
                const [savedVectors, setSavedVectors] = useState([]);
                
                const requestRef = useRef();
                const lastTimeRef = useRef();

                const animate = (time) => {
                    if (lastTimeRef.current !== undefined && !isPaused) {
                        const deltaTime = (time - lastTimeRef.current) / 1000;
                        if (!isCut) {
                            setAngle((prev) => (prev + (mode === 1 ? 0 : omega) * deltaTime) % (Math.PI * 2));
                        } else {
                            setElapsedTimeAfterCut((prev) => prev + deltaTime);
                        }
                    }
                    lastTimeRef.current = time;
                    requestRef.current = requestAnimationFrame(animate);
                };

                useEffect(() => {
                    requestRef.current = requestAnimationFrame(animate);
                    return () => cancelAnimationFrame(requestRef.current);
                }, [isPaused, isCut, mode, omega]);

                const handleReset = () => {
                    setIsCut(false); setAngle(0); setElapsedTimeAfterCut(0); setSavedVectors([]); setIsPaused(false);
                };

                const handleCut = () => {
                    const x = radius * Math.cos(angle); const y = radius * Math.sin(angle);
                    const v = radius * omega; const vx = -v * Math.sin(angle); const vy = v * Math.cos(angle);
                    setCutState({ pos: { x, y }, vel: { x: vx, y: vy } });
                    setIsCut(true);
                };

                const saveVector = () => {
                    if (savedVectors.length >= 2) setSavedVectors([]);
                    const v = radius * omega;
                    setSavedVectors(prev => [...prev, {
                        pos: { x: radius * Math.cos(angle), y: radius * Math.sin(angle) },
                        vel: { x: -v * Math.sin(angle), y: v * Math.cos(angle) }
                    }]);
                };

                const CX = 250; const CY = 220;

                return (
                    <div className="flex flex-col bg-white min-h-screen p-4 text-slate-800">
                        <div className="w-full max-w-6xl mx-auto bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col">
                            <div className="flex bg-slate-100 p-2 gap-2 border-b">
                              {[{id:1,l:'Radian',i:'layers'},{id:2,l:'v=rw',i:'zap'},{id:3,l:'Accel',i:'scissors'}].map(m=>(
                                <button key={m.id} onClick={()=>{setMode(m.id);handleReset();}} className={`flex-1 py-3 rounded-xl font-black text-xs ${mode===m.id?'bg-white shadow text-blue-600':'text-slate-400'}`}>
                                  <Icon name={m.i} size={14}/> {m.l}
                                </button>
                              ))}
                            </div>

                            <div className="flex flex-col lg:flex-row h-[520px]">
                                <div className="flex-1 bg-white relative overflow-hidden flex items-center justify-center border-r">
                                    <svg viewBox="0 0 500 450" className="w-full h-full max-w-[500px]">
                                        <circle cx={CX} cy={CY} r="2" fill="#94a3b8" />
                                        <circle cx={CX} cy={CY} r={radius} fill="none" stroke="#334155" strokeWidth="2.5" strokeDasharray="4,4" />
                                        {mode===1 && (
                                            <g>
                                                <path d={`M ${CX} ${CY} L ${CX+radius} ${CY} A ${radius} ${radius} 0 ${theta > Math.PI ? 1 : 0} 1 ${CX + radius * Math.cos(theta)} ${CY + radius * Math.sin(theta)} Z`} fill="rgba(59, 130, 246, 0.1)" stroke="#3b82f6" strokeWidth="2" />
                                                <path d={`M ${CX+radius} ${CY} A ${radius} ${radius} 0 ${theta > Math.PI ? 1 : 0} 1 ${CX+radius*Math.cos(theta)} ${CY+radius*Math.sin(theta)}`} fill="none" stroke="#ef4444" strokeWidth="5" strokeLinecap="round" />
                                            </g>
                                        )}
                                        {mode===2 && (
                                            <g>
                                              {[radius, radius*0.6].map((r,i)=>(
                                                 <g key={i}>
                                                    <circle cx={CX} cy={CY} r={r} fill="none" stroke="#334155" strokeWidth="1" strokeDasharray="4,4" />
                                                    <line x1={CX+r*Math.cos(angle)} y1={CY+r*Math.sin(angle)} x2={CX+r*Math.cos(angle)-(r*omega*0.4)*Math.sin(angle)} y2={CY+r*Math.sin(angle)+(r*omega*0.4)*Math.cos(angle)} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                                    <circle cx={CX+r*Math.cos(angle)} cy={CY+r*Math.sin(angle)} r="8" fill={i===0?"#1e293b":"#64748b"} />
                                                 </g>
                                              ))}
                                            </g>
                                        )}
                                        {mode===3 && (
                                            <g>
                                              {!isCut ? (
                                                <g>
                                                  <line x1={CX+radius*Math.cos(angle)} y1={CY+radius*Math.sin(angle)} x2={CX+radius*Math.cos(angle)-(radius*omega*0.5)*Math.sin(angle)} y2={CY+radius*Math.sin(angle)+(radius*omega*0.5)*Math.cos(angle)} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                                  <line x1={CX+radius*Math.cos(angle)} y1={CY+radius*Math.sin(angle)} x2={CX+radius*Math.cos(angle)+radius*omega*0.3*-Math.cos(angle)} y2={CY+radius*Math.sin(angle)+radius*omega*0.3*-Math.sin(angle)} stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrow-red)" />
                                                  <circle cx={CX+radius*Math.cos(angle)} cy={CY+radius*Math.sin(angle)} r="10" fill="#0f172a" />
                                                </g>
                                              ): (
                                                <circle cx={CX+cutState.pos.x+cutState.vel.x*elapsedTimeAfterCut} cy={CY+cutState.pos.y+cutState.vel.y*elapsedTimeAfterCut} r="10" fill="#64748b" />
                                              )}
                                            </g>
                                        )}
                                        <defs>
                                            <marker id="arrow-green" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#10b981"/></marker>
                                            <marker id="arrow-red" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#ef4444"/></marker>
                                        </defs>
                                    </svg>
                                    <div className="absolute top-8 left-8 p-4 bg-white/90 border rounded-2xl">
                                      <div className="text-xl font-black">{mode===1?`s = ${(radius*theta).toFixed(1)}`:mode===2?`v = ${(radius*omega).toFixed(1)}`:'a = v²/r'}</div>
                                    </div>
                                </div>
                                <div className="w-full lg:w-80 bg-slate-50 flex flex-col border-l">
                                    <div className="flex border-b">
                                        <button onClick={()=>setActiveTab('settings')} className={`flex-1 py-4 font-bold text-xs ${activeTab==='settings'?'text-blue-600 border-b-2 border-blue-600':'text-slate-400'}`}>설정</button>
                                        <button onClick={()=>setActiveTab('activity')} className={`flex-1 py-4 font-bold text-xs ${activeTab==='activity'?'text-emerald-600 border-b-2 border-emerald-600':'text-slate-400'}`}>활동지</button>
                                    </div>
                                    <div className="p-6 space-y-6 overflow-y-auto no-scrollbar">
                                        {activeTab==='settings' ? (
                                            <div className="space-y-6">
                                                <div className="space-y-1">
                                                  <div className="flex justify-between text-xs font-bold text-slate-400"><span>Radius</span><span>{radius} px</span></div>
                                                  <input type="range" min="50" max="200" value={radius} onChange={e=>setRadius(parseInt(e.target.value))} className="w-full accent-blue-600" />
                                                </div>
                                                <div className="grid grid-cols-2 gap-2">
                                                   <button onClick={()=>setIsPaused(!isPaused)} className="py-2 bg-white border rounded-xl text-xs font-bold">{isPaused?'Play':'Pause'}</button>
                                                   <button onClick={handleReset} className="py-2 bg-white border rounded-xl text-xs font-bold">Reset</button>
                                                </div>
                                                {mode===3 && <button onClick={handleCut} className="w-full py-3 bg-rose-500 text-white rounded-xl text-xs font-black shadow-lg shadow-rose-100">실 끊기 (관성)</button>}
                                            </div>
                                        ) : (
                                            <div className="space-y-4">
                                                <div className="p-3 bg-white border border-slate-200 rounded-2xl text-[11px] leading-relaxed">
                                                  <div className="font-bold text-blue-600 mb-1">Step 1. 수학적 기초</div>
                                                  s = r (1 rad) 인 순간을 찾아보세요.
                                                </div>
                                                <div className="p-3 bg-white border border-slate-200 rounded-2xl text-[11px] leading-relaxed">
                                                  <div className="font-bold text-emerald-600 mb-1">Step 2. 선속도 분석</div>
                                                  v = rω 관계를 화살표 길이로 증명하세요.
                                                </div>
                                                <div className="p-3 bg-slate-800 text-white rounded-2xl text-[11px] leading-relaxed">
                                                  <div className="font-bold text-rose-300 mb-1">Final Mission. 안전 설계</div>
                                                  빗길 커브 도로 설계 비법은?
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
            root.render(<CircularMotionAdvanced />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=720, scrolling=False)

if __name__ == "__main__":
    run_sim()
