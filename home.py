import streamlit as st
import os
import base64
from pathlib import Path
import streamlit.components.v1 as components

try:
    from streamlit_pdf_viewer import pdf_viewer
    HAS_PDF_VIEWER = True
except ImportError:
    HAS_PDF_VIEWER = False

st.title("🏠 물리학습 지원 포털")

st.markdown("""
안녕하세요! **물리학습 지원 포털**에 오신 것을 환영합니다.

이 포털은 학생들이 물리학의 핵심 개념을 직관적으로 이해하고 탐구할 수 있도록 돕기 위해 제작되었습니다.
좌측의 네비게이션 메뉴를 사용하여 다양한 시뮬레이션과 도구를 탐색해 보세요.
""")

st.markdown("---")
st.subheader("📑 2026학년도 사곡고 2학기 2학년 역학과 에너지 평가계획")

# 1. 평가계획 핵심 요약 슬라이드 (HTML 뷰어)
summary_html_path = Path(__file__).parent / "evaluation_summary.html"

if os.path.exists(summary_html_path):
    with open(summary_html_path, "r", encoding="utf-8") as f:
        summary_html_content = f.read()
    
    st.caption("💡 상단 탭(1~6)을 클릭하시면 평가 개요, 시기·비율, 성취도 기준, 수행평가 ①·② 최고수준 채점기준, 운영 원칙을 바로 확인하실 수 있습니다.")
    components.html(summary_html_content, height=530, scrolling=True)
else:
    st.info("평가계획서 요약 정보를 불러올 수 없습니다.")

# 2. 평가계획서 전문 (PDF 다운로드 및 뷰어)
pdf_file_name = "2026학년도 사곡고 2학기 2학년 역학과 에너지 평가계획서.pdf"
pdf_path = Path(__file__).parent / pdf_file_name

if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="📥 평가계획서 전문(PDF) 다운로드",
            data=pdf_data,
            file_name=pdf_file_name,
            mime="application/pdf",
            use_container_width=True
        )

    with st.expander("📖 평가계획서 전문(PDF) 원본 펼쳐보기", expanded=False):
        if HAS_PDF_VIEWER:
            pdf_viewer(str(pdf_path), width=700)
        else:
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.warning("⚠️ 평가계획서 PDF 파일을 찾을 수 없습니다.")

st.markdown("---")

st.markdown("""
### 📂 학습 자료 및 수행평가 안내
교과 수업 및 수행평가와 관련된 추가 자료는 아래 구글 드라이브에서 확인하실 수 있습니다.

*   **[구글 드라이브 바로가기](https://drive.google.com/drive/folders/1C_LpA1TGeVk6sNhMSYe-azp67Sp1Y0eT?usp=drive_link)**

| 학습 자료실 QR 코드 | 📍 물리학 / 역학과 에너지 수업 자료 |
| :---: | :--- |
| ![DRIVE_QR](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://drive.google.com/drive/folders/1C_LpA1TGeVk6sNhMSYe-azp67Sp1Y0eT?usp=drive_link) | - **벡터의 합성과 분해** <br> - **위치 벡터와 변위 시각화** <br> - **평균 및 순간 속도 탐구** <br> - **포물선(수평/비스듬히) 운동 분석** <br> - **등속 원운동 및 진자의 운동 탐구** <br> - **케플러 법칙과 궤도 역학 분석** <br> - **일반 상대성 이론 및 블랙홀 탐구** <br> - **파동의 중첩과 간섭 / 음향 제어 시뮬레이션** |

제작: 사곡고등학교 물리실
""")
