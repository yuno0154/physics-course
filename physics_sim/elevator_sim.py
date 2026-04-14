import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    # React 컴포넌트를 위한 HTML/JS 소스
    react_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>엘리베이터 관성력 시뮬레이션</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.5/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background-color: #f8fafc; }
            #root { min-height: 100vh; }
            .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(226, 232, 240, 1); }
            .vector-label { font-weight: 800; font-style: italic; font-size: 11px; }
            .num-font { font-family: 'Consolas', monospace; }
        </style>
    </head>
    <body>
        <div id="root">
            <div style="display: flex; justify-content: center; align-items: center; height: 100vh; color: #64748b;">불러오는 중...</div>
        </div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) window.lucide.createIcons();
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const App = () => {
                const [accel, setAccel] = useState(0);
                const [mass, setMass] = useState(60);
                const [view, setView] = useState('internal'); 
                const [isMoving, setIsMoving] = useState(false);
                const [history, setHistory] = useState([]);
                
                const posRef = useRef(0);
                const velRef = useRef(0);
                const [renderPos, setRenderPos] = useState(0);

                const g = 9.8;
                const apparentWeight = mass * (g + accel);
                const inertialForce = -mass * accel;

                useEffect(() => {
                    let animationId;
                    let lastTime = performance.now();

                    const animate = (time) => {
                        const dt = Math.min((time - lastTime) / 1000, 0.05);
                        lastTime = time;

                        if (isMoving) {
                            velRef.current += accel * dt;
                            posRef.current -= velRef.current * dt * 25; 
                            if (posRef.current > 120) posRef.current = -120;
                            if (posRef.current < -120) posRef.current = 120;
                            setRenderPos(posRef.current);
                        }
                        animationId = requestAnimationFrame(animate);
                    };
                    animationId = requestAnimationFrame(animate);
                    return () => cancelAnimationFrame(animationId);
                }, [isMoving, accel]);

                const addRecord = () => {
                    setHistory(prev => [{
                        id: Date.now(),
                        accel: accel.toFixed(1),
                        actual: (mass * g).toFixed(1),
                        apparent: apparentWeight.toFixed(1),
                        inertial: inertialForce.toFixed(1)
                    }, ...prev].slice(0, 10));
                };

                return (
                    <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-8">
                        <div className="flex items-center gap-4 mb-8">
                            <div className="bg-sky-600 p-3 rounded-2xl shadow-lg">
                                <Icon name="box" size={28} className="text-white" />
                            </div>
                            <div>
                                <h1 className="text-3xl font-black text-slate-900 tracking-tight">엘리베이터와 겉보기 무게 탐구</h1>
                                <p className="text-slate-500 font-medium">가속되는 엘리베이터 안에서의 체중 변화 분석</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                            <div className="lg:col-span-4 space-y-6">
                                <div className="glass-card p-6 rounded-[32px] space-y-6">
                                    <div className="space-y-4">
                                        <div className="flex bg-slate-100 p-1 rounded-2xl">
                                            <button onClick={() => setView('external')} className={`flex-1 py-2 rounded-xl text-xs font-bold ${view === 'external' ? 'bg-white shadow-sm text-sky-600' : 'text-slate-500'}`}>외부 (관성계)</button>
                                            <button onClick={() => setView('internal')} className={`flex-1 py-2 rounded-xl text-xs font-bold ${view === 'internal' ? 'bg-white shadow-sm text-sky-600' : 'text-slate-500'}`}>내부 (비관성계)</button>
                                        </div>
                                        <div className="space-y-4 pt-2">
                                            <div className="space-y-2">
                                                <div className="flex justify-between text-xs font-black text-slate-400 uppercase">가속도 (a) <span className="text-sky-600">{accel.toFixed(1)} m/s²</span></div>
                                                <input type="range" min="-9.8" max="10" step="0.2" value={accel} onChange={(e)=>setAccel(parseFloat(e.target.value))} className="w-full" />
                                            </div>
                                            <div className="space-y-2">
                                                <div className="flex justify-between text-xs font-black text-slate-400 uppercase">사람 질량 (m) <span className="text-slate-800">{mass} kg</span></div>
                                                <input type="range" min="10" max="150" value={mass} onChange={(e)=>setMass(parseInt(e.target.value))} className="w-full" />
                                            </div>
                                        </div>
                                        <div className="flex flex-col gap-2">
                                            <button onClick={()=>setIsMoving(!isMoving)} className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-3 ${isMoving ? 'bg-rose-500 text-white' : 'bg-sky-600 text-white shadow-lg shadow-sky-100'}`}>
                                                <Icon name={isMoving ? "pause" : "play"} /> {isMoving ? "실험 중지" : "운동 시작"}
                                            </button>
                                            <button onClick={addRecord} className="w-full py-3 rounded-2xl bg-slate-800 text-white font-bold text-xs flex items-center justify-center gap-2">
                                                <Icon name="save" size={14} /> 데이터 기록
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="glass-card p-6 rounded-[32px] space-y-3">
                                    <h3 className="text-[10px] font-black text-slate-400 p-2 uppercase border-l-2 border-sky-500">Live SCALE Reading</h3>
                                    <div className="bg-slate-900 p-6 rounded-3xl text-center">
                                        <span className={`text-4xl font-black num-font ${Math.abs(accel) < 0.1 ? 'text-white' : (accel > 0 ? 'text-emerald-400' : 'text-rose-400')}`}>{apparentWeight.toFixed(1)}</span>
                                        <span className="text-slate-500 ml-1 font-bold">N</span>
                                    </div>
                                </div>
                            </div>

                            <div className="lg:col-span-8 flex flex-col gap-6">
                                <div className="bg-white rounded-[40px] shadow-xl border border-slate-100 overflow-hidden relative h-[500px]">
                                    <div className="p-4 bg-slate-900 flex justify-between text-white/50 text-[10px] font-black uppercase">
                                        <span>Elevator Shaft View</span>
                                        <div className="flex gap-4">
                                            <span className="text-emerald-400">● Gravity</span>
                                            <span className="text-blue-400">● Normal Force</span>
                                            {view==='internal' && <span className="text-rose-400">● Inertial</span>}
                                        </div>
                                    </div>
                                    <div className="relative h-full bg-slate-50">
                                        <svg viewBox="0 0 600 450" className="w-full h-full select-none">
                                            <defs>
                                                <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#3b82f6" /></marker>
                                                <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#10b981" /></marker>
                                                <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 2 L 10 5 L 0 8 Z" fill="#f43f5e" /></marker>
                                            </defs>
                                            <g transform={`translate(200, ${view === 'external' ? renderPos + 100 : 85})`}>
                                                <rect x="0" y="0" width="200" height="280" rx="12" fill="white" stroke="#64748b" strokeWidth="4" />
                                                <rect x="30" y="240" width="140" height="15" rx="4" fill="#f1f5f9" stroke="#94a3b8" />
                                                <g transform="translate(100, 240) scale(0.9)">
                                                    <circle cx="0" cy="-140" r="20" fill="#334155" />
                                                    <path d="M -15 -120 Q 0 -125 15 -120 L 20 -60 L -20 -60 Z" fill="#334155" />
                                                    <rect x="-18" y="-60" width="15" height="60" rx="4" fill="#334155" />
                                                    <rect x="3" y="-60" width="15" height="60" rx="4" fill="#334155" />
                                                </g>
                                                <g transform="translate(100, 160)">
                                                    <line x1="0" y1="0" x2="0" y2="60" stroke="#10b981" strokeWidth="4" markerEnd="url(#arrow-green)" />
                                                    <line x1="0" y1="0" x2="0" y2={-apparentWeight/15} stroke="#3b82f6" strokeWidth="4" markerEnd="url(#arrow-blue)" />
                                                    {view === 'internal' && Math.abs(accel) > 0.1 && (
                                                        <line x1="0" y1="0" x2="0" y2={-inertialForce/15} stroke="#f43f5e" strokeWidth="2" strokeDasharray="4,2" markerEnd="url(#arrow-red)" />
                                                    )}
                                                </g>
                                            </g>
                                        </svg>
                                    </div>
                                </div>

                                <div className="glass-card rounded-[32px] p-6 overflow-hidden">
                                     <table className="w-full text-center text-xs">
                                        <thead className="text-slate-400 font-black uppercase tracking-widest border-b border-slate-100">
                                            <tr><th className="pb-3 text-left pl-4">가속도</th><th>몸무게(N)</th><th>측정치(N)</th><th>관성력(N)</th></tr>
                                        </thead>
                                        <tbody>
                                            {history.map(h => (
                                                <tr key={h.id} className="border-b border-slate-50 last:border-0 hover:bg-slate-50/50">
                                                    <td className="py-3 text-left pl-4 font-black">{h.accel}</td>
                                                    <td className="num-font">{h.actual}</td>
                                                    <td className="num-font font-black text-sky-600">{h.apparent}</td>
                                                    <td className="num-font text-rose-400">{h.inertial}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<App />);
        </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트로 HTML 삽입
    components.html(react_code, height=1200, scrolling=True)

if __name__ == "__main__":
    run_sim()
