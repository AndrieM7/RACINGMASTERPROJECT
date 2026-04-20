import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def scale_image_to(img, target_width, target_height):
    return pygame.transform.scale(img, (int(target_width), int(target_height)))


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text, color=(200, 110, 170), bg_color=None):
    render = font.render(text, True, color, bg_color)
    x = win.get_width()  / 2 - render.get_width()  / 2
    y = win.get_height() / 2 - render.get_height() / 2
    win.blit(render, (x, y))
