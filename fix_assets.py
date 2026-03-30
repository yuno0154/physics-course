import os
import shutil

# 프로젝트 루트 경로 설정 (한글 인코딩 방지를 위해 raw string 사용)
PROJECT_ROOT = r"d:\OneDrive - 사곡고등학교\2026학년도\프로그램 개발\물리학 가상실험"
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

# 원본 이미지 경로 (Gemini 아티팩트 보관함)
SRC_ARTIFACTS = r"C:\Users\user\AppData\Local\Google\Assistant\brain\e5b8bf18-16a3-4b13-ae8b-2b8404880aa3" # 앗! 경로가 살짝 다를 수 있으니 아까 확인한 값을 씁니다.
# 앗 위 경로는 이전 정보이니, 이전에 아티팩트 저장소로 확인된 경로를 씁니다.
SRC_PATH1 = r"C:\Users\user\.gemini\antigravity\brain\e5b8bf18-16a3-4b13-ae8b-2b8404880aa3\horizontal_cliff_diagram_1774856431303.png"
SRC_PATH2 = r"C:\Users\user\.gemini\antigravity\brain\e5b8bf18-16a3-4b13-ae8b-2b8404880aa3\oblique_launch_diagram_1774856444404.png"

# 1. assets 폴더 생성
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)
    print(f"Created directory: {ASSETS_DIR}")

# 2. 파일 복사
try:
    shutil.copy(SRC_PATH1, os.path.join(ASSETS_DIR, "horizontal_cliff.png"))
    shutil.copy(SRC_PATH2, os.path.join(ASSETS_DIR, "oblique_launch.png"))
    print("Files copied successfully!")
except Exception as e:
    print(f"Error copying files: {e}")
