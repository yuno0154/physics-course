"""
전류 모형 시뮬레이션 (Current Model Simulation)
================================================
① 자유 전자의 이동 모형
② 전류 모형 + 전위차 시각화

[ 실행 방법 ]
  pip install pygame
  python current_model_simulation.py

[ 조작 방법 ]
  마우스 슬라이더 드래그   → 전압 조절 (0 ~ 10 V)
  ↑ / ↓ 키보드             → 전압 +0.5 / -0.5 V
  ← / → 키보드 또는 버튼   → 단계 전환
  ESC                       → 종료

[ 한국어 폰트 ]
  Windows : 맑은 고딕(자동 감지)
  macOS   : AppleGothic(자동 감지)
  Linux   : sudo apt install fonts-nanum  후 재실행
"""

import pygame
import math
import random
import sys

# ──────────────────────────────────────
#  초기화
# ──────────────────────────────────────
pygame.init()
W, H = 860, 630
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("전류 모형 시뮬레이션")
clock = pygame.time.Clock()

# ──────────────────────────────────────
#  색상 팔레트
# ──────────────────────────────────────
BG       = (246, 244, 239)
WIRE_BG  = (232, 236, 250)
BORDER   = (165, 172, 200)
PLUS_C   = (208, 60, 40)
MINUS_C  = (46, 90, 215)
ELEC_F   = (165, 95, 18)
ELEC_HL  = (215, 145, 40)
ION_F    = (42, 92, 162)
ION_HL   = (58, 142, 235)
FLASH_C  = (255, 195, 58)
TEXT_PRI = (46, 44, 36)
TEXT_SEC = (108, 106, 96)
TEXT_MUT = (155, 153, 143)
ARROW_E  = (170, 102, 20)   # 전자 이동
ARROW_I  = (42, 94, 212)    # 전류 방향
STAT_BG  = (232, 230, 225)
BTN_BG   = (232, 236, 248)
BTN_ACT  = (225, 234, 255)
BTN_BOR  = (165, 172, 200)
BTN_ABOR = (78, 128, 210)

# ──────────────────────────────────────
#  폰트 로드 (한국어 우선)
# ──────────────────────────────────────
def load_fonts():
    candidates = [
        "malgungothic", "malgun gothic",
        "nanumgothic",  "nanum gothic", "NanumGothic",
        "applegothic",  "apple gothic",
        "notosanscjkkr","noto sans cjk kr",
        "gulim", "dotum", "batang",
    ]
    found = None
    for name in candidates:
        try:
            f = pygame.font.SysFont(name, 15)
            surf = f.render("한글", True, (0, 0, 0))
            if surf.get_width() > 12:
                found = name
                break
        except Exception:
            pass
    if not found:
        print("[주의] 한국어 폰트를 찾지 못했습니다. 기본 폰트로 실행합니다.")
        print("[Note] Korean font not found. Using default font.")
    src = found
    def mk(sz, bold=False):
        return pygame.font.SysFont(src, sz, bold=bold) if src \
               else pygame.font.SysFont(None, sz + 3, bold=bold)
    return {
        "sm":  mk(12),
        "md":  mk(14),
        "lg":  mk(17),
        "bsm": mk(12, bold=True),
        "bmd": mk(14, bold=True),
        "blg": mk(17, bold=True),
        "bxl": mk(20, bold=True),
    }

F = load_fonts()

# ──────────────────────────────────────
#  유틸 함수
# ──────────────────────────────────────
def txt(surf, text, fkey, color, x, y, cx=False, cy=False):
    s = F[fkey].render(text, True, color)
    dx = -s.get_width()  // 2 if cx else 0
    dy = -s.get_height() // 2 if cy else 0
    surf.blit(s, (x + dx, y + dy))

def rrect(surf, color, rect, r, w=0):
    pygame.draw.rect(surf, color, rect, w, border_radius=r)

def arrow(surf, color, x1, y1, x2, y2, lw=2):
    pygame.draw.line(surf, color, (int(x1), int(y1)), (int(x2), int(y2)), lw)
    a = math.atan2(y2 - y1, x2 - x1)
    L, da = 11, 0.4
    tip = (int(x2), int(y2))
    p1 = (int(x2 - L * math.cos(a - da)), int(y2 - L * math.sin(a - da)))
    p2 = (int(x2 - L * math.cos(a + da)), int(y2 - L * math.sin(a + da)))
    pygame.draw.polygon(surf, color, [tip, p1, p2])

def lerp_col(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def blend(base, color, alpha):
    return lerp_col(base, color, alpha)

def draw_wire_gradient(surf, bounds, voltage):
    """전위 기울기가 적용된 도선 배경 그리기"""
    x1, y1, x2, y2 = bounds
    w, h = x2 - x1, y2 - y1
    al = min(voltage / 10, 1.0)
    steps = 40
    sw = max(1, w // steps + 1)
    for i in range(steps):
        t = i / steps
        c = lerp_col(PLUS_C, MINUS_C, t)
        fc = blend(WIRE_BG, c, al * 0.38) if voltage > 0 else WIRE_BG
        pygame.draw.rect(surf, fc,
                         pygame.Rect(x1 + int(t * w), y1, sw, h))
    # 테두리
    rrect(surf, BORDER, pygame.Rect(x1, y1, w, h), 12, 2)

def draw_terminal(surf, x, y, is_plus, voltage):
    """단말 블록 (+극 / -극) 그리기"""
    c = PLUS_C if is_plus else MINUS_C
    lbl  = "+극" if is_plus else "−극"
    sub1 = "높은 전위" if is_plus else "낮은 전위"
    sub2 = f"{voltage:.1f} V" if is_plus else "0 V"
    rrect(surf, c, pygame.Rect(x - 38, y - 40, 76, 80), 9)
    txt(surf, lbl,  "bmd", (255, 255, 255), x, y - 22, cx=True, cy=True)
    txt(surf, sub1, "sm",  (240, 240, 240), x, y -  5, cx=True, cy=True)
    txt(surf, sub2, "sm",  (240, 240, 240), x, y + 14, cx=True, cy=True)

# ──────────────────────────────────────
#  전자 클래스
# ──────────────────────────────────────
class Electron:
    def __init__(self, bounds):
        x1, y1, x2, y2 = bounds
        a = random.uniform(0, math.pi * 2)
        s = random.uniform(0.8, 2.0)
        self.x = random.uniform(x1 + 12, x2 - 12)
        self.y = random.uniform(y1 + 12, y2 - 12)
        self.vx, self.vy = math.cos(a) * s, math.sin(a) * s
        self.bounds = bounds
        self.trail = []

    def update(self, voltage):
        # 열운동 (무작위 성분)
        self.vx += random.uniform(-0.52, 0.52)
        self.vy += random.uniform(-0.52, 0.52)
        # 표류 (drift): +극(left) 방향
        self.vx -= voltage * 0.072
        # 속력 제한
        sp = math.sqrt(self.vx ** 2 + self.vy ** 2)
        mx = 3.0 + voltage * 0.26
        if sp > mx:
            self.vx, self.vy = self.vx / sp * mx, self.vy / sp * mx
        self.x += self.vx
        self.y += self.vy
        # 궤적 저장
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
        # 경계 처리
        x1, y1, x2, y2 = self.bounds
        if self.x < x1 + 8:            # +극으로 진입 → -극 쪽에서 재등장
            self.x = x2 - 9
            self.y = random.uniform(y1 + 12, y2 - 12)
            self.trail = []
        if self.x > x2 - 8:
            self.x, self.vx = x2 - 8, -abs(self.vx) * 0.85
        if self.y < y1 + 6:
            self.y, self.vy = y1 + 6,  abs(self.vy) * 0.85
        if self.y > y2 - 6:
            self.y, self.vy = y2 - 6, -abs(self.vy) * 0.85

    def draw(self, surf, show_trail=False, voltage=0):
        # 궤적
        if show_trail and voltage > 2.5 and len(self.trail) > 2:
            for i in range(1, len(self.trail)):
                pygame.draw.line(surf, (190, 125, 28),
                                 (int(self.trail[i-1][0]), int(self.trail[i-1][1])),
                                 (int(self.trail[i][0]),   int(self.trail[i][1])), 1)
        # 전자 원
        ix, iy = int(self.x), int(self.y)
        pygame.draw.circle(surf, ELEC_F,  (ix, iy), 7)
        pygame.draw.circle(surf, ELEC_HL, (ix, iy), 7, 1)
        # e⁻ 레이블
        lbl = F["sm"].render("e\u207b", True, (255, 248, 225))
        surf.blit(lbl, (ix - lbl.get_width() // 2, iy - lbl.get_height() // 2))

# ──────────────────────────────────────
#  양이온 클래스
# ──────────────────────────────────────
class Ion:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.flash = 0.0

    def draw(self, surf):
        # 충돌 플래시
        if self.flash > 0:
            r = max(2, int(18 * self.flash))
            s = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*FLASH_C, int(self.flash * 125)), (r, r), r)
            surf.blit(s, (int(self.x) - r, int(self.y) - r))
            self.flash = max(0.0, self.flash - 0.058)
        c = ION_HL if self.flash > 0.15 else ION_F
        ix, iy = int(self.x), int(self.y)
        pygame.draw.circle(surf, c, (ix, iy), 10)
        pygame.draw.circle(surf, (95, 155, 225), (ix, iy), 10, 1)
        lbl = F["bsm"].render("+", True, (255, 255, 255))
        surf.blit(lbl, (ix - lbl.get_width() // 2, iy - lbl.get_height() // 2))

    def collide(self, e, particles):
        dx, dy = e.x - self.x, e.y - self.y
        d = math.sqrt(dx * dx + dy * dy)
        if 0 < d < 15:
            ang = math.atan2(dy, dx)
            e.x = self.x + 15 * math.cos(ang)
            e.y = self.y + 15 * math.sin(ang)
            na = ang + math.pi + random.uniform(-1.1, 1.1)
            ns = random.uniform(0.9, 2.2)
            e.vx, e.vy = math.cos(na) * ns, math.sin(na) * ns
            self.flash = 1.0
            if random.random() < 0.30:
                for _ in range(3):
                    pa = random.uniform(0, math.pi * 2)
                    particles.append({
                        "x": self.x, "y": self.y,
                        "vx": math.cos(pa) * random.uniform(0.8, 1.8),
                        "vy": math.sin(pa) * random.uniform(0.8, 1.8),
                        "life": 1.0,
                    })

# ──────────────────────────────────────
#  슬라이더 클래스
# ──────────────────────────────────────
class Slider:
    def __init__(self, x, y, w):
        self.x, self.y, self.w = x, y, w
        self.value = 0.0
        self.dragging = False

    def thumb_x(self):
        return int(self.x + self.value / 10.0 * self.w)

    def handle(self, event):
        tx = self.thumb_x()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (abs(event.pos[0] - tx) < 14 and abs(event.pos[1] - self.y) < 14) or \
               (self.y - 10 <= event.pos[1] <= self.y + 10 and
                    self.x <= event.pos[0] <= self.x + self.w):
                self.dragging = True
                self._set(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._set(event.pos[0])

    def _set(self, mx):
        r = max(0.0, min(1.0, (mx - self.x) / self.w))
        self.value = round(r * 10.0 / 0.5) * 0.5

    def draw(self, surf):
        # 트랙
        rrect(surf, (182, 180, 172), pygame.Rect(self.x, self.y - 3, self.w, 6), 3)
        tx = self.thumb_x()
        if tx > self.x:
            rrect(surf, (78, 130, 202), pygame.Rect(self.x, self.y - 3, tx - self.x, 6), 3)
        pygame.draw.circle(surf, (78, 130, 202), (tx, self.y), 11)
        pygame.draw.circle(surf, (255, 255, 255), (tx, self.y), 11, 2)

# ──────────────────────────────────────
#  메인 시뮬레이션
# ──────────────────────────────────────
class Simulation:
    def __init__(self):
        self.step = 1   # 현재 단계 (1 or 2)

        # ── 단계 1: 단순 전자 이동 ──
        self.w1 = (105, 110, 755, 295)     # 도선 경계
        self.els1 = [Electron(self.w1) for _ in range(44)]

        # ── 단계 2: 전류 모형 + 전위차 ──
        self.w2 = (115, 80, 745, 215)
        x1, y1, x2, y2 = self.w2
        ww, wh = x2 - x1, y2 - y1
        COLS, ROWS = 10, 4
        self.ions = [
            Ion(x1 + ww / (COLS + 1) * (c + 1),
                y1 + wh / (ROWS + 1) * (r + 1))
            for r in range(ROWS) for c in range(COLS)
        ]
        self.els2 = [Electron(self.w2) for _ in range(38)]
        self.sparks = []   # 충돌 플래시 파티클

        # ── 공유 컨트롤 ──
        self.slider = Slider(110, 498, W - 220)
        self.voltage = 0.0

    # ─── 이벤트 처리 ───
    def handle(self, event):
        self.slider.handle(event)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_TAB):
                self.step = min(2, self.step + 1)
            elif event.key == pygame.K_LEFT:
                self.step = max(1, self.step - 1)
            elif event.key == pygame.K_UP:
                self.slider.value = min(10.0, round(self.slider.value + 0.5, 1))
            elif event.key == pygame.K_DOWN:
                self.slider.value = max(0.0, round(self.slider.value - 0.5, 1))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # 단계 버튼
            if pygame.Rect(60, 42, 355, 36).collidepoint(mx, my):
                self.step = 1
            elif pygame.Rect(445, 42, 355, 36).collidepoint(mx, my):
                self.step = 2
            # 이전 / 다음 버튼
            if self.step > 1 and pygame.Rect(60, 548, 175, 36).collidepoint(mx, my):
                self.step = 1
            if self.step < 2 and pygame.Rect(W - 235, 548, 175, 36).collidepoint(mx, my):
                self.step = 2

    # ─── 물리 업데이트 ───
    def update(self):
        self.voltage = self.slider.value
        for e in self.els1:
            e.update(self.voltage)
        for e in self.els2:
            e.update(self.voltage)
            for ion in self.ions:
                ion.collide(e, self.sparks)
        for p in self.sparks:
            p["x"] += p["vx"]; p["y"] += p["vy"]; p["life"] -= 0.1
        self.sparks = [p for p in self.sparks if p["life"] > 0]

    # ─── 전체 렌더 ───
    def draw(self):
        screen.fill(BG)
        self._draw_step_tabs()
        if self.step == 1:
            self._draw_step1()
        else:
            self._draw_step2()
        self._draw_controls()
        self._draw_nav()
        pygame.display.flip()

    # ─── 단계 탭 ───
    def _draw_step_tabs(self):
        for i, (label, rx) in enumerate([
            ("① 자유 전자의 이동 모형", 60),
            ("② 전류 모형 + 전위차 시각화", 445),
        ]):
            active = (self.step == i + 1)
            bg = BTN_ACT if active else BTN_BG
            bc = BTN_ABOR if active else BTN_BOR
            rrect(screen, bg, pygame.Rect(rx, 42, 355, 36), 9)
            pygame.draw.rect(screen, bc, pygame.Rect(rx, 42, 355, 36), 1, border_radius=9)
            tc = (42, 96, 212) if active else TEXT_SEC
            txt(screen, label, "bmd", tc, rx + 177, 60, cx=True, cy=True)
        txt(screen, "→", "blg", TEXT_MUT, W // 2, 52, cx=True)

    # ─── 단계 1 렌더 ───
    def _draw_step1(self):
        x1, y1, x2, y2 = self.w1
        cy = (y1 + y2) // 2
        draw_wire_gradient(screen, self.w1, self.voltage)
        txt(screen, "금속 도체", "sm", TEXT_MUT, (x1 + x2) // 2, y1 + 7, cx=True)
        # 단말
        draw_terminal(screen, x1 - 55, cy, True,  self.voltage)
        draw_terminal(screen, x2 + 55, cy, False, self.voltage)
        pygame.draw.line(screen, PLUS_C,  (x1 - 17, cy), (x1, cy), 3)
        pygame.draw.line(screen, MINUS_C, (x2, cy), (x2 + 17, cy), 3)
        # 전자
        for e in self.els1:
            e.draw(screen, voltage=self.voltage)
        # 방향 화살표
        if self.voltage > 0:
            arrow(screen, ARROW_E, x2 - 12, y1 - 22, x1 + 12, y1 - 22, 2)
            txt(screen, "전자 이동 방향  (e⁻ : −극 → +극)",
                "sm", ARROW_E, (x1 + x2) // 2, y1 - 35, cx=True)
            arrow(screen, ARROW_I, x1 + 12, y2 + 24, x2 - 12, y2 + 24, 2)
            txt(screen, "전류 방향 I  (+극 → −극)",
                "sm", ARROW_I, (x1 + x2) // 2, y2 + 35, cx=True)
        self._draw_explain()

    # ─── 단계 2 렌더 ───
    def _draw_step2(self):
        x1, y1, x2, y2 = self.w2
        cy = (y1 + y2) // 2
        draw_wire_gradient(screen, self.w2, self.voltage)
        txt(screen, "금속 도체 (자유 전자 + 양이온 격자)",
            "sm", TEXT_MUT, (x1 + x2) // 2, y1 + 6, cx=True)
        # 단말
        draw_terminal(screen, x1 - 55, cy, True,  self.voltage)
        draw_terminal(screen, x2 + 55, cy, False, self.voltage)
        pygame.draw.line(screen, PLUS_C,  (x1 - 17, cy), (x1, cy), 3)
        pygame.draw.line(screen, MINUS_C, (x2, cy), (x2 + 17, cy), 3)
        # 양이온
        for ion in self.ions:
            ion.draw(screen)
        # 플래시 파티클
        for p in self.sparks:
            r = max(2, int(5 * p["life"]))
            s = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*FLASH_C, int(p["life"] * 112)), (r, r), r)
            screen.blit(s, (int(p["x"]) - r, int(p["y"]) - r))
        # 전자
        for e in self.els2:
            e.draw(screen, show_trail=True, voltage=self.voltage)
        # 방향 화살표
        if self.voltage > 0:
            arrow(screen, ARROW_E, x2 - 12, y1 - 22, x1 + 12, y1 - 22, 2)
            txt(screen, "전자 이동 방향  (e⁻ : −극 → +극)",
                "sm", ARROW_E, (x1 + x2) // 2, y1 - 34, cx=True)
            arrow(screen, ARROW_I, x1 + 12, y2 + 22, x2 - 12, y2 + 22, 2)
            txt(screen, "전류 방향 I  (+극 → −극)",
                "sm", ARROW_I, (x1 + x2) // 2, y2 + 33, cx=True)
        # 전위차 바
        self._draw_potential_bar(115, 260, 745, 315)
        # 통계 카드
        self._draw_stats()
        self._draw_explain()

    # ─── 전위차 시각화 바 ───
    def _draw_potential_bar(self, x1, y1, x2, y2):
        bw, bh = x2 - x1, y2 - y1
        txt(screen, "전위차 시각화", "sm", TEXT_SEC, x1, y1 - 15)
        # 그라디언트
        al = min(self.voltage / 10, 1.0)
        steps = 40
        sw = max(1, bw // steps + 1)
        for i in range(steps):
            t = i / steps
            c = lerp_col(PLUS_C, MINUS_C, t)
            fc = blend(BG, c, al * 0.82) if self.voltage > 0 \
                 else (182, 180, 172)
            pygame.draw.rect(screen, fc,
                             pygame.Rect(x1 + int(t * bw), y1, sw, bh))
        rrect(screen, BORDER, pygame.Rect(x1, y1, bw, bh), 8, 1)
        # 등전위선 + 전위값
        for i in range(1, 8):
            lx = x1 + bw // 8 * i
            pygame.draw.line(screen, (255, 255, 255), (lx, y1 + 4), (lx, y2 - 4), 1)
            if self.voltage > 0:
                vl = self.voltage * (1 - i / 8)
                s = F["sm"].render(f"{vl:.1f}V", True, (255, 255, 255))
                screen.blit(s, (lx - s.get_width() // 2,
                                (y1 + y2) // 2 - s.get_height() // 2))
        # 좌우 레이블
        cy = (y1 + y2) // 2
        txt(screen, "+극",           "bmd", PLUS_C,  x1 - 26, cy - 10, cx=True)
        txt(screen, f"{self.voltage:.1f} V", "sm", PLUS_C,  x1 - 26, cy +  6, cx=True)
        txt(screen, "−극",           "bmd", MINUS_C, x2 + 26, cy - 10, cx=True)
        txt(screen, "0 V",           "sm",  MINUS_C, x2 + 26, cy +  6, cx=True)
        # 전기장 화살표
        if self.voltage > 0:
            arrow(screen, (142, 88, 26), x1 + 14, y2 + 16, x2 - 14, y2 + 16, 2)
            txt(screen, "전기장 E  (높은 전위 → 낮은 전위 / 양전하에 작용하는 힘의 방향)",
                "sm", (142, 88, 26), (x1 + x2) // 2, y2 + 20, cx=True)
            # 시험 전하 표시
            cx = (x1 + x2) // 2
            cy2 = (y1 + y2) // 2
            # +시험전하
            pygame.draw.circle(screen, (228, 182, 28), (cx, cy2), 9)
            lp = F["bsm"].render("+", True, (55, 48, 10))
            screen.blit(lp, (cx - lp.get_width()//2, cy2 - lp.get_height()//2))
            arrow(screen, (228, 182, 28), cx + 11, cy2, cx + 32, cy2, 1)
            # −시험전하
            cx2 = cx - 80
            pygame.draw.circle(screen, (58, 148, 228), (cx2, cy2), 9)
            lm = F["bsm"].render("−", True, (255, 255, 255))
            screen.blit(lm, (cx2 - lm.get_width()//2, cy2 - lm.get_height()//2))
            arrow(screen, (58, 148, 228), cx2 - 11, cy2, cx2 - 32, cy2, 1)

    # ─── 통계 카드 ───
    def _draw_stats(self):
        labels = ["전위차", "전기장 방향", "전자 이동", "전류 방향"]
        if self.voltage == 0:
            vals   = ["0 V", "없음", "무작위", "없음"]
            colors = [TEXT_PRI] * 4
        else:
            vals   = [f"{self.voltage:.1f} V", "+극 → −극",
                      "← (−극→+극)", "→ (+극→−극)"]
            colors = [TEXT_PRI, TEXT_PRI, ARROW_E, ARROW_I]
        sw = (W - 130) // 4
        for i, (lbl, val, c) in enumerate(zip(labels, vals, colors)):
            bx = 65 + i * (sw + 4)
            rrect(screen, STAT_BG, pygame.Rect(bx, 370, sw, 52), 8)
            txt(screen, lbl, "sm",  TEXT_SEC, bx + sw // 2, 381, cx=True)
            txt(screen, val, "bmd", c,        bx + sw // 2, 402, cx=True)

    # ─── 공유 컨트롤 ───
    def _draw_controls(self):
        txt(screen, "전압 V =", "md", TEXT_SEC, 65, 485)
        txt(screen, f"{self.voltage:.1f} V", "blg", TEXT_PRI, W - 62, 485)
        self.slider.draw(screen)
        txt(screen, "슬라이더 드래그 또는 ↑↓ 키로 전압 조절",
            "sm", TEXT_MUT, W // 2, 515, cx=True)

    # ─── 설명 텍스트 ───
    def _draw_explain(self):
        V = self.voltage
        if V == 0:
            msg = "전압 = 0 V :  자유 전자는 무작위(열운동)로 움직입니다.  알짜 전류 = 0"
        elif V < 4:
            msg = (f"전압 {V:.1f} V :  자유 전자가 +극(←) 방향으로 표류합니다."
                   "  전류 방향은 전자 이동의 반대(→)입니다.")
        elif self.step == 2:
            msg = (f"전압 {V:.1f} V :  전자의 표류가 뚜렷합니다."
                   "  양이온과의 충돌(섬광)이 전기 저항의 원인입니다.")
        else:
            msg = (f"전압 {V:.1f} V :  전자의 표류(drift) 방향이 명확합니다."
                   "  전류 세기 ∝ 전위차  (옴의 법칙)")
        txt(screen, msg, "md", TEXT_SEC, W // 2, 530, cx=True)

    # ─── 이전 / 다음 버튼 ───
    def _draw_nav(self):
        if self.step > 1:
            rrect(screen, BTN_BG,  pygame.Rect(60, 548, 175, 36), 8)
            rrect(screen, BTN_BOR, pygame.Rect(60, 548, 175, 36), 8, 1)
            txt(screen, "← 이전 단계", "md", TEXT_PRI, 147, 566, cx=True, cy=True)
        if self.step < 2:
            rrect(screen, BTN_BG,  pygame.Rect(W - 235, 548, 175, 36), 8)
            rrect(screen, BTN_BOR, pygame.Rect(W - 235, 548, 175, 36), 8, 1)
            txt(screen, "다음 단계 →", "md", TEXT_PRI, W - 147, 566, cx=True, cy=True)


# ──────────────────────────────────────
#  메인 루프
# ──────────────────────────────────────
def main():
    print("=" * 50)
    print(" 전류 모형 시뮬레이션")
    print(" 조작: 슬라이더 드래그 / ↑↓ 전압 / ←→ 단계 / ESC 종료")
    print("=" * 50)
    sim = Simulation()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            sim.handle(event)
        sim.update()
        sim.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()
