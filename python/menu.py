import pygame as pg
from settings import font, ITEM_PLANT, ITEM_MAX, ITEM_N, ITEM_LEN, L_I, SYNTHESIS_ANIMAL, SYNTHESIS_PLANT, PATH_SAVES, \
    PATH_WORLDS, FPS, PATH_FONT, ITEM_L_ANIMAL, ITEM_L_PLANT, ITEM_L_CORPSE, PATH_SCREENSHOT_PNG, SCREENSHOT_SIZE, \
    PATH_SCREENSHOT_LIFEI, PATH_RECORDS, PATH_SCRIPTS, create_dirs
from os import listdir
from math import sin
import random
from random import random, randint
import world
from tools import int_to_bin
import pyperclip
import threading
import time as time_module


def draw(size, figures) -> pg.Surface:
    sc = pg.Surface(size=size)
    for f in figures:
        if f[0] == 0:
            pg.draw.rect(sc, f[1], f[2], f[3])
        elif f[0] == 1:
            pg.draw.line(sc, f[1], f[2], f[3], f[4])
        elif f[0] == 2:
            font.draw_text_d(sc, f[1], f[2])
        elif f[0] == 3:
            pg.draw.polygon(sc, f[1], f[2])
        elif f[0] == 4:
            pg.draw.circle(sc, f[1], f[2], f[3])
    return sc


menu_gen = draw((470, 300), (
    (0, (239, 228, 176), (0, 0, 470, 300), 0),
    (0, (0, 0, 0), (0, 0, 470, 300), 3),
    (0, (0, 0, 0), (205, 280, 15, 15), 0),
    (0, (0, 0, 0), (275, 280, 15, 15), 0),
    (0, (0, 0, 0), (425, 280, 40, 15), 0),
    (2, "save", (429, 280))
))

menu_item = draw((130, 300), (
    (0, (239, 228, 176), (0, 0, 130, 300), 0),
    (0, (0, 0, 0), (0, 0, 130, 300), 3),
    (1, (0, 0, 0), (0, 60), (130, 60), 3),
    (0, (0, 0, 0), (20, 280, 15, 15), 0),
    (0, (0, 0, 0), (90, 280, 15, 15), 0),
    (0, (0, 0, 0), (105, 40, 15, 15), 0)
))

menu_corpse = draw((130, 300), (
    (0, (239, 228, 176), (0, 0, 130, 300), 0),
    (0, (0, 0, 0), (0, 0, 130, 300), 3),
    (1, (0, 0, 0), (0, 60), (130, 60), 3),
    (0, (0, 0, 0), (20, 280, 15, 15), 0),
    (0, (0, 0, 0), (90, 280, 15, 15), 0),
    (3, (127, 127, 127), ((10, 40), (20, 30), (30, 40), (20, 50)))
))

menu_copy = draw((600, 300), (
    (0, (239, 228, 176), (0, 0, 600, 300), 0),
    (0, (0, 0, 0), (0, 0, 600, 300), 2),
    (0, (0, 0, 0), (515, 270, 15, 15), 0),
    (0, (0, 0, 0), (580, 270, 15, 15), 0)
))

menu_simulation = draw((260, 225), (
    (0, (239, 228, 176), (0, 0, 260, 225), 0),
    (0, (0, 0, 0), (0, 0, 260, 225), 2)
))

menu_time = draw((260, 90), (
    (0, (239, 228, 176), (0, 0, 260, 90), 0),
    (0, (255, 201, 14), (2, 45, 32, 18), 0),
    (0, (34, 177, 76), (34, 45, 64, 18), 0),
    (0, (255, 242, 0), (98, 45, 64, 18), 0),
    (0, (0, 162, 232), (162, 45, 64, 18), 0),
    (0, (255, 201, 14), (226, 45, 32, 18), 0),
    (0, (0, 0, 0), (5, 75, 250, 6), 0),
    (0, (0, 0, 0), (0, 0, 260, 90), 2)
))

TT_MAX_RESOURCE = ''
for i__ in [f'{name} = {ITEM_MAX[index]}\n' for index, name in enumerate(ITEM_PLANT)]:
    TT_MAX_RESOURCE += i__
tt = [
    '''# MOUSE(click)
LCM - copy live/load world/grab menu/click menu
WCM - menu animal/plant/corpse\n
# MOUSE(motion)
LCM - motion grab menu
RCM - motion dx & dy\n
# MOUSE(wheel)
up   - scale += 1
down - scale -= 1\n
# KEY(hold)
UP        - simulation speed += 1
DOWN      - simulation speed -= 1
PLUS      - simulation mutate += 1
MINUS     - simulation mutate -= 1

#KEY(push)
f2               - screenshot
f3               - full screenshot
f4               - world screenshot
f5               - world rec''', '''f6               - stop rec
f11              - window/full-screen mode
1 + x            - spawning animal
2 + x            - spawning plant
h                - show/hide help menu
3 + x            - spawning corpse
h                - show/hide help menu
ESCAPE           - close first menu
n                - show/hide hp block
q                - show/hide size world menu
t                - show/hide menu time
k + TAB          - clear 25% world
k + TAB + DELETE - clear world
a                - spawn animal
p                - spawn plant
c                - spawn corpse
b                - place block
m                - set speed equal to fps or 0
d                - do/don't day cycle
o                - delete obj
s                - save world(ESCAPE - exit, ENTER - save)
SPACE            - one tick simulate world
ENTER            - show/hide copy menu''', f'''LEFT             - simulation speed -= 1
RIGHT            - simulation speed -= 1
l                - show/hide load world menu
g                - show/hide grid on world
i                - show/hide info
e                - show/hide simulation menu
f                - show/hide graphics
0 + v(press)   - change view mode (all)
1 + v(press)   - change view mode animal)
2 + v(press)   - change view mode (plants)
3 + v(press)   - change view mode (corpse)
4 + v(press)   - change view mode (blocks)
5 + v(press)   - change view mode (mutate)
6 + v(press)   - change view mode previous (item)
7 + v(press)   - change view mode next (item)''', f'''PLANT
1     - mitosis                   - 50e + 10A + 3B
2     - inspect                   -
3     - double inspect            -
4     - jump                      -
5     - double jump               -
6     - back jump                 -
7     - double back jump          -
8     - photosynthesis            -
9     - root                      - 2e
10-22 - synthesis                 - ?
23    - mitosis -> successful     - 50e + 10A + 3B
24    - root -> successful        - 2e
25-37 - synthesis -> successful   - ?''', f'''ANIMAL #1 
1-8   - motion           - 5e + B
9-15  - rotate           - 2e + A
16    - get rotate       - 2e + C
17    - eat              - 3e
18    - mitosis          - 30e + C + 2D
19    - see angle        - e + B
20    - see distance     - e + B
21    - see type         - e + B
22    - inspect          -
23    - double inspect   -
24    - jump             -
25    - double jump      -
26    - back jump        -
27    - double back jump -
28    - attach           - 5e
29    - set marker       - 5e + 3D
30    - get marker       - 5e
31    - del marker       - 10e
32    - say              - e
33    - listen           - e
34    - build            - 2e + 10A + Water + Salt
35-52 - synthesis        - ?''', f'''ANIMAL #2
53-60 - motion -> type              - 5e + B
61    - eat -> successful           - 3e
62    - mitosis -> successful       - 30e + C + 2D
63    - see angle (dist)            - e + B
64    - see angle (type)            - e + B
65    - see angle (dist & type)     - e + B
66    - see distance (angle)        - e + B
67    - see distance (type)         - e + B
68    - see distance (angle & type) - e + B
69    - see type (angle)            - e + B
70    - see type (dist)             - e + B
71    - see type (angle & dist)     - e + B
72    - attach -> successful        - 5e
73    - build -> successful         - 2e + 10A + Water + Salt
74-91 - synthesis -> successful     - ?''']


def generate_text_synthesis(txt, synthesis):
    ss = f'{txt}\n\n'
    max_ = 0
    for i in synthesis:
        material = ''
        for y in range(ITEM_LEN):
            if i[0][y] > 0:
                if i[0][y] == 1:
                    material += f'{ITEM_N[y]} + '
                else:
                    material += f'{i[0][y]}{ITEM_N[y]} + '
        product = ''
        for y in range(ITEM_LEN):
            if i[1][y] > 0:
                if i[1][y] == 1:
                    product += f'{ITEM_N[y]} + '
                else:
                    product += f'{i[1][y]}{ITEM_N[y]} + '
        if len(material[:-3]) + 1 > max_:
            max_ = len(material[:-3]) + 1
        ss += material[:-3] + ' -> ' + product[:-3] + '\n'
    mm = ss
    ss = ''
    for i in mm.split('\n'):
        if i == txt or i == '':
            ss += i + '\n'
        else:
            one = i[:i.index('-')]
            two = i[i.index('-'):]
            for y in range(max_ - i.index('-')):
                one += ' '
            ss += one + two + '\n'
    tt.append(ss[:-1])


generate_text_synthesis('SYNTHESIS PLANT', SYNTHESIS_PLANT)
generate_text_synthesis('SYNTHESIS ANIMAL', SYNTHESIS_ANIMAL)

tt.append(f'MAX RESOURCE\n{TT_MAX_RESOURCE}')


tt_len = len(tt) - 1
help_menu = [pg.Surface(size=(530, 380)) for i in range(tt_len + 1)]
for index, i in enumerate(tt):
    help_menu[index].fill((239, 228, 176))
    pg.draw.rect(help_menu[index], (0, 0, 0), (0, 0, 530, 380), 2)
    pg.draw.rect(help_menu[index], (0, 0, 0), (5, 360, 15, 15))
    pg.draw.rect(help_menu[index], (0, 0, 0), (510, 360, 15, 15))
    for c, text in enumerate(i.split('\n')):
        font.draw_text_l(help_menu[index], text, (10, 10 + c * 15))

settings_menu = pg.Surface((175, 40))
settings_menu.fill((239, 228, 176))
pg.draw.rect(settings_menu, (0, 0, 0), (0, 0, 175, 40), 2)
pg.draw.rect(settings_menu, (240, 240, 240), (10, 10, 70, 15))
pg.draw.rect(settings_menu, (240, 240, 240), (90, 10, 70, 15))

IMAGE_ANIMAL = pg.Surface((20, 20))
IMAGE_ANIMAL.fill((255, 0, 0))
IMAGE_PLANT = pg.Surface((20, 20))
IMAGE_PLANT.set_colorkey((0, 0, 0))
pg.draw.circle(IMAGE_PLANT, (0, 255, 0), (10, 10), 10)
IMAGE_CORPSE = pg.Surface((20, 20))
IMAGE_CORPSE.set_colorkey((0, 0, 0))
pg.draw.polygon(IMAGE_CORPSE, (127, 127, 127), ((10, 0), (20, 10), (10, 20), (0, 10)))
IMAGE_BLOCK = pg.Surface((20, 20))
IMAGE_BLOCK.fill((30, 30, 30))
IMAGE_WATER = pg.Surface((20, 30), pg.SRCALPHA)
IMAGE_WATER.set_colorkey((0, 0, 0))
pg.draw.circle(IMAGE_WATER, (0, 150, 255), (10, 20), 10)
pg.draw.rect(IMAGE_WATER, (0, 0, 0), (0, 0, 20, 20))
pg.draw.polygon(IMAGE_WATER, (0, 150, 255), ((10, 0), (20, 20), (0, 20)))


class MenuAnimal:
    x = 0
    y = 0
    p_i = 0
    p_g = 0
    show_gen = False

    def __init__(self, target):
        self.trg = target

    def motion(self, rel, w, h):
        self.x += rel[0]
        self.y += rel[1]
        if self.x < 0:
            self.x = 0
        elif self.x > w - 130:
            self.x = w - 130
        if self.y < 0:
            self.y = 0
        elif self.y > h - 300:
            self.y = h - 300

    def collide(self, pos):
        if self.show_gen:
            if self.x <= pos[0] <= self.x + 600 and self.y <= pos[1] <= self.y + 300:
                return True
        else:
            if self.x <= pos[0] <= self.x + 130 and self.y <= pos[1] <= self.y + 300:
                return True
        return False

    def click(self, pos):
        if self.x + 105 <= pos[0] <= self.x + 120 and self.y + 40 <= pos[1] <= self.y + 55:
            self.show_gen = not self.show_gen
        if self.x + 20 <= pos[0] <= self.x + 35 and self.y + 280 <= pos[1] <= self.y + 295:
            self.p_i -= 1
        elif self.x + 90 <= pos[0] <= self.x + 105 and self.y + 280 <= pos[1] <= self.y + 295:
            self.p_i += 1
        if self.p_i < 0:
            self.p_i = 0
        elif self.p_i >= L_I:
            self.p_i = L_I - 1

        if self.show_gen:
            if 335 + self.x <= pos[0] <= 350 + self.x and 280 + self.y <= pos[1] <= 295 + self.y:
                self.p_g -= 1
            elif 405 + self.x <= pos[0] <= 420 + self.x and 280 + self.y <= pos[1] <= 295 + self.y:
                self.p_g += 1
            if self.p_g < 0:
                self.p_g = 0
            elif self.p_g >= round(self.trg[3] / 414 + 0.5):
                self.p_g = round(self.trg[3] / 414 + 0.5) - 1
            if 555 + self.x <= pos[0] <= 595 + self.x and 280 + self.y <= pos[1] <= 295 + self.y:
                time = time_module.localtime()
                year = time.tm_year
                mon = str(time.tm_mon) if time.tm_mon > 9 else '0' + str(time.tm_mon)
                day = str(time.tm_mday) if time.tm_mday > 9 else '0' + str(time.tm_mday)
                hour = str(time.tm_hour) if time.tm_hour > 9 else '0' + str(time.tm_hour)
                min_ = str(time.tm_min) if time.tm_min > 9 else '0' + str(time.tm_min)
                sec = str(time.tm_sec) if time.tm_sec > 9 else '0' + str(time.tm_sec)
                name = f'{year}_{mon}_{day}_{hour}_{min_}_{sec}'
                data = bytes(self.trg[4]) + bytes(self.trg[2])
                create_dirs(PATH_SAVES)
                with open(f'{PATH_SAVES}/{name}.lifea', 'wb') as f:
                    f.write(data)
                return True
        return False

    def draw(self, sc, w_s):
        sc.blit(menu_item, (self.x, self.y))
        font.draw_text_l(sc, f'pos: {self.trg[10] - w_s[0]}x{self.trg[11] - w_s[1]}', (10 + self.x, 5 + self.y))
        pg.draw.rect(sc, self.trg[4], (10 + self.x, 20 + self.y, 20, 20))
        r = self.trg[6]
        x4 = (10, 15, 15, 15, 10, 5, 5, 5)[r]
        y4 = (5, 5, 10, 15, 15, 15, 10, 5)[r]
        pg.draw.circle(sc, (0, 0, 0), (10 + x4 + self.x, 20 + y4 + self.y), 1)
        font.draw_text_l(sc, str(self.trg[4][0]), (35 + self.x, 22 + self.y))
        font.draw_text_l(sc, str(self.trg[4][1]), (65 + self.x, 22 + self.y))
        font.draw_text_l(sc, str(self.trg[4][2]), (95 + self.x, 22 + self.y))
        font.draw_text_l(sc, f'mutate: {self.trg[9]}', (10 + self.x, 42 + self.y))
        page_item = self.p_i * 14
        font.draw_text_l(sc, f'{self.p_i + 1}/{L_I}', (55 + self.x, 280 + self.y))
        y = 0
        for ind, item in enumerate(self.trg[1]):
            if y - 13 <= page_item <= y:
                font.draw_text_l(sc, f'{ITEM_N[ind]}: {item}', (10 + self.x, 65 + y % 14 * 15 + self.y))
            y += 1
        if self.show_gen:
            sc.blit(menu_gen, (self.x + 130, self.y))
            x = 0
            y = 0
            for num in self.trg[2][self.p_g * 414: self.p_g * 414 + 414]:
                if x == 23:
                    x = 0
                    y += 1
                if y == 19:
                    break
                txt = f"{'0123456789ABCDEF'[num // 16]}{'0123456789ABCDEF'[num % 16]}"
                pos = (135 + x * 20 + self.x, 5 + y * 15 + self.y)
                if self.trg[5] == self.p_g * 414 + x + y * 23:
                    pg.draw.rect(sc, (64, 64, 255), (pos, (16, 16)))
                    font.draw_text_d(sc, txt, pos)
                else:
                    font.draw_text_l(sc, txt, pos)
                x += 1
            font.draw_text_l(sc, f'{self.trg[5]}/{self.trg[3] - 1}', (135 + self.x, 280 + self.y))
            font.draw_text_l(sc, f'{self.p_g + 1}/{round(self.trg[3] / 414 + 0.5)}', (360 + self.x, 280 + self.y))


class MenuPlant:
    x = 0
    y = 0
    p_i = 0
    p_g = 0
    show_gen = False

    def __init__(self, target, pos):
        self.trg = target
        self.trg_x, self.trg_y = pos

    def motion(self, rel, w, h):
        self.x += rel[0]
        self.y += rel[1]
        if self.x < 0:
            self.x = 0
        elif self.x > w - 130:
            self.x = w - 130
        if self.y < 0:
            self.y = 0
        elif self.y > h - 300:
            self.y = h - 300

    def collide(self, pos):
        if self.show_gen:
            if self.x <= pos[0] <= self.x + 600 and self.y <= pos[1] <= self.y + 300:
                return True
        else:
            if self.x <= pos[0] <= self.x + 130 and self.y <= pos[1] <= self.y + 300:
                return True
        return False

    def click(self, pos):
        if self.x + 105 <= pos[0] <= self.x + 120 and self.y + 40 <= pos[1] <= self.y + 55:
            self.show_gen = not self.show_gen
        if self.x + 20 <= pos[0] <= self.x + 35 and self.y + 280 <= pos[1] <= self.y + 295:
            self.p_i -= 1
        elif self.x + 90 <= pos[0] <= self.x + 105 and self.y + 280 <= pos[1] <= self.y + 295:
            self.p_i += 1
        if self.p_i < 0:
            self.p_i = 0
        elif self.p_i >= L_I:
            self.p_i = L_I - 1
        if self.show_gen:
            if 335 + self.x <= pos[0] <= 350 + self.x and 280 + self.y <= pos[1] <= 295 + self.y:
                self.p_g -= 1
            elif 405 + self.x <= pos[0] <= 420 + self.x and 280 + self.y <= pos[1] <= 295 + self.y:
                self.p_g += 1
            if self.p_g < 0:
                self.p_g = 0
            elif self.p_g >= round(self.trg[3] / 414 + 0.5):
                self.p_g = round(self.trg[3] / 414 + 0.5) - 1
            if 555 + self.x <= pos[0] <= 595 + self.x and 280 + self.y <= pos[1] <= 295 + self.y:
                time = time_module.localtime()
                year = time.tm_year
                mon = str(time.tm_mon) if time.tm_mon > 9 else '0' + str(time.tm_mon)
                day = str(time.tm_mday) if time.tm_mday > 9 else '0' + str(time.tm_mday)
                hour = str(time.tm_hour) if time.tm_hour > 9 else '0' + str(time.tm_hour)
                min_ = str(time.tm_min) if time.tm_min > 9 else '0' + str(time.tm_min)
                sec = str(time.tm_sec) if time.tm_sec > 9 else '0' + str(time.tm_sec)
                name = f'{year}_{mon}_{day}_{hour}_{min_}_{sec}'
                data = bytes(self.trg[4]) + bytes(self.trg[2])
                create_dirs(PATH_SAVES)
                with open(f'{PATH_SAVES}/p_{name}.lifep', 'wb') as f:
                    f.write(data)
                return True
        return False

    def draw(self, sc, w_s):
        sc.blit(menu_item, (self.x, self.y))
        font.draw_text_l(sc, f'pos: {self.trg_x - w_s[0]}x{self.trg_y - w_s[1]}', (10 + self.x, 5 + self.y))
        pg.draw.circle(sc, self.trg[4], (20 + self.x, 30 + self.y), 10)
        font.draw_text_l(sc, str(self.trg[4][0]), (35 + self.x, 22 + self.y))
        font.draw_text_l(sc, str(self.trg[4][1]), (65 + self.x, 22 + self.y))
        font.draw_text_l(sc, str(self.trg[4][2]), (95 + self.x, 22 + self.y))
        font.draw_text_l(sc, f'mutate: {self.trg[6]}', (10 + self.x, 42 + self.y))
        page_item = self.p_i * 14
        font.draw_text_l(sc, f'{self.p_i + 1}/{L_I}', (55 + self.x, 280 + self.y))
        y = 0
        for ind, item in enumerate(self.trg[1]):
            if y - 13 <= page_item <= y:
                font.draw_text_l(sc, f'{ITEM_N[ind]}: {item}', (10 + self.x, 65 + y % 14 * 15 + self.y))
            y += 1
        if self.show_gen:
            sc.blit(menu_gen, (self.x + 130, self.y))
            x = 0
            y = 0
            for num in self.trg[2][self.p_g * 414: self.p_g * 414 + 414]:
                if x == 23:
                    x = 0
                    y += 1
                if y == 19:
                    break
                txt = f"{'0123456789ABCDEF'[num // 16]}{'0123456789ABCDEF'[num % 16]}"
                pos = (135 + x * 20 + self.x, 5 + y * 15 + self.y)
                if self.trg[5] == self.p_g * 414 + x + y * 23:
                    pg.draw.rect(sc, (64, 64, 255), (pos, (16, 16)))
                    font.draw_text_d(sc, txt, pos)
                else:
                    font.draw_text_l(sc, txt, pos)
                x += 1
            font.draw_text_l(sc, f'{self.trg[5]}/{self.trg[3] - 1}', (135 + self.x, 280 + self.y))
            font.draw_text_l(sc, f'{self.p_g + 1}/{round(self.trg[3] / 414 + 0.5)}', (360 + self.x, 280 + self.y))


class MenuCorpse:
    x = 0
    y = 0
    p_i = 0

    def __init__(self, target, pos):
        self.target = target
        self.trg_x, self.trg_y = pos

    def motion(self, rel, w, h):
        self.x += rel[0]
        self.y += rel[1]
        if self.x < 0:
            self.x = 0
        elif self.x > w - 130:
            self.x = w - 130
        if self.y < 0:
            self.y = 0
        elif self.y > h - 300:
            self.y = h - 300

    def collide(self, pos):
        if self.x <= pos[0] <= self.x + 130 and self.y <= pos[1] <= self.y + 300:
            return True
        return False

    def click(self, pos):
        if self.x + 20 <= pos[0] <= self.x + 35 and self.y + 280 <= pos[1] <= self.y + 295:
            self.p_i -= 1
        elif self.x + 90 <= pos[0] <= self.x + 105 and self.y + 280 <= pos[1] <= self.y + 295:
            self.p_i += 1
        if self.p_i < 0:
            self.p_i = 0
        elif self.p_i >= L_I:
            self.p_i = L_I - 1
        return False

    def draw(self, sc, w_s):
        sc.blit(menu_corpse, (self.x, self.y))
        font.draw_text_l(sc, f'pos: {self.trg_x - w_s[0]}x{self.trg_y - w_s[1]}', (10 + self.x, 10 + self.y))
        page_item = self.p_i * 14
        font.draw_text_l(sc, f'{self.p_i + 1}/{L_I}', (55 + self.x, 280 + self.y))
        y = 0
        for ind, item in enumerate(self.target[1]):
            if y - 13 <= page_item <= y:
                font.draw_text_l(sc, f'{ITEM_N[ind]}: {item}', (10 + self.x, 65 + y % 14 * 15 + self.y))
            y += 1


class HelpMenu:
    x = 0
    y = 0
    show = False
    page = 0

    def __init__(self, sound):
        self.sound = sound

    def motion(self, rel, w, h):
        self.x += rel[0]
        self.y += rel[1]
        if self.x < 0:
            self.x = 0
        elif self.x > w - 530:
            self.x = w - 530
        if self.y < 0:
            self.y = 0
        elif self.y > h - 380:
            self.y = h - 380
        return False

    def collide(self, pos):
        if self.show:
            if 0 <= pos[0] - self.x <= 530 and 0 <= pos[1] - self.y <= 380:
                return True
        return False

    def click(self, pos):
        if self.show:
            if 5 <= pos[0] - self.x <= 20 and 360 <= pos[1] - self.y <= 375:
                if self.page > 0:
                    self.sound.play('list')
                    self.page -= 1
            elif 510 <= pos[0] - self.x <= 525 and 360 <= pos[1] - self.y <= 375:
                if self.page < tt_len:
                    self.sound.play('list')
                    self.page += 1
            return False

    def draw(self, sc):
        if self.show:
            sc.blit(help_menu[self.page], (self.x, self.y))
            pos = (265 - len(f'{self.page}+{tt_len}') * 8 // 2 + self.x, 360 + self.y)
            font.draw_text_l(sc, f'{self.page + 1}/{tt_len + 1}', pos)


class SettingsMenu:
    x = 0
    y = 0
    clock = 0
    change = 0
    show = False

    def __init__(self, w_s):
        self.size = [str(w_s[0]), str(w_s[1])]

    def draw(self, sc):
        if self.show:
            sc.blit(settings_menu, (self.x, self.y))
            if self.clock > 60:
                if self.change == 1:
                    pg.draw.rect(sc, (0, 0, 0), (len(self.size[0] * 8) + 10 + self.x, 10 + self.y, 2, 15))
                elif self.change == 2:
                    pg.draw.rect(sc, (0, 0, 0), (len(self.size[1] * 8) + 90 + self.x, 10 + self.y, 2, 15))
            font.draw_text_l(sc, str(self.size[0]), (10 + self.x, 10 + self.y))
            font.draw_text_l(sc, str(self.size[1]), (90 + self.x, 10 + self.y))

    def key_press(self, key):
        if self.show and self.change:
            if 48 <= key.key <= 57:
                if self.size[self.change - 1][0] == '0':
                    self.size[self.change - 1] = ''
                self.size[self.change - 1] += key.unicode
            if key.key == 8:
                if self.size[self.change - 1]:
                    self.size[self.change - 1] = self.size[self.change - 1][:-1]
                    if self.size[self.change - 1] == '':
                        self.size[self.change - 1] = '0'

    def motion(self, rel, w, h):
        self.x += rel[0]
        self.y += rel[1]
        if self.x < 0:
            self.x = 0
        elif self.x > w - 175:
            self.x = w - 175
        if self.y < 0:
            self.y = 0
        elif self.y > h - 40:
            self.y = h - 40
        return False

    def collide(self, pos):
        if self.show:
            if 0 <= pos[0] - self.x <= 175 and 0 <= pos[1] - self.y <= 40:
                return True
        return False

    def click(self, pos):
        if self.show:
            if 10 <= pos[0] - self.x <= 80 and 10 <= pos[1] - self.y <= 25:
                self.change = 1
            elif 90 <= pos[0] - self.x <= 160 and 10 <= pos[1] - self.y <= 25:
                self.change = 2
            else:
                self.change = 0
        return False

    def update(self):
        if self.show:
            if self.clock == 120:
                self.clock = 0
            else:
                self.clock += 1


class MenuCopy:
    x = 0
    y = 0
    show = False
    page = 0

    def __init__(self, sound):
        self.sound = sound

    def collide(self, pos):
        if self.show and 0 <= pos[0] - self.x <= 600 and 0 <= pos[1] - self.y <= 300:
            return True
        return False

    def motion(self, rel, w, h):
        self.x += rel[0]
        self.y += rel[1]
        if self.x < 0:
            self.x = 0
        elif self.x > w - 600:
            self.x = w - 600
        if self.y < 0:
            self.y = 0
        elif self.y > h - 300:
            self.y = h - 300
        return False

    def click(self, pos):
        if self.show:
            animal = []
            plant = []
            create_dirs(PATH_SAVES)
            for i_ in listdir(PATH_SAVES):
                if len(i) > 5:
                    if i_[-6] == '.lifea':
                        animal.append(i_)
                    elif i_[-6] == '.lifep':
                        plant.append(i_)
            saves = animal[::-1] + plant[::-1]
            if 515 <= pos[0] - self.x <= 530 and 270 <= pos[1] - self.y <= 285:
                if self.page > 0:
                    self.sound.play('list')
                    self.page -= 1
            elif 580 <= pos[0] - self.x <= 595 and 270 <= pos[1] - self.y <= 285:
                if self.page < int(len(saves) / 42):
                    self.sound.play('list')
                    self.page += 1

            for c_ in range(42):
                a = c_ % 42 // 14 * 220
                b = c_ % 42 % 14 * 20
                if 10 + a <= pos[0] - self.x <= 220 + a and 10 + b <= pos[1] - self.y <= 28 + b:
                    try:
                        return saves[c_ + self.page * 42]
                    except IndexError:
                        pass

    def draw(self, sc):
        if self.show:
            sc.blit(menu_copy, (self.x, self.y))
            animal = []
            plant = []
            create_dirs(PATH_SAVES)
            for i_ in listdir(PATH_SAVES):
                if len(i) > 5:
                    if i_[-6] == '.lifea':
                        animal.append(i_)
                    elif i_[-6] == '.lifep':
                        plant.append(i_)
            saves = animal[::-1] + plant[::-1]
            font.draw_text_l(sc, f'{self.page + 1}/{round(len(saves) / 28 + 1)}', (540 + self.x, 270 + self.y))
            rect = pg.Surface(size=(210, 18))
            rect.fill((255, 255, 255))
            for i_ in range(42):
                try:
                    if saves[i_ + self.page * 42]:
                        sc.blit(rect, (10 + i_ % 42 // 14 * 220 + self.x, 10 + i_ % 42 % 14 * 20 + self.y))
                        a = i_ % 42
                        font.draw_text_l(sc, saves[i_ + self.page * 42], (10 + a // 14 * 220 + self.x,
                                                                          10 + a % 14 * 20 + self.y))
                except IndexError:
                    break


class MenuLoadWorld:
    x = 0
    y = 0
    show = False
    page = 0

    def __init__(self, sound):
        self.sound = sound

    def motion(self, rel, w, h):
        self.x += rel[0]
        self.y += rel[1]
        if self.x < 0:
            self.x = 0
        elif self.x > w - 600:
            self.x = w - 600
        if self.y < 0:
            self.y = 0
        elif self.y > h - 300:
            self.y = h - 300
        return False

    def collide(self, pos):
        if self.show:
            if 0 <= pos[0] - self.x <= 600 and 0 <= pos[1] - self.y <= 300:
                return True
        return False

    def click(self, pos):
        if self.show:
            create_dirs(PATH_WORLDS)
            worlds = [i for i in listdir(PATH_WORLDS) if len(i) > 5 and i[-6:] == '.lifew']
            if 515 <= pos[0] - self.x <= 530 and 270 <= pos[1] - self.y <= 285:
                if self.page > 0:
                    self.sound.play('list')
                    self.page -= 1
            elif 580 <= pos[0] - self.x <= 595 and 270 <= pos[1] - self.y <= 285:
                if self.page < round(len(worlds) / 28):
                    self.sound.play('list')
                    self.page += 1

            x = (pos[0] - self.x - 10) // 220
            y = (pos[1] - self.y - 10) // 20
            if 0 <= pos[0] - 10 - x * 220 - self.x <= 210 and 0 <= pos[1] - 10 - y * 20 - self.y <= 28:
                if x * 14 + y + self.page * 28 < len(worlds):
                    return worlds[x * 14 + y + self.page * 28]

    def draw(self, sc):
        if self.show:
            sc.blit(menu_copy, (self.x, self.y))
            create_dirs(PATH_WORLDS)
            worlds = [i for i in listdir(PATH_WORLDS) if len(i) > 5 and i[-6:] == '.lifew']
            font.draw_text_l(sc, f'{self.page + 1}/{round(len(worlds) / 28 - 0.5) + 1}', (540 + self.x, 270 + self.y))
            rect = pg.Surface(size=(210, 18))
            rect.fill((255, 255, 255))
            for i_ in range(42):
                try:
                    if worlds[i_ + self.page * 28]:
                        pos = (10 + i_ % 28 // 14 * 220 + self.x, 10 + i_ % 28 % 14 * 20 + self.y)
                        sc.blit(rect, pos)
                        font.draw_text_l(sc, worlds[i_ + self.page * 28], (pos[0] + 1, pos[1] + 1))
                except IndexError:
                    break


class MenuSimulation:
    x = 0
    y = 0
    show = False

    def __init__(self, sc: pg.Surface, statistic: list):
        self.sc = sc
        self.statistic = statistic

    def click(self, pos):
        pass

    def motion(self, rel, w, h):
        if self.show:
            self.x += rel[0]
            self.y += rel[1]
            if self.x < 0:
                self.x = 0
            elif self.x > w - 260:
                self.x = w - 260
            if self.y < 0:
                self.y = 0
            elif self.y > h - 225:
                self.y = h - 225

    def collide(self, pos):
        if self.show and self.x <= pos[0] <= self.x + 260 and self.y <= pos[1] <= self.y + 225:
            return True
        return False

    def draw(self, name_copy, world, speed, x, y, view):
        if self.show:
            if self.statistic:
                count = self.statistic[-1]
                count_of_animal = count[0]
                count_of_plant = count[1]
                count_of_corpse = count[2]
                count_of_block = count[3]
                count_of_water = count[4]
            else:
                count_of_animal = '?'
                count_of_plant = '?'
                count_of_corpse = '?'
                count_of_block = '?'
                count_of_water = '?'
            self.sc.blit(menu_simulation, (self.x, self.y))
            names = ('all', 'animal', 'plant', 'corpse', 'block', 'mutate', 'e', 'A', 'B', 'C', 'D', 'Health', 'Plant',
                     'Water', 'Salt', 'Acid', 'Fat', 'Potion'
                     )
            file_name = '' if name_copy is None else f'{name_copy}'
            speed = 'x' + str(speed) if speed > 0 else 'pause' if speed == 0 else '+inf'
            for i, txt in enumerate((
                    f'pos mouse: {x} {y}', f'speed: {speed}', f'sun: {world[1]}', f'mutate: {world[3]}',
                    f'count of animals: {count_of_animal}', f'count of plants: {count_of_plant}',
                    f'count of corpse: {count_of_corpse}', f'count of blocks: {count_of_block}',
                    f'count of water: {count_of_water}', f'file: {file_name}', f'view: {names[view]}'
            )
            ):
                if txt:
                    font.draw_text_l(self.sc, txt, (5 + self.x, 5 + i * 20 + self.y))


class MenuGraphic:
    x = 0
    y = 0
    w = 600
    h = 400
    draw_obj = [True, True, True, True, True]
    show = False
    resize = 0

    def __init__(self, sc, statistic):
        self.sc = sc
        self.sc2 = pg.Surface((self.w - 10, self.h - 10))
        self.statistic = statistic

    def click(self, pos):
        x = pos[0] - self.x - self.w + 23
        y = pos[1] - self.y
        if 0 <= x <= 12:
            if 0 <= y - 14 <= 12:
                self.draw_obj[0] = not self.draw_obj[0]
            elif 0 <= y - 44 <= 12:
                self.draw_obj[1] = not self.draw_obj[1]
            elif 0 <= y - 74 <= 12:
                self.draw_obj[2] = not self.draw_obj[2]
            elif 0 <= y - 104 <= 12:
                self.draw_obj[3] = not self.draw_obj[3]
            elif 0 <= y - 139 <= 12:
                self.draw_obj[4] = not self.draw_obj[4]
        return False

    def motion(self, rel, w, h):
        if self.show:
            self.x += rel[0]
            self.y += rel[1]
            if self.x < 0:
                self.x = 0
            elif self.x > w - self.w:
                self.x = w - self.w
            if self.y < 0:
                self.y = 0
            elif self.y > h - self.h:
                self.y = h - self.h

    def resized(self, rel, w, h):
        x, y = rel
        if self.resize == 1:
            self.x += x
            self.w -= x
        elif self.resize == 2:
            self.y += y
            self.h -= y
        elif self.resize == 3:
            self.w += x
        elif self.resize == 4:
            self.h += y
        elif self.resize == 5:
            self.x += x
            self.y += y
            self.w -= x
            self.h -= y
        elif self.resize == 6:
            self.y += y
            self.w += x
            self.h -= y
        elif self.resize == 7:
            self.w += x
            self.h += y
        elif self.resize == 8:
            self.x += x
            self.w -= x
            self.h += y
        if self.w < 150:
            self.w = 150
        elif self.w > w:
            self.w = w
        if self.h < 200:
            self.h = 200
        elif self.h > h:
            self.h = h
        self.sc2 = pg.Surface((self.w - 10, self.h - 10))

    def collide_side(self, pos):
        self.resize = 0
        if self.show:
            if -3 <= pos[0] - self.x <= 3 and self.y + 3 <= pos[1] <= self.y + self.h - 3:
                self.resize = 1
                return True
            elif 3 <= pos[0] - self.x <= self.w - 3 and -3 <= pos[1] - self.y <= 3:
                self.resize = 2
                return True
            elif -3 <= pos[0] - self.x - self.w <= 3 and 3 <= pos[1] - self.y <= self.h - 3:
                self.resize = 3
                return True
            elif 3 <= pos[0] - self.x <= self.w - 3 and -3 <= pos[1] - self.y - self.h <= 3:
                self.resize = 4
                return True
            elif -3 <= pos[0] - self.x <= 3 and -3 <= pos[1] - self.y <= 3:
                self.resize = 5
                return True
            elif -3 <= pos[0] - self.x - self.w <= 3 and -3 <= pos[1] - self.y <= 3:
                self.resize = 6
                return True
            elif -3 <= pos[0] - self.x - self.w <= 3 and -3 <= pos[1] - self.y <= self.h + 3:
                self.resize = 7
                return True
            elif -3 <= pos[0] - self.x <= self.w + 3 and -3 <= pos[1] - self.y - self.h <= 3:
                self.resize = 8
                return True
        return False

    def collide(self, pos):
        if self.show and self.x <= pos[0] <= self.x + self.w and self.y <= pos[1] <= self.y + self.h:
            return True
        return False

    def draw(self, pos, w_s2):
        if self.show:
            pg.draw.rect(self.sc2, (255, 255, 255), (0, 0, self.w, self.h))
            pg.draw.rect(self.sc, (0, 128, 76), (self.x, self.y, self.w, self.h), 5)
            pg.draw.rect(self.sc, (0, 0, 0), (self.x, self.y, self.w, self.h), 2)
            self.sc2.blit(IMAGE_ANIMAL, (self.w - 55, 5))
            self.sc2.blit(IMAGE_PLANT, (self.w - 55, 35))
            self.sc2.blit(IMAGE_CORPSE, (self.w - 55, 65))
            self.sc2.blit(IMAGE_BLOCK, (self.w - 55, 95))
            self.sc2.blit(IMAGE_WATER, (self.w - 55, 125))
            pg.draw.rect(self.sc2, (0, 0, 0), (self.w - 30, 7, 16, 16), 2)
            pg.draw.rect(self.sc2, (0, 0, 0), (self.w - 30, 37, 16, 16), 2)
            pg.draw.rect(self.sc2, (0, 0, 0), (self.w - 30, 67, 16, 16), 2)
            pg.draw.rect(self.sc2, (0, 0, 0), (self.w - 30, 97, 16, 16), 2)
            pg.draw.rect(self.sc2, (0, 0, 0), (self.w - 30, 132, 16, 16), 2)
            pg.draw.rect(self.sc2, (34, 177, 76) if self.draw_obj[0] else (237, 28, 36), (self.w - 28, 9, 12, 12))
            pg.draw.rect(self.sc2, (34, 177, 76) if self.draw_obj[1] else (237, 28, 36), (self.w - 28, 39, 12, 12))
            pg.draw.rect(self.sc2, (34, 177, 76) if self.draw_obj[2] else (237, 28, 36), (self.w - 28, 69, 12, 12))
            pg.draw.rect(self.sc2, (34, 177, 76) if self.draw_obj[3] else (237, 28, 36), (self.w - 28, 99, 12, 12))
            pg.draw.rect(self.sc2, (34, 177, 76) if self.draw_obj[4] else (237, 28, 36), (self.w - 28, 134, 12, 12))
            if len(self.statistic) > 1:
                stat = self.statistic[60 - self.w:]
                max_ = 1
                min_ = w_s2[0] * w_s2[1]
                for i in stat:
                    for i_ in range(5):
                        if self.draw_obj[i_] and i[i_] > max_:
                            max_ = i[i_]
                        elif self.draw_obj[i_] and i[i_] < min_:
                            min_ = i[i_]
                if max_ == min_:
                    max_ += 1
                for ind, i in enumerate(stat[:-1]):
                    x = ind
                    x2 = ind + 1
                    for j in range(5):
                        y = self.h - 11 - (i[j] - min_) * (self.h - 10) // (max_ - min_)
                        y2 = self.h - 11 - (stat[ind + 1][j] - min_) * (self.h - 10) // (max_ - min_)
                        col_ = ((255, 0, 0), (0, 255, 0), (127, 127, 127), (20, 20, 20), (0, 255, 255))[j]
                        pg.draw.line(self.sc2, col_, (x, y), (x2, y2), 2)
                self.sc.blit(self.sc2, (5 + self.x, 5 + self.y))

                if 5 <= pos[0] - self.x <= self.w - 5 and 5 <= pos[1] - self.y <= self.h - 5:
                    ind = pos[0] - 5 - self.x
                    if len(stat) > ind:
                        i = stat[ind]
                        ls = [0, 0, 0, 0, 0]
                        ls2 = [0, 0, 0, 0, 0]
                        for j in range(5):
                            y = self.h - 6 - (i[j] - min_) * (self.h - 10) // (max_ - min_)
                            ls[j] = pos[1] - y - self.y
                            if 5 < y < self.h - 5:
                                ls2[j] = abs(pos[1] - y - self.y)
                            else:
                                ls2[j] = 99999999999
                        j2 = ls2.index(min(ls2))
                        y3 = ls[j2]
                        x_ = pos[0] - 10
                        y_ = -ls[j2] + pos[1] - 20
                        pg.draw.circle(self.sc, (127, 0, 0), (pos[0], pos[1] - y3), 3)
                        if j2 == 0:
                            pg.draw.rect(self.sc, (255, 0, 0), (x_, y_ - 10, 20, 20))
                        elif j2 == 1:
                            pg.draw.circle(self.sc, (0, 255, 0), (pos[0], y_), 10)
                        elif j2 == 2:
                            pg.draw.polygon(self.sc, (127, 127, 127), ((x_ + 10, y_ - 10), (x_, y_),
                                                                       (x_ + 10, y_ + 10), (x_ + 20, y_)))
                        elif j2 == 3:
                            pg.draw.rect(self.sc, (20, 20, 20), (x_, y_ - 10, 20, 20))
                        else:
                            sc = pg.Surface((20, 10), pg.SRCALPHA)
                            pg.draw.circle(sc, (0, 255, 255), (10, 0), 10)
                            self.sc.blit(sc, (x_, y_ - 10))
                            pg.draw.polygon(self.sc, (0, 255, 255), ((x_, y_ - 10), (x_ + 10, y_ - 30),
                                                                     (x_ + 20, y_ - 10)))
                        txt = str(i[j2])
                        font.draw_text_l(self.sc, txt, (pos[0] + 5, y_ + 10))
                font.draw_text_l(self.sc, f'{max_}', (self.x + 7, self.y + 5))
                font.draw_text_l(self.sc, f'{min_}', (self.x + 7, self.y + self.h - 20))
            else:
                self.sc.blit(self.sc2, (5 + self.x, 5 + self.y))


class MenuTime:
    x = 0
    y = 0
    show = False
    change = 0

    def __init__(self, sc: pg.Surface):
        self.sc = sc

    def click(self, pos, world):
        x = pos[0] - self.x
        y = pos[1] - self.y
        if 0 < x - 2 <= 256 and 0 <= y - 45 <= 18:
            self.change = 1
            world[5] = (x - 35) * 4000 // 256 + 500
            sun = int((sin(world[5] / 640) * 20 + sin(world[5] / 40) * 20 + 20)) // 2  # [0, 29]
            world[1] = sun if sun > 0 else 0
        elif 0 <= x - 5 <= 250 and 0 <= y - 75 <= 6:
            self.change = 2
            time = (world[5] + 62) // 251 * 251 + (x - 5) * 251 // 250 - 63
            if time < 0:
                time += 4000
                if world[6] > 0:
                    world[6] -= 1
            elif time > 3999:
                time %= 4000
                world[6] += 1
            world[5] = time
            sun = int((sin(world[5] / 640) * 20 + sin(world[5] / 40) * 20 + 20)) // 2  # [0, 29]
            world[1] = sun if sun > 0 else 0
        else:
            self.change = 0
        return False

    def motion(self, pos, rel, w, h, world):
        x = pos[0] - self.x
        if self.show:
            if self.change == 0:
                self.x += rel[0]
                self.y += rel[1]
                if self.x < 0:
                    self.x = 0
                elif self.x > w - 260:
                    self.x = w - 260
                if self.y < 0:
                    self.y = 0
                elif self.y > h - 90:
                    self.y = h - 90
            elif self.change == 1:
                if 0 < x - 2 <= 256:
                    world[5] = (x - 35) * 4000 // 256 + 500
                    sun = int((sin(world[5] / 640) * 20 + sin(world[5] / 40) * 20 + 20)) // 2  # [0, 29]
                    world[1] = sun if sun > 0 else 0
            elif self.change == 2:
                time = (world[5] + 62) // 251 * 251 + (x - 5) * 251 // 250 - 63
                if time < 0:
                    time += 4000
                    if world[6] > 0:
                        world[6] -= 1
                elif time > 3999:
                    time %= 4000
                    world[6] += 1
                world[5] = time
                sun = int((sin(world[5] / 640) * 20 + sin(world[5] / 40) * 20 + 20)) // 2  # [0, 29]
                world[1] = sun if sun > 0 else 0

    def collide(self, pos):
        if self.show and self.x <= pos[0] <= self.x + 260 and self.y <= pos[1] <= self.y + 185:
            return True
        return False

    def draw(self, world):
        if self.show:
            self.sc.blit(menu_time, (self.x, self.y))
            time = world[5]
            if time < 500:
                mon = 'spring'
                proc = time + 500
            elif time < 1500:
                mon = 'summer'
                proc = time - 500
            elif time < 2500:
                mon = 'autumn'
                proc = time - 1500
            elif time < 3500:
                mon = 'winter'
                proc = time - 2500
            else:
                mon = 'spring'
                proc = time - 3500
            pg.draw.rect(self.sc, (237, 28, 36), (time * 256 // 4000 + 2 + self.x, 45 + self.y, 1, 18))
            pg.draw.rect(self.sc, (237, 28, 36), ((time + 62) % 251 + 5 + self.x, 75 + self.y, 1, 6))
            for i, txt in enumerate((
                    f'year: {world[6]}', f'time: {mon} {proc // 10} ({time})')
            ):
                if txt:
                    font.draw_text_l(self.sc, txt, (5 + self.x, 5 + i * 20 + self.y))


class Code:
    def __init__(self, app):
        self.app = app

    def create_animal(self, pos=(0, 0), gen=None, gen_len=16, item=None, color=None):
        gen = [randint(0, 255) for i in range(gen_len)] if gen is None else gen
        gen_len = gen_len if gen is None else len(gen)
        item = ITEM_L_ANIMAL.copy() if item is None else item
        color = [randint(0, 255), randint(0, 255), randint(0, 255)] if color is None else color
        marker = {
            1: (0, 0),
            2: (self.app.w_s2[0] - 1, 0),
            3: (self.app.w_s2[0] - 1, self.app.w_s2[1] - 1),
            4: (0, self.app.w_s2[1] - 1)
        }
        self.app.world[0][pos[1]][pos[0]] = [0, item, gen, gen_len, color, 0, 0, marker, [], 0, pos[0], pos[1]]

    def create_plant(self, pos=(0, 0), gen=None, gen_len=16, item=None, color=None):
        gen = [randint(0, 40) for i in range(gen_len)] if gen is None else gen
        gen_len = gen_len if gen is None else len(gen)
        item = ITEM_L_PLANT.copy() if item is None else item
        color = [randint(0, 255), randint(0, 255), randint(0, 255)] if color is None else color
        self.app.world[0][pos[1]][pos[0]] = [1, item, gen, gen_len, color, 0, 0]

    def create_corpse(self, pos=(0, 0), item=None):
        self.app.world[0][pos[1]][pos[0]] = [2, ITEM_L_CORPSE.copy() if item is None else item]

    def create_block(self, pos=(0, 0), hp=10):
        self.app.world[0][pos[1]][pos[0]] = [3, hp]

    def create_water(self, pos=(0, 0), count=10):
        self.app.world[0][pos[1]][pos[0]] = [4, count]

    def add_point_water(self, pos=(0, 0)):
        self.app.world[4].append((pos[0], pos[1]))

    def get_points_water(self):
        return self.app.world[4]

    def del_points_water(self):
        self.app.world[4] = []

    def set_day_cycle(self, f=True):
        self.app.world[2] = not not f

    def get_day_cycle(self):
        return self.app.world[2]

    def set_time(self, num=0):
        self.app.world[5] = num

    def get_time(self):
        return self.app.world[5]

    def set_year(self, num=0):
        self.app.world[6] = int(num)

    def get_year(self):
        return self.app.world[6]

    def get_count(self, index=-1):
        if self.app.statistic:
            return self.app.statistic[index]
        else:
            return []

    def get_count_animal(self, index=-1):
        if self.app.statistic:
            return self.app.statistic[index][0]
        else:
            return None

    def get_count_plant(self, index=-1):
        if self.app.statistic:
            return self.app.statistic[index][1]
        else:
            return None

    def get_count_corpse(self, index=-1):
        if self.app.statistic:
            return self.app.statistic[index][2]
        else:
            return None

    def get_count_block(self, index=-1):
        if self.app.statistic:
            return self.app.statistic[index][3]
        else:
            return None

    def get_count_water(self, index=-1):
        if self.app.statistic:
            return self.app.statistic[index][4]
        else:
            return None

    def get_mutate(self):
        return self.app.world[3]

    def set_mutate(self, num=0):
        self.app.world[3] = num

    def set_cell(self, pos, cell):
        self.app.world[0][pos[1]][pos[0]] = cell

    def get_cell(self, pos):
        return self.app.world[0][pos[1]][pos[0]]

    def save_world(self, name, overwrite=False):
        create_dirs(PATH_WORLDS)
        if overwrite or name not in listdir(PATH_WORLDS):
            self.app.save_world(False, name)
            return True
        return False

    def load_world(self, name):
        create_dirs(PATH_WORLDS)
        if name in listdir(PATH_WORLDS):
            self.app.load_world(name)
            return True

        return False

    def get_statistic(self):
        return self.app.statistic

    def get_dx(self):
        return self.app.dx

    def set_dx(self, num=0):
        self.app.dx = num

    def get_dy(self):
        return self.app.dy

    def set_dy(self, num=0):
        self.app.dy = num

    def get_scale(self):
        return self.app.scale

    def set_scale(self, num=0):
        self.app.scale = num

    def get_speed(self):
        return self.app.speed

    def set_speed(self, num=0):
        self.app.speed = num

    def screenshot_png(self):
        num = 0
        create_dirs(PATH_SCREENSHOT_PNG)
        ls = listdir(PATH_SCREENSHOT_PNG)
        while True:
            if f'screenshot_{num}.png' not in ls:
                break
            else:
                num += 1
        pg.image.save(self.app.sc, f'{PATH_SCREENSHOT_PNG}/screenshot_{num}.png')

    def screenshot_world_png(self):
        screenshot_image = world.screenshot(self.app.world, SCREENSHOT_SIZE, self.app.w_s2, self.app.draw_hp_block,
                                            self.app.font_for_block, self.app.view)
        num = 0
        create_dirs(PATH_SCREENSHOT_PNG)
        ls = listdir(PATH_SCREENSHOT_PNG)
        while True:
            if f'worldshot_{num}.png' not in ls:
                break
            else:
                num += 1
        pg.image.save(screenshot_image, f'{PATH_SCREENSHOT_PNG}/worldshot_{num}.png')

    def screenshot_world_lifew(self):
        sx, bsx = int_to_bin(self.app.w_s[0])
        sy, bsy = int_to_bin(self.app.w_s[1])
        data = bytes([sx, sy]) + bsx + bsy
        for y in range(self.app.w_s2[1]):
            buffer_1 = b''
            line = self.app.world[0][y]
            for x in range(self.app.w_s2[0]):
                buffer_2 = b''
                obj = line[x]
                if obj is None:
                    buffer_2 += b'\x00'
                else:
                    if obj[0] == 0:  # animal
                        buffer_2 += b'\x01' + bytes(obj[4] + [obj[6]])
                    elif obj[0] == 1:  # plant
                        buffer_2 += b'\x02' + bytes(obj[4])
                    elif obj[0] == 2:  # corpse
                        buffer_2 += b'\x03'
                    elif obj[0] == 3:  # block
                        buffer_2 += b'\x04'
                    elif obj[0] == 4:  # water
                        buffer_2 += b'\x05'
                        size, bs = int_to_bin(obj[1])
                        buffer_2 += bytes([size]) + bs
                buffer_1 += buffer_2
            data += buffer_1
        num = 0
        create_dirs(PATH_SCREENSHOT_PNG)
        ls = listdir(PATH_SCREENSHOT_LIFEI)
        while True:
            if f'screenshot_lifei_{num}.lifei' not in ls:
                break
            else:
                num += 1
        with open(f'{PATH_SCREENSHOT_LIFEI}/screenshot_lifei_{num}.lifei', 'wb') as f:
            f.write(data)

    def start_record(self):
        if not self.app.recording:
            self.app.recording = True
            create_dirs(PATH_RECORDS)
            records = [i for i in listdir(PATH_RECORDS) if len(i) > 5 and i[-6:] == '.lifev']
            num = 0
            while True:
                if f'record_{num}.lifev' not in records:
                    break
                num += 1
            self.app.record_file = open(f'{PATH_RECORDS}/record_{num}.lifev', 'wb')
            self.app.record()

    def stop_record(self):
        if self.app.recording:
            self.app.record()
            self.app.record_file.close()
            self.app.recording = False

    def run_script(self, file):
        create_dirs(PATH_SCRIPTS)
        with open(f'{"" if ":" in file else PATH_SCRIPTS}{file}') as f:
            self.app.menu_script.run_code(f.read())

    def run_script_thread(self, file):
        create_dirs(PATH_SCRIPTS)
        with open(f'{"" if ":" in file else PATH_SCRIPTS}{file}') as f:
            script = f.read()
        thread = threading.Thread(target=self.app.menu_script.run_code, args=(script, ))
        self.app.menu_script.threads.append(thread)
        thread.start()

    def set_world_size(self, size):
        w, h = size
        if w != self.app.w_s[0] or h != self.app.w_s[1]:
            world_copy = self.app.world[0]
            min_w = min(w, self.app.w_s[0]) * 2
            min_h = min(h, self.app.w_s[1]) * 2
            self.app.w_s = (w, h)
            self.app.w_s2 = (self.app.w_s[0] * 2, self.app.w_s[1] * 2)
            self.app.world = world.create(self.app.w_s)
            for y in range(min_h):
                self.app.world[0][y][:min_w] = world_copy[y][:min_w]

    def get_world_size(self):
        return self.app.w_s[0], self.app.w_s[1]

    def print(self, string=''):
        self.app.menu_script.last_text = [str(string)] + self.app.menu_script.last_text

    def clear(self):
        self.app.menu_script.last_text = []

    def console_set_height(self, height=200):
        self.app.menu_script.height = height

    def console_get_height(self):
        return self.app.menu_script.height

    def set_view(self, num=0):
        self.app.view = num

    def get_view(self):
        return self.app.view

    def isalive(self):
        return self.app.run


class MenuScript:
    width = 100
    height = 200
    show = False
    clock = 0
    writing = False
    last_text = []
    history_commands = []
    change_history = -1
    text_input = ''
    font = pg.font.Font(PATH_FONT, 16)
    command_draw = True
    change = 0
    threads: list[threading.Thread] = []

    def __init__(self, app, sc: pg.Surface):
        self.code = Code(app)
        self.sc_main = sc
        self.sc = pg.Surface((sc.get_width(), self.height))
        self.sc.set_alpha(100)

    def click(self, pos):
        if -1 < pos[0] < self.width and -1 < pos[1] < self.height:
            self.writing = True
        return False

    def motion(self, rel, w, h):
        pass

    def run_code(self, code):
        if hasattr(__builtins__, '__import__'):
            del __builtins__.__import__
        try:
            exec(code, {
                'dir': dir,
                'eval': None,
                'exec': None,
                'exit': None,
                'filter': filter,
                'float': float,
                'format': format,
                'frozenset': frozenset,
                'getattr': getattr,
                'globals': globals,
                'hasattr': hasattr,
                'hash': hash,
                'hex': hex,
                'id': id,
                'int': int,
                'isinstance': isinstance,
                'issubclass': issubclass,
                'iter': iter,
                'len': len,
                'list': list,
                'locals': locals,
                'map': map,
                'max': max,
                'memoryview': memoryview,
                'min': min,
                'next': next,
                'object': object,
                'oct': oct,
                'open': open,
                'ord': ord,
                'pow': pow,
                'print': self.code.print,
                'property': property,
                'quit': None,
                'range': range,
                'repr': repr,
                'reversed': reversed,
                'round': round,
                'set': set,
                'setattr': setattr,
                'slice': slice,
                'sorted': sorted,
                'staticmethod': staticmethod,
                'str': str,
                'sum': sum,
                'super': super,
                'tuple': tuple,
                'type': type,
                'vars': vars,
                'zip': zip,
                'create_animal': self.code.create_animal,
                'create_plant': self.code.create_plant,
                'create_corpse': self.code.create_corpse,
                'create_block': self.code.create_block,
                'create_water': self.code.create_water,
                'add_point_water': self.code.add_point_water,
                'get_points_water': self.code.get_points_water,
                'del_points_water': self.code.del_points_water,
                'set_day_cycle': self.code.set_day_cycle,
                'get_day_cycle': self.code.get_day_cycle,
                'set_time': self.code.set_time,
                'get_time': self.code.get_time,
                'set_year': self.code.set_year,
                'get_year': self.code.get_year,
                'get_count': self.code.get_count,
                'get_count_animal': self.code.get_count_animal,
                'get_count_plant': self.code.get_count_plant,
                'get_count_corpse': self.code.get_count_corpse,
                'get_count_block': self.code.get_count_block,
                'get_count_water': self.code.get_count_water,
                'set_mutate': self.code.set_mutate,
                'get_mutate': self.code.get_mutate,
                'set_cell': self.code.set_cell,
                'get_cell': self.code.get_cell,
                'save_world': self.code.save_world,
                'load_world': self.code.load_world,
                'get_keypressed': pg.key.get_pressed,
                'get_mouse_pos': pg.mouse.get_pos,
                'get_statistic': self.code.get_statistic,
                'get_dx': self.code.get_dx,
                'set_dx': self.code.set_dx,
                'get_dy': self.code.get_dy,
                'set_dy': self.code.set_dy,
                'get_scale': self.code.get_scale,
                'set_scale': self.code.set_scale,
                'get_speed': self.code.get_speed,
                'set_speed': self.code.set_speed,
                'screenshot_png': self.code.screenshot_png,
                'screenshot_world_png': self.code.screenshot_world_png,
                'screenshot_world_lifew': self.code.screenshot_world_lifew,
                'start_record': self.code.start_record,
                'stop_record': self.code.stop_record,
                'run_script': self.code.run_script,
                'run_script_thread': self.code.run_script_thread,
                'set_world_size': self.code.set_world_size,
                'get_world_size': self.code.get_world_size,
                'clear': self.code.clear,
                'console_set_height': self.code.console_set_height,
                'console_get_height': self.code.console_get_height,
                'set_view': self.code.set_view,
                'get_view': self.code.get_view,
                'sleep': time_module.sleep,
                'isalive': self.code.isalive,
                'random': random,
                'randint': randint
            })
        except Exception as e:
            self.code.print(f'{e}')

    def key_press(self, key, keypressed):
        if not (keypressed[pg.KMOD_ALT] or keypressed[pg.KMOD_CTRL]):
            if key.key == pg.K_BACKSPACE:
                if self.change > 0:
                    self.text_input = self.text_input[:self.change - 1] + self.text_input[self.change:]
                    self.change -= 1
                    if self.change < 0:
                        self.change = 0
                    self.clock = FPS // 3
            elif key.key == pg.K_DELETE:
                self.text_input = self.text_input[:self.change] + self.text_input[self.change + 1:]
                self.clock = FPS // 3
            elif key.key == pg.K_RETURN:
                if self.command_draw:
                    self.last_text = [self.text_input] + self.last_text
                self.history_commands = [self.text_input] + self.history_commands
                self.run_code(self.text_input)
                self.change = 0
                self.text_input = ''
                self.clock = FPS // 3
            elif key.key == pg.K_LEFT:
                self.change -= 1
                if self.change < 0:
                    self.change = 0
                self.clock = FPS // 3
            elif key.key == pg.K_RIGHT:
                self.change += 1
                if self.change > len(self.text_input):
                    self.change = len(self.text_input) + 1
                self.clock = FPS // 3
            elif key.key == pg.K_UP:
                self.change_history += 1
                if self.change_history >= len(self.history_commands):
                    self.change_history = len(self.history_commands) - 1
                if self.change_history > -1:
                    self.text_input = self.history_commands[self.change_history][:]
                    self.change = len(self.text_input)
            elif key.key == pg.K_DOWN:
                self.change_history -= 1
                if self.change_history < -1:
                    self.change_history = -1
                if self.change_history > -1:
                    self.text_input = self.history_commands[self.change_history]
                    self.change = len(self.text_input)
                else:
                    self.text_input = ''
                    self.change = 0
            elif keypressed[pg.K_LCTRL]:
                if key.key == pg.K_c:
                    pyperclip.copy(self.text_input)
                elif key.key == pg.K_v:
                    self.text_input = self.text_input[:self.change] + pyperclip.paste() + self.text_input[self.change:]
                    self.change = len(self.text_input)
            elif key.unicode != '':
                if key.unicode == '\x1b':
                    self.writing = False
                elif key.unicode == '`':
                    self.show = False
                    self.writing = False
                elif key.unicode not in ('\t', '\r', '\n', '\a'):
                    self.text_input = self.text_input[:self.change] + key.unicode + self.text_input[self.change:]
                    self.change += 1
                    self.clock = FPS // 3
        else:
            pass

    def load_script(self, file):
        with open(file) as f:
            self.run_code(f.read())

    def update(self, w):
        key = pg.key.get_pressed()
        for thread in self.threads:
            if not thread.is_alive():
                self.threads.remove(thread)

        if key[pg.K_BACKSPACE] and self.clock > FPS // 2 and self.change > 0:
            self.text_input = self.text_input[:self.change - 1] + self.text_input[self.change:]
            self.change -= 1
            if self.change < 0:
                self.change = 0
            self.clock = FPS // 3
        if self.width != w or self.height != self.sc.get_height():
            self.width = w
            self.sc = pg.Surface((w, self.height))
            self.sc.set_alpha(100)
        if self.writing:
            if self.clock == FPS:
                self.clock = 0
            else:
                self.clock += 1

    def collide(self, pos):
        if self.show and -1 < pos[0] < self.width and -1 < pos[1] < self.height:
            return True
        return False

    def draw(self):
        pg.draw.rect(self.sc, (0, 0, 0), (0, 0, self.width, self.height))
        txt1 = self.font.render(self.text_input[:self.change], True, (255, 255, 255))
        txt2 = self.font.render(self.text_input[self.change:], True, (255, 255, 255))
        self.sc.blit(txt1, (10, self.height - 30))
        self.sc.blit(txt2, (10 + txt1.get_width(), self.height - 30))
        dy = 0
        for i in self.last_text:
            t = self.font.render(i, True, (255, 255, 255))
            self.sc.blit(t, (10, self.height - 48 - dy))
            dy += t.get_height()
        if self.writing and self.clock > FPS // 3:
            pg.draw.rect(self.sc, (255, 255, 255), (txt1.get_width() + 10, self.height - 30, 2, 16))
        if self.show:
            self.sc_main.blit(self.sc, (0, 0))

