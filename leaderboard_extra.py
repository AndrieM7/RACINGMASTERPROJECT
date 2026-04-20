# leaderboard.py  ── Racing Master  (finish-count edition)
#
# HOW IT WORKS
# ────────────
# Call track_finish(car_id) every time a car crosses the finish line.
#   car_id  →  "P1"  |  "P2"  |  "AI"
#
# Call show_leaderboard(screen, clock, car_data) when the race ends.
#   car_data  →  list of dicts, one per racer:
#       {
#           "id":    "P1",            # "P1" | "P2" | "AI"
#           "name":  "MODERN RED",    # from CAR_DATA[index]["name"]
#           "color": (220, 60, 60),   # from CAR_DATA[index]["color"]
#       }
#
# Call reset_leaderboard() before every new race.

import math
import pygame
import responsive

# ── internal finish-count store
_finish_counts: dict[str, int] = {"P1": 0, "P2": 0, "AI": 0}


def track_finish(car_id: str) -> None:
    """Increment the finish-line counter for car_id."""
    if car_id in _finish_counts:
        _finish_counts[car_id] += 1


def reset_leaderboard() -> None:
    """Reset all counters (call before each new race)."""
    for k in _finish_counts:
        _finish_counts[k] = 0


def _build_ranking(car_data: list[dict]) -> list[dict]:
    """
    Return car_data sorted by finish count (desc).
    Ties share the same rank number.
    """
    ranked = sorted(
        car_data,
        key=lambda c: _finish_counts.get(c["id"], 0),
        reverse=True,
    )
    result = []
    rank   = 1
    for i, car in enumerate(ranked):
        if i > 0 and _finish_counts.get(car["id"], 0) == _finish_counts.get(ranked[i - 1]["id"], 0):
            r = result[-1]["rank"]          # same rank as previous
        else:
            r = rank
        result.append({**car, "rank": r, "finishes": _finish_counts.get(car["id"], 0)})
        rank += 1
    return result


# ── colour palette (mirrors MAIN_TO_DEVELOP.py)
_BG          = (10,  10,  24)
_PANEL_BG    = (18,  18,  38)
_BORDER      = (50,  50,  90)
_GOLD        = (255, 215,   0)
_GOLD_DIM    = (180, 140,   0)
_WHITE       = (230, 230, 240)
_MUTED       = (110, 110, 140)
_DARK        = ( 20,  10,  10)
_ACCENT_BLUE = ( 80, 200, 255)

# rank medal colours
_MEDAL = {
    1: (255, 215,   0),   # gold
    2: (192, 192, 192),   # silver
    3: (205, 127,  50),   # bronze
}

# ── helpers
def _grid(surf, w, h):
    col = (20, 20, 44)
    for x in range(0, w, 40):
        pygame.draw.line(surf, col, (x, 0), (x, h), 1)
    for y in range(0, h, 40):
        pygame.draw.line(surf, col, (0, y), (w, y), 1)


def _rounded_rect(surf, color, rect, radius=10, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)


def _shadow_text(surf, text, font, color, x, y):
    surf.blit(font.render(text, True, (0, 0, 0)), (x + 3, y + 3))
    surf.blit(font.render(text, True, color),     (x,     y    ))


def _glow_strip(surf, w):
    s = pygame.Surface((w, 3), pygame.SRCALPHA)
    s.fill((*_GOLD, 90))
    surf.blit(s, (0, 0))


def _lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ── main leaderboard screen
def show_leaderboard(screen, clock, car_data: list[dict]) -> None:
    """
    Display the race leaderboard.

    Parameters
    ----------
    screen   : pygame display surface (pass WIN from main)
    clock    : pygame.time.Clock
    car_data : list of {id, name, color}  – one entry per racer
    """
    ranking = _build_ranking(car_data)

    # fonts
    def _font(name, size, bold=False):
        try:    return pygame.font.SysFont(name, size, bold=bold)
        except: return pygame.font.SysFont("arial", size, bold=bold)

    f_title  = _font("Impact", 64)
    f_sub    = _font("Arial",  13)
    f_rank   = _font("Impact", 52)
    f_name   = _font("Impact", 24)
    f_count  = _font("Impact", 20)
    f_label  = _font("Arial",  11, bold=True)
    f_footer = _font("Arial",  12)

    anim_t   = 0.0
    revealed = [False] * len(ranking)   # cards pop in one by one
    reveal_timers = [i * 0.35 for i in range(len(ranking))]  # stagger

    # particle list  [x, y, vx, vy, life, color]
    particles: list[list] = []

    def _spawn_confetti(cx, cy, color):
        import random
        for _ in range(18):
            particles.append([
                cx, cy,
                random.uniform(-3, 3),
                random.uniform(-5, -1),
                random.uniform(0.6, 1.2),
                color,
            ])

    confetti_fired = [False] * len(ranking)

    while True:
        dt     = clock.tick(60) / 1000.0
        anim_t += dt

        # events
        for event in pygame.event.get():
            if responsive.handle_event(event):
                continue
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return          # any click closes

        base   = responsive.get_base_surface()
        W, H   = base.get_width(), base.get_height()

        # ── background
        base.fill(_BG)
        _grid(base, W, H)
        _glow_strip(base, W)

        # subtle radial glow behind title
        glow = pygame.Surface((W, 180), pygame.SRCALPHA)
        for r in range(120, 0, -4):
            a = max(0, int(14 * (1 - r / 120)))
            pygame.draw.ellipse(glow, (*_GOLD, a),
                                (W // 2 - r * 3, 90 - r, r * 6, r * 2))
        base.blit(glow, (0, 0))

        # ── title
        title_y = 28
        t_surf  = f_title.render("RACE RESULTS", True, _GOLD)
        t_sh    = f_title.render("RACE RESULTS", True, (0, 0, 0))
        tx      = W // 2 - t_surf.get_width() // 2
        base.blit(t_sh,  (tx + 4, title_y + 4))
        base.blit(t_surf, (tx, title_y))

        # underline
        ul_w = t_surf.get_width() + 40
        ul_x = W // 2 - ul_w // 2
        ul_y = title_y + t_surf.get_height() + 6
        pygame.draw.line(base, _GOLD_DIM, (ul_x, ul_y), (ul_x + ul_w, ul_y), 2)
        pygame.draw.circle(base, _GOLD, (ul_x,        ul_y), 3)
        pygame.draw.circle(base, _GOLD, (ul_x + ul_w, ul_y), 3)

        # subtitle
        sub = f_sub.render(
            "Ranked by number of finish-line crossings  •  Press ENTER or click to continue",
            True, _MUTED)
        base.blit(sub, (W // 2 - sub.get_width() // 2, ul_y + 10))

        # ── cards
        n          = len(ranking)
        CARD_W     = min(int(W * 0.78), 520)
        CARD_H     = 88
        CARD_GAP   = 14
        total_h    = n * CARD_H + (n - 1) * CARD_GAP
        cards_y    = ul_y + 44
        card_x     = W // 2 - CARD_W // 2

        for i, entry in enumerate(ranking):
            # reveal stagger
            age = anim_t - reveal_timers[i]
            if age < 0:
                continue                     # not yet
            revealed[i] = True

            # slide-in from right
            slide = min(1.0, age / 0.35)
            ease  = 1 - (1 - slide) ** 3    # cubic ease-out
            cx    = int(card_x + (W - card_x) * (1 - ease))
            cy    = cards_y + i * (CARD_H + CARD_GAP)

            # confetti burst for 1st place
            if i == 0 and not confetti_fired[i] and slide >= 1.0:
                _spawn_confetti(W // 2, cy + CARD_H // 2, entry["color"])
                confetti_fired[i] = True

            # ── card background
            rank      = entry["rank"]
            car_color = entry["color"]
            medal_col = _MEDAL.get(rank, _MUTED)

            # pulsing border for 1st place
            brd_col  = medal_col
            brd_w    = 2
            if rank == 1:
                pulse   = int(80 + 60 * math.sin(anim_t * 3))
                brd_col = (*medal_col, pulse)
                brd_w   = 2

                glow_c = pygame.Surface((CARD_W + 28, CARD_H + 28), pygame.SRCALPHA)
                pygame.draw.rect(glow_c,
                                 (*medal_col, int(30 + 20 * math.sin(anim_t * 3))),
                                 glow_c.get_rect(), border_radius=18)
                base.blit(glow_c, (cx - 14, cy - 14))

            _rounded_rect(base, _PANEL_BG, pygame.Rect(cx, cy, CARD_W, CARD_H),
                          radius=12)
            pygame.draw.rect(base, medal_col,
                             pygame.Rect(cx, cy, CARD_W, CARD_H),
                             brd_w, border_radius=12)

            # left accent stripe in car colour
            stripe_rect = pygame.Rect(cx, cy + 8, 4, CARD_H - 16)
            pygame.draw.rect(base, car_color, stripe_rect, border_radius=2)

            # ── rank medal circle
            medal_cx = cx + 52
            medal_cy = cy + CARD_H // 2
            pygame.draw.circle(base, _DARK,     (medal_cx, medal_cy), 28)
            pygame.draw.circle(base, medal_col, (medal_cx, medal_cy), 28, 2)

            rank_labels = {1: "1ST", 2: "2ND", 3: "3RD"}
            rl  = rank_labels.get(rank, f"{rank}TH")
            rl_s = f_rank.render(rl, True, medal_col)
            base.blit(rl_s, rl_s.get_rect(center=(medal_cx, medal_cy)))

            # tie badge
            if i > 0 and entry["rank"] == ranking[i - 1]["rank"]:
                tie_s = f_label.render("TIE", True, _ACCENT_BLUE)
                base.blit(tie_s, (medal_cx - tie_s.get_width() // 2,
                                  cy + CARD_H - tie_s.get_height() - 4))

            # ── car color swatch + name
            swatch_rect = pygame.Rect(cx + 90, cy + 18, 14, 14)
            pygame.draw.rect(base, car_color, swatch_rect, border_radius=7)
            pygame.draw.rect(base, _WHITE,    swatch_rect, 1, border_radius=7)

            label_lbl = f_label.render(
                "PLAYER 1" if entry["id"] == "P1"
                else "PLAYER 2" if entry["id"] == "P2"
                else "AI CAR",
                True, car_color)
            base.blit(label_lbl, (cx + 110, cy + 18))

            name_s = f_name.render(entry["name"], True, _WHITE)
            base.blit(name_s, (cx + 110, cy + 34))

            # ── finish count bar (right side)
            max_finishes  = max(1, max(e["finishes"] for e in ranking))
            bar_x         = cx + CARD_W - 220
            bar_y         = cy + 22
            bar_w_max     = 180
            bar_h         = 12
            fill_ratio    = entry["finishes"] / max_finishes
            fill_w        = int(bar_w_max * fill_ratio * min(1.0, (age - 0.2) / 0.5))
            fill_w        = max(0, fill_w)

            # track
            pygame.draw.rect(base, (30, 30, 55),
                             pygame.Rect(bar_x, bar_y, bar_w_max, bar_h), border_radius=6)
            # fill
            if fill_w > 0:
                fill_col = _lerp_color(car_color, _WHITE, 0.3)
                pygame.draw.rect(base, fill_col,
                                 pygame.Rect(bar_x, bar_y, fill_w, bar_h), border_radius=6)
                # shimmer
                shim_x = int((anim_t % 1.5) / 1.5 * (bar_w_max + 20)) - 10
                shim   = pygame.Surface((bar_w_max, bar_h), pygame.SRCALPHA)
                poly   = [(shim_x, 0), (shim_x + 10, 0),
                          (shim_x + 14, bar_h), (shim_x + 4, bar_h)]
                clipped = [(max(0, min(bar_w_max, px)), py) for px, py in poly]
                if len(clipped) == 4:
                    pygame.draw.polygon(shim, (255, 255, 255, 60), clipped)
                base.blit(shim, (bar_x, bar_y))

            # border
            pygame.draw.rect(base, _BORDER,
                             pygame.Rect(bar_x, bar_y, bar_w_max, bar_h), 1, border_radius=6)

            # count label
            count_lbl = f_label.render("FINISH CROSSES", True, _MUTED)
            base.blit(count_lbl, (bar_x, bar_y - 14))

            count_num = f_count.render(str(entry["finishes"]), True, medal_col)
            base.blit(count_num, (bar_x + bar_w_max + 8, bar_y - 2))

        # ── particles (confetti)
        for p in particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.15        # gravity
            p[4] -= dt
            if p[4] <= 0:
                particles.remove(p)
                continue
            alpha = int(255 * (p[4] / 1.2))
            s = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.rect(s, (*p[5], alpha), s.get_rect(), border_radius=2)
            base.blit(s, (int(p[0]), int(p[1])))

        # ── footer
        pulse_a  = int(160 + 80 * math.sin(anim_t * 2))
        foot_s   = f_footer.render("Press ENTER  •  SPACE  •  or click anywhere to continue",
                                   True, _MUTED)
        foot_s.set_alpha(pulse_a)
        base.blit(foot_s, (W // 2 - foot_s.get_width() // 2, H - 32))

        responsive.flip()
