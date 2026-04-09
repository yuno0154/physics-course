import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 조화의 법칙 데이터 분석", layout="wide")
    
    st.title("📊 케플러 제3법칙: 공전 주기와 궤도 반지름의 관계")
    st.markdown("""
    태양계 실제 행성들의 데이터를 탐구하고, **가상의 행성**이 발견되었다면 어떤 궤도 특성을 가질지 직접 예측해 보세요.
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
            input[type="number"]::-webkit-inner-spin-button { opacity: 1; }
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
                const [viewMode, setViewMode] = useState('all');
                
                // 가상 행성 상태
                const [virtualR, setVirtualR] = useState(3.0);
                const [virtualT, setVirtualT] = useState(Math.sqrt(Math.pow(3.0, 3)));
                const [showVirtual, setShowVirtual] = useState(false);

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

                const handleVirtualRChange = (val) => {
                    const r = parseFloat(val);
                    if (!isNaN(r)) {
                        setVirtualR(r);
                        setVirtualT(Math.sqrt(Math.pow(r, 3)));
                        setShowVirtual(true);
                    }
                };

                const handleVirtualTChange = (val) => {
                    const t = parseFloat(val);
                    if (!isNaN(t)) {
                        setVirtualT(t);
                        setVirtualR(Math.pow(Math.pow(t, 2), 1/3));
                        setShowVirtual(true);
                    }
                };

                if (engineState === 'loading') {
                    return <div className="flex h-80 items-center justify-center">로딩 중...</div>;
                }

                const { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Label } = window.Recharts;

                const actualPlanetData = [
                    { name: '수성', r: 0.39, t: 0.24, r3: 0.059, t2: 0.058, color: '#94a3b8', type: 'inner' },
                    { name: '금성', r: 0.72, t: 0.62, r3: 0.373, t2: 0.384, color: '#fbbf24', type: 'inner' },
                    { name: '지구', r: 1.00, t: 1.00, r3: 1.000, t2: 1.000, color: '#3b82f6', type: 'inner' },
                    { name: '화성', r: 1.52, t: 1.88, r3: 3.512, t2: 3.534, color: '#ef4444', type: 'inner' },
                    { name: '목성', r: 5.20, t: 11.86, r3: 140.6, t2: 140.7, color: '#f59e0b', type: 'outer' },
                    { name: '토성', r: 9.54, t: 29.46, r3: 868.3, t2: 867.9, color: '#a855f7', type: 'outer' }
                ];

                const virtualPlanet = { 
                    name: '가상 행성 (X)', 
                    r: virtualR, t: virtualT, 
                    r3: Math.pow(virtualR, 3), t2: Math.pow(virtualT, 2), 
                    color: '#22d3ee', isVirtual: true 
                };

                const planetData = showVirtual ? [...actualPlanetData, virtualPlanet] : actualPlanetData;
                const currentPlanet = selectedPlanet === '가상 행성 (X)' ? virtualPlanet : (actualPlanetData.find(p => p.name === selectedPlanet) || actualPlanetData[2]);
                
                const chartDomain = viewMode === 'all' ? [0, 950] : [0, 50];

                return (
                    <div className="max-w-7xl mx-auto p-4 flex flex-col gap-8 pb-32">
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
                                            className={`px-8 py-3 rounded-2xl font-black text-[11px] transition-all ${viewMode === 'all' ? 'bg-slate-900 text-white shadow-2xl' : 'bg-slate-100 text-slate-400 hover:bg-slate-200'}`}
                                         >
                                            전체 태양계 View
                                         </button>
                                         <button 
                                            onClick={() => setViewMode('inner')}
                                            className={`px-8 py-3 rounded-2xl font-black text-[11px] transition-all ${viewMode === 'inner' ? 'bg-indigo-600 text-white shadow-2xl' : 'bg-slate-100 text-slate-400 hover:bg-slate-200'}`}
                                         >
                                            궤도 집중 View (확대)
                                         </button>
                                    </div>
                                </div>
                                <div className="px-8 py-5 bg-slate-900 rounded-[2rem] text-white flex flex-col items-end gap-1 border border-white/10 shadow-2xl">
                                    <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Select Object</span>
                                    <span className="text-indigo-400 font-black text-2xl tracking-tighter">{selectedPlanet}</span>
                                </div>
                            </div>

                            <div className="h-[600px] w-full bg-slate-50/50 p-10 rounded-[3.5rem] border border-slate-100 shadow-inner relative overflow-hidden">
                                <ResponsiveContainer width="100%" height="100%">
                                    <ScatterChart margin={{ top: 20, right: 60, bottom: 80, left: 80 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                        <XAxis type="number" dataKey="r3" domain={chartDomain} stroke="#64748b" tick={{fontSize: 12, fontWeight: 'bold'}} allowDataOverflow={true}>
                                            <Label value="r³ (AU³)" position="bottom" offset={50} style={{ fontSize: '15px', fontWeight: '900', fill: '#1e293b' }} />
                                        </XAxis>
                                        <YAxis type="number" dataKey="t2" domain={chartDomain} stroke="#64748b" tick={{fontSize: 12, fontWeight: 'bold'}} allowDataOverflow={true}>
                                            <Label value="T² (yr²)" angle={-90} position="left" offset={50} style={{ fontSize: '15px', fontWeight: '900', fill: '#1e293b' }} />
                                        </YAxis>
                                        <Tooltip 
                                            cursor={{ strokeDasharray: '3 3' }} 
                                            content={({ active, payload }) => {
                                                if (active && payload && payload.length) {
                                                    const d = payload[0].payload;
                                                    return (
                                                        <div className="bg-slate-900 border border-slate-700 text-white p-6 shadow-2xl rounded-3xl backdrop-blur-xl">
                                                            <p className="font-black text-indigo-400 text-lg mb-2">{d.name}</p>
                                                            <div className="space-y-1 text-xs font-bold font-mono">
                                                                <p>r³: {d.r3.toLocaleString()}</p>
                                                                <p>T²: {d.t2.toLocaleString()}</p>
                                                            </div>
                                                        </div>
                                                    );
                                                }
                                                return null;
                                            }} 
                                        />
                                        <Scatter 
                                            name="Planets" data={planetData} 
                                            onClick={(d) => setSelectedPlanet(d.name)}
                                            style={{cursor: 'pointer'}}
                                        >
                                            {planetData.map((entry, index) => (
                                                <Cell 
                                                    key={`cell-${index}`} 
                                                    fill={entry.name === selectedPlanet ? (entry.isVirtual ? '#22d3ee' : '#6366f1') : (entry.isVirtual ? '#b8f2f2' : '#cbd5e1')} 
                                                    stroke={entry.isVirtual ? '#22d3ee' : (entry.name === selectedPlanet ? '#818cf8' : '#94a3b8')}
                                                    strokeWidth={entry.name === selectedPlanet ? 6 : 1}
                                                    r={entry.name === selectedPlanet ? 16 : 8}
                                                    style={{ transition: 'all 0.5s cubic-bezier(0.19, 1, 0.22, 1)' }}
                                                />
                                            ))}
                                        </Scatter>
                                    </ScatterChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Mid Section: Table and Virtual Lab */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                            <div className="lg:col-span-2 bg-white p-10 rounded-[3rem] border border-slate-200 shadow-xl overflow-hidden">
                                <h3 className="text-xl font-black text-slate-800 mb-8 flex items-center gap-3">
                                    <Icon name="list-checks" className="text-indigo-600" /> 태양계 정밀 관측 데이터
                                </h3>
                                <div className="overflow-hidden rounded-3xl border border-slate-100">
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
                                            {actualPlanetData.map((p) => (
                                                <tr key={p.name} onClick={() => setSelectedPlanet(p.name)} className={`planet-row border-b border-slate-50 ${p.name === selectedPlanet ? 'selected-row' : ''}`}>
                                                    <td className="p-6 font-black text-slate-800 flex items-center gap-4">
                                                        <div className="w-3 h-3 rounded-full" style={{backgroundColor: p.color}}></div>
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

                            {/* [IMPORTANT] Virtual Planet Lab */}
                            <div className="bg-slate-900 p-10 rounded-[3rem] text-white shadow-2xl space-y-8 flex flex-col justify-between">
                                <div>
                                    <h4 className="text-indigo-400 font-black text-xs tracking-widest uppercase mb-4 flex items-center gap-2">
                                        <Icon name="rocket" size={16} /> 가상 행성 탐사 시뮬레이터
                                    </h4>
                                    <p className="text-xl font-black mb-6 leading-tight text-white">우리가 새로운 행성을 발견한다면?</p>
                                    
                                    <div className="space-y-6">
                                        <div className="p-6 bg-white/5 rounded-2xl border border-white/10 group hover:border-cyan-500/50 transition-all">
                                            <label className="block text-[10px] font-bold text-slate-500 uppercase mb-3">장반경 r 입력 (AU)</label>
                                            <input 
                                                type="number" value={virtualR.toFixed(2)} 
                                                onChange={(e) => handleVirtualRChange(e.target.value)}
                                                className="w-full bg-transparent text-3xl font-mono font-black text-white focus:outline-none focus:text-cyan-400"
                                                step="0.1" min="0.1"
                                            />
                                        </div>
                                        <div className="flex justify-center">
                                            <Icon name="arrow-down-up" className="text-slate-700 animate-pulse" />
                                        </div>
                                        <div className="p-6 bg-white/5 rounded-2xl border border-white/10 group hover:border-cyan-500/50 transition-all">
                                            <label className="block text-[10px] font-bold text-slate-500 uppercase mb-3">예측된 공전 주기 T (YR)</label>
                                            <input 
                                                type="number" value={virtualT.toFixed(2)} 
                                                onChange={(e) => handleVirtualTChange(e.target.value)}
                                                className="w-full bg-transparent text-3xl font-mono font-black text-white focus:outline-none focus:text-cyan-400"
                                                step="0.1" min="0.1"
                                            />
                                        </div>
                                    </div>
                                </div>

                                <div className="p-4 bg-cyan-600/10 rounded-2xl border border-cyan-600/20 text-center">
                                    <p className="text-[10px] text-cyan-400 font-bold mb-1">Kepler Predictor Result ($T = \sqrt{r^3}$)</p>
                                    <p className="text-xs text-slate-300 font-medium leading-relaxed">입력된 조건에서 행성은 약 <span className="text-cyan-400 font-black">{virtualT.toFixed(2)}</span>년마다 태양을 공전합니다.</p>
                                    <button onClick={() => {setShowVirtual(true); setSelectedPlanet('가상 행성 (X)')}} className="mt-4 w-full py-3 bg-cyan-600 text-white rounded-xl font-black text-xs hover:bg-cyan-500 shadow-lg shadow-cyan-900/40">그래프에 표시하기</button>
                                </div>
                            </div>
                        </div>

                        {/* Summary Footer */}
                        <div className="bg-white p-10 rounded-[3rem] border border-slate-200 shadow-xl flex flex-col md:flex-row items-center gap-10">
                            <div className="bg-indigo-50 p-8 rounded-3xl flex items-center justify-center text-indigo-600 shrink-0">
                                <Icon name="lightbulb" size={40} />
                            </div>
                            <div>
                                <h4 className="text-lg font-black text-slate-800 mb-2">무엇을 발견했나요?</h4>
                                <p className="text-sm text-slate-500 font-medium leading-relaxed">
                                    실제 행성 데이터뿐만 아니라 우리가 직접 설정한 가상의 행성도 그래프상의 **동일한 직선** 위에 위치함을 알 수 있습니다. 
                                    이는 $T^2 = k \times r^3$ 이라는 조화의 법칙이 태양을 중심으로 공전하는 모든 천체에 보편적으로 성립하는 우주의 법칙임을 시사합니다.
                                </p>
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
    components.html(react_code, height=1700, scrolling=False)

if __name__ == "__main__":
    run_sim()
