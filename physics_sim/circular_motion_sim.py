import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="원운동의 기초: 라디안과 호의 길이", layout="wide")
    
    # 상단 브랜딩 및 제목
    st.title("📏 원운동의 기초: 라디안(Radian)과 호의 길이")
    st.markdown("""
    이 시뮬레이션은 원운동을 이해하기 위한 가장 기초적인 개념인 **반지름($r$), 중심각($\\theta$), 호의 길이($s$)** 사이의 관계를 탐구합니다.
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
                const [radius, setRadius] = useState(1.0); // 미터 단위
                const [angleDeg, setAngleDeg] = useState(90); // 도 단위
                
                // --- 계산 ---
                const PI = Math.PI;
                const angleRad = (angleDeg * PI) / 180;
                const arcLength = radius * angleRad;
                const circumference = 2 * PI * radius;

                // 시각화용 스케일 (1m = 120px)
                const scale = 120;
                const visualR = radius * scale;
                const centerX = 220;
                const centerY = 220;

                const ballX = centerX + visualR * Math.cos(-angleRad);
                const ballY = centerY + visualR * Math.sin(-angleRad);

                // 부채꼴 경로 생성
                const getSectorPath = () => {
                    const startX = centerX + visualR;
                    const startY = centerY;
                    const largeArcFlag = angleDeg > 180 ? 1 : 0;
                    return `M ${centerX} ${centerY} L ${startX} ${startY} A ${visualR} ${visualR} 0 ${largeArcFlag} 0 ${ballX} ${ballY} Z`;
                };

                const getArcPath = () => {
                    const startX = centerX + visualR;
                    const startY = centerY;
                    const largeArcFlag = angleDeg > 180 ? 1 : 0;
                    return `M ${startX} ${startY} A ${visualR} ${visualR} 0 ${largeArcFlag} 0 ${ballX} ${ballY}`;
                };

                return (
                    <div className="flex flex-col items-center bg-transparent min-h-screen p-2 text-slate-800">
                        <div className="w-full max-w-6xl rounded-3xl shadow-2xl border border-slate-200 overflow-hidden bg-white">
                            
                            {/* 상단 핵심 데이터 바 */}
                            <div className="grid grid-cols-3 gap-4 p-5 bg-slate-900 text-white">
                                <div className="text-center border-r border-slate-700">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-1">반지름 (r)</p>
                                    <p className="text-2xl font-black text-sky-400">{radius.toFixed(1)} <small className="text-sm">m</small></p>
                                </div>
                                <div className="text-center border-r border-slate-700">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-1">중심각 (θ)</p>
                                    <div className="flex flex-col items-center">
                                        <p className="text-xl font-black text-amber-400">{angleDeg}°</p>
                                        <p className="text-[10px] text-slate-500 font-mono">≈ {angleRad.toFixed(3)} rad</p>
                                    </div>
                                </div>
                                <div className="text-center">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-1">호의 길이 (s)</p>
                                    <p className="text-2xl font-black text-rose-400">{arcLength.toFixed(2)} <small className="text-sm">m</small></p>
                                </div>
                            </div>

                            <div className="flex flex-col lg:flex-row min-h-[500px]">
                                {/* 1. 시각화 영역 */}
                                <div className="flex-1 bg-slate-50 relative flex items-center justify-center p-8 border-b lg:border-b-0 lg:border-r border-slate-200">
                                    <svg viewBox="0 0 440 440" className="w-full h-full max-w-[400px] drop-shadow-lg">
                                        {/* 전체 원 가이드 라인 */}
                                        <circle cx={centerX} cy={centerY} r={visualR} fill="none" stroke="#e2e8f0" strokeWidth="1" strokeDasharray="4,4" />
                                        
                                        {/* 부채꼴 채우기 */}
                                        <path d={getSectorPath()} fill="rgba(56, 189, 248, 0.1)" stroke="none" />
                                        
                                        {/* 반지름과 호 */}
                                        <line x1={centerX} y1={centerY} x2={centerX + visualR} y2={centerY} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                        <line x1={centerX} y1={centerY} x2={ballX} y2={ballY} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                        
                                        {/* 강조된 호의 길이 (빨간색) */}
                                        <path d={getArcPath()} fill="none" stroke="#ef4444" strokeWidth="4" strokeLinecap="round" />
                                        
                                        {/* 라벨들 */}
                                        <circle cx={centerX} cy={centerY} r="4" fill="#1e293b" />
                                        
                                        {/* 반지름 라벨 (r) */}
                                        <text x={centerX + visualR/2} y={centerY + 15} textAnchor="middle" fill="#334155" className="text-sm italic font-bold">r</text>
                                        
                                        {/* 각도 라벨 (θ) */}
                                        <g>
                                            <path d={`M ${centerX + 30} ${centerY} A 30 30 0 ${angleDeg > 180 ? 1 : 0} 0 ${centerX + 30 * Math.cos(-angleRad)} ${centerY + 30 * Math.sin(-angleRad)}`} fill="none" stroke="#f59e0b" strokeWidth="2" />
                                            <text x={centerX + 40 * Math.cos(-angleRad/2)} y={centerY + 40 * Math.sin(-angleRad/2)} textAnchor="middle" dominantBaseline="middle" fill="#d97706" className="text-xs font-bold font-mono">θ</text>
                                        </g>

                                        {/* 호 라벨 (s) */}
                                        <text x={centerX + (visualR + 25) * Math.cos(-angleRad/2)} y={centerY + (visualR + 25) * Math.sin(-angleRad/2)} textAnchor="middle" dominantBaseline="middle" fill="#ef4444" className="text-base italic font-black">s</text>
                                    </svg>
                                    
                                    {/* 고정 예시 박스 (이미지 내용 반영) */}
                                    <div className="absolute top-4 right-4 flex flex-col gap-2">
                                        <div className="bg-white/80 backdrop-blur-md p-3 rounded-xl border border-slate-200 shadow-sm text-[11px] leading-tight w-48">
                                            <p className="font-bold text-slate-800 mb-1">💡 예시: 한 바퀴 (360°)</p>
                                            <p className="text-slate-600">• 반지름 <span className="math-font">r</span> = 1m 이면<br/>원둘레 <span className="math-font">s</span> = 6.28m (2π)</p>
                                            <p className="text-slate-600 mt-1">• 반지름 <span className="math-font">r</span> = 0.5m 이면<br/>원둘레 <span className="math-font">s</span> = 3.14m (π)</p>
                                        </div>
                                    </div>
                                </div>

                                {/* 2. 컨트롤 및 개념 학습 영역 */}
                                <div className="w-full lg:w-96 bg-slate-50 p-6 flex flex-col gap-8">
                                    {/* 조절 바 */}
                                    <div className="space-y-6">
                                        <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                            <Icon name="sliders" size={14} /> 매개변수 조절
                                        </h4>
                                        <div className="space-y-6">
                                            <div className="space-y-3">
                                                <div className="flex justify-between items-end">
                                                    <span className="text-sm font-bold text-slate-700">반지름 (<span className="math-font">r</span>)</span>
                                                    <span className="text-lg font-mono text-sky-600">{radius.toFixed(1)} m</span>
                                                </div>
                                                <input 
                                                    type="range" min="0.1" max="2.0" step="0.1" value={radius} 
                                                    onChange={e=>setRadius(parseFloat(e.target.value))} 
                                                    className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-sky-600" 
                                                />
                                            </div>
                                            <div className="space-y-3">
                                                <div className="flex justify-between items-end">
                                                    <span className="text-sm font-bold text-slate-700">중심각 (<span className="math-font">θ</span>)</span>
                                                    <span className="text-lg font-mono text-amber-600">{angleDeg}°</span>
                                                </div>
                                                <input 
                                                    type="range" min="0" max="360" step="1" value={angleDeg} 
                                                    onChange={e=>setAngleDeg(parseInt(e.target.value))} 
                                                    className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-500" 
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    {/* 관계식 카드 */}
                                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                                        <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">기본 관계식</h4>
                                        <div className="flex flex-col items-center py-2 bg-slate-50 rounded-xl">
                                            <p className="text-3xl font-black text-slate-800 tracking-widest">s = rθ</p>
                                            <p className="text-[10px] text-slate-500 mt-1">(호의 길이 = 반지름 × 라디안각)</p>
                                        </div>
                                        <div className="space-y-2 text-[12px] text-slate-600 leading-relaxed">
                                            <p className="flex items-center gap-2">
                                                <span className="w-1.5 h-1.5 bg-rose-400 rounded-full"></span>
                                                <span>{radius.toFixed(1)}m × {angleRad.toFixed(3)}rad = <b>{arcLength.toFixed(2)}m</b></span>
                                            </p>
                                            <p className="flex items-center gap-2 pt-1 border-t border-slate-100">
                                                <Icon name="check-circle-2" size={12} className="text-emerald-500" />
                                                <span>반지름(<span className="math-font">r</span>)이 커지면 호(<span className="math-font">s</span>)도 길어집니다.</span>
                                            </p>
                                            <p className="flex items-center gap-2">
                                                <Icon name="check-circle-2" size={12} className="text-emerald-500" />
                                                <span>각도(<span className="math-font">θ</span>)가 커지면 호(<span className="math-font">s</span>)도 길어집니다.</span>
                                            </p>
                                        </div>
                                    </div>

                                    {/* 라디안의 정의 (이미지 하단 내용) */}
                                    <div className="mt-auto space-y-3">
                                        <div className="bg-amber-50 p-4 rounded-2xl border border-amber-100 italic">
                                            <p className="text-[11px] font-bold text-amber-800 mb-1">📌 라디안(Radian)의 약속</p>
                                            <p className="text-[11px] text-amber-700 leading-relaxed">
                                                • <b>각도의 단위:</b> 원둘레를 360등분한 '도(°)' 대신, 반지름과 호의 길이 비율로 각을 정합니다.<br/>
                                                • <b>1 라디안:</b> 호의 길이(<span className="math-font">s</span>)가 반지름(<span className="math-font">r</span>)과 같아질 때의 각도.<br/>
                                                • <b>변환:</b> 6.28 : 360° = 1 : (<b>약 57.3°</b>)
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
            root.render(<BasicCircularSim />);
        </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트로 HTML 삽입
    components.html(react_code, height=650, scrolling=False)

if __name__ == "__main__":
    run_sim()
