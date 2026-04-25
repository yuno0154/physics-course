import streamlit as st
import streamlit.components.v1 as components
import base64, os

st.sidebar.title("? 釉?? ?援?)
st.sidebar.markdown("?異??媛 鍮? ??瑜??? 泥泥대? ?援ы⑸??")

# 釉?? 援ъ“ ?대몄? (bh_structure.png ?곗, ??쇰㈃ blackhole.png ?ъ?
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
  { name:'吏援?,    M:5.972e24,  R_real:6.371e6,   emoji:'?', color:'#3b82f6' },
  { name:'??',    M:1.989e30,  R_real:6.960e8,   emoji:'?截', color:'#fbbf24' },
  { name:'諛깆???,M:1.989e30*1.4, R_real:7e6,   emoji:'??, color:'#e2e8f0' },
  { name:'以?깆蹂',M:1.989e30*2.0, R_real:12000,  emoji:'??, color:'#60a5fa' },
  { name:'M87* BH', M:6.5e9*1.989e30, R_real:0,   emoji:'?', color:'#a78bfa' },
];

/* ?? KaTeX ?? ??留 ?? */
const Eq = ({ f, display=false, color='#c4b5fd' }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && window.katex)
      window.katex.render(f, ref.current, { throwOnError:false, displayMode:display });
  }, [f, display]);
  return <span ref={ref} style={{ color }} />;
};

/* ??????????????????????????????????????????????
   ? 1: 釉???대? (媛? + ?諛瑜댁??ㅽ???)
?????????????????????????????????????????????? */
const CONCEPT_STEPS = [
  { n:1, title:'?異?? 怨듭 異諛', color:'#3b82f6', bg:'#0d1f3c',
    formula:'v_{\\text{?異}} = \\sqrt{\\dfrac{2GM}{R}}',
    note:'??? ??吏 蹂댁〈?쇰? ??? ?異?? 怨듭????' },
  { n:2, title:'?異?? = 鍮? ?? 議곌굔 ?ㅼ', color:'#8b5cf6', bg:'#1a0d3c',
    formula:'c = \\sqrt{\\dfrac{2GM}{R_s}}',
    note:'?異??媛 鍮? ??(c)? 媛?吏? 諛吏由 Rs瑜?援ы⑸??' },
  { n:3, title:'Rs? ??* ??????????????????????????????????????????????
   3D ?怨듦? 援ъ“ ?裕щ?댁 (Three.js 湲곕?)
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

    // 2. Flamm's Paraboloid (?怨듦? 怨〓㈃)
    // ??? ??: w(r) = 2 * sqrt(Rs * (r - Rs))
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

    // 3. ?ш굔 吏?? (Event Horizon) - 寃? 援ъ껜
    const ehGeo = new THREE.SphereGeometry(Rs - 0.5, 32, 32);
    const ehMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
    const ehMesh = new THREE.Mesh(ehGeo, ehMat);
    ehMesh.position.y = -1; // 怨〓㈃ ??⑥ ?댁? 嫄몄묠
    scene.add(ehMesh);

    // ?ш굔 吏?? ?愿 (Glow)
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

    // 4. 媛李??諛 (Accretion Disk) - ????
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

    // 5. 二쇱 沅ㅻ 留 (愿?援? ISCO)
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
        
        // ?諛 ?? (?履쎌쇱濡 鍮瑜닿? - 耳??ъ ??ы寃 ?媛?)
        const pos = accretionDisk.geometry.attributes.position.array;
        for (let i = 0; i < particleCount; i++) {
            const r = orbitRadius[i];
            const speed = 0.5 * Math.pow(Rs/r, 1.5);
            const angle = time * speed + i;
            pos[i*3] = r * Math.cos(angle);
            pos[i*3+2] = r * Math.sin(angle);
        }
        accretionDisk.geometry.attributes.position.needsUpdate = true;
        
        // 移대???遺??ъ???
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
            ?? 釉?? 3D ?怨듦? 援ъ“ (3D Spacetime View)
          </p>
          <p style={{color:'#6d28d9',fontSize:12,marginTop:3}}>
            ?怨듦?? 3李⑥? 怨〓?(Flamm's Paraboloid)怨?媛李⑹諛? 紐⑥듭 ?裕щ?댁?⑸??
          </p>
        </div>
        <div style={{display:'flex',flexDirection:'column',gap:5,fontSize:11,flexShrink:0,marginLeft:20}}>
            <div style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:'#a78bfa',fontWeight:700}}>?</span>
              <span style={{color:'#64748b'}}>?ш굔 吏??</span>
            </div>
            <div style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:'#fbbf24',fontWeight:700}}>??</span>
              <span style={{color:'#64748b'}}>愿? 援?(r=1.5R?)</span>
            </div>
            <div style={{display:'flex',alignItems:'center',gap:6}}>
              <span style={{color:'#22c55e',fontWeight:700}}>??</span>
              <span style={{color:'#64748b'}}>ISCO (r=3R?)</span>
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
            ? 釉?? 二쇰? ?怨듦? 援ъ“ ? ?? ??쇰낵濡?대 (Flamm's Paraboloid)
          </p>
          <p style={{color:'#6d28d9',fontSize:12,marginTop:3}}>
            ?怨듦?? 怨듦?? 怨〓?? ?⑤㈃(Cross-section)?쇰? ???⑸?? 源?대 ?怨듦? 怨〓?? ?멸린瑜???????
          </p>
        </div>
        <div style={{display:'flex',flexDirection:'column',gap:5,fontSize:11,flexShrink:0,marginLeft:20}}>
          {[
            ['??','rgba(167,139,250,0.85)','?ш굔 吏?? (EH)'],
            ['??','rgba(251,191,36,0.8)','愿? 援?(r=1.5R?)'],
            ['? ','rgba(34,197,94,0.8)','ISCO (r=3R?)'],
            ['?','#fbbf24','?뱀댁'],
            ['?','rgba(253,224,71,0.9)','援댁?? 鍮'],
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

      // 蹂
      for (let i=0;i<80;i++){
        const sx=(i*137.5)%W, sy=(i*97+i*11)%H;
        ctx.beginPath(); ctx.arc(sx,sy,0.4+(i%3)*0.3,0,Math.PI*2);
        ctx.fillStyle=`rgba(210,225,255,${0.1+(i%5)*0.06})`; ctx.fill();
      }

      const CX=W*0.5, CY=H*0.5;
      const BH_R=55;

      // 媛李??諛 (Accretion Disk)
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

      // ???(Relativistic Jets)
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

      // 釉?? 蹂몄껜
      const bhGrad = ctx.createRadialGradient(CX-10,CY-10,5,CX,CY,BH_R);
      bhGrad.addColorStop(0,'#1a0a30'); bhGrad.addColorStop(0.5,'#08040f'); bhGrad.addColorStop(1,'#000');
      ctx.beginPath(); ctx.arc(CX,CY,BH_R,0,Math.PI*2); ctx.fillStyle=bhGrad; ctx.fill();

      // ?ш굔 吏?? 湲濡??      const ehGrad = ctx.createRadialGradient(CX,CY,BH_R,CX,CY,BH_R+20);
      ehGrad.addColorStop(0,'rgba(139,92,246,0.6)'); ehGrad.addColorStop(1,'rgba(139,92,246,0)');
      ctx.beginPath(); ctx.arc(CX,CY,BH_R+20,0,Math.PI*2); ctx.fillStyle=ehGrad; ctx.fill();
      ctx.beginPath(); ctx.arc(CX,CY,BH_R,0,Math.PI*2);
      ctx.strokeStyle='rgba(139,92,246,0.9)'; ctx.lineWidth=2; ctx.stroke();

      // 鍮? ?? (?ы?? 愿?)
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
      ctx.fillText('?ш굔 吏??', CX, CY-BH_R-12);
      ctx.fillStyle='rgba(252,211,77,0.7)'; ctx.font='11px Noto Sans KR';
      ctx.fillText('媛李??諛', CX+BH_R*2.2, CY+BH_R*0.2);
      ctx.fillStyle='rgba(139,92,246,0.7)';
      ctx.fillText('??濡? ???, CX+35, CY-BH_R-45);

      ctx.textAlign='left';
      animRef.current = requestAnimationFrame(loop);
    };
    animRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animRef.current);
  }, []);

  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>? ?듭?吏臾?/p>
        <p style={{color:'#cbd5e1',fontSize:14,lineHeight:1.8}}>
          ?異?? 怨듭 <Eq f="v_{\text{?異}}=\sqrt{2GM/R}"/> ??,
          留??泥泥댁 諛吏由? 異⑸?? ?寃 留?ㅼ?<strong style={{color:'#a78bfa'}}>?異?? = 鍮? ??(c)</strong>媛 ?硫??대산? ?源?
          鍮議곗감 ?異?吏 紐삵? ??泥泥대? <strong style={{color:'#c4b5fd'}}>釉??</strong>?대????
        </p>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginBottom:16}}>
        <canvas ref={canvasRef} width={480} height={300}
          style={{width:'100%',height:'300px',borderRadius:'12px',background:'#05070a'}}/>
        <div style={{display:'flex',flexDirection:'column',gap:12}}>
          <div className="card" style={{flex:1}}>
            <p style={{color:'#a78bfa',fontWeight:700,fontSize:14,marginBottom:10}}>? 釉??? ?듭??뱀?/p>
            {[
              ['?ш굔 吏??','鍮? ?異 遺媛?ν 寃쎄?硫? 諛吏由 = ?諛瑜댁??ㅽ?諛吏由 Rs'],
              ['?뱀댁','以?щ?. 諛?媛 臾댄?濡 諛?고? ?. ???臾쇰━?? ?怨'],
              ['媛李??諛','釉??濡 鍮⑤ㅻ? 臾쇱????대（? ?④굅???諛. X? 諛⑹?'],
              ['??濡? ???,'釉??? ?湲곗μ ????吏 諛⑺μ쇰? 肉?댁?? 臾쇱?'],
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
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>? ?諛瑜댁??ㅽ?諛吏由 ??</p>
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
                    <span style={{fontSize:15,flexShrink:0}}>??/span>
                    <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.75}}>{s.note}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ?? 釉?? 援ъ“ ?대몄? + ?ㅻ? ?? */}
      <SpacetimeCanvas/>

      <div className="card" style={{marginBottom:16}}>
        <p style={{fontWeight:800,color:'#e2e8f0',fontSize:15,marginBottom:14}}>
          ?쇽? 釉??? 援ъ“ ? ?⑤㈃?
        </p>
        <div style={{display:'grid',gridTemplateColumns:'220px 1fr',gap:20,alignItems:'flex-start'}}>
          {/* ?대몄? */}
          <div style={{borderRadius:12,overflow:'hidden',border:'1px solid #3b1e7c',
            background:'#000',display:'flex',alignItems:'center',justifyContent:'center'}}>
            {"__BH_IMG_B64__" !== "" ? (
              <img src={"data:image/png;base64,__BH_IMG_B64__"}
                style={{width:'100%',display:'block',borderRadius:11}}
                alt="釉?? 援ъ“ ?⑤㈃?"/>
            ) : (
              <div style={{padding:24,color:'#475569',fontSize:12,textAlign:'center'}}>
                ?대몄?瑜?assets/bh_structure.png濡 ??ν?二쇱몄.
              </div>
            )}
          </div>
          {/* 援ъ“ ?ㅻ? */}
          <div style={{display:'flex',flexDirection:'column',gap:10}}>
            <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.8,marginBottom:6}}>
              釉??? ?吏?쇰? ???蹂??⑤㈃????? ?怨듦?? 怨〓????ы?濡 "源??媛 源?댁????
            </p>
            {[
              ['#a78bfa','?ш굔 吏?? (Event Horizon)',
                `諛吏由 R? = 2GM/c짼??援щ㈃. ??寃쎄? ?履쎌?? ?異?? > c ?대濡 鍮? ?異 遺媛. ?몃? 愿痢≪? ??寃쎄? ?癒몃? 蹂?? ??듬??`],
              ['#fbbf24','?뱀댁 (Singularity)',
                `釉??? 以?? 諛? ? ?, 遺??? 0. ???臾쇰━?(?쇰? ?????대?)????⑸吏 ?? 吏??쇰?, ?? 以???대??????⑸??`],
              ['rgba(251,191,36,0.8)','愿? 援?(Photon Sphere)',
                `r = 1.5 R???援щ㈃. 鍮???? 沅ㅻ瑜?洹몃┫ ? ?? 寃쎄??댁?留, 遺???⑸?? ?쎄?? 援?留 ??대 鍮? ?異?嫄곕 ?ы?⑸??`],
              ['rgba(34,197,94,0.8)','ISCO (理?닿? ?? ?? 沅ㅻ)',
                `r = 3 R?. 臾쇱???????쇰? ? 沅ㅻ瑜??吏? ? ?? 媛???履?寃쎄?. ?대낫???履쎌 臾쇱?? 鍮瑜닿? 釉??濡 ????쇰? ?⑥댁????`],
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
        <p style={{color:'#c4b5fd',fontWeight:800,fontSize:15,marginBottom:8}}>? 寃곕?</p>
        <p style={{color:'#ddd6fe',fontSize:13,lineHeight:1.85}}>
          ?諛瑜댁??ㅽ?諛吏由 <Eq f="R_s = \dfrac{2GM}{c^2}"/> ?履쎌?? ?異??媛 鍮? ??瑜?珥怨쇳誘濡,
          ?대?臾쇱껜?, ?ъ???鍮議곗감? ?異? ? ??듬??<br/>
          <strong style={{color:'#a78bfa'}}>釉?????? 議곌굔</strong>: 泥泥댁 諛吏由 ??Rs = 2GM/c짼<br/>
          吏援ш? 釉??????ㅻ㈃ 諛吏由? ??<strong style={{color:'#fbbf24'}}>9 mm</strong>濡 ?異?댁??⑸??
        </p>
      </div>
    </div>
  );
}

/* ??????????????????????????????????????????????
   ? 2: ?諛瑜댁??ㅽ?諛吏由 怨?곌린
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

  // ?媛?: 諛吏由 鍮援 ?ㅼ댁닿렇??  useEffect(() => {
    const canvas = canvasRef.current; if(!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.fillStyle='#05070a'; ctx.fillRect(0,0,W,H);

    // 蹂
    for (let i=0;i<60;i++){
      const sx=(i*137)%W, sy=(i*97)%H;
      ctx.beginPath(); ctx.arc(sx,sy,0.4+(i%3)*0.25,0,Math.PI*2);
      ctx.fillStyle=`rgba(200,220,255,${0.08+(i%5)*0.05})`; ctx.fill();
    }

    const M = M_use;
    const Rs_v = Rs;
    const R_v = R_real;

    // 以? ?移
    const CX = W*0.5, CY = H*0.5;

    // 諛吏由 ?ㅼ???怨??(?媛?)
    const maxR = Math.max(Rs_v, R_v);
    const scale = Math.min(H*0.35, W*0.35) / Math.max(maxR, 1);
    const Rs_px = Math.max(Math.min(Rs_v * scale, 120), 8);
    const R_px  = R_v > 0 ? Math.max(Math.min(R_v * scale, 120), 8) : 0;

    // ?諛瑜댁??ㅽ?諛吏由 (?ш굔 吏??)
    const ehGrad = ctx.createRadialGradient(CX,CY,0,CX,CY,Rs_px);
    ehGrad.addColorStop(0,'#000'); ehGrad.addColorStop(0.7,'#0d0518'); ehGrad.addColorStop(1,'#1a0030');
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px,0,Math.PI*2); ctx.fillStyle=ehGrad; ctx.fill();
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px,0,Math.PI*2);
    ctx.strokeStyle='rgba(139,92,246,0.9)'; ctx.lineWidth=2.5; ctx.stroke();

    // 湲濡??    const gGrad = ctx.createRadialGradient(CX,CY,Rs_px,CX,CY,Rs_px+20);
    gGrad.addColorStop(0,'rgba(139,92,246,0.4)'); gGrad.addColorStop(1,'rgba(139,92,246,0)');
    ctx.beginPath(); ctx.arc(CX,CY,Rs_px+20,0,Math.PI*2); ctx.fillStyle=gGrad; ctx.fill();

    // ?ㅼ 泥泥?諛吏由 (?? 寃쎌?
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
    ctx.fillText('?ш굔 吏?? (Rs)', CX, CY - Rs_px - 12);

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
      ctx.fillText('?ㅼ 諛吏由', CX + R_px + 15, CY);
      ctx.fillStyle='rgba(200,200,255,0.55)'; ctx.font='10px Space Mono';
      ctx.fillText(fmtR(R_v), CX + R_px + 15, CY + 15);
    }

    // 鍮援 ??
    if (R_v > 0) {
      const ratio = R_v / Rs_v;
      ctx.fillStyle='rgba(148,163,184,0.8)'; ctx.font='11px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText(`?ㅼ 諛吏由 = Rs ? ${ratio.toExponential(2)}`, CX, H-14);
    }

    ctx.textAlign='left';
  }, [sel, massScale, isCustom]);

  const fmtNum = (r) => {
    if (r >= 1e12) return (r/1e12).toFixed(3) + ' Tm (??쇰명?';
    if (r >= 1e9)  return (r/1e9).toFixed(3) + ' Gm (湲곌?誘명?';
    if (r >= 1e6)  return (r/1e6).toFixed(3) + ' Mm ? ' + (r/1e3).toFixed(0) + ' km';
    if (r >= 1e3)  return (r/1e3).toFixed(3) + ' km';
    if (r >= 1)    return r.toFixed(4) + ' m';
    return (r*1000).toFixed(4) + ' mm';
  };

  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>? ?諛瑜댁??ㅽ?諛吏由 怨?곌린</p>
        <p style={{color:'#cbd5e1',fontSize:14}}>
          怨듭: <Eq f="R_s = \dfrac{2GM}{c^2}"/> &nbsp;
          吏援?Rs ? 8.9 mm | ?? Rs ? 3.0 km
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
          ?截 ??吏? 諛곗
        </button>
      </div>

      {isCustom && (
        <div className="card" style={{marginBottom:14}}>
          <label>?? 吏?? 諛곗: {massScale.toLocaleString('ko-KR')} M?</label>
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
            <p style={{color:'#64748b',fontSize:12,marginBottom:10,fontWeight:700}}>怨??寃곌낵</p>
            <div className="result-row">
              <span style={{color:'#94a3b8'}}>吏? (M)</span>
              <span className="val">{M_use.toExponential(3)} kg</span>
            </div>
            <div className="result-row">
              <span style={{color:'#94a3b8'}}>?諛瑜댁??ㅽ?諛吏由 (Rs)</span>
              <span className="val">{fmtNum(Rs)}</span>
            </div>
            {!isCustom && PRESETS_BH[sel].R_real > 0 && (
              <div className="result-row">
                <span style={{color:'#94a3b8'}}>?ㅼ 諛吏由</span>
                <span className="val" style={{color:'#60a5fa'}}>{fmtNum(PRESETS_BH[sel].R_real)}</span>
              </div>
            )}
            {!isCustom && PRESETS_BH[sel].R_real > 0 && (
              <div className="result-row">
                <span style={{color:'#94a3b8'}}>?ㅼ / Rs 鍮??/span>
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
              {isBH_now ? '? 釉?? ??' : '? ?쇰? 泥泥???'}
            </p>
            <p style={{color: isBH_now?'#ddd6fe':'#86efac', fontSize:13, lineHeight:1.75}}>
              {isBH_now
                ? '?ㅼ 諛吏由???諛瑜댁??ㅽ?諛吏由蹂대??嫄곕 媛?듬?? ??泥泥대 釉?????? ?ш굔 吏?? ?대?濡 ?ㅼ닿? 臾쇱껜? ?異 遺媛?ν⑸??'
                : `?ㅼ 諛吏由??Rs蹂대?${(PRESETS_BH[sel].R_real/Rs).toExponential(2)}諛??쎈?? 釉??????ㅻ㈃ ??泥泥대? ${fmtNum(Rs)}源吏 ?異?댁??⑸??`}
            </p>
          </div>
        </div>
      </div>

      <div className="card">
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>二쇱 泥泥댁 ?諛瑜댁??ㅽ?諛吏由 鍮援</p>
        <div style={{overflowX:'auto'}}>
          <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
            <thead>
              <tr style={{borderBottom:'1px solid #1e293b'}}>
                {['泥泥?,'吏?','?ㅼ 諛吏由','?諛瑜댁??ㅽ?諛吏由 Rs','??'].map(h=>(
                  <th key={h} style={{padding:'10px 12px',color:'#64748b',fontWeight:700,textAlign:'left'}}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                ['? 吏援?,  '5.97?10짼??kg', '6,371 km', '8.9 mm',   false],
                ['?截 ??',  '1.99?10쨀??kg', '696,000 km','3.0 km',  false],
                ['??諛깆???,'1.4 M?',       '~7,000 km', '4.1 km',  false],
                ['??以?깆蹂','2.0 M?',       '~12 km',    '5.9 km',  true ],
                ['? M87*',  '6.5?10??M?',  '?',         '~192 AU', true ],
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
                      {isBH ? '釉??' : '?쇰? 泥泥?}
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
   ? 3: 釉?? ?吏 諛⑸?
?????????????????????????????????????????????? */
const DETECT_METHODS = [
  {
    icon:'?∽?', title:'X? ??깃? (X-ray Binaries)',
    color:'#ef4444',
    summary:'釉?????諛?깆 臾쇱?? 媛李??諛?쇰? ?≪? ? 諛⑹??? X?? 愿痢?,
    how:'?諛 蹂?? ??щ??媛?ㅺ? 釉?? 二쇰? 媛李??諛? ??깊硫??諛깅??濡 媛?대??媛? X?? 諛⑹??⑸??',
    example:'諛깆“?由?X-1 (1964? 理珥 諛寃?, 沅ㅻ ?대?쇰? 釉?? 吏? 異? 媛??,
    evidence:'蹂댁댁? ?? ?諛泥?+ X? + 沅ㅻ ?대 = 釉??'
  },
  {
    icon:'?', title:'以?ν (Gravitational Waves)',
    color:'#3b82f6',
    summary:'? 釉?????⑸?? ? ?怨듦?? ??? LIGO/Virgo 媛?怨濡 寃異',
    how:'? 釉???????대?硫??⑹?吏 ? ?泥? ??吏媛 以?ν濡 諛⑹??⑸?? ??????吏援щ? ?듦낵?硫?怨듦????? ?? ?ш린? 1/1000留???異?⑸??',
    example:'GW150914 (2015?): 36M? + 29M? ? 62M? 釉??. 3M?? ?대뱁? ??吏媛 以?ν濡 諛⑹?.',
    evidence:'以?ν ?? 遺??쇰? 蹂???? 吏? ?? 怨??媛??
  },
  {
    icon:'?', title:'以???利 (Gravitational Lensing)',
    color:'#8b5cf6',
    summary:'釉??? 媛? 以?μ?諛곌꼍 蹂鍮? ?寃 留?? ?? 愿痢?,
    how:'釉????諛곌꼍 蹂怨?吏援??ъ대? ?듦낵? ?, 蹂鍮??釉?? 以?μ ??????諛湲곌? 利媛?⑸??誘몄 以???利). 珥?吏? 釉??? ??댁??? ?щ?媛濡 遺由ъ?듬??',
    example:'?釉 留?寃쎌 ??몄???留 愿痢? M87* ?ш굔 吏?? 留?寃?EHT) 珥ъ',
    evidence:'??몄?????媛, 留 ???뱀? 愿? ??'
  },
  {
    icon:'狩', title:'蹂? 沅ㅻ ?대 (Stellar Orbits)',
    color:'#fbbf24',
    summary:'珥?吏? 釉?? 二쇰? 蹂?ㅼ 沅ㅻ瑜??? ?媛 異????釉?? 吏?怨??移 寃곗',
    how:'?곕━ ?? 以??沅??由?A*) 二쇰? S2蹂? 16?媛 異?? 寃곌낵, 蹂댁댁? ?? 吏?????? 400留 諛곗? ??? ?닿???釉??? 寃곗? 利嫄?',
    example:'S2蹂: 16.0? 二쇨린, 洹쇱??? 鍮? 2.87%? ??. 2020? ?몃꺼 臾쇰━??.',
    evidence:'耳???踰移?쇰? 以??吏? 怨??? 釉?? ???
  },
  {
    icon:'??, title:'?ш굔 吏?? 留?寃?(Event Horizon Telescope)',
    color:'#10b981',
    summary:'? 吏援?洹紐⑥ ??留?寃??ㅽ몄?щ? 釉?? 洹몃┝?瑜?吏? 珥ъ',
    how:'吏援??ш린? 媛? 留?寃?VLBI 湲곗)?쇰? M87 ?? 以?ъ 珥?吏? 釉??? 珥ъ. 釉?? 洹몃┝?(shadow)? 媛李??諛? 怨由?援ъ“瑜????',
    example:'2019? M87* 釉?? 理珥 吏? 珥ъ (吏?: ??? 65?듬같). 2022? ?곕━ ?? 以??沅??由?A* 珥ъ.',
    evidence:'鍮 怨由?Photon Ring)? 以?? ?대??洹몃┝? = ?ш굔 吏??? 吏? 利嫄?
  },
];

function DetectTab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:18}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>??釉??? 諛寃ы? 諛⑸?</p>
        <p style={{color:'#cbd5e1',fontSize:14,lineHeight:1.8}}>
          釉??? 鍮? 諛⑹??吏 ??쇰濡 <strong style={{color:'#a78bfa'}}>媛????諛⑸?</strong>?쇰?留 ?吏?⑸??
          二쇰? 臾쇱?怨쇱 ??몄?? 以???④낵, ?怨듦? ?怨≪?利嫄곌? ?⑸??
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
                  <span style={{color:m.color,fontWeight:800,fontSize:12,flexShrink:0,paddingTop:2}}>?由?/span>
                  <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.75}}>{m.how}</p>
                </div>
                <div style={{display:'flex',gap:10}}>
                  <span style={{color:'#fbbf24',fontWeight:800,fontSize:12,flexShrink:0,paddingTop:2}}>?щ?</span>
                  <p style={{color:'#fcd34d',fontSize:13,lineHeight:1.75}}>{m.example}</p>
                </div>
                <div style={{display:'flex',gap:10,background:`${m.color}11`,padding:'10px 14px',borderRadius:10,border:`1px solid ${m.color}33`}}>
                  <span style={{fontSize:14,flexShrink:0}}>?</span>
                  <p style={{color:m.color,fontSize:13,lineHeight:1.7,fontWeight:600}}>{m.evidence}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card" style={{marginTop:16,background:'linear-gradient(135deg,#0c1a0c,#0a2a0a)',borderColor:'#22c55e'}}>
        <p style={{color:'#4ade80',fontWeight:800,fontSize:14,marginBottom:10}}>??怨듯??由?/p>
        <p style={{color:'#86efac',fontSize:13,lineHeight:1.85}}>
          紐⑤ ?吏 諛⑸?? <strong>釉?? 二쇰?? 臾쇰━? ?④낵</strong>瑜?愿痢≫⑸??
          釉?? ?泥대 蹂댁댁? ?吏留, ?댄댁 以??踰移怨??쇰? ?????대??쇰? ?痢≫ ???ㅼ?          ??? 愿痢〓??釉??? 議댁щ? 利紐?⑸??
          2020? ?몃꺼 臾쇰━??? ?곕━ ?? 以??釉?? ?곌뎄? ??щ??듬??
        </p>
      </div>
    </div>
  );
}

/* ??????????????????????????????????????????????
   ? 4: ?援?吏臾??????????????????????????????????????????????? */
const QA_BH = [
  { q:'釉??? "紐⑤ 寃? 鍮⑥?ㅼ몃?? 留??留?源?',
    a:'諛? 留怨 諛? ?由쎈?? ?ш굔 吏?? ?대???? ?異??遺媛?ν吏留, ?ш굔 吏?? 諛源μ?? 釉??? 媛? 吏?? 蹂怨???쇳寃 以?μ ??⑺⑸?? ????媛? 吏?? 釉??濡 諛??대 吏援?沅ㅻ? 蹂?吏 ??듬?? 釉??? "媛源??媛硫????吏留" 硫由ъ? ?踰? 以?μ껜????' },
  { q:'????釉????? ? ??源?',
    a:'????? 釉??????ㅻ㈃ 珥????諛?????怨, ?대? ??댁? ?? 吏?? ??8諛??댁?????⑸?? ??? ??50??? ? ?? 嫄곗깆 嫄곗? 諛깆 ??깆쇰? ?? 留媛?⑸?? ??? 釉??濡 留?ㅻㅻ㈃ 諛吏由? ??3 km濡 ?異?댁????? ??곗??怨쇱?쇰?? 遺媛?ν⑸??' },
  { q:'釉???? ??ㅻ ?蹂대 ??源? (?명?蹂듭?',
    a:'?ㅽ곕? ?명뱀 1974? ?? ?? ?④낵濡 釉?????대났?щ? 諛⑹???ㅺ? ?痢≫?듬???명?蹂듭?. 釉?? 二쇰??? 媛? ??-諛?? ?????깅 ?, ? ??媛 ?ш굔 吏?? ??쇰? ?ㅼ닿?怨 ?ㅻⅨ ??媛 ?異?硫?釉??? 吏?? ??듬?? 留ㅼ??? 釉??? 鍮瑜닿? 利諛? ? ?吏留, 嫄곕 釉??? ?명??⑤? ?곗＜ 諛곌꼍 蹂듭щ낫?ㅻ ?? ??ㅼ?쇰? 痢≪??遺媛?ν⑸??' },
  { q:'釉?? ?대?? ?ㅼ닿?硫??대산? ?源?',
    a:'硫由ъ 蹂대㈃: ?媛 ?쎌갹(以???? ?몄? ?臾몄 吏??媛 ?ш굔 吏??? ??? ?洹쇳? 寃泥??蹂댁대ŉ ?? ?由욱댁???? 吏?? ??? 吏????ъ? ?? 釉???대쇰㈃ ?ш굔 吏??? ?듦낵? ? ?밸?? 蹂?瑜???쇱? 紐삵 ? ??듬?? ?吏留 ?뱀댁? 媛源?吏?濡 議곗??tidal force)??洹밸⑥?쇰? 而ㅼ?"?ㅽ寃?고(spaghettification)"?⑸?? ?뱀댁??? ??ъ 臾쇰━ 踰移????⑸吏 ??듬??' },
  { q:'?곕━ ?? 以?ъ? 釉??????源?',
    a:'?? 沅??由?A*(Sgr A*)?쇰 珥?吏? 釉??????쇰ŉ, 吏?? ??? ??400留 諛곗??? 吏援ъ? ??26,000愿? ?⑥댁???듬?? 2022? ?ш굔 吏?? 留?寃?EHT)??Sgr A*? ?대몄?瑜?吏? 珥ъ??쇰ŉ, 2020? ?몃꺼 臾쇰━??? S2蹂 沅ㅻ 異?? ?듯 Sgr A* ?곌뎄? ??щ??듬??' },
];

function QATab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:18}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:4}}>? ?援?吏臾?/p>
        <p style={{color:'#94a3b8',fontSize:13}}>吏臾몄 ?대┃????듬?? ??명?몄. 癒쇱 ?ㅼㅻ? ?媛??蹂댁몄.</p>
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
        <p style={{color:'#c4b5fd',fontWeight:800,marginBottom:10}}>? ?곌껐 媛?</p>
        <p style={{color:'#a78bfa',fontSize:13,lineHeight:1.9}}>
          釉?? ?援щ ?댄댁 以??踰移 ? ?異?? ? ?諛瑜댁??ㅽ?諛吏由 ? ??몄??몄 ?쇰? ?????대??쇰? ?댁댁?? 媛?? ?곌껐????
          怨? ???쇰? ?痢≫ "鍮? ?異 紐삵? 泥泥?媛 ?ㅼ濡 愿痢≪쇰? ??몃??ㅻ 寃?
          臾쇰━?? ?痢〓κ낵 ?由?ㅼ? 蹂댁ъ＜? ??? ?щ?????
        </p>
      </div>
    </div>
  );
}

/* ??????????????????????????????????????????????
   硫?????????????????????????????????????????????????? */
const TABS = [
  { id:'concept',  label:'? 釉???대?' },
  { id:'calc',     label:'? ?諛瑜댁??ㅽ?怨?곌린' },
  { id:'detect',   label:'??釉?? ?吏' },
  { id:'qa',       label:'? ?援?吏臾? },
];

const App = () => {
  const [tab, setTab] = useState('concept');
  return (
    <div style={{maxWidth:1100,margin:'0 auto'}}>
      <div style={{background:'linear-gradient(135deg,#0f0520,#1a0a3e)',borderRadius:16,padding:'20px 24px',
        marginBottom:20,border:'1px solid #5b21b6'}}>
        <h2 style={{color:'#c4b5fd',margin:0,fontSize:'1.4rem'}}>? ??듭＜? 6-2: 釉?? ?援?/h2>
        <p style={{color:'#94a3b8',margin:'8px 0 0',fontSize:'0.95rem'}}>
          <strong style={{color:'#fbbf24'}}>?듭?吏臾?</strong> ?異??媛 鍮? ??蹂대???泥泥닿? 議댁ы ? ??源? 洹?泥泥대? ?대산? 諛寃ы ? ??源?
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
