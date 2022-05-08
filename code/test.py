# import pygame
import random
import requests
import sys
from PIL import Image, ImageDraw
import sqlite3
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

# geo_x = 37.60226
# center_py = [225, 225]
# center_geo = [37.6, 55.7]
# center_x_geo = 37.6022
# center_y_geo = 55.69893333333334
# ssp = 0.004
# w = 450
# h = 450
# x = 359
# y = 222
#
# dx = x - center_py[0]
# dx_geo = center_x_geo + (3 * dx * ssp / w)
#
# dy = center_y_geo - y
# dy_geo = center_y_geo + (2 * dy * ssp / h)
#
#
# dx_geo = geo_x - center_geo[0]
# print(dx_geo)
# dx = (-dx_geo + center_geo[0] + (3 * ssp / w))
# print(center_py[0] + dx)

#
# pt = ''
# run = True
# updating = False
# map_file = "map_1.png"
# left_bottom, rith_top = [36.6, 54.6], [38.6, 56.6]
# center_geo = [37.6, 55.7]
# center_geo_1 = [38.7612, 56.13096]
# center_py = [225, 225]
# sp = 0.004
# z = 17
# points_list = []
# params1 = {
#     "ll": f'{center_geo[0]},{center_geo[1]}',
#     'spn': f'{sp},{sp}',
#     "l": 'sat',
#     'size': '450,450',
#     "pt": pt,
#     'z': z
# }
# map_request = "http://static-maps.yandex.ru/1.x/"
# response = requests.get(map_request, params1)
# if not response:
#     print("Ошибка выполнения запроса:")
#     print(response)
#     print("Http статус:", response.status_code, "(", response.reason, ")")
#     sys.exit(1)
#
# with open(map_file, "wb") as file:
#     file.write(response.content)

# map_file = "map.png"
#
#
# def update_map(num):
#     global map_file
#     map_file = "map.png"
#     map_file_1 = f'maps_vz/map_{num}.png'
#     map_file = Image.open(map_file)
#     map_file.save(map_file_1, 'png')
#
#
# # update_map(1)
login = 'captain2'
con = sqlite3.connect("db/fire-map_data.db")
cur = con.cursor()
result = cur.execute(f"""SELECT position_name FROM users
WHERE (login = '{login}')""").fetchone()
print(result)
coords = cur.execute(f"""SELECT x1 FROM positions
WHERE (name_position = '{result[0]}')""").fetchone()
con.close()
print(coords)