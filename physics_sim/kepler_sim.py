import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 법칙: 타원 궤도와 면적 속도", layout="wide")
    
    st.title("🪐 케플러 제1, 2법칙: 타원 궤도와 면적 속도 일정 법칙")
    st.markdown("""
    행성은 태양을 한 초점으로 하는 **타원 궤도**를 따라 공전하며, 태양과 행성을 잇는 선분이 같은 시간 동안 훑고 지나가는 **면적은 항상 일정**합니다.
    이심률을 조절하며 행성의 속력이 어느 지점에서 가장 빠르고 느려지는지 관찰해 보세요.
    """)

    react_code = r"""
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
            input[type="range"]::-webkit-slider-thumb {
                -webkit-appearance: none;
                height: 20px;
                width: 20px;
                border-radius: 50%;
                background: #3b82f6;
                cursor: pointer;
                border: 2px solid white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) window.lucide.createIcons();
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const KeplerSim = () => {
                const [eccentricity, setEccentricity] = useState(0.5);
                const [semiMajorAxis, setSemiMajorAxis] = useState(140);
                const [isPlaying, setIsPlaying] = useState(false);
                const [showAxes, setShowAxes] = useState(true);
                const [showAreas, setShowAreas] = useState(false);
                const [timeFraction, setTimeFraction] = useState(8);
                const [planetPos, setPlanetPos] = useState({ x: 0, y: 0, angle: 0 });
                const canvasRef = useRef(null);

                // 시뮬레이션 물리 파라미터
                const a = semiMajorAxis;
                const e = eccentricity;
                const b = a * Math.sqrt(1 - e * e);
                const focusOffset = a * e;
                const baseSpeed = 100;

                useEffect(() => {
                    let animationFrame;
                    if (isPlaying) {
                        const animate = () => {
                            setPlanetPos(prev => {
                                const r = a * (1 - e * e) / (1 + e * Math.cos(prev.angle));
                                const deltaAngle = (baseSpeed / (r * r)) * 10; 
                                const newAngle = prev.angle + deltaAngle;
                                const x = -focusOffset + r * Math.cos(newAngle + Math.PI);
                                const y = r * Math.sin(newAngle + Math.PI);
                                return { x, y, angle: newAngle };
                            });
                            animationFrame = requestAnimationFrame(animate);
                        };
                        animate();
                    }
                    return () => cancelAnimationFrame(animationFrame);
                }, [isPlaying, e, a]);

                useEffect(() => {
                    setPlanetPos(prev => {
                        const r = a * (1 - e * e) / (1 + e * Math.cos(prev.angle));
                        const x = -focusOffset + r * Math.cos(prev.angle + Math.PI);
                        const y = r * Math.sin(prev.angle + Math.PI);
                        return { ...prev, x, y };
                    });
                }, [e, a]);

                useEffect(() => {
                    const canvas = canvasRef.current;
                    if (!canvas) return;
                    const ctx = canvas.getContext('2d');
                    const width = canvas.width;
                    const height = canvas.height;
                    const centerX = width / 2;
                    const centerY = height / 2;

                    ctx.clearRect(0, 0, width, height);

                    // 1. 궤도 도우미 (그리드)
                    ctx.strokeStyle = '#1e293b';
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(0, centerY); ctx.lineTo(width, centerY);
                    ctx.moveTo(centerX, 0); ctx.lineTo(centerX, height);
                    ctx.stroke();

                    // 2. 타원 궤도
                    ctx.beginPath();
                    ctx.ellipse(centerX, centerY, a, b, 0, 0, Math.PI * 2);
                    ctx.strokeStyle = '#475569';
                    ctx.setLineDash([5, 5]);
                    ctx.lineWidth = 1.5;
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // 3. 장반경, 단반경 표시 (옵션)
                    if (showAxes) {
                        ctx.lineWidth = 2;
                        // 장반경 (a) - 센터에서 근일점 축
                        ctx.strokeStyle = '#ef4444';
                        ctx.beginPath();
                        ctx.moveTo(centerX, centerY);
                        ctx.lineTo(centerX - a, centerY);
                        ctx.stroke();
                        // 단반경 (b) - 센터에서 위쪽 축
                        ctx.strokeStyle = '#10b981';
                        ctx.beginPath();
                        ctx.moveTo(centerX, centerY);
                        ctx.lineTo(centerX, centerY - b);
                        ctx.stroke();

                        ctx.font = 'bold 12px Pretendard';
                        ctx.fillStyle = '#ef4444'; ctx.fillText(`장반경(a): ${a}`, centerX - a/2 - 30, centerY - 10);
                        ctx.fillStyle = '#10b981'; ctx.fillText(`단반경(b): ${b.toFixed(0)}`, centerX + 10, centerY - b/2);
                    }

                    // 4. 면적 속도 일정 법칙 시각화 (동일 시간 구간 2개 표시)
                    if (showAreas) {
                        // 케플러 방정식 수치해석 (Mean Anomaly -> True Anomaly)
                        const solveKepler = (M, e) => {
                            let E = M;
                            for (let i = 0; i < 15; i++) {
                                E = E - (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
                            }
                            return E;
                        };
                        const getTrueAnomaly = (M, e) => {
                            const E = solveKepler(M, e);
                            return 2 * Math.atan2(Math.sqrt(1 + e) * Math.sin(E / 2), Math.sqrt(1 - e) * Math.cos(E / 2));
                        };

                        const drawSector = (startM, color, label) => {
                            ctx.beginPath();
                            ctx.fillStyle = color;
                            ctx.globalAlpha = 0.4;
                            ctx.moveTo(centerX - focusOffset, centerY);
                            
                            // 주기의 1/N 만큼의 시간(Mean Anomaly 각도) 경과
                            const dM = (Math.PI * 2) / timeFraction; 
                            const numSteps = 60;
                            
                            for(let i = 0; i <= numSteps; i++) {
                                const currentM = startM + (dM * i) / numSteps;
                                const theta = getTrueAnomaly(currentM, e);
                                const r = a * (1 - e * e) / (1 + e * Math.cos(theta));
                                const x = -focusOffset + r * Math.cos(theta + Math.PI);
                                const y = r * Math.sin(theta + Math.PI);
                                ctx.lineTo(centerX + x, centerY + y);
                            }
                            
                            ctx.lineTo(centerX - focusOffset, centerY);
                            ctx.fill();
                            ctx.globalAlpha = 1.0;
                            ctx.strokeStyle = color;
                            ctx.lineWidth = 1.5;
                            ctx.stroke();
                        };

                        drawSector(0, '#ef4444', '근일점 통과'); // 근일점 (왼쪽)
                        // 원일점 통과는 최원점을 중심으로 좌우 절반씩 면적을 차지하도록 시작점 조정
                        drawSector(Math.PI - (Math.PI / timeFraction), '#3b82f6', '원일점 통과');
                    }

                    // 5. 태양
                    ctx.beginPath();
                    ctx.arc(centerX - focusOffset, centerY, 15, 0, Math.PI * 2);
                    ctx.fillStyle = '#fbbf24';
                    ctx.shadowBlur = 20;
                    ctx.shadowColor = '#fbbf24';
                    ctx.fill();
                    ctx.shadowBlur = 0;

                    // 6. 행성 연결선 및 행성
                    ctx.beginPath();
                    ctx.moveTo(centerX - focusOffset, centerY);
                    ctx.lineTo(centerX + planetPos.x, centerY + planetPos.y);
                    ctx.strokeStyle = '#3b82f6';
                    ctx.lineWidth = 1;
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.arc(centerX + planetPos.x, centerY + planetPos.y, 8, 0, Math.PI * 2);
                    ctx.fillStyle = '#3b82f6';
                    ctx.fill();
                    ctx.strokeStyle = 'white'; ctx.lineWidth = 2; ctx.stroke();

                }, [planetPos, e, a, showAxes, showAreas]);

                return (
                    <div className="max-w-7xl mx-auto p-4 flex flex-col gap-6">
                        <div className="flex flex-col lg:flex-row gap-6">
                            {/* Main Simulation View */}
                            <div className="flex-1 space-y-4">
                                <div className="bg-slate-900 rounded-[3rem] overflow-hidden relative shadow-2xl border-x-[12px] border-y-[12px] border-slate-800 aspect-video flex items-center justify-center">
                                    <canvas ref={canvasRef} width={900} height={550} className="w-full h-auto" />
                                    
                                    {/* Info Overlay */}
                                    <div className="absolute top-8 left-8 flex flex-col gap-2">
                                        <div className="px-4 py-2 bg-black/60 backdrop-blur-md rounded-2xl border border-white/10 text-white text-[11px] font-black uppercase tracking-widest flex items-center gap-2">
                                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-ping"></div>
                                            Kepler System Live
                                        </div>
                                    </div>

                                    <div className="absolute bottom-8 right-8 flex gap-4 text-white text-[11px] bg-black/60 p-5 rounded-3xl backdrop-blur-md border border-white/10 font-bold">
                                        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-yellow-400 rounded-full shadow-[0_0_10px_#fbbf24]"></div> 태양 (초점)</div>
                                        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-blue-500 rounded-full shadow-[0_0_10px_#3b82f6]"></div> 행성</div>
                                        {showAreas && (
                                            <>
                                                <div className="flex items-center gap-2"><div className="w-3 h-3 bg-red-400/50 border border-red-400 rounded-sm"></div> 구역 A</div>
                                                <div className="flex items-center gap-2"><div className="w-3 h-3 bg-blue-400/50 border border-blue-400 rounded-sm"></div> 구역 B</div>
                                            </>
                                        )}
                                    </div>
                                </div>

                                {/* Comparison Dashboard */}
                                {showAreas && (
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-in slide-in-from-bottom-4 duration-500">
                                        <div className="bg-white p-6 rounded-[2rem] border border-slate-200 shadow-md flex items-center gap-6">
                                            <div className="w-16 h-16 bg-red-50 rounded-2xl flex items-center justify-center text-red-500 shrink-0 border border-red-100 italic font-black">A</div>
                                            <div>
                                                <h5 className="font-black text-slate-800 text-sm mb-1">근일점 구역 (Perihelion)</h5>
                                                <p className="text-xs text-slate-500 leading-relaxed pr-4">거리는 가깝지만 각도 변화가 커서 <span className="text-red-600 font-bold">넓고 얇은 부채꼴</span>을 형성합니다.</p>
                                            </div>
                                            <div className="ml-auto text-right">
                                                <span className="text-xs text-slate-400 uppercase font-black block">측정 면적</span>
                                                <span className="text-lg font-black text-slate-800">100.0%</span>
                                            </div>
                                        </div>
                                        <div className="bg-white p-6 rounded-[2rem] border border-slate-200 shadow-md flex items-center gap-6">
                                            <div className="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-500 shrink-0 border border-blue-100 italic font-black">B</div>
                                            <div>
                                                <h5 className="font-black text-slate-800 text-sm mb-1">원일점 구역 (Aphelion)</h5>
                                                <p className="text-xs text-slate-500 leading-relaxed pr-4">거리는 멀지만 각도 변화가 작아 <span className="text-blue-600 font-bold">좁고 긴 부채꼴</span>을 형성합니다.</p>
                                            </div>
                                            <div className="ml-auto text-right">
                                                <span className="text-xs text-slate-400 uppercase font-black block">측정 면적</span>
                                                <span className="text-lg font-black text-slate-800">100.0%</span>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* Control Sidebar */}
                            <div className="w-full lg:w-[350px] space-y-6">
                                <div className="bg-white p-8 rounded-[2.5rem] border border-slate-200 shadow-xl space-y-8">
                                    <h3 className="text-lg font-black text-slate-800 flex items-center gap-3">
                                        <div className="w-10 h-10 bg-blue-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-blue-200">
                                            <Icon name="sliders" size={20} />
                                        </div>
                                        궤도 분석 설정
                                    </h3>

                                    <div className="space-y-6">
                                        <div className="space-y-3">
                                            <div className="flex justify-between items-center">
                                                <label className="text-xs font-black text-slate-400 uppercase tracking-widest">이심률 (Eccentricity)</label>
                                                <span className="px-3 py-1 bg-blue-50 text-blue-600 rounded-full font-mono font-black text-sm">{e.toFixed(2)}</span>
                                            </div>
                                            <input type="range" min="0" max="0.8" step="0.01" value={e} onChange={(ev) => setEccentricity(parseFloat(ev.target.value))} className="w-full h-2 bg-slate-100 rounded-xl appearance-none cursor-pointer" />
                                        </div>

                                        <div className="grid grid-cols-2 gap-3 pt-2">
                                            <button onClick={() => setShowAxes(!showAxes)} className={`p-4 rounded-2xl border-2 transition-all flex flex-col items-center gap-2 font-bold text-[11px] ${showAxes ? 'border-blue-600 bg-blue-50 text-blue-600' : 'border-slate-100 text-slate-400 hover:border-slate-200'}`}>
                                                <Icon name="maximize" size={20} /> 장/단반경 {showAxes ? 'ON' : 'OFF'}
                                            </button>
                                            <button onClick={() => setShowAreas(!showAreas)} className={`p-4 rounded-2xl border-2 transition-all flex flex-col items-center gap-2 font-bold text-[11px] ${showAreas ? 'border-red-600 bg-red-50 text-red-600' : 'border-slate-100 text-slate-400 hover:border-slate-200'}`}>
                                                <Icon name="pie-chart" size={20} /> 면적 속도 {showAreas ? 'ON' : 'OFF'}
                                            </button>
                                        </div>

                                        {showAreas && (
                                            <div className="space-y-3 pt-2 animate-in fade-in zoom-in duration-300">
                                                <div className="flex justify-between items-center">
                                                    <label className="text-[11px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-1">
                                                        <Icon name="clock" size={14} /> 공전 관측 시간 (주기 T 기준)
                                                    </label>
                                                    <span className="px-3 py-1 bg-red-50 text-red-600 rounded-full font-mono font-black text-sm">T / {timeFraction}</span>
                                                </div>
                                                <input type="range" min="4" max="24" step="1" value={timeFraction} onChange={(ev) => setTimeFraction(parseInt(ev.target.value))} className="w-full h-2 bg-slate-100 rounded-xl appearance-none cursor-pointer" />
                                                <p className="text-[10px] text-slate-400 text-center">조절 바를 움직여 동일 시간 동안 쓸고 간 면적의 크기를 비교해 보세요.</p>
                                            </div>
                                        )}

                                        <div className="space-y-3 pt-4 border-t border-slate-50">
                                            <button onClick={() => setIsPlaying(!isPlaying)} className={`w-full py-5 rounded-[1.5rem] font-black text-lg shadow-xl transition-all flex items-center justify-center gap-3 ${isPlaying ? 'bg-slate-800 text-white' : 'bg-blue-600 text-white hover:bg-blue-700 shadow-blue-200'}`}>
                                                <Icon name={isPlaying ? "pause" : "play"} size={24} /> {isPlaying ? '시뮬레이션 중지' : '위성 발사하기'}
                                            </button>
                                            <button onClick={() => {setPlanetPos({x:0, y:0, angle:0}); setIsPlaying(false);}} className="w-full py-4 bg-slate-50 text-slate-400 rounded-[1.5rem] font-bold text-xs hover:bg-slate-100 flex items-center justify-center gap-2">
                                                <Icon name="refresh-cw" size={16} /> 데이터 초기화
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <div className="bg-slate-900 p-8 rounded-[2.5rem] text-white shadow-2xl relative overflow-hidden">
                                     <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-[60px]"></div>
                                     <h4 className="text-emerald-400 font-black text-xs uppercase tracking-widest mb-4 flex items-center gap-2">
                                        <Icon name="info" size={14} /> 학습 핵심 정리
                                     </h4>
                                     <div className="space-y-4">
                                        <div className="flex items-start gap-4">
                                            <div className="w-1 h-1 bg-white rounded-full mt-2"></div>
                                            <p className="text-[13px] text-slate-400 leading-relaxed font-medium">이심률(e)이 커질수록 두 초점 사이의 거리가 멀어지며 궤도가 더 길쭉한 타원이 됩니다.</p>
                                        </div>
                                        <div className="flex items-start gap-4">
                                            <div className="w-1 h-1 bg-white rounded-full mt-2"></div>
                                            <p className="text-[13px] text-slate-400 leading-relaxed font-medium">행성은 태양에 가까울 때 면적을 채우기 위해 더 빠르게 움직여야 합니다.</p>
                                        </div>
                                        <div className="p-4 bg-white/5 rounded-2xl border border-white/10 text-center text-sm font-mono text-blue-400 font-bold">
                                            Same Time = Same Area
                                        </div>
                                     </div>
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
    components.html(react_code, height=950, scrolling=False)

if __name__ == "__main__":
    run_sim()
