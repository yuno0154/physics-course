import os
import subprocess
import sys
import shutil
import argparse

def find_working_venv():
    # Candidates for venv
    candidates = [
        r"d:\project\물리학 가상실험\.venv",
        r"d:\project\물리학 가상실험\venv",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv"),
    ]
    for cand in candidates:
        py_path = os.path.join(cand, "Scripts", "python.exe")
        if os.path.exists(py_path):
            return cand, py_path
    return None, None

def setup(launch=False, target_file="main_app.py"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(current_dir, "requirements.txt")
    
    # Target file path resolution
    if not os.path.isabs(target_file):
        target_path = os.path.join(current_dir, target_file)
    else:
        target_path = target_file

    print(f"[*] Project directory: {current_dir}")
    print(f"[*] Target launch file: {target_path}")

    try:
        venv_dir, venv_python = find_working_venv()
        target_venv_root = r"d:\project\물리학 가상실험"
        default_venv_path = os.path.join(target_venv_root, ".venv")

        if not venv_python:
            print("[*] 가상환경을 찾지 못하여 기본 경로에 생성합니다...")
            os.makedirs(target_venv_root, exist_ok=True)
            subprocess.run([sys.executable, "-m", "venv", default_venv_path], check=True)
            venv_dir = default_venv_path
            venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
            print("[*] 가상환경 생성 완료.")

        print(f"[*] 사용 중인 파이썬 환경: {venv_python}")

        # Ensure pip and requirements are installed
        if os.path.exists(requirements_path):
            # Check if streamlit is already installed in this venv
            check_res = subprocess.run([venv_python, "-c", "import streamlit"], capture_output=True)
            if check_res.returncode != 0:
                print("[*] 필요한 패키지를 설치 중입니다...")
                subprocess.run([venv_python, "-m", "pip", "install", "-U", "pip"], check=True)
                subprocess.run([venv_python, "-m", "pip", "install", "-r", requirements_path], check=True)
                print("[*] 패키지 설치 완료.")
            else:
                print("[*] 가상환경 패키지가 이미 완비되어 있습니다.")

        print("[*] 실행 환경 준비 완료!")

        # Launch if requested
        if launch:
            print(f"[*] Streamlit 앱을 실행합니다 ({os.path.basename(target_path)})...")
            streamlit_path = os.path.join(venv_dir, "Scripts", "streamlit.exe")
            if os.path.exists(streamlit_path):
                cmd = [streamlit_path, "run", target_path]
            else:
                cmd = [venv_python, "-m", "streamlit", "run", target_path]
            
            subprocess.run(cmd, check=True)

    except Exception as e:
        print(f"\n[오류 발생]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", action="store_true", help="Launch the app after setup")
    parser.add_argument("--file", type=str, default="main_app.py", help="Target python file to run with streamlit")
    args = parser.parse_args()
    
    setup(launch=args.launch, target_file=args.file)
