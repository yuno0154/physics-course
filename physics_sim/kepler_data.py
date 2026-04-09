import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 조화의 법칙 데이터 분석", layout="wide")
    
    st.title("📊 케플러 제3법칙: 공전 주기와 궤도 반지름의 관계")
    st.markdown("""
    실제 태양계 행성들의 데이터를 통해 **조화의 법칙($T^2 \propto a^3$)**이 성립함을 수학적으로 확인합니다. 
    행성의 공전 궤도 장반경($a$)의 세제곱과 공전 주기($T$)의 제곱이 그리는 비례 관계를 그래프로 탐구해 보세요.
    """)

    react_code = """
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
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const KeplerData = () => {
                const [engineState, setEngineState] = useState('loading'); // loading, ready, error

                useEffect(() => {
                    let attempts = 0;
                    const checkEngine = setInterval(() => {
                        attempts++;
                        if (window.Recharts) {
                            setEngineState('ready');
                            clearInterval(checkEngine);
                        } else if (attempts > 60) { // 6초 경과 시 에러 처리
                            setEngineState('error');
                            clearInterval(checkEngine);
                        }
                    }, 100);
                    return () => clearInterval(checkEngine);
                }, []);

                if (engineState === 'loading') {
                    return (
                        <div className="flex flex-col items-center justify-center h-80 bg-slate-50 rounded-[32px] border-2 border-dashed border-slate-200">
                            <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
                            <p className="text-slate-400 font-bold tracking-tight">차트 엔진을 준비 중입니다...</p>
                        </div>
                    );
                }

                if (engineState === 'error') {
                    return (
                        <div className="flex flex-col items-center justify-center h-80 bg-red-50 rounded-[32px] border-2 border-dashed border-red-200 p-8">
                             <p className="text-red-800 font-black mb-2">엔진 로드 실패</p>
                             <p className="text-red-500 text-xs mb-4">인터넷 연결을 확인해 주세요.</p>
                             <button onClick={() => window.location.reload()} className="px-4 py-2 bg-red-600 text-white rounded-xl text-[11px] font-bold shadow-lg shadow-red-200">다시 시도</button>
                        </div>
                    );
                }

                const { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } = window.Recharts;

                const planetData = [
                    { name: '수성', r: 0.39, t: 0.24, r3: 0.059, t2: 0.058 },
                    { name: '금성', r: 0.72, t: 0.62, r3: 0.373, t2: 0.384 },
                    { name: '지구', r: 1.00, t: 1.00, r3: 1.000, t2: 1.000 },
                    { name: '화성', r: 1.52, t: 1.88, r3: 3.512, t2: 3.534 },
                    { name: '목성', r: 5.20, t: 11.86, r3: 140.6, t2: 140.7 }
                ];

                return (
                    <div className="max-w-6xl mx-auto p-4 flex flex-col gap-8 animate-in fade-in duration-700">
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                            <div className="bg-white p-8 rounded-[40px] border border-slate-200 shadow-xl space-y-6">
                                <h3 className="text-xl font-black text-slate-800 flex items-center gap-2">
                                    <Icon name="bar-chart-3" className="text-blue-600" /> 데이터 시각화 (T² vs r³)
                                </h3>
                                <div className="h-80 w-full bg-slate-50 p-6 rounded-3xl border border-slate-100">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <ScatterChart margin={{ top: 20, right: 30, bottom: 40, left: 40 }}>
                                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                            <XAxis 
                                                type="number" 
                                                dataKey="r3" 
                                                name="r³" 
                                                label={{ value: 'r³ (AU³)', position: 'insideBottom', offset: -25, fontSize: 12, fontWeight: 'bold' }} 
                                            />
                                            <YAxis 
                                                type="number" 
                                                dataKey="t2" 
                                                name="T²" 
                                                label={{ value: 'T² (yr²)', angle: -90, position: 'insideLeft', offset: -15, fontSize: 12, fontWeight: 'bold' }} 
                                            />
                                            <Tooltip cursor={{ strokeDasharray: '3 3' }} content={({ payload }) => {
                                                if (payload && payload[0]) {
                                                    const data = payload[0].payload;
                                                    return (
                                                        <div className="bg-slate-900 border border-slate-700 text-white p-5 shadow-2xl rounded-2xl">
                                                            <p className="font-black text-blue-400 text-base mb-2">{data.name}</p>
                                                            <div className="text-[12px] text-slate-400 space-y-1">
                                                                <p className="flex justify-between gap-4"><span>r³:</span> <span className="text-white font-mono">{data.r3.toFixed(3)} AU³</span></p>
                                                                <p className="flex justify-between gap-4"><span>T²:</span> <span className="text-white font-mono">{data.t2.toFixed(3)} yr²</span></p>
                                                            </div>
                                                        </div>
                                                    );
                                                }
                                                return null;
                                            }} />
                                            <Scatter name="Planets" data={planetData}>
                                                {planetData.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={index === 2 ? '#ef4444' : '#3b82f6'} stroke="white" strokeWidth={2} />
                                                ))}
                                            </Scatter>
                                        </ScatterChart>
                                    </ResponsiveContainer>
                                </div>
                                <div className="p-5 bg-blue-50/50 rounded-2xl border-l-4 border-blue-500">
                                    <h4 className="font-bold text-slate-800 mb-2 underline underline-offset-4 flex items-center gap-2">
                                        <Icon name="lightbulb" size={16} /> 탐구 포인트
                                    </h4>
                                    <p className="text-[13px] text-slate-600 leading-relaxed font-medium">
                                        모든 데이터가 기울기가 1인 직선상에 위치합니다. 이는 <span className="text-blue-600 font-bold">$T^2$</span>과 <span className="text-blue-600 font-bold">$r^3$</span>이 완벽한 정비례 관계임을 시사합니다.
                                    </p>
                                </div>
                            </div>

                            <div className="bg-white p-8 rounded-[40px] border border-slate-200 shadow-xl">
                                <h3 className="text-xl font-black text-slate-800 mb-6 flex items-center gap-2">
                                    <Icon name="table" className="text-amber-600" /> 수치 데이터 분석
                                </h3>
                                <div className="overflow-hidden rounded-2xl border border-slate-100 mb-6 bg-white shadow-inner">
                                    <table className="w-full text-[13px] text-left border-collapse">
                                        <thead>
                                            <tr className="bg-slate-50 text-slate-500 border-b border-slate-100 uppercase tracking-tighter">
                                                <th className="p-4 font-black">행성</th>
                                                <th className="p-4 font-black">r (AU)</th>
                                                <th className="p-4 font-black">T (yr)</th>
                                                <th className="p-4 font-black text-blue-600">r³ (AU³)</th>
                                                <th className="p-4 font-black text-amber-600">T² (yr²)</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {planetData.map((p) => (
                                                <tr key={p.name} className="hover:bg-slate-50 transition-colors border-b border-slate-50 last:border-0">
                                                    <td className="p-4 font-bold text-slate-800">{p.name}</td>
                                                    <td className="p-4 font-mono text-slate-500">{p.r}</td>
                                                    <td className="p-4 font-mono text-slate-500">{p.t}</td>
                                                    <td className="p-4 font-mono bg-blue-50/20 font-black text-blue-700">{p.r3.toFixed(3)}</td>
                                                    <td className="p-4 font-mono bg-amber-50/20 font-black text-amber-700">{p.t2.toFixed(3)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                                <div className="bg-slate-900 p-8 rounded-3xl text-white relative">
                                    <div className="absolute top-0 right-0 p-6 opacity-10">
                                        <Icon name="calculator" size={60} />
                                    </div>
                                    <div className="flex items-center gap-2 text-amber-400 mb-4 text-xs font-black uppercase tracking-widest">
                                        <Icon name="calculator" size={16} /> 이론적 배경
                                    </div>
                                    <div className="font-mono text-xl p-5 bg-white/5 rounded-2xl border border-white/10 text-center mb-6 text-white tracking-widest">
                                        T² = K × r³
                                    </div>
                                    <p className="text-[12px] text-slate-400 leading-relaxed font-medium italic">
                                        이 비례상수 K는 $4\pi^2/GM$으로 정의되며, 태양계 내 모든 행성에서 동일한 값을 가집니다.
                                    </p>
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
    components.html(react_code, height=900, scrolling=False)

if __name__ == "__main__":
    run_sim()
