# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

img_cross = os.path.join(assets_dir, "einstein_cross.png")
img_3d_curve = os.path.join(assets_dir, "spacetime_curvature.png")
img_blackhole = os.path.join(assets_dir, "blackhole.png")
img_reunion = os.path.join(assets_dir, "reunion.png")

def render_header_cards():
    st.markdown("#### 🔭 현대 우주론의 결정적 관측 및 이론적 모델")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image(img_cross, use_container_width=True, caption="아인슈타인의 십자가 (관측 모델)")
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); padding: 10px; border-radius: 8px;">
            <p style="font-size: 0.8rem; color: #cbd5e1; margin: 0;">중심 은하의 중력으로 뒤쪽 퀘이사의 상이 4개로 분리된 모습입니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.image(img_3d_curve, use_container_width=True, caption="3D 시공간 곡률과 빛의 경로")
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.4); padding: 10px; border-radius: 8px;">
            <p style="font-size: 0.8rem; color: #cbd5e1; margin: 0;">질량이 시공간을 함몰시키면, 빛은 그 골짜기를 따라 입체적으로 굴절됩니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.7); padding: 15px; border-radius: 12px; border-left: 5px solid #10b981; height: 100%;">
            <strong style="color: #10b981;">허블 딥 필드 (HDF)</strong><br/>
            <p style="font-size: 0.85rem; color: #cbd5e1; margin-top: 8px;">
                중력 렌즈는 '우주의 돋보기' 역할을 하여 인류가 관측할 수 있는 한계를 수십 배 이상 확장해 줍니다.
                아래 3D 시뮬레이션에서 마우스로 직접 회전하며 탐구해 보세요.
            </p>
        </div>
        """, unsafe_allow_html=True)

# 3D gravitational lensing simulation - pure Canvas 2D with custom 3D engine
LENSING_3D_HTML = """
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#030608; overflow:hidden; }
#wrap { position:relative; width:100%; height:560px; user-select:none; }
#sim { display:block; width:100%; height:560px; cursor:grab; }
#sim:active { cursor:grabbing; }
#hint {
  position:absolute; bottom:14px; left:50%; transform:translateX(-50%);
  color:#64748b; font:12px/1 sans-serif;
  background:rgba(0,0,0,0.55); padding:6px 14px; border-radius:20px;
  pointer-events:none; white-space:nowrap;
}
#mbadge {
  position:absolute; top:12px; left:12px;
  color:#a5b4fc; font:bold 12px sans-serif;
  background:rgba(15,23,42,0.82); padding:6px 14px; border-radius:8px;
  border:1px solid rgba(99,102,241,0.35); pointer-events:none;
}
#inset {
  position:absolute; top:12px; right:12px; border-radius:12px;
  background:rgba(5,8,18,0.88); border:1px solid rgba(99,102,241,0.35);
  pointer-events:none;
}
</style>
<div id="wrap">
  <canvas id="sim" width="820" height="560"></canvas>
  <div id="hint">&#x1F5B1; 드래그: 회전 &nbsp;|&nbsp; 스크롤: 줌</div>
  <div id="mbadge">질량: <span id="mv">?</span> M&#x2609;</div>
  <canvas id="inset" width="160" height="160"></canvas>
</div>
<script>
(function () {
  var MASS = 5;
  var CASE = 'cross';
  try {
    if (window.stParams) {
      MASS = parseFloat(window.stParams.mass) || 5;
      CASE = window.stParams.case || 'cross';
    }
  } catch(e) {}
  document.getElementById('mv').textContent = MASS.toFixed(1);

  var canvas = document.getElementById('sim');
  var ctx = canvas.getContext('2d');
  var W = 820, H = 560;
  canvas.width = W; canvas.height = H;

  // Camera rotation state
  var theta = -0.15;
  var phi   =  0.22;
  var zoom  =  1.0;
  var drag  = false, lx = 0, ly = 0;

  canvas.addEventListener('mousedown', function(e) { drag=true; lx=e.offsetX; ly=e.offsetY; });
  canvas.addEventListener('mouseup',   function()  { drag=false; });
  canvas.addEventListener('mouseleave',function()  { drag=false; });
  canvas.addEventListener('mousemove', function(e) {
    if (!drag) return;
    theta += (e.offsetX - lx) * 0.007;
    phi   += (e.offsetY - ly) * 0.007;
    phi = Math.max(-1.35, Math.min(1.35, phi));
    lx = e.offsetX; ly = e.offsetY;
  });
  canvas.addEventListener('wheel', function(e) {
    zoom *= e.deltaY > 0 ? 0.92 : 1.09;
    zoom = Math.max(0.25, Math.min(4.0, zoom));
    e.preventDefault();
  }, { passive: false });

  // 3D -> 2D perspective projection
  // Y-axis rotation (theta) then X-axis rotation (phi) then perspective
  function proj(x, y, z) {
    var x1 =  x*Math.cos(theta) - z*Math.sin(theta);
    var z1 =  x*Math.sin(theta) + z*Math.cos(theta);
    var y2 =  y*Math.cos(phi)   + z1*Math.sin(phi);
    var z2 = -y*Math.sin(phi)   + z1*Math.cos(phi);
    var f  = 510 * zoom;
    var d  = 900;
    var s  = f / (d + z2);
    return { sx: W/2 + x1*s, sy: H/2 + y2*s, z: z2, s: s };
  }

  // Scene constants
  var SRC_X = -540, OBS_X = 540;
  var LENS_R = 15 + MASS * 2.2;
  var EIN_R  = 30 + MASS * 13;

  // Stars - uniform spherical distribution
  var stars = [];
  for (var i = 0; i < 350; i++) {
    var u  = Math.random()*2 - 1;
    var th = Math.random()*Math.PI*2;
    var sq = Math.sqrt(1 - u*u);
    stars.push({
      x: 3200*sq*Math.cos(th),
      y: 3200*u,
      z: 3200*sq*Math.sin(th),
      r: Math.random()*1.1+0.3,
      op: Math.random()*0.45+0.3
    });
  }

  // Spacetime grid - deformed by gravity well
  var gridLines = [];
  var GR = 500, GS = 55;
  for (var gi = -GR; gi <= GR; gi += GS) {
    var lxPts = [], lyPts = [];
    for (var gv = -GR; gv <= GR; gv += 18) {
      var dX = Math.max(-MASS*62, -MASS*520 / (Math.sqrt(gv*gv+gi*gi)+1));
      var dY = Math.max(-MASS*62, -MASS*520 / (Math.sqrt(gi*gi+gv*gv)+1));
      lxPts.push([gv, gi, dX]);
      lyPts.push([gi, gv, dY]);
    }
    gridLines.push(lxPts);
    gridLines.push(lyPts);
  }

  // Bent light rays: quadratic Bezier
  // Source(-540,0,0) -> control(0,by,bz) -> Observer(540,0,0)
  function makeBezier(by, bz) {
    var N = 52, pts = [];
    for (var i = 0; i <= N; i++) {
      var t = i/N, mt = 1-t;
      pts.push([
        mt*mt*SRC_X + t*t*OBS_X,
        2*mt*t*by,
        2*mt*t*bz
      ]);
    }
    return pts;
  }

  var rayCfg = CASE === 'cross'
    ? [
        {bF:0.30, n:16, r:255, g:215, b:0,   op:0.88, lw:1.55},
        {bF:0.54, n:16, r:251, g:191, b:36,  op:0.72, lw:1.25},
        {bF:0.84, n:16, r:245, g:158, b:11,  op:0.55, lw:1.00},
        {bF:1.40, n:12, r:217, g:119, b:6,   op:0.34, lw:0.75},
        {bF:2.40, n: 8, r:146, g: 64, b:14,  op:0.18, lw:0.55}
      ]
    : [
        {bF:0.28, n: 8, r:255, g:215, b:0,   op:0.90, lw:1.55},
        {bF:0.54, n: 8, r:251, g:191, b:36,  op:0.72, lw:1.25},
        {bF:0.90, n: 6, r:245, g:158, b:11,  op:0.50, lw:1.00},
        {bF:1.60, n: 4, r:217, g:119, b:6,   op:0.27, lw:0.70}
      ];

  var allRays = [];
  for (var ri = 0; ri < rayCfg.length; ri++) {
    var c = rayCfg[ri];
    var b = EIN_R * c.bF;
    for (var j = 0; j < c.n; j++) {
      var ang = (j/c.n)*Math.PI*2;
      allRays.push({
        pts: makeBezier(b*Math.cos(ang), b*Math.sin(ang)),
        cfg: c,
        phase: j/c.n
      });
    }
  }

  // Photon state - one per ray
  var photons = allRays.map(function(r) { return { ray: r, t: r.phase }; });

  // Observer view inset canvas
  var inset = document.getElementById('inset');
  var ic = inset.getContext('2d');

  function drawInset(ft) {
    ic.clearRect(0, 0, 160, 160);
    ic.font = 'bold 8.5px sans-serif';
    ic.fillStyle = '#64748b';
    ic.textAlign = 'center';
    ic.fillText("EARTH'S VIEW (TELESCOPE)", 80, 13);

    ic.beginPath(); ic.arc(80, 88, 58, 0, Math.PI*2);
    ic.strokeStyle = 'rgba(51,65,85,0.5)'; ic.lineWidth = 1; ic.stroke();

    var gr = ic.createRadialGradient(80,88,0,80,88,9);
    gr.addColorStop(0,'rgba(255,255,255,0.95)');
    gr.addColorStop(1,'rgba(165,180,252,0.1)');
    ic.beginPath(); ic.arc(80,88,9,0,Math.PI*2);
    ic.fillStyle = gr; ic.fill();

    var eR = 16 + MASS * 1.9;
    if (CASE === 'cross') {
      var pulse = 0.93 + 0.07*Math.sin(ft*0.038);
      ic.beginPath(); ic.arc(80, 88, eR*pulse, 0, Math.PI*2);
      ic.strokeStyle = 'rgba(251,191,36,' + (0.42+0.2*Math.sin(ft*0.038)) + ')';
      ic.lineWidth = 2.6; ic.stroke();
      var crossPts = [[80,88-eR*1.18],[80,88+eR*1.18],[80-eR*1.18,88],[80+eR*1.18,88]];
      for (var ci = 0; ci < crossPts.length; ci++) {
        var px = crossPts[ci][0], py = crossPts[ci][1];
        ic.save(); ic.shadowColor='#ffd700'; ic.shadowBlur=10;
        ic.beginPath(); ic.arc(px,py,4,0,Math.PI*2);
        ic.fillStyle='#ffd700'; ic.fill(); ic.restore();
      }
    } else {
      var sA = eR*(0.80 + MASS*0.07), sB = eR*0.55;
      var imgPts = [[80-sA,88,'A', MASS>5?0.95:0.40],[80+sB,88,'B',0.95]];
      for (var ii = 0; ii < imgPts.length; ii++) {
        var ipx=imgPts[ii][0], ipy=imgPts[ii][1], lbl=imgPts[ii][2], op=imgPts[ii][3];
        ic.save(); ic.shadowColor='#fbbf24'; ic.shadowBlur=8;
        ic.beginPath(); ic.arc(ipx,ipy,4,0,Math.PI*2);
        ic.fillStyle='rgba(251,191,36,'+op+')'; ic.fill(); ic.restore();
        ic.font='bold 10px sans-serif'; ic.fillStyle='#fbbf24'; ic.textAlign='center';
        ic.fillText(lbl, ipx, ipy-9);
      }
    }
  }

  // Main render loop
  var ft = 0;
  function render() {
    ft++;

    ctx.fillStyle = '#030608';
    ctx.fillRect(0, 0, W, H);

    // Stars
    for (var si = 0; si < stars.length; si++) {
      var s = stars[si];
      var p = proj(s.x, s.y, s.z);
      if (p.s <= 0) continue;
      ctx.beginPath(); ctx.arc(p.sx, p.sy, s.r, 0, Math.PI*2);
      ctx.fillStyle = 'rgba(255,255,255,' + s.op + ')'; ctx.fill();
    }

    // Spacetime grid
    ctx.lineWidth = 0.75;
    for (var gli = 0; gli < gridLines.length; gli++) {
      var line = gridLines[gli];
      ctx.beginPath(); ctx.strokeStyle = 'rgba(50,64,210,0.30)';
      var first = true;
      for (var gpi = 0; gpi < line.length; gpi++) {
        var gp = proj(line[gpi][0], line[gpi][1], line[gpi][2]);
        if (first) { ctx.moveTo(gp.sx, gp.sy); first=false; }
        else ctx.lineTo(gp.sx, gp.sy);
      }
      ctx.stroke();
    }

    // Bent light rays
    for (var ryi = 0; ryi < allRays.length; ryi++) {
      var ray = allRays[ryi];
      var rc = ray.cfg;
      ctx.strokeStyle = 'rgba('+rc.r+','+rc.g+','+rc.b+','+rc.op+')';
      ctx.lineWidth = rc.lw;
      ctx.beginPath();
      for (var pi = 0; pi < ray.pts.length; pi++) {
        var rp = proj(ray.pts[pi][0], ray.pts[pi][1], ray.pts[pi][2]);
        if (pi===0) ctx.moveTo(rp.sx, rp.sy); else ctx.lineTo(rp.sx, rp.sy);
      }
      ctx.stroke();
    }

    // Photons (moving light particles)
    for (var phi2 = 0; phi2 < photons.length; phi2++) {
      var ph = photons[phi2];
      ph.t = (ph.t + 0.0042) % 1;
      var idx  = Math.min(Math.floor(ph.t * 52), 51);
      var frac = ph.t*52 - idx;
      var p0 = ph.ray.pts[idx];
      var p1 = ph.ray.pts[Math.min(idx+1, 52)];
      var wx = p0[0]+(p1[0]-p0[0])*frac;
      var wy = p0[1]+(p1[1]-p0[1])*frac;
      var wz = p0[2]+(p1[2]-p0[2])*frac;
      var boost = Math.max(0, 1 - Math.sqrt(wx*wx+wy*wy+wz*wz)/170);
      var pp = proj(wx, wy, wz);
      var pr = Math.max(1, (2.2 + boost*3.5)*Math.min(1.6, pp.s*2.5));
      ctx.save();
      ctx.shadowColor='#fff'; ctx.shadowBlur = 7 + boost*14;
      ctx.beginPath(); ctx.arc(pp.sx, pp.sy, pr, 0, Math.PI*2);
      ctx.fillStyle = 'rgba(255,255,255,' + (0.5+boost*0.5) + ')'; ctx.fill();
      ctx.restore();
    }

    // Gravitational lens galaxy (center)
    var pL = proj(0, 0, 0);
    var lR = Math.max(5, LENS_R * pL.s * 1.1);
    var glowSizes = [lR*6, lR*3.5, lR*2];
    var glowAlphas = [0.055, 0.10, 0.18];
    for (var gli2 = 0; gli2 < 3; gli2++) {
      var grd = ctx.createRadialGradient(pL.sx,pL.sy,0,pL.sx,pL.sy,glowSizes[gli2]);
      grd.addColorStop(0, 'rgba(110,110,255,'+glowAlphas[gli2]+')');
      grd.addColorStop(1, 'rgba(50,50,200,0)');
      ctx.beginPath(); ctx.arc(pL.sx,pL.sy,glowSizes[gli2],0,Math.PI*2);
      ctx.fillStyle=grd; ctx.fill();
    }
    ctx.save();
    ctx.shadowColor='rgba(180,180,255,0.7)'; ctx.shadowBlur=22;
    var lGrd = ctx.createRadialGradient(pL.sx-lR*0.3,pL.sy-lR*0.3,0,pL.sx,pL.sy,lR);
    lGrd.addColorStop(0,'#ffffff'); lGrd.addColorStop(1,'#c7d2fe');
    ctx.beginPath(); ctx.arc(pL.sx,pL.sy,lR,0,Math.PI*2);
    ctx.fillStyle=lGrd; ctx.fill(); ctx.restore();

    // Source quasar
    var pS = proj(SRC_X, 0, 0);
    var sR = Math.max(4, 11*pS.s*1.1);
    var pls = 1 + 0.08*Math.sin(ft*0.055);
    ctx.save();
    ctx.shadowColor='#ffd700'; ctx.shadowBlur=28;
    var sGrd = ctx.createRadialGradient(pS.sx,pS.sy,0,pS.sx,pS.sy,sR*3.2*pls);
    sGrd.addColorStop(0,'rgba(251,191,36,0.32)'); sGrd.addColorStop(1,'rgba(251,191,36,0)');
    ctx.beginPath(); ctx.arc(pS.sx,pS.sy,sR*3.2*pls,0,Math.PI*2); ctx.fillStyle=sGrd; ctx.fill();
    ctx.beginPath(); ctx.arc(pS.sx,pS.sy,sR*pls,0,Math.PI*2); ctx.fillStyle='#fbbf24'; ctx.fill();
    ctx.restore();

    // Observer (Earth)
    var pO = proj(OBS_X, 0, 0);
    var oR = Math.max(4, 13*pO.s*1.1);
    ctx.save();
    ctx.shadowColor='#60a5fa'; ctx.shadowBlur=20;
    var oGrd = ctx.createRadialGradient(pO.sx-oR*0.3,pO.sy-oR*0.3,0,pO.sx,pO.sy,oR);
    oGrd.addColorStop(0,'#93c5fd'); oGrd.addColorStop(1,'#1e40af');
    ctx.beginPath(); ctx.arc(pO.sx,pO.sy,oR,0,Math.PI*2); ctx.fillStyle=oGrd; ctx.fill();
    ctx.restore();

    // Labels
    ctx.font = 'bold 12px "Malgun Gothic","Noto Sans KR",sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle='#fbbf24'; ctx.fillText('실제 광원 (케이사)', pS.sx, pS.sy - sR*pls - 10);
    ctx.fillStyle='#a5b4fc'; ctx.fillText('중력 렌즈 (중심 은하단)', pL.sx, pL.sy + lR + 18);
    ctx.fillStyle='#60a5fa'; ctx.fillText('지구 (관측자)', pO.sx, pO.sy - oR - 10);

    drawInset(ft);
    requestAnimationFrame(render);
  }

  render();
})();
</script>
"""

DISK_HTML = """
<div id="root"></div>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

const STARS = Array.from({length:120},(_,i)=>{
    const s=(n)=>{let x=Math.sin(n)*43758.54;return x-Math.floor(x);};
    return { x:s(i*1.1), y:s(i*2.3), r:s(i*3.2)*1.2+0.1, ph:s(i*5)*Math.PI*2 };
});
const drawStars = (ctx, W, H, t) => {
    STARS.forEach(st=>{
        const op = 0.15 + 0.35*Math.sin(st.ph+t*0.001);
        ctx.beginPath(); ctx.arc(st.x*W, st.y*H, st.r, 0, Math.PI*2);
        ctx.fillStyle=`rgba(255,255,255,${op})`; ctx.fill();
    });
};

function drawDashboard(ctx, clocks) {
    const sX=20,sY=20,bW=180,bH=160;
    ctx.fillStyle='rgba(15,23,42,0.9)'; ctx.strokeStyle='rgba(99,102,241,0.6)';
    ctx.lineWidth=2; ctx.beginPath(); ctx.rect(sX,sY,bW,bH); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#fff'; ctx.font='bold 14px Inter'; ctx.textAlign='center';
    ctx.fillText('[시계] 시간 흐름 비교', sX+bW/2, sY+25);
    const renderClock=(y,label,time,color)=>{
        ctx.save(); ctx.translate(sX+30,y);
        ctx.beginPath(); ctx.arc(0,0,14,0,Math.PI*2); ctx.strokeStyle=color; ctx.lineWidth=2; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0,0); ctx.rotate(time*0.002); ctx.lineTo(0,-11); ctx.stroke();
        ctx.restore();
        ctx.fillStyle=color; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='left';
        ctx.fillText(label,sX+55,y-5);
        ctx.font='12px monospace'; ctx.fillText(time.toFixed(1),sX+55,y+10);
    };
    renderClock(sY+60,'A (지면/정지)',clocks.A,'#3b82f6');
    renderClock(sY+100,'B (중심/회전)',clocks.B,'#10b981');
    renderClock(sY+140,'C (가장자리)',clocks.C,'#f59e0b');
}

function drawRotatingDisk(ctx, W, H, vel, t, clocks, pov) {
    const cx=W*0.5,cy=H*0.45,r=160;
    const ang=t*0.001*vel;
    drawStars(ctx, W, H, t);
    ctx.save();
    if(pov==='B'){ctx.translate(cx,cy);}
    else if(pov==='C'){ctx.translate(cx,cy);ctx.rotate(-ang);ctx.translate(-r*0.85,0);ctx.translate(cx,cy);}
    else{ctx.translate(cx,cy);ctx.rotate(ang);}
    const grad=ctx.createRadialGradient(0,0,r*0.8,0,0,r);
    grad.addColorStop(0,'rgba(30,41,59,0.9)'); grad.addColorStop(1,'rgba(71,85,105,0.4)');
    ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth=2; ctx.stroke();
    ctx.beginPath(); ctx.arc(0,0,10,0,Math.PI*2); ctx.fillStyle='#10b981'; ctx.fill();
    ctx.beginPath(); ctx.arc(r*0.85,0,10,0,Math.PI*2); ctx.fillStyle='#f59e0b'; ctx.fill();
    ctx.restore();
    if(pov==='A'){ctx.beginPath();ctx.arc(cx-r-60,cy,10,0,Math.PI*2);ctx.fillStyle='#3b82f6';ctx.fill();}
    else{ctx.save();ctx.translate(cx,cy);ctx.rotate(-ang);ctx.beginPath();ctx.arc(-r-60,0,10,0,Math.PI*2);ctx.fillStyle='#3b82f6';ctx.fill();ctx.restore();}
    drawDashboard(ctx, clocks);
}

const Main = () => {
    const canvasRef = React.useRef(null);
    const [t, setT] = React.useState(0);
    const [clocks, setClocks] = React.useState({ A: 0, B: 0, C: 0 });

    React.useEffect(() => {
        let frame;
        const loop = (t_val) => {
            setT(t_val);
            setClocks(prev => {
                const speed = (window.stParams && window.stParams.speed) || 1;
                const discVel = (window.stParams && window.stParams.discVel) || 1;
                const fac = Math.max(0.1, 1 - (discVel * 0.08));
                return { A: prev.A + 0.1*speed, B: prev.B + 0.1*speed, C: prev.C + 0.1*speed*fac };
            });
            frame = requestAnimationFrame(loop);
        };
        frame = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(frame);
    }, []);

    React.useEffect(() => {
        const ctx = canvasRef.current.getContext('2d');
        const W=800, H=500;
        ctx.clearRect(0,0,W,H);
        drawRotatingDisk(ctx, W, H, window.stParams.discVel, t, clocks, window.stParams.pov);
    }, [t, clocks]);

    return (
        <div style={{position:'relative',width:'100%',height:'500px'}}>
            <canvas ref={canvasRef} width={800} height={500}
                style={{width:'100%',height:'500px',borderRadius:'12px',background:'#05070a'}} />
        </div>
    );
};
ReactDOM.render(<Main />, document.getElementById('root'));
</script>
<style>
body { font-family:'Inter','Noto Sans KR',sans-serif; background:transparent; margin:0; padding:0; overflow:hidden; color:#fff; }
</style>
"""

st.sidebar.title("아인슈타인 탐구 메뉴")
mode = st.sidebar.radio("탐구 모드 선택",
                        ["중력 렌즈 탐구 (3D)", "등가 원리 학습", "인터스텔라 스토리"])

render_header_cards()
st.write("---")

if mode == "중력 렌즈 탐구 (3D)":
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.success("**중력 렌즈 현상 탐구 (3D)**")
        case = st.radio("실험 케이스 선택",
                        ["별의 위치 변화 (A/B)", "아인슈타인의 십자가"], index=0)
        mass = st.slider("렌즈 천체(은하단)의 질량", 1.0, 20.0, 5.0, step=0.5)
        st.write("---")
        if case == "별의 위치 변화 (A/B)":
            st.markdown("""
**교과서 탐구 내용**
- 질량이 작을 때 : 별이 원래 위치와 가까운 **B** 부근에 보임.
- 질량이 클 때 : 빛이 더 많이 휘어 별이 더 먼 **A** 위치에 보임.

**3D 조작**
- 왼쪽 드래그 → 시점 회전
- 스크롤 → 줌 인/아웃
""")
        else:
            st.markdown("""
**아인슈타인의 십자가**
- 퀘이사 빛이 중간 은하의 중력으로 4개로 쪼개져 보입니다.
- 우상단 인셋에서 지구 망원경 시야를 확인하세요.

**3D 조작**
- 왼쪽 드래그 → 시점 회전
- 스크롤 → 줌 인/아웃
""")
    with col2:
        case_val = 'shift' if case == "별의 위치 변화 (A/B)" else 'cross'
        components.html(
            "<script>window.stParams = {{ mode:'lensing', case:'{c}', mass:{m} }};</script>".format(
                c=case_val, m=mass)
            + LENSING_3D_HTML,
            height=580
        )

elif mode == "등가 원리 학습":
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.success("**가속도와 중력의 등가성**")
        pov = st.radio("관찰 시점 선택", ["A (지면)", "B (중심)", "C (가장자리)"])
        disc_vel = st.slider("원판 회전 속도 (ω)", 0.5, 10.0, 5.0)
        st.write("---")
        st.markdown("**특징 요약**")
        if "A" in pov:
            st.write("- 정지한 지면에서 회전하는 C의 시간이 느려지는 것을 관찰합니다.")
        elif "B" in pov:
            st.write("- 회전 축에서 주변부가 왜곡되어 보이는 기하학적 효과를 경험합니다.")
        else:
            st.write("- 가속도를 느끼는 C는 자신을 정지했다 생각하나, 관성력이 중력처럼 작용해 시간이 느려집니다.")
    with col2:
        pov_val = pov[0]
        components.html(
            "<script>window.stParams = {{ mode:'disk', pov:'{p}', discVel:{d}, speed:1.0 }};</script>".format(
                p=pov_val, d=disc_vel)
            + DISK_HTML,
            height=520
        )

else:
    st.markdown("### 영화 '인터스텔라'로 배우는 상대성 이론")
    col_img1, col_txt1 = st.columns([1, 1.2])
    with col_img1:
        st.image(img_blackhole, use_container_width=True, caption="블랙홀 가르강튀아")
    with col_txt1:
        st.markdown("""
#### 1. 블랙홀의 중력 렌즈 효과
영화 속 블랙홀 주변의 빛나는 고리는 실제 중력 렌즈 효과를 물리적으로 정확히 계산하여 렌더링한 결과입니다.
빛이 블랙홀을 한 바퀴 돌아 우리에게 오기 때문에 위아래로 고리가 형성됩니다.
""")
    st.write("")
    col_txt2, col_img2 = st.columns([1.2, 1])
    with col_txt2:
        st.markdown("""
#### 2. 밀러 행성에서의 1시간 = 지구의 7년
질량이 무지막지한 블랙홀 주변에서는 시공간 곡률이 극심합니다.
블랙홀에 가까운 밀러 행성에서는 시간이 매우 느리게 흐르며,
이는 등가 원리에 의해 '강한 중력'이 시간을 느리게 만드는 실제 현상입니다.
""")
    with col_img2:
        st.image(img_reunion, use_container_width=True, caption="시간의 상대성이 만든 재회")
    st.info("결론: 아인슈타인의 일반 상대성 이론은 '중력 = 시공간의 휘어짐'임을 증명하며, "
            "이는 중력 렌즈와 시간 지연이라는 놀라운 현상으로 나타납니다.")
