import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """탄성파(2차시) 수업용 시뮬레이션 — 학습지 A~D와 같은 순서의 탭형.
    ① 횡파 → ② 종파 → ③ 파장·진동수·속력(1진동 1파장 순차 진행) → ④ 탄성파의 진행·그래프(y-x, y-t 분석)
    → ⑤ 매질과 속력 → ⑥ 반사(고정단/자유단) → ⑦ 경계: 투과·반사 → ⑧ 초음파 거리 측정 → ⑨ 용수철(슬링키) 영상
    - 기본 재생 속도 0.5배(느리게), 0.1~1.5배 조절 및 일시정지 가능.
    - 외부 CDN 없이 순수 HTML/JS 로 동작합니다. (하단 영상 섹션만 YouTube 접속 필요)
    - 영상은 VIDEOS 목록(HTML 상단)에서 바꿀 수 있고, 시작·끝 구간은 화면에서 지정하면 브라우저에 저장됩니다.
    """
    st.title("🌊 탄성파: 진행 · 속력 · 반사와 투과")
    components.html(HTML, height=1120, scrolling=True)
    video_section()


# ⑧ 용수철(슬링키) 영상 — Streamlit 기본 플레이어(st.video)로 재생
#    (HTML 컴포넌트 안에 넣은 유튜브는 보안 설정 때문에 재생이 막히는 경우가 있어 분리함)
VIDEOS = [
    ("E8KUQCu7UYE", "슬링키로 보는 횡파와 종파 (0.5 m 파장 눈금 표시)"),
    ("DL3Zmi2krdU", "슬링키 종파: 밀한 부분과 소한 부분"),
    ("g8GcMn7K0u4", "슬링키 횡파"),
    ("sRbSQ9wGA1I", "슬링키로 보는 종파와 횡파 (비교)"),
]
# 수업 전에 구간을 정해 두려면 여기에 (시작초, 끝초)를 적는다. 끝 0 = 영상 끝까지
SEGMENTS = {
    "E8KUQCu7UYE": (0, 0),
    "DL3Zmi2krdU": (0, 0),
    "g8GcMn7K0u4": (0, 0),
    "sRbSQ9wGA1I": (0, 0),
}


def video_section():
    st.markdown("---")
    st.subheader("⑨ 용수철(슬링키) 영상: 횡파와 종파 비교 (학습지 A⑤)")
    titles = [t for _, t in VIDEOS]
    k = st.selectbox("영상 선택", range(len(VIDEOS)), format_func=lambda i: titles[i], key="wave_vid")
    vid = VIDEOS[k][0]
    s0, e0 = SEGMENTS.get(vid, (0, 0))
    c1, c2 = st.columns(2)
    start = int(c1.number_input("시작 (초)", min_value=0, value=s0, step=1, key="wave_s_" + vid))
    end = int(c2.number_input("끝 (초, 0 = 끝까지)", min_value=0, value=e0, step=1, key="wave_e_" + vid))
    url = "https://www.youtube.com/watch?v=" + vid
    try:
        if end > start:
            st.video(url, start_time=start, end_time=end, loop=True)
        else:
            st.video(url, start_time=start)
    except TypeError:  # 구버전 Streamlit (end_time/loop 미지원)
        st.video(url, start_time=start)
    st.caption("🐢 느리게 보기: 영상 오른쪽 아래 ⚙(설정) → 재생 속도 → 0.5 또는 0.25 "
               "· 구간을 바꾼 뒤 영상의 ▶를 다시 누르세요.")
    st.markdown(f"[↗ 유튜브에서 열기 (학교망에서 영상이 안 뜰 때)]({url}&t={start}s)")


HTML = r"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
:root{--ink:#0f172a;--sub:#64748b;--line:#e2e8f0;--bg:#f8fafc;--key:#1d4ed8;--bl:#2563eb;--rd:#e11d48;--gr:#059669}
*{box-sizing:border-box}
body{margin:0;font-family:"Pretendard","Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:var(--ink);background:transparent}
#app{max-width:1120px;margin:0 auto;padding:6px 4px 20px}
h1{font-size:20px;margin:4px 0 2px}.lead{font-size:13px;color:var(--sub);margin:0 0 8px}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0 10px}
.tab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font-size:13.5px;font-weight:700;color:var(--sub);cursor:pointer;font-family:inherit}
.tab:hover{border-color:#94a3b8}.tab.on{background:var(--key);border-color:var(--key);color:#fff}
.ctrl{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:16px;padding:8px 14px;margin-bottom:8px}
.grp{display:flex;align-items:center;gap:7px;font-size:13px;font-weight:600}
.ctrl input[type=range]{width:120px}.val{min-width:64px;font-variant-numeric:tabular-nums;color:var(--key);font-weight:800}
.btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:6px 11px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit;color:var(--ink)}
.btn:hover{background:var(--bg)}.btn.on{background:#eff6ff;border-color:#93c5fd;color:#1e3a8a}.btn.primary{background:#0f172a;color:#fff;border-color:#0f172a}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:8px}
canvas{display:block;width:100%;height:auto}
.speed{background:#fffbeb;border-color:#fde68a}
.note{margin-top:8px;background:#f1f5f9;border-radius:14px;padding:9px 14px;font-size:13.5px;line-height:1.6}
.note b{color:var(--key)}.ws{display:inline-block;background:#dbeafe;color:#1e3a8a;border-radius:6px;padding:0 6px;font-size:12px;font-weight:800;margin-right:6px}
.read{margin-left:auto;font-size:13.5px;font-weight:700}.read b{color:var(--key);font-variant-numeric:tabular-nums}
.view{display:none}.show{display:block}
#ytbox{position:relative;width:100%;aspect-ratio:16/9;background:#0f172a;border-radius:14px;overflow:hidden}
#ytbox iframe,#yt{position:absolute;inset:0;width:100%;height:100%}
input[type=number],input[type=text],select{border:1px solid var(--line);border-radius:8px;padding:5px 7px;font-size:13px;font-family:inherit}
input[type=number]{width:72px}
</style></head><body><div id="app">
<h1>🌊 탄성파: 진행 · 속력 · 반사와 투과</h1>
<p class="lead">2차시 학습지 A~D와 순서대로 연결된 시뮬레이션입니다. 기본 재생 속도는 <b>0.5배(느리게)</b>이며 언제든 속도를 바꾸거나 멈출 수 있습니다.</p>
<div class="ctrl speed"><div class="grp">⏱ 재생 속도</div>
<button class="btn" data-sp="0.1">0.1×</button><button class="btn" data-sp="0.25">0.25×</button><button class="btn on" data-sp="0.5">0.5×</button><button class="btn" data-sp="1">1×</button>
<div class="grp"><input type="range" id="spd" min="0.05" max="1.5" step="0.05" value="0.5"><span class="val" id="spdv">0.50×</span></div>
<button class="btn primary" id="pp">⏸ 일시정지</button><button class="btn" id="rs">↺ 처음부터</button></div>
<div class="tabs" id="tabs"></div>

<div id="pCtl" class="ctrl view">
 <div class="grp">진동수 <i>f</i><input type="range" id="sf" min="0.5" max="5" step="0.1" value="1"><span class="val" id="vf"></span></div>
 <div class="grp">파장 <i>λ</i><input type="range" id="sl" min="0.2" max="1.2" step="0.05" value="0.6"><span class="val" id="vl"></span></div>
 <div class="grp">진폭 <i>A</i><input type="range" id="sa" min="1" max="5" step="0.5" value="3"><span class="val" id="va"></span></div>
 <button class="btn" id="ex">예: <i>f</i>=5 Hz, <i>λ</i>=0.4 m</button>
 <label class="grp"><input type="checkbox" id="mk" checked> 표시(마루·밀소·길이)</label>
 <div class="read" id="rd"></div>
</div>
<div id="s3Ctl" class="ctrl view" style="background:#eff6ff;border-color:#bfdbfe">
 <div class="grp" style="color:#1e3a8a">🎯 진행 관찰 모드</div>
 <button class="btn on" id="bSeq">순차 진행 (1진동 → 1파장)</button>
 <button class="btn" id="bCont">연속 파동 보기</button>
 <div class="grp" style="margin-left:6px;color:#1e3a8a">단계별 바로가기:</div>
 <button class="btn" data-q="0"><i>t</i>=0</button>
 <button class="btn" data-q="0.25">¼<i>T</i> (¼<i>λ</i>)</button>
 <button class="btn" data-q="0.5">²⁄₄<i>T</i> (½<i>λ</i>)</button>
 <button class="btn" data-q="0.75">¾<i>T</i> (¾<i>λ</i>)</button>
 <button class="btn on" data-q="1">1<i>T</i> (1파장 <i>λ</i>)</button>
 <button class="btn" data-q="2">2<i>T</i> (2<i>λ</i>)</button>
 <button class="btn" data-q="3">3<i>T</i> (3<i>λ</i>)</button>
 <button class="btn primary" id="bNextQ">⏭ +¼<i>T</i> 한 단계</button>
</div>
<div id="gCtl" class="ctrl view" style="background:#f8fafc;border-color:#cbd5e1">
 <div class="grp">📚 대표 자료</div>
 <button class="btn on" id="gMode1">📘 [자료 1] <i>y–x</i>와 <i>y–t</i> 그래프 분석 (P·Q 진동 방향)</button>
 <button class="btn" id="gMode2">📗 [자료 2] 실선(<i>t</i>=0) → 점선(Δ<i>t</i> 후) 파형 이동과 속력</button>
 <div class="grp" style="margin-left:6px">진행 방향</div>
 <button class="btn on" id="gDirR">오른쪽 (+<i>x</i>) ▶</button>
 <button class="btn" id="gDirL">◀ 왼쪽 (−<i>x</i>)</button>
 <div class="grp" id="gPtGrp" style="margin-left:6px">(나) 그래프 점:
  <button class="btn on" id="gPtP">점 P (<i>x</i>=2m)</button>
  <button class="btn" id="gPtQ">점 Q (<i>x</i>=4m)</button>
  <button class="btn" id="gPtPQ">P·Q 동시 비교</button>
 </div>
 <div class="grp" style="width:100%;margin-top:4px;padding-top:6px;border-top:1px dashed #cbd5e1">
  <span>⏱ 시간 경과 Δ<i>t</i> (점선 파형):</span>
  <button class="btn" data-gq="0"><i>t</i>=0 (실선)</button>
  <button class="btn on" data-gq="0.15">직후 (진동 방향 판별)</button>
  <button class="btn" data-gq="0.25">¼<i>T</i> (¼<i>λ</i> 이동)</button>
  <button class="btn" data-gq="0.5">²⁄₄<i>T</i> (½<i>λ</i> 이동)</button>
  <button class="btn" data-gq="0.75">¾<i>T</i> (¾<i>λ</i> 이동)</button>
  <button class="btn" data-gq="1">1<i>T</i> (1<i>λ</i> 이동)</button>
  <input type="range" id="gDt" min="0" max="1" step="0.01" value="0.15" style="width:130px">
  <span class="val" id="gDtv">0.15 <i>T</i></span>
  <button class="btn primary" id="gAnim">▶ 연속 진행 보기</button>
 </div>
</div>
<div id="mCtl" class="ctrl view">
 <div class="grp">소리의 진동수 <i>f</i><input type="range" id="mf" min="100" max="1000" step="50" value="500"><span class="val" id="mfv"></span></div>
 <div class="read">같은 진동수 → 속력이 클수록 파장이 길어진다 (<i>λ</i> = <i>v</i>/<i>f</i>)</div>
</div>
<div id="rCtl" class="ctrl view">
 <div class="grp">끝의 종류</div><button class="btn on" id="bfix">고정단</button><button class="btn" id="bfree">자유단</button>
 <button class="btn primary" id="rl">▶ 펄스 보내기</button><div class="read" id="rr"></div>
</div>
<div id="bCtl" class="ctrl view">
 <div class="grp">입사 방향</div><button class="btn on" id="b1">가벼운 줄 → 무거운 줄</button><button class="btn" id="b2">무거운 줄 → 가벼운 줄</button>
 <div class="grp">무거운 줄의 질량 비 <input type="range" id="bm" min="2" max="6" step="1" value="4"><span class="val" id="bmv"></span></div>
 <button class="btn primary" id="bl">▶ 펄스 보내기</button><div class="read" id="br"></div>
</div>
<div id="sCtl" class="ctrl view">
 <div class="grp">바다의 깊이 <i>d</i><input type="range" id="sd" min="50" max="500" step="10" value="300"><span class="val" id="sdv"></span></div>
 <div class="grp">초음파 속력 <i>v</i> = 1500 m/s</div><button class="btn primary" id="sl2">▶ 초음파 보내기</button><div class="read" id="sr"></div>
</div>

<div class="card" id="cvcard"><canvas id="cv" width="1000" height="400"></canvas></div>

<div id="vidView" class="view">
 <div class="ctrl"><div class="grp">영상</div><select id="vsel"></select>
  <div class="grp">재생 속도</div><button class="btn" data-vr="0.25">0.25×</button><button class="btn on" data-vr="0.5">0.5×</button><button class="btn" data-vr="1">1×</button>
  <button class="btn primary" id="vgo">▶ 선택 구간 재생</button></div>
 <div class="ctrl"><div class="grp">구간 (초)</div><label class="grp">시작 <input type="number" id="vs" min="0" step="1" value="0"></label><label class="grp">끝 <input type="number" id="ve" min="0" step="1" value="0"></label>
  <button class="btn" id="mkS">현재 위치 → 시작</button><button class="btn" id="mkE">현재 위치 → 끝</button><span style="font-size:12px;color:var(--sub)">끝 = 0 이면 영상 끝까지 · 구간은 이 브라우저에 저장됩니다</span></div>
 <div class="card"><div id="ytbox"><div id="yt"></div></div></div>
 <div class="note" id="vnote"></div>
</div>
<div class="note" id="note"></div>
</div>
<script>
const VIDEOS=[{"id": "E8KUQCu7UYE", "title": "슬링키로 보는 횡파와 종파 (0.5 m 파장 눈금 표시)", "start": 0, "end": 0, "note": "<b>구간 설정 필요:</b> 영상을 보면서 횡파가 나오는 부분 → '현재 위치 → 시작/끝' 버튼으로 구간을 지정하세요."}, {"id": "DL3Zmi2krdU", "title": "슬링키 종파: 밀한 부분과 소한 부분", "start": 0, "end": 0, "note": "종파(밀·소) 설명 영상입니다."}, {"id": "g8GcMn7K0u4", "title": "슬링키 횡파", "start": 0, "end": 0, "note": "횡파 시연 영상입니다."}, {"id": "sRbSQ9wGA1I", "title": "슬링키로 보는 종파와 횡파 (비교)", "start": 0, "end": 0, "note": "두 파동을 한 영상에서 비교합니다."}];
const $=id=>document.getElementById(id);
const cv=$('cv'),ctx=cv.getContext('2d'),W=1000;let H=400;
function setCanvasH(h){if(H!==h){H=h;cv.height=h;}}
const BL='#2563eb',RD='#e11d48',GR='#059669',INK='#0f172a',SUB='#64748b',LN='#cbd5e1',PU='#9333ea',AM='#d97706';
const TABS=[
 ['① 횡파','A②~③ · 입자는 위아래로 진동하고 파동은 옆으로 진행합니다.'],
 ['② 종파','A⑤ · 입자는 진행 방향과 나란히 진동하며 밀한 곳과 소한 곳이 이동합니다.'],
 ['③ 파장·진동수·속력','A②~④ · 파원이 <b>¼<i>T</i> → ²⁄₄<i>T</i> → ¾<i>T</i> → 1<i>T</i>(1회 진동)</b> 진동할 때 파동은 <b>¼<i>λ</i> → ²⁄₄<i>λ</i> → ¾<i>λ</i> → 1<i>λ</i>(한 파장)</b> 진행하므로 <b><i>v</i> = <i>λ</i>/<i>T</i> = <i>fλ</i></b> 입니다.'],
 ['④ 탄성파의 진행·그래프','자료분석 · 실선(<i>t</i>=0)과 점선(<i>t</i>=Δ<i>t</i>)을 비교해 매질(P·Q)의 진동 방향을 찾고, <b>변위–위치(<i>y–x</i>, 파장 <i>λ</i>)</b>와 <b>변위–시간(<i>y–t</i>, 주기 <i>T</i>)</b> 그래프로 속력 <b><i>v</i> = <i>λ</i>/<i>T</i> = Δ<i>x</i>/Δ<i>t</i></b>를 구합니다.'],
 ['⑤ 매질과 속력','B · 진동수는 파원이 정하고, 속력은 매질이 정합니다. 같은 <i>f</i>라도 속력이 큰 매질에서 파장이 깁니다.'],
 ['⑥ 반사','C②~④ · 고정단에서는 펄스가 뒤집혀(위상 반대), 자유단에서는 그대로(위상 변화 없음) 반사됩니다.'],
 ['⑦ 경계: 투과·반사','C⑤ · 느린 매질로 들어가면 반사파가 뒤집히고, 투과파는 속력·파장이 작아지지만 진동수는 같습니다.'],
 ['⑧ 초음파 거리 측정','D① · 파동이 왕복한 거리 <i>v</i>Δ<i>t</i>의 절반이 거리입니다: <b><i>d</i> = <i>v</i>Δ<i>t</i>/2</b>']];
let tab=0,paused=false,speed=0.5,T=0,last=performance.now();
const P={f:1,lam:0.6,A:3,mk:true,seq:true};
const G={mode:1,dir:1,pt:'P',q:0.15,anim:false};
// ---------- UI ----------
TABS.forEach((t,i)=>{const b=document.createElement('button');b.className='tab';b.textContent=t[0];b.onclick=()=>go(i);$('tabs').appendChild(b)});
function setSpeed(v){speed=v;$('spd').value=v;$('spdv').textContent=v.toFixed(2)+'×';document.querySelectorAll('[data-sp]').forEach(b=>b.classList.toggle('on',Math.abs(+b.dataset.sp-v)<1e-6));}
document.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>setSpeed(+b.dataset.sp));
$('spd').oninput=e=>setSpeed(+e.target.value);
function setPaused(p){paused=p;$('pp').textContent=paused?'▶ 재생':'⏸ 일시정지';}
$('pp').onclick=()=>setPaused(!paused);
$('rs').onclick=()=>reset();
function sync(){ $('vf').textContent=P.f.toFixed(1)+' Hz';$('vl').textContent=P.lam.toFixed(2)+' m';$('va').textContent=P.A.toFixed(1)+' cm';
 $('rd').innerHTML='<i>T</i> = <b>'+(1/P.f).toFixed(2)+' s</b> &nbsp; <i>v</i> = <i>fλ</i> = <b>'+(P.f*P.lam).toFixed(2)+' m/s</b>';}
$('sf').oninput=e=>{P.f=+e.target.value;sync()};$('sl').oninput=e=>{P.lam=+e.target.value;sync()};$('sa').oninput=e=>{P.A=+e.target.value;sync()};
$('mk').onchange=e=>P.mk=e.target.checked;
$('ex').onclick=()=>{P.f=5;P.lam=0.4;$('sf').value=5;$('sl').value=0.4;sync();if(tab===2)T=1/P.f;};
$('mf').oninput=()=>{$('mfv').textContent=$('mf').value+' Hz'};

// Tab 3 controls (sequential 1 oscillation -> 1 wavelength)
function syncSeqBtns(){
 const T0=1/P.f,q=T/T0;
 document.querySelectorAll('#s3Ctl [data-q]').forEach(b=>b.classList.toggle('on',Math.abs(+b.dataset.q-q)<0.03));
}
$('bSeq').onclick=()=>{P.seq=true;$('bSeq').classList.add('on');$('bCont').classList.remove('on');T=0;setPaused(false);};
$('bCont').onclick=()=>{P.seq=false;$('bCont').classList.add('on');$('bSeq').classList.remove('on');};
document.querySelectorAll('#s3Ctl [data-q]').forEach(b=>b.onclick=()=>{
 P.seq=true;$('bSeq').classList.add('on');$('bCont').classList.remove('on');
 T=(+b.dataset.q)*(1/P.f);setPaused(true);syncSeqBtns();
});
$('bNextQ').onclick=()=>{
 P.seq=true;$('bSeq').classList.add('on');$('bCont').classList.remove('on');
 const T0=1/P.f,curQ=Math.round((T/T0)*4)/4;
 let nextQ=curQ+0.25;if(nextQ>3.01)nextQ=0.25;
 T=nextQ*T0;setPaused(true);syncSeqBtns();
};

// Tab 4 controls (wave propagation & graph analysis)
function syncGCtl(){
 $('gMode1').classList.toggle('on',G.mode===1);
 $('gMode2').classList.toggle('on',G.mode===2);
 $('gDirR').classList.toggle('on',G.dir===1);
 $('gDirL').classList.toggle('on',G.dir===-1);
 $('gPtGrp').style.display=G.mode===1?'flex':'none';
 $('gPtP').classList.toggle('on',G.pt==='P');
 $('gPtQ').classList.toggle('on',G.pt==='Q');
 $('gPtPQ').classList.toggle('on',G.pt==='PQ');
 $('gDt').value=G.q;
 $('gDtv').innerHTML=G.mode===2?(G.q*4).toFixed(2)+' s ('+G.q.toFixed(2)+' <i>T</i>)':(G.q*0.2).toFixed(3)+' s ('+G.q.toFixed(2)+' <i>T</i>)';
 document.querySelectorAll('#gCtl [data-gq]').forEach(b=>b.classList.toggle('on',Math.abs(+b.dataset.gq-G.q)<0.02));
 $('gAnim').textContent=G.anim?'⏸ 진행 멈추기':'▶ 연속 진행 보기';
}
$('gMode1').onclick=()=>{G.mode=1;G.dir=1;G.q=0.15;G.anim=false;syncGCtl();};
$('gMode2').onclick=()=>{G.mode=2;G.dir=1;G.q=0.25;G.anim=false;syncGCtl();};
$('gDirR').onclick=()=>{G.dir=1;syncGCtl();};
$('gDirL').onclick=()=>{G.dir=-1;syncGCtl();};
$('gPtP').onclick=()=>{G.pt='P';syncGCtl();};
$('gPtQ').onclick=()=>{G.pt='Q';syncGCtl();};
$('gPtPQ').onclick=()=>{G.pt='PQ';syncGCtl();};
document.querySelectorAll('#gCtl [data-gq]').forEach(b=>b.onclick=()=>{G.q=+b.dataset.gq;G.anim=false;syncGCtl();});
$('gDt').oninput=e=>{G.q=+e.target.value;G.anim=false;syncGCtl();};
$('gAnim').onclick=()=>{G.anim=!G.anim;if(G.anim)setPaused(false);syncGCtl();};

function go(i){tab=i;[...$('tabs').children].forEach((b,k)=>b.classList.toggle('on',k===i));
 ['pCtl','s3Ctl','gCtl','mCtl','rCtl','bCtl','sCtl'].forEach(id=>$(id).classList.remove('show'));
 const vid=(i===8);$('cvcard').style.display=vid?'none':'block';$('vidView').classList.toggle('show',vid);
 if(i<=2)$('pCtl').classList.add('show');
 if(i===2)$('s3Ctl').classList.add('show');
 if(i===3){$('gCtl').classList.add('show');syncGCtl();}
 if(i===4)$('mCtl').classList.add('show');
 if(i===5)$('rCtl').classList.add('show');
 if(i===6)$('bCtl').classList.add('show');
 if(i===7)$('sCtl').classList.add('show');
 setCanvasH((i===2||i===3)?500:400);
 $('note').innerHTML='<span class="ws">'+TABS[i][1].split(' · ')[0]+'</span>'+TABS[i][1].split(' · ')[1];
 $('note').style.display=vid?'none':'block';
 reset(); if(vid)initVideo();}
function reset(){T=0;if(tab===5)launch5();if(tab===6)launch6();if(tab===7){sn.t=0;sn.on=false}}
// ---------- drawing helpers ----------
function txt(s,x,y,o){o=o||{};ctx.font=(o.b?'700 ':'500 ')+(o.s||14)+'px "Pretendard","Malgun Gothic",sans-serif';ctx.fillStyle=o.c||INK;ctx.textAlign=o.a||'center';ctx.textBaseline=o.v||'middle';ctx.fillText(s,x,y)}
function rbox(x,y,w,h,r,fill,stroke,sw){ctx.beginPath();ctx.roundRect(x,y,w,h,r||8);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=sw||1;ctx.stroke()}}
function ln(x0,y0,x1,y1,c,w,d){ctx.beginPath();ctx.setLineDash(d||[]);ctx.strokeStyle=c;ctx.lineWidth=w||1;ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();ctx.setLineDash([])}
function head(x,y,dx,dy,c){const a=Math.atan2(dy,dx);ctx.beginPath();ctx.fillStyle=c;ctx.moveTo(x,y);ctx.lineTo(x-9*Math.cos(a-0.4),y-9*Math.sin(a-0.4));ctx.lineTo(x-9*Math.cos(a+0.4),y-9*Math.sin(a+0.4));ctx.fill()}
function dbl(x0,y0,x1,y1,c){ln(x0,y0,x1,y1,c,2);head(x1,y1,x1-x0,y1-y0,c);head(x0,y0,x0-x1,y0-y1,c)}
function arr(x0,y0,x1,y1,c,w){ln(x0,y0,x1,y1,c,w||2.5);head(x1,y1,x1-x0,y1-y0,c)}
function clear(){ctx.clearRect(0,0,W,H)}
const X0=70,X1=930;
// ---------- scenes 1-3: sinusoidal wave ----------
const L3=3,pxm=(X1-X0)/L3,cm2px=14;
function yAt(x,t){return P.A*Math.sin(2*Math.PI*x/P.lam-2*Math.PI*P.f*t)}
function sceneTrans(base,showT,cm2px){
 const n=Math.round(L3/0.05),xh=1.5;
 ln(X0,base,X1,base,LN,1);
 ctx.beginPath();ctx.strokeStyle='#93c5fd';ctx.lineWidth=2;
 for(let i=0;i<=300;i++){const x=L3*i/300,px=X0+x*pxm,py=base-yAt(x,T)*cm2px;i?ctx.lineTo(px,py):ctx.moveTo(px,py)}ctx.stroke();
 ln(X0+xh*pxm,base-P.A*cm2px-8,X0+xh*pxm,base+P.A*cm2px+8,RD,1.2,[3,3]);
 for(let i=0;i<=n;i++){const x=i*0.05,px=X0+x*pxm,py=base-yAt(x,T)*cm2px;const h=Math.abs(x-xh)<1e-6;
  ctx.beginPath();ctx.fillStyle=h?RD:BL;ctx.arc(px,py,h?7:3.6,0,7);ctx.fill();}
 const k=2*Math.PI/P.lam,w=2*Math.PI*P.f;
 if(P.mk){const crests=[];for(let nn=-8;nn<=12;nn++){const x=(Math.PI/2+w*T)/k+nn*P.lam;if(x>=0&&x<=L3)crests.push(x)}
  crests.forEach(x=>{txt('마루',X0+x*pxm,base-P.A*cm2px-22,{c:BL,s:12,b:1});ln(X0+x*pxm,base-P.A*cm2px-12,X0+x*pxm,base-P.A*cm2px-3,BL,1.2)});
  if(crests.length>=2){const a=crests[0],b=crests[1],yy=base-P.A*cm2px-48;dbl(X0+a*pxm,yy,X0+b*pxm,yy,GR);
   txt('파장 λ = '+P.lam.toFixed(2)+' m',X0+(a+b)/2*pxm,yy-12,{c:GR,b:1});
   ln(X0+a*pxm,yy-4,X0+a*pxm,base-P.A*cm2px-24,GR,1,[2,3]);ln(X0+b*pxm,yy-4,X0+b*pxm,base-P.A*cm2px-24,GR,1,[2,3])}
  const xa=0.06;dbl(X0+xa*pxm,base,X0+xa*pxm,base-P.A*cm2px,'#9333ea');txt('A',X0+xa*pxm+14,base-P.A*cm2px/2,{c:'#9333ea',b:1})}
 txt('입자 위·아래 진동',X0+xh*pxm+10,base+P.A*cm2px+20,{c:RD,b:1,s:13,a:'left'});
 arr(X1-190,base+P.A*cm2px+20,X1-40,base+P.A*cm2px+20,BL);txt('파동의 진행 방향',X1-115,base+P.A*cm2px+38,{c:BL,s:13,b:1});
}
function scene1(){clear();txt('횡파: 입자(●)는 제자리에서 위아래로만 움직입니다. 빨간 입자의 점선 경로를 보세요.',W/2,24,{s:15,b:1});sceneTrans(200,false,14)}
function scene2(){clear();txt('종파: 입자는 좌우로 진동하고, 밀한 곳과 소한 곳이 오른쪽으로 이동합니다.',W/2,24,{s:15,b:1});
 const k=2*Math.PI/P.lam,w=2*Math.PI*P.f,ua=Math.min(0.3*P.lam,0.18*P.lam*P.A/3),xh=1.5,base=190;
 ln(X0,base-70,X0,base+70,'#e2e8f0',1);
 for(let i=0;i<=120;i++){const x0=i*0.025,u=ua*Math.sin(k*x0-w*T),px=X0+(x0+u)*pxm,h=Math.abs(x0-xh)<1e-6;
  ln(px,base-(h?70:55),px,base+(h?70:55),h?RD:'#334155',h?4:1.6)}
 const ph=X0+xh*pxm;ln(ph,base+78,ph,base+92,RD,1.5);txt('이 입자의 평형 위치',ph,base+104,{c:RD,s:12,b:1});
 txt('좌우 진동',ph,base-90,{c:RD,s:13,b:1});dbl(ph-30,base-78,ph+30,base-78,RD);
 if(P.mk){const comp=[],rar=[];for(let nn=-8;nn<=12;nn++){const xc=(Math.PI+w*T)/k+nn*P.lam,xr=(w*T)/k+nn*P.lam;if(xc>=0&&xc<=L3)comp.push(xc);if(xr>=0&&xr<=L3)rar.push(xr)}
  comp.forEach(x=>txt('밀',X0+x*pxm,base-82,{c:RD,b:1,s:15}));rar.forEach(x=>txt('소',X0+x*pxm,base-82,{c:BL,b:1,s:15}));
  if(comp.length>=2){const a=comp[0],b=comp[1],yy=base+128;dbl(X0+a*pxm,yy,X0+b*pxm,yy,GR);txt('파장 λ = '+P.lam.toFixed(2)+' m (밀–밀)',X0+(a+b)/2*pxm,yy+16,{c:GR,b:1});
   ln(X0+a*pxm,base+60,X0+a*pxm,yy-4,GR,1,[2,3]);ln(X0+b*pxm,base+60,X0+b*pxm,yy-4,GR,1,[2,3])}}
 arr(X1-190,base+160,X1-40,base+160,BL);txt('파동의 진행 방향',X1-115,base+178,{c:BL,s:13,b:1});}
function scene3(){
 clear();
 const T0=1/P.f,v=P.f*P.lam,k=2*Math.PI/P.lam,w=2*Math.PI*P.f;
 if(!P.seq){
  txt('(가) 한 순간의 파형 (연속 파동)',W-30,18,{b:1,s:14,a:'right'});sceneTrans(145,true,10);
  const gx0=X0+10,gx1=X1-10,gy=360,Tmax=4,tt=T%Tmax,xh=1.5;
  txt('(나) 빨간 입자(x=1.5m)의 위치–시간 그래프',W-30,255,{b:1,s:14,a:'right'});
  ln(gx0,gy,gx1,gy,INK,1.5);ln(gx0,gy-75,gx0,gy+75,INK,1.5);txt('t (s)',gx1,gy+16,{a:'right',s:12});
  for(let s=1;s<=Tmax;s++){const px=gx0+(gx1-gx0)*s/Tmax;ln(px,gy-3,px,gy+3,INK,1);txt(String(s),px,gy+15,{s:11,c:SUB})}
  const sc=(gx1-gx0)/Tmax;
  ctx.beginPath();ctx.strokeStyle=RD;ctx.lineWidth=2.5;let first=true;
  for(let t=0;t<=tt;t+=0.01){const px=gx0+t*sc,py=gy-P.A*Math.sin(k*xh-w*t)*cm2px*0.8*1.4;first?ctx.moveTo(px,py):ctx.lineTo(px,py);first=false}ctx.stroke();
  const py=gy-P.A*Math.sin(k*xh-w*tt)*cm2px*0.8*1.4;ctx.beginPath();ctx.fillStyle=RD;ctx.arc(gx0+tt*sc,py,6,0,7);ctx.fill();
  if(P.mk){let t1=((k*xh-Math.PI/2)/w)%T0;if(t1<0)t1+=T0;
   if(t1+T0<=tt&&t1+T0<=Tmax){const a=gx0+t1*sc,b=gx0+(t1+T0)*sc,yy=gy-P.A*cm2px*0.8*1.4-26;dbl(a,yy,b,yy,GR);txt('주기 T = '+T0.toFixed(2)+' s',(a+b)/2,yy-12,{c:GR,b:1});ln(a,yy-4,a,gy-P.A*cm2px*0.8*1.4,GR,1,[2,3]);ln(b,yy-4,b,gy-P.A*cm2px*0.8*1.4,GR,1,[2,3])}}
  txt('v = λ/T = '+P.lam.toFixed(2)+' ÷ '+T0.toFixed(2)+' = '+v.toFixed(2)+' m/s',W-30,42,{a:'right',c:BL,b:1,s:15});
  return;
 }
 const maxCycles=Math.max(3,Math.min(5,Math.floor(L3/P.lam)));
 const Tmax=maxCycles*T0;
 if(T>Tmax){T=0;}
 syncSeqBtns();
 const q=T/T0;
 const xFront=Math.min(L3,v*T);
 const base=150,scY=11;

 let stepMsg='';
 if(q<0.02) stepMsg='출발 전 (t = 0): 왼쪽 끝 파원(●)이 위(+A)로 진동을 시작하려는 순간입니다.';
 else if(q<=0.26) stepMsg='① 0 → ¼T (¼회 진동): 파원이 평형점(0)에서 마루(+A)까지 올라가는 동안, 파동은 오른쪽으로 ¼파장(¼λ) 진행합니다.';
 else if(q<=0.51) stepMsg='② ¼T → ²⁄₄T (½회 진동): 파원이 마루(+A)에서 평형점(0)으로 내려오는 동안, 파동은 반 파장(½λ) 진행합니다.';
 else if(q<=0.76) stepMsg='③ ²⁄₄T → ¾T (¾회 진동): 파원이 평형점(0)에서 골(−A)까지 내려가는 동안, 파동은 ¾파장(¾λ) 진행합니다.';
 else if(q<=1.02) stepMsg='④ ¾T → 1T (1회 진동 완료!): 파원이 다시 평형점(0)으로 돌아와 1번 진동(1주기 T)을 마치면, 파동은 정확히 한 파장(1λ) 진행합니다!';
 else stepMsg='연속 진동 중 ('+q.toFixed(2)+'T 경과): 파원이 '+q.toFixed(2)+'번 진동하는 동안 파동은 '+q.toFixed(2)+'파장('+(xFront).toFixed(2)+' m) 진행했습니다.';
 rbox(24,8,W-48,32,8,'#eff6ff','#bfdbfe',1);
 txt(stepMsg,W/2,24,{c:'#1e3a8a',b:1,s:13.5});

 txt('(가) 한 순간의 파형 — 파원(x=0)이 진동하며 오른쪽으로 파장이 만들어지는 모습',X0,54,{b:1,s:13.5,a:'left',c:INK});
 txt('v = λ/T = '+P.lam.toFixed(2)+' m ÷ '+T0.toFixed(2)+' s = '+v.toFixed(2)+' m/s',X1,54,{a:'right',c:BL,b:1,s:14});

 const bandCols=['rgba(37,99,235,0.06)','rgba(5,150,105,0.06)','rgba(147,51,234,0.06)','rgba(217,119,6,0.06)'];
 for(let m=0;m<maxCycles;m++){
  const xa=m*P.lam,xb=Math.min(L3,(m+1)*P.lam);
  if(xa>=L3)break;
  const pxa=X0+xa*pxm,pxb=X0+xb*pxm;
  if(xFront>xa){
   const curEnd=X0+Math.min(xb,xFront)*pxm;
   ctx.fillStyle=bandCols[m%bandCols.length];
   ctx.fillRect(pxa,base-P.A*scY-18,curEnd-pxa,2*P.A*scY+36);
  }
  ln(pxb,base-P.A*scY-24,pxb,base+P.A*scY+28,'#cbd5e1',1.2,[4,3]);
  txt((m+1)+'λ ('+((m+1)*P.lam).toFixed(2)+'m)',pxb,base+P.A*scY+40,{c:SUB,s:11,b:1});
  if(m===0){
   [0.25,0.5,0.75].forEach((qq,idx)=>{
    const xq=qq*P.lam,pxq=X0+xq*pxm;
    ln(pxq,base-P.A*scY-12,pxq,base+P.A*scY+14,'#e2e8f0',1,[2,2]);
    txt(['¼λ','²⁄₄λ','¾λ'][idx],pxq,base+P.A*scY+24,{c:'#64748b',s:10.5,b:1});
   });
  }
 }

 ln(X0,base,X1,base,LN,1.5);
 ln(X0,base-P.A*scY-12,X0,base+P.A*scY+12,RD,1.5,[3,3]);

 ctx.beginPath();ctx.strokeStyle='#3b82f6';ctx.lineWidth=3;
 for(let i=0;i<=360;i++){
  const x=L3*i/360,px=X0+x*pxm;
  const y=(x<=xFront+1e-5)?P.A*Math.sin(w*T-k*x):0;
  const py=base-y*scY;
  i?ctx.lineTo(px,py):ctx.moveTo(px,py);
 }
 ctx.stroke();

 const nPts=Math.round(L3/0.05);
 for(let i=0;i<=nPts;i++){
  const x=i*0.05,px=X0+x*pxm;
  const active=(x<=xFront+1e-4);
  const y=active?P.A*Math.sin(w*T-k*x):0;
  const py=base-y*scY;
  const isSource=(i===0);
  ctx.beginPath();
  ctx.fillStyle=isSource?RD:(active?BL:'#94a3b8');
  ctx.arc(px,py,isSource?7.5:(active?3.8:2.8),0,7);
  ctx.fill();
 }
 txt('파원(진동 중심)',X0+8,base-P.A*scY-24,{c:RD,b:1,s:12,a:'left'});

 const pxFront=X0+xFront*pxm;
 if(xFront>0.01){
  ln(pxFront,base-P.A*scY-26,pxFront,base+P.A*scY+16,GR,2,[4,3]);
  ctx.beginPath();ctx.fillStyle=GR;ctx.arc(pxFront,base,5.5,0,7);ctx.fill();
  const yy=base-P.A*scY-34;
  dbl(X0,yy,pxFront,yy,GR);
  txt('진행 거리 x = '+q.toFixed(2)+' λ = '+xFront.toFixed(2)+' m',(X0+pxFront)/2,yy-13,{c:GR,b:1,s:13});
 }
 if(P.mk){
  dbl(X0-22,base,X0-22,base-P.A*scY,PU);
  txt('A',X0-34,base-P.A*scY/2,{c:PU,b:1,s:12});
 }

 const gx0=X0,gx1=X1,gy=380,gH=68;
 txt('(나) 파원(빨간 입자, x=0)의 변위–시간 그래프 (y–t) — 1주기(T) 진동할 때마다 위 파동이 1파장(λ)씩 진행!',X0,268,{b:1,s:13.5,a:'left',c:INK});
 ln(gx0,gy,gx1,gy,INK,1.5);ln(gx0,gy-gH-10,gx0,gy+gH+10,INK,1.5);
 txt('t (s)',gx1,gy+28,{a:'right',s:12,b:1});
 txt('+A',gx0-8,gy-gH,{a:'right',s:11,c:PU,b:1});
 txt('0',gx0-8,gy,{a:'right',s:11,c:SUB});
 txt('−A',gx0-8,gy+gH,{a:'right',s:11,c:PU,b:1});

 const scT=(gx1-gx0)/Tmax;
 for(let m=0;m<maxCycles;m++){
  const ta=m*T0,tb=(m+1)*T0,pxa=gx0+ta*scT,pxb=gx0+tb*scT;
  if(T>ta){
   ctx.fillStyle=bandCols[m%bandCols.length];
   ctx.fillRect(pxa,gy-gH-8,Math.min(pxb,gx0+T*scT)-pxa,2*gH+16);
  }
  ln(pxb,gy-gH-14,pxb,gy+gH+14,'#cbd5e1',1.2,[4,3]);
  txt((m+1)+'T ('+tb.toFixed(2)+'s)',pxb,gy+gH+24,{c:SUB,s:11,b:1});
  if(m===0){
   [0.25,0.5,0.75].forEach((qq,idx)=>{
    const tq=qq*T0,pxq=gx0+tq*scT;
    ln(pxq,gy-gH-6,pxq,gy+gH+6,'#e2e8f0',1,[2,2]);
    txt(['¼T','²⁄₄T','¾T'][idx],pxq,gy+gH+12,{c:'#64748b',s:10.5,b:1});
   });
  }
 }

 ctx.beginPath();ctx.strokeStyle='#fecdd3';ctx.lineWidth=1.8;ctx.setLineDash([4,4]);
 for(let i=0;i<=360;i++){
  const t=Tmax*i/360,px=gx0+t*scT,py=gy-Math.sin(w*t)*gH;
  i?ctx.lineTo(px,py):ctx.moveTo(px,py);
 }
 ctx.stroke();ctx.setLineDash([]);

 ctx.beginPath();ctx.strokeStyle=RD;ctx.lineWidth=3;
 const steps=Math.max(2,Math.round(360*(T/Tmax)));
 for(let i=0;i<=steps;i++){
  const t=T*(i/steps),px=gx0+t*scT,py=gy-Math.sin(w*t)*gH;
  i?ctx.lineTo(px,py):ctx.moveTo(px,py);
 }
 ctx.stroke();

 const curPx=gx0+T*scT,curPy=gy-Math.sin(w*T)*gH;
 ln(curPx,gy-gH-14,curPx,gy+gH+8,RD,1.5,[3,3]);
 ctx.beginPath();ctx.fillStyle=RD;ctx.arc(curPx,curPy,6.5,0,7);ctx.fill();

 if(T>0.01){
  const yy=gy-gH-20;
  dbl(gx0,yy,curPx,yy,RD);
  txt('경과 시간 t = '+q.toFixed(2)+' T = '+T.toFixed(2)+' s',(gx0+curPx)/2,yy-12,{c:RD,b:1,s:13});
 }
}

function sceneProp(){
 clear();
 if(G.anim&&!paused){
  G.q+=0.004*speed;
  if(G.q>1)G.q-=1;
  syncGCtl();
 }
 if(G.mode===1){
  const lam=4,T0=0.2,v=lam/T0,dt=G.q*T0,dx=G.dir*v*dt;
  rbox(20,8,W-40,34,8,'#eff6ff','#bfdbfe',1);
  txt('📘 [대표자료 1] (가) 변위–위치 그래프에서 파장(λ=4m)·진폭(A=1m)을, (나) 변위–시간 그래프에서 주기(T=0.2s)를 구해 속력 v = λ/T = 20 m/s 산출',W/2,25,{c:'#1e3a8a',b:1,s:13.2});

  rbox(20,50,475,310,12,'#ffffff','#e2e8f0',1.5);
  txt('(가) 변위–위치 그래프 (y–x) : 파장 λ = 4 m, 진폭 A = 1 m',257,72,{b:1,s:14,c:INK});
  const lx0=72,lx1=465,ly=205,lW=lx1-lx0,lH=78,xMax=6.5;
  const pxX1=x=>lx0+(x/xMax)*lW;
  const pyY1=y=>ly-y*lH;

  ln(lx0,pyY1(1),lx1,pyY1(1),'#e2e8f0',1,[3,3]);
  ln(lx0,pyY1(-1),lx1,pyY1(-1),'#e2e8f0',1,[3,3]);
  ln(lx0,ly,lx1,ly,INK,1.5);
  ln(lx0,ly-lH-22,lx0,ly+lH+22,INK,1.5);
  txt('변위(m)',lx0-6,ly-lH-28,{a:'center',s:11.5,b:1,c:SUB});
  txt('1',lx0-10,pyY1(1),{a:'right',s:12,b:1});
  txt('0',lx0-10,ly,{a:'right',s:12});
  txt('−1',lx0-10,pyY1(-1),{a:'right',s:12,b:1});
  [2,4,6].forEach(x=>{
   ln(pxX1(x),ly-4,pxX1(x),ly+4,INK,1.2);
   txt(String(x),pxX1(x),ly+18,{s:12,b:1,c:SUB});
  });
  txt('위치(m)',lx1,ly+32,{a:'right',s:12,b:1,c:INK});

  const dirX0=pxX1(1.3),dirX1=pxX1(2.9),dirY=ly-lH-22;
  if(G.dir===1) arr(dirX0,dirY,dirX1,dirY,'#b91c1c',2.5);
  else arr(dirX1,dirY,dirX0,dirY,'#b91c1c',2.5);
  txt('진행 방향 ('+(G.dir===1?'오른쪽 +x':'왼쪽 −x')+')',(dirX0+dirX1)/2,dirY-13,{c:'#b91c1c',b:1,s:12});

  ctx.beginPath();ctx.strokeStyle='#9a3412';ctx.lineWidth=3;
  for(let i=0;i<=260;i++){
   const x=6*i/260,y=Math.sin(2*Math.PI*x/lam);
   i?ctx.lineTo(pxX1(x),pyY1(y)):ctx.moveTo(pxX1(x),pyY1(y));
  }
  ctx.stroke();

  if(G.q>0.005){
   ctx.beginPath();ctx.strokeStyle='#0284c7';ctx.lineWidth=2.5;ctx.setLineDash([5,4]);
   for(let i=0;i<=260;i++){
    const x=6*i/260,y=Math.sin(2*Math.PI*(x-dx)/lam);
    i?ctx.lineTo(pxX1(x),pyY1(y)):ctx.moveTo(pxX1(x),pyY1(y));
   }
   ctx.stroke();ctx.setLineDash([]);
  }

  const yP=Math.sin(2*Math.PI*(2-dx)/lam),yQ=Math.sin(2*Math.PI*(4-dx)/lam);
  const vDirP=G.dir===1?1:-1, vDirQ=G.dir===1?-1:1;
  ln(pxX1(2),ly,pxX1(2),pyY1(yP),RD,2,[2,2]);
  if(Math.abs(yP)>0.08) arr(pxX1(2),ly,pxX1(2),pyY1(yP),RD,3);
  else arr(pxX1(2),ly,pxX1(2),pyY1(vDirP*0.45),RD,2.5);
  ctx.beginPath();ctx.fillStyle='#9a3412';ctx.arc(pxX1(2),ly,4.5,0,7);ctx.fill();
  ctx.beginPath();ctx.fillStyle=RD;ctx.arc(pxX1(2),pyY1(yP),6.5,0,7);ctx.fill();
  txt('P',pxX1(2)+12,ly-12,{c:RD,b:1,s:13.5});

  ln(pxX1(4),ly,pxX1(4),pyY1(yQ),BL,2,[2,2]);
  if(Math.abs(yQ)>0.08) arr(pxX1(4),ly,pxX1(4),pyY1(yQ),BL,3);
  else arr(pxX1(4),ly,pxX1(4),pyY1(vDirQ*0.45),BL,2.5);
  ctx.beginPath();ctx.fillStyle='#9a3412';ctx.arc(pxX1(4),ly,4.5,0,7);ctx.fill();
  ctx.beginPath();ctx.fillStyle=BL;ctx.arc(pxX1(4),pyY1(yQ),6.5,0,7);ctx.fill();
  txt('Q',pxX1(4)-12,ly-12,{c:BL,b:1,s:13.5});

  dbl(pxX1(0),ly+lH+18,pxX1(4),ly+lH+18,GR);
  txt('파장 λ = 4 m',pxX1(2),ly+lH+33,{c:GR,b:1,s:12.5});
  txt('실선: t=0  /  점선: t='+dt.toFixed(3)+'s ('+G.q.toFixed(2)+'T)',257,344,{c:'#0369a1',b:1,s:12.5});

  rbox(505,50,475,310,12,'#ffffff','#e2e8f0',1.5);
  const ptLabel=G.pt==='P'?'점 P (x=2m)':(G.pt==='Q'?'점 Q (x=4m)':'점 P(실선) · 점 Q(점선)');
  txt('(나) 변위–시간 그래프 (y–t) : '+ptLabel+'  [주기 T = 0.2 s]',742,72,{b:1,s:14,c:INK});
  const rx0=558,rx1=950,ry=205,rW=rx1-rx0,rH=78,tMax=0.325;
  const pxT1=t=>rx0+(t/tMax)*rW;
  const pyYt=y=>ry-y*rH;

  ln(rx0,pyYt(1),rx1,pyYt(1),'#e2e8f0',1,[3,3]);
  ln(rx0,pyYt(-1),rx1,pyYt(-1),'#e2e8f0',1,[3,3]);
  ln(rx0,ry,rx1,ry,INK,1.5);
  ln(rx0,ry-rH-22,rx0,ry+rH+22,INK,1.5);
  txt('변위(m)',rx0-6,ry-rH-28,{a:'center',s:11.5,b:1,c:SUB});
  txt('1',rx0-10,pyYt(1),{a:'right',s:12,b:1});
  txt('0',rx0-10,ry,{a:'right',s:12});
  txt('−1',rx0-10,pyYt(-1),{a:'right',s:12,b:1});
  [0.1,0.2,0.3].forEach(t=>{
   ln(pxT1(t),ry-4,pxT1(t),ry+4,INK,1.2);
   txt(t.toFixed(1),pxT1(t),ry+18,{s:12,b:1,c:SUB});
  });
  txt('시간(s)',rx1,ry+32,{a:'right',s:12,b:1,c:INK});

  function drawYtCurve(sign,col,dashed,label){
   ctx.beginPath();ctx.strokeStyle=col;ctx.lineWidth=dashed?2.2:3;ctx.setLineDash(dashed?[5,4]:[]);
   for(let i=0;i<=260;i++){
    const t=0.3*i/260,y=sign*Math.sin(2*Math.PI*t/T0);
    i?ctx.lineTo(pxT1(t),pyYt(y)):ctx.moveTo(pxT1(t),pyYt(y));
   }
   ctx.stroke();ctx.setLineDash([]);
   const curY=sign*Math.sin(2*Math.PI*dt/T0);
   ln(pxT1(dt),ry,pxT1(dt),pyYt(curY),col,1.5,[2,2]);
   ctx.beginPath();ctx.fillStyle=col;ctx.arc(pxT1(dt),pyYt(curY),6.5,0,7);ctx.fill();
   arr(pxT1(0.018),ry,pxT1(0.018),pyYt(sign*0.55),col,2.5);
   txt(label+' (t=0 직후 '+(sign>0?'+':'−')+')',pxT1(0.025)+4,pyYt(sign*0.72),{c:col,b:1,s:12,a:'left'});
  }
  if(G.pt==='P'||G.pt==='PQ') drawYtCurve(vDirP,RD,false,'P');
  if(G.pt==='Q'||G.pt==='PQ') drawYtCurve(vDirQ,BL,G.pt==='PQ','Q');

  dbl(pxT1(0),ry+rH+18,pxT1(0.2),ry+rH+18,GR);
  txt('주기 T = 0.2 s (1회 진동 시간)',pxT1(0.1),ry+rH+33,{c:GR,b:1,s:12.5});
  txt('현재 t = '+dt.toFixed(3)+' s : y_P = '+(yP>=0?'+':'')+yP.toFixed(2)+' m, y_Q = '+(yQ>=0?'+':'')+yQ.toFixed(2)+' m (크기 차 = '+Math.abs(Math.abs(yP)-Math.abs(yQ)).toFixed(2)+' m)',742,344,{c:INK,b:1,s:12});

  rbox(20,370,W-40,120,12,'#fefce8','#fde68a',1.5);
  txt('📝 [대표자료 분석 핵심 풀이]',40,392,{a:'left',b:1,s:13.5,c:'#854d0e'});
  txt('1. 파동의 요소 : (가) 변위–위치 그래프에서 진폭 A = 1 m, 파장 λ = 4 m  |  (나) 변위–시간 그래프에서 주기 T = 0.2 s (진동수 f = 1/T = 5 Hz)',40,415,{a:'left',s:13,c:INK,b:1});
  txt('2. 파동의 속력 : v = 파장(λ) / 주기(T) = 4 m ÷ 0.2 s = 20 m/s',40,437,{a:'left',s:13,c:BL,b:1});
  const pSignTxt=vDirP>0?'(+) 위쪽':'(−) 아래쪽', qSignTxt=vDirQ>0?'(+) 위쪽':'(−) 아래쪽';
  txt('3. 매질의 진동 방향 판별 : (가) 직후 P는 '+pSignTxt+', Q는 '+qSignTxt+'으로 진동 → t=0 직후 변위가 (+)인 그래프는 '+(vDirP>0?'[점 P]':'[점 Q]')+'의 변위–시간 그래프!',40,459,{a:'left',s:13,c:RD,b:1});
  txt('4. t = 0.1초(주기 0.2초의 절반 = T/2)일 때 : 파동이 반 파장(2 m) 이동하므로 P와 Q의 변위는 모두 0 m → 변위의 크기 차 = 0 m',40,480,{a:'left',s:13,c:GR,b:1});
 } else {
  const lam=8,A=10,T0=4,v=lam/T0,dt=G.q*T0,dx=G.dir*v*dt;
  rbox(20,8,W-40,34,8,'#ecfdf5','#a7f3d0',1);
  txt('📗 [대표자료 2 · 서술형 05] 실선(t=0)에서 점선(1초 후 첫 모습)까지 이동한 파장 비율로 주기(T)와 파동의 속력(v) 구하기',W/2,25,{c:'#065f46',b:1,s:13.5});

  rbox(20,50,W-40,295,12,'#ffffff','#e2e8f0',1.5);
  txt('변위–위치 그래프 (y–x) : 실선(t = 0)  →  점선(Δt = '+dt.toFixed(2)+' 초 후, Δx = '+(Math.abs(dx)).toFixed(1)+' cm = '+G.q.toFixed(2)+' λ 이동)',W/2,72,{b:1,s:14.5,c:INK});

  const gx0=90,gx1=920,gy=195,gW=gx1-gx0,gH=78,xMax=18;
  const pxX2=x=>gx0+(x/xMax)*gW;
  const pyY2=y=>gy-(y/A)*gH;

  ln(gx0,pyY2(10),pxX2(16),pyY2(10),'#cbd5e1',1,[3,3]);
  ln(gx0,pyY2(-10),pxX2(16),pyY2(-10),'#cbd5e1',1,[3,3]);
  for(let x=2;x<=16;x+=2){
   ln(pxX2(x),pyY2(10),pxX2(x),pyY2(-10),'#f1f5f9',1);
   ln(pxX2(x),gy-4,pxX2(x),gy+4,INK,1.2);
   txt(String(x),pxX2(x),gy+18,{s:12,b:1,c:SUB});
  }
  ln(gx0,gy,gx1,gy,INK,1.5);
  ln(gx0,gy-gH-22,gx0,gy+gH+22,INK,1.5);
  txt('변위(cm)',gx0-10,gy-gH-28,{s:12,b:1,c:SUB});
  txt('10',gx0-12,pyY2(10),{a:'right',s:12,b:1});
  txt('0',gx0-12,gy,{a:'right',s:12});
  txt('−10',gx0-12,pyY2(-10),{a:'right',s:12,b:1});
  txt('위치(cm)',gx1,gy+26,{a:'right',s:12,b:1,c:INK});

  const d0=pxX2(11.5),d1=pxX2(14.8),dy=gy-gH-22;
  if(G.dir===1) arr(d0,dy,d1,dy,'#b91c1c',2.8);
  else arr(d1,dy,d0,dy,'#b91c1c',2.8);
  txt('진행 방향',(d0+d1)/2,dy-13,{c:'#b91c1c',b:1,s:12.5});

  ctx.beginPath();ctx.strokeStyle='#9a3412';ctx.lineWidth=3.2;
  for(let i=0;i<=320;i++){
   const x=16*i/320,y=A*Math.sin(2*Math.PI*x/lam);
   i?ctx.lineTo(pxX2(x),pyY2(y)):ctx.moveTo(pxX2(x),pyY2(y));
  }
  ctx.stroke();

  ctx.beginPath();ctx.strokeStyle='#dc2626';ctx.lineWidth=2.8;ctx.setLineDash([6,4]);
  for(let i=0;i<=360;i++){
   const x=18*i/360,y=A*Math.sin(2*Math.PI*(x-dx)/lam);
   i?ctx.lineTo(pxX2(x),pyY2(y)):ctx.moveTo(pxX2(x),pyY2(y));
  }
  ctx.stroke();ctx.setLineDash([]);

  const c0=2,c1=2+dx;
  ctx.beginPath();ctx.fillStyle='#9a3412';ctx.arc(pxX2(c0),pyY2(10),5.5,0,7);ctx.fill();
  if(Math.abs(dx)>0.05){
   ctx.beginPath();ctx.fillStyle='#dc2626';ctx.arc(pxX2(c1),pyY2(10),6,0,7);ctx.fill();
   arr(pxX2(c0),pyY2(10)-14,pxX2(c1),pyY2(10)-14,'#dc2626',2.5);
   txt('마루 이동 Δx = '+Math.abs(dx).toFixed(1)+' cm ('+G.q.toFixed(2)+' λ)',pxX2((c0+c1)/2),pyY2(10)-28,{c:'#dc2626',b:1,s:12.5});
  }

  dbl(pxX2(0),gy+gH+28,pxX2(8),gy+gH+28,GR);
  txt('한 파장 λ = 8 cm = 0.08 m (¼λ = 2 cm 마다 1초 소요 → 1파장 8 cm 진행 시간 T = 4초)',pxX2(5.5),gy+gH+45,{c:GR,b:1,s:12.5});

  rbox(20,355,W-40,135,12,'#f0fdf4','#bbf7d0',1.5);
  txt('✍️ [서술형 05 모범 답안 및 단계별 풀이 과정]',40,378,{a:'left',b:1,s:13.5,c:'#166534'});
  txt('① 파장(λ) 구하기 : 실선(t = 0)에서 한 파장의 길이는 λ = 8 cm = 0.08 m 이다.',40,402,{a:'left',s:13,c:INK,b:1});
  txt('② 주기(T) 구하기 : 파동이 ¼파장(2 cm) 진행하여 점선이 되는 데 걸린 시간이 1초이므로, 한 파장(8 cm) 진행하는 데 걸린 시간인 주기는 T = 1초 × 4 = 4 s 이다.',40,425,{a:'left',s:13,c:RD,b:1});
  txt('③ 파동의 속력(v) 구하기 : 파동의 속력 v = 파장(λ) / 주기(T) = 0.08 m ÷ 4 s = 0.02 m/s (= 2 cm/s) 이다.',40,448,{a:'left',s:13.5,c:BL,b:1});
  txt('💡 현재 시뮬레이션 상태 : Δt = '+dt.toFixed(2)+' s 동안 Δx = '+Math.abs(dx).toFixed(2)+' cm ('+G.q.toFixed(2)+' λ) 진행  ⇒  속력 v = Δx / Δt = 2 cm/s = 0.02 m/s',40,472,{a:'left',s:12.5,c:'#065f46',b:1});
 }
}
// ---------- scene 4: media ----------
const MED=[['공기',340,'#0ea5e9'],['물',1500,'#2563eb'],['철',5000,'#64748b']];
function scene4(){clear();const f=+$('mf').value,L=10,pm=(X1-X0)/L;txt('같은 소리(진동수 '+f+' Hz)가 서로 다른 매질에서 진행할 때 — 화면은 실제보다 매우 느리게 재생됩니다',W/2,22,{b:1,s:14});
 MED.forEach((m,i)=>{const lam=m[1]/f,by=100+i*125;ln(X0,by,X1,by,'#e2e8f0',1);
  txt(m[0],34,by,{b:1,s:15,c:m[2]});
  const ph=2*Math.PI*(f/500)*0.5*T;ctx.beginPath();ctx.strokeStyle=m[2];ctx.lineWidth=2.4;
  for(let j=0;j<=500;j++){const x=L*j/500,px=X0+x*pm,py=by-34*Math.sin(2*Math.PI*x/lam-ph);j?ctx.lineTo(px,py):ctx.moveTo(px,py)}ctx.stroke();
  txt('v = '+m[1]+' m/s   λ = v/f = '+lam.toFixed(lam<1?2:1)+' m',W-30,by-50,{a:'right',b:1,s:14,c:m[2]});
  const L1=Math.min(lam,L)*pm;dbl(X0,by+46,X0+L1,by+46,GR);txt('λ',X0+L1/2,by+60,{c:GR,b:1,s:13})});
}
// ---------- scenes 5-6: string FD (domain -7~16 m, visible 0~9 m, absorbers outside view) ----------
const DX=0.015,DT=0.006,XMIN=-7,XMAX=16,N=Math.round((XMAX-XMIN)/DX)+1,QM=0.035;
const xi=i=>XMIN+i*DX,ix=x=>Math.round((x-XMIN)/DX),I9=ix(9);
let ys=new Float64Array(N),yp=new Float64Array(N),cc=new Float64Array(N),sg=new Float64Array(N);let acc=0,st5={free:false},st6={rev:false,m:4},tsim=0,iEnd=N-1;
function g(x,x0){return Math.exp(-Math.pow((x-x0)/0.4,2))}
function setup(cfun,rightSponge){for(let i=0;i<N;i++){const x=xi(i);cc[i]=cfun(x);let q=0;if(x<0)q=QM*Math.pow(-x/7,3);if(rightSponge&&x>9)q=QM*Math.pow((x-9)/7,3);sg[i]=q}}
function pulse(x0,c0){for(let i=0;i<N;i++){const x=xi(i);ys[i]=i<=iEnd?g(x,x0):0;yp[i]=i<=iEnd?g(x+c0*DT,x0):0}acc=0;tsim=0}
function launch5(){iEnd=I9;setup(()=>2,false);pulse(2.0,2)}
function launch6(){const s=Math.sqrt(st6.m);const cl=st6.rev?2/s:2,cr=st6.rev?2:2/s;iEnd=N-1;setup(x=>x<4.5?cl:cr,true);pulse(2.0,cl)}
function stepFD(dts){acc+=dts*2.2;let n=Math.floor(acc/DT);acc-=n*DT;
 while(n-->0){const yn=new Float64Array(N);
  for(let i=1;i<iEnd;i++){const r=cc[i]*DT/DX,q=sg[i];yn[i]=(2*ys[i]-(1-q)*yp[i]+r*r*(ys[i+1]-2*ys[i]+ys[i-1]))/(1+q)}
  if(tab===5&&st5.free){const r=cc[iEnd]*DT/DX;yn[iEnd]=2*ys[iEnd]-yp[iEnd]+r*r*(2*ys[iEnd-1]-2*ys[iEnd])}
  yp=ys;ys=yn;tsim+=DT}}
const pxX=x=>X0+(x/9)*(X1-X0);
function scene5(){clear();txt(st5.free?'(나) 자유단에서의 반사':'(가) 고정단에서의 반사',W/2,24,{b:1,s:16});
 const by=200,sc=95;ln(X0,by,X1,by,'#e2e8f0',1);
 ctx.beginPath();ctx.strokeStyle=BL;ctx.lineWidth=3;let f=true;
 for(let i=ix(0);i<=I9;i++){const xx=pxX(xi(i)),yy=by-ys[i]*sc;f?ctx.moveTo(xx,yy):ctx.lineTo(xx,yy);f=false}ctx.stroke();
 if(!st5.free){ln(X1,by-110,X1,by+110,INK,5);for(let y=by-110;y<by+110;y+=16)ln(X1,y,X1+16,y-12,INK,1.2);}
 else{ln(X1,by-110,X1,by+110,INK,2);ctx.beginPath();ctx.fillStyle='#fff';ctx.strokeStyle=INK;ctx.lineWidth=2;ctx.arc(X1,by-ys[I9]*sc,8,0,7);ctx.fill();ctx.stroke()}
 const pr=pxX(7.2),py=by-ys[ix(7.2)]*sc;ctx.beginPath();ctx.fillStyle=RD;ctx.arc(pr,py,6,0,7);ctx.fill();txt('입자(위아래로만 움직임)',pr,by+130,{c:RD,s:12,b:1});
 const msg=tsim<3.0?'① 입사 펄스(위로 볼록)가 오른쪽 끝을 향해 진행':(tsim<4.0?'② 끝에서 반사되는 중':(tsim<8?(st5.free?'③ 반사 펄스가 그대로(위로 볼록) 돌아옴 → 위상 변화 없음':'③ 반사 펄스가 뒤집혀(아래로 볼록) 돌아옴 → 위상 반대'):'▶ 펄스를 다시 보내 보세요'));
 txt(msg,W/2,370,{c:INK,s:15,b:1});
 $('rr').innerHTML='반사파의 위상: <b>'+(st5.free?'변화 없음':'반대로 바뀜')+'</b>'}
function scene6(){clear();const by=200,sc=95,xb=pxX(4.5);
 const s=Math.sqrt(st6.m),cl=st6.rev?2/s:2,cr=st6.rev?2:2/s,heavyL=st6.rev;
 ctx.fillStyle='#e0f2fe';ctx.fillRect(X0,60,xb-X0,280);ctx.fillStyle='#f1f5f9';ctx.fillRect(xb,60,X1-xb,280);
 ln(xb,60,xb,340,INK,1.5,[6,4]);txt('경계면',xb,50,{b:1,s:13});
 txt((heavyL?'무거운 줄':'가벼운 줄')+' (속력 '+cl.toFixed(2)+')',(X0+xb)/2,352,{c:SUB,b:1,s:13});txt((heavyL?'가벼운 줄':'무거운 줄')+' (속력 '+cr.toFixed(2)+')',(xb+X1)/2,352,{c:SUB,b:1,s:13});
 ln(X0,by,X1,by,'#cbd5e1',1);
 for(let seg=0;seg<2;seg++){ctx.beginPath();ctx.strokeStyle=BL;ctx.lineWidth=((seg===0)===heavyL)?6:2.4;let first=true;
  for(let i=ix(seg?4.5:0);i<=ix(seg?9:4.5);i++){const xx=pxX(xi(i)),yy=by-ys[i]*sc;first?ctx.moveTo(xx,yy):ctx.lineTo(xx,yy);first=false}ctx.stroke()}
 txt('진동수는 두 줄에서 같고, 속력과 파장만 달라집니다. (두꺼운 선 = 무거운 줄)',W/2,24,{b:1,s:15});
 $('br').innerHTML='반사파 위상: <b>'+(cr<cl?'반대로 바뀜':'변화 없음')+'</b> · 투과파 위상: <b>변화 없음</b> · 투과파 속력: <b>'+(cr<cl?'느려짐':'빨라짐')+'</b> · 파장: <b>'+(cr<cl?'짧아짐':'길어짐')+'</b> · 진동수: <b>같음</b>'}
// ---------- scene 7: sonar ----------
const sn={t:0,on:false,done:false};
function scene7(){clear();const d=+$('sd').value,v=1500,dtt=2*d/v;if(sn.on&&!paused){sn.t+=0.016*speed*0.22;if(sn.t>=dtt+0.05){sn.t=dtt;sn.on=false;sn.done=true}}
 const sy=70,by=360,ps=(by-sy-30)*(d/500);const fy=sy+Math.max(60,ps);
 ctx.fillStyle='#dbeafe';ctx.fillRect(0,sy,W,H-sy);ctx.fillStyle='#a8a29e';ctx.beginPath();ctx.moveTo(0,fy);ctx.lineTo(W,fy);ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.fill();
 ln(0,sy,W,sy,BL,2.5);ctx.fillStyle='#475569';ctx.beginPath();ctx.moveTo(180,sy);ctx.lineTo(330,sy);ctx.lineTo(310,sy+22);ctx.lineTo(200,sy+22);ctx.fill();ctx.fillStyle='#e2e8f0';ctx.fillRect(235,sy-26,40,26);
 txt('수면',60,sy-12,{c:BL,b:1});txt('바닥(경계면)',900,fy+20,{b:1,c:'#fff'});
 dbl(780,sy,780,fy,INK);txt('d = '+d+' m',780,(sy+fy)/2,{c:INK,b:1,a:'right',s:15});
 const s=Math.min(v*sn.t,2*d);let y1,y2;
 if(sn.on||sn.done||sn.t>0){if(s<=d){y1=sy+22+s/d*(fy-sy-22);arr(250,sy+22,250,y1,BL);txt('발신',230,(sy+y1)/2,{c:BL,b:1,a:'right'})}
  else{arr(250,sy+22,250,fy,BL);y2=fy-(s-d)/d*(fy-sy-22);arr(300,fy,300,y2,RD);txt('발신',230,(sy+fy)/2,{c:BL,b:1,a:'right'});txt('수신(반사파)',325,(fy+y2)/2,{c:RD,b:1,a:'left'})}}
 txt('경과 시간 Δt = '+(sn.t).toFixed(3)+' s',500,100,{b:1,s:16,c:INK,a:'left'});
 const fin=sn.done||sn.t>=dtt-1e-6&&sn.t>0;
 $('sr').innerHTML=fin?'Δt = <b>'+dtt.toFixed(3)+' s</b> → <i>d</i> = <i>v</i>Δ<i>t</i>/2 = 1500 × '+dtt.toFixed(3)+' ÷ 2 = <b>'+d+' m</b>':'▶ 버튼을 눌러 초음파를 보내 보세요 (실제보다 느리게 재생)';
 txt('초음파가 지나간 거리 = '+Math.round(s)+' m',500,126,{a:'left',c:SUB,b:1,s:14})}
$('sd').oninput=()=>{$('sdv').textContent=$('sd').value+' m';sn.t=0;sn.on=false;sn.done=false};
$('sl2').onclick=()=>{sn.t=0;sn.on=true;sn.done=false};
// ---------- buttons of 5/6 ----------
$('bfix').onclick=()=>{st5.free=false;$('bfix').classList.add('on');$('bfree').classList.remove('on');launch5()};
$('bfree').onclick=()=>{st5.free=true;$('bfree').classList.add('on');$('bfix').classList.remove('on');launch5()};
$('rl').onclick=launch5;
$('b1').onclick=()=>{st6.rev=false;$('b1').classList.add('on');$('b2').classList.remove('on');launch6()};
$('b2').onclick=()=>{st6.rev=true;$('b2').classList.add('on');$('b1').classList.remove('on');launch6()};
$('bm').oninput=()=>{st6.m=+$('bm').value;$('bmv').textContent=st6.m+'배';launch6()};$('bl').onclick=launch6;
// ---------- loop ----------
function frame(now){const dt=Math.min(0.05,(now-last)/1000);last=now;const ds=paused?0:dt*speed;
 if(!paused)T+=ds;
 if(tab===5||tab===6){stepFD(ds)}
 if(tab===0)scene1();else if(tab===1)scene2();else if(tab===2)scene3();else if(tab===3)sceneProp();else if(tab===4)scene4();else if(tab===5)scene5();else if(tab===6)scene6();else if(tab===7)scene7();
 requestAnimationFrame(frame)}
// ---------- video ----------
let player=null,ytReady=false,vrate=0.5,vInit=false;
function key(){return 'wave_seg_'+$('vsel').value}
function loadSeg(){let o={};try{o=JSON.parse(localStorage.getItem(key())||'{}')}catch(e){}
 const v=VIDEOS.find(x=>x.id===$('vsel').value)||{};$('vs').value=(o.s!=null?o.s:v.start||0);$('ve').value=(o.e!=null?o.e:v.end||0);$('vnote').innerHTML=(v.note||'')+' &nbsp;<a href="https://www.youtube.com/watch?v='+$('vsel').value+'&t='+(+$('vs').value)+'s" target="_blank" rel="noopener">↗ 유튜브에서 열기</a> (학교망에서 임베드가 막히면 사용)'}
function saveSeg(){try{localStorage.setItem(key(),JSON.stringify({s:+$('vs').value,e:+$('ve').value}))}catch(e){}}
function playSeg(){saveSeg();if(!player||!ytReady)return;const s=+$('vs').value,e=+$('ve').value;
 const o={videoId:$('vsel').value,startSeconds:s};if(e>s)o.endSeconds=e;player.loadVideoById(o);setTimeout(()=>{try{player.setPlaybackRate(vrate)}catch(x){}},600)}
function initVideo(){if(vInit)return;vInit=true;
 VIDEOS.forEach(v=>{const o=document.createElement('option');o.value=v.id;o.textContent=v.title;$('vsel').appendChild(o)});
 $('vsel').onchange=()=>{loadSeg();playSeg()};loadSeg();
 document.querySelectorAll('[data-vr]').forEach(b=>b.onclick=()=>{vrate=+b.dataset.vr;document.querySelectorAll('[data-vr]').forEach(x=>x.classList.toggle('on',x===b));try{player&&player.setPlaybackRate(vrate)}catch(e){}});
 $('vgo').onclick=playSeg;
 $('mkS').onclick=()=>{if(player)$('vs').value=Math.floor(player.getCurrentTime());saveSeg()};$('mkE').onclick=()=>{if(player)$('ve').value=Math.ceil(player.getCurrentTime());saveSeg()};
 const sc=document.createElement('script');sc.src='https://www.youtube.com/iframe_api';document.head.appendChild(sc);
 window.onYouTubeIframeAPIReady=()=>{player=new YT.Player('yt',{videoId:$('vsel').value,playerVars:{start:+$('vs').value,rel:0,modestbranding:1,playsinline:1},events:{onReady:()=>{ytReady=true;player.setPlaybackRate(vrate)},onStateChange:e=>{if(e.data===1){try{player.setPlaybackRate(vrate)}catch(x){}}}}})};}
setSpeed(0.5);sync();$('mfv').textContent='500 Hz';$('bmv').textContent='4배';$('sdv').textContent='300 m';
go(0);requestAnimationFrame(frame);
</script></body></html>
"""


if __name__ == "__main__":
    run_sim()
