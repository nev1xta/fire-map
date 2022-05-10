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
# map_file = "map_3.png"
# left_bottom, rith_top = [36.6, 54.6], [38.6, 56.6]
# center_geo = [60.619897, 56.826355]
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

# l = 60.61748
# v = 56.82767
# n = 56.82504
# p = 60.6223

pt = ''
run = True
updating = False
map_file = "map_3_pv.png"
left_bottom, rith_top = [36.6, 54.6], [38.6, 56.6]
center_geo = [60.619897, 56.826355]
center_geo_1 = [60.6223, 56.82767]
center_py = [225, 225]
sp = 0.002
z = 17
points_list = []
params1 = {
    "ll": f'{center_geo_1[0]},{center_geo_1[1]}',
    'spn': f'{sp},{sp}',
    "l": 'sat',
    'size': '450,450',
    "pt": pt,
    'z': z
}
map_request = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_request, params1)
if not response:
    print("Ошибка выполнения запроса:")
    print(response)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

with open(map_file, "wb") as file:
    file.write(response.content)



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
# login = 'captain2'
# con = sqlite3.connect("db/fire-map_data.db")
# cur = con.cursor()
# result = cur.execute(f"""SELECT position_name FROM users
# WHERE (login = '{login}')""").fetchone()
# print(result)
# coords = cur.execute(f"""SELECT x1 FROM positions
# WHERE (name_position = '{result[0]}')""").fetchone()
# con.close()
# print(coords)

# point_list = []
# con = sqlite3.connect("db/fire-map_data.db")
# cur = con.cursor()
# result = cur.execute(f"""SELECT x0, y0, point_id FROM points_on_maps""").fetchall()
# posit = cur.execute(f"""SELECT position_id FROM points_on_maps""").fetchall()
# con.close()
# print(result)
# for i in result:
#     con = sqlite3.connect("db/fire-map_data.db")
#     cur = con.cursor()
#     result = cur.execute(f"""SELECT x0, y0, point_id FROM points_on_maps""").fetchall()
#     con.close()

# con = sqlite3.connect("db/fire-map_data.db")
# cur = con.cursor()
# curr_map_res = cur.execute(f"""SELECT x1 FROM positions
# WHERE id = '{1}'""").fetchone()
# con.close()
# curr_map = curr_map_res[0].split('.')[0]
# print(curr_map)

import pygame
import time
from pygame.locals import *

# pygame.init()
# image_surf = pygame.image.load("dddd.png")
# angle = 90
# surf = pygame.transform.rotate(image_surf, 90)
# map_image = 'dddd.png'
# pygame.image.save(surf, map_image)
#
# len_ac = i[2] - i[4]
# len_cb = i[1] - i[3]
# len_ab = math.sqrt((len_ac ** 2) + (len_cb ** 2))
# if len_ab != 0:
#     if i[0] < i[3]:
#         angle = -math.degrees(math.asin(len_ac / len_ab))
#         angle = 90 + (90 - angle)
#     else:
#         angle = -math.degrees(math.asin(len_ac / len_ab))
#
# len_ac = i[1] - i[4]
# len_cb = i[0] - i[3]
# len_ab = math.sqrt((len_ac ** 2) + (len_cb ** 2))
# if len_ab != 0:
#     if i[0] < i[3]:
#         angle = -math.degrees(math.asin(len_ac / len_ab))
#         angle = 90 + (90 - angle)
#     else:
#         angle = -math.degrees(math.asin(len_ac / len_ab))

# image_point = {'РПК': 'images/RPK.png', 'ПК': 'images/PK.png, ', 'крупонкалиберный': 'images/large-caliber.png',
#                'РПГ': 'images/RPG.png', 'СПГ': 'images/SPG.png', 'АГС': 'images/AGS.png',
#                'БМП': 'images/BMP.png', 'БМП с тралом': 'images/BMP_tral.png',
#                'БТР': 'images/BTR.png', 'БРМ': 'images/BRM.png', 'БРДМ': 'images/BRDM.png'}
# print(' '.join(image_point.keys()).split())
