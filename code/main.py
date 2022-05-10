import pygame

from PIL import Image, ImageDraw, ImageFont
import sqlite3
import pygame_gui
from werkzeug.security import generate_password_hash, check_password_hash
import math

clock = pygame.time.Clock()
run = True
updating = False
quarter = ['pv', 'lv', 'ln', 'pn']
map_file_name = "map.png"
center_py = [225, 225]
points_list = []
login = 'h'
zvan = ''


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
    coords = cur.execute(f"""SELECT img_map FROM positions
    WHERE (name_position = '{result[0]}')""").fetchone()
    con.close()

    if coords[0] == '':
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
    relative_rect=pygame.Rect((470, 340), (160, 50)), text="подтвердить", manager=manager
)
save = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((470, 290), (160, 50)), text="сохранить", manager=manager
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
    global menu_manager, start, login, zvan
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
                        if result:
                            if result[0] == 4:
                                con = sqlite3.connect("db/fire-map_data.db")
                                cur = con.cursor()
                                map = cur.execute(f"""SELECT img_map FROM positions
                                                    WHERE (id = '{result[0]}')""").fetchone()
                                con.close()
                                print(map)
                                if map[0]:
                                    main_cycle(result)
                                if not map[0]:
                                    select_menu()
                            else:
                                con = sqlite3.connect("db/fire-map_data.db")
                                cur = con.cursor()
                                zvan = cur.execute(f"""SELECT position_name FROM users
                                                    WHERE (id = '{result[0]}')""").fetchone()
                                con.close()
                                main_cycle(result)
                        else:
                            diolog_window = pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect((125, 125), (380, 200)),
                                manager=menu_manager,
                                window_title='Ошибка входа',
                                action_long_desc='Не верный логин или пароль!',
                                blocking=True
                            )
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
    relative_rect=pygame.Rect((75, 100), (200, 50)), text="Карта №1", manager=select_manager
)
btn_map_2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((375, 100), (200, 50)), text="Карта №2", manager=select_manager
)
btn_map_3 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((75, 200), (200, 50)), text="Карта №3", manager=select_manager
)
btn_map_4 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((375, 200), (200, 50)), text="Карта №4", manager=select_manager
)


def select_menu():
    menu_bg = pygame.image.load('menu_bg.jpg')
    show = True
    num_map = 1
    while show:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btn_map_1:
                    num_map = 1
                if event.ui_element == btn_map_2:
                    num_map = 2
                if event.ui_element == btn_map_3:
                    num_map = 3
                if event.ui_element == btn_map_4:
                    num_map = 4
                con = sqlite3.connect("db/fire-map_data.db")
                cur = con.cursor()
                cur.execute(f'UPDATE positions SET img_map = "map_{num_map}.png"'
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


def point_draw(vz, pos):
    global screen, points_list, width, height
    angle = 0
    if not vz:
        con = sqlite3.connect("db/fire-map_data.db")
        cur = con.cursor()
        points_l = cur.execute(f"""SELECT point_id, x0, y0, x1, y1 FROM points_on_maps 
        WHERE position_id = '{pos}'""").fetchall()
        con.close()
        for i in points_l:
            con = sqlite3.connect("db/fire-map_data.db")
            cur = con.cursor()
            point_name = cur.execute(f"""SELECT id, name_point, image_point FROM points 
            WHERE id = '{i[0]}'""").fetchall()
            con.close()

            len_ac = i[2] - i[4]
            len_cb = i[1] - i[3]
            len_ab = math.sqrt((len_ac ** 2) + (len_cb ** 2))
            if len_ab != 0:
                if i[1] < i[3]:
                    angle = -math.degrees(math.asin(len_ac / len_ab))
                    angle = 90 + (90 - angle)
                else:
                    angle = -math.degrees(math.asin(len_ac / len_ab))

            for j in point_name:
                if j[0] == i[0]:
                    if j[2] != 'images/arrow.png':
                        image = pygame.image.load(j[2]).convert_alpha()
                        if j[2] != 'images/sign.png':
                            image = pygame.transform.rotate(image, angle)
                        image.set_colorkey((255, 255, 255))
                        screen.blit(image, (i[1], i[2]))
                    if j[2] == 'images/arrow.png':
                        if i[3] > 450:
                            i[3] = i[3] - (i[3] - 450)
                            pygame.draw.line(screen, (255, 0, 0), (i[1], i[2]), (i[3], i[4]), 3)
                        else:
                            pygame.draw.line(screen, (255, 0, 0), (i[1], i[2]), (i[3], i[4]), 3)
                        image = pygame.image.load(j[2]).convert_alpha()
                        image = pygame.transform.rotate(image, angle)
                        image.set_colorkey((255, 255, 255))
                        if i[3] < i[1] and i[4] > i[2] and angle <= 45:
                            screen.blit(image, (i[3] - 8, i[4] - 4))
                        elif i[3] < i[1] and i[4] > i[2] and angle >= 45:
                            screen.blit(image, (i[3] - 6, i[4] - 2))
                        else:
                            screen.blit(image, (i[3] - 4, i[4] - 4))
    if vz:
        con = sqlite3.connect("db/fire-map_data.db")
        cur = con.cursor()
        points_l = cur.execute(f"""SELECT point_id, x0, y0, x1, y1, position_id FROM points_on_maps """).fetchall()
        con.close()
        for i in points_l:
            con = sqlite3.connect("db/fire-map_data.db")
            cur = con.cursor()
            curr_map_res = cur.execute(f"""SELECT img_map FROM positions
            WHERE id = '{i[5]}'""").fetchone()
            curr_map = curr_map_res[0].split('.')[0]
            point_name = cur.execute(f"""SELECT id, name_point, image_point FROM points 
            WHERE id = '{i[0]}'""").fetchall()
            con.close()
            len_ac = i[2] - i[4]
            len_cb = i[1] - i[3]
            len_ab = math.sqrt((len_ac ** 2) + (len_cb ** 2))
            if len_ab != 0:
                if i[1] < i[3]:
                    angle = -math.degrees(math.asin(len_ac / len_ab))
                    angle = 90 + (90 - angle)
                else:
                    angle = -math.degrees(math.asin(len_ac / len_ab))
            for j in point_name:
                if j[0] == i[0]:
                    if j[2] != 'images/arrow.png':
                        x = i[1] / 2
                        y = i[2] / 2
                        if curr_map[-1] == 'n':
                            y += 225
                        if curr_map[-2] == 'p':
                            x += 225
                        image = pygame.image.load(j[2]).convert_alpha()
                        if j[2] != 'images/sign.png':
                            image = pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2))
                        image = pygame.transform.rotate(image, angle)
                        image.set_colorkey((255, 255, 255))
                        screen.blit(image, (x, y))
                    if j[2] == 'images/arrow.png':
                        x = i[1] / 2
                        y = i[2] / 2
                        x1 = i[3] / 2
                        y1 = i[4] / 2
                        if curr_map[-1] == 'n':
                            y += 225
                            y1 += 225
                        if curr_map[-2] == 'p':
                            x += 225
                            x1 += 225
                        pygame.draw.line(screen, (255, 0, 0), (x, y), (x1, y1), 3)
                        image = pygame.image.load(j[2]).convert_alpha()
                        image = pygame.transform.rotate(image, angle)
                        image.set_colorkey((255, 255, 255))
                        if x1 < x and y1 > y and angle <= 45:
                            screen.blit(image, (x1 - 8, y1 - 4))
                        elif x1 < x and y1 > y and angle >= 45:
                            screen.blit(image, (x1 - 6, y1 - 2))
                        else:
                            screen.blit(image, (x1 - 4, y1 - 4))

    image_point = {'РПК': 'images/RPK.png', 'ПК': 'images/PK.png', 'крупнокалиберный': 'images/large-caliber.png',
                   'РПГ': 'images/RPG.png', 'СПГ': 'images/SPG.png', 'АГС': 'images/AGS.png',
                   'БМП': 'images/BMP.png', 'БМП с тралом': 'images/BMP_tral.png',
                   'БТР': 'images/BTR.png', 'БРМ': 'images/BRM.png', 'БРДМ': 'images/BRDM.png',
                   'Ориентир': 'images/sign.png'}
    for i in points_list:
        if len(i) > 3:
            len_ac = i[1] - i[4]
            len_cb = i[0] - i[3]
            len_ab = math.sqrt((len_ac ** 2) + (len_cb ** 2))
            if len_ab != 0:
                if i[0] < i[3]:
                    angle = -math.degrees(math.asin(len_ac / len_ab))
                    angle = 90 + (90 - angle)
                else:
                    angle = -math.degrees(math.asin(len_ac / len_ab))

            if i[2] in ' '.join(image_point.keys()).split():
                image = pygame.image.load(image_point[i[2]]).convert_alpha()
                if i[2] != 'Ориентир':
                    image = pygame.transform.rotate(image, angle)
                image.set_colorkey((255, 255, 255))
                screen.blit(image, (i[0], i[1]))
                angle = 0

            elif i not in ' '.join(image_point.keys()).split():
                if i[3] > 450:
                    i[3] = i[3] - (i[3] - 450)
                    pygame.draw.line(screen, (255, 0, 0), (i[0], i[1]), (i[3], i[4]), 3)
                else:
                    pygame.draw.line(screen, (255, 0, 0), (i[0], i[1]), (i[3], i[4]), 3)
                image = pygame.image.load('images/arrow.png').convert_alpha()
                image = pygame.transform.rotate(image, angle)
                print(angle)
                image.set_colorkey((255, 255, 255))
                if i[3] < i[0] and i[4] > i[1] and angle <= 45:
                    screen.blit(image, (i[3] - 8, i[4] - 4))
                elif i[3] < i[0] and i[4] > i[1] and angle >= 45:
                    screen.blit(image, (i[3] - 6, i[4] - 2))
                else:
                    screen.blit(image, (i[3] - 4, i[4] - 4))


def main_cycle(res):
    global run, updating, map_file_name, points_list, login, zvan
    vz = False
    options_list_point = []
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
            relative_rect=pygame.Rect((470, 230), (160, 50)), manager=manager)
        close_map = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((470, 60), (160, 50)), text="закрыть", manager=manager)
        points = None
        vz = True
    update_map(vz)
    platoon = ''
    if not vz:
        platoons = None
        close_map = None
        options_list_point = ['РПК', 'ПК', 'крупнокалиберный', 'РПГ', 'СПГ', 'АГС', 'БМП', 'БМП с тралом', 'БТР',
                              'БРМ', 'БРДМ', 'Сектор обстрела', 'Ориентир']
        points = pygame_gui.elements.UIDropDownMenu(
            options_list=options_list_point,
            starting_option='',
            relative_rect=pygame.Rect((470, 230), (160, 50)), manager=manager)
        updating = True

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
                    text1 = ''
                    text2 = ''
                    text3 = ''
                    font = ImageFont.truetype('arial.ttf', size=20)
                    if vz:
                        text1 = 'КАРТОЧКА ОГНЯ 1 МСВ'
                        text2 = 'командир 1 МСВ ______'
                        text3 = f'"_____"_______20__ г.'
                    if not vz:
                        text1 = f'КАРТОЧКА ОГНЯ {zvan[0][-1]} МСО'
                        text2 = f'командир {zvan[0][-1]} МСО ______'
                        text3 = f'"_____"_______20__ г.'
                    map_image = 'map_platoon.png'
                    pygame.image.save(screen, map_image)
                    im = Image.open('map_platoon.png')
                    im_crop_outside = im.crop((0, 0, 450, 450))
                    a = ImageDraw.Draw(im_crop_outside)
                    a.text((100, 20), text1, fill="White", anchor="lt", font=font)
                    a.text((100, 380), text2, fill="White", anchor="lt", font=font)
                    a.text((100, 420), text3, fill="White", anchor="lt", font=font)
                    im_crop_outside.save('map_platoon.png', quality=95)

                if event.ui_element == close_map:
                    con = sqlite3.connect("db/fire-map_data.db")
                    cur = con.cursor()
                    cur.execute(f"""DELETE from points_on_maps""")
                    print('удалил')
                    cur.execute(f"""UPDATE positions SET img_map = ''""")
                    con.commit()
                    con.close()
                    select_menu()
                    return None
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
                            cur.execute(f'UPDATE positions SET img_map = "{current[9:]}", complited = "processed"'
                                        f'WHERE name_position = "Командир отделения №{platoon[0]}"')
                            cur.execute(f'DELETE from points_on_maps WHERE position_id = {platoon[0]}')
                            con.commit()
                            con.close()
                            num = 0
                            updating = True
                    if not vz:
                        for i in points_list:
                            if len(i) > 3:
                                id_point += 1
                                con = sqlite3.connect("db/fire-map_data.db")
                                cur = con.cursor()
                                id_point_db = cur.execute(f"""SELECT id FROM points
                                       WHERE (name_point = '{i[2]}')""").fetchone()
                                cur.execute(f'INSERT INTO points_on_maps(id, point_id, position_id, x0, y0, x1, y1) '
                                            f'VALUES("{id_point}", "{id_point_db[0]}", "{res[0]}", "{i[0]}", "{i[1]}", '
                                            f'"{i[3]}", "{i[4]}")')
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
                if point and options_list_point:
                    if options_list_point.index(point) >= 5 and x <= 420 and not vz:
                        points_list.append([x, y, point])
                    elif options_list_point.index(point) < 5 and x <= 430 and not vz:
                        points_list.append([x, y, point])
                    elif options_list_point.index(point) > 10 and x <= 450 and not vz:
                        points_list.append([x, y, point])
                    elif options_list_point.index(point) > 11 and x <= 430 and not vz:
                        points_list.append([x, y, point])
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = event.pos
                if points_list:
                    points_list[-1].append(x1)
                    points_list[-1].append(y1)
                print(points_list)
                for i in points_list:
                    if len(i) < 4:
                        points_list.pop(points_list.index(i))
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
