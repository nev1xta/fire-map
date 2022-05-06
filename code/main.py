import os
import sys

import pygame
import requests
from PIL import Image
import sqlite3
import pygame_gui
from werkzeug.security import generate_password_hash, check_password_hash
import pickle


clock = pygame.time.Clock()
pt = ''
run = True
updating = False
map_file = "map.png"
left_bottom, rith_top = [36.6, 54.6], [38.6, 56.6]
center_geo = [37.6, 55.7]
center_py = [225, 225]
sp = 0.004
z = None
points_list = []


def update_map(pt):
    params1 = {
        "ll": f'{center_geo[0]},{center_geo[1]}',
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
    return response


update_map(pt)


im = Image.open("map.png")
(width, height) = im.size
pygame.init()
screen = pygame.display.set_mode((650, height))

manager = pygame_gui.UIManager((650, 450))
back = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((470, 390), (160, 50)), text="Назад", manager=manager
)
confirm = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((470, 330), (160, 50)), text="подтвердить", manager=manager
)
save = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((470, 270), (160, 50)), text="сохранить", manager=manager
)


menu_manager = pygame_gui.UIManager((650, 450))
start = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((250, 275), (150, 50)), text="Начать", manager=menu_manager
)
login_line = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((225, 125), (200, 50)), manager=menu_manager
)
password_line = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((225, 175), (200, 50)), manager=menu_manager
)


def show_menu():
    global menu_manager, start
    menu_bg = pygame.image.load('menu_bg.jpg')
    hash_password = []
    password = 'h'
    login = 'h'
    show = True
    result = []
    while show:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start:
                    con = sqlite3.connect("db/fire-map_data.db")
                    cur = con.cursor()
                    hash_password = cur.execute(f"""SELECT hashed_password FROM users 
                    WHERE (login = '{login}')""").fetchone()
                    if not hash_password is None:
                        if check_password_hash(hash_password[0], password):
                            result = cur.execute(f"""SELECT position_id FROM users
                            WHERE (login = '{login}')""").fetchone()
                            con.close()
                        if result:
                            main_cycle(result, login, password)

                    else:
                        diolog_window = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((125, 125), (380, 200)),
                            manager=menu_manager,
                            window_title='Ошибка входа',
                            action_long_desc='Не верный логин или пароль!',
                            blocking=True
                        )
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == login_line:
                    login = login_line.text
                if event.ui_element == password_line:
                    password = password_line.text

            menu_manager.process_events(event)
        menu_manager.update(time_delta)
        screen.fill((220, 220, 220))
        screen.blit(menu_bg, (0, 0))
        menu_manager.draw_ui(screen)
        pygame.display.flip()


def coord_click(x, y, w, h, vz):
    dx = x - center_py[0]
    dx_geo = center_geo[0] + (3 * dx * sp / w)

    dy = center_geo[1] - y
    dy_geo = center_geo[1] + (0.1 * dy * sp / h)
    if vz:
        print('да')
        dy_geo += (dy_geo - center_geo[1]) * 20
        if center_geo[0] < dx_geo:
            dx_geo -= (dx_geo - center_geo[0]) / 3.7
        elif center_geo[0] > dx_geo:
            dx_geo += (center_geo[0] - dx_geo) / 3.7
    else:
        if center_geo[1] < dy_geo:
            dy_geo -= (dy_geo - center_geo[1]) / 7
        elif center_geo[1] > dy_geo:
            dy_geo -= (center_geo[1] - dy_geo) / 7
        if center_geo[0] < dx_geo:
            dx_geo += (dx_geo - center_geo[0]) / 15
        elif center_geo[0] > dx_geo:
            dx_geo -= (center_geo[0] - dx_geo) / 15
    print(dx_geo, dy_geo)
    return dx_geo, dy_geo


# def coord_click_py(dx_geo, dy_geo, w, h, ssp, vz):
#     global center_py
#     dx = (-dx_geo + center_geo[0] + (3 * ssp / w))
#
#     dy = (-dy_geo + center_geo[1] + (2 * sp / h))
#     if vz:
#         if center_py[1] < dy:
#             dy -= (dy - center_py[1]) / 2.5
#
#         elif center_py[1] > dy:
#             dy += (center_py[1] - dy) / 3.5
#
#         if center_py[0] < dx:
#             dx -= (dx - center_py[0]) / 4
#
#         elif center_py[0] > dx:
#             dx += (center_py[0] - dx) / 2.7
#     return dx, dy


def point_draw(vz, pos):
    global screen, points_list, width, height
    l = 0
    if not vz:
        con = sqlite3.connect("db/fire-map_data.db")
        cur = con.cursor()
        points_l = cur.execute(f"""SELECT point_id, x0, y0 FROM points_on_maps 
        WHERE position_id = '{pos}'""").fetchall()
        con.close()
        for i in points_l:
            con = sqlite3.connect("db/fire-map_data.db")
            cur = con.cursor()
            point_name = cur.execute(f"""SELECT id, type, image_point FROM points 
            WHERE id = '{i[0]}'""").fetchall()
            con.close()
            for j in point_name:
                if j[0] == i[0]:
                    image = pygame.image.load(j[2]).convert_alpha()
                    image.set_colorkey((255, 255, 255))
                    screen.blit(image, (i[1], i[2]))
    if vz:
        pass
        # con = sqlite3.connect("fire-map_data.db")
        # cur = con.cursor()
        # center_geo_ot = cur.execute(f"""SELECT x0, y0 FROM positions
        #     WHERE id < 4""").fetchall()
        # points_l = cur.execute(f"""SELECT point_id, x0, y0 FROM points_on_maps """).fetchall()
        # con.close()
        # for h in center_geo_ot:
        #     for i in points_l:
        #         l += 1
        #         con = sqlite3.connect("fire-map_data.db")
        #         cur = con.cursor()
        #         point_name = cur.execute(f"""SELECT id, type, image_point FROM points
        #         WHERE id = '{i[0]}'""").fetchall()
        #         con.close()
        #         dx_geo = coord_click(i[1], i[2], width, height, h[0], h[1], 0.0015, False, True)[0]
        #         dy_geo = coord_click(i[1], i[2], width, height, h[0], h[1], 0.0015, False, True)[1]
        #         fx = coord_click_py(dx_geo, dy_geo, width, height, sp, vz)[0]
        #         fy = coord_click_py(dx_geo, dy_geo, width, height, sp, vz)[1]
        #         print(f"GEO_X{l}:", dx_geo, "GEO_Y:", dy_geo, "FX:", fx, "FY:", fy)
        #         if l == 6:
        #             l = 0
        #         for j in point_name:
        #             if j[0] == i[0]:
        #                 image = pygame.image.load(j[2]).convert_alpha()
        #                 image.set_colorkey((255, 255, 255))
        #                 screen.blit(image, (fx, fy))

    for i in points_list:
        if i[2] == 'РПК':
            image = pygame.image.load('images/RPK.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'ПК':
            image = pygame.image.load('images/PK.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'крупонкалиберный':
            image = pygame.image.load('images/large-caliber.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'РПГ':
            image = pygame.image.load('images/RPG.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'СПГ':
            image = pygame.image.load('images/SPG.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'АГС':
            image = pygame.image.load('images/AGS.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'БМП':
            image = pygame.image.load('images/BMP.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'БМП с тралом':
            image = pygame.image.load('images/BMP_tral.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'БТР':
            image = pygame.image.load('images/BTR.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'БРМ':
            image = pygame.image.load('images/BRM.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))
        if i[2] == 'БРДМ':
            image = pygame.image.load('images/BRDM.png').convert_alpha()
            image.set_colorkey((255, 255, 255))
            screen.blit(image, (i[0], i[1]))


def main_cycle(res, login, password):
    global run, center_geo, z, sp, pt, updating, map_file, points_list
    a = ''
    vz = False
    x = -300
    y = -300
    point = ''
    con = sqlite3.connect("db/fire-map_data.db")
    cur = con.cursor()
    b = cur.execute(f"""SELECT MAX(id) FROM points_on_maps""").fetchone()
    con.close()
    if b[0]:
        id_point = b[0]
    else:
        id_point = 0
    if res[0] == 4:
        platoons = pygame_gui.elements.UIDropDownMenu(
            options_list=['1 отделение', '2 отделение', '3 отделение'], starting_option='',
            relative_rect=pygame.Rect((470, 50), (160, 50)), manager=manager)
        vz = True
    platoon = ''
    if not vz:
        con = sqlite3.connect("db/fire-map_data.db")
        cur = con.cursor()

        result = cur.execute(f"""SELECT position_name FROM users 
        WHERE (login = '{login}')""").fetchall()

        coords = cur.execute(f"""SELECT x0, y0 FROM positions
        WHERE (name_position = '{result[0][0]}')""").fetchall()
        con.close()
        center_geo[0], center_geo[1] = coords[0][0], coords[0][1]
        z = 16
        sp = 0.0015
        updating = True
        points = pygame_gui.elements.UIDropDownMenu(
            options_list=['РПК', 'ПК', 'крупонкалиберный', 'РПГ', 'СПГ', 'АГС', 'БМП', 'БМП с тралом', 'БТР',
                          'БРМ', 'БРДМ'],
            starting_option='',
            relative_rect=pygame.Rect((470, 50), (160, 50)), manager=manager)
    while run:

        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if vz:
                    platoon = event.text
                if not vz:
                    point = event.text
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == save:
                    map_image = 'map_platoon.png'
                    pygame.image.save(screen, map_image)

                if event.ui_element == back:
                    if vz:
                        if center_geo != [37.6, 55.7]:
                            center_geo = [37.6, 55.7]
                            z = None
                            sp = 0.004
                            pt = '37.6,55.7,round'
                            updating = True
                    else:

                        points_list.pop(-1)
                if event.ui_element == confirm:
                    if vz:
                        if center_geo != [37.6, 55.7] and platoon != '':
                            con = sqlite3.connect("db/fire-map_data.db")
                            cur = con.cursor()
                            cur.execute(f'UPDATE positions SET x0 = {center_geo[0]}, y0 = {center_geo[1]},'
                                        f' complited = "processed"'
                                        f'WHERE name_position = "Командир отделения №{platoon[0]}"')
                            cur.execute(f'DELETE from point_on_maps WHERE position_id = {platoon[0]}')
                            con.commit()
                            con.close()
                            center_geo = [37.6, 55.7]
                            z = None
                            sp = 0.004
                            updating = True
                    if not vz:
                        con = sqlite3.connect("db/fire-map_data.db")
                        cur = con.cursor()
                        id_point_db = cur.execute(f"""SELECT id FROM points
                               WHERE (type = '{point}')""").fetchone()
                        con.close()
                        for i in points_list:
                            id_point += 1
                            con = sqlite3.connect("db/fire-map_data.db")
                            cur = con.cursor()
                            cur.execute(f'INSERT INTO points_on_maps(id, point_id, position_id, x0, y0) '
                                        f'VALUES("{id_point}", "{id_point_db[0]}", "{res[0]}", "{i[0]}", "{i[1]}")')
                            con.commit()
                            con.close()
                        points_list.clear()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if center_geo[0] == 37.6 and center_geo[1] == 55.7 and x <= 450 and vz:
                    center_geo[0] = coord_click(x, y, width, height, True)[0]
                    center_geo[1] = coord_click(x, y, width, height, True)[1]
                    z = 16
                    sp = 0.0015
                    updating = True
                elif x <= 450 and not vz:
                    if point:
                        points_list.append([x, y, point])
            manager.process_events(event)

        if updating:
            update_map(pt)
            updating = False
        manager.update(time_delta)
        screen.fill((220, 220, 220))
        screen.blit(pygame.image.load(map_file), (0, 0))
        manager.draw_ui(screen)

        point_draw(vz, res[0])
        pygame.display.flip()


show_menu()
pygame.quit()

# Удаляем за собой файл с изображением.
