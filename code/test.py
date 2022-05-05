# import pygame
import random
#
#
# def draw(screen):
#     screen.fill((0, 0, 0))
#     font = pygame.font.Font(None, 50)
#     text = font.render("Hello, Pygame!", True, (100, 255, 100))
#     text_x = width // 2 - text.get_width() // 2
#     text_y = height // 2 - text.get_height() // 2
#     text_w = text.get_width()
#     text_h = text.get_height()
#     screen.blit(text, (text_x, text_y))
#     pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
#                                            text_w + 20, text_h + 20), 1)
#
#
# if __name__ == '__main__':
#     # инициализация Pygame:
#     pygame.init()
#     # размеры окна:
#     size = width, height = 800, 600
#     # screen — холст, на котором нужно рисовать:
#     screen = pygame.display.set_mode(size)
#     # формирование кадра:
#     # команды рисования на холсте
#     draw(screen)
#     # смена (отрисовка) кадра:
#     pygame.display.flip()
#     # ожидание закрытия окна:
#     while pygame.event.wait().type != pygame.QUIT:
#         pass
#     # завершение работы:
#     pygame.quit()

# dx = x - center_py[0]
# dx_geo = center_geo[0] + (3 * dx * ssp / w)

geo_x = 37.60226
center_py = [225, 225]
center_geo = [37.6, 55.7]
center_x_geo = 37.6022
center_y_geo = 55.69893333333334
ssp = 0.004
w = 450
h = 450
x = 359
y = 222

dx = x - center_py[0]
dx_geo = center_x_geo + (3 * dx * ssp / w)

dy = center_y_geo - y
dy_geo = center_y_geo + (2 * dy * ssp / h)


dx_geo = geo_x - center_geo[0]
print(dx_geo)
dx = (-dx_geo + center_geo[0] + (3 * ssp / w))
print(center_py[0] + dx)