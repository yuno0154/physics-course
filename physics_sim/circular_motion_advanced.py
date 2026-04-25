import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="?깆 ??대 ?ы ?援?, layout="wide")
    
    st.title("? [???媛 1-3] ?깆 ??대 ?ы ?援?(Advanced Study)")
    st.markdown("""
    ???裕щ?댁? ?깆 ??대? ?湲 媛???**?쇰?? ?    react_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
            body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; background: transparent; overflow: hidden; }
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

            const CircularMotionAdvanced = () => {
                const [mode, setMode] = useState(1);
                const [isPaused, setIsPaused] = useState(false);
                const [isCut, setIsCut] = useState(false);
                const [activeTab, setActiveTab] = useState('settings');
                const [radius, setRadius] = useState(120);
                const [theta, setTheta] = useState(1.0);
                const [omega, setOmega] = useState(1.5);
                const [angle, setAngle] = useState(0);
                const [elapsedTimeAfterCut, setElapsedTimeAfterCut] = useState(0);
                const [cutState, setCutState] = useState({ pos: { x: 0, y: 0 }, vel: { x: 0, y: 0 } });
                const [savedVectors, setSavedVectors] = useState([]);
                
                const requestRef = useRef();
                const lastTimeRef = useRef();

                const animate = (time) => {
                    if (lastTimeRef.current !== undefined && !isPaused) {
                        const deltaTime = (time - lastTimeRef.current) / 1000;
                        if (!isCut) {
                            setAngle((prev) => (prev + (mode === 1 ? 0 : omega) * deltaTime) % (Math.PI * 2));
                        } else {
                            setElapsedTimeAfterCut((prev) => prev + deltaTime);
                        }
                    }
                    lastTimeRef.current = time;
                    requestRef.current = requestAnimationFrame(animate);
                };

                useEffect(() => {
                    requestRef.current = requestAnimationFrame(animate);
                    return () => cancelAnimationFrame(requestRef.current);
                }, [isPaused, isCut, mode, omega]);

                const handleReset = () => {
                    setIsCut(false); setAngle(0); setElapsedTimeAfterCut(0); setSavedVectors([]); setIsPaused(false);
                };

                const handleCut = () => {
                    const x = radius * Math.cos(angle); const y = radius * Math.sin(angle);
                    const v = radius * omega; const vx = -v * Math.sin(angle); const vy = v * Math.cos(angle);
                    setCutState({ pos: { x, y }, vel: { x: vx, y: vy } });
                    setIsCut(true);
                };

                const saveVector = () => {
                    if (savedVectors.length >= 2) setSavedVectors([]);
                    const v = radius * omega;
                    setSavedVectors(prev => [...prev, {
                        pos: { x: radius * Math.cos(angle), y: radius * Math.sin(angle) },
                        vel: { x: -v * Math.sin(angle), y: v * Math.cos(angle) }
                    }]);
                };

                const CX = 250; const CY = 250;

                return (
                    <div className="flex flex-col bg-white min-h-screen p-4 text-slate-800">
                      <div className="w-full max-w-6xl mx-auto bg-white rounded-[2rem] shadow-2xl border border-slate-200 overflow-hidden flex flex-col">
                        <div className="flex bg-slate-100 p-2 gap-2 border-b border-slate-200">
                          {[{id:1,label:'?쇰? ??',icon:'layers'},{id:2,label:'v = r? ?援?,icon:'zap'},{id:3,label:'媛?? 利紐',icon:'scissors'}].map(m=>(
                            <button key={m.id} onClick={()=>{setMode(m.id);handleReset();}} className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-bold transition-all ${mode===m.id?'bg-white shadow text-blue-600':'text-slate-400 hover:bg-slate-200'}`}>
                              <Icon name={m.icon} size={16}/> {m.label}
                            </button>
                          ))}
                        </div>
                        <div className="flex flex-col lg:flex-row h-[520px]">
                          <div className="flex-1 bg-white relative overflow-hidden flex items-center justify-center border-r border-slate-100">
                            <div className="absolute top-4 left-4 bg-white/80 p-3 rounded-2xl border border-slate-100 text-[10px] space-y-1 shadow-sm z-10">
                              <div className="flex items-center gap-2 font-bold"><div className="w-2 h-2 bg-emerald-500 rounded-full"></div><span>?? (Green)</span></div>
                              <div className="flex items-center gap-2 font-bold"><div className="w-2 h-2 bg-rose-500 rounded-full"></div><span>媛?? (Red)</span></div>
                            </div>
                            <svg viewBox="0 0 500 500" className="w-full h-full max-w-[500px]">
                              <circle cx={CX} cy={CY} r="2" fill="#94a3b8" />
                              <line x1="0" y1={CY} x2="500" y2={CY} stroke="#f1f5f9" strokeWidth="1" />
                              <line x1={CX} y1="0" x2={CX} y2="500" stroke="#f1f5f9" strokeWidth="1" />
                              {mode===1 && (
                                <g>
                                  <circle cx={CX} cy={CY} r={radius} fill="none" stroke="#334155" strokeWidth="2.5" strokeDasharray="4,4" />
                                  <path d={`M ${CX} ${CY} L ${CX + radius} ${CY} A ${radius} ${radius} 0 ${theta > Math.PI ? 1 : 0} 1 ${CX + radius * Math.cos(theta)} ${CY + radius * Math.sin(theta)} Z`} fill="rgba(59,130, 246, 0.1)" stroke="#3b82f6" strokeWidth="2" />
                                  <path d={`M ${CX + radius} ${CY} A ${radius} ${radius} 0 ${theta > Math.PI ? 1 : 0} 1 ${CX + radius * Math.cos(theta)} ${CY + radius * Math.sin(theta)}`} fill="none" stroke="#ef4444" strokeWidth="5" strokeLinecap="round" />
                                </g>
                              )}
                              {mode===2 && (
                                <g>
                                  {[radius, radius*0.6].map((r,i)=>(
                                    <g key={i}>
                                      <circle cx={CX} cy={CY} r={r} fill="none" stroke="#334155" strokeWidth="2.5" strokeDasharray="4,4" />
                                      <line x1={CX} y1={CY} x2={CX+r*Math.cos(angle)} y2={CY+r*Math.sin(angle)} stroke="#94a3b8" strokeWidth="2" />
                                      <line x1={CX+r*Math.cos(angle)} y1={CY+r*Math.sin(angle)} x2={CX+r*Math.cos(angle)-(r*omega*0.5)*Math.sin(angle)} y2={CY+r*Math.sin(angle)+(r*omega*0.5)*Math.cos(angle)} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                      <circle cx={CX+r*Math.cos(angle)} cy={CY+r*Math.sin(angle)} r="8" fill={i===0?"#1e293b":"#64748b"} />
                                    </g>
                                  ))}
                                </g>
                              )}
                              {mode===3 && (
                                <g>
                                  <circle cx={CX} cy={CY} r={radius} fill="none" stroke="#334155" strokeWidth="2.5" strokeDasharray="4,4" />
                                  {!isCut ? (
                                    <g>
                                      <line x1={CX} y1={CY} x2={CX+radius*Math.cos(angle)} y2={CY+radius*Math.sin(angle)} stroke="#94a3b8" strokeWidth="2" />
                                      <line x1={CX+radius*Math.cos(angle)} y1={CY+radius*Math.sin(angle)} x2={CX+radius*Math.cos(angle)-(radius*omega*0.5)*Math.sin(angle)} y2={CY+radius*Math.sin(angle)+(radius*omega*0.5)*Math.cos(angle)} stroke="#10b981" strokeWidth="3" markerEnd="url(#arrow-green)" />
                                      <line x1={CX+radius*Math.cos(angle)} y1={CY+radius*Math.sin(angle)} x2={CX+radius*Math.cos(angle)+radius*omega*0.3*-Math.cos(angle)} y2={CY+radius*Math.sin(angle)+radius*omega*0.3*-Math.sin(angle)} stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrow-red)" />
                                      <circle cx={CX+radius*Math.cos(angle)} cy={CY+radius*Math.sin(angle)} r="10" fill="#0f172a" />
                                    </g>
                                  ):(
                                    <circle cx={CX+cutState.pos.x+cutState.vel.x*elapsedTimeAfterCut} cy={CY+cutState.pos.y+cutState.vel.y*elapsedTimeAfterCut} r="10" fill="#64748b" />
                                  )}
                                </g>
                              )}
                              <defs>
                                <marker id="arrow-green" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#10b981"/></marker>
                                <marker id="arrow-red" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L0,8 L9,4 Z" fill="#ef4444"/></marker>
                              </defs>
                            </svg>
                          </div>
                          <div className="w-full lg:w-80 bg-slate-50 flex flex-col border-l border-slate-100 p-6 space-y-6">
                            <div className="flex border-b border-slate-200">
                                <button onClick={()=>setActiveTab('settings')} className={`flex-1 py-3 font-bold text-xs ${activeTab==='settings'?'text-blue-600 border-b-2 border-blue-600':'text-slate-400'}`}>?ㅼ</button>
                                <button onClick={()=>setActiveTab('activity')} className={`flex-1 py-3 font-bold text-xs ${activeTab==='activity'?'text-emerald-600 border-b-2 border-emerald-600':'text-slate-400'}`}>??吏</button>
                            </div>
                            {activeTab==='settings' ? (
                              <div className="space-y-4">
                                <div className="text-xs font-bold text-slate-400">Radius: {radius}px</div>
                                <input type="range" min="50" max="200" value={radius} onChange={e=>setRadius(parseInt(e.target.value))} className="w-full accent-blue-600" />
                                <div className="grid grid-cols-2 gap-2">
                                  <button onClick={()=>setIsPaused(!isPaused)} className="py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold">{isPaused?'?ш?':'?吏'}</button>
                                  <button onClick={handleReset} className="py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold">由ъ</button>
                                </div>
                                {mode===3 && <button onClick={handleCut} className="w-full py-2 bg-rose-500 text-white rounded-xl text-xs font-bold">???湲?(愿??</button>}
                              </div>
                            ) : (
                              <div className="space-y-4 text-xs leading-relaxed">
                                <div className="p-3 bg-white border border-slate-200 rounded-xl">
                                  <strong>Mission:</strong> ??吏? ?몄? 吏臾?Retrieval)? 梨?곕ŉ ?援ы?몄.
                                </div>
                                <div className="p-3 bg-slate-800 text-white rounded-xl">
                                   怨≪ ?濡 ?ㅺ? ? F = mv짼/r 怨듭? ?대산? ??⑺댁????源??
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                );
            };
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<CircularMotionAdvanced />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=720, scrolling=False)
      </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<CircularMotionAdvanced />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=720, scrolling=False)

if __name__ == "__main__":
    run_sim()
