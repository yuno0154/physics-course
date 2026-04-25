import streamlit as st
import streamlit.components.v1 as components
import base64, os

st.sidebar.title("?뙌 釉붾옓? ?먭뎄")
st.sidebar.markdown("?덉텧?띾룄媛 鍮쏆쓽 ?띾룄瑜??섎뒗 泥쒖껜瑜??먭뎄?⑸땲??")

# 釉붾옓? 援ъ“ ?대?吏 (bh_structure.png ?곗꽑, ?놁쑝硫?blackhole.png ?ъ슜)
_assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_struct_path = os.path.join(_assets, "bh_structure.png")
_fallback_path = os.path.join(_assets, "blackhole.png")
_img_path = _struct_path if os.path.exists(_struct_path) else _fallback_path
_img_b64 = ""
if os.path.exists(_img_path):
    with open(_img_path, "rb") as _f:
        _img_b64 = base64.b64encode(_f.read()).decode("utf-8")
    _img_mime = "image/png"

REACT_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#070c18;color:#e2e8f0;padding:16px;}
.tab-bar{display:flex;gap:6px;margin-bottom:20px;flex-wrap:wrap;}
.tab-btn{padding:9px 18px;border-radius:10px;border:1px solid #1e293b;background:#0d1526;
  color:#64748b;cursor:pointer;font-size:13px;font-weight:700;font-family:inherit;transition:all 0.2s;}
.tab-btn.active{background:#7c3aed;border-color:#8b5cf6;color:#fff;}
.tab-btn:hover:not(.active){border-color:#334155;color:#e2e8f0;}
.card{background:#0d1526;border:1px solid #1e293b;border-radius:14px;padding:20px;margin-bottom:16px;}
.hl-box{background:linear-gradient(135deg,#1a0a2e,#2e1060);border:1px solid #7c3aed;border-radius:12px;padding:16px;margin-bottom:14px;}
.result-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #1e293b;font-size:13px;}
.result-row:last-child{border-bottom:none;}
.val{color:#a78bfa;font-family:'Space Mono',monospace;font-weight:700;}
.preset-btn{padding:6px 14px;background:#1e293b;border:1px solid #334155;border-radius:8px;
  color:#94a3b8;cursor:pointer;font-size:12px;font-family:inherit;transition:all 0.2s;font-weight:600;}
.preset-btn:hover,.preset-btn.sel{border-color:#8b5cf6;color:#e2e8f0;background:#2d1060;}
input[type=range]{-webkit-appearance:none;width:100%;height:5px;background:#1e293b;border-radius:3px;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;
  background:#8b5cf6;cursor:pointer;box-shadow:0 0 8px rgba(139,92,246,0.6);}
.qa-btn{width:100%;display:flex;align-items:flex-start;gap:12px;padding:14px 18px;
  background:transparent;border:none;cursor:pointer;text-align:left;font-family:inherit;}
.step-btn{width:100%;display:flex;align-items:center;gap:12px;padding:14px 18px;
  background:#0d1526;border:none;cursor:pointer;text-align:left;font-family:inherit;border-radius:12px;}
.detect-card{border-radius:14px;border:1px solid #1e293b;padding:18px;
  background:#0d1526;transition:border-color 0.2s;}
.detect-card:hover{border-color:#7c3aed;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

const G_REAL = 6.674e-11;
const C_LIGHT = 3e8; // m/s

const calcRs = (M) => 2 * G_REAL * M / (C_LIGHT * C_LIGHT); // Schwarzschild radius (m)

const PRESETS_BH = [
  { name:'吏援?,    M:5.972e24,  R_real:6.371e6,   emoji:'?뙇', color:'#3b82f6' },
  { name:'?쒖뼇',    M:1.989e30,  R_real:6.960e8,   emoji:'?截?, color:'#fbbf24' },
  { name:'諛깆깋?쒖꽦',M:1.989e30*1.4, R_real:7e6,   emoji:'??, color:'#e2e8f0' },
  { name:'以묒꽦?먮퀎',M:1.989e30*2.0, R_real:12000,  emoji:'?뮟', color:'#60a5fa' },
  { name:'M87* BH', M:6.5e9*1.989e30, R_real:0,   emoji:'?뙌', color:'#a78bfa' },
];

/* ?? KaTeX ?섏떇 ?뚮뜑留??? */
const Eq = ({ f, display=false, color='#c4b5fd' }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && window.katex)
      window.katex.render(f, ref.current, { throwOnError:false, displayMode:display });
  }, [f, display]);
  return <span ref={ref} style={{ color }} />;
};

/* ??????????????????????????????????????????????
   ??1: 釉붾옓??대?? (媛쒕뀗 + ?덈컮瑜댁툩?ㅽ듃 ?좊룄)
?????????????????????????????????????????????? */
const CONCEPT_STEPS = [
  { n:1, title:'?덉텧?띾룄 怨듭떇 異쒕컻', color:'#3b82f6', bg:'#0d1f3c',
    formula:'v_{\\text{?덉텧}} = \\sqrt{\\dfrac{2GM}{R}}',
    note:'??븰???먮꼫吏 蹂댁〈?쇰줈 ?좊룄???덉텧?띾룄 怨듭떇?낅땲??' },
  { n:2, title:'?덉텧?띾룄 = 鍮쏆쓽 ?띾룄 議곌굔 ?ㅼ젙', color:'#8b5cf6', bg:'#1a0d3c',
    formula:'c = \\sqrt{\\dfrac{2GM}{R_s}}',
    note:'?덉텧?띾룄媛 鍮쏆쓽 ?띾룄(c)? 媛숈븘吏??諛섏?由?Rs瑜?援ы빀?덈떎.' },
  { n:3, title:'Rs????* ??????????????????????????????????????????????
   3D ?쒓났媛?援ъ“ ?쒕??덉씠??(Three.js 湲곕컲)
?????????????????????????????????????????????? */
function Spacetime3D() {
  const mountRef = useRef(null);

  useEffect(() => {
    if (!window.THREE) return;
    const { THREE } = window;
    
    // 1. Scene Setup
    const W = 820, H = 550;
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x04060d);
    const camera = new THREE.PerspectiveCamera(45, W / H, 0.1, 2000);
    camera.position.set(0, 180, 420);
    camera.lookAt(0, -60, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(W, H);
    renderer.setPixelRatio(window.devicePixelRatio);
    mountRef.current.appendChild(renderer.domElement);

    // 2. Flamm's Paraboloid (?쒓났媛?怨〓㈃)
    // ?섑븰???뺥깭: w(r) = 2 * sqrt(Rs * (r - Rs))
    const Rs = 40;
    const segments = 64;
    const rMax = 320;
    
    const geometry = new THREE.ParametricGeometry((u, v, target) => {
        const theta = v * Math.PI * 2;
        const r = Rs + u * (rMax - Rs);
        const x = r * Math.cos(theta);
        const z = r * Math.sin(theta);
        const y = -2 * Math.sqrt(Rs * Math.max(0, r - Rs));
        target.set(x, y, z);
    }, segments, segments);

    const material = new THREE.MeshBasicMaterial({
        color: 0x4c1d95,
        wireframe: true,
        transparent: true,
        opacity: 0.35,
        side: THREE.DoubleSide
    });
    const paraboloid = new THREE.Mesh(geometry, material);
    scene.add(paraboloid);

    // 3. ?ш굔 吏?됱꽑 (Event Horizon) - 寃? 援ъ껜
    const ehGeo = new THREE.SphereGeometry(Rs - 0.5, 32, 32);
    const ehMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
    const ehMesh = new THREE.Mesh(ehGeo, ehMat);
    ehMesh.position.y = -1; // 怨〓㈃ ?곷떒???댁쭩 嫄몄묠
    scene.add(ehMesh);

    // ?ш굔 吏?됱꽑 ?꾧킅 (Glow)
    const ehGlowGeo = new THREE.SphereGeometry(Rs + 2, 32, 32);
    const ehGlowMat = new THREE.ShaderMaterial({
        transparent: true,
        uniforms: {
            c: { type: "f", value: 0.1 },
            p: { type: "f", value: 4.5 },
            glowColor: { type: "c", value: new THREE.Color(0x8b5cf6) },
            viewVector: { type: "v3", value: camera.position }
        },
        vertexShader: `
            uniform vec3 viewVector;
            varying float intensity;
            void main() {
                gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
                vec3 actualNormal = vec3(modelMatrix * vec4(normal, 0.0));
                intensity = pow( dot(normalize(viewVector), normalize(actualNormal)), 6.0 );
            }
        `,
        fragmentShader: `
            uniform vec3 glowColor;
            varying float intensity;
            void main() {
                gl_FragColor = vec4( glowColor, intensity );
            }
        `,
        side: THREE.BackSide
    });
    const ehGlow = new THREE.Mesh(ehGlowGeo, ehGlowMat);
    scene.add(ehGlow);

    // 4. 媛뺤갑 ?먮컲 (Accretion Disk) - ?낆옄?뺥깭
    const particleCount = 1200;
    const particlesGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const orbitRadius = [];

    for (let i = 0; i < particleCount; i++) {
        const r = Rs * 2 + Math.random() * Rs * 4;
        const angle = Math.random() * Math.PI * 2;
        positions[i*3] = r * Math.cos(angle);
        positions[i*3+1] = -2 * Math.sqrt(Rs * Math.max(0, r - Rs)) + (Math.random() - 0.5) * 5;
        positions[i*3+2] = r * Math.sin(angle);
        
        orbitRadius.push(r);
        
        const mix = Math.random();
        colors[i*3] = 1.0;
        colors[i*3+1] = 0.4 + mix * 0.4;
        colors[i*3+2] = 0.1;
    }
    particlesGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particlesGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    const particlesMat = new THREE.PointsMaterial({ size: 2.2, vertexColors: true, transparent: true, opacity: 0.8 });
    const accretionDisk = new THREE.Points(particlesGeo, particlesMat);
    scene.add(accretionDisk);

    // 5. 二쇱슂 沅ㅻ룄 留?(愿묒옄援? ISCO)
    const createRing = (r, color, dash = false) => {
        const ringGeo = new THREE.RingGeometry(r, r + 1, 64);
        const ringMat = new THREE.MeshBasicMaterial({ color: color, side: THREE.DoubleSide, transparent: true, opacity: 0.6 });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.rotation.x = Math.PI / 2;
        ring.position.y = -2 * Math.sqrt(Rs * Math.max(0, r - Rs));
        return ring;
    };
    const photonSphere = createRing(Rs * 1.5, 0xfbbf24);
    const isco = createRing(Rs * 3, 0x22c55e);
    scene.add(photonSphere);
    scene.add(isco);

    // 6. Animation
    let frame = 0;
    const animate = () => {
        frame = requestAnimationFrame(animate);
        const time = Date.now() * 0.001;
        
        // ?먮컲 ?뚯쟾 (?덉そ?쇱닔濡?鍮좊Ⅴ寃?- 耳?뚮윭? ?좎궗?섍쾶 ?쒓컖??
        const pos = accretionDisk.geometry.attributes.position.array;
        for (let i = 0; i < particleCount; i++) {
            const r = orbitRadius[i];
            const speed = 0.5 * Math.pow(Rs/r, 1.5);
            const angle = time * speed + i;
            pos[i*3] = r * Math.cos(angle);
            pos[i*3+2] = r * Math.sin(angle);
        }
        accretionDisk.geometry.attributes.position.needsUpdate = true;
        
        // 移대찓??遺?쒕윭???뚯쟾
        camera.position.x = 420 * Math.sin(time * 0.15);
        camera.position.z = 420 * Math.cos(time * 0.15);
        camera.lookAt(0, -80, 0);
        
        renderer.render(scene, camera);
    };
    animate();

    return () => {
        cancelAnimationFrame(frame);
        mountRef.current.removeChild(renderer.domElement);
    };
  }, []);

  return (
    <div style={{marginBottom:16}}>
      <div style={{background:'linear-gradient(135deg,#08031a,#120830)',borderRadius:'14px 14px 0 0',
        padding:'13px 20px',border:'1px solid #4c1d95',borderBottom:'none',
        display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          <p style={{color:'#c4b5fd',fontWeight:800,fontSize:14}}>
            ?첃 釉붾옓? 3D ?쒓났媛?援ъ“ (3D Spacetime View)
          </p>
          <p style={{color:'#6d28d9',fontSize:12,marginTop:3}}>
            ?쒓났媛꾩쓽 3李⑥썝??怨〓쪧(Flamm's Paraboloid)怨?媛뺤갑?먮컲??紐⑥뒿???쒕??덉씠?섑빀?덈떎.
          </p>
        </div>
        <div style={{display:'flex',flexDirection:'column',gap:5,fontSize:11,flexShrink:0,marginLeft:20}}>
            <div style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:'#a78bfa',fontWeight:700}}>??/span>
              <span style={{color:'#64748b'}}>?ш굔 吏?됱꽑</span>
            </div>
            <div style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:'#fbbf24',fontWeight:700}}>??</span>
              <span style={{color:'#64748b'}}>愿묒옄 援?(r=1.5R??</span>
            </div>
            <div style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:'#22c55e',fontWeight:700}}>??</span>
              <span style={{color:'#64748b'}}>ISCO (r=3R??</span>
            </div>
        </div>
      </div>
      <div ref={mountRef} style={{width:'100%',height:'550px',borderRadius:'0 0 14px 14px',
          background:'#04060d',display:'block',border:'1px solid #4c1d95',borderTop:'none', overflow:'hidden'}}/>
    </div>
  );
}
_Y - 12);

      ctx.restore();

      animRef.current = requestAnimationFrame(loop);
    };

    animRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animRef.current);
  }, []);

  return (
    <div style={{marginBottom:16}}>
      <div style={{background:'linear-gradient(135deg,#08031a,#120830)',borderRadius:'14px 14px 0 0',
        padding:'13px 20px',border:'1px solid #4c1d95',borderBottom:'none',
        display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          <p style={{color:'#c4b5fd',fontWeight:800,fontSize:14}}>
            ?? 釉붾옓? 二쇰? ?쒓났媛?援ъ“ ???뚮엺 ?뚮씪蹂쇰줈?대뱶 (Flamm's Paraboloid)
          </p>
          <p style={{color:'#6d28d9',fontSize:12,marginTop:3}}>
            ?쒓났媛꾩쓽 怨듦컙??怨〓쪧???⑤㈃(Cross-section)?쇰줈 ?쒗쁽?⑸땲?? 源딆씠???쒓났媛?怨〓쪧???멸린瑜??섑??낅땲??
          </p>
        </div>
        <div style={{display:'flex',flexDirection:'column',gap:5,fontSize:11,flexShrink:0,marginLeft:20}}>
          {[
            ['??','rgba(167,139,250,0.85)','?ш굔 吏?됱꽑 (EH)'],
            ['?뚢븣','rgba(251,191,36,0.8)','愿묒옄 援?(r=1.5R??'],
            ['??','rgba(34,197,94,0.8)','ISCO (r=3R??'],
            ['??,'#fbbf24','?뱀씠??],
            ['??,'rgba(253,224,71,0.9)','援댁젅?섎뒗 鍮?],
          ].map(([sym,col,lbl],i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:col,fontFamily:'monospace',fontWeight:700,minWidth:22,fontSize:13}}>{sym}</span>
              <span style={{color:'#64748b'}}>{lbl}</span>
            </div>
          ))}
        </div>
      </div>
      <canvas ref={ref} width={820} height={500}
        style={{width:'100%',height:'500px',borderRadius:'0 0 14px 14px',
          background:'#04060d',display:'block',border:'1px solid #4c1d95',borderTop:'none'}}/>
    </div>
  );
}

function ConceptTab() {
  const [open, setOpen] = useState(null);
  const [animT, setAnimT] = useState(0);
  const canvasRef = useRef(null);
  const animRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current; if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let t = 0;
    const loop = () => {
      t += 0.015;
      const W = canvas.width, H = canvas.height;
      ctx.fillStyle = '#05070a'; ctx.fillRect(0,0,W,H);

      // 蹂?
      for (let i=0;i<80;i++){
        const sx=(i*137.5)%W, sy=(i*97+i*11)%H;
        ctx.beginPath(); ctx.arc(sx,sy,0.4+(i%3)*0.3,0,Math.PI*2);
        ctx.fillStyle=`rgba(210,225,255,${0.1+(i%5)*0.06})`; ctx.fill();
      }

      const CX=W*0.5, CY=H*0.5;
      const BH_R=55;

      // 媛뺤갑 ?먮컲 (Accretion Disk)
      for (let layer=0; layer<3; layer++){
        const rx = BH_R*(2.0+layer*0.7);
        const ry = rx*0.22;
        const col = ['rgba(255,100,20,', 'rgba(255,160,40,', 'rgba(255,200,80,'][layer];
        const alpha = [0.55, 0.35, 0.2][layer];
        ctx.save();
        ctx.translate(CX, CY);
        ctx.beginPath(); ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI*2);
        const grad = ctx.createRadialGradient(0,0,BH_R,0,0,rx);
        grad.addColorStop(0, col+alpha+')');
        grad.addColorStop(1, col+'0)');
        ctx.fillStyle = grad; ctx.fill();
        ctx.restore();
      }

      // ?쒗듃 (Relativistic Jets)
      [[-1,1],[1,-1]].forEach(([sign, dir])=>{
        const jetLen = 100;
        const spread = 14;
        const jetGrad = ctx.createLinearGradient(CX, CY, CX, CY+sign*jetLen);
        jetGrad.addColorStop(0, 'rgba(139,92,246,0.8)');
        jetGrad.addColorStop(1, 'rgba(139,92,246,0)');
        ctx.beginPath();
        ctx.moveTo(CX-spread*0.3, CY+sign*BH_R*0.8);
        ctx.lineTo(CX-spread, CY+sign*(BH_R+jetLen));
        ctx.lineTo(CX+spread, CY+sign*(BH_R+jetLen));
        ctx.lineTo(CX+spread*0.3, CY+sign*BH_R*0.8);
        ctx.fillStyle = jetGrad; ctx.fill();
      });

      // 釉붾옓? 蹂몄껜
      const bhGrad = ctx.createRadialGradient(CX-10,CY-10,5,CX,CY,BH_R);
      bhGrad.addColorStop(0,'#1a0a30'); bhGrad.addColorStop(0.5,'#08040f'); bhGrad.addColorStop(1,'#000');
      ctx.beginPath(); ctx.arc(CX,CY,BH_R,0,Math.PI*2); ctx.fillStyle=bhGrad; ctx.fill();

      // ?ш굔 吏?됱꽑 湲濡쒖슦
      const ehGrad = ctx.createRadialGradient(CX,CY,BH_R,CX,CY,BH_R+20);
      ehGrad.addColorStop(0,'rgba(139,92,246,0.6)'); ehGrad.addColorStop(1,'rgba(139,92,246,0)');
      ctx.beginPath(); ctx.arc(CX,CY,BH_R+20,0,Math.PI*2); ctx.fillStyle=ehGrad; ctx.fill();
      ctx.beginPath(); ctx.arc(CX,CY,BH_R,0,Math.PI*2);
      ctx.strokeStyle='rgba(139,92,246,0.9)'; ctx.lineWidth=2; ctx.stroke();

      // 鍮쏆쓽 ?섏꽑 (?ы쉷?섎뒗 愿묒옄)
      const photons = [0, 1.2, 2.4, 3.8, 5.0];
      photons.forEach((ph, pi) => {
        const angle = t * 1.8 + ph;
        const decayFac = Math.min(1, (t % (Math.PI*2)) / (Math.PI*2));
        const r = BH_R * 2.8 - (t * 6 + pi * 25) % (BH_R * 1.8);
        if (r < BH_R) return;
        const px2 = CX + r * Math.cos(angle);
        const py2 = CY + r * Math.sin(angle) * 0.4;
        ctx.beginPath(); ctx.arc(px2,py2,2.5,0,Math.PI*2);
        ctx.fillStyle=`rgba(253,224,71,0.85)`; ctx.fill();
        ctx.beginPath(); ctx.arc(px2,py2,5,0,Math.PI*2);
        ctx.strokeStyle='rgba(253,224,71,0.2)'; ctx.lineWidth=1; ctx.stroke();
      });

      // ?쇰꺼
      ctx.fillStyle='rgba(167,139,250,0.9)'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText('?ш굔 吏?됱꽑', CX, CY-BH_R-12);
      ctx.fillStyle='rgba(252,211,77,0.7)'; ctx.font='11px Noto Sans KR';
      ctx.fillText('媛뺤갑 ?먮컲', CX+BH_R*2.2, CY+BH_R*0.2);
      ctx.fillStyle='rgba(139,92,246,0.7)';
      ctx.fillText('?곷?濡좎쟻 ?쒗듃', CX+35, CY-BH_R-45);

      ctx.textAlign='left';
      animRef.current = requestAnimationFrame(loop);
    };
    animRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animRef.current);
  }, []);

  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>?뙌 ?듭떖 吏덈Ц</p>
        <p style={{color:'#cbd5e1',fontSize:14,lineHeight:1.8}}>
          ?덉텧?띾룄 怨듭떇 <Eq f="v_{\text{?덉텧}}=\sqrt{2GM/R}"/> ?먯꽌,
          留뚯빟 泥쒖껜??諛섏?由꾩쓣 異⑸텇???묎쾶 留뚮뱾??<strong style={{color:'#a78bfa'}}>?덉텧?띾룄 = 鍮쏆쓽 ?띾룄(c)</strong>媛 ?섎㈃ ?대뼸寃??좉퉴?
          鍮쏆“李??덉텧?섏? 紐삵븯????泥쒖껜瑜?<strong style={{color:'#c4b5fd'}}>釉붾옓?</strong>?대씪 ?쒕떎.
        </p>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginBottom:16}}>
        <canvas ref={canvasRef} width={480} height={300}
          style={{width:'100%',height:'300px',borderRadius:'12px',background:'#05070a'}}/>
        <div style={{display:'flex',flexDirection:'column',gap:12}}>
          <div className="card" style={{flex:1}}>
            <p style={{color:'#a78bfa',fontWeight:700,fontSize:14,marginBottom:10}}>?뱦 釉붾옓????듭떖 ?뱀꽦</p>
            {[
              ['?ш굔 吏?됱꽑','鍮쏅룄 ?덉텧 遺덇??ν븳 寃쎄퀎硫? 諛섏?由?= ?덈컮瑜댁툩?ㅽ듃 諛섏?由?Rs'],
              ['?뱀씠??,'以묒떖遺. 諛?꾧? 臾댄븳?濡?諛쒖궛?섎뒗 ?? ?꾩옱 臾쇰━?숈쓽 ?쒓퀎'],
              ['媛뺤갑 ?먮컲','釉붾옓?濡?鍮⑤젮?쒕뒗 臾쇱쭏???대（???④굅???먮컲. X??諛⑹텧'],
              ['?곷?濡좎쟻 ?쒗듃','釉붾옓????먭린?μ뿉 ?섑빐 ?섏쭅 諛⑺뼢?쇰줈 肉쒖뼱吏??臾쇱쭏'],
            ].map(([t,d],i)=>(
              <div key={i} style={{borderBottom:'1px solid #1e293b',padding:'8px 0',display:'flex',gap:10}}>
                <span style={{color:'#8b5cf6',fontWeight:800,fontSize:12,flexShrink:0,paddingTop:2}}>??/span>
                <div>
                  <p style={{color:'#e2e8f0',fontSize:13,fontWeight:700}}>{t}</p>
                  <p style={{color:'#64748b',fontSize:12,lineHeight:1.6,marginTop:2}}>{d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card" style={{marginBottom:16}}>
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>?뱪 ?덈컮瑜댁툩?ㅽ듃 諛섏?由??좊룄</p>
        <div style={{display:'flex',flexDirection:'column',gap:10}}>
          {CONCEPT_STEPS.map((s,i)=>(
            <div key={i} style={{border:`1px solid ${open===i?s.color+'90':'#1e293b'}`,borderRadius:14,overflow:'hidden',transition:'border-color 0.25s'}}>
              <button className="step-btn" onClick={()=>setOpen(open===i?null:i)}>
                <div style={{width:32,height:32,borderRadius:'50%',background:s.color,display:'flex',
                  alignItems:'center',justifyContent:'center',color:'#fff',fontWeight:800,fontSize:14,flexShrink:0}}>{s.n}</div>
                <div style={{flex:1}}>
                  <p style={{color:'#e2e8f0',fontSize:14,fontWeight:700}}>{s.title}</p>
                </div>
                <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',
                  transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>??/span>
              </button>
              <div style={{maxHeight:open===i?'250px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
                <div style={{padding:'18px 24px',background:s.bg,display:'flex',flexDirection:'column',gap:12}}>
                  <div style={{background:'rgba(0,0,0,0.3)',borderRadius:12,padding:'16px 24px',
                    display:'flex',justifyContent:'center',border:`1px solid ${s.color}30`}}>
                    <Eq f={s.formula} display={true} color={s.color}/>
                  </div>
                  <div style={{display:'flex',gap:10,alignItems:'flex-start'}}>
                    <span style={{fontSize:15,flexShrink:0}}>?뮕</span>
                    <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.75}}>{s.note}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ?? 釉붾옓? 援ъ“ ?대?吏 + ?ㅻ챸 ?? */}
      <SpacetimeCanvas/>

      <div className="card" style={{marginBottom:16}}>
        <p style={{fontWeight:800,color:'#e2e8f0',fontSize:15,marginBottom:14}}>
          ?뼹截?釉붾옓???援ъ“ ???⑤㈃??
        </p>
        <div style={{display:'grid',gridTemplateColumns:'220px 1fr',gap:20,alignItems:'flex-start'}}>
          {/* ?대?吏 */}
          <div style={{borderRadius:12,overflow:'hidden',border:'1px solid #3b1e7c',
            background:'#000',display:'flex',alignItems:'center',justifyContent:'center'}}>
            {"__BH_IMG_B64__" !== "" ? (
              <img src={"data:image/png;base64,__BH_IMG_B64__"}
                style={{width:'100%',display:'block',borderRadius:11}}
                alt="釉붾옓? 援ъ“ ?⑤㈃??/>
            ) : (
              <div style={{padding:24,color:'#475569',fontSize:12,textAlign:'center'}}>
                ?대?吏瑜?assets/bh_structure.png濡???ν빐 二쇱꽭??
              </div>
            )}
          </div>
          {/* 援ъ“ ?ㅻ챸 */}
          <div style={{display:'flex',flexDirection:'column',gap:10}}>
            <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.8,marginBottom:6}}>
              釉붾옓????섏쭅?쇰줈 ?섎씪 蹂??⑤㈃?꾩엯?덈떎. ?쒓났媛꾩쓽 怨〓쪧???ы븷?섎줉 "源딆씠"媛 源딆뼱吏묐땲??
            </p>
            {[
              ['#a78bfa','?ш굔 吏?됱꽑 (Event Horizon)',
                `諛섏?由?R??= 2GM/c짼??援щ㈃. ??寃쎄퀎 ?덉そ?먯꽌???덉텧?띾룄 > c ?대?濡?鍮쏅룄 ?덉텧 遺덇?. ?몃? 愿痢≪옄????寃쎄퀎 ?덈㉧瑜?蹂????놁뒿?덈떎.`],
              ['#fbbf24','?뱀씠??(Singularity)',
                `釉붾옓???以묒떖. 諛?????? 遺????0. ?꾩옱 臾쇰━???쇰컲 ?곷????대줎)???곸슜?섏? ?딅뒗 吏?먯쑝濡? ?묒옄 以묐젰 ?대줎???꾩슂?⑸땲??`],
              ['rgba(251,191,36,0.8)','愿묒옄 援?(Photon Sphere)',
                `r = 1.5 R?쏆씤 援щ㈃. 鍮쏆씠 ?먰삎 沅ㅻ룄瑜?洹몃┫ ???덈뒗 寃쎄퀎?댁?留? 遺덉븞?뺥빀?덈떎. ?쎄컙??援먮?留??덉뼱??鍮쏆? ?덉텧?섍굅???ы쉷?⑸땲??`],
              ['rgba(34,197,94,0.8)','ISCO (理쒕궡媛??덉젙 ?먰삎 沅ㅻ룄)',
                `r = 3 R?? 臾쇱쭏???덉젙?곸쑝濡???沅ㅻ룄瑜??좎??????덈뒗 媛???덉そ 寃쎄퀎. ?대낫???덉そ??臾쇱쭏? 鍮좊Ⅴ寃?釉붾옓?濡??섏꽑?뺤쑝濡??⑥뼱吏묐땲??`],
            ].map(([col,title,desc],i)=>(
              <div key={i} style={{display:'flex',gap:10,padding:'8px 0',
                borderBottom:'1px solid #1e293b'}}>
                <div style={{width:4,flexShrink:0,borderRadius:2,background:col,marginTop:3,alignSelf:'stretch'}}/>
                <div>
                  <p style={{color:col,fontWeight:700,fontSize:13,marginBottom:3}}>{title}</p>
                  <p style={{color:'#64748b',fontSize:12,lineHeight:1.7}}>{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{background:'linear-gradient(135deg,#2e0a4e,#1a0030)',borderRadius:16,padding:'20px 28px',border:'1px solid #8b5cf6'}}>
        <p style={{color:'#c4b5fd',fontWeight:800,fontSize:15,marginBottom:8}}>??寃곕줎</p>
        <p style={{color:'#ddd6fe',fontSize:13,lineHeight:1.85}}>
          ?덈컮瑜댁툩?ㅽ듃 諛섏?由?<Eq f="R_s = \dfrac{2GM}{c^2}"/> ?덉そ?먯꽌???덉텧?띾룄媛 鍮쏆쓽 ?띾룄瑜?珥덇낵?섎?濡?
          ?대뼡 臾쇱껜?? ?ъ???鍮쏆“李⑤룄 ?덉텧?????놁뒿?덈떎.<br/>
          <strong style={{color:'#a78bfa'}}>釉붾옓????섎뒗 議곌굔</strong>: 泥쒖껜??諛섏?由???Rs = 2GM/c짼<br/>
          吏援ш? 釉붾옓????섎젮硫?諛섏?由꾩쓣 ??<strong style={{color:'#fbbf24'}}>9 mm</strong>濡??뺤텞?댁빞 ?⑸땲??
        </p>
      </div>
    </div>
  );
}

/* ??????????????????????????????????????????????
   ??2: ?덈컮瑜댁툩?ㅽ듃 諛섏?由?怨꾩궛湲?
?????????????????????????????????????????????? */
function SchwarzschildTab() {
  const [sel, setSel]    = useState(0);
  const [massScale, setMassScale] = useState(1); // solar mass multiplier
  const [isCustom, setIsCustom]   = useState(false);
  const canvasRef = useRef(null);

  const preset = PRESETS_BH[sel];
  const M_use  = isCustom ? massScale * 1.989e30 : preset.M;
  const Rs = calcRs(M_use);
  const R_real = isCustom ? preset.R_real : preset.R_real;
  const isBH_now = !isCustom && (R_real === 0 || R_real < Rs);

  // ?쒓컖?? 諛섏?由?鍮꾧탳 ?ㅼ씠?닿렇??
  useEffect(() => {
    const canvas = canvasRef.current; if(!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.fillStyle='#05070a'; ctx.fillRect(0,0,W,H);

    // 蹂?
    for (let i=0;i<60;i++){
      const sx=(i*137)%W, sy=(i*97)%H;
      ctx.beginPath(); ctx.arc(sx,sy,0.4+(i%3)*0.25,0,Math.PI*2);
      ctx.fillStyle=`rgba(200,220,255,${0.08+(i%5)*0.05})`; ctx.fill();
    }

    const M = M_use;
    const Rs_v = Rs;
    const R_v = R_real;

    // 以묒븰 ?꾩튂
    const CX = W*0.5, CY = H*0.5;

    // 諛섏?由??ㅼ???怨꾩궛 (?쒓컖??
    const maxR = Math.max(Rs_v, R_v);
    const scale = Math.min(H*0.35, W*0.35) / Math.max(maxR, 1);
    const Rs_px = Math.max(Math.min(Rs_v * scale, 120), 8);
    const R_px  = R_v > 0 ? Math.max(Math.min(R_v * scale, 120), 8) : 0;

    // ?덈컮瑜댁툩?ㅽ듃 諛섏?由?(?ш굔 吏?됱꽑)
    const ehGrad = ctx.createRadialGradient(CX,CY,0,CX,CY,Rs_px);
    ehGrad.addColorStop(0,'#000'); ehGrad.addColorStop(0.7,'#0d0518'); ehGrad.addColorStop(1,'#1a0030');
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px,0,Math.PI*2); ctx.fillStyle=ehGrad; ctx.fill();
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px,0,Math.PI*2);
    ctx.strokeStyle='rgba(139,92,246,0.9)'; ctx.lineWidth=2.5; ctx.stroke();

    // 湲濡쒖슦
    const gGrad = ctx.createRadialGradient(CX,CY,Rs_px,CX,CY,Rs_px+20);
    gGrad.addColorStop(0,'rgba(139,92,246,0.4)'); gGrad.addColorStop(1,'rgba(139,92,246,0)');
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px+20,0,Math.PI*2); ctx.fillStyle=gGrad; ctx.fill();

    // ?ㅼ젣 泥쒖껜 諛섏?由?(?덈뒗 寃쎌슦)
    if (R_v > 0) {
      const bodyGrad = ctx.createRadialGradient(CX-R_px*0.2,CY-R_px*0.2,R_px*0.1,CX,CY,R_px);
      const col = preset.color;
      bodyGrad.addColorStop(0, col+'ff'); bodyGrad.addColorStop(1, col+'66');
      ctx.save(); ctx.globalAlpha=0.5;
      ctx.beginPath(); ctx.arc(CX,CY,R_px,0,Math.PI*2);
      ctx.fillStyle = bodyGrad; ctx.fill();
      ctx.restore();
      ctx.beginPath(); ctx.arc(CX,CY,R_px,0,Math.PI*2);
      ctx.strokeStyle=col+'99'; ctx.lineWidth=1.5; ctx.stroke();
    }

    // ?쇰꺼 - Rs
    ctx.fillStyle='#a78bfa'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
    ctx.fillText('?ш굔 吏?됱꽑 (Rs)', CX, CY - Rs_px - 12);

    const fmtR = (r) => {
      if (r >= 1e9) return (r/1e9).toFixed(2) + ' Gm';
      if (r >= 1e6) return (r/1e6).toFixed(2) + ' Mm';
      if (r >= 1e3) return (r/1e3).toFixed(2) + ' km';
      if (r >= 1)   return r.toFixed(2) + ' m';
      return (r*1000).toFixed(2) + ' mm';
    };

    ctx.fillStyle='#ddd6fe'; ctx.font='11px Space Mono'; ctx.textAlign='center';
    ctx.fillText(fmtR(Rs_v), CX, CY - Rs_px - 28);

    if (R_v > 0) {
      ctx.fillStyle='rgba(200,200,255,0.7)'; ctx.font='bold 11px Noto Sans KR';
      ctx.fillText('?ㅼ젣 諛섏?由?, CX + R_px + 15, CY);
      ctx.fillStyle='rgba(200,200,255,0.55)'; ctx.font='10px Space Mono';
      ctx.fillText(fmtR(R_v), CX + R_px + 15, CY + 15);
    }

    // 鍮꾧탳 ?쒖떆
    if (R_v > 0) {
      const ratio = R_v / Rs_v;
      ctx.fillStyle='rgba(148,163,184,0.8)'; ctx.font='11px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText(`?ㅼ젣 諛섏?由?= Rs 횞 ${ratio.toExponential(2)}`, CX, H-14);
    }

    ctx.textAlign='left';
  }, [sel, massScale, isCustom]);

  const fmtNum = (r) => {
    if (r >= 1e12) return (r/1e12).toFixed(3) + ' Tm (?뚮씪誘명꽣)';
    if (r >= 1e9)  return (r/1e9).toFixed(3) + ' Gm (湲곌?誘명꽣)';
    if (r >= 1e6)  return (r/1e6).toFixed(3) + ' Mm ??' + (r/1e3).toFixed(0) + ' km';
    if (r >= 1e3)  return (r/1e3).toFixed(3) + ' km';
    if (r >= 1)    return r.toFixed(4) + ' m';
    return (r*1000).toFixed(4) + ' mm';
  };

  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>?뵯 ?덈컮瑜댁툩?ㅽ듃 諛섏?由?怨꾩궛湲?/p>
        <p style={{color:'#cbd5e1',fontSize:14}}>
          怨듭떇: <Eq f="R_s = \dfrac{2GM}{c^2}"/> &nbsp;
          吏援?Rs ??8.9 mm | ?쒖뼇 Rs ??3.0 km
        </p>
      </div>

      <div style={{display:'flex',gap:8,flexWrap:'wrap',marginBottom:16}}>
        {PRESETS_BH.map((p,i)=>(
          <button key={i} className={`preset-btn ${!isCustom&&sel===i?'sel':''}`}
            onClick={()=>{ setSel(i); setIsCustom(false); }}>
            {p.emoji} {p.name}
          </button>
        ))}
        <button className={`preset-btn ${isCustom?'sel':''}`} onClick={()=>setIsCustom(true)}>
          ?륅툘 ?쒖뼇吏덈웾 諛곗닔
        </button>
      </div>

      {isCustom && (
        <div className="card" style={{marginBottom:14}}>
          <label>?쒖뼇 吏덈웾??諛곗닔: {massScale.toLocaleString('ko-KR')} M??/label>
          <input type="range" min={0.1} max={1e10} step={0.1}
            value={massScale} onChange={e=>setMassScale(parseFloat(e.target.value))}/>
          <p style={{textAlign:'center',fontSize:12,color:'#64748b',marginTop:6}}>
            M = {M_use.toExponential(3)} kg
          </p>
        </div>
      )}

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginBottom:16}}>
        <canvas ref={canvasRef} width={440} height={280}
          style={{width:'100%',height:'280px',borderRadius:'12px',background:'#05070a'}}/>

        <div style={{display:'flex',flexDirection:'column',gap:12}}>
          <div className="card">
            <p style={{color:'#64748b',fontSize:12,marginBottom:10,fontWeight:700}}>怨꾩궛 寃곌낵</p>
            <div className="result-row">
              <span style={{color:'#94a3b8'}}>吏덈웾 (M)</span>
              <span className="val">{M_use.toExponential(3)} kg</span>
            </div>
            <div className="result-row">
              <span style={{color:'#94a3b8'}}>?덈컮瑜댁툩?ㅽ듃 諛섏?由?(Rs)</span>
              <span className="val">{fmtNum(Rs)}</span>
            </div>
            {!isCustom && PRESETS_BH[sel].R_real > 0 && (
              <div className="result-row">
                <span style={{color:'#94a3b8'}}>?ㅼ젣 諛섏?由?/span>
                <span className="val" style={{color:'#60a5fa'}}>{fmtNum(PRESETS_BH[sel].R_real)}</span>
              </div>
            )}
            {!isCustom && PRESETS_BH[sel].R_real > 0 && (
              <div className="result-row">
                <span style={{color:'#94a3b8'}}>?ㅼ젣 / Rs 鍮꾩쑉</span>
                <span className="val" style={{color: isBH_now?'#ef4444':'#22c55e'}}>
                  {(PRESETS_BH[sel].R_real / Rs).toExponential(2)}
                </span>
              </div>
            )}
          </div>

          <div className={`card`} style={{
            background: isBH_now ? 'linear-gradient(135deg,#1a0030,#2e0050)' : 'linear-gradient(135deg,#0a1f0a,#0f300f)',
            borderColor: isBH_now ? '#8b5cf6' : '#22c55e'
          }}>
            <p style={{color: isBH_now?'#c4b5fd':'#4ade80', fontWeight:800, fontSize:16, marginBottom:8}}>
              {isBH_now ? '?뙌 釉붾옓? ?곹깭' : '???쇰컲 泥쒖껜 ?곹깭'}
            </p>
            <p style={{color: isBH_now?'#ddd6fe':'#86efac', fontSize:13, lineHeight:1.75}}>
              {isBH_now
                ? '?ㅼ젣 諛섏?由꾩씠 ?덈컮瑜댁툩?ㅽ듃 諛섏?由꾨낫???묎굅??媛숈뒿?덈떎. ??泥쒖껜??釉붾옓??낅땲?? ?ш굔 吏?됱꽑 ?대?濡??ㅼ뼱媛?臾쇱껜???덉텧 遺덇??ν빀?덈떎.'
                : `?ㅼ젣 諛섏?由꾩씠 Rs蹂대떎 ${(PRESETS_BH[sel].R_real/Rs).toExponential(2)}諛??쎈땲?? 釉붾옓????섎젮硫???泥쒖껜瑜?${fmtNum(Rs)}源뚯? ?뺤텞?댁빞 ?⑸땲??`}
            </p>
          </div>
        </div>
      </div>

      <div className="card">
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>二쇱슂 泥쒖껜???덈컮瑜댁툩?ㅽ듃 諛섏?由?鍮꾧탳</p>
        <div style={{overflowX:'auto'}}>
          <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
            <thead>
              <tr style={{borderBottom:'1px solid #1e293b'}}>
                {['泥쒖껜','吏덈웾','?ㅼ젣 諛섏?由?,'?덈컮瑜댁툩?ㅽ듃 諛섏?由?Rs','?곹깭'].map(h=>(
                  <th key={h} style={{padding:'10px 12px',color:'#64748b',fontWeight:700,textAlign:'left'}}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                ['?뙇 吏援?,  '5.97횞10짼??kg', '6,371 km', '8.9 mm',   false],
                ['?截??쒖뼇',  '1.99횞10쨀??kg', '696,000 km','3.0 km',  false],
                ['??諛깆깋?쒖꽦','1.4 M??,       '~7,000 km', '4.1 km',  false],
                ['?뮟 以묒꽦?먮퀎','2.0 M??,       '~12 km',    '5.9 km',  true ],
                ['?뙌 M87*',  '6.5횞10??M??,  '??,         '~192 AU', true ],
              ].map(([nm,m,r,rs,isBH],i)=>(
                <tr key={i} style={{borderBottom:'1px solid #0f172a',background:isBH?'rgba(139,92,246,0.08)':undefined}}>
                  <td style={{padding:'10px 12px',fontWeight:700,color:'#e2e8f0'}}>{nm}</td>
                  <td style={{padding:'10px 12px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:12}}>{m}</td>
                  <td style={{padding:'10px 12px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:12}}>{r}</td>
                  <td style={{padding:'10px 12px',color:'#a78bfa',fontWeight:800,fontFamily:'Space Mono'}}>{rs}</td>
                  <td style={{padding:'10px 12px'}}>
                    <span style={{
                      padding:'3px 10px',borderRadius:20,fontSize:11,fontWeight:700,
                      background: isBH?'rgba(139,92,246,0.2)':'rgba(34,197,94,0.15)',
                      color: isBH?'#c4b5fd':'#4ade80',
                      border: `1px solid ${isBH?'#8b5cf6':'#22c55e'}`
                    }}>
                      {isBH ? '釉붾옓?' : '?쇰컲 泥쒖껜'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ??????????????????????????????????????????????
   ??3: 釉붾옓? ?먯? 諛⑸쾿
?????????????????????????????????????????????? */
const DETECT_METHODS = [
  {
    icon:'?뙜截?, title:'X???띿꽦怨?(X-ray Binaries)',
    color:'#ef4444',
    summary:'釉붾옓????숇컲?깆쓽 臾쇱쭏??媛뺤갑 ?먮컲?쇰줈 ?≪닔????諛⑹텧?섎뒗 X?좎쓣 愿痢?,
    how:'?숇컲 蹂꾩뿉???섎윭?섏삩 媛?ㅺ? 釉붾옓? 二쇰? 媛뺤갑 ?먮컲???뺤꽦?섎ŉ ?섎갚留뚢꼦濡?媛?대릺??媛뺥븳 X?좎쓣 諛⑹텧?⑸땲??',
    example:'諛깆“?먮━ X-1 (1964??理쒖큹 諛쒓껄), 沅ㅻ룄 ?대룞?쇰줈 釉붾옓? 吏덈웾 異붿젙 媛??,
    evidence:'蹂댁씠吏 ?딅뒗 ?숇컲泥?+ X??+ 沅ㅻ룄 ?대룞 = 釉붾옓?'
  },
  {
    icon:'?뙄', title:'以묐젰??(Gravitational Waves)',
    color:'#3b82f6',
    summary:'??釉붾옓????⑸퀝?????쒓났媛꾩쓽 ?뚮룞??LIGO/Virgo 媛꾩꽠怨꾨줈 寃異?,
    how:'??釉붾옓????섏꽑?대룞?섎ŉ ?⑹퀜吏????꾩껌???먮꼫吏媛 以묐젰?뚮줈 諛⑹텧?⑸땲?? ???뚮룞??吏援щ? ?듦낵?섎㈃ 怨듦컙???섏냼 ?먯옄 ?ш린??1/1000留뚰겮 ?좎텞?⑸땲??',
    example:'GW150914 (2015??: 36M??+ 29M????62M??釉붾옓?. 3M?됱뿉 ?대떦?섎뒗 ?먮꼫吏媛 以묐젰?뚮줈 諛⑹텧.',
    evidence:'以묐젰???뚰삎 遺꾩꽍?쇰줈 蹂묓빀 ?꾪썑 吏덈웾 ?뺥솗 怨꾩궛 媛??
  },
  {
    icon:'?뵯', title:'以묐젰 ?뚯쫰 (Gravitational Lensing)',
    color:'#8b5cf6',
    summary:'釉붾옓???媛뺥븳 以묐젰??諛곌꼍 蹂꾨튆???섍쾶 留뚮뱶???꾩긽 愿痢?,
    how:'釉붾옓???諛곌꼍 蹂꾧낵 吏援??ъ씠瑜??듦낵???? 蹂꾨튆??釉붾옓? 以묐젰???섑빐 ?섏뼱 諛앷린媛 利앷??⑸땲??誘몄떆 以묐젰 ?뚯쫰). 珥덈?吏덈웾 釉붾옓?? ?섏씠???곸쓣 ?щ윭 媛쒕줈 遺꾨━?쒗궢?덈떎.',
    example:'?덈툝 留앹썝寃쎌쓽 ?꾩씤?덊???留?愿痢? M87* ?ш굔 吏?됱꽑 留앹썝寃?EHT) 珥ъ쁺',
    evidence:'?꾩씤?덊?????옄媛, 留????뱀쑀??愿묓븰 ?꾩긽'
  },
  {
    icon:'狩?, title:'蹂꾩쓽 沅ㅻ룄 ?대룞 (Stellar Orbits)',
    color:'#fbbf24',
    summary:'珥덈?吏덈웾 釉붾옓? 二쇰? 蹂꾨뱾??沅ㅻ룄瑜??섏떗 ?꾧컙 異붿쟻?섏뿬 釉붾옓? 吏덈웾怨??꾩튂 寃곗젙',
    how:'?곕━ ???以묒떖(沅곸닔?먮━ A*) 二쇰? S2蹂꾩쓣 16?꾧컙 異붿쟻??寃곌낵, 蹂댁씠吏 ?딅뒗 吏덈웾???쒖뼇??400留?諛곗엫???뺤씤. ?닿쾬??釉붾옓???寃곗젙??利앷굅.',
    example:'S2蹂? 16.0??二쇨린, 洹쇱젒?먯뿉??鍮쏆쓽 2.87%???띾룄. 2020???몃꺼 臾쇰━?숈긽.',
    evidence:'耳?뚮윭 踰뺤튃?쇰줈 以묒떖 吏덈웾 怨꾩궛 ??釉붾옓? ?뺤씤'
  },
  {
    icon:'?뱻', title:'?ш굔 吏?됱꽑 留앹썝寃?(Event Horizon Telescope)',
    color:'#10b981',
    summary:'??吏援?洹쒕え???꾪뙆留앹썝寃??ㅽ듃?뚰겕濡?釉붾옓? 洹몃┝?먮? 吏곸젒 珥ъ쁺',
    how:'吏援??ш린??媛??留앹썝寃?VLBI 湲곗닠)?쇰줈 M87 ???以묒떖??珥덈?吏덈웾 釉붾옓???珥ъ쁺. 釉붾옓? 洹몃┝??shadow)? 媛뺤갑 ?먮컲??怨좊━ 援ъ“瑜??뺤씤.',
    example:'2019??M87* 釉붾옓? 理쒖큹 吏곸젒 珥ъ쁺 (吏덈웾: ?쒖뼇??65?듬같). 2022???곕━ ???以묒떖 沅곸닔?먮━ A* 珥ъ쁺.',
    evidence:'鍮?怨좊━(Photon Ring)? 以묒븰???대몢??洹몃┝??= ?ш굔 吏?됱꽑??吏곸젒 利앷굅'
  },
];

function DetectTab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:18}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>?뱻 釉붾옓???諛쒓껄?섎뒗 諛⑸쾿</p>
        <p style={{color:'#cbd5e1',fontSize:14,lineHeight:1.8}}>
          釉붾옓?? 鍮쏆쓣 諛⑹텧?섏? ?딆쑝誘濡?<strong style={{color:'#a78bfa'}}>媛꾩젒?곸씤 諛⑸쾿</strong>?쇰줈留??먯??⑸땲??
          二쇰? 臾쇱쭏怨쇱쓽 ?곹샇?묒슜, 以묐젰 ?④낵, ?쒓났媛??쒓끝??利앷굅媛 ?⑸땲??
        </p>
      </div>

      <div style={{display:'flex',flexDirection:'column',gap:12}}>
        {DETECT_METHODS.map((m,i)=>(
          <div key={i} className="detect-card"
            style={{borderColor:open===i?m.color+'80':'#1e293b',transition:'border-color 0.2s'}}>
            <div style={{display:'flex',gap:14,alignItems:'flex-start',cursor:'pointer'}}
              onClick={()=>setOpen(open===i?null:i)}>
              <div style={{width:46,height:46,borderRadius:12,background:`${m.color}22`,
                border:`1px solid ${m.color}44`,display:'flex',alignItems:'center',justifyContent:'center',
                fontSize:22,flexShrink:0}}>
                {m.icon}
              </div>
              <div style={{flex:1}}>
                <p style={{color:m.color,fontWeight:800,fontSize:15}}>{m.title}</p>
                <p style={{color:'#94a3b8',fontSize:13,marginTop:4,lineHeight:1.6}}>{m.summary}</p>
              </div>
              <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',marginTop:4,
                transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>??/span>
            </div>
            <div style={{maxHeight:open===i?'400px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
              <div style={{marginTop:14,paddingTop:14,borderTop:'1px solid #1e293b',display:'flex',flexDirection:'column',gap:10}}>
                <div style={{display:'flex',gap:10}}>
                  <span style={{color:m.color,fontWeight:800,fontSize:12,flexShrink:0,paddingTop:2}}>?먮━</span>
                  <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.75}}>{m.how}</p>
                </div>
                <div style={{display:'flex',gap:10}}>
                  <span style={{color:'#fbbf24',fontWeight:800,fontSize:12,flexShrink:0,paddingTop:2}}>?щ?</span>
                  <p style={{color:'#fcd34d',fontSize:13,lineHeight:1.75}}>{m.example}</p>
                </div>
                <div style={{display:'flex',gap:10,background:`${m.color}11`,padding:'10px 14px',borderRadius:10,border:`1px solid ${m.color}33`}}>
                  <span style={{fontSize:14,flexShrink:0}}>?뵎</span>
                  <p style={{color:m.color,fontSize:13,lineHeight:1.7,fontWeight:600}}>{m.evidence}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card" style={{marginTop:16,background:'linear-gradient(135deg,#0c1a0c,#0a2a0a)',borderColor:'#22c55e'}}>
        <p style={{color:'#4ade80',fontWeight:800,fontSize:14,marginBottom:10}}>?뮕 怨듯넻 ?먮━</p>
        <p style={{color:'#86efac',fontSize:13,lineHeight:1.85}}>
          紐⑤뱺 ?먯? 諛⑸쾿? <strong>釉붾옓? 二쇰???臾쇰━???④낵</strong>瑜?愿痢≫빀?덈떎.
          釉붾옓? ?먯껜??蹂댁씠吏 ?딆?留? ?댄꽩??以묐젰 踰뺤튃怨??쇰컲 ?곷????대줎?쇰줈 ?덉륫???꾩긽?ㅼ씠
          ?뺥솗??愿痢〓릺??釉붾옓???議댁옱瑜?利앸챸?⑸땲??
          2020???몃꺼 臾쇰━?숈긽? ?곕━ ???以묒떖 釉붾옓? ?곌뎄???섏뿬?섏뿀?듬땲??
        </p>
      </div>
    </div>
  );
}

/* ??????????????????????????????????????????????
   ??4: ?먭뎄 吏덈Ц
?????????????????????????????????????????????? */
const QA_BH = [
  { q:'釉붾옓?? "紐⑤뱺 寃껋쓣 鍮⑥븘?ㅼ씤????留먯씠 留욎쓣源?',
    a:'諛섏? 留욊퀬 諛섏? ?由쎈땲?? ?ш굔 吏?됱꽑 ?대??먯꽌???덉텧??遺덇??ν븯吏留? ?ш굔 吏?됱꽑 諛붽묑?먯꽌??釉붾옓???媛숈? 吏덈웾??蹂꾧낵 ?숈씪?섍쾶 以묐젰???묒슜?⑸땲?? ?쒖뼇??媛숈? 吏덈웾??釉붾옓?濡?諛붾뚯뼱??吏援?沅ㅻ룄??蹂?섏? ?딆뒿?덈떎. 釉붾옓?? "媛源뚯씠 媛硫??꾪뿕?섏?留? 硫由ъ꽌???됰쾾??以묐젰泥댁엯?덈떎.' },
  { q:'?쒖뼇??釉붾옓????????덉쓣源?',
    a:'?꾨떃?덈떎. 釉붾옓????섎젮硫?珥덉떊????컻???꾩슂?섍퀬, ?대? ?꾪빐?쒕뒗 ?쒖뼇 吏덈웾????8諛??댁긽???꾩슂?⑸땲?? ?쒖뼇? ??50???????곸깋 嫄곗꽦??嫄곗퀜 諛깆깋 ?쒖꽦?쇰줈 ?앹쓣 留덇컧?⑸땲?? ?쒖뼇??釉붾옓?濡?留뚮뱾?ㅻ㈃ 諛섏?由꾩쓣 ??3 km濡??뺤텞?댁빞 ?섎뒗?? ?먯뿰?곸씤 怨쇱젙?쇰줈??遺덇??ν빀?덈떎.' },
  { q:'釉붾옓??먯꽌 ?섏삤???뺣낫???놁쓣源? (?명궧 蹂듭궗)',
    a:'?ㅽ떚釉??명궧? 1974???묒옄 ??븰 ?④낵濡?釉붾옓????대났?щ? 諛⑹텧?쒕떎怨??덉륫?덉뒿?덈떎(?명궧 蹂듭궗). 釉붾옓? 二쇰??먯꽌 媛???낆옄-諛섏엯???띿씠 ?앹꽦???? ???낆옄媛 ?ш굔 吏?됱꽑 ?덉쑝濡??ㅼ뼱媛怨??ㅻⅨ ?낆옄媛 ?덉텧?섎㈃ 釉붾옓?? 吏덈웾???껋뒿?덈떎. 留ㅼ슦 ?묒? 釉붾옓?? 鍮좊Ⅴ寃?利앸컻?????덉?留? 嫄곕? 釉붾옓????명궧 ?⑤룄???곗＜ 諛곌꼍 蹂듭궗蹂대떎????븘 ?꾩떎?곸쑝濡?痢≪젙??遺덇??ν빀?덈떎.' },
  { q:'釉붾옓? ?대????ㅼ뼱媛硫??대뼸寃??좉퉴?',
    a:'硫由ъ꽌 蹂대㈃: ?쒓컙 ?쎌갹(以묐젰 ?곸깋 ?몄씠) ?뚮Ц??吏꾩엯?먭? ?ш굔 吏?됱꽑???곸썝???묎렐?섎뒗 寃껋쿂??蹂댁씠硫??먯젏 ?먮┸?댁쭛?덈떎. 吏꾩엯???낆옣: 吏덈웾???ъ? ?딆? 釉붾옓??대씪硫??ш굔 吏?됱꽑???듦낵?????밸퀎??蹂?붾? ?먮겮吏 紐삵븷 ???덉뒿?덈떎. ?섏?留??뱀씠?먯뿉 媛源뚯썙吏덉닔濡?議곗꽍??tidal force)??洹밸떒?곸쑝濡?而ㅼ졇 "?ㅽ뙆寃뚰떚??spaghettification)"?⑸땲?? ?뱀씠?먯뿉?쒕뒗 ?꾩옱??臾쇰━ 踰뺤튃???곸슜?섏? ?딆뒿?덈떎.' },
  { q:'?곕━ ???以묒떖?먮룄 釉붾옓????덉쓣源?',
    a:'?? 沅곸닔?먮━ A*(Sgr A*)?쇰뒗 珥덈?吏덈웾 釉붾옓????덉쑝硫? 吏덈웾? ?쒖뼇????400留?諛곗엯?덈떎. 吏援ъ뿉????26,000愿묐뀈 ?⑥뼱???덉뒿?덈떎. 2022???ш굔 吏?됱꽑 留앹썝寃?EHT)??Sgr A*???대?吏瑜?吏곸젒 珥ъ쁺?덉쑝硫? 2020???몃꺼 臾쇰━?숈긽? S2蹂?沅ㅻ룄 異붿쟻???듯븳 Sgr A* ?곌뎄???섏뿬?섏뿀?듬땲??' },
];

function QATab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:18}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:4}}>???먭뎄 吏덈Ц</p>
        <p style={{color:'#94a3b8',fontSize:13}}>吏덈Ц???대┃?섏뿬 ?듬????뺤씤?섏꽭?? 癒쇱? ?ㅼ뒪濡??앷컖??蹂댁꽭??</p>
      </div>
      <div style={{display:'flex',flexDirection:'column',gap:10}}>
        {QA_BH.map((item,i)=>(
          <div key={i} style={{borderRadius:13,border:`1px solid ${open===i?'#8b5cf6':'#1e293b'}`,
            overflow:'hidden',background:'#070b14',transition:'border-color 0.2s'}}>
            <button className="qa-btn" onClick={()=>setOpen(open===i?null:i)}>
              <span style={{color:'#8b5cf6',fontWeight:800,fontSize:15,flexShrink:0,marginTop:1}}>Q{i+1}.</span>
              <span style={{color:'#cbd5e1',fontSize:14,lineHeight:1.65,flex:1}}>{item.q}</span>
              <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',
                transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>??/span>
            </button>
            <div style={{maxHeight:open===i?'350px':'0px',overflow:'hidden',transition:'max-height 0.35s ease'}}>
              <div style={{padding:'0 18px 14px 46px',display:'flex',gap:10}}>
                <span style={{color:'#10b981',fontWeight:800,fontSize:13,flexShrink:0,marginTop:1}}>A.</span>
                <span style={{color:'#6ee7b7',fontSize:13,lineHeight:1.85}}>{item.a}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card" style={{marginTop:16,background:'linear-gradient(135deg,#0f172a,#1a1040)',borderColor:'#8b5cf6'}}>
        <p style={{color:'#c4b5fd',fontWeight:800,marginBottom:10}}>?뙆 ?곌껐 媛쒕뀗</p>
        <p style={{color:'#a78bfa',fontSize:13,lineHeight:1.9}}>
          釉붾옓? ?먭뎄???댄꽩??以묐젰 踰뺤튃 ???덉텧?띾룄 ???덈컮瑜댁툩?ㅽ듃 諛섏?由????꾩씤?덊??몄쓽 ?쇰컲 ?곷????대줎?쇰줈 ?댁뼱吏??媛쒕뀗???곌껐?낅땲??
          怨좎쟾 ??븰?쇰줈 ?덉륫??"鍮쏅룄 ?덉텧 紐삵븯??泥쒖껜"媛 ?ㅼ젣濡?愿痢≪쑝濡??뺤씤?섏뿀?ㅻ뒗 寃껋?
          臾쇰━?숈쓽 ?덉륫?κ낵 ?꾨쫫?ㅼ???蹂댁뿬二쇰뒗 ??쒖쟻 ?щ??낅땲??
        </p>
      </div>
    </div>
  );
}

/* ??????????????????????????????????????????????
   硫붿씤 ??
?????????????????????????????????????????????? */
const TABS = [
  { id:'concept',  label:'?뙌 釉붾옓??대??' },
  { id:'calc',     label:'?뵯 ?덈컮瑜댁툩?ㅽ듃 怨꾩궛湲? },
  { id:'detect',   label:'?뱻 釉붾옓? ?먯?' },
  { id:'qa',       label:'???먭뎄 吏덈Ц' },
];

const App = () => {
  const [tab, setTab] = useState('concept');
  return (
    <div style={{maxWidth:1100,margin:'0 auto'}}>
      <div style={{background:'linear-gradient(135deg,#0f0520,#1a0a3e)',borderRadius:16,padding:'20px 24px',
        marginBottom:20,border:'1px solid #5b21b6'}}>
        <h2 style={{color:'#c4b5fd',margin:0,fontSize:'1.4rem'}}>?뙌 ?숈뒿二쇱젣 6-2: 釉붾옓? ?먭뎄</h2>
        <p style={{color:'#94a3b8',margin:'8px 0 0',fontSize:'0.95rem'}}>
          <strong style={{color:'#fbbf24'}}>?듭떖 吏덈Ц:</strong> ?덉텧?띾룄媛 鍮쏆쓽 ?띾룄蹂대떎 ??泥쒖껜媛 議댁옱?????덉쓣源? 洹?泥쒖껜瑜??대뼸寃?諛쒓껄?????덉쓣源?
        </p>
      </div>
      <div className="tab-bar">
        {TABS.map(t=>(
          <button key={t.id} className={`tab-btn ${tab===t.id?'active':''}`}
            onClick={()=>setTab(t.id)}>{t.label}</button>
        ))}
      </div>
      {tab==='concept' && <ConceptTab/>}
      {tab==='calc'    && <SchwarzschildTab/>}
      {tab==='detect'  && <DetectTab/>}
      {tab==='qa'      && <QATab/>}
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""

REACT_HTML_FINAL = REACT_HTML.replace("__BH_IMG_B64__", _img_b64)
components.html(REACT_HTML_FINAL, height=1500, scrolling=True)
