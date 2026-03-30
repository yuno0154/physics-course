import os
import subprocess
import sys
import shutil
import argparse

def setup(launch=False):
    # Standard venv path (Absolute)
    target_venv_root = r"d:\project\물리학 가상실험"
    target_venv_path = os.path.join(target_venv_root, ".venv")
    
    # Current project path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    old_venv_path = os.path.join(current_dir, "venv")
    requirements_path = os.path.join(current_dir, "requirements.txt")
    main_app_path = os.path.join(current_dir, "main_app.py")

    print(f"[*] Project directory: {current_dir}")
    print(f"[*] Target Venv path: {target_venv_path}")

    try:
        # 1. Ensure target directory exists
        if not os.path.exists(target_venv_root):
            print(f"[*] Creating directory: {target_venv_root}")
            os.makedirs(target_venv_root, exist_ok=True)

        # 2. Check/Create Virtual Environment
        if not os.path.exists(target_venv_path):
            print("[*] Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", target_venv_path], check=True)
            print("[*] Venv creation successful.")
        else:
            print("[*] Virtual environment already exists.")

        # 3. Install Requirements
        if os.path.exists(requirements_path):
            print("[*] Installing requirements...")
            venv_python = os.path.join(target_venv_path, "Scripts", "python.exe")
            if not os.path.exists(venv_python):
                print("[!] python.exe not found in venv. Repairing...")
                subprocess.run([sys.executable, "-m", "venv", "--clear", target_venv_path], check=True)
            
            # Use 'python -m pip' to upgrade pip to avoid file lock issues on Windows
            print("[*] Upgrading pip...")
            subprocess.run([venv_python, "-m", "pip", "install", "-U", "pip"], check=True)
            
            print("[*] Installing dependencies from requirements.txt...")
            subprocess.run([venv_python, "-m", "pip", "install", "-r", requirements_path], check=True)
            print("[*] Installation successful.")
        else:
            print("[!] Warning: requirements.txt not found.")

        # 4. Delete old "venv" folder in project directory
        if os.path.exists(old_venv_path):
            print(f"[*] Deleting old venv at {old_venv_path}...")
            try:
                shutil.rmtree(old_venv_path)
                print("[*] Old venv deleted.")
            except Exception as e:
                print(f"[!] Warning: Could not delete venv: {e}")

        print("[*] Setup complete!")

        # 5. Launch if requested
        if launch:
            print("[*] Launching Streamlit App...")
            streamlit_path = os.path.join(target_venv_path, "Scripts", "streamlit.exe")
            if os.path.exists(streamlit_path):
                subprocess.run([streamlit_path, "run", main_app_path], check=True)
            else:
                print("[ERROR] streamlit.exe not found. Please check dependencies.")
                sys.exit(1)
        
    except Exception as e:
        print(f"\n[ERROR] Process failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", action="store_true", help="Launch the app after setup")
    args = parser.parse_args()
    
    setup(launch=args.launch)
