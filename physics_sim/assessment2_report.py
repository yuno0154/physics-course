# -*- coding: utf-8 -*-
"""
[수행평가 2] Ⅰ. 모둠 실험 보고서 — 정상파 공명으로 차내 음속 구하기
2026학년도 2학기 · 2학년 역학과 에너지 · 사곡고등학교

- 평가지 Ⅰ(모둠 실험 보고서, 1차시, 40점)을 화면에서 작성하고 PDF로 받아 패들렛에 제출한다.
- 평가지 Ⅱ(개별 서술형)는 이 페이지에서 다루지 않는다(종이 평가).
- 학생 이름은 화면(세션)과 학생이 받는 파일에만 들어가며, 서버·저장소에는 저장하지 않는다.
- 메뉴 노출 여부는 main_app.py 의 ASSESSMENT2_REPORT_OPEN 값으로 정한다.
교사 코드: .streamlit/secrets.toml 의 teacher_code (없으면 DEFAULT_TEACHER_CODE)
"""
import base64
import io
import json
import os
import re
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape
from zoneinfo import ZoneInfo

import streamlit as st

# ════════════════════════════════════════════════════════════════════
# 0. 설정값 (여기만 고치면 됨)
# ════════════════════════════════════════════════════════════════════
TITLE = "정상파 공명 데이터로 차내 음속 구하기"
COURSE = "2026학년도 2학기 · 2학년 역학과 에너지"
AREA = "탄성파와 소리 원리를 적용한 미래형 모빌리티 음향 역학 및 파동 제어 탐구 (수행평가 2)"
STANDARD = "[12역학03-05] 현악기, 관악기 등에서 소리를 내는 원리를 정상파를 이용하여 설명할 수 있다."
POINTS = 40

# 모둠 보고서 제출 패들렛 (비워 두면 '선생님이 안내합니다'로 표시)
PADLET_SUBMIT_URL = "https://padlet.com/sgh/2-s025ucluu74gvowdee49"
PADLET_SUBMIT_NOTE = "A반·B반 공통 · 자기 반·모둠 칸에 PDF 올리기 · 제목: A반_1모둠_모둠실험보고서_최종"

# 참고 페이지 (앱 안의 url_path 또는 전체 주소)
REF_PAGES = [
    ("🚗 수행평가 2 안내자료", "/assessment2_guide", "평가 방법·실험 절차 연습"),
    ("🎸 정상파와 악기 (3D 공명 실험실)", "/standing_wave_components", "관 속 정상파·공명 시뮬레이션"),
]

DEFAULT_TEACHER_CODE = "sagok-physics"
KST = ZoneInfo("Asia/Seoul")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_REG = os.path.join(HERE, "fonts", "NanumGothic.ttf")
FONT_BOLD = os.path.join(HERE, "fonts", "NanumGothicBold.ttf")
FONT_SYM = os.path.join(HERE, "fonts", "DejaVuSans.ttf")   # λ Δ − Ⅰ ① 등 나눔고딕에 없는 기호용

ROLES = ["음원", "측정", "기록", "계산"]
N_MEMBERS = 4
N_TRIALS = 3          # 기본 회차 수 (모둠이 ➕로 늘릴 수 있음)
MAX_TRIALS = 10
IMG_DIR = os.path.join(HERE, "images", "assessment2")

# 문항 문구 (화면·PDF·Word가 같은 문구를 사용) — 평가지 Ⅰ 원문
SITUATION = ("자율주행차 음향 설계팀은 차량 실내 마이크로 바깥 소리를 분석하고 소음을 제어한다. "
             "이 계산의 기준이 되는 것이 차내 공기에서 소리의 속력이다. "
             "여러분의 모둠은 정상파 공명을 이용하여 이 값을 직접 측정한다.")
STEPS = [
    "준비물: 눈금실린더(메스실린더), OHP 투명 필름, 접착테이프, 자, 온도계, 스마트폰(소리 발생 앱)",
    "투명 필름을 둥글게 말아 원통을 만들어 눈금실린더 안쪽에 끼운다. 실린더 바닥이 막힌 끝, 필름 위 끝이 열린 끝이다.",
    "스마트폰으로 일정한 진동수 f의 소리를 내어 필름 끝에 가까이 둔다. <b>진동수는 1개로 정해</b> 모든 회차에 같은 값을 쓴다.",
    "필름을 끝까지 밀어 넣은 뒤 조금씩 빼면서 소리가 가장 크게 들리는 곳(공명)을 찾고, "
    "바닥에서 필름 끝까지의 높이를 첫 번째 공명 L1, 두 번째 공명 L2로 기록한다. "
    "3회 이상 반복한다(추가 측정은 표의 <b>➕ 회차 추가</b>).",
]
Q = {
    "q2a": "① 두 공기 기둥에 공명할 때 관 속 공기의 정상파(진동 범위)를 그리고, 배와 마디를 표시하시오.",
    "q2b": "② 막힌 끝(눈금실린더 바닥)과 열린 끝(필름 끝)이 각각 배인지 마디인지 쓰고, 그 까닭을 매질(공기) 입자가 진동할 수 있는지로 설명하시오.",
    "q2c": "③ L1, L2를 파장 λ으로 나타내고, λ = 2(L2 − L1)임을 보이시오.",
    "q3a": "① 측정한 평균값으로 소리의 파장과 속력을 구하시오. (식 → 대입 → 결과·단위)",
    "q3b": "② 이론값 v = 331 + 0.6t (m/s, t는 °C)로 실내 온도에서의 음속을 구하고, 측정값과의 오차율(%)을 구하시오.",
    "q4a": "① 측정한 L1을 λ/4의 홀수 배 중 가장 가까운 값 (2n − 1)λ/4와 비교하여 차이(Δ = (2n − 1)λ/4 − L1)를 구하시오. "
           "이 차이가 생기는 까닭을 쓰고, "
           "음속을 L1만으로 구하지 않고 두 공명 위치의 차로 구하면 좋은 까닭을 인과적으로 서술하시오.",
    "q4b": "② 개구단 보정 외에 측정값에 영향을 준 요인을 한 가지 들고, 그 요인이 측정한 음속을 크게 하는지 "
           "작게 하는지 근거와 함께 쓰시오.",
    "q5": "여름철 햇빛을 받은 차량 실내 온도가 35 °C라면 차내 음속은 얼마인가? 같은 관과 같은 진동수로 실험하면 "
          "두 공명 위치 사이의 거리(L2 − L1)는 어떻게 달라지는지 까닭과 함께 쓰시오.",
}
# 식 → 대입 → 결과 칸 (key 접두어, 구할 양)
CALC_ROWS = {
    "c_lam": "파장 λ",
    "c_v": "음속 v (측정값)",
    "c_vth": "이론 음속 v (실내 온도)",
    "c_err": "오차율 (%)",
    "c_delta": "Δ = (2n − 1)λ/4 − L1",
    "c_v35": "35 °C 차내 음속",
}
CALC_STEPS = [("f", "식"), ("s", "값 대입"), ("r", "결과 (단위)")]

SAVE_KEYS = (
    ["cls", "team"]
    + [f"m{i}_{x}" for i in range(N_MEMBERS) for x in ("num", "name", "role")]
    + ["freq", "temp", "n_trials"]
    + [f"L{j}_{i}" for i in range(MAX_TRIALS) for j in (1, 2)]
    + ["draw_img_b64", "draw_img_name", "q2a_txt", "q2b", "q2c"]
    + [f"{k}_{s}" for k in CALC_ROWS for s, _ in CALC_STEPS]
    + ["q4a", "q4b", "q5"]
)

# ════════════════════════════════════════════════════════════════════
# 1. 불러오기 대기 데이터 반영 (위젯 생성 전에 실행)
# ════════════════════════════════════════════════════════════════════
if "_a2_pending" in st.session_state:
    for k, v in st.session_state.pop("_a2_pending").items():
        if k in SAVE_KEYS:
            st.session_state[k] = v
    st.session_state["_a2_loaded"] = True
for k, v in {"draw_img_b64": None, "draw_img_name": None, "a2_exports": None, "n_trials": N_TRIALS}.items():
    st.session_state.setdefault(k, v)

# ════════════════════════════════════════════════════════════════════
# 2. 디자인 (노란 칸 = 학생 작성 영역)
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
:root { --navy:#1F3B5C; --blue:#2E6DA4; --soft:#EEF4FA; --line:#D5DEE8; --stu:#FFF8DC; --stu-line:#E8C766; }
.hero { background: linear-gradient(135deg,#0F3D3E 0%,#2E6DA4 100%); color:#fff; border-radius:14px;
        padding:20px 24px; margin-bottom:6px; }
.hero .k { font-size:13px; opacity:.85; }
.hero h1 { color:#fff !important; font-size:24px !important; margin:4px 0 6px 0 !important; padding:0 !important; }
.hero .m { font-size:13px; opacity:.9; }
.sec { display:flex; align-items:center; gap:10px; margin:26px 0 6px 0; padding-bottom:6px;
       border-bottom:2px solid var(--navy); }
.sec .b { background:var(--navy); color:#fff; border-radius:8px; min-width:30px; height:30px; display:flex;
          align-items:center; justify-content:center; font-weight:700; }
.sec .t { font-size:19px; font-weight:700; color:var(--navy); }
.sec .s { font-size:13px; color:#6B7A8C; margin-left:auto; }
.q { font-weight:600; margin:14px 0 4px 0; line-height:1.55; }
.tip { font-size:13px; color:#5B6B7D; background:#F4F7FA; border-left:3px solid #9DB3C9;
       padding:6px 10px; border-radius:4px; margin:4px 0 8px 0; }
.legend { font-size:13px; color:#5B6B7D; }
.legend .sw { display:inline-block; width:14px; height:14px; border-radius:3px; vertical-align:-2px; margin-right:4px; }
.card-t { font-weight:700; color:var(--navy); font-size:16px; margin-bottom:6px; }
.steps li { margin-bottom:4px; line-height:1.55; }
.score { width:100%; border-collapse:collapse; font-size:14px; }
.score td, .score th { border:1px solid var(--line); padding:6px 8px; vertical-align:top; }
.score th { background:var(--soft); color:var(--navy); text-align:left; white-space:nowrap; }
.pill { display:inline-block; background:var(--soft); color:var(--navy); border-radius:20px; padding:2px 10px;
        font-size:13px; margin:2px 4px 2px 0; border:1px solid var(--line); }
.auto { background:var(--soft); border:1px solid var(--line); border-radius:8px; padding:6px 10px; font-size:14px; }
.auto-label { font-size:12px; color:#2E6DA4; font-weight:600; }
.cellh { font-size:13px; font-weight:700; color:var(--navy); padding-top:8px; }
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
    background: var(--stu) !important; border:1px solid var(--stu-line) !important; color:#222 !important; }
button[kind="primary"] { background:#1F3B5C !important; border-color:#1F3B5C !important; }
.submit-btn { background:#1F3B5C;color:#fff;border-radius:10px;padding:14px;text-align:center;font-weight:700;
              font-size:16px;box-shadow:0 2px 6px rgba(0,0,0,0.15);margin:10px 0 6px; }
.submit-btn .s { font-size:12px;font-weight:normal;color:#B8C9E0;margin-top:5px; }
</style>
""", unsafe_allow_html=True)

_VER = tuple(int(x) for x in re.findall(r"\d+", st.__version__)[:2])
FULL = {"width": "stretch"} if _VER >= (1, 46) else {"use_container_width": True}


def sec(num, title, sub=""):
    st.markdown(f"<div class='sec'><div class='b'>{num}</div><div class='t'>{title}</div>"
                f"<div class='s'>{sub}</div></div>", unsafe_allow_html=True)


def tip(text):
    st.markdown(f"<div class='tip'>💡 {text}</div>", unsafe_allow_html=True)


def qtext(text):
    st.markdown(f"<div class='q'>{text}</div>", unsafe_allow_html=True)


def ss(k, default=""):
    v = st.session_state.get(k, default)
    return default if v is None else v


def num(k):
    """학생이 쓴 숫자 칸을 float로 (쉼표·단위가 섞여도 첫 숫자만)."""
    m = re.search(r"-?\d+(?:\.\d+)?", str(ss(k)).replace(",", "."))
    return float(m.group()) if m else None


def fmt(v, nd=3):
    return "" if v is None else f"{v:.{nd}f}"


def teacher_code():
    try:
        return str(st.secrets["teacher_code"])
    except Exception:
        return DEFAULT_TEACHER_CODE


def now_kst():
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M")


def file_stem():
    stem = f"{ss('cls')}반_{ss('team')}모둠_모둠실험보고서"
    return re.sub(r"[\\/:*?\"<>|\s]+", "_", stem)


def measurements():
    """회차별 L1, L2, L2−L1 과 평균 (앱 자동 계산: 단순 산술만)."""
    rows, s1, s2, sd = [], [], [], []
    for i in range(n_trials()):
        a, b = num(f"L1_{i}"), num(f"L2_{i}")
        dd = (b - a) if a is not None and b is not None else None
        rows.append((a, b, dd))
        if a is not None: s1.append(a)
        if b is not None: s2.append(b)
        if dd is not None: sd.append(dd)
    avg = lambda xs: sum(xs) / len(xs) if xs else None
    return rows, (avg(s1), avg(s2), avg(sd))


def n_trials():
    try:
        return max(1, min(MAX_TRIALS, int(st.session_state.get("n_trials") or N_TRIALS)))
    except (TypeError, ValueError):
        return N_TRIALS


def cb_add_trial():
    st.session_state["n_trials"] = min(MAX_TRIALS, n_trials() + 1)


def cb_del_trial():
    n = n_trials()
    if n > N_TRIALS:
        st.session_state.pop(f"L1_{n - 1}", None)
        st.session_state.pop(f"L2_{n - 1}", None)
        st.session_state["n_trials"] = n - 1


def cb_draw_img():
    f = st.session_state.get("draw_upload")
    if f is not None:
        st.session_state["draw_img_b64"] = base64.b64encode(f.getvalue()).decode()
        st.session_state["draw_img_name"] = f.name
    st.session_state["a2_exports"] = None


def cb_clear_img():
    st.session_state["draw_img_b64"] = None
    st.session_state["draw_img_name"] = None


# ════════════════════════════════════════════════════════════════════
# 3. 화면 — 머리
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class='hero'>
  <div class='k'>{COURSE} · 수행평가 2 · Ⅰ. 모둠 실험 보고서 (1차시 · 실험 · 모둠별 · {POINTS}점)</div>
  <h1>🚗 {TITLE}</h1>
  <div class='m'>평가영역: {AREA}</div>
</div>""", unsafe_allow_html=True)

bar1, bar2, bar3 = st.columns([3.6, 1.0, 1.2])
with bar1:
    st.markdown("<div class='legend'><span class='sw' style='background:#FFF8DC;border:1px solid #E8C766'></span>"
                "노란 칸 = 모둠이 작성하는 곳 &nbsp;&nbsp; <span class='sw' style='background:#EEF4FA;border:1px solid #D5DEE8'>"
                "</span>파란 칸 = 앱이 자동으로 계산하는 곳(차와 평균)</div>", unsafe_allow_html=True)
with bar2:
    payload = {k: st.session_state.get(k) for k in SAVE_KEYS}
    payload["_saved_at"] = now_kst()
    st.download_button("💾 저장", json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8"),
                       file_name=file_stem() + "_작성중.json", mime="application/json", **FULL,
                       help="지금까지 입력한 내용을 파일로 내려받습니다.")
with bar3:
    with st.popover("📂 불러오기", **FULL):
        up = st.file_uploader("저장한 JSON 파일", type=["json"], key="a2_load_json")
        if up is not None and st.button("이 파일로 이어서 작성", **FULL):
            try:
                st.session_state["_a2_pending"] = json.load(up)
                st.rerun()
            except Exception as e:
                st.error(f"파일을 읽을 수 없습니다: {e}")
if st.session_state.pop("_a2_loaded", False):
    st.success("저장한 내용을 불러왔습니다. 이어서 작성하세요.")

# ── 모둠 정보 ──────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("<div class='card-t'>👥 모둠 정보 · 역할</div>", unsafe_allow_html=True)
    h0, h1 = st.columns([1, 1])
    h0.text_input("수강반", key="cls", placeholder="예: A")
    h1.text_input("모둠", key="team", placeholder="예: 1")
    for i in range(N_MEMBERS):
        c1, c2, c3 = st.columns([1, 1.4, 1.4])
        c1.text_input(f"반-번호 {i + 1}", key=f"m{i}_num", placeholder="예: 2-3")
        c2.text_input(f"이름 {i + 1}", key=f"m{i}_name")
        if st.session_state.get(f"m{i}_role") not in ROLES:
            st.session_state[f"m{i}_role"] = ROLES[i % len(ROLES)]
        c3.selectbox(f"역할 {i + 1}", ROLES, key=f"m{i}_role")
    tip("모둠 공동 결과물로 채점합니다. 모든 계산에는 <b>식, 값 대입, 결과와 단위</b>를 쓰십시오. "
        "계산기 사용 가능, <b>교과서·AI 도구 사용 불가</b>. "
        "창을 닫아야 할 때는 <b>💾 저장</b>으로 파일을 받아 두고 <b>📂 불러오기</b>로 이어서 작성합니다 "
        "(새로고침하면 입력한 내용이 사라집니다).")

# ── 상황 · 과정 · 평가 안내 ────────────────────────────────────────
g1, g2 = st.columns([1, 1])
with g1:
    with st.container(border=True):
        st.markdown("<div class='card-t'>🚘 상황</div>", unsafe_allow_html=True)
        st.markdown(SITUATION)
        st.markdown(f"<span class='pill'>성취기준 {STANDARD.split(']')[0]}]</span>"
                    "<span class='pill'>눈금실린더 + OHP 필름 공기 기둥</span><span class='pill'>진동수 1개 고정</span>"
                    "<span class='pill'>3회 이상 반복 측정</span>",
                    unsafe_allow_html=True)
with g2:
    with st.container(border=True):
        st.markdown("<div class='card-t'>🧪 실험 과정</div>", unsafe_allow_html=True)
        st.markdown("<div class='steps'><ol>" + "".join(f"<li>{s}</li>" for s in STEPS) +
                    "<li>이 페이지 <b>1~5번</b>을 작성하고, 맨 아래에서 <b>보고서 PDF</b>를 받아 패들렛에 제출한다.</li>"
                    "</ol></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown(f"<div class='card-t'>📋 평가 안내 — 정상파 공명 데이터 분석 및 관 경계 조건 기반 차내 음속 구하기 "
                f"[실험, 모둠별] {POINTS}점</div>", unsafe_allow_html=True)
    st.markdown("""
<table class='score'>
<tr><th>만점(40점) 조건</th><td>
① 관의 경계 조건(막힌 끝 마디, 열린 끝 배)을 매질 입자가 진동할 수 있는지로 설명한다 (2번)<br>
② 정상파로 파장을 유도하고 음속을 <b>식 → 대입 → 결과·단위</b>로 비약 없이 산출한다 (2-③, 3번)<br>
③ 오차가 생긴 물리적 요인(개구단 보정, 실내 온도 등)과 그것이 측정값에 미친 영향을 <b>인과적으로</b> 서술한다 (4번)<br>
※ 한 가지의 개념적 오류나 수식·단위 누락이 없어야 합니다.</td></tr>
<tr><th>점수가 낮아지는 경우</th><td>
• 오차 원인을 단편적으로 언급하거나 나열에 그치면 → 32점<br>
• 계산이 완벽해도 관의 경계 조건에 핵심 오개념이 있으면 → 24점<br>
• 수치 기록 위주로 속력 유도 과정을 전개하지 못하면 → 16점 &nbsp;&nbsp; • 설명이 대폭 누락·미완성 → 8점</td></tr>
<tr><th>참여</th><td>모둠 공동 점수가 원칙이며, 실험 활동에 참여하지 않은 학생은 0점으로 판정합니다.</td></tr>
</table>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# 4. [1] 실험 준비와 측정
# ════════════════════════════════════════════════════════════════════
sec(1, "실험 준비와 측정", "숫자만 입력 · 단위는 표 머리에")
m1, m2 = st.columns([1.5, 1])
with m1:
    e1, e2 = st.columns(2)
    e1.text_input("진동수 f (Hz)", key="freq", placeholder="예: 1150")
    e2.text_input("실내 온도 (°C)", key="temp")
    tip("모둠이 정한 <b>진동수 1개</b>를 모든 회차에 사용합니다. L은 <b>눈금실린더 바닥에서 필름 끝까지의 높이</b>"
        "(공기 기둥 길이)입니다. 짧은 쪽부터 첫 번째 공명 L1, 두 번째 공명 L2입니다. "
        "참고 페이지의 <b>3D 공명 실험실</b>로 측정할 때도 진동수 1개만 정해 사용합니다.")
with m2:
    _res_img = os.path.join(IMG_DIR, "resonance_L1_L2.png")
    if os.path.exists(_res_img):
        st.image(_res_img, caption="공기 기둥 길이 L1, L2 (바닥 → 필름 끝)", **FULL)

hdr = st.columns([0.8, 1, 1, 1])
for c, t in zip(hdr, ["회차", "L1 (m)", "L2 (m)", "L2 − L1 (m)"]):
    c.markdown(f"<div class='cellh'>{t}</div>", unsafe_allow_html=True)
rows, avgs = measurements()
for i in range(n_trials()):
    rc = st.columns([0.8, 1, 1, 1])
    rc[0].markdown(f"<div style='padding-top:8px'>{i + 1}</div>", unsafe_allow_html=True)
    rc[1].text_input(f"L1 {i + 1}회", key=f"L1_{i}", label_visibility="collapsed")
    rc[2].text_input(f"L2 {i + 1}회", key=f"L2_{i}", label_visibility="collapsed")
    rc[3].markdown(f"<div class='auto'>{fmt(rows[i][2]) or '&nbsp;'}</div>", unsafe_allow_html=True)
rc = st.columns([0.8, 1, 1, 1])
rc[0].markdown("<div style='padding-top:6px'><b>평균</b></div>", unsafe_allow_html=True)
for j in range(3):
    rc[j + 1].markdown(f"<div class='auto'>{fmt(avgs[j]) or '&nbsp;'}</div>", unsafe_allow_html=True)
st.markdown("<div class='auto-label'>▣ L2 − L1 과 평균은 입력한 값으로 자동 계산됩니다. "
            "파장·속력 계산은 3번에 모둠이 직접 씁니다.</div>", unsafe_allow_html=True)
tb1, tb2, _ = st.columns([1, 1, 2.5])
tb1.button("➕ 회차 추가", on_click=cb_add_trial, disabled=n_trials() >= MAX_TRIALS, **FULL)
tb2.button("➖ 마지막 회차 삭제", on_click=cb_del_trial, disabled=n_trials() <= N_TRIALS, **FULL)

# ════════════════════════════════════════════════════════════════════
# 5. [2] 관의 경계 조건과 파장
# ════════════════════════════════════════════════════════════════════
sec(2, "관의 경계 조건과 파장")
qtext(Q["q2a"])
st.caption("평가지(종이)의 두 공기 기둥 그림에 정상파를 그리고 배·마디를 표시한 뒤, 사진을 찍어 올립니다.")
_draw_img = os.path.join(IMG_DIR, "draw_template.png")
if os.path.exists(_draw_img):
    st.image(_draw_img, caption="평가지 2-① 그림 (막힌 끝: 눈금실린더 바닥, 열린 끝: 필름 끝)", width=360)
p1, p2 = st.columns([1.3, 1])
with p1:
    st.file_uploader("그림 사진 올리기 (jpg·png)", type=["png", "jpg", "jpeg"], key="draw_upload",
                     on_change=cb_draw_img)
    st.text_area("그림 설명 (선택) — 각 공명에서 배와 마디의 위치", key="q2a_txt", height=90)
with p2:
    if ss("draw_img_b64"):
        st.image(base64.b64decode(ss("draw_img_b64")), caption="올린 그림", **FULL)
        st.button("🗑 사진 지우기", on_click=cb_clear_img)
qtext(Q["q2b"])
st.text_area("2-②", key="q2b", height=120, label_visibility="collapsed")
qtext(Q["q2c"])
st.text_area("2-③", key="q2c", height=120, label_visibility="collapsed")


def calc_block(prefix):
    st.markdown(f"<div class='cellh'>{CALC_ROWS[prefix]}</div>", unsafe_allow_html=True)
    cc = st.columns([1.2, 1.5, 1])
    for c, (s, lab) in zip(cc, CALC_STEPS):
        c.text_input(f"{CALC_ROWS[prefix]} · {lab}", key=f"{prefix}_{s}", placeholder=lab)


# ════════════════════════════════════════════════════════════════════
# 6. [3] 차내 음속 산출
# ════════════════════════════════════════════════════════════════════
sec(3, "차내 음속 산출", "식 → 대입 → 결과·단위")
qtext(Q["q3a"])
calc_block("c_lam")
calc_block("c_v")
qtext(Q["q3b"])
calc_block("c_vth")
calc_block("c_err")

# ════════════════════════════════════════════════════════════════════
# 7. [4] 오차의 물리적 원인 분석
# ════════════════════════════════════════════════════════════════════
sec(4, "오차의 물리적 원인 분석")
qtext(Q["q4a"])
calc_block("c_delta")
st.text_area("4-① 까닭과 두 공명 위치의 차를 쓰는 까닭", key="q4a", height=150)
qtext(Q["q4b"])
st.text_area("4-②", key="q4b", height=130, label_visibility="collapsed")
tip("요인만 쓰지 말고 <b>요인 → 측정값(L, λ, v)에 미친 영향 → 음속이 커지는지/작아지는지</b>를 이어서 씁니다.")

# ════════════════════════════════════════════════════════════════════
# 8. [5] 차내 환경에 적용하기
# ════════════════════════════════════════════════════════════════════
sec(5, "차내 환경에 적용하기")
qtext(Q["q5"])
calc_block("c_v35")
st.text_area("L2 − L1 의 변화와 까닭", key="q5", height=130)

# ════════════════════════════════════════════════════════════════════
# 9. 제출 전 점검
# ════════════════════════════════════════════════════════════════════
def filled(*keys, min_len=1):
    return all(len(str(ss(k)).strip()) >= min_len for k in keys)


def calc_done(prefix):
    return filled(*[f"{prefix}_{s}" for s, _ in CALC_STEPS])


checks = [
    ("모둠 정보", filled("cls", "team", "m0_num", "m0_name")),
    ("1. 진동수·온도", filled("freq", "temp")),
    ("1. 3회 이상 측정값", sum(r[0] is not None and r[1] is not None for r in rows) >= N_TRIALS),
    ("2-① 정상파 그림", bool(ss("draw_img_b64")) or filled("q2a_txt", min_len=10)),
    ("2-②③ 경계 조건·λ 유도", filled("q2b", "q2c", min_len=10)),
    ("3-① 파장·속력", calc_done("c_lam") and calc_done("c_v")),
    ("3-② 이론값·오차율", calc_done("c_vth") and calc_done("c_err")),
    ("4-① Δ·까닭", calc_done("c_delta") and filled("q4a", min_len=10)),
    ("4-② 다른 요인", filled("q4b", min_len=10)),
    ("5. 35 °C 적용", calc_done("c_v35") and filled("q5", min_len=10)),
]
sec("✓", "제출 전 점검 · 보고서 만들기")
done = sum(ok for _, ok in checks)
st.progress(done / len(checks), text=f"작성 완료 {done} / {len(checks)}")
ck = st.columns(4)
for i, (name, ok) in enumerate(checks):
    ck[i % 4].markdown(("✅ " if ok else "⬜ ") + name)
tip("⬜ 표시가 남아 있어도 보고서 파일은 만들 수 있지만, 빈 칸은 보고서에 '(미작성)'으로 표시됩니다.")


# ════════════════════════════════════════════════════════════════════
# 10. 보고서 내용 (PDF·Word 공통 블록)
# ════════════════════════════════════════════════════════════════════
def report_blocks():
    """('h', 번호, 제목) ('q', 문구) ('box', 내용) ('grid', 머리, 행, 학생열, 폭mm) ('img', b64) ('note', 문구)"""
    B = []
    members = [[ss(f"m{i}_num"), ss(f"m{i}_name"), ss(f"m{i}_role")] for i in range(N_MEMBERS)]
    B.append(("grid", ["수강반", "모둠"], [[ss("cls"), ss("team")]], (0, 1), [89, 89]))
    B.append(("grid", ["반-번호", "이름", "역할"], members, (0, 1, 2), [50, 70, 58]))
    B.append(("note", f"[상황] {SITUATION}"))
    B.append(("h", 1, "실험 준비와 측정"))
    B.append(("grid", ["진동수 f (Hz)", "실내 온도 (°C)", "L 측정 기준"],
              [[ss("freq"), ss("temp"), "눈금실린더 바닥 → 필름 끝"]], (0, 1), [50, 50, 78]))
    trow = [[str(i + 1), ss(f"L1_{i}"), ss(f"L2_{i}"), fmt(rows[i][2])] for i in range(n_trials())]
    trow.append(["평균", fmt(avgs[0]), fmt(avgs[1]), fmt(avgs[2])])
    B.append(("grid", ["회차", "L1 (m)", "L2 (m)", "L2 − L1 (m)  ▣자동"], trow, (1, 2), [28, 50, 50, 50]))
    B.append(("h", 2, "관의 경계 조건과 파장"))
    B.append(("q", Q["q2a"]))
    if ss("draw_img_b64"):
        B.append(("img", ss("draw_img_b64")))
    if str(ss("q2a_txt")).strip() or not ss("draw_img_b64"):
        B.append(("box", ss("q2a_txt")))
    B.append(("q", Q["q2b"])); B.append(("box", ss("q2b")))
    B.append(("q", Q["q2c"])); B.append(("box", ss("q2c")))

    def calc(prefixes):
        return ("grid", ["구할 양", "식", "값 대입", "결과 (단위)"],
                [[CALC_ROWS[p]] + [ss(f"{p}_{s}") for s, _ in CALC_STEPS] for p in prefixes],
                (1, 2, 3), [36, 44, 60, 38])

    B.append(("h", 3, "차내 음속 산출"))
    B.append(("q", Q["q3a"])); B.append(calc(["c_lam", "c_v"]))
    B.append(("q", Q["q3b"])); B.append(calc(["c_vth", "c_err"]))
    B.append(("h", 4, "오차의 물리적 원인 분석"))
    B.append(("q", Q["q4a"])); B.append(calc(["c_delta"])); B.append(("box", ss("q4a")))
    B.append(("q", Q["q4b"])); B.append(("box", ss("q4b")))
    B.append(("h", 5, "차내 환경에 적용하기"))
    B.append(("q", Q["q5"])); B.append(calc(["c_v35"])); B.append(("box", ss("q5")))
    B.append(("note", "제출 전 점검: " + "   ".join(("■ " if ok else "□ ") + nm for nm, ok in checks)))
    return B


def footer_text():
    return f"{ss('cls')}반 {ss('team')}모둠  |  수행평가 2 · Ⅰ. 모둠 실험 보고서"


# ── PDF ────────────────────────────────────────────────────────────
def build_pdf(B):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    if "NG" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("NG", FONT_REG))
        pdfmetrics.registerFont(TTFont("NGB", FONT_BOLD if os.path.exists(FONT_BOLD) else FONT_REG))
    NAVY, STU, STU_L, HEAD = (colors.HexColor("#1F3B5C"), colors.HexColor("#FFF8DC"),
                              colors.HexColor("#E0B84A"), colors.HexColor("#E3ECF6"))
    P = lambda size=9.5, bold=False, color="#222222", align=0, lead=None: ParagraphStyle(
        "x", fontName="NGB" if bold else "NG", fontSize=size, leading=lead or size * 1.45,
        textColor=colors.HexColor(color), alignment=align, wordWrap="CJK")
    has_sym = os.path.exists(FONT_SYM)
    if has_sym and "DJ" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("DJ", FONT_SYM))
    ng_map = pdfmetrics.getFont("NG").face.charToGlyph
    dj_map = pdfmetrics.getFont("DJ").face.charToGlyph if has_sym else {}

    def esc(s):
        out = []
        for ch in str(s):
            e = xml_escape(ch)
            if ch == "\n":
                out.append("<br/>")
            elif ord(ch) not in ng_map and ord(ch) in dj_map:
                out.append(f"<font name='DJ'>{e}</font>")
            else:
                out.append(e)
        return "".join(out)
    W = 178 * mm
    el = [Paragraph(esc(COURSE + " · 수행평가 2 · Ⅰ. 모둠 실험 보고서"), P(8.5, False, "#5B6B7D", 1)),
          Paragraph(esc(TITLE), P(15, True, "#1F3B5C", 1, 21)),
          Paragraph(esc(f"성취기준 {STANDARD}"), P(7.5, False, "#5B6B7D", 1)),
          Paragraph(esc(f"평가 요소: 정상파 공명 데이터 분석 및 관 경계 조건 기반 차내 음속 구하기 (실험, 모둠별, {POINTS}점)"
                        f"  ·  보고서 생성 {now_kst()}"), P(7.5, False, "#5B6B7D", 1)),
          Spacer(1, 6)]
    for b in B:
        kind = b[0]
        if kind == "h":
            t = Table([[Paragraph(f"{b[1]}. {esc(b[2])}", P(12, True, "#1F3B5C"))]], colWidths=[W])
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1.2, NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            el.append(t)
        elif kind == "q":
            el += [Spacer(1, 4), Paragraph(esc(b[1]), P(9.5, True)), Spacer(1, 2)]
        elif kind == "note":
            el += [Spacer(1, 4), Paragraph(esc(b[1]), P(8, False, "#5B6B7D"))]
        elif kind == "box":
            body = str(b[1]).strip()
            inner = [Paragraph("[모둠 작성]", P(7, False, "#9A7A1E")),
                     Paragraph(esc(body) if body else "(미작성)", P(9.5, False, "#222222" if body else "#C0392B"))]
            t = Table([[inner]], colWidths=[W])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), STU), ("BOX", (0, 0), (-1, -1), 0.9, STU_L),
                                   ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            el.append(t)
        elif kind == "img":
            try:
                raw = base64.b64decode(b[1])
                iw, ih = ImageReader(io.BytesIO(raw)).getSize()
                w_, h_ = 120 * mm, 120 * mm * ih / iw
                if h_ > 150 * mm:
                    w_, h_ = 150 * mm * iw / ih, 150 * mm
                el.append(Paragraph("[모둠 작성] 정상파 그림 (사진)", P(7, False, "#9A7A1E")))
                el.append(Image(io.BytesIO(raw), width=w_, height=h_))
            except Exception:
                el.append(Paragraph("(그림 사진을 넣지 못했습니다)", P(8, False, "#C0392B")))
        elif kind == "grid":
            headers, rws, stu_cols, widths = b[1], b[2], b[3], b[4]
            data = [[Paragraph(esc(h), P(8.5, True, "#1F3B5C", 1)) for h in headers]]
            for r in rws:
                line = []
                for j, v in enumerate(r):
                    empty = j in stu_cols and not str(v).strip()
                    line.append(Paragraph("(미작성)" if empty else esc(v),
                                          P(8.5, False, "#C0392B" if empty else "#222222", 1)))
                data.append(line)
            t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
            sty = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D2")), ("BACKGROUND", (0, 0), (-1, 0), HEAD),
                   ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
            for j in stu_cols:
                sty.append(("BACKGROUND", (j, 1), (j, -1), STU))
            t.setStyle(TableStyle(sty))
            el += [t, Spacer(1, 3)]

    def footer(cv, doc_):
        cv.saveState(); cv.setFont("NG", 7.5); cv.setFillColor(colors.HexColor("#8A97A6"))
        cv.drawString(16 * mm, 9 * mm, footer_text())
        cv.drawRightString(194 * mm, 9 * mm, f"{doc_.page}쪽")
        cv.restoreState()

    bio = io.BytesIO()
    SimpleDocTemplate(bio, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=14 * mm,
                      bottomMargin=16 * mm, title=TITLE).build(el, onFirstPage=footer, onLaterPages=footer)
    return bio.getvalue()


# ── DOCX ───────────────────────────────────────────────────────────
def build_docx(B):
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Mm, Pt, RGBColor

    doc = Document()
    s0 = doc.sections[0]
    s0.page_width, s0.page_height = Mm(210), Mm(297)
    s0.left_margin = s0.right_margin = Mm(16)
    s0.top_margin = s0.bottom_margin = Mm(14)
    stn = doc.styles["Normal"]
    stn.font.name, stn.font.size = "맑은 고딕", Pt(10)
    stn.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")
    stn.paragraph_format.space_after = Pt(2)

    def shade(cell, hexcolor):
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcolor)
        cell._tc.get_or_add_tcPr().append(shd)

    def run(p, text, bold=False, size=None, color=None):
        r = p.add_run(text)
        r.bold = bold
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = RGBColor.from_string(color)
        return r

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, COURSE + " · 수행평가 2 · Ⅰ. 모둠 실험 보고서", size=8.5, color="5B6B7D")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, TITLE, bold=True, size=15, color="1F3B5C")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, f"평가 요소: 정상파 공명 데이터 분석 및 관 경계 조건 기반 차내 음속 구하기 (실험, 모둠별, {POINTS}점)",
        size=8, color="5B6B7D")
    for b in B:
        kind = b[0]
        if kind == "h":
            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.keep_with_next = True
            run(p, f"{b[1]}. {b[2]}", bold=True, size=12.5, color="1F3B5C")
        elif kind == "q":
            p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.keep_with_next = True
            run(p, b[1], bold=True, size=10)
        elif kind == "note":
            run(doc.add_paragraph(), b[1], size=8, color="5B6B7D")
        elif kind == "box":
            t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"
            c = t.cell(0, 0); shade(c, "FFF8DC")
            run(c.paragraphs[0], "[모둠 작성]", size=7.5, color="9A7A1E")
            body = str(b[1]).strip()
            run(c.add_paragraph(), body or "(미작성)", size=10, color=None if body else "C0392B")
        elif kind == "img":
            try:
                doc.add_picture(io.BytesIO(base64.b64decode(b[1])), width=Mm(110))
            except Exception:
                run(doc.add_paragraph(), "(그림 사진을 넣지 못했습니다)", size=9, color="C0392B")
        elif kind == "grid":
            headers, rws, stu_cols, widths = b[1], b[2], b[3], b[4]
            t = doc.add_table(rows=1 + len(rws), cols=len(headers))
            t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.style = "Table Grid"
            for j, h in enumerate(headers):
                c = t.cell(0, j); c.text = ""
                run(c.paragraphs[0], h, bold=True, size=9, color="1F3B5C"); shade(c, "E3ECF6")
                c.width = Mm(widths[j])
            for i, r in enumerate(rws):
                for j, v in enumerate(r):
                    c = t.cell(i + 1, j); c.text = ""; c.width = Mm(widths[j])
                    empty = j in stu_cols and not str(v).strip()
                    run(c.paragraphs[0], "(미작성)" if empty else str(v), size=9, color="C0392B" if empty else None)
                    if j in stu_cols:
                        shade(c, "FFF8DC")
            doc.add_paragraph()
    fp = s0.footer.paragraphs[0]
    run(fp, footer_text(), size=7.5, color="8A97A6")
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()


# ════════════════════════════════════════════════════════════════════
# 11. 보고서 파일 · 제출
# ════════════════════════════════════════════════════════════════════
with st.container(border=True):
    st.markdown("<div class='card-t'>📤 보고서 파일 만들기와 제출</div>", unsafe_allow_html=True)
    b1, b2 = st.columns([1, 2])
    if b1.button("📄 보고서 파일 만들기", type="primary", **FULL):
        with st.spinner("보고서를 만드는 중입니다…"):
            B = report_blocks()
            out = {"docx": None, "pdf": None, "err": None, "name": file_stem()}
            try:
                out["docx"] = build_docx(B)
            except Exception as e:
                out["err"] = f"Word 파일 오류: {e}"
            if os.path.exists(FONT_REG):
                try:
                    out["pdf"] = build_pdf(B)
                except Exception as e:
                    out["err"] = f"PDF 오류: {e}"
            else:
                out["err"] = "fonts/NanumGothic.ttf 가 없어 PDF를 만들 수 없습니다. (선생님께 알려 주세요)"
            st.session_state["a2_exports"] = out
    b2.markdown("<div class='tip' style='margin-top:4px'>💡 내용을 고친 뒤에는 이 버튼을 <b>다시</b> 눌러야 "
                "고친 내용이 파일에 들어갑니다.</div>", unsafe_allow_html=True)
    ex = st.session_state.get("a2_exports")
    if ex:
        x1, x2 = st.columns(2)
        if ex.get("pdf"):
            x1.download_button("⬇️ PDF 받기 (제출용)", ex["pdf"], file_name=ex["name"] + ".pdf",
                               mime="application/pdf", type="primary", **FULL)
        else:
            x1.warning(ex.get("err") or "PDF를 만들지 못했습니다.")
        if ex.get("docx"):
            x2.download_button("⬇️ Word 받기 (참고용)", ex["docx"], file_name=ex["name"] + ".docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", **FULL)

    st.markdown("""
**제출 방법 (모둠 보고서 제출방 · 패들렛)**
1. 위 버튼으로 **PDF**를 받습니다. 파일 이름은 자동으로 `A반_1모둠_모둠실험보고서.pdf` 형식이 됩니다.
2. 아래 **모둠 보고서 제출방(패들렛)**을 열고 **자기 반·모둠 칸**에 PDF를 올립니다. 게시물 제목: `A반_1모둠_모둠실험보고서_최종`
3. 수정해서 다시 올릴 때는 제목에 ‘재제출’을 표시합니다. 제출 후에도 💾 저장 파일은 지우지 마세요.
""")
    if PADLET_SUBMIT_URL:
        st.markdown(f"""<a href="{PADLET_SUBMIT_URL}" target="_blank" style="text-decoration:none;">
<div class="submit-btn">🚀 [모둠 보고서 제출방 (패들렛)] 새 창에서 열기 ↗
<div class="s">{PADLET_SUBMIT_NOTE}</div></div></a>""", unsafe_allow_html=True)
    else:
        st.info("📌 제출방(패들렛) 링크는 평가 당일 선생님이 안내합니다.")

# ── 참고 페이지 ────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("<div class='card-t'>🔗 참고 페이지</div>", unsafe_allow_html=True)
    rcols = st.columns(len(REF_PAGES))
    for c, (label, url, desc) in zip(rcols, REF_PAGES):
        c.link_button(label + " ↗", url, **FULL)
        c.caption(desc)
    tip("참고 페이지는 새 창으로 열립니다. 이 창은 닫지 마세요(작성한 내용이 사라질 수 있습니다).")

# ════════════════════════════════════════════════════════════════════
# 12. 교사용 확인 (학생 입력값 기준 계산)
# ════════════════════════════════════════════════════════════════════
with st.expander("🔒 교사용 확인"):
    if st.text_input("교사 코드", type="password", key="a2_teacher") == teacher_code():
        f = num("freq")
        t = num("temp")
        L1a, L2a, dLa = avgs
        if f and dLa:
            lam = 2 * dLa
            v = f * lam
            lines = [f"- 사용 진동수 f = **{f:g} Hz** · 평균 L2 − L1 = **{dLa:.4f} m**",
                     f"- λ = 2(L2 − L1) ≈ **{lam:.4f} m** → v = fλ ≈ **{v:.1f} m/s**"]
            if t is not None:
                vth = 331 + 0.6 * t
                lines.append(f"- 이론값 v = 331 + 0.6×{t:g} ≈ **{vth:.1f} m/s** → 오차율 ≈ **{abs(v - vth) / vth * 100:.2f} %**")
            if L1a is not None:
                k = max(1, round((L1a / (lam / 4) + 1) / 2))   # (2n − 1)λ/4 가 L1에 가장 가까운 n
                q = (2 * k - 1) * lam / 4
                lines.append(f"- L1에 가장 가까운 (2n − 1)λ/4: n = {k} → {q:.4f} m, 평균 L1 = {L1a:.4f} m "
                             f"→ Δ ≈ **{q - L1a:.4f} m**")
            v35 = 331 + 0.6 * 35
            lines.append(f"- 35 °C: v = {v35:.1f} m/s → 같은 f에서 L2 − L1 = v/(2f) ≈ **{v35 / (2 * f):.4f} m**")
            st.markdown("\n".join(lines))
        else:
            st.caption("측정 진동수와 L1·L2가 입력되면 기준 계산값이 표시됩니다.")
        st.caption("예시(3D 공명 실험실, 1150 Hz, 20 °C): L1 ≈ 0.367 m, L2 ≈ 0.516 m → λ ≈ 0.299 m, "
                   "v ≈ 343 m/s, Δ = 5λ/4 − L1 ≈ 0.006 m (개구단 보정)")

st.caption("사곡고등학교 역학과 에너지 · 시뮬레이션 및 실습 지원 포털")
