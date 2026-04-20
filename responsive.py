import pygame

BASE_WIDTH  = 750
BASE_HEIGHT = 650

_fullscreen   = False
_base_surface = None   # everything is drawn here at BASE size
_screen       = None   # the actual OS window / display surface


def init(caption="Game"):
    global _base_surface, _screen

    _base_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
    _screen = pygame.display.set_mode(
        (BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE
    )
    pygame.display.set_caption(caption)
    return _base_surface


def get_base_surface():
    return _base_surface


def toggle_fullscreen():
    global _fullscreen, _screen

    _fullscreen = not _fullscreen
    if _fullscreen:
        _screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        _screen = pygame.display.set_mode(
            (BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE
        )


def handle_event(event):
    global _screen

    if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
        toggle_fullscreen()
        return True

    if event.type == pygame.VIDEORESIZE and not _fullscreen:
        _screen = pygame.display.set_mode(
            (event.w, event.h), pygame.RESIZABLE
        )
        return True

    return False


def scale_pos(screen_pos):
    win_w, win_h = _screen.get_size()
    base_aspect  = BASE_WIDTH  / BASE_HEIGHT
    win_aspect   = win_w / win_h

    if win_aspect > base_aspect:
        scaled_h = win_h
        scaled_w = int(scaled_h * base_aspect)
    else:
        scaled_w = win_w
        scaled_h = int(scaled_w / base_aspect)

    offset_x = (win_w - scaled_w) // 2
    offset_y = (win_h - scaled_h) // 2

    bx = (screen_pos[0] - offset_x) * BASE_WIDTH  / scaled_w
    by = (screen_pos[1] - offset_y) * BASE_HEIGHT / scaled_h
    return (int(bx), int(by))


def flip():
    win_w, win_h = _screen.get_size()
    base_aspect  = BASE_WIDTH  / BASE_HEIGHT
    win_aspect   = win_w / win_h

    if win_aspect > base_aspect:
        scaled_h = win_h
        scaled_w = int(scaled_h * base_aspect)
    else:
        scaled_w = win_w
        scaled_h = int(scaled_w / base_aspect)

    scaled = pygame.transform.smoothscale(_base_surface, (scaled_w, scaled_h))

    offset_x = (win_w - scaled_w) // 2
    offset_y = (win_h - scaled_h) // 2

    _screen.fill((0, 0, 0))          # letterbox bars
    _screen.blit(scaled, (offset_x, offset_y))
    pygame.display.flip()