import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    # st.set_page_config is removed as it's handled by main_app.py
    
    # 상단 브랜딩 및 제목
    st.title("🏹 원운동의 가속도: 속도 벡터의 변화와 극한")
    st.markdown("""
    이 시뮬레이션은 등속 원운동에서 **가속도의 방향과 크기**가 어떻게 결정되는지 탐구합니다.
    두 지점에서의 **속도 벡터 차이($\\Delta \\vec{v} = \\vec{v}_2 - \\vec{v}_1$)**를 구하고, 시간 간격($\\Delta t$)을 줄여가며 **순간 가속도**의 개념을 이해해 보세요.
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
            .math-font { font-family: 'Times New Roman', serif; font-style: italic; font-weight: bold; }
            .vector-label { font-weight: 800; font-style: italic; }
            .zoom-transition { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
            .math-card { background: rgba(15, 23, 42, 0.02); border: 1px solid rgba(15, 23, 42, 0.05); border-radius: 20px; transition: all 0.3s; }
            .math-card:hover { background: white; shadow: 0 10px 20px -5px rgba(0,0,0,0.05); border-color: rgba(37, 99, 235, 0.2); }
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

            const MathSymbol = ({ text, color = "#1e293b" }) => (
                <span className="math-font px-0.5" style={{ color }}>{text}</span>
            );

            const VectorAccelSim = () => {
                const [theta1, setTheta1] = useState(Math.PI / 4);
                const [dTheta, setDTheta] = useState(0.8);
                const [radius, setRadius] = useState(150);
                const [velMag, setVelMag] = useState(80);
                const [isZoomed, setIsZoomed] = useState(false);
                
                const [showV1, setShowV1] = useState(true);
                const [showV2, setShowV2] = useState(true);
                const [showDV, setShowDV] = useState(true);

                // 반시계 방향(CCW) 운동: theta2가 theta1보다 앞선 각도
                const theta2 = theta1 + dTheta;
                const centerX = 250;
                const centerY = 250;

                // 위치 벡터 p (SVG y축 반전 고려)
                const p1 = { x: centerX + radius * Math.cos(theta1), y: centerY - radius * Math.sin(theta1) };
                const p2 = { x: centerX + radius * Math.cos(theta2), y: centerY - radius * Math.sin(theta2) };

                // 속도 벡터 v: r(t) = (r cos wt, r sin wt) -> v(t) = (-rw sin wt, rw cos wt)
                // SVG y축 반전 때문에 v_y 성분의 부호가 계산과 반대로 적용됨
                const v1 = { x: -velMag * Math.sin(theta1), y: -velMag * Math.cos(theta1) };
                const v2 = { x: -velMag * Math.sin(theta2), y: -velMag * Math.cos(theta2) };

                // Δv = v2 - v1 (나중 속도 - 처음 속도)
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
                        let diff = angle - theta1;
                        while (diff < 0) diff += 2 * Math.PI;
                        while (diff > 2 * Math.PI) diff -= 2 * Math.PI;
                        if (diff > Math.PI) diff = Math.PI; 
                        setDTheta(diff);
                    }
                };

                return (
                    <div className="flex flex-col items-center bg-transparent min-h-screen p-1 text-slate-800" onMouseMove={handleMouseMove} onMouseUp={() => setIsDragging(null)} onMouseLeave={() => setIsDragging(null)}>
                        <div className="w-full max-w-6xl rounded-[32px] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.15)] border border-slate-200 overflow-hidden bg-white mb-8">
                            
                            <div className="grid grid-cols-4 gap-0 bg-slate-900 text-white border-b border-slate-800 font-bold">
                                <div className="text-center py-4 px-2 border-r border-slate-800/50">
                                    <p className="text-[10px] text-sky-400 font-black uppercase tracking-widest mb-1">시간 간격 (Δt)</p>
                                    <div className="flex items-center justify-center gap-1"><span className="text-2xl">{dTheta.toFixed(2)}</span><span className="text-sm text-slate-500">rad</span></div>
                                </div>
                                <div className="text-center py-4 px-2 border-r border-slate-800/50 text-emerald-400">
                                    <p className="text-[10px] font-black uppercase tracking-widest mb-1">속도 변화량 (|Δv|)</p>
                                    <div className="flex items-center justify-center gap-1 text-2xl font-black">{(Math.sqrt(dv.x**2 + dv.y**2)/velMag).toFixed(2)}</div>
                                </div>
                                <div className="text-center py-4 px-2 border-r border-slate-800/50 text-rose-500">
                                    <p className="text-[10px] font-black uppercase tracking-widest mb-1">평균 가속도</p>
                                    <div className="flex items-center justify-center gap-1 text-2xl">{(Math.sqrt(dv.x**2+dv.y**2)/(velMag*dTheta || 1)).toFixed(2)}</div>
                                </div>
                                <div className="text-center py-4 px-2 text-amber-400">
                                    <p className="text-[10px] font-black uppercase tracking-widest mb-1">운동 방향</p>
                                    <div className="text-sm font-black text-white mt-1">반시계 방향 (CCW)</div>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row min-h-[620px]">
                                <div className="flex-1 bg-slate-50 relative flex flex-col items-center justify-center p-4 border-b lg:border-b-0 lg:border-r-2 border-slate-100">
                                    <div className="absolute top-6 left-6 flex gap-2 z-10 w-full pl-6">
                                        <div onClick={()=>setShowV1(!showV1)} className={`px-4 py-1.5 rounded-full text-[11px] font-black border-2 cursor-pointer transition-all ${showV1 ? 'bg-blue-600 border-blue-600 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>처음 속도 v₁</div>
                                        <div onClick={()=>setShowV2(!showV2)} className={`px-4 py-1.5 rounded-full text-[11px] font-black border-2 cursor-pointer transition-all ${showV2 ? 'bg-emerald-500 border-emerald-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>나중 속도 v₂</div>
                                        <div onClick={()=>setShowDV(!showDV)} className={`px-4 py-1.5 rounded-full text-[11px] font-black border-2 cursor-pointer transition-all ${showDV ? 'bg-rose-500 border-rose-500 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400'}`}>속도 변화 Δv</div>
                                    </div>

                                    <svg ref={svgRef} viewBox="0 0 500 500" className="w-full h-full max-w-[500px] select-none">
                                        <defs>
                                            <marker id="arrow-blue" markerWidth="5" markerHeight="5" refX="4.5" refY="2.5" orientation="auto"><path d="M0,0 L5,2.5 L0,5 Z" fill="#3b82f6" /></marker>
                                            <marker id="arrow-green" markerWidth="5" markerHeight="5" refX="4.5" refY="2.5" orientation="auto"><path d="M0,0 L5,2.5 L0,5 Z" fill="#10b981" /></marker>
                                            <marker id="arrow-red" markerWidth="5" markerHeight="5" refX="4.5" refY="2.5" orientation="auto"><path d="M0,0 L5,2.5 L0,5 Z" fill="#f43f5e" /></marker>
                                        </defs>
                                        <circle cx={centerX} cy={centerY} r={radius} fill="none" stroke="#e2e8f0" strokeWidth="2" strokeDasharray="4,4" />
                                        <line x1={centerX-200} y1={centerY} x2={centerX+200} y2={centerY} stroke="#cbd5e1" strokeWidth="1" opacity="0.3" />
                                        <line x1={centerX} y1={centerY-200} x2={centerX} y2={centerY+200} stroke="#cbd5e1" strokeWidth="1" opacity="0.3" />

                                        {showV1 && (<g><line x1={p1.x} y1={p1.y} x2={p1.x + v1.x} y2={p1.y + v1.y} stroke="#3b82f6" strokeWidth="2" markerEnd="url(#arrow-blue)" /><text x={p1.x + v1.x * 1.3} y={p1.y + v1.y * 1.3} textAnchor="middle" fill="#3b82f6" className="vector-label text-[11px]">v₁</text></g>)}
                                        {showV2 && (<g><line x1={p2.x} y1={p2.y} x2={p2.x + v2.x} y2={p2.y + v2.y} stroke="#10b981" strokeWidth="2" markerEnd="url(#arrow-green)" /><text x={p2.x + v2.x * 1.3} y={p2.y + v2.y * 1.3} textAnchor="middle" fill="#10b981" className="vector-label text-[11px]">v₂</text></g>)}
                                        
                                        <circle cx={p1.x} cy={p1.y} r="8" fill="#3b82f6" stroke="white" strokeWidth="3" className="cursor-move shadow-md" onMouseDown={()=>setIsDragging('p1')} />
                                        <circle cx={p2.x} cy={p2.y} r="8" fill="#10b981" stroke="white" strokeWidth="3" className="cursor-move shadow-md" onMouseDown={()=>setIsDragging('p2')} />
                                        <circle cx={centerX} cy={centerY} r="4" fill="#0f172a" />

                                        {/* 벡터 분산 상세 박스 (확대 지원) */}
                                        <g transform={`translate(${isZoomed ? 50 : 350}, ${isZoomed ? 50 : 350})`} className="zoom-transition cursor-pointer" onClick={() => setIsZoomed(!isZoomed)}>
                                            <rect width={isZoomed ? 400 : 130} height={isZoomed ? 400 : 130} rx="24" fill="white" stroke="#cbd5e1" strokeWidth="1" fillOpacity="0.98" className="shadow-2xl" />
                                            <text x={isZoomed ? 200 : 65} y="22" textAnchor="middle" className={`font-black text-slate-400 ${isZoomed ? 'text-base' : 'text-[9px]'}`}>
                                                {isZoomed ? "속도 변화 관찰: Δv = v₂ - v₁" : "벡터 상세 관찰"}
                                            </text>
                                            
                                            <g transform={`translate(${isZoomed ? 200 : 65}, ${isZoomed ? 200 : 70}) scale(${isZoomed ? 2.5 : 1})`}>
                                                {/* v1 벡터 (시작점) */}
                                                <line x1="0" y1="0" x2={v1.x/1.5} y2={v1.y/1.5} stroke="#3b82f6" strokeWidth="1.5" strokeDasharray="3,2" markerEnd="url(#arrow-blue)" opacity="0.6" />
                                                {/* v2 벡터 (같은 원점 시작) */}
                                                <line x1="0" y1="0" x2={v2.x/1.5} y2={v2.y/1.5} stroke="#10b981" strokeWidth="1.5" markerEnd="url(#arrow-green)" />
                                                
                                                {/* Δv 벡터 (v1의 끝에서 v2의 끝으로) */}
                                                <line x1={v1.x/1.5} y1={v1.y/1.5} x2={v2.x/1.5} y2={v2.y/1.5} stroke="#f43f5e" strokeWidth="2.5" markerEnd="url(#arrow-red)" />
                                                
                                                {isZoomed && (
                                                    <g>
                                                        <text x={v1.x/1.8} y={v1.y/1.8} dx="-10" className="text-[6px] fill-blue-600 font-bold">v₁</text>
                                                        <text x={v2.x/1.8} y={v2.y/1.8} dx="10" className="text-[6px] fill-emerald-600 font-bold">v₂</text>
                                                        <text x={(v1.x+v2.x)/3} y={(v1.y+v2.y)/3} dy="-5" className="text-[7px] fill-rose-600 font-black">Δv</text>
                                                    </g>
                                                )}
                                            </g>
                                        </g>
                                    </svg>
                                </div>

                                <div className="w-full lg:w-[400px] bg-white flex flex-col p-6 space-y-6">
                                    <div className="space-y-4">
                                        <h4 className="text-[11px] font-black text-slate-400 uppercase tracking-widest px-1 border-l-4 border-sky-500 pl-3">물리 분석 가이드</h4>
                                        <div className="space-y-4">
                                            <div className="math-card p-4">
                                                <div className="flex gap-3">
                                                    <span className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-[11px] font-black shrink-0">1</span>
                                                    <div className="text-[13px] font-bold text-slate-700 leading-snug">가속도 <MathSymbol text="a" color="#f43f5e"/>는 속도 변화량 <MathSymbol text="Δv"/>을 시간 <MathSymbol text="Δt"/>으로 나눈 값입니다.</div>
                                                </div>
                                            </div>
                                            <div className="math-card p-4">
                                                <div className="flex gap-3">
                                                    <span className="w-6 h-6 rounded-full bg-emerald-500 text-white flex items-center justify-center text-[11px] font-black shrink-0">2</span>
                                                    <div className="text-[13px] font-bold text-slate-700 leading-snug">벡터 뺄셈 <MathSymbol text="Δv = v₂ - v₁"/>은 <MathSymbol text="v₁"/>의 끝에서 <MathSymbol text="v₂"/>의 끝을 잇는 화살표입니다.</div>
                                                </div>
                                            </div>
                                            <div className="math-card p-4">
                                                <div className="flex gap-3">
                                                    <span className="w-6 h-6 rounded-full bg-amber-500 text-white flex items-center justify-center text-[11px] font-black shrink-0">3</span>
                                                    <div className="text-[13px] font-bold text-slate-700 leading-snug">가속도 식에 대입하면: <br/><MathSymbol text="a = (v·Δθ) / Δt"/> 가 됩니다.</div>
                                                </div>
                                            </div>
                                            <div className="math-card p-4 bg-slate-900 border-slate-800">
                                                <div className="flex gap-3">
                                                    <span className="w-6 h-6 rounded-full bg-rose-500 text-white flex items-center justify-center text-[11px] font-black shrink-0">4</span>
                                                    <div className="text-[13px] font-black text-rose-100 leading-snug">
                                                        <MathSymbol text="Δθ/Δt = ω" color="#fbbf24"/> 이므로, <br/>구심 가속도 크기는 <MathSymbol text="a = v·ω" color="#fbbf24"/> 입니다.
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <button onClick={() => setIsZoomed(!isZoomed)} className="w-full py-4 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-black text-sm transition-all shadow-xl flex items-center justify-center gap-2">
                                        <Icon name={isZoomed ? "minimize-2" : "maximize-2"} size={16} />
                                        {isZoomed ? "원래 크기로 보기" : "벡터 분석 창 확대하기"}
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 gap-6 pb-12">
                            <div className="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm space-y-4">
                                <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                                    <Icon name="sigma" className="text-blue-600" />
                                    벡터 뺄셈의 시각화
                                </h3>
                                <p className="text-slate-600 text-[14px] leading-relaxed">
                                    상세 분석 창에서 **파란색 점선($v_1$)**의 끝에서 **초록색 실선($v_2$)**의 끝으로 향하는 **빨간색 화살표($\Delta v$)**를 확인하세요. 
                                    두 지점 사이의 거리($\Delta \theta$)를 줄이면 이 빨간 화살표가 점점 원의 중심을 향하게 되는 것을 볼 수 있습니다.
                                </p>
                            </div>
                            <div className="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm space-y-4">
                                <h3 className="text-lg font-black text-slate-900 flex items-center gap-2">
                                    <Icon name="function" className="text-emerald-600" />
                                    결론적 관계식
                                </h3>
                                <div className="space-y-3">
                                    <div className="flex justify-between items-center p-4 bg-slate-50 rounded-2xl border border-slate-100">
                                        <span className="text-xs font-black text-slate-400 uppercase tracking-tighter">Velocity formula</span>
                                        <span className="text-xl font-black text-slate-900 italic">a = v · ω</span>
                                    </div>
                                    <div className="flex justify-between items-center p-4 bg-slate-50 rounded-2xl border border-slate-100">
                                        <span className="text-xs font-black text-slate-400 uppercase tracking-tighter">Radius formula</span>
                                        <span className="text-xl font-black text-slate-900 italic">a = v² / r</span>
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
    components.html(react_code, height=1050, scrolling=True)

if __name__ == "__main__":
    run_sim()
