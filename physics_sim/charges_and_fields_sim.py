"""
Charges and Fields Simulator  (PhET-style)
==========================================
사용법:
  - 마우스 왼쪽 버튼으로 캔버스 클릭 → +1 nC 양전하 추가
  - 마우스 오른쪽 버튼으로 캔버스 클릭 → -1 nC 음전하 추가
  - 전하를 드래그하여 이동
  - 전하 위에서 마우스 가운데 버튼(또는 Ctrl+클릭) → 전하 삭제
  - 체크박스 버튼으로 표시 옵션 토글
  - 'C' 키: 모든 전하 삭제
  - 'Q' 키: 종료
"""

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import CheckButtons, Button
import matplotlib.patheffects as pe

# ── 상수 ──────────────────────────────────────────────────────────────────────
K_E = 8.99e9          # 쿨롱 상수 [N·m²/C²]
Q_UNIT = 1e-9         # 1 nC
GRID_N = 22           # 화살표 격자 해상도 (NxN)
CONTOUR_LEVELS = 14   # 등전위선 개수
CHARGE_RADIUS = 0.18  # 전하 원 반지름 (축 단위)
DOMAIN = (-5, 5)      # x, y 범위

# ── 전기장 계산 ────────────────────────────────────────────────────────────────
def compute_field(charges, X, Y):
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)
    V  = np.zeros_like(X)
    for (cx, cy, q) in charges:
        dx = X - cx
        dy = Y - cy
        r2 = dx**2 + dy**2
        r2 = np.where(r2 < 0.01, 0.01, r2)   # 특이점 회피
        r  = np.sqrt(r2)
        r3 = r2 * r
        coeff = K_E * q * Q_UNIT
        Ex += coeff * dx / r3
        Ey += coeff * dy / r3
        V  += coeff / r
    return Ex, Ey, V

# ── 메인 시뮬레이터 클래스 ────────────────────────────────────────────────────
class ChargesAndFields:
    def __init__(self):
        self.charges = []          # [(x, y, sign), ...]  sign ∈ {+1, -1}
        self.dragging_idx = None
        self.drag_offset  = (0, 0)

        # ── 옵션 상태 ──
        self.show_field      = True
        self.direction_only  = False
        self.show_voltage    = False
        self.show_grid       = False
        self.show_values     = False

        self._build_figure()
        self._connect_events()
        self.redraw()
        plt.show()

    # ── 그림 레이아웃 구성 ─────────────────────────────────────────────────────
    def _build_figure(self):
        self.fig = plt.figure(figsize=(13, 9), facecolor='#111111')
        self.fig.canvas.manager.set_window_title('Charges & Fields  —  PhET Style (Python)')

        # 메인 캔버스
        self.ax = self.fig.add_axes([0.03, 0.06, 0.76, 0.92], facecolor='#111111')
        self.ax.set_xlim(*DOMAIN)
        self.ax.set_ylim(*DOMAIN)
        self.ax.set_aspect('equal')
        self.ax.tick_params(colors='#555555')
        self.ax.spines[:].set_color('#333333')

        # ── 오른쪽 패널: 체크박스 ──
        ax_cb = self.fig.add_axes([0.81, 0.60, 0.17, 0.30], facecolor='#1e1e2e')
        labels = ['Electric Field', 'Direction only', 'Voltage', 'Values', 'Grid']
        actives = [self.show_field, self.direction_only,
                   self.show_voltage, self.show_values, self.show_grid]
        self.checkboxes = CheckButtons(ax_cb, labels, actives)
        self.checkboxes.on_clicked(self._on_checkbox)
        for txt in self.checkboxes.labels:
            txt.set_color('white')
            txt.set_fontsize(10)
        ax_cb.set_title('Display', color='white', fontsize=10, pad=4)

        # ── 버튼: Clear ──
        ax_btn = self.fig.add_axes([0.83, 0.52, 0.12, 0.05])
        self.btn_clear = Button(ax_btn, 'Clear All',
                                color='#cc3333', hovercolor='#ff5555')
        self.btn_clear.label.set_color('white')
        self.btn_clear.on_clicked(self._clear_all)

        # ── 하단 범례 ──
        ax_leg = self.fig.add_axes([0.35, 0.01, 0.30, 0.04], facecolor='none')
        ax_leg.axis('off')
        ax_leg.text(0.0, 0.5, '● LClick: +1nC', color='#ff6666',
                    fontsize=9, va='center', transform=ax_leg.transAxes)
        ax_leg.text(0.45, 0.5, '● RClick: −1nC', color='#6699ff',
                    fontsize=9, va='center', transform=ax_leg.transAxes)
        ax_leg.text(0.9, 0.5, 'Drag to move', color='#aaaaaa',
                    fontsize=9, va='center', transform=ax_leg.transAxes)

        # ── 전압 표시 텍스트 ──
        self.voltage_text = self.ax.text(
            0.02, 0.97, '', transform=self.ax.transAxes,
            color='#ffdd55', fontsize=11, va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#222244', alpha=0.8))

    # ── 이벤트 연결 ────────────────────────────────────────────────────────────
    def _connect_events(self):
        self.fig.canvas.mpl_connect('button_press_event',   self._on_press)
        self.fig.canvas.mpl_connect('button_release_event', self._on_release)
        self.fig.canvas.mpl_connect('motion_notify_event',  self._on_motion)
        self.fig.canvas.mpl_connect('key_press_event',      self._on_key)
        self.fig.canvas.mpl_connect('motion_notify_event',  self._on_hover)

    # ── 화살표/등전위 등 전체 다시 그리기 ─────────────────────────────────────
    def redraw(self):
        ax = self.ax
        ax.cla()
        ax.set_xlim(*DOMAIN)
        ax.set_ylim(*DOMAIN)
        ax.set_aspect('equal')
        ax.set_facecolor('#111111')
        ax.tick_params(colors='#555555')
        ax.spines[:].set_color('#333333')
        ax.set_title('Charges & Fields Simulator', color='#aaaaaa',
                     fontsize=12, pad=6)

        # 격자선
        if self.show_grid:
            ax.grid(True, color='#2a2a2a', linewidth=0.6, linestyle='--')
        else:
            ax.grid(False)

        if self.charges:
            xs = np.linspace(*DOMAIN, GRID_N)
            ys = np.linspace(*DOMAIN, GRID_N)
            X, Y = np.meshgrid(xs, ys)
            Ex, Ey, V = compute_field(self.charges, X, Y)
            E_mag = np.sqrt(Ex**2 + Ey**2)

            # ── 등전위선 ──
            if self.show_voltage:
                vmax = min(np.percentile(np.abs(V), 97), 100)
                lvl  = np.linspace(-vmax, vmax, CONTOUR_LEVELS)
                try:
                    cs = ax.contour(X, Y, V, levels=lvl,
                                    cmap='coolwarm', alpha=0.55, linewidths=1.2)
                    if self.show_values:
                        ax.clabel(cs, fmt='%.1f V', fontsize=7,
                                  colors='#dddddd', inline=True)
                except Exception:
                    pass

            # ── 전기장 화살표 ──
            if self.show_field:
                if self.direction_only:
                    # 단위 벡터
                    safe_mag = np.where(E_mag == 0, 1, E_mag)
                    Ux = Ex / safe_mag
                    Uy = Ey / safe_mag
                    color_arr = 'white'
                    scale_q   = GRID_N * 1.4
                    ax.quiver(X, Y, Ux, Uy,
                              color=color_arr, scale=scale_q,
                              width=0.0025, headwidth=4,
                              headlength=5, alpha=0.85)
                else:
                    # 크기 비례 (log 스케일)
                    log_mag = np.log10(np.clip(E_mag, 1e-3, None))
                    norm    = (log_mag - log_mag.min()) / \
                              (log_mag.max() - log_mag.min() + 1e-10)
                    safe_mag = np.where(E_mag == 0, 1, E_mag)
                    Ux = Ex / safe_mag * norm
                    Uy = Ey / safe_mag * norm
                    ax.quiver(X, Y, Ux, Uy,
                              norm, cmap='plasma',
                              scale=GRID_N * 1.6,
                              width=0.003, headwidth=4,
                              headlength=5, alpha=0.9,
                              clim=(0, 1))

        # ── 전하 그리기 ──
        for i, (cx, cy, sign) in enumerate(self.charges):
            color  = '#ff4444' if sign > 0 else '#4488ff'
            symbol = '＋' if sign > 0 else '－'
            circle = plt.Circle((cx, cy), CHARGE_RADIUS,
                                 color=color, zorder=5)
            ax.add_patch(circle)
            ax.text(cx, cy, symbol, ha='center', va='center',
                    fontsize=13, color='white', fontweight='bold',
                    zorder=6)
            if self.show_values:
                ax.text(cx, cy - CHARGE_RADIUS - 0.15,
                        f'{"+1" if sign>0 else "−1"} nC',
                        ha='center', va='top', fontsize=8,
                        color='#ddddaa', zorder=6)

        # 전압 텍스트 위치 유지
        self.voltage_text = ax.text(
            0.02, 0.97, '', transform=ax.transAxes,
            color='#ffdd55', fontsize=11, va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#222244', alpha=0.8))

        self.fig.canvas.draw_idle()

    # ── 마우스 이벤트 ──────────────────────────────────────────────────────────
    def _find_charge_at(self, x, y, tol=CHARGE_RADIUS * 1.3):
        for i, (cx, cy, _) in enumerate(self.charges):
            if (x - cx)**2 + (y - cy)**2 < tol**2:
                return i
        return None

    def _on_press(self, event):
        if event.inaxes != self.ax:
            return
        x, y = event.xdata, event.ydata
        idx = self._find_charge_at(x, y)

        if event.button == 1:            # 왼쪽 클릭
            if idx is not None:
                self.dragging_idx = idx
                cx, cy, _ = self.charges[idx]
                self.drag_offset = (cx - x, cy - y)
            else:
                self.charges.append((x, y, +1))
                self.redraw()

        elif event.button == 3:          # 오른쪽 클릭
            if idx is not None:
                # 오른쪽으로 기존 전하 삭제
                self.charges.pop(idx)
            else:
                self.charges.append((x, y, -1))
            self.redraw()

    def _on_release(self, event):
        self.dragging_idx = None

    def _on_motion(self, event):
        if self.dragging_idx is None or event.inaxes != self.ax:
            return
        x, y = event.xdata, event.ydata
        ox, oy = self.drag_offset
        cx, cy, sign = self.charges[self.dragging_idx]
        self.charges[self.dragging_idx] = (x + ox, y + oy, sign)
        self.redraw()

    def _on_hover(self, event):
        """마우스 위치의 전압값 표시"""
        if event.inaxes != self.ax or not self.charges:
            if hasattr(self, 'voltage_text'):
                self.voltage_text.set_text('')
                self.fig.canvas.draw_idle()
            return
        x, y = event.xdata, event.ydata
        V_here = sum(
            K_E * q * Q_UNIT / max(np.sqrt((x - cx)**2 + (y - cy)**2), 0.05)
            for cx, cy, q in self.charges
        )
        self.voltage_text.set_text(f'V = {V_here:.2f} V  at ({x:.2f}, {y:.2f})')
        self.fig.canvas.draw_idle()

    # ── 체크박스 토글 ──────────────────────────────────────────────────────────
    def _on_checkbox(self, label):
        if label == 'Electric Field':
            self.show_field = not self.show_field
        elif label == 'Direction only':
            self.direction_only = not self.direction_only
        elif label == 'Voltage':
            self.show_voltage = not self.show_voltage
        elif label == 'Values':
            self.show_values = not self.show_values
        elif label == 'Grid':
            self.show_grid = not self.show_grid
        self.redraw()

    def _clear_all(self, event):
        self.charges.clear()
        self.redraw()

    # ── 키 단축키 ─────────────────────────────────────────────────────────────
    def _on_key(self, event):
        if event.key in ('c', 'C'):
            self.charges.clear()
            self.redraw()
        elif event.key in ('q', 'Q'):
            plt.close('all')


if __name__ == '__main__':
    print("=" * 55)
    print("  Charges & Fields Simulator  (PhET Python Edition)")
    print("=" * 55)
    print("  LClick  : +1 nC 양전하 추가")
    print("  RClick  : -1 nC 음전하 추가  /  전하 위에서: 삭제")
    print("  Drag    : 전하 이동")
    print("  C       : 전체 삭제")
    print("  Q       : 종료")
    print("=" * 55)
    ChargesAndFields()
