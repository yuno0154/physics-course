import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    # st.set_page_config is removed as it's handled by main_app.py
    
    # 상단 브랜딩 및 제목
    st.title("🏹 원운동의 가속도: 속도 벡터의 변화와 극한")
    st.markdown("""
    이 시뮬레이션은 등속 원운동에서 **가속도의 방향과 크기**가 어떻게 결정되는지 탐구합니다.
    두 지점에서의 **속도 벡터 차이($\Delta \\vec{v}$)**를 구하고, 시간 간격($\Delta t$)을 줄여가며 **순간 가속도**의 개념을 이해해 보세요.
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
            .vector-label { font-weight: 800; font-style: italic; }
            .toggle-pill { transition: all 0.2s ease; cursor: pointer; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const VectorAccelSim = () => {
                const [theta1, setTheta1] = useState(Math.PI / 4);
                const [dTheta, setDTheta] = useState(0.8);
                const [radius, setRadius] = useState(150);
                const [velMag, setVelMag] = useState(80);
                
                // 벡터 표시 토글 상태
                const [showV1, setShowV1] = useState(true);
                const [showV2, setShowV2] = useState(true);
                const [showDV, setShowDV] = useState(true);

                const theta2 = theta1 - dTheta;
                const centerX = 250;
                const centerY = 250;

                const p1 = { x: centerX + radius * Math.cos(theta1), y: centerY - radius * Math.sin(theta1) };
                const v1 = { x: -velMag * Math.sin(theta1), y: -velMag * Math.cos(theta1) };

                const p2 = { x: centerX + radius * Math.cos(theta2), y: centerY - radius * Math.sin(theta2) };
                const v2 = { x: -velMag * Math.sin(theta2), y: -velMag * Math.cos(theta2) };

                const dv = { x: v2.x - v1.x, y: v2.y - v1.y };

                const svgRef = useRef(null);
                const [isDragging, setIsDragging] = useState(null);

                const handleMouseMove = (e) => {
                    if (!isDragging) return;
                    const rect = svgRef.current.getBoundingClientRect();
                    const x = e.clientX - rect.left - centerX;
                    const y = -(e.clientY - rect.top - centerY);
                    let angle = Math.atan2(y, x);
                    
                    if (isDragging === 'p1') setTheta1(angle);
                    else if (isDragging === 'p2') {
                        let diff = theta1 - angle;
                        if (diff < 0) diff += 2 * Math.PI;
                        if (diff > Math.PI) diff = Math.PI; 
                        setDTheta(diff);
                    }
                };

                return (
                    <div className="flex flex-col items-center bg-transparent min-h-screen p-1 text-slate-800" onMouseMove={handleMouseMove} onMouseUp={() => setIsDragging(null)} onMouseLeave={() => setIsDragging(null)}>
                        <div className="w-full max-w-6xl rounded-[32px] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.15)] border border-slate-200 overflow-hidden bg-white">
                            
                            <div className="grid grid-cols-4 gap-0 bg-slate-900 text-white border-b border-slate-800">
                                <div className="text-center py-4 px-2 border-r border-slate-800/50">
                                    <p className="text-[10px] text-sky-400 font-black uppercase tracking-widest mb-1">시간 간격 (Δt)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-2xl font-black">{dTheta.toFixed(2)}</span>
                                        <span className="text-sm font-bold text-slate-500">rad</span>
                                    </div>
                                </div>
                                <div className="text-center py-4 px-2 border-r border-slate-800/50">
                                    <p className="text-[10px] text-emerald-400 font-black uppercase tracking-widest mb-1">속도 변화량 (|Δv|)</p>
                                    <div className="flex items-center justify-center gap-1 text-2xl font-black">
                                        {(Math.sqrt(dv.x**2 + dv.y**2)/velMag).toFixed(2)}
                                    </div>
                                </div>
                                <div className="text-center py-4 px-2 border-r border-slate-800/50 text-rose-500">
                                    <p className="text-[10px] font-black uppercase tracking-widest mb-1">평균 가속도</p>
                                    <div className="flex items-center justify-center gap-1 text-2xl font-black">
                                        {(Math.sqrt(dv.x**2+dv.y**2)/(velMag*dTheta || 1)).toFixed(2)}
                                    </div>
                                </div>
                                <div className="text-center py-4 px-2 text-amber-400">
                                    <p className="text-[10px] font-black uppercase tracking-widest mb-1">방향 수렴도</p>
                                    <div className="text-sm font-black text-white mt-2">
                                        {dTheta < 0.1 ? "중심 일치" : dTheta < 0.5 ? "중심 근접" : "중심 오차"}
                                    </div>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row min-h-[620px]">
                                <div className="flex-1 bg-slate-50 relative flex flex-col items-center justify-center p-4 border-b lg:border-b-0 lg:border-r-2 border-slate-100">
                                    
                                    {/* 벡터 토글 스위치 */}
                                    <div className="absolute top-6 left-6 flex gap-2 z-10">
                                        <div onClick={()=>setShowV1(!showV1)} className={`px-3 py-1.5 rounded-full text-[11px] font-black border-2 transition-all ${showV1 ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-100' : 'bg-white border-slate-200 text-slate-400'}`}>v₁ 벡터</div>
                                        <div onClick={()=>setShowV2(!showV2)} className={`px-3 py-1.5 rounded-full text-[11px] font-black border-2 transition-all ${showV2 ? 'bg-emerald-500 border-emerald-500 text-white shadow-lg shadow-emerald-100' : 'bg-white border-slate-200 text-slate-400'}`}>v₂ 벡터</div>
                                        <div onClick={()=>setShowDV(!showDV)} className={`px-3 py-1.5 rounded-full text-[11px] font-black border-2 transition-all ${showDV ? 'bg-rose-500 border-rose-500 text-white shadow-lg shadow-rose-100' : 'bg-white border-slate-200 text-slate-400'}`}>Δv 벡터</div>
                                    </div>

                                    <svg ref={svgRef} viewBox="0 0 500 500" className="w-full h-full max-w-[500px] filter drop-shadow-xl select-none">
                                        <defs>
                                            <marker id="arrow-blue" markerWidth="6" markerHeight="6" refX="5" refY="3" orientation="auto">
                                                <path d="M0,0 L6,3 L0,6 Z" fill="#3b82f6" />
                                            </marker>
                                            <marker id="arrow-green" markerWidth="6" markerHeight="6" refX="5" refY="3" orientation="auto">
                                                <path d="M0,0 L6,3 L0,6 Z" fill="#10b981" />
                                            </marker>
                                            <marker id="arrow-red" markerWidth="6" markerHeight="6" refX="5" refY="3" orientation="auto">
                                                <path d="M0,0 L6,3 L0,6 Z" fill="#f43f5e" />
                                            </marker>
                                        </defs>

                                        <circle cx={centerX} cy={centerY} r={radius} fill="none" stroke="#e2e8f0" strokeWidth="2" />
                                        <line x1={centerX-200} y1={centerY} x2={centerX+200} y2={centerY} stroke="#f1f5f9" strokeWidth="1" />
                                        <line x1={centerX} y1={centerY-200} x2={centerX} y2={centerY+200} stroke="#f1f5f9" strokeWidth="1" />
                                        <path d={`M ${centerX} ${centerY} L ${p1.x} ${p1.y} A ${radius} ${radius} 0 0 1 ${p2.x} ${p2.y} Z`} fill="rgba(56, 189, 248, 0.05)" />

                                        {showV1 && (
                                            <g>
                                                <line x1={p1.x} y1={p1.y} x2={p1.x + v1.x} y2={p1.y + v1.y} stroke="#3b82f6" strokeWidth="3" markerEnd="url(#arrow-blue)" />
                                                <text x={p1.x + v1.x * 1.2} y={p1.y + v1.y * 1.2} textAnchor="middle" fill="#3b82f6" className="vector-label text-sm">v₁</text>
                                            </g>
                                        )}

                                        {showV2 && (
                                            <g>
                                                <line x1={p2.x} y1={p2.y} x2={p2.x + v2.x} y2={p2.y + v2.y} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                                <text x={p2.x + v2.x * 1.2} y={p2.y + v2.y * 1.2} textAnchor="middle" fill="#10b981" className="vector-label text-sm">v₂</text>
                                            </g>
                                        )}

                                        {showDV && dTheta > 0.05 && (
                                            <g opacity="0.6">
                                                <line x1={p2.x} y1={p2.y} x2={p2.x - v1.x} y2={p2.y - v1.y} stroke="#3b82f6" strokeWidth="2" strokeDasharray="4,4" />
                                                <line x1={p2.x - v1.x} y1={p2.y - v1.y} x2={p2.x + v2.x} y2={p2.y + v2.y} stroke="#f43f5e" strokeWidth="3" markerEnd="url(#arrow-red)" />
                                            </g>
                                        )}

                                        <circle cx={p1.x} cy={p1.y} r="10" fill="#3b82f6" stroke="white" strokeWidth="3" className="cursor-move" onMouseDown={()=>setIsDragging('p1')} />
                                        <circle cx={p2.x} cy={p2.y} r="10" fill="#10b981" stroke="white" strokeWidth="3" className="cursor-move" onMouseDown={()=>setIsDragging('p2')} />
                                        <circle cx={centerX} cy={centerY} r="4" fill="#0f172a" />

                                        <g transform="translate(360, 40)">
                                            <rect width="120" height="120" rx="20" fill="white" stroke="#f1f5f9" strokeWidth="2" fillOpacity="0.8" />
                                            <text x="60" y="15" textAnchor="middle" className="text-[9px] font-black text-slate-400">벡터 평행이동</text>
                                            <g transform="translate(60, 60)">
                                                <line x1="0" y1="0" x2={v2.x/1.5} y2={v2.y/1.5} stroke="#10b981" strokeWidth="2" markerEnd="url(#arrow-green)" />
                                                <line x1="0" y1="0" x2={-v1.x/1.5} y2={-v1.y/1.5} stroke="#3b82f6" strokeWidth="1.5" strokeDasharray="3,3" opacity="0.4" />
                                                <line x1="0" y1="0" x2={(v2.x-v1.x)/1.5} y2={(v2.y-v1.y)/1.5} stroke="#f43f5e" strokeWidth="2.5" markerEnd="url(#arrow-red)" />
                                            </g>
                                        </g>
                                    </svg>
                                </div>

                                <div className="w-full lg:w-[400px] bg-white flex flex-col p-6 space-y-6 overflow-y-auto no-scrollbar">
                                    <div className="space-y-4">
                                        <h4 className="text-[11px] font-black text-slate-400 uppercase tracking-widest px-1">조절 및 물리량</h4>
                                        <div className="space-y-3">
                                            <div className="flex justify-between items-center">
                                                <span className="text-[13px] font-black text-slate-500 uppercase">시간 간격 (Δθ)</span>
                                                <span className="text-lg font-black text-amber-600">{dTheta.toFixed(2)}</span>
                                            </div>
                                            <input type="range" min="0.01" max="1.5" step="0.01" value={dTheta} onChange={e=>setDTheta(parseFloat(e.target.value))} className="w-full h-2 bg-slate-100 rounded-full appearance-none cursor-pointer accent-amber-500" />
                                        </div>
                                    </div>

                                    <div className="p-5 bg-slate-900 rounded-[28px] shadow-xl space-y-4">
                                        <div className="bg-white/5 p-4 rounded-2xl border border-white/10">
                                            <p className="text-white text-[15px] font-bold leading-tight mb-2">가속도의 방향</p>
                                            <p className="text-amber-400 text-[12px] leading-relaxed">
                                                Δt 가 줄어들수록 속도 변화량 Δv 의 방향은 원의 중심을 향하게 됩니다. 이것이 곧 등속 원운동의 가속도 방향입니다.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<VectorAccelSim />);
        </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트로 HTML 삽입
    components.html(react_code, height=820, scrolling=False)

if __name__ == "__main__":
    run_sim()
