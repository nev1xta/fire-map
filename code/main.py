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
run = True
updating = False
quarter = ['pv', 'lv', 'ln', 'pn']
map_file_name = "map.png"
center_py = [225, 225]
points_list = []
num_map = 0
login = 'h'


def update_map(vz, num=0):
    global map_file_name, login, quarter
    direc = ''
    is_none = ''
    if vz:
        direc = "maps_vz/"
    if not vz:
        direc = "maps_otd/"

    con = sqlite3.connect("db/fire-map_data.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT position_name FROM users
    WHERE (login = '{login}')""").fetchone()
    print(result)
    coords = cur.execute(f"""SELECT x1 FROM positions
    WHERE (name_position = '{result[0]}')""").fetchone()
    con.close()

    if coords[0] == 0:
        is_none = "maps_otd/None.png"
    elif vz and num != 0:
        print('да')
        is_none = f"maps_otd/{coords[0][:-4]}_{quarter[num - 1]}.png"
    else:
        is_none = direc + coords[0]
    map_file_name = "map.png"
    map_file_1 = is_none
    map_file = Image.open(map_file_1)
    map_file.save(map_file_name, 'png')
    return is_none


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
    global menu_manager, start, login
    menu_bg = pygame.image.load('menu_bg.jpg')
    hash_password = []
    password = 'h'
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
                        if result[0] == 4:
                            select_menu()
                        else:
                            main_cycle(result)

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


select_manager = pygame_gui.UIManager((650, 450))
btn_map_1 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((250, 275), (150, 50)), text="Карта №1", manager=select_manager
)


def select_menu():
    menu_bg = pygame.image.load('menu_bg.jpg')
    show = True
    while show:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btn_map_1:
                    con = sqlite3.connect("db/fire-map_data.db")
                    cur = con.cursor()
                    cur.execute(f'UPDATE positions SET x1 = "map_1.png"'
                                f'WHERE name_position = "Командир взвода"')
                    con.commit()
                    con.close()
                    main_cycle((4,))

            select_manager.process_events(event)
        select_manager.update(time_delta)
        screen.fill((220, 220, 220))
        screen.blit(menu_bg, (0, 0))
        select_manager.draw_ui(screen)
        pygame.display.flip()


def coord_click(x, y, w, h, vz):
    pass


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


def main_cycle(res):
    global run, updating, map_file_name, points_list, login
    vz = False
    current = 'maps_vz/'
    num = 0
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
    update_map(vz)
    platoon = ''
    if not vz:
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
                        num = 0
                        updating = True
                    else:
                        if points_list:
                            points_list.pop(-1)
                if event.ui_element == confirm:
                    if vz:
                        if platoon != '' and 'maps_vz/' not in current:
                            con = sqlite3.connect("db/fire-map_data.db")
                            cur = con.cursor()
                            cur.execute(f'UPDATE positions SET x1 = "{current[9:]}", complited = "processed"'
                                        f'WHERE name_position = "Командир отделения №{platoon[0]}"')
                            cur.execute(f'DELETE from points_on_maps WHERE position_id = {platoon[0]}')
                            con.commit()
                            con.close()
                            num = 0
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
                if x <= 450 and vz:
                    if x > center_py[0] and y < center_py[1]:
                        num = 1
                    elif x < center_py[0] and y < center_py[1]:
                        num = 2
                    elif x < center_py[0] and y > center_py[1]:
                        num = 3
                    else:
                        num = 4
                    updating = True
                elif x <= 450 and not vz:
                    if point:
                        points_list.append([x, y, point])
            manager.process_events(event)

        if updating:
            current = update_map(vz, num)
            updating = False
        manager.update(time_delta)
        screen.fill((220, 220, 220))
        screen.blit(pygame.image.load(map_file_name), (0, 0))
        manager.draw_ui(screen)

        point_draw(vz, res[0])
        pygame.display.flip()


show_menu()
pygame.quit()

# Удаляем за собой файл с изображением.
