import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 조화의 법칙 데이터 분석", layout="wide")
    
    st.title("📊 케플러 제3법칙: 공전 주기와 궤도 반지름의 관계")
    st.markdown("""
    태양계 모든 행성(수성~토성)의 데이터를 통해 **조화의 법칙($T^2 \propto a^3$)**을 탐구합니다. 
    내행성부터 거대 행성인 토성까지의 비례 관계가 완벽하게 일치하는지 확인해 보세요.
    """)

    react_code = r"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/prop-types@15.8.1/prop-types.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/recharts@2.12.7/umd/Recharts.js"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            .planet-row { transition: all 0.2s ease; cursor: pointer; }
            .planet-row:hover { background-color: #f1f5f9; }
            .selected-row { background-color: #eff6ff !important; border-left: 4px solid #3b82f6 !important; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) window.lucide.createIcons();
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const KeplerData = () => {
                const [engineState, setEngineState] = useState('loading');
                const [selectedPlanet, setSelectedPlanet] = useState('지구');
                const [viewMode, setViewMode] = useState('all'); // 'all' or 'inner'

                useEffect(() => {
                    let attempts = 0;
                    const checkEngine = setInterval(() => {
                        attempts++;
                        if (window.Recharts) {
                            setEngineState('ready');
                            clearInterval(checkEngine);
                        } else if (attempts > 60) {
                            setEngineState('error');
                            clearInterval(checkEngine);
                        }
                    }, 100);
                    return () => clearInterval(checkEngine);
                }, []);

                if (engineState === 'loading') {
                    return <div className="flex h-80 items-center justify-center">로딩 중...</div>;
                }

                const { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Label } = window.Recharts;

                const planetData = [
                    { name: '수성', r: 0.39, t: 0.24, r3: 0.059, t2: 0.058, color: '#94a3b8', type: 'inner' },
                    { name: '금성', r: 0.72, t: 0.62, r3: 0.373, t2: 0.384, color: '#fbbf24', type: 'inner' },
                    { name: '지구', r: 1.00, t: 1.00, r3: 1.000, t2: 1.000, color: '#3b82f6', type: 'inner' },
                    { name: '화성', r: 1.52, t: 1.88, r3: 3.512, t2: 3.534, color: '#ef4444', type: 'inner' },
                    { name: '목성', r: 5.20, t: 11.86, r3: 140.6, t2: 140.7, color: '#f59e0b', type: 'outer' },
                    { name: '토성', r: 9.54, t: 29.46, r3: 868.3, t2: 867.9, color: '#a855f7', type: 'outer' }
                ];

                const currentPlanet = planetData.find(p => p.name === selectedPlanet) || planetData[2];
                
                // 도메인 설정: 토성까지 포함하기 위해 천(1000) 단위로 확장
                const chartDomain = viewMode === 'all' ? [0, 950] : [0, 5];

                return (
                    <div className="max-w-7xl mx-auto p-4 flex flex-col gap-8 animate-in fade-in duration-700 pb-20">
                        {/* Top: Large Chart Section */}
                        <div className="bg-white p-10 rounded-[3rem] border border-slate-200 shadow-2xl space-y-8">
                            <div className="flex flex-col md:flex-row justify-between items-end gap-6">
                                <div className="space-y-4">
                                    <h3 className="text-2xl font-black text-slate-800 flex items-center gap-4">
                                        <div className="w-14 h-14 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-xl shadow-indigo-100">
                                            <Icon name="activity" size={28} />
                                        </div>
                                        조화의 법칙 물리 데이터 분석
                                    </h3>
                                    <div className="flex gap-2">
                                         <button 
                                            onClick={() => setViewMode('all')}
                                            className={`px-8 py-3 rounded-2xl font-black text-[11px] uppercase tracking-tighter transition-all ${viewMode === 'all' ? 'bg-slate-900 text-white shadow-2xl scale-105' : 'bg-slate-100 text-slate-400 hover:bg-slate-200'}`}
                                         >
                                            전체 태양계 (수성~토성)
                                         </button>
                                         <button 
                                            onClick={() => setViewMode('inner')}
                                            className={`px-8 py-3 rounded-2xl font-black text-[11px] uppercase tracking-tighter transition-all ${viewMode === 'inner' ? 'bg-indigo-600 text-white shadow-2xl scale-105 shadow-indigo-200' : 'bg-slate-100 text-slate-400 hover:bg-slate-200'}`}
                                         >
                                            내행성 집중 (Mercury~Mars)
                                         </button>
                                    </div>
                                </div>
                                <div className="px-8 py-5 bg-slate-900 rounded-[2rem] text-white flex flex-col items-end gap-1 border border-white/10 shadow-2xl">
                                    <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Selected Object</span>
                                    <span className="text-indigo-400 font-black text-2xl tracking-tighter">{selectedPlanet}</span>
                                </div>
                            </div>

                            <div className="h-[600px] w-full bg-slate-50/50 p-10 rounded-[3.5rem] border border-slate-100 shadow-inner relative overflow-hidden">
                                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-500/5 rounded-full blur-[120px]"></div>
                                <ResponsiveContainer width="100%" height="100%">
                                    <ScatterChart margin={{ top: 20, right: 60, bottom: 80, left: 80 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                        <XAxis 
                                            type="number" dataKey="r3" name="r³" domain={chartDomain} 
                                            stroke="#64748b" tick={{fontSize: 12, fontWeight: 'bold'}}
                                            allowDataOverflow={true}
                                        >
                                            <Label value="궤도 장반경의 세제곱 r³ (AU³)" position="bottom" offset={50} style={{ fontSize: '15px', fontWeight: '900', fill: '#1e293b' }} />
                                        </XAxis>
                                        <YAxis 
                                            type="number" dataKey="t2" name="T²" domain={chartDomain} 
                                            stroke="#64748b" tick={{fontSize: 12, fontWeight: 'bold'}}
                                            allowDataOverflow={true}
                                        >
                                            <Label value="공전 주기의 제곱 T² (yr²)" angle={-90} position="left" offset={50} style={{ fontSize: '15px', fontWeight: '900', fill: '#1e293b' }} />
                                        </YAxis>
                                        <Tooltip 
                                            cursor={{ strokeDasharray: '3 3', stroke: '#6366f1' }} 
                                            content={({ active, payload }) => {
                                                if (active && payload && payload.length) {
                                                    const data = payload[0].payload;
                                                    return (
                                                        <div className="bg-slate-900 border border-slate-700 text-white p-8 shadow-[0_30px_60px_rgba(0,0,0,0.6)] rounded-[2.5rem] animate-in zoom-in-95 backdrop-blur-xl">
                                                            <p className="font-black text-indigo-400 text-2xl mb-4 flex items-center gap-3">
                                                                <span className="w-4 h-4 rounded-full bg-indigo-400 shadow-[0_0_15px_#818cf8]"></span>{data.name}
                                                            </p>
                                                            <div className="space-y-4 text-sm font-bold border-t border-white/10 pt-5">
                                                                <div className="flex justify-between gap-12"><span className="text-slate-500 uppercase text-[10px] tracking-widest">r³ Radius³ed</span> <span className="font-mono text-indigo-200 text-lg">{data.r3.toLocaleString()}</span></div>
                                                                <div className="flex justify-between gap-12"><span className="text-slate-500 uppercase text-[10px] tracking-widest">T² Period²ed</span> <span className="font-mono text-indigo-200 text-lg">{data.t2.toLocaleString()}</span></div>
                                                                <div className="mt-4 p-3 bg-white/5 rounded-xl border border-white/10 text-center">
                                                                    <span className="text-[10px] text-slate-500 block mb-1">Constant (T²/r³)</span>
                                                                    <span className="text-emerald-400 font-mono text-base">{(data.t2/data.r3).toFixed(5)}</span>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    );
                                                }
                                                return null;
                                            }} 
                                        />
                                        <Scatter 
                                            name="Planets" data={planetData} 
                                            onClick={(data) => setSelectedPlanet(data.name)}
                                            style={{cursor: 'pointer'}}
                                        >
                                            {planetData.map((entry, index) => (
                                                <Cell 
                                                    key={`cell-${index}`} 
                                                    fill={entry.name === selectedPlanet ? '#6366f1' : '#cbd5e1'} 
                                                    stroke={entry.name === selectedPlanet ? '#818cf8' : '#94a3b8'}
                                                    strokeWidth={entry.name === selectedPlanet ? 6 : 1}
                                                    r={entry.name === selectedPlanet ? 16 : 8}
                                                    style={{ transition: 'all 0.5s cubic-bezier(0.19, 1, 0.22, 1)' }}
                                                />
                                            ))}
                                        </Scatter>
                                    </ScatterChart>
                                </ResponsiveContainer>
                                <div className="absolute top-10 left-1/2 -translate-x-1/2 px-6 py-2 bg-indigo-600/10 text-indigo-600 rounded-full text-[11px] font-black uppercase tracking-[0.2em] border border-indigo-600/20 backdrop-blur-md">
                                    {viewMode === 'all' ? 'Solar System Scale' : 'Inner Planets Focus'}
                                </div>
                            </div>
                        </div>

                        {/* Bottom: Table and Details */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                            <div className="lg:col-span-2 bg-white p-10 rounded-[3rem] border border-slate-200 shadow-2xl">
                                <h3 className="text-xl font-black text-slate-800 mb-8 flex items-center gap-3">
                                    <Icon name="list-checks" className="text-indigo-600" /> 태양계 정밀 관측 데이터
                                </h3>
                                <div className="overflow-hidden rounded-3xl border border-slate-100 shadow-sm bg-white">
                                    <table className="w-full text-sm text-left border-collapse">
                                        <thead>
                                            <tr className="bg-slate-50 text-slate-400 border-b border-slate-100 uppercase tracking-widest text-[10px] font-black">
                                                <th className="p-6">Planet</th>
                                                <th className="p-6 text-center">Semi-major r (AU)</th>
                                                <th className="p-6 text-center">Period T (yr)</th>
                                                <th className="p-6 text-center text-indigo-600">r³ (AU³)</th>
                                                <th className="p-6 text-center text-amber-600">T² (yr²)</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {planetData.map((p) => (
                                                <tr 
                                                    key={p.name} 
                                                    onClick={() => setSelectedPlanet(p.name)}
                                                    className={`planet-row border-b border-slate-50 last:border-0 ${p.name === selectedPlanet ? 'selected-row' : ''}`}
                                                >
                                                    <td className="p-6 font-black text-slate-800 flex items-center gap-4">
                                                        <div className="w-3 h-3 rounded-full shadow-lg" style={{backgroundColor: p.color}}></div>
                                                        {p.name}
                                                    </td>
                                                    <td className="p-6 text-center font-mono text-slate-400">{p.r.toFixed(2)}</td>
                                                    <td className="p-6 text-center font-mono text-slate-400">{p.t.toFixed(2)}</td>
                                                    <td className={`p-6 text-center font-mono font-black ${p.name === selectedPlanet ? 'text-indigo-600' : 'text-slate-500'}`}>{p.r3.toLocaleString()}</td>
                                                    <td className={`p-6 text-center font-mono font-black ${p.name === selectedPlanet ? 'text-amber-600' : 'text-slate-500'}`}>{p.t2.toLocaleString()}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div className="bg-slate-900 p-12 rounded-[3rem] text-white flex flex-col justify-between shadow-2xl relative overflow-hidden group">
                                <div className="absolute top-0 right-0 w-48 h-48 bg-indigo-500/20 rounded-full blur-[80px]"></div>
                                <div>
                                    <div className="flex items-center gap-3 text-indigo-400 mb-8 font-black tracking-widest uppercase text-xs">
                                        <Icon name="search" size={18} /> Deep Discovery
                                    </div>
                                    <h4 className="text-5xl font-black mb-4 text-white hover:text-indigo-400 transition-colors">{currentPlanet.name}</h4>
                                    <p className="text-slate-400 text-sm font-bold mb-12 leading-relaxed italic pr-4">
                                        "거리의 세제곱과 주기의 제곱은 어떤 행성에서도 한결같은 비례를 유지합니다."
                                    </p>
                                    <div className="space-y-8">
                                        <div className="p-8 bg-white/5 rounded-[2rem] border border-white/10 shadow-inner group-hover:border-indigo-500/30 transition-all">
                                            <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest mb-3">Constant K = T² / r³</p>
                                            <p className="text-4xl font-mono font-black text-indigo-400">{(currentPlanet.t2/currentPlanet.r3).toFixed(5)}</p>
                                        </div>
                                        <div className="flex items-center gap-4 p-5 bg-emerald-600/10 rounded-2xl border border-emerald-600/20">
                                            <div className="w-10 h-10 bg-emerald-600 rounded-xl flex items-center justify-center text-white shrink-0">
                                                <Icon name="check" size={20} />
                                            </div>
                                            <p className="text-[11px] font-black text-emerald-400 leading-snug">케플러 제3법칙이 수치적으로 완벽하게 성립함을 증명하고 있습니다.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerData />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=1250, scrolling=False)

if __name__ == "__main__":
    run_sim()
