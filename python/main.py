import pygame as pg
import world
from sys import argv
from menu import MenuCopy, MenuAnimal, MenuPlant, MenuCorpse, HelpMenu, SettingsMenu, MenuLoadWorld,\
    MenuSimulation, MenuGraphic, MenuTime, MenuScript
from tools import int_to_bin, bin_to_int, testing
from settings import font, IMAGE_MOUSE, IMAGE_MOUSE_RESIZE, ITEM_LEN, WIDTH, HEIGHT, FPS, VSYNC, SCREENSHOT_SIZE, \
    PATH_FONT, PATH_RECORDS, RECORD_TIME, PATH_SCREENSHOT_LIFEI, PATH_SCREENSHOT_PNG, PATH_SAVES, PATH_WORLDS,\
    create_dirs
from random import randint, choice
from math import sin
from os import listdir, mkdir
from time import localtime


class Sound:
    def __init__(self):
        if not pg.mixer.get_init():
            pg.mixer.init(channels=1)
        self.sounds = {i: [pg.mixer.Sound(f'audio/{i}/{ii}') for ii in listdir(f'audio/{i}')] for i in listdir('audio')}

    def play(self, category):
        if category in self.sounds and self.sounds[category]:
            choice(self.sounds[category]).play()


class App:
    def __init__(self):
        self.sound = Sound()
        self.w_s = (50, 50)
        self.w_s2 = (self.w_s[0] * 2, self.w_s[1] * 2)
        self.s_animal = False
        self.s_plant = False
        self.s_corpse = False
        self.W = WIDTH
        self.H = HEIGHT
        self.H_W, self.H_H = self.W // 2, self.H // 2
        self.sc = pg.display.set_mode((self.W, self.H), pg.DOUBLEBUF | pg.HWSURFACE | pg.RESIZABLE, vsync=VSYNC)
        self.scale = 10
        self.dx = self.H_W - self.scale // 2
        self.dy = self.H_H - self.scale // 2
        self.world = world.create(self.w_s)
        self.statistic = []
        self.menu_obj = []
        self.grab_menu = None
        self.clock = pg.time.Clock()
        self.ticks = 0
        self.menu_copy = MenuCopy(self.sound)
        self.menu_help = HelpMenu(self.sound)
        self.menu_simulation = MenuSimulation(self.sc, self.statistic)
        self.menu_graphic = MenuGraphic(self.sc, self.statistic)
        self.menu_time = MenuTime(self.sc)
        self.menu_script = MenuScript(self, self.sc)
        self.copy_obj = None
        self.saved = 0
        self.menu_load_world = MenuLoadWorld(self.sound)
        self.name_copy = None
        self.grid_drawing = True
        self.mouse_trace = [(0, 0) for j in range(5)]
        self.speed = 0
        self.run = True
        self.draw_hp_block = False
        self.font_for_block = pg.font.Font('C:/Windows/Fonts/freesansbold.ttf', round(self.scale / 2))
        self.menu_settings = SettingsMenu(self.w_s)
        self.view = 0
        self.info = False
        self.recording = False
        self.record_folder = None
        self.record_frame = 0
        self.record_time = 0
        self.name_label = 'Life'
        pg.mouse.set_visible(False)
        icon = pg.Surface((16, 16))
        icon.fill((255, 255, 255))
        n = randint(0, 4)
        if n == 0:
            pg.draw.circle(icon, (0, randint(200, 255), 0), (8, 8), 8)
        elif n == 1:
            icon.fill((randint(200, 255), 0, 0))
            pg.draw.rect(icon, (0, 0, 0), (7, 3, 2, 2))
        elif n == 2:
            pg.draw.polygon(icon, (127, 127, 127), ((7, 0), (8, 0), (15, 7), (15, 8), (8, 15), (7, 15), (0, 8), (0, 7)))
        elif n == 3:
            icon.fill((30, 30, 30))
        elif n == 4:
            icon.fill((0, 255, 255))
        d = {
            'Life': 490,
            'Simulation Life': 1,
            'made by dimga': 1,
            'live': 1,
            'Life = Death': 1,
            'unknown.lifew': 1,
            'They all will die': 1,
            'SashOK was here!': 1,
            'Love': 1,
            'Is anyone reading this?': 1,
            'Mutations': 1
        }
        num = randint(0, 500)
        for i in d:
            if num <= d[i]:
                self.name_label = i
                break
            else:
                num -= d[i]
        pg.display.set_icon(icon)
        pg.display.set_caption(self.name_label)

    def record(self):
        if self.recording:
            if self.record_time < RECORD_TIME:
                self.record_time += 1
            else:
                self.record_time = 0
                sx, bsx = int_to_bin(self.w_s[0])
                sy, bsy = int_to_bin(self.w_s[1])
                data = bytes([sx, sy]) + bsx + bsy
                for y in range(self.w_s2[1]):
                    buffer_1 = b''
                    for x in range(self.w_s2[0]):
                        buffer_2 = b''
                        obj = self.world[0][y][x]
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
                with open(f'{self.record_folder}/frame_{self.record_frame}', 'wb') as f:
                    f.write(data)
                self.record_frame += RECORD_TIME

    def screenshot_world(self):
        sx, bsx = int_to_bin(self.w_s[0])
        sy, bsy = int_to_bin(self.w_s[1])
        data = bytes([sx, sy]) + bsx + bsy

        for y in range(self.w_s2[1]):
            buffer_1 = b''
            for x in range(self.w_s2[0]):
                buffer_2 = b''
                obj = self.world[0][y][x]
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
        ls = listdir(PATH_SCREENSHOT_LIFEI)
        while True:
            if f'screenshot_lifei_{num}.lifei' not in ls:
                break
            else:
                num += 1
        with open(f'{PATH_SCREENSHOT_LIFEI}/screenshot_lifei_{num}.lifei', 'wb') as f:
            f.write(data)

    def close(self):
        run = True
        change = 0
        while run:
            self.sc.fill((239, 228, 176))
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if change == 0:
                            time = localtime()
                            year = time.tm_year
                            mon = str(time.tm_mon) if time.tm_mon > 9 else '0' + str(time.tm_mon)
                            day = str(time.tm_mday) if time.tm_mday > 9 else '0' + str(time.tm_mday)
                            hour = str(time.tm_hour) if time.tm_hour > 9 else '0' + str(time.tm_hour)
                            min_ = str(time.tm_min) if time.tm_min > 9 else '0' + str(time.tm_min)
                            sec = str(time.tm_sec) if time.tm_sec > 9 else '0' + str(time.tm_sec)
                            self.save_world(False, f'{year}_{mon}_{day}_{hour}_{min_}_{sec}')
                            self.run = False
                        elif change == 1:
                            self.run = False
                        elif change == 2:
                            pass
                        run = False
                    elif event.key == pg.K_UP:
                        if change > 0:
                            change -= 1
                    elif event.key == pg.K_DOWN:
                        if change < 2:
                            change += 1
                    elif event.key == pg.K_ESCAPE:
                        run = False
            font.draw_text_l(self.sc, 'save', (self.H_W - 16, self.H_H - 30))
            font.draw_text_l(self.sc, 'do not save', (self.H_W - 44, self.H_H - 10))
            font.draw_text_l(self.sc, 'cancel', (self.H_W - 24, self.H_H + 10))
            pg.draw.rect(self.sc, (0, 0, 0), (self.H_W - 50, self.H_H - 32 + 20 * change, 100, 20), 2)
            pg.display.flip()

    def draw_grid(self):
        if self.grid_drawing:
            s = self.scale // 20 if self.scale >= 20 else 1
            x_ = (self.dx + self.scale - s // 2) % self.scale
            y_ = (self.dy + self.scale - s // 2) % self.scale
            for y in range(0, (self.H // self.scale + 1) * self.scale, self.scale):
                pg.draw.rect(self.sc, (0, 85, 0), (0, y_ + y, self.W, s))
            for x in range(0, (self.W // self.scale + 1) * self.scale, self.scale):
                pg.draw.rect(self.sc, (0, 85, 0), (x_ + x, 0, s, self.H))

    def draw_mouse(self):
        if pg.mouse.get_focused():
            x, y = pg.mouse.get_pos()
            if pg.mouse.get_pressed(3)[2]:
                self.mouse_trace = [(x, y) for i in range(5)]
            else:
                self.mouse_trace.pop(0)
                self.mouse_trace.append((x, y))
                for i, p in enumerate(self.mouse_trace[:-1]):
                    pg.draw.line(self.sc, (239, 228, 176), p, (self.mouse_trace[i + 1]), round(i * 3 + 1.5) // 2)
            if self.menu_graphic.show:
                for i in (self.menu_simulation, self.menu_time):
                    if i.collide((x, y)):
                        self.sc.blit(IMAGE_MOUSE, (x - 5, y - 5))
                        break
                else:
                    if self.menu_graphic.collide_side((x, y)):
                        self.sc.blit(IMAGE_MOUSE_RESIZE, (x - 7, y - 7))
                    else:
                        self.sc.blit(IMAGE_MOUSE, (x - 5, y - 5))
            else:
                self.sc.blit(IMAGE_MOUSE, (x - 5, y - 5))

    def draw_border(self):
        x = self.w_s[0] * self.scale + self.dx
        x2 = -self.w_s[0] * self.scale + self.dx
        y = self.w_s[1] * self.scale + self.dy
        y2 = -self.w_s[1] * self.scale + self.dy
        if x <= self.W:
            pg.draw.rect(self.sc, (0, 150, 255), (x, 0, self.W - x, self.H))
        if y <= self.H:
            pg.draw.rect(self.sc, (0, 150, 255), (0, y, self.W, self.H - y))
        if x2 >= -self.W:
            pg.draw.rect(self.sc, (0, 150, 255), (-self.W, 0, self.W + x2, self.H))
        if y2 >= -self.H:
            pg.draw.rect(self.sc, (0, 150, 255), (0, -self.H, self.W, self.H + y2))

    def draw_saved(self):
        if self.saved > 0:
            x, y = pg.mouse.get_pos()
            font.draw_text_l(self.sc, 'save', (x - 15, y - 80 + self.saved))
            self.saved -= 1

    def event(self):
        key = pg.key.get_pressed()
        x, y = pg.mouse.get_pos()
        if not self.menu_script.writing:
            x = int((x - self.dx) // self.scale + self.w_s[0])
            y = int((y - self.dy) // self.scale + self.w_s[1])
            if -1 < x < self.w_s2[0] and -1 < y < self.w_s2[1]:
                if key[pg.K_o] and self.world[0][y][x] is not None:
                    self.world[0][y][x] = None
                if key[pg.K_a] and self.world[0][y][x] is None:
                    if self.name_copy is not None and len(self.name_copy) > 5 and self.name_copy[-6:] == '.lifea':
                        with open(f'{PATH_SAVES}/{self.name_copy}', 'rb') as f:
                            data = f.read()
                        color = [data[0], data[1], data[2]]
                        gen = [i for i in data[3:]]
                        world.add_animal(self.world, pos=(x, y), color=color, gen=gen, w_s=self.w_s)
                    else:
                        world.add_animal(self.world, pos=(x, y), w_s=self.w_s)
                if key[pg.K_p] and self.world[0][y][x] is None:
                    if self.name_copy is not None and len(self.name_copy) > 5 and self.name_copy[-6:] == '.lifep':
                        with open(f'{PATH_SAVES}/{self.name_copy}', 'rb') as f:
                            data = f.read()
                        color = [data[0], data[1], data[2]]
                        gen = [i for i in data[3:]]
                        world.add_plant(self.world, pos=(x, y), color=color, gen=gen)
                    else:
                        world.add_plant(self.world, pos=(x, y))
                if key[pg.K_c] and self.world[0][y][x] is None:
                    world.add_corpse(self.world, pos=(x, y))
                if key[pg.K_b] and self.world[0][y][x] is None:
                    world.add_block(self.world, pos=(x, y))
            if key[pg.K_DOWN]:
                if self.speed > 0:
                    self.speed -= 1
            if key[pg.K_UP]:
                self.speed += 1
            if key[61]:
                self.world[3] += 1
            if key[pg.K_MINUS]:
                if self.world[3] > 0:
                    self.world[3] -= 1
            self.s_animal = key[pg.K_x] and key[pg.K_1] and not key[pg.K_v] and self.menu_settings.change == 0
            self.s_plant = key[pg.K_x] and key[pg.K_2] and not key[pg.K_v] and self.menu_settings.change == 0
            self.s_corpse = key[pg.K_x] and key[pg.K_3] and not key[pg.K_v] and self.menu_settings.change == 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()
            elif event.type == pg.DROPFILE:
                if len(event.file) > 5 and event.file[-6:] == '.lifew':
                    self.load_world(event.file, True)
                elif len(event.file) > 6 and event.file[-7:] == '.script':
                    self.menu_script.load_script(event.file)
            elif event.type == pg.VIDEORESIZE:
                self.W, self.H = pg.display.get_window_size()
                self.H_W, self.H_H = self.W // 2, self.H // 2
                for i in (self.menu_simulation, self.menu_time, self.menu_graphic, self.menu_help,
                          self.menu_settings, self.menu_load_world, self.menu_copy, self.menu_script):
                    if i.__class__ == MenuTime:
                        i.motion((0, 0), (0, 0), self.W, self.H, self.world)
                    else:
                        i.motion((0, 0), self.W, self.H)
                for i in self.menu_obj:
                    i.motion((0, 0), self.W, self.H)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.grab_menu = None
                    self.menu_script.writing = False
                    for i in (self.menu_script, self.menu_simulation, self.menu_time, self.menu_graphic, self.menu_help,
                              self.menu_settings, self.menu_load_world, self.menu_copy):
                        if i.collide(event.pos):
                            self.grab_menu = i
                            if i.__class__ == MenuTime:
                                res = i.click(event.pos, self.world)
                            else:
                                res = i.click(event.pos)
                            if i == self.menu_copy:
                                self.name_copy = res
                            elif i == self.menu_load_world:
                                if res is not None:
                                    self.load_world(res)
                            break
                    else:
                        for i in self.menu_obj[::-1]:
                            if i.collide(event.pos):
                                self.grab_menu = i
                                self.menu_obj.append(i)
                                self.menu_obj.remove(i)
                                break
                        for i in self.menu_obj[::-1]:
                            if i.collide(event.pos):
                                if self.grab_menu == i:
                                    if self.grab_menu.click(event.pos):
                                        self.saved = 60
                                    break
                elif event.button == 2:
                    x = (event.pos[0] - self.dx) // self.scale + self.w_s[0]
                    y = (event.pos[1] - self.dy) // self.scale + self.w_s[1]
                    if 0 <= x < self.w_s2[0] and 0 <= y < self.w_s2[1]:
                        obj = self.world[0][y][x]
                        if obj is not None:
                            name = obj[0]
                            if name == 0:
                                self.menu_obj.append(MenuAnimal(obj))
                            elif name == 1:
                                self.menu_obj.append(MenuPlant(obj, (x, y)))
                            elif name == 2:
                                self.menu_obj.append(MenuCorpse(obj, (x, y)))
                elif event.button == 3:
                    self.name_copy = None
                    self.menu_graphic.collide_side(event.pos)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    self.menu_graphic.resize = 0
            elif event.type == pg.MOUSEMOTION:
                if event.buttons[0]:
                    if self.grab_menu is not None:
                        if self.grab_menu.__class__ == MenuTime:
                            self.grab_menu.motion(event.pos, event.rel, self.W, self.H, self.world)
                        else:
                            self.grab_menu.motion(event.rel, self.W, self.H)
                elif event.buttons[2]:
                    if self.menu_graphic.resize:
                        self.menu_graphic.resized(event.rel, self.W, self.H)
                        self.menu_graphic.motion((0, 0), self.W, self.H)
                    else:
                        self.dx += event.rel[0]
                        self.dy += event.rel[1]
            elif event.type == pg.MOUSEWHEEL:
                x, y = pg.mouse.get_pos()
                dx = (x - self.dx) / self.scale
                dy = (y - self.dy) / self.scale
                self.scale += event.y
                if self.scale < 1:
                    self.scale = 1
                elif self.scale > 100:
                    self.scale = 100
                self.dx = int(x - dx * self.scale)
                self.dy = int(y - dy * self.scale)
                self.font_for_block = pg.font.Font(PATH_FONT, round(self.scale / 2))
            elif event.type == pg.KEYDOWN:
                if self.menu_script.writing:
                    if self.menu_script.show:
                        self.menu_script.key_press(event, key)
                else:
                    if event.key == pg.K_ESCAPE:
                        if self.menu_obj:
                            self.menu_obj.pop(-1)
                        else:
                            self.close()
                    elif event.key == pg.K_f:
                        self.menu_graphic.show = not self.menu_graphic.show
                    elif event.key == pg.K_t:
                        self.menu_time.show = not self.menu_time.show
                    elif event.key == pg.K_F2:
                        num = 0
                        ls = listdir(PATH_SCREENSHOT_PNG)
                        while f'screenshot_{num}.png' in ls:
                            num += 1
                        create_dirs(PATH_SCREENSHOT_PNG)
                        pg.image.save(self.sc, f'{PATH_SCREENSHOT_PNG}/screenshot_{num}.png')
                    elif event.key == pg.K_F3:
                        screenshot_image = world.screenshot(self.world, SCREENSHOT_SIZE, self.w_s2, self.draw_hp_block,
                                                            self.font_for_block, self.view)
                        num = 0
                        ls = listdir(PATH_SCREENSHOT_PNG)
                        while f'worldshot_{num}.png' in ls:
                            num += 1
                        create_dirs(PATH_SCREENSHOT_PNG)
                        pg.image.save(screenshot_image, f'{PATH_SCREENSHOT_PNG}/worldshot_{num}.png')
                    elif event.key == pg.K_F4:
                        self.screenshot_world()
                    elif event.key == pg.K_F5:
                        if not self.recording:
                            self.recording = True
                            records = listdir(PATH_RECORDS)
                            num = 0
                            while f'record_{num}' in records:
                                num += 1

                            mkdir(f'{PATH_RECORDS}/record_{num}')
                            self.record_folder = f'{PATH_RECORDS}/record_{num}/'
                    elif event.key == pg.K_F6:
                        if self.recording:
                            self.recording = False
                            self.record_folder = None
                            self.record_frame = 0
                            self.record_time = 0
                    elif event.key == pg.K_F11:
                        if pg.display.is_fullscreen():
                            self.W, self.H = 800, 600
                            self.H_W, self.H_H = self.W // 2, self.H // 2
                            self.sc = pg.display.set_mode((self.W, self.H), pg.DOUBLEBUF | pg.HWSURFACE | pg.RESIZABLE,
                                                          vsync=VSYNC)
                            self.dx = self.H_W - self.scale // 2
                            self.dy = self.H_H - self.scale // 2
                        else:
                            self.W, self.H = pg.display.get_desktop_sizes()[0]
                            self.H_W, self.H_H = self.W // 2, self.H // 2
                            self.sc = pg.display.set_mode((self.W, self.H), pg.FULLSCREEN | pg.DOUBLEBUF | pg.HWSURFACE,
                                                          vsync=VSYNC)
                            self.dx = self.H_W - self.scale // 2
                            self.dy = self.H_H - self.scale // 2
                    elif event.key == pg.K_e:
                        self.menu_simulation.show = not self.menu_simulation.show
                    elif event.key == pg.K_h:
                        self.menu_help.show = not self.menu_help.show
                    elif event.key == pg.K_i:
                        self.info = not self.info
                    elif pg.K_0 <= event.key <= pg.K_9:
                        if self.menu_settings.show:
                            self.menu_settings.key_press(event)
                        elif key[pg.K_v]:
                            if event.key < pg.K_6:
                                self.view = event.key - pg.K_0
                            elif event.key == pg.K_6:
                                if self.view < 6:
                                    self.view = 6
                                else:
                                    if self.view < 7:
                                        self.view = ITEM_LEN + 5
                                    else:
                                        self.view -= 1
                            elif event.key == pg.K_7:
                                if self.view < 6:
                                    self.view = 6
                                else:
                                    if self.view - 4 > ITEM_LEN:
                                        self.view = 6
                                    else:
                                        self.view += 1
                    elif event.key == pg.K_n:
                        self.draw_hp_block = not self.draw_hp_block
                    elif event.key == pg.K_q:
                        if self.menu_settings.show:
                            self.menu_settings.show = False
                            self.menu_settings.update()
                            self.menu_settings.draw(self.sc)
                            w = int(self.menu_settings.size[0])
                            h = int(self.menu_settings.size[1])
                            self.menu_settings.change = 0
                            if w != self.w_s[0] or h != self.w_s[1]:
                                world_copy = self.world[0]
                                min_w = min(w, self.w_s[0]) * 2
                                min_h = min(h, self.w_s[1]) * 2
                                self.w_s = (w, h)
                                self.w_s2 = (self.w_s[0] * 2, self.w_s[1] * 2)
                                self.world = world.create(self.w_s)
                                for y in range(min_h):
                                    self.world[0][y][:min_w] = world_copy[y][:min_w]
                        else:
                            self.menu_settings.show = True
                    elif event.key == pg.K_k:
                        if pg.key.get_pressed()[pg.K_TAB]:
                            if pg.key.get_pressed()[pg.K_DELETE]:
                                self.world[0] = [[None for i_ in range(self.w_s2[0])] for i in range(self.w_s2[1])]
                            else:
                                lx, ly = self.w_s2[0] - 1, self.w_s2[1] - 1
                                for i in range(self.w_s2[1] * self.w_s2[0] // 4):
                                    self.world[0][randint(0, ly)][randint(0, lx)] = None
                    elif event.key == pg.K_m:
                        if self.speed == FPS:
                            self.speed = 0
                        else:
                            self.speed = FPS
                    elif event.key == pg.K_d:
                        self.world[2] = not self.world[2]
                    elif event.key == pg.K_s:
                        self.save_world()
                    elif event.key == pg.K_SPACE:
                        world.update_1(self.world, self.s_animal, self.s_plant, self.s_corpse, self.w_s, self.w_s2)
                        count = world.update_2(self.world, self.w_s, self.w_s2)
                        self.statistic.append(count)
                        self.record()
                    elif event.key == 13:
                        self.menu_copy.show = not self.menu_copy.show
                    elif event.key == pg.K_LEFT:
                        if self.speed > 0:
                            self.speed -= 1
                    elif event.key == pg.K_RIGHT:
                        self.speed += 1
                    elif event.key == pg.K_l:
                        self.menu_load_world.show = not self.menu_load_world.show
                    elif event.key == pg.K_g:
                        self.grid_drawing = not self.grid_drawing
                    elif event.key == 96:
                        self.menu_script.show = not self.menu_script.show
                        self.menu_script.writing = True
                    else:
                        if self.menu_settings.show and self.menu_settings.change:
                            self.menu_settings.key_press(event)

    def load_world(self, name, mode=False):
        if mode:
            if len(name) > 5 and name[-6:] == '.lifew':
                with open(name, 'rb') as f:
                    data = f.read()
            else:
                return
        else:
            with open(f'{PATH_WORLDS}/{name}', 'rb') as f:
                data = f.read()
        os = 0
        sx = data[os]
        os += 1
        sy = data[os]
        os += 1
        width = bin_to_int(data[os:os + sx])
        os += sx
        height = bin_to_int(data[os:os + sy])
        os += sy
        self.w_s = (width, height)
        self.w_s2 = (width * 2, height * 2)
        self.menu_settings.size = [str(self.w_s[0]), str(self.w_s[1])]
        self.world = world.create(self.w_s)
        sx = data[os]
        os += 1
        self.world[5] = bin_to_int(data[os:os + sx])
        os += sx
        sy = data[os]
        os += 1
        self.world[6] = bin_to_int(data[os:os + sy])
        sun = int((sin(self.world[6] / 640) * 20 + sin(self.world[6] / 40) * 20 + 20)) // 2
        self.world[1] = sun if sun > 0 else 0
        os += sy
        size = data[os]
        os += 1
        num = bin_to_int(data[os:os + size])
        os += size
        water_point = [i for i in range(num)]
        for i in range(num):
            sx = data[os]
            os += 1
            sy = data[os]
            os += 1
            x = bin_to_int(data[os:os + sx])
            os += sx
            y = bin_to_int(data[os:os + sy])
            os += sy
            water_point[i] = (x, y)
        self.world[4] = water_point
        for y in range(self.w_s2[1]):
            for x in range(self.w_s2[0]):
                name = data[os]
                if name == 0:
                    pass
                elif name == 1:
                    os += 1
                    color = [data[os], data[os + 1], data[os + 2]]
                    os += 2
                    item = [i for i in range(ITEM_LEN)]
                    for i in range(ITEM_LEN):
                        os += 1
                        item[i] = bin_to_int(data[os + 1:os + data[os] + 1])
                        os += data[os]
                    os += 2
                    gen_len = bin_to_int(data[os:os + data[os - 1]])
                    os += data[os - 1]
                    gen = [data[os + i] for i in range(gen_len)]
                    os += gen_len
                    os += 1
                    gen_point = bin_to_int(data[os:os + data[os - 1]])
                    os += data[os - 1]
                    rotate = data[os]
                    os += 1
                    len_marker = data[os]
                    marker = {}
                    os += 1
                    for i in range(len_marker):
                        name = data[os]
                        os += 1
                        sx = data[os]
                        sy = data[os + 1]
                        os += 2
                        _x = bin_to_int(data[os:os + sx])
                        os += sx
                        _y = bin_to_int(data[os:os + sy])
                        os += sy
                        marker[name] = (_x, _y)
                    len_message = data[os]
                    os += 1
                    message = [data[os + i] for i in range(len_message)]
                    os += 1 + len_message
                    c_m = bin_to_int(data[os:os + data[os - 1]])
                    self.world[0][y][x] = [0, item, gen, gen_len, color, gen_point, rotate, marker, message, c_m, x, y]
                elif name == 2:
                    os += 1
                    color = [data[os], data[os + 1], data[os + 2]]
                    os += 2
                    item = [i for i in range(ITEM_LEN)]
                    for i in range(ITEM_LEN):
                        os += 1
                        item[i] = bin_to_int(data[os + 1:os + data[os] + 1])
                        os += data[os]
                    os += 2
                    gen_len = bin_to_int(data[os:os + data[os - 1]])
                    os += data[os - 1]
                    gen = [data[os + i] for i in range(gen_len)]
                    os += gen_len
                    os += 1
                    gen_point = bin_to_int(data[os:os + data[os - 1]])
                    os += data[os - 1] + 1
                    count_mutate = bin_to_int(data[os:os + data[os - 1]])
                    self.world[0][y][x] = [1, item, gen, gen_len, color, gen_point, count_mutate, x, y]
                elif name == 3:
                    item = [i for i in range(ITEM_LEN)]
                    for i in range(ITEM_LEN):
                        os += 1
                        item[i] = bin_to_int(data[os + 1:os + data[os] + 1])
                        os += data[os]
                    self.world[0][y][x] = [2, item, x, y]
                elif name == 4:
                    os += 2
                    self.world[0][y][x] = [3, bin_to_int(data[os:os + data[os - 1]])]
                elif name == 5:
                    os += 2
                    self.world[0][y][x] = [4, bin_to_int(data[os:os + data[os - 1]])]
                os += 1

    def update(self):
        if self.speed > 0:
            a = FPS / self.speed
            r = round(self.ticks / a)
            self.ticks -= round(r * a)
            self.ticks += 1
            for i in range(r):
                world.update_1(self.world, self.s_animal, self.s_plant, self.s_corpse, self.w_s, self.w_s2)
                count = world.update_2(self.world, self.w_s, self.w_s2)
                self.statistic.append(count)
                self.record()

    def save_world(self, run=True, name_save=''):
        self.sc.fill((0, 111, 0))
        self.draw_grid()
        world.draw(self.world, self.sc, self.scale, self.W, self.H, self.w_s, self.w_s2, self.dx, self.dy,
                   self.draw_hp_block, self.font_for_block, self.view)
        self.draw_border()
        [i.draw(self.sc, self.w_s) for i in self.menu_obj]
        self.menu_copy.draw(self.sc)
        self.menu_load_world.draw(self.sc)
        self.menu_settings.update()
        self.menu_settings.draw(self.sc)
        self.menu_help.draw(self.sc)
        pos = pg.mouse.get_pos()
        x = (pos[0] - self.dx) // self.scale
        y = (pos[1] - self.dy) // self.scale
        self.menu_graphic.draw(pos, self.w_s2)
        self.menu_time.draw(self.world)
        self.menu_simulation.draw(self.name_copy, self.world, self.speed, x, y, self.view)
        sc = self.sc.copy()
        while run:
            self.sc.blit(sc, (0, 0))
            self.draw_mouse()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        run = False
                    elif event.key == pg.K_ESCAPE:
                        pg.display.set_caption(self.name_label)
                        return
                    elif event.key == pg.K_BACKSPACE:
                        name_save = name_save[:-1]
                    elif event.unicode and event.unicode not in '\\/:*?"<>|':
                        name_save += event.unicode
            pg.display.set_caption(f'{name_save}.lifew')
            pg.display.flip()
            self.clock.tick(FPS)
        pg.display.set_caption(self.name_label)
        sx, bsx = int_to_bin(self.w_s[0])
        sy, bsy = int_to_bin(self.w_s[1])
        data = bytes([sx, sy]) + bsx + bsy                                  # save size_world
        s, b = int_to_bin(self.world[5])                                    # save time
        data += bytes([s]) + b
        s, b = int_to_bin(self.world[6])                                    # save year
        data += bytes([s]) + b
        s, b = int_to_bin(len(self.world[4]))                               # save water_point
        data += bytes([s]) + b
        for i in self.world[4]:
            sx, bsx = int_to_bin(i[0])
            sy, bsy = int_to_bin(i[1])
            data += bytes([sx, sy]) + bsx + bsy

        for y in range(self.w_s2[1]):
            buffer_1 = b''
            for x in range(self.w_s2[0]):
                buffer_2 = b''
                obj = self.world[0][y][x]
                if obj is None:
                    buffer_2 += b'\x00'
                else:
                    if obj[0] == 0:              # animal
                        buffer_2 += b'\x01' + bytes(obj[4])
                        for it in obj[1]:
                            s, bs = int_to_bin(it)
                            buffer_2 += bytes([s]) + bs
                        s, bs = int_to_bin(obj[3])
                        buffer_2 += bytes([s]) + bs + bytes(obj[2])
                        s, bs = int_to_bin(obj[5])
                        buffer_2 += bytes([s]) + bs + bytes([obj[6], len(obj[7])])
                        for mr in obj[7]:
                            buffer_2 += bytes([mr])
                            sx, bsx = int_to_bin(obj[7][mr][0])
                            sy, bsy = int_to_bin(obj[7][mr][1])
                            buffer_2 += bytes([sx, sy]) + bsx + bsy
                        buffer_2 += bytes([len(obj[8])]) + bytes(obj[8])
                        s, bs = int_to_bin(obj[9])
                        buffer_2 += bytes([s]) + bs
                    elif obj[0] == 1:            # plant
                        buffer_2 += b'\x02' + bytes(obj[4])
                        for it in obj[1]:
                            s, bs = int_to_bin(it)
                            buffer_2 += bytes([s]) + bs
                        s, bs = int_to_bin(obj[3])
                        buffer_2 += bytes([s]) + bs + bytes(obj[2])
                        s, bs = int_to_bin(obj[5])
                        buffer_2 += bytes([s]) + bs
                        s, bs = int_to_bin(obj[6])
                        buffer_2 += bytes([s]) + bs
                    elif obj[0] == 2:            # corpse
                        buffer_2 += b'\x03'
                        for i in range(ITEM_LEN):
                            size, bs = int_to_bin(obj[1][i])
                            buffer_2 += bytes([size]) + bs
                    elif obj[0] == 3:            # block
                        buffer_2 += b'\x04'
                        size, bs = int_to_bin(obj[1])
                        buffer_2 += bytes([size]) + bs
                    elif obj[0] == 4:            # water
                        buffer_2 += b'\x05'
                        size, bs = int_to_bin(obj[1])
                        buffer_2 += bytes([size]) + bs
                buffer_1 += buffer_2
            data += buffer_1
        create_dirs(PATH_WORLDS)
        with open(f'{PATH_WORLDS}/{name_save}.lifew', 'wb') as f:
            f.write(data)

    def loop_tm(self):
        while self.run:
            pos = pg.mouse.get_pos()
            x = (pos[0] - self.dx) // self.scale
            y = (pos[1] - self.dy) // self.scale
            self.sc.fill((0, 111, 0))

            # event
            event_tm = testing(self.event)
            # update
            self.update()

            # draw grid
            draw_grid_tm = testing(self.draw_grid)
            # draw world
            draw_world_tm = testing(world.draw, self.world, self.sc, self.scale, self.W, self.H, self.w_s, self.w_s2,
                                    self.dx, self.dy, self.draw_hp_block, self.font_for_block, self.view)
            # draw border
            draw_border_tm = testing(self.draw_border)
            [i.draw(self.sc, self.w_s) for i in self.menu_obj]
            self.menu_copy.draw(self.sc)
            self.menu_load_world.draw(self.sc)
            self.menu_settings.update()
            self.menu_settings.draw(self.sc)
            self.menu_help.draw(self.sc)
            self.menu_graphic.draw(pos, self.w_s2)
            self.menu_time.draw(self.world)
            self.menu_simulation.draw(self.name_copy, self.world, self.speed, x, y, self.view)
            self.menu_script.update(self.W)
            self.menu_script.draw()

            # draw mouse
            draw_mouse_tm = testing(self.draw_mouse)
            # draw saved
            self.draw_saved()

            # draw info
            if self.info:
                ls = (draw_grid_tm, draw_border_tm, draw_world_tm, draw_mouse_tm, event_tm)
                sum_tm = sum(ls)
                fps = (
                    FPS if round(600000000 / sum_tm) > FPS else round(600000000 / sum_tm)) if sum_tm > 0 else '+inf'
                t = f'''draw_grid: {draw_grid_tm}\ndraw_border: {draw_border_tm}\ndraw_world: {draw_world_tm}
draw_mouse: {draw_mouse_tm}\nevent: {event_tm}\n\nsum_time: {sum_tm}\nFPS: {fps}
'''.split('\n')
                if sum_tm > 0:
                    for y in range(5):
                        tm = ls[y] / sum_tm
                        pg.draw.rect(self.sc, (255, 0, 0), (10, y * 20, round(tm * self.W), 20))
                for y, txt in enumerate(t):
                    font.draw_text_d(self.sc, txt, (10, y * 20))
            pg.display.flip()
            self.clock.tick(FPS)

    def loop(self):
        while self.run:
            pos = pg.mouse.get_pos()
            x = (pos[0] - self.dx) // self.scale
            y = (pos[1] - self.dy) // self.scale
            self.sc.fill((0, 111, 0))
            self.event()
            self.update()
            self.draw_grid()
            world.draw(self.world, self.sc, self.scale, self.W, self.H, self.w_s, self.w_s2, self.dx, self.dy,
                       self.draw_hp_block, self.font_for_block, self.view)
            self.draw_border()
            [i.draw(self.sc, self.w_s) for i in self.menu_obj]
            self.menu_copy.draw(self.sc)
            self.menu_load_world.draw(self.sc)
            self.menu_settings.update()
            self.menu_settings.draw(self.sc)
            self.menu_help.draw(self.sc)
            self.menu_graphic.draw(pos, self.w_s2)
            self.menu_time.draw(self.world)
            self.menu_simulation.draw(self.name_copy, self.world, self.speed, x, y, self.view)
            self.menu_script.update(self.W)
            self.menu_script.draw()
            self.draw_mouse()
            self.draw_saved()
            pg.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    app = App()
    if len(argv) > 1:
        if argv[1] == '-info':
            app.loop_tm()
    else:
        app.loop()
