import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 조화의 법칙 데이터 분석", layout="wide")
    
    st.title("📊 케플러 제3법칙: 공전 주기와 궤도 반지름의 관계")
    st.markdown("""
    실제 태양계 행성들의 데이터를 통해 **조화의 법칙($T^2 \propto a^3$)**을 탐구합니다. 
    행성을 클릭하여 해당 데이터가 그래프상의 어느 위치에 있는지 확인해 보세요.
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
                    { name: '수성', r: 0.39, t: 0.24, r3: 0.059, t2: 0.058, color: '#94a3b8' },
                    { name: '금성', r: 0.72, t: 0.62, r3: 0.373, t2: 0.384, color: '#fbbf24' },
                    { name: '지구', r: 1.00, t: 1.00, r3: 1.000, t2: 1.000, color: '#3b82f6' },
                    { name: '화성', r: 1.52, t: 1.88, r3: 3.512, t2: 3.534, color: '#ef4444' },
                    { name: '목성', r: 5.20, t: 11.86, r3: 140.6, t2: 140.7, color: '#f97316' }
                ];

                const currentPlanet = planetData.find(p => p.name === selectedPlanet) || planetData[2];

                return (
                    <div className="max-w-7xl mx-auto p-4 flex flex-col gap-8 animate-in fade-in duration-700 pb-20">
                        {/* Top: Large Chart Section */}
                        <div className="bg-white p-10 rounded-[3rem] border border-slate-200 shadow-2xl space-y-8">
                            <div className="flex justify-between items-center">
                                <h3 className="text-2xl font-black text-slate-800 flex items-center gap-3">
                                    <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-blue-200">
                                        <Icon name="bar-chart-3" size={24} />
                                    </div>
                                    조화의 법칙 데이터 시각화 ($T^2$ vs $r^3$)
                                </h3>
                                <div className="px-6 py-3 bg-slate-900 rounded-2xl text-white flex items-center gap-4 border border-white/10 shadow-xl">
                                    <span className="text-xs font-black text-slate-400 uppercase tracking-widest">실시간 매칭</span>
                                    <span className="text-blue-400 font-black text-lg">{selectedPlanet}</span>
                                </div>
                            </div>

                            <div className="h-[500px] w-full bg-slate-50/50 p-8 rounded-[2.5rem] border border-slate-100 shadow-inner relative overflow-hidden">
                                <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/5 rounded-full blur-[80px]"></div>
                                <ResponsiveContainer width="100%" height="100%">
                                    <ScatterChart margin={{ top: 20, right: 40, bottom: 60, left: 60 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                        <XAxis 
                                            type="number" dataKey="r3" name="r³" domain={[0, 160]} 
                                            stroke="#64748b" tick={{fontSize: 12, fontWeight: 'bold'}}
                                        >
                                            <Label value="궤도 장반경의 세제곱 r³ (AU³)" position="bottom" offset={40} style={{ fontSize: '14px', fontWeight: '900', fill: '#475569' }} />
                                        </XAxis>
                                        <YAxis 
                                            type="number" dataKey="t2" name="T²" domain={[0, 160]} 
                                            stroke="#64748b" tick={{fontSize: 12, fontWeight: 'bold'}}
                                        >
                                            <Label value="공전 주기의 제곱 T² (yr²)" angle={-90} position="left" offset={40} style={{ fontSize: '14px', fontWeight: '900', fill: '#475569' }} />
                                        </YAxis>
                                        <Tooltip 
                                            cursor={{ strokeDasharray: '3 3' }} 
                                            content={({ active, payload }) => {
                                                if (active && payload && payload.length) {
                                                    const data = payload[0].payload;
                                                    return (
                                                        <div className="bg-slate-900 border border-slate-700 text-white p-6 shadow-[0_20px_50px_rgba(0,0,0,0.5)] rounded-3xl animate-in zoom-in-95 backdrop-blur-md">
                                                            <p className="font-black text-blue-400 text-xl mb-3 flex items-center gap-2">
                                                                <span className="w-3 h-3 rounded-full bg-blue-400"></span>{data.name}
                                                            </p>
                                                            <div className="space-y-2 text-sm font-medium border-t border-white/10 pt-3">
                                                                <p className="flex justify-between gap-6"><span className="text-slate-400">r³ (AU³):</span> <span className="font-mono text-white">{data.r3.toFixed(3)}</span></p>
                                                                <p className="flex justify-between gap-6"><span className="text-slate-400">T² (yr²):</span> <span className="font-mono text-white">{data.t2.toFixed(3)}</span></p>
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
                                                    fill={entry.name === selectedPlanet ? '#3b82f6' : '#cbd5e1'} 
                                                    stroke={entry.name === selectedPlanet ? '#3b82f6' : '#94a3b8'}
                                                    strokeWidth={entry.name === selectedPlanet ? 4 : 1}
                                                    r={entry.name === selectedPlanet ? 12 : 6}
                                                    style={{ transition: 'all 0.3s ease' }}
                                                />
                                            ))}
                                        </Scatter>
                                    </ScatterChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Bottom: Table and Details Section */}
                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                            <div className="lg:col-span-2 bg-white p-8 rounded-[2.5rem] border border-slate-200 shadow-xl overflow-hidden">
                                <h3 className="text-xl font-black text-slate-800 mb-6 flex items-center gap-2">
                                    <Icon name="table" className="text-blue-600" /> 수치 데이터 탐색
                                </h3>
                                <div className="overflow-hidden rounded-2xl border border-slate-100 bg-white">
                                    <table className="w-full text-sm text-left border-collapse">
                                        <thead>
                                            <tr className="bg-slate-50 text-slate-500 border-b border-slate-100 uppercase tracking-widest text-[11px] font-black">
                                                <th className="p-5">행성 명칭</th>
                                                <th className="p-5 text-center">장반경 r (AU)</th>
                                                <th className="p-5 text-center">주기 T (yr)</th>
                                                <th className="p-5 text-center text-blue-600">r³ (AU³)</th>
                                                <th className="p-5 text-center text-amber-600">T² (yr²)</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {planetData.map((p) => (
                                                <tr 
                                                    key={p.name} 
                                                    onClick={() => setSelectedPlanet(p.name)}
                                                    className={`planet-row border-b border-slate-50 last:border-0 ${p.name === selectedPlanet ? 'selected-row' : ''}`}
                                                >
                                                    <td className="p-5 font-black text-slate-800 flex items-center gap-3">
                                                        <div className="w-2 h-2 rounded-full" style={{backgroundColor: p.color}}></div>
                                                        {p.name}
                                                    </td>
                                                    <td className="p-5 text-center font-mono text-slate-400">{p.r}</td>
                                                    <td className="p-5 text-center font-mono text-slate-400">{p.t}</td>
                                                    <td className={`p-5 text-center font-mono font-black ${p.name === selectedPlanet ? 'text-blue-600' : 'text-slate-600'}`}>{p.r3.toFixed(3)}</td>
                                                    <td className={`p-5 text-center font-mono font-black ${p.name === selectedPlanet ? 'text-amber-600' : 'text-slate-600'}`}>{p.t2.toFixed(3)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            <div className="bg-slate-900 p-10 rounded-[2.5rem] text-white flex flex-col justify-between shadow-2xl relative overflow-hidden group">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-600/20 rounded-full blur-[60px] group-hover:bg-blue-600/40 transition-all"></div>
                                <div>
                                    <div className="flex items-center gap-2 text-blue-400 mb-6 font-black tracking-widest uppercase text-xs">
                                        <Icon name="search" size={16} /> Planet Detail
                                    </div>
                                    <h4 className="text-4xl font-black mb-2 text-white">{currentPlanet.name}</h4>
                                    <p className="text-slate-400 text-sm font-medium mb-10 leading-relaxed italic pr-4">가장 가까운 태양계 행성 데이터를 통해 물리적 관계식을 검증합니다.</p>
                                    
                                    <div className="space-y-6">
                                        <div className="p-6 bg-white/5 rounded-3xl border border-white/10">
                                            <p className="text-[11px] text-slate-500 font-black uppercase tracking-tighter mb-2">계산된 조화 비례 (T²/r³)</p>
                                            <p className="text-3xl font-mono font-black text-amber-400">{(currentPlanet.t2/currentPlanet.r3).toFixed(5)}</p>
                                        </div>
                                        <div className="flex items-center gap-3 p-4 bg-blue-600/10 rounded-2xl border border-blue-600/20">
                                            <Icon name="check-circle" className="text-blue-400" />
                                            <span className="text-xs font-bold text-slate-300 tracking-tight leading-snug">모든 행성에서 이 값이 약 1.000으로 일정함을 알 수 있습니다.</span>
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
    components.html(react_code, height=1100, scrolling=False)

if __name__ == "__main__":
    run_sim()
