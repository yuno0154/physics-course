"""Streamlit Community Cloud 앱을 깨우는 스크립트.

헤드리스 브라우저로 앱에 접속해서
1) 잠자기 화면("Yes, get this app back up!" 버튼)이 보이면 버튼을 누르고
2) 실제 앱 화면(stApp)이 뜰 때까지 기다린다.
제한 시간 안에 앱이 뜨지 않으면 실패(exit 1)로 끝나서 GitHub에서 알림 메일이 온다.
"""
import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

APP_URL = os.environ.get("APP_URL", "https://physics-course.streamlit.app/")
TIMEOUT_SEC = int(os.environ.get("WAKE_TIMEOUT_SEC", "420"))
WAKE_BUTTON = re.compile(r"get this app back up", re.I)


def all_frames(page):
    return [page.main_frame] + [f for f in page.frames if f != page.main_frame]


def click_wake_button(page):
    for frame in all_frames(page):
        btn = frame.get_by_role("button", name=WAKE_BUTTON)
        try:
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                return True
        except Exception:
            pass
    return False


def app_is_ready(page):
    for frame in all_frames(page):
        try:
            if frame.locator('[data-testid="stApp"], .stApp').count() > 0:
                # 앱 본문이 실제로 그려졌는지(사이드바나 본문 블록) 확인
                if frame.locator(
                    '[data-testid="stSidebar"], [data-testid="stMain"], '
                    '[data-testid="stAppViewContainer"]'
                ).count() > 0:
                    return True
        except Exception:
            pass
    return False


def main():
    deadline = time.time() + TIMEOUT_SEC
    clicked = False
    with sync_playwright() as p:
        exe = os.environ.get("CHROMIUM_PATH")  # 로컬 테스트용(선택)
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL, wait_until="domcontentloaded", timeout=90_000)
        last_reload = time.time()

        while time.time() < deadline:
            if app_is_ready(page):
                print(f"앱이 깨어 있습니다. (잠자기 버튼 클릭: {'예' if clicked else '아니오'})")
                browser.close()
                return 0
            if click_wake_button(page):
                clicked = True
                print("잠자기 화면 발견: 'Yes, get this app back up!' 버튼을 눌렀습니다.")
            # "taking longer than normal" 화면에 오래 멈춰 있으면 2분마다 새로고침
            if time.time() - last_reload > 120:
                print("아직 부팅 중이라 새로고침합니다.")
                page.reload(wait_until="domcontentloaded", timeout=90_000)
                last_reload = time.time()
            page.wait_for_timeout(5_000)

        page.screenshot(path="wake_failure.png", full_page=True)
        browser.close()
    print(f"{TIMEOUT_SEC}초 안에 앱이 뜨지 않았습니다.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
