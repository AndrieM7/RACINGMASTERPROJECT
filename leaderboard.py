import math
import random
import pygame
import responsive

#  FINISH-COUNT TRACKER
#  Every time a car crosses the finish line, we add 1 to its counter.
#  "P1" = Player 1,  "P2" = Player 2,  "AI" = Computer car

_finish_counts: dict[str, int] = {"P1": 0, "P2": 0, "AI": 0}

def track_finish(car_id: str) -> None:
    # Call this every time a car successfully crosses the finish line.
    if car_id in _finish_counts:
        _finish_counts[car_id] += 1


def reset_leaderboard() -> None:
    # Call this after the leaderboard is shown to clear counts for next race.
    for key in _finish_counts:
        _finish_counts[key] = 0

# --- Backgrounds & Panels ---
BG_DARK         = (10,  10,  24)   # main screen background (same as SEL_BG)
OVERLAY_COLOR   = (20,  10,  10)
PANEL_BG        = (18,  18,  38)
PANEL_BORDER    = (50,  50,  90)

# --- Text & Accents ---
COLOR_WHITE     = (230, 230, 240)
COLOR_MUTED     = (110, 110, 140)
COLOR_BLACK     = (0,   0,   0)

# --- Gold (title, winner banner, 1st place) ---
GOLD_BRIGHT     = (255, 215,   0)  # bright gold  (same as FERRARI_YELLOW)
GOLD_DIM        = (180, 140,   0)  # dimmer gold for underlines (same as SEL_GOLD_DIM)

# --- Medal colors for 1st / 2nd / 3rd ---
MEDAL_GOLD      = (255, 215,   0)  # 1st place
MEDAL_SILVER    = (192, 192, 192)  # 2nd place
MEDAL_BRONZE    = (205, 127,  50)  # 3rd place
MEDAL_DEFAULT   = (110, 110, 140)  # 4th place and beyond (muted)

TIE_COLOR       = ( 80, 200, 255)  # blue highlight used for TIE badge

FLAG_LIGHT      = (255, 215,   0)  # gold squares
FLAG_DARK       = (0,   0,   0)    # black squares


#  LAYOUT SETTINGS
#  Change these numbers to adjust spacing, sizes, and positions.

TITLE_FONT_SIZE         = 52
SUBTITLE_FONT_SIZE      = 13
WINNER_NAME_FONT_SIZE   = 28
WINNER_COUNT_FONT_SIZE  = 48    # big finish-count number in banner
CARD_RANK_FONT_SIZE     = 20    # "2ND" / "3RD" inside rank badge circle
CARD_LABEL_FONT_SIZE    = 16    # small "PLAYER 1" tag above car name
CARD_NAME_FONT_SIZE     = 20    # car name on the rank cards
CARD_COUNT_FONT_SIZE    = 30    # finish count number on rank cards
FOOTER_FONT_SIZE        = 18    # "CONTINUE" button text
HINT_FONT_SIZE          = 12    # "Press ENTER..." hint text

WINNER_BANNER_HEIGHT    = 100   # height of the top winner spotlight box
WINNER_BANNER_PADDING   = 18    # inner padding of winner banner
FLAG_STRIPE_HEIGHT      = 5     # height of checkered stripe on banner top
FLAG_SQUARE_SIZE        = 10    # width of each square in the stripe

RANK_CARD_HEIGHT        = 80    # height of each 2nd/3rd place card
RANK_CARD_PADDING       = 14    # inner padding of rank cards
RANK_CARD_GAP           = 10    # vertical gap between rank cards
RANK_BADGE_RADIUS       = 24    # radius of the circle rank badge
RANK_BADGE_BORDER       = 2     # thickness of circle outline

LEFT_STRIPE_WIDTH       = 4     # coloured left edge stripe on cards
BAR_WIDTH               = 130   # max width of the finish-count bar
BAR_HEIGHT              = 5     # height of the finish-count bar

CONTINUE_BTN_W          = 220   # width of the CONTINUE button
CONTINUE_BTN_H          = 56    # height of the CONTINUE button
CONTINUE_BTN_RADIUS     = 14    # corner rounding (matches draw_button in main)
CONTINUE_BTN_BORDER     = 2     # white border thickness

CARD_SLIDE_SPEED        = 0.30  # seconds each card takes to slide in
CARD_SLIDE_DELAY        = 0.25  # seconds between each card appearing
CONFETTI_COUNT          = 22    # number of confetti pieces per burst

#  INTERNAL HELPERS
#  Small reusable drawing functions — kept simple and clearly named.

def _make_font(name: str, size: int, bold: bool = False) -> pygame.font.Font:
    try:
        return pygame.font.SysFont(name, size, bold=bold)
    except Exception:
        return pygame.font.SysFont("arial", size, bold=bold)


def _shadow_text(surf, font, text, color, x, y,
                 shadow_offset: int = 3) -> None:
    # """Draw text with a black drop shadow underneath — same as draw_shadow_text in main."""
    surf.blit(font.render(text, True, COLOR_BLACK), (x + shadow_offset,
                                                      y + shadow_offset))
    surf.blit(font.render(text, True, color), (x, y))


def _rounded_box(surf, color, rect: pygame.Rect,
                 radius: int = 12, border_color=None, border_w: int = 2) -> None:
    # """Draw a filled rounded rectangle, with an optional border outline."""
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border_color:
        pygame.draw.rect(surf, border_color, rect, border_w,
                         border_radius=radius)


def _draw_grid(surf, width: int, height: int) -> None:
    # """Draw the subtle dark grid pattern used on menu/options screens."""
    grid_color = (20, 20, 44)
    for x in range(0, width, 40):
        pygame.draw.line(surf, grid_color, (x, 0), (x, height), 1)
    for y in range(0, height, 40):
        pygame.draw.line(surf, grid_color, (0, y), (width, y), 1)


def _draw_checkered_stripe(surf, x: int, y: int,
                            width: int, height: int) -> None:
    # """Draw a gold-and-black checkered stripe — used on the winner banner top edge."""
    cols = width // FLAG_SQUARE_SIZE + 1
    rows = height // FLAG_SQUARE_SIZE + 1
    for col in range(cols):
        for row in range(rows):
            # alternate black and gold like a real checkered flag
            is_gold = (col + row) % 2 == 0
            color   = FLAG_LIGHT if is_gold else FLAG_DARK
            pygame.draw.rect(
                surf, color,
                pygame.Rect(x + col * FLAG_SQUARE_SIZE,
                            y + row * FLAG_SQUARE_SIZE,
                            FLAG_SQUARE_SIZE, FLAG_SQUARE_SIZE)
            )


def _get_medal_color(rank: int) -> tuple:
    # """Return the right medal color for a given rank number."""
    return {1: MEDAL_GOLD, 2: MEDAL_SILVER, 3: MEDAL_BRONZE}.get(
        rank, MEDAL_DEFAULT)


def _rank_label(rank: int) -> str:
    # """Turn a rank number into a display string: 1 → '1ST', 2 → '2ND', etc."""
    return {1: "1ST", 2: "2ND", 3: "3RD"}.get(rank, f"{rank}TH")

def _spawn_confetti(cx: int, cy: int, car_color: tuple) -> list:
    """
    Create a burst of confetti pieces centred at (cx, cy).
    Returns a list of pieces, each piece is a dict with position,
    velocity, lifetime, size, and color.
    """
    pieces = []
    for _ in range(CONFETTI_COUNT):
        pieces.append({
            "x":      float(cx),
            "y":      float(cy),
            "vx":     random.uniform(-4.0,  4.0),   # horizontal speed
            "vy":     random.uniform(-6.0, -1.5),   # upward launch speed
            "life":   random.uniform(0.8,  1.4),    # seconds before fading out
            "max_life": 1.4,                         # used to calculate alpha
            "size":   random.randint(4, 8),          # square size in pixels
            # mix the car's own colour with gold for variety
            "color":  car_color if random.random() > 0.4 else GOLD_BRIGHT,
        })
    return pieces


def _update_confetti(pieces: list, dt: float) -> list:
    """
    Move every confetti piece by its velocity, apply gravity,
    and remove any that have expired.  Returns the surviving pieces.
    """
    gravity = 0.18   # how fast pieces fall
    alive   = []
    for p in pieces:
        p["x"]    += p["vx"]
        p["y"]    += p["vy"]
        p["vy"]   += gravity      # gravity pulls pieces down
        p["life"] -= dt
        if p["life"] > 0:
            alive.append(p)
    return alive


def _draw_confetti(surf, pieces: list) -> None:
    """Draw all living confetti pieces, fading out as their life drops."""
    for p in pieces:
        # alpha goes from 255 (full) down to 0 as life runs out
        alpha = int(255 * (p["life"] / p["max_life"]))
        alpha = max(0, min(255, alpha))

        piece_surf = pygame.Surface((p["size"], p["size"]), pygame.SRCALPHA)
        piece_surf.fill((*p["color"], alpha))
        surf.blit(piece_surf, (int(p["x"]), int(p["y"])))


# =============================================================================
#  RANKING LOGIC
#  Sort cars by finish count and assign rank numbers.
#  Cars with the same count get the same rank number (a tie).
# =============================================================================

def _build_ranking(car_data: list[dict]) -> list[dict]:
    """
    Sort car_data by finish count (highest first).
    Each entry gets a 'rank' number and a 'finishes' count added to it.
    Cars with equal counts share the same rank number.

    Returns a new list of dicts — original car_data is not modified.
    """
    # attach the finish count to each car dict
    enriched = []
    for car in car_data:
        enriched.append({
            **car,
            "finishes": _finish_counts.get(car["id"], 0),
        })

    # sort by finishes descending (most first)
    enriched.sort(key=lambda c: c["finishes"], reverse=True)

    # assign rank numbers — ties share the same rank
    ranked = []
    current_rank = 1
    for i, car in enumerate(enriched):
        if i > 0 and car["finishes"] == enriched[i - 1]["finishes"]:
            # same count as the car above → same rank (tie)
            car["rank"] = ranked[-1]["rank"]
        else:
            car["rank"] = current_rank
        ranked.append(car)
        current_rank += 1

    return ranked


# =============================================================================
#  DRAWING — WINNER SPOTLIGHT BANNER
#  The big gold panel at the top that shows just the 1st-place winner.
# =============================================================================

def _draw_winner_banner(surf, ranking: list[dict],
                        banner_x: int, banner_y: int, banner_w: int,
                        font_name: str, font_sub: str, anim_t: float) -> None:
    """
    Draw the winner spotlight banner.
    Shows the car name, player label, and finish count of whoever is in 1st.
    """
    winner      = ranking[0]
    winner_col  = winner["color"]
    medal_col   = _get_medal_color(winner["rank"])
    banner_rect = pygame.Rect(banner_x, banner_y,
                              banner_w, WINNER_BANNER_HEIGHT)

    # --- pulsing gold glow behind the banner ---
    pulse_alpha = int(25 + 15 * math.sin(anim_t * 3))
    glow_surf   = pygame.Surface((banner_w + 20, WINNER_BANNER_HEIGHT + 20),
                                 pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*medal_col, pulse_alpha),
                     glow_surf.get_rect(), border_radius=16)
    surf.blit(glow_surf, (banner_x - 10, banner_y - 10))

    # --- banner background and gold border ---
    _rounded_box(surf, PANEL_BG, banner_rect,
                 radius=14, border_color=medal_col, border_w=2)

    # --- checkered flag stripe along the top edge ---
    stripe_rect = pygame.Rect(banner_x + 2, banner_y + 2,
                              banner_w - 4, FLAG_STRIPE_HEIGHT)
    # clip drawing to just the stripe area so it doesn't overflow
    surf.set_clip(stripe_rect)
    _draw_checkered_stripe(surf, banner_x + 2, banner_y + 2,
                           banner_w - 4, FLAG_STRIPE_HEIGHT)
    surf.set_clip(None)

    # --- layout inside the banner: [trophy] [name block] [count] ---
    inner_y  = banner_y + FLAG_STRIPE_HEIGHT + WINNER_BANNER_PADDING
    inner_h  = WINNER_BANNER_HEIGHT - FLAG_STRIPE_HEIGHT - WINNER_BANNER_PADDING * 2

    # trophy icon on the left
    trophy_font = _make_font("Impact", 42)
    trophy_surf = trophy_font.render("1ST", True, medal_col)
    trophy_x    = banner_x + WINNER_BANNER_PADDING + 8
    trophy_y    = inner_y + (inner_h - trophy_surf.get_height()) // 2
    # shadow then text
    surf.blit(trophy_font.render("1ST", True, COLOR_BLACK),
              (trophy_x + 3, trophy_y + 3))
    surf.blit(trophy_surf, (trophy_x, trophy_y))

    # car name and player label in the centre
    name_font  = _make_font(font_name, WINNER_NAME_FONT_SIZE)
    label_font = _make_font(font_sub, CARD_LABEL_FONT_SIZE, bold=True)
    sub_font   = _make_font(font_sub, 11)

    player_label = ("PLAYER 1" if winner["id"] == "P1"
                    else "PLAYER 2" if winner["id"] == "P2"
                    else "AI CAR")

    label_surf = label_font.render(f"● {player_label}  ·  RACE WINNER",
                                   True, winner_col)
    name_surf  = name_font.render(winner["name"], True, COLOR_WHITE)
    sub_surf   = sub_font.render("most finish-line crossings",
                                 True, COLOR_MUTED)

    text_x  = trophy_x + trophy_surf.get_width() + 20
    label_y = inner_y + 2
    name_y  = label_y + label_surf.get_height() + 3
    sub_y   = name_y  + name_surf.get_height() + 2

    surf.blit(label_surf, (text_x, label_y))
    _shadow_text(surf, name_font, winner["name"],
                 COLOR_WHITE, text_x, name_y, shadow_offset=2)
    surf.blit(sub_surf, (text_x, sub_y))

    # big finish count on the right
    count_font = _make_font(font_name, WINNER_COUNT_FONT_SIZE)
    unit_font  = _make_font(font_sub, 10)

    count_str  = str(winner["finishes"])
    count_surf = count_font.render(count_str, True, medal_col)
    unit_surf  = unit_font.render("CROSSES", True, COLOR_MUTED)

    count_x    = (banner_x + banner_w
                  - WINNER_BANNER_PADDING - count_surf.get_width())
    count_y    = inner_y + (inner_h - count_surf.get_height()) // 2 - 4
    unit_x     = (banner_x + banner_w
                  - WINNER_BANNER_PADDING - unit_surf.get_width())
    unit_y     = count_y + count_surf.get_height() + 2

    _shadow_text(surf, count_font, count_str, medal_col,
                 count_x, count_y, shadow_offset=3)
    surf.blit(unit_surf, (unit_x, unit_y))


# =============================================================================
#  DRAWING — RANK CARDS (2nd place, 3rd place, and beyond)
#  Each card slides in from the right when it first appears.
# =============================================================================

def _draw_rank_card(surf, entry: dict, card_x: int, card_y: int,
                    card_w: int, max_finishes: int,
                    font_name: str, font_sub: str,
                    show_tie: bool) -> None:
    """
    Draw a single rank card for a non-winner racer.
    card_x is already adjusted for the slide-in animation by the caller.
    """
    car_color  = entry["color"]
    medal_col  = _get_medal_color(entry["rank"])
    card_rect  = pygame.Rect(card_x, card_y, card_w, RANK_CARD_HEIGHT)

    # --- card background and border ---
    _rounded_box(surf, PANEL_BG, card_rect,
                 radius=12, border_color=medal_col, border_w=2)

    # --- left colour stripe in the car's own colour ---
    stripe_rect = pygame.Rect(card_x, card_y + 8,
                              LEFT_STRIPE_WIDTH, RANK_CARD_HEIGHT - 16)
    pygame.draw.rect(surf, car_color, stripe_rect, border_radius=2)

    # --- rank badge circle on the left ---
    badge_cx = card_x + RANK_CARD_PADDING + RANK_BADGE_RADIUS + 4
    badge_cy = card_y + RANK_CARD_HEIGHT // 2
    pygame.draw.circle(surf, BG_DARK, (badge_cx, badge_cy), RANK_BADGE_RADIUS)
    pygame.draw.circle(surf, medal_col, (badge_cx, badge_cy),
                       RANK_BADGE_RADIUS, RANK_BADGE_BORDER)

    rank_font = _make_font(font_name, CARD_RANK_FONT_SIZE)
    rank_text = _rank_label(entry["rank"])
    rank_surf = rank_font.render(rank_text, True, medal_col)
    surf.blit(rank_surf, rank_surf.get_rect(center=(badge_cx, badge_cy)))

    # --- car name and player label ---
    label_font = _make_font(font_sub, CARD_LABEL_FONT_SIZE, bold=True)
    name_font  = _make_font(font_name, CARD_NAME_FONT_SIZE)

    player_label = ("PLAYER 1" if entry["id"] == "P1"
                    else "PLAYER 2" if entry["id"] == "P2"
                    else "AI CAR")

    # add TIE badge text next to the label when applicable
    label_text = f"● {player_label}"
    label_surf = label_font.render(label_text, True, car_color)
    name_surf  = name_font.render(entry["name"], True, COLOR_WHITE)

    text_x  = badge_cx + RANK_BADGE_RADIUS + 12
    label_y = badge_cy - label_surf.get_height() - 3
    name_y  = label_y + label_surf.get_height() + 2

    surf.blit(label_surf, (text_x, label_y))

    # TIE badge drawn right after the label if needed
    if show_tie:
        tie_font = _make_font(font_sub, 10, bold=True)
        tie_surf = tie_font.render("TIE", True, TIE_COLOR)
        tie_bg   = pygame.Rect(
            text_x + label_surf.get_width() + 6,
            label_y + 1,
            tie_surf.get_width() + 10,
            tie_surf.get_height() + 2
        )
        _rounded_box(surf,
                     (20, 50, 70),   # dark blue background for tie badge
                     tie_bg, radius=4,
                     border_color=TIE_COLOR, border_w=1)
        surf.blit(tie_surf, (tie_bg.x + 5, tie_bg.y + 1))

    surf.blit(name_surf, (text_x, name_y))

    # --- finish count bar below the car name ---
    bar_x      = text_x
    bar_y      = name_y + name_surf.get_height() + 5
    fill_ratio = (entry["finishes"] / max_finishes) if max_finishes > 0 else 0
    fill_w     = int(BAR_WIDTH * fill_ratio)

    # bar track (empty background)
    pygame.draw.rect(surf, (30, 30, 55),
                     pygame.Rect(bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT),
                     border_radius=3)
    # bar fill (coloured progress)
    if fill_w > 0:
        pygame.draw.rect(surf, car_color,
                         pygame.Rect(bar_x, bar_y, fill_w, BAR_HEIGHT),
                         border_radius=3)

    # --- finish count number and label on the right ---
    count_font = _make_font(font_name, CARD_COUNT_FONT_SIZE)
    lbl_font   = _make_font(font_sub, 9)

    count_surf = count_font.render(str(entry["finishes"]), True, medal_col)
    lbl_surf   = lbl_font.render("FINISH CROSSES", True, COLOR_MUTED)

    count_right_x = card_x + card_w - RANK_CARD_PADDING
    count_x       = count_right_x - count_surf.get_width()
    lbl_x         = count_right_x - lbl_surf.get_width()
    count_y_pos   = badge_cy - count_surf.get_height() // 2 - 4
    lbl_y_pos     = count_y_pos + count_surf.get_height() + 2

    _shadow_text(surf, count_font, str(entry["finishes"]),
                 medal_col, count_x, count_y_pos, shadow_offset=2)
    surf.blit(lbl_surf, (lbl_x, lbl_y_pos))


# =============================================================================
#  DRAWING — TITLE SECTION
#  The "RACE RESULTS" header with gold shadow text and underline decoration.
#  Matches the same style used on the pause menu title.
# =============================================================================

def _draw_title(surf, W: int, font_name: str, font_sub: str) -> int:
    """
    Draw the title block at the top of the screen.
    Returns the Y position right after the title block ends,
    so the caller knows where to start drawing content below it.
    """
    title_font    = _make_font(font_name, TITLE_FONT_SIZE)
    subtitle_font = _make_font(font_sub, SUBTITLE_FONT_SIZE)

    title_text = "RACE RESULTS"
    title_surf = title_font.render(title_text, True, GOLD_BRIGHT)
    title_x    = W // 2 - title_surf.get_width() // 2
    title_y    = 28

    _shadow_text(surf, title_font, title_text,
                 GOLD_BRIGHT, title_x, title_y, shadow_offset=4)

    # gold underline with dot endpoints — same as car selection screen
    underline_y  = title_y + title_surf.get_height() + 6
    underline_x0 = W // 2 - (title_surf.get_width() // 2 + 20)
    underline_x1 = W // 2 + (title_surf.get_width() // 2 + 20)
    pygame.draw.line(surf, GOLD_DIM,
                     (underline_x0, underline_y),
                     (underline_x1, underline_y), 2)
    pygame.draw.circle(surf, GOLD_BRIGHT, (underline_x0, underline_y), 3)
    pygame.draw.circle(surf, GOLD_BRIGHT, (underline_x1, underline_y), 3)

    # small subtitle below
    sub_text = "FINISH LINE CROSSINGS  ·  RANKED"
    sub_surf = subtitle_font.render(sub_text, True, COLOR_MUTED)
    sub_y    = underline_y + 10
    surf.blit(sub_surf, (W // 2 - sub_surf.get_width() // 2, sub_y))

    # return where content should start below the title block
    return sub_y + sub_surf.get_height() + 18


# =============================================================================
#  DRAWING — CONTINUE BUTTON
#  Same rounded style as draw_button() in MAIN_TO_DEVELOP.py.
# =============================================================================

def _draw_continue_button(surf, W: int, H: int,
                          font_sub: str, anim_t: float) -> pygame.Rect:
    """
    Draw the CONTINUE button at the bottom of the screen.
    Returns the button Rect so the caller can check for mouse clicks.
    """
    btn_x    = W // 2 - CONTINUE_BTN_W // 2
    btn_y    = H - CONTINUE_BTN_H - 28
    btn_rect = pygame.Rect(btn_x, btn_y, CONTINUE_BTN_W, CONTINUE_BTN_H)

    # draw button — gold fill, white border, black text (same as draw_button)
    pygame.draw.rect(surf, GOLD_BRIGHT, btn_rect,
                     border_radius=CONTINUE_BTN_RADIUS)
    pygame.draw.rect(surf, (255, 255, 255), btn_rect,
                     CONTINUE_BTN_BORDER, border_radius=CONTINUE_BTN_RADIUS)

    btn_font = _make_font(font_sub, FOOTER_FONT_SIZE, bold=True)
    btn_surf = btn_font.render("CONTINUE", True, COLOR_BLACK)
    surf.blit(btn_surf, btn_surf.get_rect(center=btn_rect.center))
    btn_surf = btn_font.render("TRY AGAIN", True, COLOR_BLACK)
    surf.blit(btn_surf, btn_surf.get_rect(center=btn_rect.center))

    # pulsing hint text below the button
    hint_alpha = int(160 + 80 * math.sin(anim_t * 2))
    hint_font  = _make_font(font_sub, HINT_FONT_SIZE)
    hint_surf  = hint_font.render(
        "Press ENTER  ·  SPACE  ·  or click to continue",
        True, COLOR_MUTED)
    hint_surf.set_alpha(hint_alpha)
    surf.blit(hint_surf, (W // 2 - hint_surf.get_width() // 2,
                          btn_y + CONTINUE_BTN_H + 8))

    return btn_rect


# =============================================================================
#  MAIN LEADERBOARD SCREEN
#  This is the function you call from MAIN_TO_DEVELOP.py.
# =============================================================================

def show_leaderboard(screen, clock, car_data: list[dict]) -> None:
    """
    Show the end-of-race leaderboard screen.

    Parameters
    ----------
    screen   : the pygame display (pass WIN from main)
    clock    : pygame.time.Clock (pass clock from main)
    car_data : list of dicts, one per racer:
               [{"id": "P1", "name": "MODERN RED", "color": (220, 60, 60)},
                {"id": "P2", "name": "MODERN BLUE","color": ( 60,120,255)},
                {"id": "AI", "name": "MODERN PINK","color": (255, 90,160)}]
    """

    # --- font names (Impact + Georgia, same as the rest of the game) ---
    FONT_IMPACT  = "Impact"
    FONT_GEORGIA = "Georgia"

    # --- build the ranked list from finish counts ---
    ranking      = _build_ranking(car_data)
    max_finishes = max(1, max(e["finishes"] for e in ranking))

    # --- animation state ---
    anim_t           = 0.0          # total elapsed seconds
    confetti_pieces  = []           # list of active confetti pieces
    confetti_spawned = False        # only spawn once for the winner

    # --- card slide-in state ---
    # We skip ranking[0] (winner) since it uses the banner, not a card.
    # The remaining entries each get a slide-in animation.
    non_winner_entries = ranking[1:]   # 2nd, 3rd, etc.
    card_revealed      = [False] * len(non_winner_entries)

    # each card starts sliding in after a staggered delay
    card_reveal_at = [
        0.30 + i * CARD_SLIDE_DELAY
        for i in range(len(non_winner_entries))
    ]
    # banner appears after a short delay too
    banner_reveal_at = 0.10

    # --- main loop ---
    while True:
        dt      = clock.tick(60) / 1000.0
        anim_t += dt

        # ── event handling ──────────────────────────────────────────
        for event in pygame.event.get():
            if responsive.handle_event(event):
                continue
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN,
                                 pygame.K_SPACE,
                                 pygame.K_ESCAPE):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return    # any click closes the screen

        # ── get the drawable surface and its size ────────────────────
        base   = responsive.get_base_surface()
        W, H   = base.get_width(), base.get_height()

        # content width — centred, with side margins
        CONTENT_W = min(int(W * 0.82), 560)
        CONTENT_X = W // 2 - CONTENT_W // 2

        # ── background ───────────────────────────────────────────────
        base.fill(BG_DARK)
        _draw_grid(base, W, H)

        # thin gold glow strip at the very top (same as options screen)
        glow_strip = pygame.Surface((W, 3), pygame.SRCALPHA)
        glow_strip.fill((*GOLD_BRIGHT, 90))
        base.blit(glow_strip, (0, 0))

        # semi-transparent dark overlay (same as pause menu overlay)
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((*OVERLAY_COLOR, 140))
        base.blit(overlay, (0, 0))

        # ── title ────────────────────────────────────────────────────
        content_start_y = _draw_title(base, W, FONT_IMPACT, FONT_GEORGIA)

        # ── winner banner (slides in from right) ─────────────────────
        banner_age   = anim_t - banner_reveal_at
        banner_ease  = min(1.0, banner_age / CARD_SLIDE_SPEED)
        banner_ease  = 1 - (1 - banner_ease) ** 3   # cubic ease-out

        banner_final_x = CONTENT_X
        banner_slide_x = int(banner_final_x + (W - banner_final_x)
                             * (1 - banner_ease))

        if banner_age >= 0:
            _draw_winner_banner(base, ranking,
                                banner_slide_x, content_start_y,
                                CONTENT_W, FONT_IMPACT, FONT_GEORGIA,
                                anim_t)

            # spawn confetti once the banner fully settles in
            if not confetti_spawned and banner_ease >= 1.0:
                winner_cx = W // 2
                winner_cy = content_start_y + WINNER_BANNER_HEIGHT // 2
                confetti_pieces = _spawn_confetti(
                    winner_cx, winner_cy, ranking[0]["color"])
                confetti_spawned = True

        # ── rank cards (2nd, 3rd ...) ─────────────────────────────────
        cards_start_y = (content_start_y
                         + WINNER_BANNER_HEIGHT + 14)

        for i, entry in enumerate(non_winner_entries):
            card_age  = anim_t - card_reveal_at[i]
            if card_age < 0:
                continue    # not time yet — skip this card

            card_revealed[i] = True

            # slide-in ease
            card_ease = min(1.0, card_age / CARD_SLIDE_SPEED)
            card_ease = 1 - (1 - card_ease) ** 3   # cubic ease-out

            card_final_x = CONTENT_X
            card_slide_x = int(card_final_x + (W - card_final_x)
                               * (1 - card_ease))
            card_y       = (cards_start_y
                            + i * (RANK_CARD_HEIGHT + RANK_CARD_GAP))

            # a card shows the TIE badge if it shares a rank with the one above it
            is_tied = (i > 0
                       and entry["rank"] == non_winner_entries[i - 1]["rank"])

            _draw_rank_card(base, entry,
                            card_slide_x, card_y, CONTENT_W,
                            max_finishes, FONT_IMPACT, FONT_GEORGIA,
                            show_tie=is_tied)

        # ── confetti ─────────────────────────────────────────────────
        if confetti_pieces:
            confetti_pieces = _update_confetti(confetti_pieces, dt)
            _draw_confetti(base, confetti_pieces)

        # ── continue button ──────────────────────────────────────────
        _draw_continue_button(base, W, H, FONT_GEORGIA, anim_t)

        # ── push frame to screen ─────────────────────────────────────
        responsive.flip()
