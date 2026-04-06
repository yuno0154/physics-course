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
                const [activeTab, setActiveTab] = useState('missions'); // 'missions' 또는 'settings'
                
                // --- 계산 ---
                const PI = Math.PI;
                const angleRad = (angleDeg * PI) / 180;
                const arcLength = radius * angleRad;

                // 시각화용 스케일 조정 (2m가 충분히 들어가도록)
                const scale = 110; 
                const visualR = radius * scale;
                const viewSize = 540;
                const centerX = viewSize / 2;
                const centerY = viewSize / 2;

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

                            <div className="flex flex-col lg:flex-row min-h-[580px]">
                                {/* 1. 시각화 영역 */}
                                <div className="flex-1 bg-slate-50 relative flex items-center justify-center p-4 border-b lg:border-b-0 lg:border-r border-slate-200">
                                    <svg viewBox={`0 0 ${viewSize} ${viewSize}`} className="w-full h-full max-w-[500px] drop-shadow-xl">
                                        {/* 가이드 그리드 */}
                                        <circle cx={centerX} cy={centerY} r={50} fill="none" stroke="#cbd5e1" strokeWidth="0.5" />
                                        <circle cx={centerX} cy={centerY} r={100} fill="none" stroke="#cbd5e1" strokeWidth="0.5" />
                                        <circle cx={centerX} cy={centerY} r={150} fill="none" stroke="#cbd5e1" strokeWidth="0.5" />
                                        <circle cx={centerX} cy={centerY} r={200} fill="none" stroke="#cbd5e1" strokeWidth="1" />
                                        
                                        {/* 전체 원 가이드 라인 */}
                                        <circle cx={centerX} cy={centerY} r={visualR} fill="none" stroke="#e2e8f0" strokeWidth="1.5" strokeDasharray="4,4" />
                                        
                                        {/* 부채꼴 채우기 */}
                                        <path d={getSectorPath()} fill="rgba(56, 189, 248, 0.08)" stroke="none" />
                                        
                                        {/* 반지름과 호 */}
                                        <line x1={centerX} y1={centerY} x2={centerX + visualR} y2={centerY} stroke="#475569" strokeWidth="3" strokeLinecap="round" />
                                        <line x1={centerX} y1={centerY} x2={ballX} y2={ballY} stroke="#475569" strokeWidth="3" strokeLinecap="round" />
                                        
                                        {/* 강조된 호의 길이 (빨간색) */}
                                        <path d={getArcPath()} fill="none" stroke="#ef4444" strokeWidth="6" strokeLinecap="round" />
                                        
                                        {/* 중앙점 */}
                                        <circle cx={centerX} cy={centerY} r="6" fill="#1e293b" />
                                        
                                        {/* 반지름 라벨 (r) */}
                                        <text x={centerX + visualR/2} y={centerY + 20} textAnchor="middle" fill="#334155" className="text-sm italic font-bold">r = {radius}m</text>
                                        
                                        {/* 각도 라벨 (θ) */}
                                        <g>
                                            <path d={`M ${centerX + 40} ${centerY} A 40 40 0 ${angleDeg > 180 ? 1 : 0} 0 ${centerX + 40 * Math.cos(-angleRad)} ${centerY + 40 * Math.sin(-angleRad)}`} fill="none" stroke="#f59e0b" strokeWidth="2.5" />
                                            <text x={centerX + 55 * Math.cos(-angleRad/2)} y={centerY + 55 * Math.sin(-angleRad/2)} textAnchor="middle" dominantBaseline="middle" fill="#d97706" className="text-xs font-bold font-mono">θ</text>
                                        </g>

                                        {/* 호 라벨 (s) */}
                                        <text x={centerX + (visualR + 35) * Math.cos(-angleRad/2)} y={centerY + (visualR + 35) * Math.sin(-angleRad/2)} textAnchor="middle" dominantBaseline="middle" fill="#ef4444" className="text-lg italic font-black">s = {arcLength.toFixed(2)}m</text>
                                    </svg>
                                    
                                    {/* 고정 예시 박스 */}
                                    <div className="absolute top-4 right-4 flex flex-col gap-2 pointer-events-none">
                                        <div className="bg-white/90 backdrop-blur-md p-3 rounded-xl border border-slate-200 shadow-lg text-[10px] leading-tight w-40">
                                            <p className="font-bold text-slate-800 mb-1">📏 스케일 가이드</p>
                                            <p className="text-slate-600">• 실선 원 : <span className="math-font">r</span> = 1.8m 지점</p>
                                            <p className="text-slate-600">• 점선 : 현재 반지름 (<span className="math-font">r</span>)</p>
                                        </div>
                                    </div>
                                </div>

                                {/* 2. 컨트롤 및 미션 탐구 영역 */}
                                <div className="w-full lg:w-[400px] bg-slate-50 flex flex-col border-l border-slate-200">
                                    {/* 탭 네비게이션 */}
                                    <div className="flex bg-slate-100 p-1 border-b">
                                        <button 
                                            onClick={() => setActiveTab('missions')} 
                                            className={`flex-1 py-3 text-xs font-bold rounded-t-xl transition-all ${activeTab === 'missions' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}
                                        >
                                            <Icon name="target" size={14} className="inline mr-1" /> 탐구 미션
                                        </button>
                                        <button 
                                            onClick={() => setActiveTab('settings')} 
                                            className={`flex-1 py-3 text-xs font-bold rounded-t-xl transition-all ${activeTab === 'settings' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}
                                        >
                                            <Icon name="settings-2" size={14} className="inline mr-1" /> 조절 및 수식
                                        </button>
                                    </div>

                                    <div className="p-6 flex-1 overflow-y-auto no-scrollbar space-y-6">
                                        {activeTab === 'missions' ? (
                                            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
                                                <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest px-1">실험에 의한 탐구 과제</h4>
                                                
                                                <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm group hover:border-blue-300 transition-colors">
                                                    <div className="flex gap-3">
                                                        <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-black">1</span>
                                                        <p className="text-[12px] leading-relaxed text-slate-700">
                                                            반지름(<span className="math-font">r</span>)을 <b>1.0m</b>로 설정하세요. <b>호의 길이(<span className="math-font">s</span>)가 반지름과 똑같이 1.0m</b>가 되는 각도(<span className="math-font">θ</span>)는 약 몇 도입니까? 
                                                            <span className="block mt-1 text-slate-400 text-[10px] font-medium">(이것을 1라디안의 정의라고 합니다.)</span>
                                                        </p>
                                                    </div>
                                                </div>

                                                <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm group hover:border-blue-300 transition-colors">
                                                    <div className="flex gap-3">
                                                        <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-xs font-black">2</span>
                                                        <p className="text-[12px] leading-relaxed text-slate-700">
                                                            반지름을 <b>0.5m</b>로 줄였을 때, 호의 길이가 <b>3.14m(π)</b>가 되려면 각도는 몇 도가 되어야 할까요? 시뮬레이션으로 확인해 보세요.
                                                        </p>
                                                    </div>
                                                </div>

                                                <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm group hover:border-blue-300 transition-colors">
                                                    <div className="flex gap-3">
                                                        <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-xs font-black">3</span>
                                                        <p className="text-[12px] leading-relaxed text-slate-700">
                                                            반지름을 <b>2.0m</b>로 설정하고 원의 절반(180°)을 만들었을 때, 호의 길이는 1.0m일 때의 호의 길이에 비해 몇 배가 됩니까?
                                                        </p>
                                                    </div>
                                                </div>

                                                <div className="p-4 bg-slate-900 rounded-2xl shadow-lg shadow-slate-100 mt-2">
                                                    <p className="text-white text-[11px] font-bold mb-2 flex items-center gap-2 italic">
                                                        <Icon name="lightbulb" size={14} className="text-amber-400" /> 탐구 정리
                                                    </p>
                                                    <p className="text-slate-400 text-[11px] leading-relaxed italic">
                                                        "각도가 고정되어 있을 때, 원의 호의 길이는 반지름에 <b>정비례</b>한다."
                                                    </p>
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="space-y-6 animate-in fade-in slide-in-from-left-4 duration-300">
                                                {/* 조절 섹션 */}
                                                <div className="space-y-5">
                                                    <div className="space-y-3">
                                                        <div className="flex justify-between items-end">
                                                            <span className="text-xs font-bold text-slate-500 uppercase tracking-tight">반지름 (<span className="math-font">r</span>)</span>
                                                            <span className="text-lg font-black text-sky-600">{radius.toFixed(1)} m</span>
                                                        </div>
                                                        <input 
                                                            type="range" min="0.1" max="2.0" step="0.1" value={radius} 
                                                            onChange={e=>setRadius(parseFloat(e.target.value))} 
                                                            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-sky-600" 
                                                        />
                                                    </div>
                                                    <div className="space-y-3">
                                                        <div className="flex justify-between items-end">
                                                            <span className="text-xs font-bold text-slate-500 uppercase tracking-tight">중심각 (<span className="math-font">θ</span>)</span>
                                                            <span className="text-lg font-black text-amber-600">{angleDeg}°</span>
                                                        </div>
                                                        <input 
                                                            type="range" min="0" max="360" step="1" value={angleDeg} 
                                                            onChange={e=>setAngleDeg(parseInt(e.target.value))} 
                                                            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-500" 
                                                        />
                                                    </div>
                                                </div>

                                                {/* 관계식 카드 */}
                                                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                                                    <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">기본 관계식</h4>
                                                    <div className="flex flex-col items-center py-4 bg-slate-50 rounded-2xl">
                                                        <p className="text-3xl font-black text-slate-800 tracking-widest drop-shadow-sm">s = rθ</p>
                                                        <p className="text-[10px] text-slate-500 mt-1 uppercase font-bold tracking-tighter">(Arc Length = Radius × Radians)</p>
                                                    </div>
                                                    <div className="space-y-2 text-[12px] text-slate-600 leading-relaxed font-medium">
                                                        <p className="flex items-center justify-between">
                                                            <span>실제 계산:</span>
                                                            <span className="font-bold">{radius.toFixed(1)}m × {angleRad.toFixed(3)}rad = <span className="text-rose-500">{arcLength.toFixed(2)}m</span></span>
                                                        </p>
                                                    </div>
                                                </div>

                                                {/* 라디안 정의 */}
                                                <div className="bg-amber-50 p-5 rounded-2xl border border-amber-100">
                                                    <p className="text-[11px] font-black text-amber-800 mb-2 flex items-center gap-1">
                                                        <Icon name="bookmark" size={14} /> 라디안(Radian)의 약속
                                                    </p>
                                                    <p className="text-[11px] text-amber-950/70 leading-relaxed space-y-1">
                                                        • <b>1 라디안:</b> 이미 약속된 값으로, 호의 길이(<span className="math-font">s</span>)가 반지름(<span className="math-font">r</span>)과 똑같아지는 순간의 각도입니다.<br/>
                                                        • <b>360°</b>의 라디안 값은 <b>약 6.28 (2π)</b> 입니다.<br/>
                                                        • <b>1 라디안</b>은 각도기로 쟀을 때 <b>약 57.3°</b> 입니다.
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
            root.render(<BasicCircularSim />);
        </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트로 HTML 삽입 (높이를 더 확보하여 잘림 방지)
    components.html(react_code, height=820, scrolling=False)

if __name__ == "__main__":
    run_sim()
