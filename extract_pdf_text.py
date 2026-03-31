import pdfplumber
import sys

pdf_path = r"D:\OneDrive - 사곡고등학교\2026학년도\수업\2026년 물리학Ⅱ\수행평가\비스듬히 위로 던진 물체의 운동 분석 보고서 양식(모둠용-이름).pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        print(text)
except Exception as e:
    print(f"Error: {e}")
