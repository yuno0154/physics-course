"""
1차시 모둠별 포물선 운동 영상 분석 JSON 제출 목록 (단독 전체화면 페이지)
Streamlit Cloud / 로컬 어디서나 /submission_list_1 경로로 직접 열 수 있습니다.
"""
import os
import json
import streamlit as st
import streamlit.components.v1 as components

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = {"use_container_width": True}


def load_submission_html():
    candidates = [
        os.path.join(HERE, "..", "static", "submission_list_1.html"),
        os.path.join(HERE, "..", "1차시_JSON_제출목록.html"),
        os.path.join(HERE, "1차시_JSON_제출목록.html"),
        os.path.join(os.getcwd(), "1차시_JSON_제출목록.html"),
        os.path.join(HERE, "..", "static", "1차시_JSON_제출목록.html"),
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    return None


st.markdown("""
<div style="background:linear-gradient(135deg, #1B3555 0%, #2A5298 100%);color:#fff;padding:22px 24px;border-radius:12px;margin-bottom:20px;box-shadow:0 4px 14px rgba(0,0,0,0.1);">
  <h2 style="margin:0 0 8px 0;font-size:22px;color:#fff;">📋 1차시 모둠별 포물선 운동 JSON 제출 목록 전체보기</h2>
  <p style="margin:0;font-size:14px;color:#D8E6F5;line-height:1.6;">
    1차시 패들렛에 제출된 A반(14건)·B반(15건) 총 29개 모둠의 데이터 목록입니다.<br>
    아래 목록에서 <b>[JSON ⬇]</b> 버튼을 누르면 권한 오류 없이 즉시 다운로드되며, 상단 불러오기 기능으로 보고서에 즉시 반영할 수 있습니다.
  </p>
</div>
""", unsafe_allow_html=True)

# 1. 보고서 바로가기 및 외부 링크
top_c1, top_c2, top_c3 = st.columns([1.5, 1.2, 1.2])
with top_c1:
    st.page_link("physics_sim/video_analysis_eval.py", label="📹 [수행1] 포물선 운동 보고서로 돌아가기", icon="📹", **FULL)
with top_c2:
    st.link_button("🌐 원본 패들렛 열기 ↗", "https://padlet.com/sgh/padlet-s024ptsns1f0aj91uyqt", **FULL)
with top_c3:
    html_data = load_submission_html()
    if html_data:
        st.download_button(
            "💾 HTML 목록 파일 다운로드",
            data=html_data,
            file_name="1차시_JSON_제출목록.html",
            mime="text/html",
            **FULL,
        )

# 2. 내 모둠 선택해서 보고서로 바로 불러오기 기능
sub_dir = os.path.join(HERE, "..", "static", "submissions_1")
if os.path.isdir(sub_dir):
    files = sorted(os.listdir(sub_dir))
    file_map = {}
    for f in files:
        if f.endswith(".json") and "_" in f:
            wid, rest = f.split("_", 1)
            team_name = rest.replace(".json", "")
            label = f"[{team_name}] (제출 ID: {wid})"
            file_map[label] = os.path.join(sub_dir, f)

    if file_map:
        with st.container(border=True):
            st.markdown("<b>🚀 내 모둠 선택해서 보고서 데이터로 저장하기</b>", unsafe_allow_html=True)
            sc1, sc2 = st.columns([3, 1.4])
            with sc1:
                sel_opt = st.selectbox("불러올 모둠 제출본 선택", list(file_map.keys()), key="fullpage_sub_sel", label_visibility="collapsed")
            with sc2:
                if st.button("⚡ 이 파일로 보고서 불러오기", key="fullpage_load_btn", type="primary", **FULL):
                    try:
                        with open(file_map[sel_opt], "r", encoding="utf-8") as jf:
                            st.session_state["_pending_load"] = json.load(jf)
                        st.success(f"{sel_opt} 데이터를 준비했습니다! 아래 버튼을 눌러 보고서로 이동하세요.")
                        st.page_link("physics_sim/video_analysis_eval.py", label="👉 불러온 데이터로 보고서 작성하러 가기", icon="✍️")
                    except Exception as e:
                        st.error(f"불러오기 실패: {e}")

st.markdown("---")

# 3. 전체 목록 렌더링
if html_data:
    components.html(html_data, height=950, scrolling=True)
else:
    st.error("1차시 제출 목록 파일(1차시_JSON_제출목록.html)을 찾을 수 없습니다.")
