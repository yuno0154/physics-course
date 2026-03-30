import base64
import os

# 원본 및 대상 경로
IMG1 = r"C:\Users\user\.gemini\antigravity\brain\e5b8bf18-16a3-4b13-ae8b-2b8404880aa3\horizontal_cliff_diagram_1774856431303.png"
IMG2 = r"C:\Users\user\.gemini\antigravity\brain\e5b8bf18-16a3-4b13-ae8b-2b8404880aa3\oblique_launch_diagram_1774856444404.png"
OUTPUT_DIR = r"d:\OneDrive - 사곡고등학교\2026학년도\프로그램 개발\물리학 가상실험"

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 데이터 추출 및 파일 저장
try:
    data1 = get_b64(IMG1)
    data2 = get_b64(IMG2)
    
    with open(os.path.join(OUTPUT_DIR, "img_data.txt"), "w") as f:
        f.write("IMAGE1:" + data1 + "\n")
        f.write("IMAGE2:" + data2 + "\n")
    print("DONE_SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
