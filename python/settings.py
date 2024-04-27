import pygame as pg
from font import Font
from json import load
from json.decoder import JSONDecodeError
from os import listdir, mkdir, chdir


def create_dirs(path: str):
    print(path)
    directors = []
    name = ''
    for char in path:
        if char in '\\/':
            if name:
                if name not in '..':
                    directors.append(name)
                name = ''
        else:
            name += char
    if name:
        directors.append(name)
    print(directors)
    for directory in directors:
        if directory not in listdir():
            mkdir(directory)
        chdir(directory)
    for _ in directors:
        chdir('..')


try:
    with open('config.json') as f:
        load(f)
except (JSONDecodeError, FileNotFoundError):
    with open('config.json', 'w') as f:
        f.write('''{
  "width": 800,
  "height": 600,
  "fps": 60,
  "vsync": false,
  "screenshot_size": 20,
  "font": "./fonts/JetBrainsMono[wght].ttf",
  "records": "./saves/records/",
  "record_time": 10,
  "screenshot_lifei": "./saves/lifei/",
  "screenshot_png": "./saves/png/",
  "saves": "./saves/saves/",
  "worlds": "./saves/worlds/",
  "scripts": "./scripts/"
}''')
with open('config.json') as f:
    data = load(f)

WIDTH = data['width']
HEIGHT = data['height']
FPS = data['fps']
VSYNC = data['vsync']
SCREENSHOT_SIZE = data['screenshot_size']
PATH_FONT = data['font']
PATH_RECORDS = data['records']
RECORD_TIME = data['record_time']
PATH_SCREENSHOT_LIFEI = data['screenshot_lifei']
PATH_SCREENSHOT_PNG = data['screenshot_png']
PATH_SAVES = data['saves']
PATH_WORLDS = data['worlds']
PATH_SCRIPTS = data['scripts']

# simulate settings
ITEM_PLANT = {
    'e': 300,
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'Health': 3,
    'Plant': 1,
    'Water': 0,
    'Salt': 0,
    'Acid': 0,
    'Fat': 0,
    'Potion': 0
}
ITEM_ANIMAL = {
    'e': 300,
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'Health': 3,
    'Plant': 0,
    'Water': 0,
    'Salt': 0,
    'Acid': 0,
    'Fat': 0,
    'Potion': 0
}
ITEM_CORPSE = {
    'e': 300,
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'Health': 0,
    'Plant': 0,
    'Water': 0,
    'Salt': 0,
    'Acid': 0,
    'Fat': 0,
    'Potion': 0
}


ITEM_MAX = (5000, 100, 100, 100, 100, 15, 10, 10, 10, 10, 30, 30)
SYNTHESIS_ANIMAL = (
    (
        (5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (4, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0)
    ),
    (
        (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
    ),
    (
        (0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0)
    ),
    (
        (0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0),
        (300, 50, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (200, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
    ),
    (
        (5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
        (200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (0, 0, 0, 0, 0, 0, 0, 5, 1, 1, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10)
    ),
    (
        (20, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 5),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    )
)
SYNTHESIS_PLANT = (
    (
        (5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 10, 0, 0,  0, 0, 0, 0, 0, 0)
    ),
    (
        (4, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0)
    ),
    (
        (0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0)
    ),
    (
        (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
    ),
    (
        (0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0)
    ),
    (
        (100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
    ),
    (
        (0, 0, 0, 0, 0, 0, 0, 5, 1, 1, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10)
    ),
    (
        (20, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 5),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    )
)


# init
def c(r) -> list:
    a = []
    for i in range(2*r+1):
        a.append((-r+i, -r))
    for i in range(2*r-1):
        a.append((r, -r+i+1))
    for i in range(2*r+1):
        a.append((r-i, r))
    for i in range(2*r-1):
        a.append((-r, r-i-1))
    return a


RANGE = [c(i + 1) for i in range(10)]
RADIUS = []
for i in RANGE:
    for ii in i:
        RADIUS.append(ii)

RADIUS_PLANT = []
for i in [c(i + 1) for i in range(3)]:
    for ii in i:
        RADIUS_PLANT.append(ii)
del i, ii, c


ANGLE_1 = {1, 4, 5, 9, 10, 16, 17, 18, 25, 26, 27, 28, 36, 37, 38, 39, 49, 50, 51, 52, 53, 64, 65, 66, 66, 67, 68, 69,
           81, 82, 83, 84, 85, 86, 100, 101, 102, 103, 104, 105, 106}
ANGLE_2 = {2, 6, 11, 12, 13, 19, 20, 21, 29, 30, 31, 40, 41, 42, 43, 44, 54, 55, 56, 57, 58, 70, 71, 72, 73, 74, 87, 88,
           89, 90, 91, 92, 93, 107, 108, 109, 110, 111, 112, 113}
ANGLE_3 = {3, 7, 8, 14, 15, 22, 23, 24, 32, 33, 34, 35, 45, 46, 47, 48, 59, 60, 61, 62, 63, 75, 76, 77, 78, 79, 80, 94,
           95, 96, 97, 98, 99, 114, 115, 116, 117, 118, 119, 120}

IMAGE_MOUSE = pg.Surface((10, 10), pg.SRCALPHA)
mmap = (
    (0, 0, 0, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 2, 2, 2, 2, 1, 0, 0),
    (0, 1, 2, 3, 3, 3, 3, 2, 1, 0),
    (1, 2, 3, 3, 3, 3, 3, 3, 2, 1),
    (1, 2, 3, 3, 3, 3, 3, 3, 2, 1),
    (1, 2, 3, 3, 3, 3, 3, 3, 2, 1),
    (1, 2, 3, 3, 3, 3, 3, 3, 2, 1),
    (0, 1, 2, 3, 3, 3, 3, 2, 1, 0),
    (0, 0, 1, 2, 2, 2, 2, 1, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 0, 0, 0)
)
for y__, iy in enumerate(mmap):
    for x__, ix in enumerate(iy):
        if ix:
            col = (87, 83, 64) if ix == 1 else (154, 147, 113) if ix == 2 else (239, 228, 176)
            IMAGE_MOUSE.set_at((x__, y__), col)
IMAGE_MOUSE_RESIZE = pg.Surface((14, 14), pg.SRCALPHA)
mmap = (
    (0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0),
    (0, 0, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 0, 0),
    (0, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 0),
    (1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
    (1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1),
    (0, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 0),
    (0, 0, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 0, 0),
    (0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 2, 1, 1, 2, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0)
)
for y__, iy in enumerate(mmap):
    for x__, ix in enumerate(iy):
        if ix:
            col = (87, 83, 64) if ix == 1 else (154, 147, 113) if ix == 2 else (239, 228, 176)
            IMAGE_MOUSE_RESIZE.set_at((x__, y__), col)
del mmap, y__, iy, x__, ix, col


font = Font(PATH_FONT)
SYNTHESIS_ANIMAL_LEN = len(SYNTHESIS_ANIMAL)
SYNTHESIS_PLANT_LEN = len(SYNTHESIS_PLANT)
ITEM_N = [i for i in ITEM_PLANT]
ITEM_L_ANIMAL = [ITEM_ANIMAL[i] for i in ITEM_ANIMAL]
ITEM_L_PLANT = [ITEM_PLANT[i] for i in ITEM_PLANT]
ITEM_L_CORPSE = [ITEM_CORPSE[i] for i in ITEM_CORPSE]
ITEM_LEN = len(ITEM_PLANT)
CORPSE_KILL = ITEM_LEN * 8
L_I = round(len(ITEM_PLANT) / 14 + 0.49)
