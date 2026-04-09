import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 법칙: 타원 궤도와 면적 속도", layout="wide")
    
    st.title("🪐 케플러 제1, 2법칙: 타원 궤도와 면적 속도 일정 법칙")
    st.markdown("""
    행성은 태양을 한 초점으로 하는 **타원 궤도**를 따라 공전하며, 태양과 행성을 잇는 선분이 같은 시간 동안 훑고 지나가는 **면적은 항상 일정**합니다.
    이심률을 조절하며 행성의 속력이 어느 지점에서 가장 빠르고 느려지는지 관찰해 보세요.
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
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
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

            const KeplerSim = () => {
                const [eccentricity, setEccentricity] = useState(0.5);
                const [semiMajorAxis, setSemiMajorAxis] = useState(140);
                const [isPlaying, setIsPlaying] = useState(false);
                const [planetPos, setPlanetPos] = useState({ x: 0, y: 0, angle: 0 });
                const canvasRef = useRef(null);

                useEffect(() => {
                    let animationFrame;
                    if (isPlaying) {
                        const animate = () => {
                            setPlanetPos(prev => {
                                const a = semiMajorAxis;
                                const e = eccentricity;
                                const focusOffset = a * e;
                                
                                // 타원 궤도 방정식: r = a(1-e^2) / (1 + e cos(theta))
                                // theta=0을 근일점(태양과 가장 가까운 지점)으로 설정
                                const r = a * (1 - e * e) / (1 + e * Math.cos(prev.angle));
                                
                                // 각속도 dTheta = (h / r^2) dt -> 면적 속도 일정 법칙 모사
                                const baseSpeed = 80; 
                                const deltaAngle = (baseSpeed / (r * r)) * 10; 
                                const newAngle = prev.angle + deltaAngle;
                                
                                // 태양의 위치(왼쪽 초점: -focusOffset)를 기준으로 좌표 계산
                                // theta=0이 왼쪽(근일점)을 향하도록 Math.PI를 더함
                                const x = -focusOffset + r * Math.cos(newAngle + Math.PI);
                                const y = r * Math.sin(newAngle + Math.PI);
                                
                                return { x, y, angle: newAngle };
                            });
                            animationFrame = requestAnimationFrame(animate);
                        };
                        animate();
                    }
                    return () => cancelAnimationFrame(animationFrame);
                }, [isPlaying, eccentricity, semiMajorAxis]);

                // 파라미터(이심률, 장반경) 변경 시 정지 상태에서도 행성 위치 동기화
                useEffect(() => {
                    setPlanetPos(prev => {
                        const a = semiMajorAxis;
                        const e = eccentricity;
                        const focusOffset = a * e;
                        const r = a * (1 - e * e) / (1 + e * Math.cos(prev.angle));
                        const x = -focusOffset + r * Math.cos(prev.angle + Math.PI);
                        const y = r * Math.sin(prev.angle + Math.PI);
                        return { ...prev, x, y };
                    });
                }, [eccentricity, semiMajorAxis]);

                useEffect(() => {
                    const canvas = canvasRef.current;
                    if (!canvas) return;
                    const ctx = canvas.getContext('2d');
                    const width = canvas.width;
                    const height = canvas.height;
                    const centerX = width / 2;
                    const centerY = height / 2;

                    ctx.clearRect(0, 0, width, height);

                    const a = semiMajorAxis;
                    const e = eccentricity;
                    const b = a * Math.sqrt(1 - e * e);
                    const focusOffset = a * e;

                    // 1. 궤도
                    ctx.beginPath();
                    ctx.ellipse(centerX, centerY, a, b, 0, 0, Math.PI * 2);
                    ctx.strokeStyle = '#334155';
                    ctx.setLineDash([5, 5]);
                    ctx.lineWidth = 1;
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // 2. 초점 (태양)
                    ctx.beginPath();
                    ctx.arc(centerX - focusOffset, centerY, 12, 0, Math.PI * 2);
                    ctx.fillStyle = '#f59e0b';
                    ctx.shadowBlur = 15;
                    ctx.shadowColor = '#f59e0b';
                    ctx.fill();
                    ctx.shadowBlur = 0;

                    // 3. 면적 섹터
                    ctx.beginPath();
                    ctx.moveTo(centerX - focusOffset, centerY);
                    ctx.lineTo(centerX + planetPos.x, centerY + planetPos.y);
                    ctx.strokeStyle = 'rgba(59, 130, 246, 0.3)';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    // 4. 행성
                    ctx.beginPath();
                    ctx.arc(centerX + planetPos.x, centerY + planetPos.y, 8, 0, Math.PI * 2);
                    ctx.fillStyle = '#3b82f6';
                    ctx.fill();
                    ctx.strokeStyle = 'white';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                }, [planetPos, eccentricity, semiMajorAxis]);

                return (
                    <div className="max-w-6xl mx-auto p-4 flex flex-col lg:flex-row gap-8">
                        <div className="flex-1 space-y-6">
                            <div className="bg-slate-900 rounded-3xl overflow-hidden relative shadow-2xl border-8 border-slate-800 aspect-video flex items-center justify-center">
                                <canvas ref={canvasRef} width={800} height={500} className="w-full h-auto" />
                                <div className="absolute bottom-6 right-6 flex gap-4 text-white text-xs bg-black/50 p-4 rounded-2xl backdrop-blur-md">
                                    <div className="flex items-center gap-2">
                                        <div className="w-3 h-3 bg-yellow-400 rounded-full"></div> 초점 (태양)
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <div className="w-3 h-3 bg-blue-500 rounded-full"></div> 행성
                                    </div>
                                </div>
                            </div>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="p-5 bg-blue-50 rounded-2xl border border-blue-100 flex gap-4">
                                    <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600 shrink-0">
                                        <Icon name="target" size={20} />
                                    </div>
                                    <div>
                                        <span className="font-bold text-blue-800 block mb-1">관찰: 근일점 vs 원일점</span>
                                        <p className="text-[13px] text-slate-600 leading-snug">태양과 가장 가까울 때(근일점)와 멀 때(원일점)의 공전 속도를 비교해 보세요.</p>
                                    </div>
                                </div>
                                <div className="p-5 bg-amber-50 rounded-2xl border border-amber-100 flex gap-4">
                                    <div className="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center text-amber-600 shrink-0">
                                        <Icon name="orbit" size={20} />
                                    </div>
                                    <div>
                                        <span className="font-bold text-amber-800 block mb-1">탐구: 이심률의 변화</span>
                                        <p className="text-[13px] text-slate-600 leading-snug">이심률이 커질수록 궤도가 찌그러지는 정도와 속력 변화의 극단성을 관찰하세요.</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="w-full lg:w-80 space-y-6">
                            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xl">
                                <h3 className="font-bold text-slate-800 mb-6 flex items-center gap-2">
                                    <Icon name="settings-2" className="text-blue-600" /> 시뮬레이션 제어
                                </h3>
                                
                                <div className="space-y-8">
                                    <div>
                                        <div className="flex justify-between items-center mb-3">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest">이심률 (e)</label>
                                            <span className="text-blue-600 font-mono font-bold text-lg">{eccentricity.toFixed(2)}</span>
                                        </div>
                                        <input 
                                            type="range" min="0" max="0.8" step="0.01" value={eccentricity} 
                                            onChange={(e) => setEccentricity(parseFloat(e.target.value))}
                                            className="w-full h-2 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-blue-600"
                                        />
                                        <div className="flex justify-between text-[10px] text-slate-400 mt-2 font-bold uppercase">
                                            <span>원형 (0.0)</span>
                                            <span>타원 (0.8)</span>
                                        </div>
                                    </div>

                                    <div className="pt-4 space-y-3">
                                        <button 
                                            onClick={() => setIsPlaying(!isPlaying)}
                                            className={`w-full flex items-center justify-center gap-3 py-4 rounded-2xl font-bold transition-all ${
                                                isPlaying ? 'bg-amber-100 text-amber-700 hover:bg-amber-200' : 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-200'
                                            }`}
                                        >
                                            <Icon name={isPlaying ? "pause" : "play"} />
                                            {isPlaying ? '일시정지' : '시시작하기'}
                                        </button>
                                        <button 
                                            onClick={() => {setPlanetPos({x:0, y:0, angle:0}); setIsPlaying(false);}}
                                            className="w-full py-4 bg-slate-50 text-slate-500 rounded-2xl font-bold hover:bg-slate-100 flex items-center justify-center gap-2"
                                        >
                                            <Icon name="rotate-ccw" size={18} /> 초기화
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-slate-900 p-6 rounded-3xl text-white shadow-2xl relative overflow-hidden group">
                                <div className="absolute -top-4 -right-4 w-24 h-24 bg-blue-600/20 rounded-full blur-2xl group-hover:bg-blue-600/30 transition-all"></div>
                                <h4 className="font-bold mb-4 flex items-center gap-2 text-sm text-blue-400">
                                    <Icon name="info" size={18} /> 핵심 물리 인사이트
                                </h4>
                                <div className="space-y-4 text-xs">
                                    <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                                        <p className="text-white/60 mb-1">면적 속도 일정</p>
                                        <p className="font-mono text-sm">dA/dt = Const.</p>
                                    </div>
                                    <p className="text-slate-400 leading-relaxed italic">
                                        "거리가 가까워지면(r↓) 중력이 강해져 속력이 빨라지고, 거리가 멀어지면(r↑) 중력이 약해져 속력이 느려집니다."
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerSim />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=750, scrolling=False)

if __name__ == "__main__":
    run_sim()
