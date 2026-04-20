import pygame
import time
import math
import sys
pygame.init()

from utils import scale_image, blit_rotate_center, blit_text_center
import responsive
from leaderboard import show_leaderboard, track_finish, reset_leaderboard

GRASS             = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK             = scale_image(pygame.image.load("imgs/NEW_TRACK.jpg"), 0.9)
TRACK_BORDER      = scale_image(pygame.image.load("imgs/TRACK_COLLISION.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH            = pygame.image.load("imgs/FINISH_LINE_MARK.jpg")
FINISH_MASK       = pygame.mask.from_surface(FINISH)

RED_CAR           = scale_image(pygame.image.load("imgs/red-car.png"),           0.50)
GREEN_CAR         = scale_image(pygame.image.load("imgs/green-car.png"),         0.50)
PURPLE_CAR        = scale_image(pygame.image.load("imgs/purple-car.png"),        0.50)
SPORTS_CAR        = scale_image(pygame.image.load("imgs/sports_car.png"),        0.50)
MODERN_BLUE_CAR   = scale_image(pygame.image.load("imgs/MODERN_BLUE_CAR.png"),   0.50)
MODERN_RED_CAR    = scale_image(pygame.image.load("imgs/MODERN_RED_CAR.png"),    0.50)
MODERN_PINK_CAR   = scale_image(pygame.image.load("imgs/MODERN_PINK_CAR.png"),   0.50)
MODERN_PURPLE_CAR = scale_image(pygame.image.load("imgs/MODERN_PURPLE_CAR.png"), 0.50)
MODERN_NEON_CAR   = scale_image(pygame.image.load("imgs/MODERN_NEON_CAR.png"),   0.50)
NITRO_IMG         = scale_image(pygame.image.load("imgs/nitro_img.png"),         0.3)

CAR_OPTIONS = [
    MODERN_RED_CAR, MODERN_BLUE_CAR, MODERN_PINK_CAR,
    MODERN_PURPLE_CAR, MODERN_NEON_CAR,
    RED_CAR, GREEN_CAR, PURPLE_CAR, SPORTS_CAR,
]

CAR_DATA = [
    {"name": "MODERN RED",    "color": (220,  60,  60)},
    {"name": "MODERN BLUE",   "color": ( 60, 120, 255)},
    {"name": "MODERN PINK",   "color": (255,  90, 160)},
    {"name": "MODERN PURPLE", "color": (170,  90, 255)},
    {"name": "NEON RACER",    "color": ( 30, 220, 180)},
    {"name": "RED CLASSIC",   "color": (200,  30,  30)},
    {"name": "GREEN BOLT",    "color": ( 60, 190,  80)},
    {"name": "PURPLE BEAST",  "color": (130,  60, 200)},
    {"name": "SPORTS ACE",    "color": (255, 140,   0)},
]

# Lap selector globals
selected_laps    = 3
LAP_CHOICES      = [1, 3, 5]
lap_choice_index = 1

player1_car_index = 0
player2_car_index = 1

TRACK_W = TRACK.get_width()
TRACK_H = TRACK.get_height()
HUD_HEIGHT = 80
WIDTH  = TRACK_W
HEIGHT = TRACK_H + HUD_HEIGHT

TRACK_OFFSET_X = 0
TRACK_OFFSET_Y = 0

FINISH_POSITION = (285, 415)
NITRO_POSITIONS = [
    (125, 287), (160, 255), (180, 240),
    (145, 190), (177, 161), (201, 143),
    (503, 262), (276, 296), (361, 206),
]

active_nitros = NITRO_POSITIONS.copy()
NITRO_MASK    = pygame.mask.from_surface(NITRO_IMG)
nitro_angle   = 0
offset        = math.sin(pygame.time.get_ticks() * 0.003) * 5

P1_START = (220, 412)
P2_START = (185, 435)
AI_START = (185, 412)

responsive.BASE_WIDTH  = WIDTH
responsive.BASE_HEIGHT = HEIGHT
WIN = responsive.init("Racing Master")

MAIN_FONT  = pygame.font.SysFont("cambria", 26, bold=True)
LABEL_FONT = pygame.font.SysFont("cambria", 15)

sound                  = pygame.mixer.Sound('bg_sounds/bounce_eff.wav')
sound.set_volume(.2)
sound_completed_effect = pygame.mixer.Sound('bg_sounds/level_completed.wav')
turbo_sound            = pygame.mixer.Sound('bg_sounds/turbo_sound.mp3')
exit_sound             = pygame.mixer.Sound('bg_sounds/exit_sound.mp3')
nitro_sound            = pygame.mixer.Sound('bg_sounds/nitro_engine.wav')
count3   = pygame.mixer.Sound('bg_sounds/3.mp3')
count2   = pygame.mixer.Sound('bg_sounds/2.mp3')
count1   = pygame.mixer.Sound('bg_sounds/1.mp3')
count_go = pygame.mixer.Sound('bg_sounds/go.mp3')
click_sound1 = pygame.mixer.Sound('bg_sounds/click_btn1.mp3')
click_sound2 = pygame.mixer.Sound('bg_sounds/click_btn2.mp3')

pygame.mixer.music.load('bg_sounds/RACING_MASTER_SOUNDTRACK.mp3')
pygame.time.delay(1000)
pygame.mixer.music.play(-1, 0.0)

FPS  = 60
PATH = [
    (75, 428), (58, 364), (57, 308), (96, 254), (164, 187),
    (240, 121), (337, 63), (400, 64), (452, 66), (495, 78),
    (522, 121), (510, 268), (589, 396), (558, 430), (426, 431), (304, 429)
]
PATH_RECORDING = False

WHITE            = (255, 255, 255)
BLACK            = (0,   0,   0)
FERRARI_YELLOW   = (255, 215, 0)
FERRARI_GREEN    = (0,   180, 0)
FERRARI_EXIT_RED = (200, 0,   0)
DARK             = (20,  10,  10)

SEL_BG        = (10,  10,  24)
SEL_PANEL_BG  = (18,  18,  38)
SEL_BORDER    = (50,  50,  90)
SEL_GOLD      = (255, 215,  0)
SEL_GOLD_DIM  = (180, 140,  0)
SEL_P1        = (220,  60,  60)
SEL_P2        = ( 60, 120, 255)
SEL_WHITE     = (230, 230, 240)
SEL_MUTED     = (110, 110, 140)
SEL_NAV_BG    = ( 30,  30,  55)
SEL_NAV_HOVER = ( 55,  55,  90)

LAP_ACCENT    = ( 80, 200, 255)
LAP_CARD_BG   = ( 14,  22,  42)
LAP_CARD_SEL  = ( 20,  36,  70)
LAP_CARD_BRD  = ( 40,  80, 160)
LAP_CARD_ABRD = ( 80, 160, 255)

try:
    title_font     = pygame.font.SysFont("Impact", 62)
    button_font    = pygame.font.SysFont("Georgia", 30, bold=True)
    sel_title_font = pygame.font.SysFont("Impact", 52)
    sel_name_font  = pygame.font.SysFont("Impact", 18)
    sel_label_font = pygame.font.SysFont("Arial",  13, bold=True)
    sel_idx_font   = pygame.font.SysFont("Arial",  10)
    sel_sub_font   = pygame.font.SysFont("Arial",  10)
    sel_nav_font   = pygame.font.SysFont("Impact", 22)
    sel_warn_font  = pygame.font.SysFont("Arial",  11, bold=True)
    sel_vs_font    = pygame.font.SysFont("Impact", 28)
    sel_race_font  = pygame.font.SysFont("Impact", 24)
    sel_back_font  = pygame.font.SysFont("Impact", 18)
    lap_big_font   = pygame.font.SysFont("Impact", 72)
    lap_tag_font   = pygame.font.SysFont("Impact", 14)
    lap_hint_font  = pygame.font.SysFont("Arial",  11)
    lap_tab_font   = pygame.font.SysFont("Impact", 15)
except Exception:
    title_font     = pygame.font.SysFont("arial", 62, bold=True)
    button_font    = pygame.font.SysFont("arial", 30, bold=True)
    sel_title_font = pygame.font.SysFont("arial", 52, bold=True)
    sel_name_font  = pygame.font.SysFont("arial", 18, bold=True)
    sel_label_font = pygame.font.SysFont("arial", 13, bold=True)
    sel_idx_font   = pygame.font.SysFont("arial", 10)
    sel_sub_font   = pygame.font.SysFont("arial", 10)
    sel_nav_font   = pygame.font.SysFont("arial", 22, bold=True)
    sel_warn_font  = pygame.font.SysFont("arial", 11, bold=True)
    sel_vs_font    = pygame.font.SysFont("arial", 28, bold=True)
    sel_race_font  = pygame.font.SysFont("arial", 24, bold=True)
    sel_back_font  = pygame.font.SysFont("arial", 18, bold=True)
    lap_big_font   = pygame.font.SysFont("arial", 72, bold=True)
    lap_tag_font   = pygame.font.SysFont("arial", 14, bold=True)
    lap_hint_font  = pygame.font.SysFont("arial", 11)
    lap_tab_font   = pygame.font.SysFont("arial", 15, bold=True)


# ── Shared helpers

def draw_shadow_text(screen, text, font, color, x, y):
    screen.blit(font.render(text, True, BLACK), (x + 4, y + 4))
    screen.blit(font.render(text, True, color), (x, y))


def draw_button(screen, rect, text, base_color, mouse_pos):
    if rect.collidepoint(mouse_pos):
        glow = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*base_color, 120), glow.get_rect(), border_radius=14)
        screen.blit(glow, (rect.x - 10, rect.y - 10))
    pygame.draw.rect(screen, base_color, rect, border_radius=14)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=14)
    txt = button_font.render(text, True, BLACK)
    screen.blit(txt, txt.get_rect(center=rect.center))


# ── Car selection helpers

def _draw_grid(surf, w, h):
    grid_col = (20, 20, 44)
    for x in range(0, w, 40):
        pygame.draw.line(surf, grid_col, (x, 0), (x, h), 1)
    for y in range(0, h, 40):
        pygame.draw.line(surf, grid_col, (0, y), (w, y), 1)


def _draw_rounded_rect(surf, color, rect, radius=10, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)


def _draw_dot_indicators(surf, cx, y, count, active, active_color):
    dot_r, active_w, spacing = 4, 14, 11
    start_x = cx - ((count - 1) * spacing + active_w) // 2
    for i in range(count):
        ox = start_x + i * spacing
        if i == active:
            rect = pygame.Rect(ox, y - dot_r, active_w, dot_r * 2)
            pygame.draw.rect(surf, active_color, rect, border_radius=dot_r)
            glow_surf = pygame.Surface((active_w + 8, dot_r * 2 + 8), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*active_color, 60),
                             glow_surf.get_rect(), border_radius=dot_r + 2)
            surf.blit(glow_surf, (ox - 4, y - dot_r - 4))
        else:
            pygame.draw.circle(surf, (60, 60, 100), (ox + dot_r, y), dot_r - 1)


def _draw_spotlight(surf, cx, cy, r_x, r_y, color):
    spot = pygame.Surface((r_x * 2, r_y * 2), pygame.SRCALPHA)
    for step in range(8, 0, -1):
        ex = int(r_x * step / 8)
        ey = int(r_y * step / 8)
        pygame.draw.ellipse(spot, (*color, int(18 * step)),
                            (r_x - ex, r_y - ey, ex * 2, ey * 2))
    surf.blit(spot, (cx - r_x, cy - r_y))


def _draw_car_shadow(surf, cx, cy):
    shadow = pygame.Surface((90, 22), pygame.SRCALPHA)
    for i in range(5):
        pygame.draw.ellipse(shadow, (0, 0, 0, 30 - i * 5),
                            (i * 4, i * 2, 90 - i * 8, 22 - i * 3))
    surf.blit(shadow, (cx - 45, cy - 11))


def _draw_player_panel(surf, px, py, pw, ph, player_idx,
                       car_index, float_offset, hover_nav, t):
    data    = CAR_DATA[car_index]
    p_color = SEL_P1 if player_idx == 0 else SEL_P2
    p_label = "PLAYER 1" if player_idx == 0 else "PLAYER 2"
    p_num   = "1" if player_idx == 0 else "2"

    panel_rect = pygame.Rect(px, py, pw, ph)
    _draw_rounded_rect(surf, SEL_PANEL_BG, panel_rect, radius=14,
                       border=1, border_color=SEL_BORDER)
    pygame.draw.rect(surf, p_color,
                     pygame.Rect(px + 14, py, pw - 28, 3), border_radius=2)

    header_h    = 36
    header_surf = pygame.Surface((pw, header_h), pygame.SRCALPHA)
    header_surf.fill((*p_color, 28))
    surf.blit(header_surf, (px, py))
    pygame.draw.line(surf, (*SEL_BORDER, 200),
                     (px, py + header_h), (px + pw, py + header_h), 1)

    dot_x, dot_y = px + 14, py + header_h // 2
    pygame.draw.circle(surf, p_color, (dot_x, dot_y), 5)
    glow_s = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(glow_s, (*p_color, int(60 + 40 * math.sin(t * 3))), (10, 10), 9)
    surf.blit(glow_s, (dot_x - 10, dot_y - 10))
    lbl_surf = sel_label_font.render(p_label, True, p_color)
    surf.blit(lbl_surf, (px + 26, dot_y - lbl_surf.get_height() // 2))

    ghost = sel_vs_font.render(p_num, True, (255, 255, 255))
    ghost.set_alpha(18)
    surf.blit(ghost, (px + pw - ghost.get_width() - 10, py + 4))

    showcase_y  = py + header_h
    showcase_h  = 155
    showcase_cx = px + pw // 2
    _draw_spotlight(surf, showcase_cx, showcase_y + showcase_h - 30,
                    70, 28, data["color"])
    scaled_car = pygame.transform.rotozoom(CAR_OPTIONS[car_index], 0, 1.18)
    scw, sch   = scaled_car.get_width(), scaled_car.get_height()
    surf.blit(scaled_car, (showcase_cx - scw // 2,
                           showcase_y + (showcase_h - sch) // 2 - 8 + int(float_offset)))
    _draw_car_shadow(surf, showcase_cx, showcase_y + showcase_h - 18)

    swatch_rect = pygame.Rect(px + pw - 20, showcase_y + 8, 12, 12)
    pygame.draw.rect(surf, data["color"], swatch_rect, border_radius=6)
    pygame.draw.rect(surf, WHITE, swatch_rect, 1, border_radius=6)

    pygame.draw.line(surf, SEL_BORDER,
                     (px, showcase_y + showcase_h),
                     (px + pw, showcase_y + showcase_h), 1)

    info_y   = showcase_y + showcase_h
    info_pad = 12

    name_surf = sel_name_font.render(data["name"], True, SEL_WHITE)
    surf.blit(name_surf, (px + pw // 2 - name_surf.get_width() // 2, info_y + 10))

    idx_surf = sel_idx_font.render(f"{car_index + 1} / {len(CAR_OPTIONS)}", True, SEL_MUTED)
    surf.blit(idx_surf, (px + pw - idx_surf.get_width() - info_pad, info_y + 13))

    nav_y      = info_y + 36
    btn_sz     = 34
    left_rect  = pygame.Rect(px + info_pad, nav_y, btn_sz, btn_sz)
    right_rect = pygame.Rect(px + pw - info_pad - btn_sz, nav_y, btn_sz, btn_sz)

    for btn_rect, symbol, is_hovered in [
        (left_rect,  "<", hover_nav == 0),
        (right_rect, ">", hover_nav == 1),
    ]:
        _draw_rounded_rect(surf,
                           SEL_NAV_HOVER if is_hovered else SEL_NAV_BG,
                           btn_rect, radius=8)
        pygame.draw.rect(surf, p_color if is_hovered else SEL_BORDER,
                         btn_rect, 1, border_radius=8)
        sym_surf = sel_nav_font.render(symbol, True,
                                       p_color if is_hovered else SEL_WHITE)
        surf.blit(sym_surf, sym_surf.get_rect(center=btn_rect.center))

    _draw_dot_indicators(surf, px + pw // 2, nav_y + btn_sz // 2,
                         len(CAR_OPTIONS), car_index, p_color)
    return left_rect, right_rect


# ── Lap page helpers

LAP_HINTS = {
    1: ("Quick Sprint",  "One lap — fastest wins!"),
    3: ("Standard Race", "The classic three-lap challenge."),
    5: ("Grand Prix",    "Five laps — endurance and strategy."),
}


def _draw_lap_card(surf, cx, cy, lap_val, is_selected, hover, t):
    CW, CH = 140, 170
    rx, ry = cx - CW // 2, cy - CH // 2
    card_rect = pygame.Rect(rx, ry, CW, CH)

    bg  = LAP_CARD_SEL  if is_selected else LAP_CARD_BG
    brd = LAP_CARD_ABRD if is_selected else (LAP_CARD_BRD if not hover else (60, 120, 200))
    brd_w = 2 if is_selected else 1
    pygame.draw.rect(surf, bg, card_rect, border_radius=14)
    pygame.draw.rect(surf, brd, card_rect, brd_w, border_radius=14)

    if is_selected:
        pulse = int(30 + 20 * math.sin(t * 3))
        glow  = pygame.Surface((CW + 24, CH + 24), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*LAP_ACCENT, pulse), glow.get_rect(), border_radius=18)
        surf.blit(glow, (rx - 12, ry - 12))
        pygame.draw.rect(surf, bg, card_rect, border_radius=14)
        pygame.draw.rect(surf, brd, card_rect, brd_w, border_radius=14)

    stripe_col = LAP_ACCENT if is_selected else (40, 60, 100)
    pygame.draw.rect(surf, stripe_col,
                     pygame.Rect(rx + 14, ry, CW - 28, 3), border_radius=2)

    num_col  = LAP_ACCENT if is_selected else SEL_MUTED
    num_surf = lap_big_font.render(str(lap_val), True, num_col)
    surf.blit(num_surf, (cx - num_surf.get_width() // 2, ry + 18))

    unit     = "LAP" if lap_val == 1 else "LAPS"
    unit_col = SEL_WHITE if is_selected else (80, 90, 120)
    unit_s   = lap_tag_font.render(unit, True, unit_col)
    surf.blit(unit_s, (cx - unit_s.get_width() // 2, ry + 88))

    pygame.draw.line(surf, (30, 45, 80),
                     (rx + 16, ry + 108), (rx + CW - 16, ry + 108), 1)

    title, hint = LAP_HINTS[lap_val]
    title_col   = LAP_ACCENT if is_selected else SEL_WHITE
    title_s     = lap_hint_font.render(title, True, title_col)
    hint_s      = lap_hint_font.render(hint,  True, SEL_MUTED)
    surf.blit(title_s, (cx - title_s.get_width() // 2, ry + 118))
    surf.blit(hint_s,  (cx - hint_s.get_width()  // 2, ry + 136))

    if is_selected:
        tick_rect = pygame.Rect(rx + CW - 26, ry + 8, 18, 18)
        pygame.draw.rect(surf, LAP_ACCENT, tick_rect, border_radius=9)
        tick_s = lap_tag_font.render("v", True, BLACK)
        surf.blit(tick_s, tick_s.get_rect(center=tick_rect.center))

    return card_rect


def _draw_lap_page(surf, W, H, t, mouse, lap_idx):
    title_s = sel_title_font.render("RACE LENGTH", True, SEL_GOLD)
    title_s.set_alpha(220)
    t_sh = sel_title_font.render("RACE LENGTH", True, BLACK)
    t_sh.set_alpha(100)
    tx = W // 2 - title_s.get_width() // 2
    surf.blit(t_sh, (tx + 3, 33))
    surf.blit(title_s, (tx, 30))

    ul_w = title_s.get_width() + 40
    ul_x = W // 2 - ul_w // 2
    ul_y = 30 + title_s.get_height() + 4
    pygame.draw.line(surf, SEL_GOLD_DIM, (ul_x, ul_y), (ul_x + ul_w, ul_y), 2)
    pygame.draw.circle(surf, SEL_GOLD, (ul_x, ul_y), 3)
    pygame.draw.circle(surf, SEL_GOLD, (ul_x + ul_w, ul_y), 3)

    sub = sel_sub_font.render("HOW MANY LAPS DO YOU WANT TO RACE?", True, SEL_MUTED)
    surf.blit(sub, (W // 2 - sub.get_width() // 2, ul_y + 18))

    CARD_CY  = H // 2 - 10
    CARD_GAP = 170
    centres  = [W // 2 - CARD_GAP, W // 2, W // 2 + CARD_GAP]
    clickables = []

    for i, (lap_val, cx) in enumerate(zip(LAP_CHOICES, centres)):
        is_sel = (i == lap_idx)
        hover  = pygame.Rect(cx - 70, CARD_CY - 85, 140, 170).collidepoint(mouse)
        rect   = _draw_lap_card(surf, cx, CARD_CY, lap_val, is_sel, hover, t)
        clickables.append((rect, i))

    inst = sel_sub_font.render(
        "Click a card to choose  •  current selection highlighted in blue",
        True, (55, 65, 95))
    surf.blit(inst, (W // 2 - inst.get_width() // 2, CARD_CY + 105))
    return clickables


def _draw_tab_bar(surf, W, active_page, slide_x, t):
    TAB_W, TAB_H = 160, 32
    TAB_Y        = 62
    TAB_GAP      = 12
    total        = TAB_W * 2 + TAB_GAP
    t0_x         = W // 2 - total // 2
    t1_x         = t0_x + TAB_W + TAB_GAP

    for tx, label, idx in [(t0_x, "SELECT CAR", 0), (t1_x, "RACE LENGTH", 1)]:
        rect   = pygame.Rect(tx, TAB_Y, TAB_W, TAB_H)
        is_act = (idx == active_page)
        pygame.draw.rect(surf, (30, 50, 90) if is_act else (18, 18, 38),
                         rect, border_radius=8)
        pygame.draw.rect(surf, LAP_ACCENT if is_act else SEL_BORDER,
                         rect, 2 if is_act else 1, border_radius=8)
        if is_act:
            pygame.draw.rect(surf, LAP_ACCENT,
                             pygame.Rect(tx + 12, TAB_Y + TAB_H - 3, TAB_W - 24, 3),
                             border_radius=2)
        lbl_s = lap_tab_font.render(label, True, SEL_WHITE if is_act else SEL_MUTED)
        surf.blit(lbl_s, lbl_s.get_rect(center=rect.center))

    bar_y  = TAB_Y + TAB_H + 4
    bar_x0 = W // 2 - total // 2
    bar_x1 = bar_x0 + total
    pygame.draw.line(surf, (30, 30, 60), (bar_x0, bar_y), (bar_x1, bar_y), 1)
    seg_w  = total // 2
    seg_x  = bar_x0 + int(slide_x * seg_w)
    pygame.draw.line(surf, LAP_ACCENT, (seg_x, bar_y), (seg_x + seg_w, bar_y), 2)

    return (pygame.Rect(t0_x, TAB_Y, TAB_W, TAB_H),
            pygame.Rect(t1_x, TAB_Y, TAB_W, TAB_H))


# ── Main menu

def show_menu():
    buttons = ["PLAY", "OPTIONS", "EXIT"]
    rects = [
        pygame.Rect(WIDTH // 2 - 110, 280, 220, 60),
        pygame.Rect(WIDTH // 2 - 110, 360, 220, 60),
        pygame.Rect(WIDTH // 2 - 110, 440, 220, 60),
    ]

    # Logo animation variables
    logo_scale = 0.0
    logo_target_scale = 0.20  # Smaller scale (was 0.35)
    logo_alpha = 0

    menu_surf = responsive.get_base_surface()

    # Load the new menu background and logo
    try:
        background = pygame.transform.scale(
            pygame.image.load("imgs/RACING_MASTER_BG.jpg"), (WIDTH, HEIGHT))
    except:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill((30, 30, 50))

    # Load and prepare the logo
    try:
        logo_raw = pygame.image.load("imgs/racing_master_logo.png")
    except:
        logo_raw = None

    clock = pygame.time.Clock()
    while True:
        menu_surf.blit(background, (0, 0))

        # Subtle dark overlay for better contrast
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(60)  # Even lighter overlay
        overlay.fill(BLACK)
        menu_surf.blit(overlay, (0, 0))

        # Animate logo appearance
        if logo_scale < logo_target_scale:
            logo_scale += 0.015
            if logo_scale > logo_target_scale:
                logo_scale = logo_target_scale
        if logo_alpha < 255:
            logo_alpha += 5
            if logo_alpha > 255:
                logo_alpha = 255

        # Draw the logo with animation - positioned at top
        if logo_raw:
            logo_w = int(logo_raw.get_width() * logo_scale)
            logo_h = int(logo_raw.get_height() * logo_scale)
            logo_scaled = pygame.transform.smoothscale(logo_raw, (logo_w, logo_h))

            # Apply fade-in effect
            if logo_alpha < 255:
                logo_scaled.set_alpha(logo_alpha)

            logo_x = (WIDTH - logo_w) // 2
            logo_y = -50  # Higher position
            menu_surf.blit(logo_scaled, (logo_x, logo_y))

        raw_mouse = pygame.mouse.get_pos()
        mouse = responsive.scale_pos(raw_mouse)

        for i, rect in enumerate(rects):
            color = FERRARI_YELLOW if i == 0 else FERRARI_GREEN if i == 1 else FERRARI_EXIT_RED
            draw_button(menu_surf, rect, buttons[i], color, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            responsive.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = responsive.scale_pos(event.pos)
                for i, rect in enumerate(rects):
                    if rect.collidepoint(click):
                        if buttons[i] == "PLAY": turbo_sound.play(); return
                        elif buttons[i] == "EXIT":
                            exit_sound.play(); time.sleep(1); pygame.quit(); sys.exit()
                        elif buttons[i] == "OPTIONS":
                            click_sound2.play();pygame.mixer.music.set_volume(0.35); options_menu(WIN, clock)

        responsive.flip()
        clock.tick(60)



# ── Options menu (two-page with slide transition)

def options_menu(win, clock):
    global player1_car_index, player2_car_index
    global lap_choice_index, selected_laps

    menu_surf = responsive.get_base_surface()
    W, H      = WIDTH, HEIGHT

    PANEL_W = min(230, W // 3)
    PANEL_H = 340
    PANEL_Y = 118
    GAP     = 40
    START_X = W // 2 - (PANEL_W * 2 + GAP + 60) // 2
    P1_X    = START_X
    VS_CX   = START_X + PANEL_W + GAP // 2 + 30
    P2_X    = VS_CX + 30 + GAP // 2

    RACE_W, RACE_H = 180, 52
    BACK_W, BACK_H = 110, 42
    RACE_RECT = pygame.Rect(W // 2 - RACE_W // 2, PANEL_Y + PANEL_H + 36, RACE_W, RACE_H)
    BACK_RECT = pygame.Rect(W // 2 - BACK_W // 2, RACE_RECT.bottom + 12, BACK_W, BACK_H)

    def _nav_rects(px):
        nav_y    = PANEL_Y + 36 + 155 + 1 + 36 + 10
        info_pad = 12
        btn_sz   = 34
        return (pygame.Rect(px + info_pad, nav_y, btn_sz, btn_sz),
                pygame.Rect(px + PANEL_W - info_pad - btn_sz, nav_y, btn_sz, btn_sz))

    current_page   = 0
    slide_x        = 0.0
    slide_target   = 0.0
    content_offset = 0.0
    content_target = 0.0
    title_alpha    = 0
    warn_flash_t   = 0.0

    while True:
        t  = pygame.time.get_ticks() / 1000.0
        dt = clock.tick(60) / 1000.0

        ease = 1 - (0.75 ** (dt * 60))
        slide_x        += (slide_target  - slide_x)        * ease
        content_offset += (content_target - content_offset) * ease

        p1_float = math.sin(t * 2.2) * 7
        p2_float = math.sin(t * 2.2 + 1.4) * 7
        if title_alpha < 255:
            title_alpha = min(255, title_alpha + 8)

        mouse = responsive.scale_pos(pygame.mouse.get_pos())

        menu_surf.fill(SEL_BG)
        _draw_grid(menu_surf, W, H)
        glow_strip = pygame.Surface((W, 3), pygame.SRCALPHA)
        glow_strip.fill((*SEL_GOLD, 90))
        menu_surf.blit(glow_strip, (0, 0))

        tab0_rect, tab1_rect = _draw_tab_bar(menu_surf, W, current_page, slide_x, t)

        off = int(content_offset)

        # ── Page 0: car selection
        page0 = pygame.Surface((W, H), pygame.SRCALPHA)
        t_surf = sel_title_font.render("SELECT YOUR CAR", True, SEL_GOLD)
        t_surf.set_alpha(title_alpha)
        t_sh = sel_title_font.render("SELECT YOUR CAR", True, BLACK)
        t_sh.set_alpha(int(title_alpha * 0.6))
        tx = W // 2 - t_surf.get_width() // 2
        page0.blit(t_sh, (tx + 3, 33))
        page0.blit(t_surf, (tx, 30))
        ul_w = t_surf.get_width() + 40
        ul_x = W // 2 - ul_w // 2
        ul_y = 30 + t_surf.get_height() + 4
        pygame.draw.line(page0, SEL_GOLD_DIM, (ul_x, ul_y), (ul_x + ul_w, ul_y), 2)
        pygame.draw.circle(page0, SEL_GOLD, (ul_x, ul_y), 3)
        pygame.draw.circle(page0, SEL_GOLD, (ul_x + ul_w, ul_y), 3)
        sub = sel_sub_font.render("CHOOSE YOUR RIDE  •  PRESS RACE TO START", True, SEL_MUTED)
        page0.blit(sub, (W // 2 - sub.get_width() // 2, ul_y + 10))

        p1_l, p1_r = _nav_rects(P1_X)
        p2_l, p2_r = _nav_rects(P2_X)
        if current_page == 0:
            p1_hover = 0 if p1_l.collidepoint(mouse) else 1 if p1_r.collidepoint(mouse) else -1
            p2_hover = 0 if p2_l.collidepoint(mouse) else 1 if p2_r.collidepoint(mouse) else -1
        else:
            p1_hover = p2_hover = -1

        p1_left, p1_right = _draw_player_panel(
            page0, P1_X, PANEL_Y, PANEL_W, PANEL_H,
            0, player1_car_index, p1_float, p1_hover, t)
        p2_left, p2_right = _draw_player_panel(
            page0, P2_X, PANEL_Y, PANEL_W, PANEL_H,
            1, player2_car_index, p2_float, p2_hover, t)

        vs_top = PANEL_Y + 20
        vs_bot = PANEL_Y + PANEL_H - 20
        vs_mid = (vs_top + vs_bot) // 2
        for sy in range(vs_top, vs_mid - 20, 16):
            pygame.draw.line(page0, SEL_BORDER, (VS_CX, sy), (VS_CX, sy + 8), 1)
        for sy in range(vs_mid + 22, vs_bot, 16):
            pygame.draw.line(page0, SEL_BORDER, (VS_CX, sy), (VS_CX, sy + 8), 1)
        vs_r = 22 + int(4 * math.sin(t * 2.5))
        pygame.draw.circle(page0, (60,  20, 20), (VS_CX, vs_mid), vs_r + 3)
        pygame.draw.circle(page0, (160, 30, 30), (VS_CX, vs_mid), vs_r)
        pygame.draw.circle(page0, (220, 50, 50), (VS_CX, vs_mid), vs_r, 1)
        vs_s = sel_vs_font.render("VS", True, (255, 220, 220))
        page0.blit(vs_s, vs_s.get_rect(center=(VS_CX, vs_mid)))

        same_car = (player1_car_index == player2_car_index)
        if same_car:
            warn_flash_t += dt
            w_surf = sel_warn_font.render("  SAME CAR SELECTED", True, (255, 140, 60))
            w_surf.set_alpha(int(160 + 95 * math.sin(warn_flash_t * 5)))
            page0.blit(w_surf, (W // 2 - w_surf.get_width() // 2, PANEL_Y + PANEL_H + 10))
        else:
            warn_flash_t = 0.0

        race_hovered = RACE_RECT.collidepoint(mouse) and current_page == 0
        race_col     = (240, 210, 40) if race_hovered else ((200, 160, 0) if same_car else (220, 175, 0))
        if race_hovered:
            glow_r = pygame.Surface((RACE_W + 30, RACE_H + 30), pygame.SRCALPHA)
            pygame.draw.rect(glow_r, (*race_col, 55), glow_r.get_rect(), border_radius=18)
            page0.blit(glow_r, (RACE_RECT.x - 15, RACE_RECT.y - 15))
        pygame.draw.rect(page0, race_col, RACE_RECT, border_radius=12)
        pygame.draw.rect(page0, BLACK, RACE_RECT, 2, border_radius=12)
        shimmer_x    = int((t % 2.0) / 2.0 * (RACE_W + 60)) - 30
        shim_surf    = pygame.Surface((RACE_W, RACE_H), pygame.SRCALPHA)
        clipped_poly = [(max(0, min(RACE_W, bx)), by) for bx, by in [
            (shimmer_x, 0), (shimmer_x + 20, 0),
            (shimmer_x + 30, RACE_H), (shimmer_x + 10, RACE_H),
        ]]
        if len(clipped_poly) == 4:
            pygame.draw.polygon(shim_surf, (255, 255, 255, 55), clipped_poly)
        page0.blit(shim_surf, RACE_RECT.topleft)
        r_text = sel_race_font.render(" LETS RACE!", True, (20, 12, 0))
        page0.blit(r_text, r_text.get_rect(center=RACE_RECT.center))

        back_hovered = BACK_RECT.collidepoint(mouse) and current_page == 0
        _draw_rounded_rect(page0, (50, 50, 80) if back_hovered else (30, 30, 55),
                           BACK_RECT, radius=8)
        pygame.draw.rect(page0, (120, 120, 170) if back_hovered else SEL_BORDER,
                         BACK_RECT, 1, border_radius=8)
        b_text = sel_back_font.render("  BACK", True,
                                      (200, 200, 220) if back_hovered else SEL_MUTED)
        page0.blit(b_text, b_text.get_rect(center=BACK_RECT.center))

        hint = sel_idx_font.render("P1: <- -> ARROWS     P2: A D KEYS", True, (60, 60, 90))
        page0.blit(hint, (W // 2 - hint.get_width() // 2, H - 22))

        # ── Page 1: lap selector
        page1 = pygame.Surface((W, H), pygame.SRCALPHA)
        lap_mouse      = mouse if current_page == 1 else (-1, -1)
        lap_clickables = _draw_lap_page(page1, W, H, t, lap_mouse, lap_choice_index)

        lap_back_rect = pygame.Rect(W // 2 - BACK_W // 2, H - 70, BACK_W, BACK_H)
        lb_hovered = lap_back_rect.collidepoint(mouse) and current_page == 1
        _draw_rounded_rect(page1, (50, 50, 80) if lb_hovered else (30, 30, 55),
                           lap_back_rect, radius=8)
        pygame.draw.rect(page1, (120, 120, 170) if lb_hovered else SEL_BORDER,
                         lap_back_rect, 1, border_radius=8)
        lb_text = sel_back_font.render("  BACK", True,
                                       (200, 200, 220) if lb_hovered else SEL_MUTED)
        page1.blit(lb_text, lb_text.get_rect(center=lap_back_rect.center))

        # Blit both pages with clip below the tab bar
        clip_rect = pygame.Rect(0, 112, W, H - 112)
        menu_surf.set_clip(clip_rect)
        menu_surf.blit(page0, (off,     0))
        menu_surf.blit(page1, (off + W, 0))
        menu_surf.set_clip(None)

        # Tab bar always on top
        _draw_tab_bar(menu_surf, W, current_page, slide_x, t)

        responsive.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            responsive.handle_event(event)

            if event.type == pygame.KEYDOWN:
                click_sound2.play()
                if event.key == pygame.K_q and current_page == 1:
                    current_page = 0; slide_target = 0.0; content_target = 0.0
                if event.key == pygame.K_e and current_page == 0:
                    current_page = 1; slide_target = 1.0; content_target = -W
                if current_page == 0:
                    click_sound2.play()
                    if event.key == pygame.K_LEFT:
                        player1_car_index = (player1_car_index - 1) % len(CAR_OPTIONS)
                    if event.key == pygame.K_RIGHT:
                        player1_car_index = (player1_car_index + 1) % len(CAR_OPTIONS)
                    if event.key == pygame.K_a:
                        player2_car_index = (player2_car_index - 1) % len(CAR_OPTIONS)
                    if event.key == pygame.K_d:
                        player2_car_index = (player2_car_index + 1) % len(CAR_OPTIONS)
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound2.play()
                click = responsive.scale_pos(event.pos)
                if tab0_rect.collidepoint(click) and current_page != 0:
                    current_page = 0; slide_target = 0.0; content_target = 0.0
                elif tab1_rect.collidepoint(click) and current_page != 1:
                    current_page = 1; slide_target = 1.0; content_target = -W
                elif current_page == 0:
                    if p1_left.collidepoint(click):
                        player1_car_index = (player1_car_index - 1) % len(CAR_OPTIONS)
                    if p1_right.collidepoint(click):
                        player1_car_index = (player1_car_index + 1) % len(CAR_OPTIONS)
                    if p2_left.collidepoint(click):
                        player2_car_index = (player2_car_index - 1) % len(CAR_OPTIONS)
                    if p2_right.collidepoint(click):
                        player2_car_index = (player2_car_index + 1) % len(CAR_OPTIONS)
                    if RACE_RECT.collidepoint(click):
                        turbo_sound.play(); return
                    if BACK_RECT.collidepoint(click):
                        return
                elif current_page == 1:
                    for card_rect, lap_idx in lap_clickables:
                        if card_rect.collidepoint(click):
                            lap_choice_index = lap_idx
                            selected_laps    = LAP_CHOICES[lap_idx]
                    if lap_back_rect.collidepoint(click):
                        return

# ── Game classes

class GameInfo:
    def __init__(self, level=1):
        self.level            = level
        self.started          = False
        self.level_start_time = 0
        self.LEVELS           = selected_laps

    def next_level(self):    self.level += 1; self.started = False
    def reset(self):
        self.level   = 1
        self.started = False
        self.LEVELS  = selected_laps

    def game_finished(self): return self.level > self.LEVELS

    def start_level(self):
        self.started          = True
        self.level_start_time = time.time()

    def get_level_time(self):
        return 0 if not self.started else round(time.time() - self.level_start_time)


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img              = self.IMG
        self.max_vel          = max_vel
        self.vel              = 0
        self.rotation_vel     = rotation_vel
        self.angle            = 0
        self.x, self.y        = self.START_POS
        self.acceleration     = 0.2
        self.nitro_active     = False
        self.nitro_start_time = 0
        self.normal_max_vel   = max_vel

    def rotate(self, left=False, right=False):
        if left:  self.angle += self.rotation_vel
        if right: self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel); self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2); self.move()

    def move(self):
        radians = math.radians(self.angle)
        self.x -= math.cos(radians) * self.vel
        self.y += math.sin(radians) * self.vel

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        return mask.overlap(car_mask, (int(self.x - x), int(self.y - y)))

    def reset(self):
        self.x, self.y    = self.START_POS
        self.angle        = 0
        self.vel          = 0
        self.nitro_active = False
        self.max_vel      = self.normal_max_vel


class PlayerCar(AbstractCar):
    START_POS = P1_START

    def __init__(self, max_vel, rotation_vel, img):
        self.IMG = img
        super().__init__(max_vel, rotation_vel)
        self.img = img

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0); self.move()

    def bounce(self):
        self.vel = -self.vel; sound.play(); self.move()

    def activate_nitro(self):
        if self.nitro_active: return
        self.nitro_active     = True
        self.nitro_start_time = time.time()
        nitro_sound.play()
        self.max_vel = self.normal_max_vel * 2

    def update_nitro(self):
        if self.nitro_active and time.time() - self.nitro_start_time > 2:
            self.nitro_active = False
            self.max_vel      = self.normal_max_vel


class PlayerCar2(AbstractCar):
    START_POS = P2_START

    def __init__(self, max_vel, rotation_vel, img):
        self.IMG = img
        super().__init__(max_vel, rotation_vel)
        self.img = img

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0); self.move()

    def bounce(self):
        self.vel = -self.vel; sound.play(); self.move()

    def activate_nitro(self):
        self.nitro_active     = True
        self.nitro_start_time = time.time()
        nitro_sound.play()
        self.max_vel = self.normal_max_vel * 2

    def update_nitro(self):
        if self.nitro_active and time.time() - self.nitro_start_time > 2:
            self.nitro_active = False
            self.max_vel      = self.normal_max_vel


class ComputerCar(AbstractCar):
    IMG       = MODERN_PINK_CAR
    START_POS = AI_START

    def __init__(self, max_vel, rotation_vel, path):
        super().__init__(max_vel, rotation_vel)
        self.path          = path
        self.current_point = 0
        self.vel           = max_vel

    def reset(self):
        super().reset()
        self.current_point = 0
        self.vel = self.max_vel

    def draw(self, win): super().draw(win)

    def bounce(self):
        self.vel = -self.vel; sound.play(); self.move()

    def activate_nitro(self):
        self.nitro_active = True
        self.nitro_start_time = time.time()
        nitro_sound.play()

        self.vel = min(self.vel * 1.5, self.max_vel)
        self.vel = self.max_vel

    def update_nitro(self):
        if self.nitro_active and time.time() - self.nitro_start_time > 2:
            self.nitro_active = False
            self.max_vel      = self.normal_max_vel

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        diff = (math.degrees(math.atan2(target_y - self.y, -(target_x - self.x)))
                - self.angle + 180) % 360 - 180
        self.angle += min(self.rotation_vel, diff) if diff > 0 else max(-self.rotation_vel, diff)

    def update_path_point(self):
        if math.hypot(self.x - self.path[self.current_point][0],
                      self.y - self.path[self.current_point][1]) < 25:
            self.current_point = (self.current_point + 1) % len(self.path)

    def move(self):
        if not self.path or self.current_point >= len(self.path): return
        self.calculate_angle(); self.update_path_point(); super().move()

    def next_level(self, level):
        self.reset()
        self.vel           = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

# ── Game logic

def reset_nitros():
    global active_nitros
    active_nitros = NITRO_POSITIONS.copy()


def draw_hud(win, player_car, player_car2, game_info):
    hud_y    = TRACK_H
    hud_surf = pygame.Surface((WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
    hud_surf.fill((10, 10, 30, 230))
    win.blit(hud_surf, (0, hud_y))
    pygame.draw.line(win, (60, 120, 255), (0, hud_y), (WIDTH, hud_y), 2)
    col_w = WIDTH // 4
    cy    = hud_y + HUD_HEIGHT // 2
    items = [
        ("LAP",    f"{game_info.level} / {game_info.LEVELS}", (180, 220, 255)),
        ("TIME",   f"{game_info.get_level_time()}s",           (140, 255, 180)),
        ("P1 VEL", f"{round(player_car.vel,  1)} px/s",       (255, 210,  80)),
        ("P2 VEL", f"{round(player_car2.vel, 1)} px/s",       ( 80, 210, 255)),
    ]
    for i, (label, value, color) in enumerate(items):
        cx = col_w * i + col_w // 2
        if i > 0:
            pygame.draw.line(win, (50, 70, 130),
                             (col_w * i, hud_y + 10),
                             (col_w * i, hud_y + HUD_HEIGHT - 10), 1)
        win.blit(LABEL_FONT.render(label, True, (150, 170, 220)),
                 LABEL_FONT.render(label, True, (150, 170, 220)).get_rect(center=(cx, cy - 16)))
        win.blit(MAIN_FONT.render(value, True, color),
                 MAIN_FONT.render(value, True, color).get_rect(center=(cx, cy + 14)))


def draw(win, images, player_car, player_car2, computer_car, game_info):
    win.fill((20, 20, 20))
    for img, pos in images:
        win.blit(img, pos)
    for nitro in active_nitros:
        rotated = pygame.transform.rotate(NITRO_IMG, nitro_angle)
        rect    = rotated.get_rect(center=(nitro[0] + NITRO_IMG.get_width() // 2,
                                           nitro[1] + NITRO_IMG.get_height() // 2))
        win.blit(rotated, rect.topleft)
        win.blit(rotated, (rect.x, rect.y + offset))
    draw_hud(win, player_car, player_car2, game_info)
    player_car.draw(win)
    player_car2.draw(win)
    computer_car.draw(win)
    responsive.flip()

    if PATH_RECORDING:
        for i, point in enumerate(computer_car.path):
            pygame.draw.circle(win, (255, 0, 0), point, 6)
            if i > 0:
                pygame.draw.line(win, (255, 100, 0),
                                 computer_car.path[i - 1], point, 2)


def move_player(player_car, player_car2):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:     player_car2.move_forward()
    if keys[pygame.K_s]:     player_car2.move_backward()
    if keys[pygame.K_a]:     player_car2.rotate(left=True)
    if keys[pygame.K_d]:     player_car2.rotate(right=True)
    if keys[pygame.K_UP]:    player_car.move_forward()
    if keys[pygame.K_DOWN]:  player_car.move_backward()
    if keys[pygame.K_RIGHT]: player_car.rotate(right=True)
    if keys[pygame.K_LEFT]:  player_car.rotate(left=True)
    if not keys[pygame.K_UP]  and not keys[pygame.K_DOWN]: player_car.reduce_speed()
    if not keys[pygame.K_w]   and not keys[pygame.K_s]:    player_car2.reduce_speed()


def _level_up(player_car, player_car2, computer_car, game_info):
    for car in (player_car, player_car2):
        car.max_vel       += 0.2
        car.acceleration  += 0.03
        car.normal_max_vel = car.max_vel

    game_info.next_level()
    game_info.start_level()
    player_car.reset()
    player_car2.reset()
    reset_nitros()
    computer_car.next_level(game_info.level)


def handle_collision(player_car, player_car2, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK, TRACK_OFFSET_X, TRACK_OFFSET_Y) is not None:
        player_car.bounce()
    if player_car2.collide(TRACK_BORDER_MASK, TRACK_OFFSET_X, TRACK_OFFSET_Y) is not None:
        player_car2.bounce()
    # if computer_car.collide(TRACK_BORDER_MASK, TRACK_OFFSET_X, TRACK_OFFSET_Y) is not None:
    #     computer_car.bounce()

    if computer_car.collide(FINISH_MASK, *FINISH_POSITION) is not None:
        track_finish("AI")
        game_info.next_level()
        game_info.start_level()
        player_car.reset()
        player_car2.reset()
        reset_nitros()
        computer_car.next_level(game_info.level)
        responsive.flip()

        player_car.normal_max_vel = player_car.max_vel
        player_car2.normal_max_vel = player_car2.max_vel

        player_car2.max_vel += 0.2; player_car.max_vel += 0.2; computer_car.max_vel += 0.1
        player_car2.acceleration += 0.03; player_car.acceleration += 0.03; computer_car.acceleration += 0.03

    p1_col = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if p1_col is not None:
        if p1_col[0] == 0:
            player_car.bounce(); player_car.reset()
        else:
            track_finish("P1")
            _level_up(player_car, player_car2, computer_car, game_info)

    p2_col = player_car2.collide(FINISH_MASK, *FINISH_POSITION)
    if p2_col is not None:
        if p2_col[0] == 0:
            player_car2.bounce(); player_car2.reset()
        else:
            track_finish("P2")
            _level_up(player_car, player_car2, computer_car, game_info)

    # ai_col = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    # if ai_col is not None:
    #     if ai_col[0] == 0:
    #         computer_car.bounce(); computer_car.reset()
    #     else:
    #         _level_up(player_car, player_car2, computer_car, game_info)

    for nitro in active_nitros[:]:
        if player_car.collide(NITRO_MASK, *nitro) is not None:
            player_car.activate_nitro(); active_nitros.remove(nitro)
        elif player_car2.collide(NITRO_MASK, *nitro) is not None:
            player_car2.activate_nitro(); active_nitros.remove(nitro)
        elif computer_car.collide(NITRO_MASK, *nitro) is not None:
            computer_car.activate_nitro(); active_nitros.remove(nitro)

def start_countdown(win, images, player_car, player_car2, computer_car, game_info):
    font      = pygame.font.SysFont("impact", 120)
    countdown = ["3", "2", "1", "GO!"]
    sounds    = [count3, count2, count1, count_go]
    for i in range(4):
        start_time = pygame.time.get_ticks()
        sounds[i].play()
        while pygame.time.get_ticks() - start_time < 1000:
            draw(win, images, player_car, player_car2, computer_car, game_info)
            text = font.render(countdown[i], True, (255, 50, 50))
            win.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            responsive.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()


def pause_menu(win, clock, frozen_screen):
    menu_surf = responsive.get_base_surface()
    buttons   = ["RESUME", "RESTART", "EXIT"]
    rects     = [
        pygame.Rect(WIDTH // 2 - 110, 260, 220, 60),
        pygame.Rect(WIDTH // 2 - 110, 340, 220, 60),
        pygame.Rect(WIDTH // 2 - 110, 420, 220, 60),
    ]
    while True:
        clock.tick(60)
        menu_surf.blit(frozen_screen, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(160)
        overlay.fill(DARK)
        menu_surf.blit(overlay, (0, 0))
        draw_shadow_text(menu_surf, "RACING MASTER\n\t\tPAUSED\t\t",
                         title_font, FERRARI_YELLOW, WIDTH // 2 - 180, 80)
        mouse = responsive.scale_pos(pygame.mouse.get_pos())
        for i, rect in enumerate(rects):
            color = FERRARI_YELLOW if i == 0 else FERRARI_GREEN if i == 1 else FERRARI_EXIT_RED
            draw_button(menu_surf, rect, buttons[i], color, mouse)
        responsive.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = responsive.scale_pos(event.pos)
                if rects[0].collidepoint(click): click_sound2.play(); return "resume"
                if rects[1].collidepoint(click): click_sound2.play(); return "restart"
                if rects[2].collidepoint(click): exit_sound.play(); return "exit"
# ── Main

def main():
    show_menu()
    clock  = pygame.time.Clock()
    pygame.mixer.music.set_volume(0.30)

    images = [
        (GRASS,        (TRACK_OFFSET_X, TRACK_OFFSET_Y)),
        (FINISH,        FINISH_POSITION),
        (TRACK,        (TRACK_OFFSET_X, TRACK_OFFSET_Y)),
        (TRACK_BORDER, (TRACK_OFFSET_X, TRACK_OFFSET_Y)),
    ]

    def make_players():
        return (PlayerCar(1.5, 2, CAR_OPTIONS[player1_car_index]),
                PlayerCar2(1.5, 2, CAR_OPTIONS[player2_car_index]))

    player_car, player_car2 = make_players()
    computer_car = ComputerCar(1.4, 2.5, PATH)
    game_info    = GameInfo()

    start_countdown(WIN, images, player_car, player_car2, computer_car, game_info)
    game_info.start_level()

    run              = True
    paused           = False
    pause_start_time = 0

    while run:
        clock.tick(FPS)
        global nitro_angle
        nitro_angle = (nitro_angle + 0.25) % 360
        draw(WIN, images, player_car, player_car2, computer_car, game_info)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False; break
            responsive.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    pause_start_time = time.time()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PATH_RECORDING:
                    base_pos = responsive.scale_pos(event.pos)
                    computer_car.path.append(base_pos)
                    # print(f"Point added: {base_pos}  | Total: {len(computer_car.path)}")
                    print(base_pos)

        if paused:
            action          = pause_menu(WIN, clock, WIN.copy())
            paused_duration = time.time() - pause_start_time
            game_info.level_start_time += paused_duration
            paused = False
            if action == "restart":
                player_car.reset(); player_car2.reset(); game_info.reset()
                computer_car.next_level(game_info.level)
                start_countdown(WIN, images, player_car, player_car2, computer_car, game_info)
                game_info.start_level()
                player_car, player_car2 = make_players()
                computer_car = ComputerCar(1.4, 2.5, PATH)
                reset_leaderboard()

            elif action == "exit":
                show_menu()
                game_info.reset()
                player_car.reset(); player_car2.reset()
                computer_car.next_level(game_info.level)
                player_car, player_car2 = make_players()
                start_countdown(WIN, images, player_car, player_car2, computer_car, game_info)
                game_info.start_level()
                reset_leaderboard()
                reset_nitros()

        if not paused:
            move_player(player_car, player_car2)
            computer_car.move()
            handle_collision(player_car, player_car2, computer_car, game_info)
            player_car.update_nitro()
            player_car2.update_nitro()
            computer_car.update_nitro()

        if game_info.game_finished():
            sound_completed_effect.play()
            car_data = [
                {"id": "P1", "name": CAR_DATA[player1_car_index]["name"],
                 "color": CAR_DATA[player1_car_index]["color"]},
                {"id": "P2", "name": CAR_DATA[player2_car_index]["name"],
                 "color": CAR_DATA[player2_car_index]["color"]},
                {"id": "AI", "name": "MODERN PINK",
                 "color": (255, 90, 160)},
            ]
            show_leaderboard(WIN, clock, car_data)
            reset_leaderboard()  # ← reset for next race
            show_menu()
            ...
            game_info.reset(); player_car.reset(); player_car2.reset()
            start_countdown(WIN, images, player_car, player_car2, computer_car, game_info)
            game_info.start_level()
            player_car, player_car2 = make_players()
            computer_car = ComputerCar(1.4, 2.5, PATH)

    pygame.quit()


if __name__ == "__main__":
    main()
