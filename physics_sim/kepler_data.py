import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 조화의 법칙 데이터 분석", layout="wide")
    
    st.title("📊 케플러 제3법칙: 공전 주기와 궤도 반지름의 관계")
    st.markdown("""
    실제 행성 데이터와 가상의 행성 예측 시뮬레이션을 통해 **조화의 법칙($T^2 \\propto r^3$)**을 탐구합니다.
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
            .planet-row:hover { background-color: #f8fafc; cursor: pointer; }
            .selected-row { background-color: #f1f5f9 !important; border-left: 4px solid #6366f1 !important; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => { if (window.lucide) window.lucide.createIcons(); }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const KeplerData = () => {
                const [engineReady, setEngineReady] = useState(false);
                const [selectedPlanet, setSelectedPlanet] = useState('지구');
                const [viewMode, setViewMode] = useState('all');
                const [virtualR, setVirtualR] = useState(3.0);
                const [virtualT, setVirtualT] = useState(5.2);
                const [showVirtual, setShowVirtual] = useState(false);

                useEffect(() => {
                    const timer = setInterval(() => {
                        if (window.Recharts && window.lucide) {
                            setEngineReady(true);
                            clearInterval(timer);
                        }
                    }, 100);
                    return () => clearInterval(timer);
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
                        setVirtualR(Math.pow(t * t, 1/3));
                        setShowVirtual(true);
                    }
                };

                if (!engineReady) return <div className="p-20 text-center font-bold text-slate-400">데이터 분석 엔진 로딩 중...</div>;

                const { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Label } = window.Recharts;

                const actualData = [
                    { name: '수성', r: 0.39, t: 0.24, r3: 0.059, t2: 0.058, color: '#94a3b8' },
                    { name: '금성', r: 0.72, t: 0.62, r3: 0.373, t2: 0.384, color: '#fbbf24' },
                    { name: '지구', r: 1.00, t: 1.00, r3: 1.000, t2: 1.000, color: '#3b82f6' },
                    { name: '화성', r: 1.52, t: 1.88, r3: 3.512, t2: 3.534, color: '#ef4444' },
                    { name: '목성', r: 5.20, t: 11.86, r3: 140.6, t2: 140.7, color: '#f59e0b' },
                    { name: '토성', r: 9.54, t: 29.46, r3: 868.3, t2: 867.9, color: '#a855f7' }
                ];

                const virtualPlanet = { 
                    name: '가상 행성 (X)', r: virtualR, t: virtualT, 
                    r3: Math.pow(virtualR, 3), t2: Math.pow(virtualT, 2), 
                    color: '#22d3ee', isVirtual: true 
                };

                const planetData = showVirtual ? [...actualData, virtualPlanet] : actualData;
                const current = selectedPlanet === '가상 행성 (X)' ? virtualPlanet : (actualData.find(p => p.name === selectedPlanet) || actualData[2]);
                const chartDomain = viewMode === 'all' ? [0, 950] : [0, 50];

                return (
                    <div className="max-w-7xl mx-auto p-4 flex flex-col gap-8 pb-32">
                        <div className="bg-white p-10 rounded-[3rem] border border-slate-200 shadow-xl space-y-6">
                            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                                <h3 className="text-2xl font-black text-slate-800 flex items-center gap-3">
                                    <Icon name="bar-chart-3" className="text-indigo-600" /> 조화의 법칙 데이터 분석
                                </h3>
                                <div className="flex gap-2 bg-slate-100 p-1.5 rounded-2xl">
                                    <button onClick={() => setViewMode('all')} className={`px-5 py-2.5 rounded-xl text-xs font-black transition-all ${viewMode === 'all' ? 'bg-white shadow-md text-slate-900' : 'text-slate-500'}`}>태양계 전체</button>
                                    <button onClick={() => setViewMode('inner')} className={`px-5 py-2.5 rounded-xl text-xs font-black transition-all ${viewMode === 'inner' ? 'bg-white shadow-md text-slate-900' : 'text-slate-500'}`}>궤도 확대</button>
                                </div>
                            </div>

                            <div className="h-[550px] w-full bg-slate-50 p-6 rounded-[2.5rem] border border-slate-100 shadow-inner relative">
                                <div className="absolute top-8 right-8 z-10 px-4 py-2 bg-indigo-900 text-indigo-100 rounded-2xl text-[10px] font-black uppercase tracking-widest">{selectedPlanet}</div>
                                <ResponsiveContainer width="100%" height="100%">
                                    <ScatterChart margin={{ top: 20, right: 40, bottom: 60, left: 60 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                        <XAxis type="number" dataKey="r3" domain={chartDomain} stroke="#94a3b8" tick={{fontSize: 11, fontWeight: 700}} allowDataOverflow>
                                            <Label value="r³ (AU³)" position="bottom" offset={35} style={{fontSize: 12, fontWeight: 800}} />
                                        </XAxis>
                                        <YAxis type="number" dataKey="t2" domain={chartDomain} stroke="#94a3b8" tick={{fontSize: 11, fontWeight: 700}} allowDataOverflow>
                                            <Label value="T² (yr²)" angle={-90} position="left" offset={35} style={{fontSize: 12, fontWeight: 800}} />
                                        </YAxis>
                                        <Tooltip cursor={{ strokeDasharray: '4 4' }} content={({ active, payload }) => {
                                            if (active && payload && payload.length) {
                                                const d = payload[0].payload;
                                                return (
                                                    <div className="bg-slate-900 text-white p-5 rounded-3xl shadow-2xl border border-slate-700 min-w-[120px]">
                                                        <p className="font-black text-indigo-400 mb-2">{d.name}</p>
                                                        <div className="text-[11px] font-bold font-mono opacity-80">
                                                            <p>r³: {d.r3.toLocaleString()}</p>
                                                            <p>T²: {d.t2.toLocaleString()}</p>
                                                        </div>
                                                    </div>
                                                );
                                            }
                                            return null;
                                        }} />
                                        <Scatter data={planetData} onClick={(d) => setSelectedPlanet(d.name)}>
                                            {planetData.map((e, i) => (
                                                <Cell key={i} fill={e.name === selectedPlanet ? (e.isVirtual ? '#22d3ee' : '#6366f1') : '#cbd5e1'} stroke={e.isVirtual ? '#22d3ee' : '#cbd5e1'} strokeWidth={e.name === selectedPlanet ? 4 : 1} r={e.name === selectedPlanet ? 14 : 7} style={{ transition: 'all 0.3s ease' }} />
                                            ))}
                                        </Scatter>
                                    </ScatterChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        <div className="grid lg:grid-cols-3 gap-8">
                            <div className="lg:col-span-2 bg-white p-10 rounded-[3rem] border border-slate-200 shadow-xl overflow-x-auto">
                                <h4 className="font-black mb-6 flex items-center gap-2"><Icon name="table" /> 태양계 정밀 데이터</h4>
                                <table className="w-full text-sm">
                                    <thead><tr className="text-slate-400 border-b border-slate-100 text-[10px] font-black uppercase text-center"><th className="p-4 text-left">행성</th><th>반지름 r</th><th>주기 T</th><th className="text-indigo-600">r³</th><th className="text-amber-600">T²</th></tr></thead>
                                    <tbody>
                                        {actualData.map((p) => (
                                            <tr key={p.name} onClick={() => setSelectedPlanet(p.name)} className={`planet-row border-b border-slate-50 last:border-0 ${p.name === selectedPlanet ? 'selected-row' : ''}`}>
                                                <td className="p-4 font-black flex items-center gap-3"><div className="w-2.5 h-2.5 rounded-full" style={{backgroundColor: p.color}}></div>{p.name}</td>
                                                <td className="text-center font-mono opacity-60">{p.r.toFixed(2)}</td>
                                                <td className="text-center font-mono opacity-60">{p.t.toFixed(2)}</td>
                                                <td className="text-center font-mono font-black text-indigo-600">{p.r3.toLocaleString()}</td>
                                                <td className="text-center font-mono font-black text-amber-600">{p.t2.toLocaleString()}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>

                            <div className="bg-slate-900 p-10 rounded-[3rem] text-white shadow-2xl flex flex-col justify-between">
                                <div className="space-y-6">
                                    <h4 className="text-indigo-400 font-black text-[10px] uppercase tracking-[0.3em]">Virtual Explorer</h4>
                                    <div className="space-y-4">
                                        <div className="p-5 bg-white/5 rounded-2xl border border-white/10">
                                            <label className="text-[10px] font-bold text-slate-500 uppercase block mb-2">장반경 r (AU)</label>
                                            <input type="number" value={virtualR.toFixed(2)} onChange={(e) => handleVirtualRChange(e.target.value)} className="w-full bg-transparent text-2xl font-black focus:outline-none" step="0.1" />
                                        </div>
                                        <div className="p-5 bg-white/5 rounded-2xl border border-white/10">
                                            <label className="text-[10px] font-bold text-slate-500 uppercase block mb-2">공전 주기 T (YR)</label>
                                            <input type="number" value={virtualT.toFixed(2)} onChange={(e) => handleVirtualTChange(e.target.value)} className="w-full bg-transparent text-2xl font-black focus:outline-none" step="0.1" />
                                        </div>
                                    </div>
                                    <button onClick={() => {setShowVirtual(true); setSelectedPlanet('가상 행성 (X)')}} className="w-full py-4 bg-cyan-600 hover:bg-cyan-500 rounded-2xl font-black text-xs transition-colors shadow-lg">그래프에 매핑하기</button>
                                </div>
                                <div className="mt-8 pt-8 border-t border-white/10">
                                    <p className="text-[11px] font-bold text-slate-400 mb-2">Constant check (T²/r³)</p>
                                    <p className="text-3xl font-black text-emerald-400 font-mono">{(current.t2/current.r3).toFixed(4)}</p>
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
    components.html(react_code, height=1350, scrolling=True)

if __name__ == "__main__":
    run_sim()
