import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.title("🏀 [심화 탐구] 원운동의 벡터 및 성분 분석")
    st.markdown("""
    이 시뮬레이션은 등속 원운동의 **속도 벡터 성분(Vx, Vy) 시각화**와 **수동 조작** 기능을 제공합니다.
    우측의 설정 패널에서 각 벡터를 개별적으로 켜고 끌 수 있으며, 수동 모드에서 물체를 직접 돌려볼 수 있습니다.
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
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; overflow: hidden; }
            .no-scrollbar::-webkit-scrollbar { display: none; }
            input[type="range"] { height: 6px; -webkit-appearance: none; background: #e2e8f0; border-radius: 10px; }
            input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; background: #3b82f6; border-radius: 50%; cursor: pointer; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        </style>
    </head>
    <body>
        <div id="root"></div>
        <script type="text/babel">
            const { useState, useEffect, useRef, useCallback } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => { if (window.lucide) window.lucide.createIcons(); }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const CircularMotionV3 = () => {
                const [isPlaying, setIsPlaying] = useState(true);
                const [isManual, setIsManual] = useState(false);
                const [radius, setRadius] = useState(120);
                const [omega, setOmega] = useState(1.5);
                const [angle, setAngle] = useState(0);
                
                const [showPosition, setShowPosition] = useState(true);
                const [showVelocity, setShowVelocity] = useState(true);
                const [showAccel, setShowAccel] = useState(false);
                const [showComponents, setShowComponents] = useState(true);
                
                const [activeTab, setActiveTab] = useState('settings');
                const [isDragging, setIsDragging] = useState(false);
                
                const svgRef = useRef(null);
                const requestRef = useRef();
                const lastTimeRef = useRef();

                const animate = (time) => {
                    if (lastTimeRef.current !== undefined && isPlaying && !isManual && !isDragging) {
                        const deltaTime = (time - lastTimeRef.current) / 1000;
                        setAngle((prev) => (prev + omega * deltaTime) % (Math.PI * 2));
                    }
                    lastTimeRef.current = time;
                    requestRef.current = requestAnimationFrame(animate);
                };

                useEffect(() => {
                    requestRef.current = requestAnimationFrame(animate);
                    return () => cancelAnimationFrame(requestRef.current);
                }, [isPlaying, isManual, omega, isDragging]);

                const CX = 250; const CY = 220;
                
                const x = radius * Math.cos(angle);
                const y = radius * Math.sin(angle);
                
                const vMag = radius * omega * 0.8; 
                const vx = -vMag * Math.sin(angle);
                const vy = vMag * Math.cos(angle);
                
                const aMag = radius * omega * omega * 0.2;
                const ax = -aMag * Math.cos(angle);
                const ay = -aMag * Math.sin(angle);

                const handleMouseDown = (e) => {
                    if (!isManual) return;
                    setIsDragging(true);
                    updateAngleFromEvent(e);
                };

                const updateAngleFromEvent = useCallback((e) => {
                    if (!svgRef.current) return;
                    const rect = svgRef.current.getBoundingClientRect();
                    const mouseX = e.clientX - rect.left;
                    const mouseY = e.clientY - rect.top;
                    const svgX = (mouseX / rect.width) * 500;
                    const svgY = (mouseY / rect.height) * 450;
                    const newAngle = Math.atan2(svgY - CY, svgX - CX);
                    setAngle(newAngle);
                }, [CX, CY]);

                useEffect(() => {
                    const handleMouseMove = (e) => { if (isDragging) updateAngleFromEvent(e); };
                    const handleMouseUp = () => { setIsDragging(false); };
                    if (isDragging) {
                        window.addEventListener('mousemove', handleMouseMove);
                        window.addEventListener('mouseup', handleMouseUp);
                    }
                    return () => {
                        window.removeEventListener('mousemove', handleMouseMove);
                        window.removeEventListener('mouseup', handleMouseUp);
                    };
                }, [isDragging, updateAngleFromEvent]);

                const handleReset = () => { setAngle(0); setIsPlaying(true); setIsDragging(false); };

                return (
                    <div className="flex flex-col bg-slate-50 min-h-screen p-4 text-slate-800">
                        <div className="w-full max-w-6xl mx-auto bg-white rounded-[2.5rem] shadow-2xl border border-slate-200 overflow-hidden flex flex-col">
                            <div className="flex items-center justify-between px-8 py-5 bg-slate-900 text-white">
                                <div className="flex items-center gap-4">
                                    <div className={`p-3 rounded-2xl ${isPlaying && !isManual ? 'bg-emerald-500 animate-pulse' : 'bg-slate-700'}`}>
                                        <Icon name={isPlaying && !isManual ? "zap" : "pause"} size={20} />
                                    </div>
                                    <div>
                                        <h2 className="text-lg font-black tracking-tight">Circular Motion Analysis</h2>
                                        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">속도 성분 및 수동 조작 모드</p>
                                    </div>
                                </div>
                                <div className="flex gap-4">
                                    <button onClick={() => setIsManual(!isManual)} className={`px-4 py-2 rounded-xl text-xs font-black transition-all border-2 ${isManual ? 'bg-amber-500 border-amber-500 text-white shadow-lg' : 'bg-transparent border-slate-700 text-slate-400 hover:border-slate-500'}`}>{isManual ? 'MANUAL' : 'AUTO'}</button>
                                    <button onClick={() => setIsPlaying(!isPlaying)} className={`w-10 h-10 rounded-xl flex items-center justify-center transition-all ${isPlaying ? 'bg-slate-700 hover:bg-slate-600' : 'bg-emerald-500 hover:bg-emerald-600'}`}><Icon name={isPlaying ? "pause" : "play"} size={18} /></button>
                                    <button onClick={handleReset} className="w-10 h-10 rounded-xl bg-slate-700 hover:bg-slate-600 flex items-center justify-center"><Icon name="refresh-cw" size={18} /></button>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row h-[580px]">
                                <div className="flex-1 bg-white relative overflow-hidden flex items-center justify-center border-r">
                                    <svg ref={svgRef} viewBox="0 0 500 450" className={`w-full h-full max-w-[500px] select-none ${isManual ? 'cursor-move' : ''}`} onMouseDown={handleMouseDown}>
                                        <line x1="50" y1={CY} x2="450" y2={CY} stroke="#f1f5f9" strokeWidth="2" strokeDasharray="4,4" />
                                        <line x1={CX} y1="50" x2={CX} y2="400" stroke="#f1f5f9" strokeWidth="2" strokeDasharray="4,4" />
                                        <circle cx={CX} cy={CY} r={radius} fill="none" stroke="#e2e8f0" strokeWidth="1.5" strokeDasharray="5,5" />
                                        
                                        {showPosition && <line x1={CX} y1={CY} x2={CX + x} y2={CY + y} stroke="#3b82f6" strokeWidth="2.5" markerEnd="url(#arrow-blue)" />}
                                        {showAccel && <line x1={CX + x} y1={CY + y} x2={CX + x + ax} y2={CY + y + ay} stroke="#ef4444" strokeWidth="3" markerEnd="url(#arrow-red)" />}
                                        {showComponents && (
                                            <g opacity="0.6">
                                                <line x1={CX + x} y1={CY + y} x2={CX + x + vx} y2={CY + y} stroke="#10b981" strokeWidth="6" strokeLinecap="round" />
                                                <text x={CX + x + vx} y={CY + y - 12} textAnchor="middle" className="fill-emerald-600 text-[11px] font-black italic shadow-white">Vx</text>
                                                <line x1={CX + x} y1={CY + y} x2={CX + x} y2={CY + y + vy} stroke="#059669" strokeWidth="6" strokeLinecap="round" />
                                                <text x={CX + x + 12} y={CY + y + vy} dominantBaseline="middle" className="fill-emerald-800 text-[11px] font-black italic text-stroke">Vy</text>
                                            </g>
                                        )}
                                        {showVelocity && <line x1={CX + x} y1={CY + y} x2={CX + x + vx} y2={CY + y + vy} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />}
                                        <circle cx={CX + x} cy={CY + y} r="10" fill="#0f172a" className={isDragging ? 'fill-blue-600' : ''} />
                                        <defs>
                                            <marker id="arrow-green" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#10b981"/></marker>
                                            <marker id="arrow-blue" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#3b82f6"/></marker>
                                            <marker id="arrow-red" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#ef4444"/></marker>
                                        </defs>
                                    </svg>
                                    <div className="absolute top-8 left-8 flex flex-col gap-2">
                                        <div className="px-4 py-2 bg-white/95 backdrop-blur border rounded-2xl shadow-sm"><div className="text-[9px] font-black text-slate-400 mb-1">POSITION</div><div className="text-xs font-black text-blue-600">({x.toFixed(1)}, {y.toFixed(1)})</div></div>
                                        <div className="px-4 py-2 bg-white/95 backdrop-blur border rounded-2xl shadow-sm"><div className="text-[9px] font-black text-slate-400 mb-1">VELOCITY</div><div className="text-xs font-black text-emerald-600">({(vx/0.8).toFixed(1)}, {(vy/0.8).toFixed(1)})</div></div>
                                    </div>
                                    {isManual && <div className="absolute bottom-8 bg-amber-500 text-white px-6 py-2 rounded-full text-xs font-black animate-bounce shadow-xl shadow-amber-200">드래그하여 직접 돌려보세요!</div>}
                                </div>

                                <div className="w-full lg:w-80 bg-slate-50 flex flex-col border-l">
                                    <div className="flex border-b bg-white">
                                        <button onClick={()=>setActiveTab('settings')} className={`flex-1 py-4 font-black text-[10px] tracking-widest ${activeTab==='settings'?'text-blue-600 border-b-2 border-blue-600':'text-slate-400'}`}>SETTINGS</button>
                                        <button onClick={()=>setActiveTab('vectors')} className={`flex-1 py-4 font-black text-[10px] tracking-widest ${activeTab==='vectors'?'text-blue-600 border-b-2 border-blue-600':'text-slate-400'}`}>VECTORS</button>
                                    </div>
                                    <div className="p-6 space-y-8 overflow-y-auto no-scrollbar flex-1">
                                        {activeTab==='settings' ? (
                                            <div className="space-y-8">
                                                <div className="space-y-3">
                                                    <div className="flex justify-between items-end"><span className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">Radius (r)</span><span className="text-sm font-black text-blue-600">{radius}</span></div>
                                                    <input type="range" min="50" max="200" value={radius} onChange={e=>setRadius(parseInt(e.target.value))} className="w-full" />
                                                </div>
                                                <div className="space-y-3">
                                                    <div className="flex justify-between items-end"><span className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">Angular Speed (ω)</span><span className="text-sm font-black text-emerald-600">{omega.toFixed(1)}</span></div>
                                                    <input type="range" min="0.1" max="4.0" step="0.1" value={omega} onChange={e=>setOmega(parseFloat(e.target.value))} className="w-full" />
                                                </div>
                                                <div className="p-5 bg-slate-900 rounded-[2rem] text-white shadow-xl shadow-slate-200">
                                                    <div className="text-[9px] font-black text-slate-500 uppercase mb-3 tracking-tighter">SPEED v = rω</div>
                                                    <div className="text-3xl font-black text-emerald-400 italic">{(radius * omega).toFixed(1)} <span className="text-xs text-slate-500 font-normal ml-1">px/s</span></div>
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="space-y-3">
                                                <p className="text-[10px] font-black text-slate-400 tracking-widest mb-2 uppercase">VISUALIZATION</p>
                                                {[
                                                    {id: 'pos', label: '위치 벡터 (Position)', state: showPosition, set: setShowPosition, color: 'text-blue-600', icon: 'map-pin'},
                                                    {id: 'vel', label: '속도 벡터 (Velocity)', state: showVelocity, set: setShowVelocity, color: 'text-emerald-600', icon: 'zap'},
                                                    {id: 'comp', label: '속도 성분 (vx, vy)', state: showComponents, set: setShowComponents, color: 'text-teal-600', icon: 'layers'},
                                                    {id: 'acc', label: '가속도 벡터 (Accel)', state: showAccel, set: setShowAccel, color: 'text-rose-500', icon: 'target'}
                                                ].map(item => (
                                                    <label key={item.id} className={`flex items-center justify-between p-4 bg-white rounded-2xl border transition-all cursor-pointer ${item.state ? 'border-blue-200 shadow-md ring-1 ring-blue-50' : 'border-slate-100 opacity-60'}`}>
                                                        <div className="flex items-center gap-3">
                                                            <div className={`w-8 h-8 rounded-xl flex items-center justify-center ${item.state ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-400'}`}><Icon name={item.icon} size={14} /></div>
                                                            <span className={`text-[11px] font-black ${item.state ? 'text-slate-800' : 'text-slate-400'}`}>{item.label}</span>
                                                        </div>
                                                        <input type="checkbox" checked={item.state} onChange={() => item.set(!item.state)} className="w-4 h-4 rounded border-slate-300" />
                                                    </label>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                    <div className="p-6 bg-white border-t">
                                        <div className="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-2">Analysis Note</div>
                                        <p className="text-[10px] text-slate-600 leading-relaxed">
                                            속도 벡터 <span className="font-bold">v</span>는 항상 접선 방향이며, 
                                            수평 성분 <span className="font-bold text-emerald-600">vx = -v sin ωt</span>와 
                                            수직 성분 <span className="font-bold text-emerald-800">vy = v cos ωt</span>로 분해됩니다.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<CircularMotionV3 />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=720, scrolling=False)

if __name__ == "__main__":
    run_sim()
