import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="원운동의 가속도: 벡터의 변화와 극한", layout="wide")
    
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
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef, useMemo } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                const iconRef = useRef(null);
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const VectorAccelSim = () => {
                // --- 상태 관리 ---
                const [theta1, setTheta1] = useState(Math.PI / 4); // 첫 번째 지점 각도 (rad)
                const [dTheta, setDTheta] = useState(0.8); // 사이 각도 (rad)
                const [radius, setRadius] = useState(150); // 시각적 반지름
                const [velMag, setVelMag] = useState(80); // 속도 벡터 시각적 크기
                
                const theta2 = theta1 - dTheta; // 두 번째 지점 (시계 방향으로 진행 가정하면 -dt)
                
                const centerX = 250;
                const centerY = 250;

                // 지점 1 (P1)
                const p1 = {
                    x: centerX + radius * Math.cos(theta1),
                    y: centerY - radius * Math.sin(theta1)
                };
                // 속도 1 (V1): 위치에 수직
                const v1 = {
                    x: -velMag * Math.sin(theta1),
                    y: -velMag * Math.cos(theta1)
                };

                // 지점 2 (P2)
                const p2 = {
                    x: centerX + radius * Math.cos(theta2),
                    y: centerY - radius * Math.sin(theta2)
                };
                // 속도 2 (V2)
                const v2 = {
                    x: -velMag * Math.sin(theta2),
                    y: -velMag * Math.cos(theta2)
                };

                // 속도 변화량 (delta V = V2 - V1)
                const dv = {
                    x: v2.x - v1.x,
                    y: v2.y - v1.y
                };

                // 벡터 뺄셈 시각화 공간 (우상단 또는 별도 박스)
                const subBoxSize = 200;
                const subCenterX = 100;
                const subCenterY = 100;

                // 마우스 드래그 핸들링 (각도 조절)
                const svgRef = useRef(null);
                const [isDragging, setIsDragging] = useState(null); // 'p1' or 'p2'

                const handleMouseMove = (e) => {
                    if (!isDragging) return;
                    const rect = svgRef.current.getBoundingClientRect();
                    const x = e.clientX - rect.left - centerX;
                    const y = -(e.clientY - rect.top - centerY);
                    let angle = Math.atan2(y, x);
                    
                    if (isDragging === 'p1') {
                        setTheta1(angle);
                    } else if (isDragging === 'p2') {
                        let diff = theta1 - angle;
                        // 보정 (각도 차이가 너무 커지거나 뒤집히는 것 방지)
                        if (diff < 0) diff += 2 * Math.PI;
                        if (diff > Math.PI) diff = Math.PI; 
                        setDTheta(diff);
                    }
                };

                const handleMouseUp = () => setIsDragging(null);

                // 가속도 벡터 (평균) - 크기를 키워서 보여주기
                // a_avg = (v2-v1) / dt. 여기선 시각적으로 dv의 방향을 강조.
                const accelScale = dTheta > 0.05 ? 1 / dTheta : 20;

                return (
                    <div className="flex flex-col items-center bg-transparent min-h-screen p-1 text-slate-800" onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp}>
                        <div className="w-full max-w-6xl rounded-[32px] shadow-[0_20px_40px_-10px_rgba(0,0,0,0.15)] border border-slate-200 overflow-hidden bg-white">
                            
                            {/* 상단 핵심 데이터 바 */}
                            <div className="grid grid-cols-4 gap-0 bg-slate-900 text-white border-b border-slate-800">
                                <div className="text-center py-4 px-2 border-r border-slate-800/50">
                                    <p className="text-[10px] text-sky-400 font-black uppercase tracking-widest mb-1">시간 간격 (Δt ∝ Δθ)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-2xl font-black text-white">{dTheta.toFixed(2)}</span>
                                        <span className="text-sm font-bold text-slate-500">rad</span>
                                    </div>
                                </div>
                                <div className="text-center py-4 px-2 border-r border-slate-800/50">
                                    <p className="text-[10px] text-emerald-400 font-black uppercase tracking-widest mb-1">속도 변화량 (|Δv|)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-2xl font-black text-white">{(Math.sqrt(dv.x**2 + dv.y**2)/velMag).toFixed(2)}</span>
                                        <span className="text-sm font-bold text-slate-500">v₀</span>
                                    </div>
                                </div>
                                <div className="text-center py-4 px-2 border-r border-slate-800/50">
                                    <p className="text-[10px] text-rose-500 font-black uppercase tracking-widest mb-1">평균 가속도 (|a_avg|)</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-2xl font-black text-white">{(Math.sqrt(dv.x**2+dv.y**2)/(velMag*dTheta || 1)).toFixed(2)}</span>
                                        <span className="text-sm font-bold text-slate-500">a₀</span>
                                    </div>
                                </div>
                                <div className="text-center py-4 px-2">
                                    <p className="text-[10px] text-amber-400 font-black uppercase tracking-widest mb-1">가속도 방향</p>
                                    <div className="flex items-center justify-center gap-1">
                                        <span className="text-sm font-black text-white">
                                            {dTheta < 0.1 ? "중심 방향 (향심)" : dTheta < 0.5 ? "중심에 근접" : "중심과 오차발생"}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row min-h-[620px]">
                                {/* 1. 시각화 영역 */}
                                <div className="flex-1 bg-slate-50 relative flex items-center justify-center p-4 border-b lg:border-b-0 lg:border-r-2 border-slate-100">
                                    <svg ref={svgRef} viewBox="0 0 500 500" className="w-full h-full max-w-[500px] filter drop-shadow-xl select-none">
                                        {/* 가이드 격자 */}
                                        <circle cx={centerX} cy={centerY} r={radius} fill="none" stroke="#e2e8f0" strokeWidth="2" />
                                        <line x1={centerX-200} y1={centerY} x2={centerX+200} y2={centerY} stroke="#f1f5f9" strokeWidth="1" />
                                        <line x1={centerX} y1={centerY-200} x2={centerX} y2={centerY+200} stroke="#f1f5f9" strokeWidth="1" />
                                        
                                        {/* P1, P2 경로 표시 (부채꼴) */}
                                        <path d={`M ${centerX} ${centerY} L ${p1.x} ${p1.y} A ${radius} ${radius} 0 0 1 ${p2.x} ${p2.y} Z`} fill="rgba(56, 189, 248, 0.05)" />

                                        {/* V1 벡터 */}
                                        <line x1={p1.x} y1={p1.y} x2={p1.x + v1.x} y2={p1.y + v1.y} stroke="#3b82f6" strokeWidth="3" markerEnd="url(#arrow-blue)" />
                                        <text x={p1.x + v1.x * 1.2} y={p1.y + v1.y * 1.2} textAnchor="middle" fill="#3b82f6" className="vector-label text-sm">v₁</text>

                                        {/* V2 벡터 */}
                                        <line x1={p2.x} y1={p2.y} x2={p2.x + v2.x} y2={p2.y + v2.y} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                        <text x={p2.x + v2.x * 1.2} y={p2.y + v2.y * 1.2} textAnchor="middle" fill="#10b981" className="vector-label text-sm">v₂</text>

                                        {/* Delta V (P1에서 가이드로 보여줌) */}
                                        {dTheta > 0.05 && (
                                            <g opacity="0.6">
                                                <line x1={p2.x} y1={p2.y} x2={p2.x - v1.x} y2={p2.y - v1.y} stroke="#3b82f6" strokeWidth="2" strokeDasharray="4,4" />
                                                <line x1={p2.x - v1.x} y1={p2.y - v1.y} x2={p2.x + v2.x} y2={p2.y + v2.y} stroke="#f43f5e" strokeWidth="3" markerEnd="url(#arrow-red)" />
                                            </g>
                                        )}

                                        {/* P1 핸들 */}
                                        <circle cx={p1.x} cy={p1.y} r="12" fill="#3b82f6" stroke="white" strokeWidth="3" className="cursor-move hover:scale-110 transition-transform" onMouseDown={()=>setIsDragging('p1')} />
                                        <text x={p1.x} y={p1.y - 20} textAnchor="middle" weight="bold" className="font-bold text-xs uppercase text-slate-400">P₁</text>

                                        {/* P2 핸들 */}
                                        <circle cx={p2.x} cy={p2.y} r="12" fill="#10b981" stroke="white" strokeWidth="3" className="cursor-move hover:scale-110 transition-transform" onMouseDown={()=>setIsDragging('p2')} />
                                        <text x={p2.x} y={p2.y - 20} textAnchor="middle" weight="bold" className="font-bold text-xs uppercase text-slate-400">P₂</text>
                                        
                                        {/* 원점 */}
                                        <circle cx={centerX} cy={centerY} r="4" fill="#0f172a" />

                                        {/* 마커 정의 */}
                                        <defs>
                                            <marker id="arrow-blue" markerWidth="10" markerHeight="10" refX="9" refY="5" orientation="auto">
                                                <path d="M0,0 L10,5 L0,10 Z" fill="#3b82f6" />
                                            </marker>
                                            <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="9" refY="5" orientation="auto">
                                                <path d="M0,0 L10,5 L0,10 Z" fill="#10b981" />
                                            </marker>
                                            <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="9" refY="5" orientation="auto">
                                                <path d="M0,0 L10,5 L0,10 Z" fill="#f43f5e" />
                                            </marker>
                                            <marker id="arrow-amber" markerWidth="10" markerHeight="10" refX="9" refY="5" orientation="auto">
                                                <path d="M0,0 L10,5 L0,10 Z" fill="#f59e0b" />
                                            </marker>
                                        </defs>

                                        {/* 벡터 뺄셈 확대창 (오른쪽 상단 구석) */}
                                        <g transform="translate(340, 40)">
                                            <rect width="140" height="140" rx="20" fill="white" stroke="#f1f5f9" strokeWidth="2" fillOpacity="0.8" />
                                            <text x="70" y="20" textAnchor="middle" className="text-[10px] font-black text-slate-400 uppercase tracking-widest">벡터 뺄셈 상세</text>
                                            
                                            {/* v2 - v1 */}
                                            <g transform="translate(70, 70)">
                                                <line x1="0" y1="0" x2={v2.x/1.2} y2={v2.y/1.2} stroke="#10b981" strokeWidth="2.5" markerEnd="url(#arrow-green)" />
                                                <line x1="0" y1="0" x2={-v1.x/1.2} y2={-v1.y/1.2} stroke="#3b82f6" strokeWidth="2" strokeDasharray="3,3" opacity="0.4" />
                                                <line x1={-v1.x/1.2} y1={-v1.y/1.2} x2={(v2.x-v1.x)/1.2} y2={(v2.y-v1.y)/1.2} stroke="none" />
                                                {/* Δv 벡터 */}
                                                <line x1="0" y1="0" x2={(v2.x-v1.x)/1.2} y2={(v2.y-v1.y)/1.2} stroke="#f43f5e" strokeWidth="3" markerEnd="url(#arrow-red)" />
                                                <text x={(v2.x-v1.x)/2} y={(v2.y-v1.y)/2} textAnchor="middle" fill="#f43f5e" className="vector-label text-[10px]" dx="10">Δv</text>
                                            </g>
                                        </g>
                                    </svg>
                                </div>

                                {/* 2. 컨트롤 영역 */}
                                <div className="w-full lg:w-[420px] bg-white flex flex-col">
                                    <div className="p-6 flex-1 overflow-y-auto no-scrollbar space-y-6">
                                        <div className="space-y-4">
                                            <h4 className="text-[11px] font-black text-slate-400 uppercase tracking-widest px-1">단계별 탐구 가이드</h4>
                                            
                                            <div className="p-4 bg-blue-50/50 rounded-[24px] border-2 border-blue-100/50 space-y-3">
                                                <div className="flex gap-3">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs font-black">1</span>
                                                    <p className="text-[14px] text-slate-700 font-bold leading-relaxed">
                                                        원을 따라 <span className="text-blue-600">P₁</span>과 <span className="text-emerald-500">P₂</span>를 드래그하여 두 지점을 정해 보세요.
                                                    </p>
                                                </div>
                                                <div className="flex gap-3">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs font-black">2</span>
                                                    <p className="text-[14px] text-slate-700 font-bold leading-relaxed">
                                                        우측 상단의 <span className="text-rose-500 font-black">상세 창</span>에서 속도 벡터의 차이($\Delta \vec{v}$)가 어떻게 만들어지는지 확인하세요.
                                                    </p>
                                                </div>
                                                <div className="flex gap-3">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs font-black">3</span>
                                                    <p className="text-[14px] text-slate-700 font-bold leading-relaxed">
                                                        아래 슬라이더를 이용해 <span className="text-amber-500 underline decoration-2">시간 간격(Δθ)</span>을 아주 작게 줄여보세요.
                                                    </p>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="space-y-6 border-t-2 border-slate-50 pt-6">
                                            <div className="space-y-3">
                                                <div className="flex justify-between items-center">
                                                    <span className="text-[13px] font-black text-slate-500 tracking-tight uppercase px-2 border-l-4 border-amber-400">시간 간격 조절 (Δθ)</span>
                                                    <span className="text-lg font-black text-amber-600 bg-amber-50 px-3 py-1 rounded-xl">{dTheta.toFixed(2)} rad</span>
                                                </div>
                                                <input 
                                                    type="range" min="0.01" max="1.5" step="0.01" 
                                                    value={dTheta} 
                                                    onChange={e=>setDTheta(parseFloat(e.target.value))} 
                                                    className="w-full h-2 bg-slate-100 rounded-full appearance-none cursor-pointer accent-amber-500" 
                                                />
                                                <div className="flex justify-between text-[10px] font-black text-slate-400 uppercase">
                                                    <span>순간 (Δt→0)</span>
                                                    <span>평균</span>
                                                </div>
                                            </div>

                                            <div className="bg-slate-900 p-5 rounded-[28px] shadow-xl relative overflow-hidden group">
                                                <div className="absolute top-0 right-0 p-4 opacity-10">
                                                    <Icon name="zap" size={40} className="text-white" />
                                                </div>
                                                <h4 className="text-[10px] font-black text-slate-500 uppercase mb-3 tracking-widest">핵심 물리 결론</h4>
                                                <div className="space-y-4">
                                                    <div className="bg-white/5 p-4 rounded-2xl border border-white/10 group-hover:bg-white/10 transition-colors">
                                                        <p className="text-white text-[15px] font-bold leading-tight mb-2">가속도의 방향 (Limit)</p>
                                                        <p className="text-amber-400 text-[13px] font-medium opacity-90">
                                                            $\Delta t$가 0에 가까워질수록 $\Delta \vec{v}$의 방향은 원의 <span className="text-rose-400 font-black underline">중심</span>을 향하게 됩니다.
                                                        </p>
                                                    </div>
                                                    <div className="p-2 space-y-1">
                                                        <p className="text-slate-500 text-[11px] font-bold uppercase">순간 가속도 정의</p>
                                                        <p className="text-white text-2xl font-black italic tracking-tighter">
                                                            a = lim <span className="text-[14px] align-middle text-slate-400">(Δv/Δt)</span>
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
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
