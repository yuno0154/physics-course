import streamlit as st
import pandas as pd
import numpy as np
import json

# 페이지 설정
# st.set_page_config(page_title="포물선 운동 영상 분석 실습", layout="wide") # main_app에서 설정됨

# CSS를 활용한 인쇄 최적화 및 폰트 크기 설정
st.markdown("""
    <style>
    /* 메인 콘텐츠 영역에만 폰트 설정 적용 (사이드바 제외) */
    [data-testid="stAppViewMainContent"] {
        font-size: 12pt !important;
    }
    
    /* 제목 크기 (18pt) */
    [data-testid="stAppViewMainContent"] h1 {
        font-size: 18pt !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* 주요 섹션 제목 (13pt) */
    [data-testid="stAppViewMainContent"] h2, 
    [data-testid="stAppViewMainContent"] h3 {
        font-size: 13pt !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* 질문 및 소제목 (12pt Bold) */
    [data-testid="stAppViewMainContent"] h4, 
    [class*="[data-testid='stAppViewMainContent']"] h5, 
    [class*="[data-testid='stAppViewMainContent']"] h6 {
        font-size: 12pt !important;
        font-weight: bold !important;
    }

    @media print {
        header, [data-testid="stSidebar"], [data-testid="stToolbar"], .stActionButton, [data-testid="stFileUploader"] { display: none !important; }
        .main .block-container { padding: 0 !important; }
        .stMarkdown, .stTable, .stPlotlyChart { page-break-inside: avoid; }
    }
    .answer-box { border: 1px solid #ccc; min-height: 80px; padding: 10px; margin-bottom: 20px; background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

# --- 상단 헤더 섹션 (제목 및 작업 버튼 한 줄 배치) ---
header_col1, header_col2, header_col3, header_col4 = st.columns([3.5, 0.8, 0.8, 0.8])

with header_col1:
    st.markdown("<h2 style='margin:0; padding:0; line-height:1.5;'>📹 [포물선 운동 영상 분석 실습] 보고서</h2>", unsafe_allow_html=True)

with header_col2:
    if st.button("🖨️ 인쇄", key="print_btn", use_container_width=True):
        st.components.v1.html("<script>parent.window.print()</script>", height=0)

with header_col3:
    with st.popover("📥 로드", use_container_width=True):
        uploaded_json = st.file_uploader("JSON 파일 선택", type=["json"], key="load_json", label_visibility="collapsed")
        if uploaded_json:
            try:
                loaded_data = json.load(uploaded_json)
                for k, v in loaded_data.items():
                    st.session_state[k] = v
                st.success("복구 완료!")
                st.rerun()
            except Exception as e:
                st.error(f"오류: {e}")

with header_col4:
    save_keys = ['class_num', 'student_num', 'student_name', 'a1', 'a2', 'a3', 'a4']
    save_dict = {k: st.session_state.get(k, '') for k in save_keys}
    json_save = json.dumps(save_dict, ensure_ascii=False, indent=4)
    
    st.download_button(
        "💾 저장", 
        data=json_save, 
        file_name=f"영상분석_실습_{st.session_state.get('student_name', '무명')}.json", 
        key="save_btn", 
        use_container_width=True
    )

st.divider()

# --- 학생 정보 입력부 ---
st.markdown("### 👤 학생 정보")
info_c1, info_c2, info_c3 = st.columns(3)
with info_c1:
    class_num = st.text_input("반 (Class)", placeholder="예: 3-1", key="class_num")
with info_c2:
    student_num = st.text_input("번호 (Number)", placeholder="예: 01", key="student_num")
with info_c3:
    student_name = st.text_input("성함 (Name)", placeholder="홍길동", key="student_name")

st.divider()

# --- 탐구 기본 정보 ---
st.markdown("### 📝 탐구 개요")
c1, c2 = st.columns(2)
with c1:
    st.info("**탐구 주제**: 운동 분석 프로그램으로 운동 분석")
with c2:
    st.success("**탐구 목표**: 비스듬히 위로 던진 물체의 운동을 분석하고 뉴턴의 운동 법칙으로 설명할 수 있다.")

st.markdown("---")

# --- 준비물 및 과정 ---
st.subheader("🛠️ 준비물 및 탐구 과정")
st.markdown("""
**[준비물]**
- **동영상 분석 프로그램**: [웹 서비스 접속 (https://videoanalysis.app?key=tvavTYNBRc)](https://videoanalysis.app?key=tvavTYNBRc)
- **분석용 영상**: 야구공 또는 농구공의 포물선 운동 영상

**[탐구 과정]**
1. **프로그램 접속**: 상단 링크를 통해 동영상 분석 프로그램에 접속합니다.
2. **영상 재생 및 설정**:
    - 분석할 영상을 프로그램에서 재생시킵니다.
    - 운동 분석을 위해 **클립 설정, 교정막대자 설정, 좌표축 설정, 질점 설정**을 수행합니다.
3. **데이터 추출**: 물체의 위치 변화를 추적하여 데이터와 그래프를 생성합니다.
""")

st.divider()

# --- 탐구 결과 1: 데이터 및 그래프 ---
st.subheader("📊 탐구 결과 1: 데이터 및 그래프 기록")
st.write("동영상 분석 프로그램에서 추출한 데이터 표와 5가지 종류의 그래프를 각각 캡처하여 업로드하세요.")

# 1. 데이터 표 업로드
st.markdown("#### 📋 1. 분석 데이터 표 기록")
data_file = st.file_uploader("데이터 표 이미지 또는 CSV 파일 업로드", type=['png', 'jpg', 'jpeg', 'csv'], key="data_file")

if data_file:
    if data_file.name.lower().endswith('.csv'):
        try:
            df = pd.read_csv(data_file)
            st.dataframe(df, use_container_width=True)
            st.caption("[기록] 분석 데이터 (CSV)")
        except Exception as e:
            st.error(f"CSV 파일을 읽는데 실패했습니다: {e}")
    else:
        st.image(data_file, use_container_width=True, caption="[기록] 분석 데이터 표 이미지")
else:
    st.info("실습 프로그램에서 다운로드한 CSV 파일 또는 캡처한 데이터 표 이미지를 업로드해 주세요.")

st.divider()

# 2. 분석 그래프 기록
st.markdown("#### 📈 2. 분석 그래프 기록")
st.caption("실습 프로그램의 그래프 화면을 캡처하여 업로드해 주세요.")

graph_sections = [
    ("pos", "① 시간-위치 (x-t, y-t) 그래프"),
    ("vel", "② 시간-속도 (vx-t, vy-t) 그래프")
]

for key, label in graph_sections:
    with st.container():
        st.write(f"**{label}**")
        g_img = st.file_uploader(f"{label} 이미지 업로드", type=['png', 'jpg', 'jpeg'], key=f"g_img_{key}", label_visibility="collapsed")
        if g_img:
            st.image(g_img, use_container_width=True, caption=label)
        else:
            st.info(f"{label} 이미지를 업로드해 주세요.")
        st.write("") # 간격 조절

st.divider()

# --- 탐구 결과 2: 분석 결과 질문 ---
st.subheader("🤔 탐구 결과 2: 분석 결과 정리")
st.write("분석 데이터를 바탕으로 다음 질문에 답해 보세요.")

# 질문 및 답변 입력 영역
st.markdown("#### 가. 수평 방향 운동에서 속력은 시간에 따라 어떻게 변하는가?")
a1 = st.text_area("답변 입력 (가)", placeholder="실험 데이터를 통해 관찰한 내용을 적어주세요.", height=100, label_visibility="collapsed", key="a1")

st.markdown("#### 나. 수평 방향 운동이 가와 같이 일어나는 이유는 무엇인가?")
a2 = st.text_area("답변 입력 (나)", placeholder="뉴턴의 운동 법칙을 적용하여 설명하세요.", height=100, label_visibility="collapsed", key="a2")

st.markdown("#### 다. 연직 방향의 운동에서 속력은 시간에 따라 어떻게 변하는가?")
a3 = st.text_area("답변 입력 (다)", placeholder="최고점 도달 전후의 속력 변화를 포함하여 설명하세요.", height=100, label_visibility="collapsed", key="a3")

st.markdown("#### 라. 연직 방향 운동에서 다와 같이 일어나는 이유는 무엇인가?")
a4 = st.text_area("답변 입력 (라)", placeholder="작용하는 힘(알짜힘)의 관점에서 설명하세요.", height=100, label_visibility="collapsed", key="a4")

st.divider()
st.caption("사곡고등학교 물리학 II 시뮬레이션 및 실습 지원 포털 | 본 보고서는 작성 후 상단 인쇄 버튼을 통해 PDF로 저장할 수 있습니다.")
