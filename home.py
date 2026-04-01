import streamlit as st
import os
import base64

st.title("🏠 물리학습 지원 포털")

st.markdown("""
안녕하세요! **물리학습 지원 포털**에 오신 것을 환영합니다.

이 포털은 학생들이 물리학의 핵심 개념을 직관적으로 이해할 수 있도록 돕기 위해 제작되었습니다.
좌측의 네비게이션 메뉴를 사용하여 다양한 시뮬레이션과 도구를 탐색해 보세요.
""")

st.markdown("---")
st.subheader("📑 2026학년도 사곡고 1학기 3학년 물리학Ⅱ 평가계획")

pdf_file_name = "2026학년도 사곡고 1학기 3학년 물리학Ⅱ 평가계획 세부 계획서.pdf"
pdf_path = os.path.join(os.path.dirname(__file__), pdf_file_name)

if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    
    st.download_button(
        label="📥 평가계획 세부 계획서 다운로드",
        data=pdf_data,
        file_name=pdf_file_name,
        mime="application/pdf"
    )

    with st.expander("평가계획 세부 계획서 내용 펼쳐보기"):
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.warning("⚠️ 평가계획 세부 계획서 파일을 찾을 수 없습니다.")

st.markdown("---")

st.markdown("""
### 📂 학습 자료 및 수행평가 안내
교과 수업 및 수행평가와 관련된 추가 자료는 아래 구글 드라이브에서 확인하실 수 있습니다.

*   **[구글 드라이브 바로가기](https://drive.google.com/drive/folders/1C_LpA1TGeVk6sNhMSYe-azp67Sp1Y0eT?usp=drive_link)**

| 학습 자료실 QR 코드 | 📍 제공 기능 요약 |
| :---: | :--- |
| ![DRIVE_QR](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://drive.google.com/drive/folders/1C_LpA1TGeVk6sNhMSYe-azp67Sp1Y0eT?usp=drive_link) | - **위치 벡터와 변위 시각화** <br> - **평균 및 순간 속도 탐구** <br> - **포물선(수평/비스듬히) 운동 분석** <br> - **영상 분석 실습 및 정밀 데이터 분석** |

제작: 사곡고등학교 물리실
""")
