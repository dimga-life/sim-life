from settings import *
from random import randint
from tools import mutate_gen
from math import sin


def create(w_s):
    # world sun day_cycle mutate water_point time year
    water_point = [(randint(0, w_s[0] * 2 - 1), randint(0, w_s[1] * 2 - 1)) for i in range(w_s[0] * w_s[1] // 500)]
    world = [[None for i_ in range(w_s[0] * 2)] for i in range(w_s[1] * 2)]
    return [world, 10, False, 0, water_point, 0, 0]


def draw(world, sc, scale, w, h, w_s, w_s2, dx, dy, draw_hp_block, font_for_block, e) -> None:
    h_scale = scale // 2
    dxx = dx // scale - w_s[0]
    dyy = dy // scale - w_s[1]
    r1 = range(-1, w // scale + 1)
    r2 = range(-1, h // scale + 1)
    if e == 0:
        for y in r2:
            for x in r1:
                x2 = x - dxx
                y2 = y - dyy
                if -1 < x2 < w_s2[0] and -1 < y2 < w_s2[1]:
                    if world[0][y2][x2] is not None:
                        obj = world[0][y2][x2]
                        name = obj[0]
                        x3 = (x2 - w_s[0]) * scale + dx
                        y3 = (y2 - w_s[1]) * scale + dy
                        if name == 0:
                            r = obj[6]
                            pg.draw.rect(sc, obj[4], (x3, y3, scale, scale))
                            if scale >= 20:
                                x4 = (0, 1, 1, 1, 0, -1, -1, -1)[r] * scale // 4 + scale // 2
                                y4 = (-1, -1, 0, 1, 1, 1, 0, -1)[r] * scale // 4 + scale // 2
                                pg.draw.circle(sc, (0, 0, 0), (x3 + x4, y3 + y4), scale // 20)
                        elif name == 1:
                            if scale >= 2:
                                pg.draw.circle(sc, obj[4], (x3 + h_scale, y3 + h_scale), h_scale)
                            else:
                                pg.draw.rect(sc, obj[4], (x3, y3, scale, scale))
                        elif name == 2:
                            pg.draw.polygon(sc, (127, 127, 127), (
                                (x3, y3 + h_scale),
                                (x3 + h_scale, y3),
                                (x3 + scale, y3 + h_scale),
                                (x3 + h_scale, y3 + scale)
                            ))
                        elif name == 3:
                            pg.draw.rect(sc, (30, 30, 30), (x3, y3, scale, scale))
                            if draw_hp_block and scale >= 10:
                                text = font_for_block.render(f"{obj[1]}", False, (255, 255, 255))
                                r = text.get_rect()
                                sc.blit(text, (x3 + h_scale - r[2] // 2, y3 + h_scale - r[3] // 2))
                        elif name == 4:
                            water = obj[1] * 10
                            pg.draw.rect(sc, (0, min(111 + water, 255), min(water, 255)), (x3, y3, scale, scale))
                            if draw_hp_block and scale >= 10:
                                text = font_for_block.render(f"{obj[1]}", False, (255, 255, 255))
                                r = text.get_rect()
                                sc.blit(text, (x3 + h_scale - r[2] // 2, y3 + h_scale - r[3] // 2))
    elif e < 5:
        for y in r2:
            for x in r1:
                x2 = x - dxx
                y2 = y - dyy
                if -1 < x2 < w_s2[0] and -1 < y2 < w_s2[1]:
                    if world[0][y2][x2] is not None:
                        obj = world[0][y2][x2]
                        name = obj[0]
                        x3 = (x2 - w_s[0]) * scale + dx
                        y3 = (y2 - w_s[1]) * scale + dy
                        if name == 0 and e == 1:
                            r = obj[6]
                            pg.draw.rect(sc, obj[4], (x3, y3, scale, scale))
                            if scale >= 20:
                                x4 = (0, 1, 1, 1, 0, -1, -1, -1)[r] * scale // 4 + scale // 2
                                y4 = (-1, -1, 0, 1, 1, 1, 0, -1)[r] * scale // 4 + scale // 2
                                pg.draw.circle(sc, (0, 0, 0), (x3 + x4, y3 + y4), scale // 20)
                        elif name == 1 and e == 2:
                            if scale >= 2:
                                pg.draw.circle(sc, obj[4], (x3 + h_scale, y3 + h_scale), h_scale)
                            else:
                                pg.draw.rect(sc, obj[4], (x3, y3, scale, scale))
                        elif name == 2 and e == 3:
                            pg.draw.polygon(sc, (127, 127, 127), (
                                           (x3, y3 + h_scale),
                                           (x3 + h_scale, y3),
                                           (x3 + scale, y3 + h_scale),
                                           (x3 + h_scale, y3 + scale)
                                       ))
                        elif name == 3 and e == 4:
                            pg.draw.rect(sc, (30, 30, 30), (x3, y3, scale, scale))
                            if draw_hp_block and scale >= 10:
                                text = font_for_block.render(f"{obj[1]}", False, (255, 255, 255))
                                r = text.get_rect()
                                sc.blit(text, (x3 + h_scale - r[2] // 2, y3 + h_scale - r[3] // 2))
    elif e == 5:
        for y in r2:
            for x in r1:
                x2 = x - dxx
                y2 = y - dyy
                if -1 < x2 < w_s2[0] and -1 < y2 < w_s2[1]:
                    obj = world[0][y2][x2]
                    if obj is not None:
                        name = obj[0]
                        x3 = (x2 - w_s[0]) * scale + dx
                        y3 = (y2 - w_s[1]) * scale + dy
                        if name in (0, 1):
                            rad = min(obj[6] * 10, 255)
                            pg.draw.rect(sc, (rad, rad, rad), (x3, y3, scale, scale))
    else:
        for y in r2:
            for x in r1:
                x2 = x - dxx
                y2 = y - dyy
                if -1 < x2 < w_s2[0] and -1 < y2 < w_s2[1]:
                    obj = world[0][y2][x2]
                    if obj is not None:
                        name = obj[0]
                        x3 = (x2 - w_s[0]) * scale + dx
                        y3 = (y2 - w_s[1]) * scale + dy
                        if name == 3:
                            pg.draw.rect(sc, (0, 0, 255), (x3, y3, scale, scale))
                        elif name == 4:
                            pg.draw.rect(sc, (0, 255, 255), (x3, y3, scale, scale))
                        else:
                            c_ = obj[1][e - 6] * 255 // ITEM_MAX[e - 6]
                            if -1 < c_ < 256:
                                pg.draw.rect(sc, (c_, c_, 0), (x3, y3, scale, scale))


def mutate(world, w_s2):
    x = randint(0, w_s2[0] - 1)
    y = randint(0, w_s2[1] - 1)
    obj = world[0][y][x]
    if obj is not None:
        if obj[0] == 0 or obj[0] == 1:
            l, m = mutate_gen(obj[2], obj[3])
            if m:
                if obj[0] == 0:
                    obj[9] += 1
                else:
                    obj[6] += 1
                obj[3] = l
                obj[5] %= l
                obj[4] = [randint(0, 255), randint(0, 255), randint(0, 255)]


def screenshot(world, scale, w_s2, draw_hp_block, font_for_block, e) -> pg.Surface:
    sc = pg.Surface((w_s2[0] * scale, w_s2[1] * scale))
    sc.fill((0, 111, 0))
    h_scale = scale // 2
    r1 = range(w_s2[0])
    r2 = range(w_s2[1])
    if e == 0:
        for y2 in r2:
            for x2 in r1:
                if world[0][y2][x2] is not None:
                    obj = world[0][y2][x2]
                    name = obj[0]
                    x3 = x2 * scale
                    y3 = y2 * scale
                    if name == 0:
                        r = obj[6]
                        pg.draw.rect(sc, obj[4], (x3, y3, scale, scale))
                        if scale >= 20:
                            x4 = (0, 1, 1, 1, 0, -1, -1, -1)[r] * scale // 4 + scale // 2
                            y4 = (-1, -1, 0, 1, 1, 1, 0, -1)[r] * scale // 4 + scale // 2
                            pg.draw.circle(sc, (0, 0, 0), (x3 + x4, y3 + y4), scale // 20)
                    elif name == 1:
                        if scale >= 2:
                            pg.draw.circle(sc, obj[4], (x3 + h_scale, y3 + h_scale), h_scale)
                        else:
                            pg.draw.rect(sc, obj[4], (x3, y3, scale, scale))
                    elif name == 2:
                        pg.draw.polygon(sc, (127, 127, 127), (
                            (x3, y3 + h_scale),
                            (x3 + h_scale, y3),
                            (x3 + scale, y3 + h_scale),
                            (x3 + h_scale, y3 + scale)
                        ))
                    elif name == 3:
                        pg.draw.rect(sc, (30, 30, 30), (x3, y3, scale, scale))
                        if draw_hp_block and scale >= 10:
                            text = font_for_block.render(f"{obj[1]}", False, (255, 255, 255))
                            r = text.get_rect()
                            sc.blit(text, (x3 + h_scale - r[2] // 2, y3 + h_scale - r[3] // 2))
                    elif name == 4:
                        water = obj[1] * 10
                        pg.draw.rect(sc, (0, min(111 + water, 255), min(water, 255)), (x3, y3, scale, scale))
                        if draw_hp_block and scale >= 10:
                            text = font_for_block.render(f"{obj[1]}", False, (255, 255, 255))
                            r = text.get_rect()
                            sc.blit(text, (x3 + h_scale - r[2] // 2, y3 + h_scale - r[3] // 2))
    elif e < 5:
        for y2 in r2:
            for x2 in r1:
                if world[0][y2][x2] is not None:
                    obj = world[0][y2][x2]
                    name = obj[0]
                    x3 = x2 * scale
                    y3 = y2 * scale
                    if name == 0 and e == 1:
                        r = obj[6]
                        pg.draw.rect(sc, obj[4], (x3, y3, scale, scale))
                        if scale >= 20:
                            x4 = (0, 1, 1, 1, 0, -1, -1, -1)[r] * scale // 4 + scale // 2
                            y4 = (-1, -1, 0, 1, 1, 1, 0, -1)[r] * scale // 4 + scale // 2
                            pg.draw.circle(sc, (0, 0, 0), (x3 + x4, y3 + y4), scale // 20)
                    elif name == 1 and e == 2:
                        if scale >= 2:
                            pg.draw.circle(sc, obj[4], (x3 + h_scale, y3 + h_scale), h_scale)
                        else:
                            pg.draw.rect(sc, obj[4], (x3, y3, scale, scale))
                    elif name == 2 and e == 3:
                        pg.draw.polygon(sc, (127, 127, 127), (
                                       (x3, y3 + h_scale),
                                       (x3 + h_scale, y3),
                                       (x3 + scale, y3 + h_scale),
                                       (x3 + h_scale, y3 + scale)
                                   ))
                    elif name == 3 and e == 4:
                        pg.draw.rect(sc, (30, 30, 30), (x3, y3, scale, scale))
                        if draw_hp_block and scale >= 10:
                            text = font_for_block.render(f"{obj[1]}", False, (255, 255, 255))
                            r = text.get_rect()
                            sc.blit(text, (x3 + h_scale - r[2] // 2, y3 + h_scale - r[3] // 2))
    elif e == 5:
        for y2 in r2:
            for x2 in r1:
                obj = world[0][y2][x2]
                if obj is not None:
                    name = obj[0]
                    x3 = x2 * scale
                    y3 = y2 * scale
                    if name in (0, 1):
                        rad = min(obj[6] * 10, 255)
                        pg.draw.rect(sc, (rad, rad, rad), (x3, y3, scale, scale))
    else:
        for y2 in r2:
            for x2 in r1:
                if -1 < x2 < w_s2[0] and -1 < y2 < w_s2[1]:
                    obj = world[0][y2][x2]
                    if obj is not None:
                        name = obj[0]
                        x3 = x2 * scale
                        y3 = y2 * scale
                        if name == 3:
                            pg.draw.rect(sc, (0, 0, 255), (x3, y3, scale, scale))
                        elif name == 4:
                            pg.draw.rect(sc, (0, 255, 255), (x3, y3, scale, scale))
                        else:
                            c_ = obj[1][e - 6] * 255 // ITEM_MAX[e - 6]
                            if -1 < c_ < 256:
                                pg.draw.rect(sc, (c_, c_, 0), (x3, y3, scale, scale))
    return sc


def update_1(world, sp_animal, sp_plant, sp_corpse, w_s, w_s2):
    if sp_animal:
        for i in range(w_s[0] * w_s[1] // 100):
            x = randint(0, w_s2[0] - 1)
            y = randint(0, w_s2[1] - 1)
            if world[0][y][x] is None:
                add_animal(world, pos=(x, y), gen_len=randint(5, 48), w_s=w_s)
    if sp_plant:
        for i in range(w_s[0] * w_s[1]):
            x = randint(0, w_s2[0] - 1)
            y = randint(0, w_s2[1] - 1)
            if world[0][y][x] is None:
                add_plant(world, pos=(x, y), gen_len=randint(5, 20))
    if sp_corpse:
        for i in range(w_s[0] * w_s[1]):
            x = randint(0, w_s2[0] - 1)
            y = randint(0, w_s2[1] - 1)
            if world[0][y][x] is None:
                add_corpse(world, pos=(x, y))

    if world[4]:
        x = randint(0, w_s2[0] - 1)
        y = randint(0, w_s2[1] - 1)
        new_point = world[4][0]
        min_ = (new_point[0] - x) ** 2 + (new_point[1] - y) ** 2
        for point in world[4][1:]:
            r = (point[0] - x) ** 2 + (point[1] - y) ** 2
            if r < min_:
                min_ = r
                new_point = point
        o = world[0][new_point[1]][new_point[0]]
        if o is None or o[0] != 4:
            world[0][new_point[1]][new_point[0]] = [4, 2]
        elif o[1] < 100:
            o[1] += 2
            if o[1] > 100:
                o[1] = 100
        else:
            for i in RADIUS:
                x2 = new_point[0] + i[0]
                y2 = new_point[1] + i[1]
                if -1 < x2 < w_s2[0] and -1 < y2 < w_s2[1]:
                    if (o := world[0][y2][x2]) is not None and o[0] == 4:
                        if o[1] < 100:
                            o[1] += 2
                            if o[1] > 100:
                                o[1] = 100
                            break
                    else:
                        world[0][y2][x2] = [4, 0]
                        break

    if world[2]:
        if world[5] == 4000:
            world[5] = 0
            world[6] += 1
        else:
            world[5] += 1
        sun = int((sin(world[5] / 640) * 20 + sin(world[5] / 40) * 20 + 20)) // 2  # [0, 29]
        world[1] = sun if sun > 0 else 0


def update_2(world, w_s, w_s2) -> tuple[int, int, int, int, int]:
    count_animal = 0
    count_plant = 0
    count_corpse = 0
    count_block = 0
    count_water = 0
    zero_one = {0, 1}
    w_s20, w_s21 = w_s2
    _sun = world[1]
    do_not_update = [[False for i_ in range(w_s20)] for i in range(w_s21)]
    # update animal & plant
    for _y_ in range(w_s21):
        for _x_ in range(w_s20):
            if do_not_update[_y_][_x_]:
                do_not_update[_y_][_x_] = False
            else:
                obj = world[0][_y_][_x_]
                if obj is not None:
                    _name = obj[0]
                    if _name == 0:
                        _item = obj[1]
                        _item[0] -= 1
                        if _item[0] < 1 or _item[5] < 1 or _item[11] > 19:
                            if _item[0] < 1:
                                _item[0] = 0
                            _item[5] = 0
                            world[0][_y_][_x_] = None
                            add_corpse(world, (_x_, _y_), _item)
                            continue
                        _gen = obj[2]
                        _gen_len = obj[3]
                        _color = obj[4]
                        _marker = obj[7]
                        _listen = obj[8]
                        count_animal += 1
                        cmd = _gen[obj[5]]
                        # wait
                        if cmd == 0:
                            pass
                        # motion
                        elif cmd < 9:
                            if _item[0] > 4 and _item[2] > 0:
                                _item[0] -= 5
                                _item[2] -= 1
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[(cmd - 1 + obj[6]) % 8] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[(cmd - 1 + obj[6]) % 8] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21:
                                    if world[0][y][x] is None:
                                        obj[10] = x
                                        obj[11] = y
                                        do_not_update[y][x] = True
                                        world[0][y][x] = obj
                                        world[0][_y_][_x_] = None
                        # rotate
                        elif cmd < 16:
                            if _item[0] > 1 and _item[1] > 0:
                                _item[0] -= 2
                                _item[1] -= 1
                                obj[6] = (obj[6] + cmd) % 8
                        # get rotate
                        elif cmd == 16:
                            if _item[0] > 1 and _item[3] > 0:
                                _item[0] -= 2
                                _item[3] -= 1
                                obj[5] = (obj[5] + obj[6] + 1) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # eat
                        elif cmd == 17:
                            if _item[0] > 2:
                                _item[0] -= 3
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[obj[6]] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[obj[6]] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None:
                                    if o[0] == 1:
                                        for index, im in enumerate(o[1]):
                                            if index != 5:
                                                d = im // 4
                                                _item[index] += d
                                                if _item[index] > ITEM_MAX[index]:
                                                    _item[index] = ITEM_MAX[index]
                                                    d -= _item[index] - ITEM_MAX[index]
                                                o[1][index] -= d
                                    elif o[0] == 2:
                                        s = 0
                                        for index, im in enumerate(o[1]):
                                            if index != 5:
                                                d = im // 4
                                                _item[index] += d
                                                if _item[index] > ITEM_MAX[index]:
                                                    _item[index] = ITEM_MAX[index]
                                                    d -= _item[index] - ITEM_MAX[index]
                                                o[1][index] -= d
                                                s += im - d
                                        if s < CORPSE_KILL:
                                            world[0][y][x] = None
                                    elif o[0] == 4:
                                        water = o[1] // 4
                                        _item[7] += water
                                        if _item[7] > ITEM_MAX[7]:
                                            _item[7] = ITEM_MAX[7]
                                            water -= _item[7] - ITEM_MAX[7]
                                        o[1] -= water
                                        if o[1] == 0:
                                            world[0][y][x] = None
                        # mitosis
                        elif cmd == 18:
                            if _item[0] > 29 and _item[3] > 0 and _item[4] > 1:
                                _item[0] -= 30
                                _item[3] -= 1
                                _item[4] -= 2
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[obj[6]] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[obj[6]] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21:
                                    if world[0][y][x] is None:
                                        items = [it // 4 for it in _item]
                                        items[5] = 3
                                        add_animal(world, pos=(x, y), gen=_gen.copy(), color=_color,
                                                   item=items.copy(), w_s=w_s)
                                        do_not_update[y][x] = True
                                        items[5] = 0
                                        for index, it in enumerate(items):
                                            _item[index] -= it
                        # see angle
                        elif cmd == 19:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                angle = 1
                                f = False
                                for rr, circle in enumerate(RANGE):
                                    r = rr + 1
                                    for index in range(r * 2 + 1):
                                        p = circle[(index + obj[6]) % 8]
                                        x = p[0] + _x_
                                        y = p[1] + _y_
                                        if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is not None:
                                            indexes = r ** 2 + index
                                            if indexes in ANGLE_1:
                                                angle = 2
                                            elif indexes in ANGLE_2:
                                                angle = 3
                                            elif indexes in ANGLE_3:
                                                angle = 4
                                            f = True
                                            break
                                    if f:
                                        break
                                obj[5] = (obj[5] + angle) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see distance
                        elif cmd == 20:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                radius = 1
                                f = False
                                for rr, circle in enumerate(RANGE):
                                    r = rr + 1
                                    for index in range(r * 2 + 1):
                                        p = circle[(index + obj[6]) % 8]
                                        x = p[0] + _x_
                                        y = p[1] + _y_
                                        if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is not None:
                                            radius = r + 1
                                            f = True
                                            break
                                    if f:
                                        break
                                obj[5] = (obj[5] + radius) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see type
                        elif cmd == 21:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                t = 1
                                f = False
                                for rr, circle in enumerate(RANGE):
                                    r = rr + 1
                                    for index in range(r * 2 + 1):
                                        p = circle[(index + obj[6]) % 8]
                                        x = p[0] + _x_
                                        y = p[1] + _y_
                                        if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None:
                                            if o[0] == 0 and o[4] == _color:
                                                t = 7
                                            else:
                                                t = o[0] + 2
                                            f = True
                                            break
                                    if f:
                                        break
                                obj[5] = (obj[5] + t) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # inspect
                        elif cmd == 22:
                            obj[5] = (obj[5] + 1) % _gen_len
                            index = _gen[obj[5]]
                            if index <= ITEM_LEN:
                                it = _sun if index == ITEM_LEN else _item[index]
                                obj[5] = (obj[5] + 1) % _gen_len
                                val = _gen[obj[5]]
                                if it < val:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                elif it == val:
                                    obj[5] = (obj[5] + 2) % _gen_len
                                else:
                                    obj[5] = (obj[5] + 3) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # double inspect
                        elif cmd == 23:
                            obj[5] = (obj[5] + 1) % _gen_len
                            index = _gen[obj[5]]
                            if index <= ITEM_LEN:
                                it = _sun if index == ITEM_LEN else obj[1][index]
                                obj[5] = (obj[5] + 1) % _gen_len
                                val = _gen[obj[5]] << 8
                                obj[5] = (obj[5] + 1) % _gen_len
                                val += _gen[obj[5]]
                                if it < val:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                elif it == val:
                                    obj[5] = (obj[5] + 2) % _gen_len
                                else:
                                    obj[5] = (obj[5] + 3) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # jump
                        elif cmd == 24:
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] += _gen[obj[5]]
                        # double jump
                        elif cmd == 25:
                            obj[5] = (obj[5] + 1) % _gen_len
                            val = _gen[obj[5]]
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] += val << 8 + _gen[obj[5]]
                        # back jump
                        elif cmd == 26:
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] -= _gen[obj[5]] + 2
                        # double back jump
                        elif cmd == 27:
                            obj[5] = (obj[5] + 1) % _gen_len
                            val = _gen[obj[5]] << 8
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] -= val + _gen[obj[5]] + 2
                        # attach
                        elif cmd == 28:
                            if _item[0] > 4:
                                _item[0] -= 5
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[obj[6]] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[obj[6]] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None:
                                    if o[0] in zero_one:
                                        o[1][5] -= 1
                                        if o[1][5] < 1:
                                            world[0][y][x] = None
                                            add_corpse(world, (x, y), o[1])
                                    elif o[0] == 3:
                                        o[1] -= 1
                                        if o[1] < 1:
                                            world[0][y][x] = None
                        # set_marker
                        elif cmd == 29:
                            if _item[0] > 4 and _item[4] > 2:
                                _item[0] -= 5
                                _item[4] -= 3
                                obj[5] = (obj[5] + 1) % _gen_len
                                if _gen[obj[5]] != 255:
                                    _marker[_gen[obj[5]]] = (_x_, _y_)
                        # get_marker
                        elif cmd == 30:
                            if _item[0] > 4:
                                _item[0] -= 5
                                obj[5] = (obj[5] + 1) % _gen_len
                                if _gen[obj[5]] in _marker:
                                    v = _marker[_gen[obj[5]]]
                                    x = v[0] - _x_
                                    y = v[1] - _y_
                                    d = max(abs(x), abs(y))
                                    if d == 0:
                                        obj[5] += 9
                                    else:
                                        x = round(x / d) + 1
                                        y = round(y / d) + 1
                                        ang = (
                                            (7, 0, 1),
                                            (6, 0, 2),
                                            (5, 4, 3)
                                        )
                                        obj[5] += ((ang[y][x] + 8 - obj[6]) % 8) + 1
                                    obj[5] %= _gen_len
                                    obj[5] += _gen[obj[5]]
                                elif _gen[obj[5]] == 255:
                                    x = w_s[0] - _x_
                                    y = w_s[1] - _y_
                                    d = max(abs(x), abs(y))
                                    if d == 0:
                                        obj[5] += 9
                                    else:
                                        x = round(x / d) + 1
                                        y = round(y / d) + 1
                                        ang = (
                                            (7, 0, 1),
                                            (6, 0, 2),
                                            (5, 4, 3)
                                        )
                                        obj[5] += ((ang[y][x] + 8 - obj[6]) % 8) + 1
                                    obj[5] %= _gen_len
                                    obj[5] += _gen[obj[5]]
                                else:
                                    obj[5] = (obj[5] + 10) % _gen_len
                                    obj[5] += _gen[obj[5]]
                        # del_marker
                        elif cmd == 31:
                            if _item[0] > 9:
                                _item[0] -= 10
                                obj[5] = (obj[5] + 1) % _gen_len
                                name = _gen[obj[5]]
                                if name in _marker:
                                    _marker.pop(name)
                        # say
                        elif cmd == 32:
                            if _item[0] > 0:
                                _item[0] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                for x, y in RADIUS:
                                    x2 = x + _x_
                                    y2 = y + _y_
                                    if -1 < x2 < w_s20 and -1 < y2 < w_s21:
                                        o = world[0][y2][x2]
                                        if o is not None and o[0] == 0 and o[4] == obj[4]:
                                            o[8].append(_gen[obj[5]] % 16)
                        # listen
                        elif cmd == 33:
                            if _item[0] > 0:
                                _item[0] -= 1
                                if obj[8]:
                                    obj[5] = (obj[5] + _listen.pop(0) + 1) % _gen_len
                                    obj[5] += _gen[obj[5]]
                        # build
                        elif cmd == 34:
                            if _item[0] > 1 and _item[1] > 9 and _item[7] > 0 and _item[8] > 0:
                                _item[0] -= 2
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[obj[6]] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[obj[6]] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is None:
                                    _item[1] -= 10
                                    _item[7] -= 1
                                    _item[8] -= 1
                                    add_block(world, (x, y))
                        # synthesis
                        elif cmd < 47:
                            index = cmd - 35
                            mat = SYNTHESIS_ANIMAL[index][0]
                            prod = SYNTHESIS_ANIMAL[index][1]
                            for m in range(ITEM_LEN):
                                if _item[m] < mat[m]:
                                    break
                            else:
                                for m in range(ITEM_LEN):
                                    _item[m] -= mat[m]
                                for p in range(ITEM_LEN):
                                    _item[p] += prod[p]
                                    if _item[p] > ITEM_MAX[p]:
                                        _item[p] = ITEM_MAX[p]
                        # motion -> type
                        elif cmd < 55:
                            if _item[0] > 4 and _item[2] > 0:
                                _item[0] -= 5
                                _item[2] -= 1
                                rot = (cmd - 46 + obj[6]) % 8
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[rot] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[rot] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21:
                                    if world[0][y][x] is None:
                                        obj[10] = x
                                        obj[11] = y
                                        do_not_update[y][x] = True
                                        world[0][y][x] = obj
                                        world[0][_y_][_x_] = None
                                        obj[5] = (obj[5] + 1) % _gen_len
                                        obj[5] = (obj[5] + _gen[obj[5]])
                                    else:
                                        obj[5] = (obj[5] + world[0][y][x][0] + 2) % _gen_len
                                        obj[5] = (obj[5] + _gen[obj[5]])
                                else:
                                    obj[5] = (obj[5] + 4) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]])
                            else:
                                obj[5] = (obj[5] + 4) % _gen_len
                                obj[5] = (obj[5] + _gen[obj[5]])
                        # eat -> successful
                        elif cmd == 55:
                            if _item[0] > 2:
                                _item[0] -= 3
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[obj[6]] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[obj[6]] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None:
                                    if o[0] == 1:
                                        obj[5] = (obj[5] + 2) % _gen_len
                                        obj[5] = (obj[5] + _gen[obj[5]])
                                        for index, im in enumerate(o[1]):
                                            if index != 5:
                                                d = im // 4
                                                _item[index] += d
                                                if _item[index] > ITEM_MAX[index]:
                                                    _item[index] = ITEM_MAX[index]
                                                    d -= _item[index] - ITEM_MAX[index]
                                                o[1][index] -= d
                                    elif o[0] == 2:
                                        obj[5] = (obj[5] + 2) % _gen_len
                                        obj[5] = (obj[5] + _gen[obj[5]])
                                        s = 0
                                        for index, im in enumerate(o[1]):
                                            if index != 5:
                                                d = im // 4
                                                _item[index] += d
                                                if _item[index] > ITEM_MAX[index]:
                                                    _item[index] = ITEM_MAX[index]
                                                    d -= _item[index] - ITEM_MAX[index]
                                                o[1][index] -= d
                                                s += im - d
                                        if s <= CORPSE_KILL:
                                            world[0][y][x] = None
                                    elif o[0] == 4:
                                        obj[5] = (obj[5] + 2) % _gen_len
                                        obj[5] = (obj[5] + _gen[obj[5]])
                                        water = o[1] // 4
                                        o[1] -= water
                                        _item[7] += water
                                        if _item[7] > ITEM_MAX[7]:
                                            _item[7] = ITEM_MAX[7]
                                        if o[1] == 0:
                                            world[0][y][x] = None
                                else:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]])
                            else:
                                obj[5] = (obj[5] + 1) % _gen_len
                                obj[5] = (obj[5] + _gen[obj[5]])
                        # mitosis -> successful
                        elif cmd == 56:
                            if _item[0] > 29 and _item[3] > 0 and _item[4] > 1:
                                _item[0] -= 30
                                _item[3] -= 1
                                _item[4] -= 2
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[obj[6]] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[obj[6]] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is None:
                                    obj[5] = (obj[5] + 2) % obj[3]
                                    obj[5] = (obj[5] + obj[2][obj[5]])
                                    items = [it // 4 for it in obj[1]]
                                    items[5] = 3
                                    add_animal(world, pos=(x, y), gen=_gen.copy(), color=_color, item=_item.copy(),
                                               w_s=w_s)
                                    do_not_update[y][x] = True
                                    items[5] = 0
                                    for index, it in enumerate(items):
                                        if index != 5:
                                            obj[1][index] -= it
                                else:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]])
                            else:
                                obj[5] = (obj[5] + 1) % _gen_len
                                obj[5] = (obj[5] + _gen[obj[5]])
                        # see angle (dist)
                        elif cmd == 57:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                dist = _gen[obj[5]] % 10 + 1
                                angle = 1
                                for i in range(dist * 2 + 1):
                                    p = RANGE[dist - 1][(i + obj[6]) % 8]
                                    x = p[0] + _x_
                                    y = p[1] + _y_
                                    if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is not None:
                                        indexes = dist ** 2 + i
                                        if indexes in ANGLE_1:
                                            angle = 2
                                        elif indexes in ANGLE_2:
                                            angle = 3
                                        elif indexes in ANGLE_3:
                                            angle = 4
                                        break
                                obj[5] = (obj[5] + angle) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see angle (type)
                        elif cmd == 58:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                type_ = _gen[obj[5]]
                                angle = 1
                                f = False
                                for rr, circle in enumerate(RANGE):
                                    r = rr + 1
                                    for index in range(r * 2 + 1):
                                        p = circle[(index + obj[6]) % 8]
                                        x = p[0] + _x_
                                        y = p[1] + _y_
                                        if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is not None and \
                                                world[0][y][x][0] == type_:
                                            indexes = r ** 2 + index
                                            if indexes in ANGLE_1:
                                                angle = 2
                                            elif indexes in ANGLE_2:
                                                angle = 3
                                            elif indexes in ANGLE_3:
                                                angle = 4
                                            f = True
                                            break
                                    if f:
                                        break
                                obj[5] = (obj[5] + angle) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see angle (dist & type)
                        elif cmd == 59:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                dist = _gen[obj[5]] % 10 + 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                type_ = _gen[obj[5]]
                                angle = 1

                                for i in range(dist * 2 + 1):
                                    p = RANGE[dist - 1][(i + obj[6]) % 8]
                                    x = p[0] + _x_
                                    y = p[1] + _y_
                                    if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None and o[0] == type_:
                                        indexes = dist ** 2 + i
                                        if indexes in ANGLE_1:
                                            angle = 2
                                        elif indexes in ANGLE_2:
                                            angle = 3
                                        elif indexes in ANGLE_3:
                                            angle = 4
                                        break
                                obj[5] = (obj[5] + angle) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see distance (angle)
                        elif cmd == 60:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                radius = 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                angle = _gen[obj[5]] % 3
                                f = False
                                for rr, circle in enumerate(RANGE):
                                    r = rr + 1
                                    for index in range(r * 2 + 1):
                                        p = circle[(index + obj[6]) % 8]
                                        x = p[0] + _x_
                                        y = p[1] + _y_
                                        if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is not None:
                                            if r ** 2 + index in (ANGLE_1, ANGLE_2, ANGLE_3)[angle]:
                                                radius = r + 1
                                                f = True
                                                break
                                    if f:
                                        break
                                obj[5] = (obj[5] + radius) % obj[3]
                                obj[5] += obj[2][obj[5]]
                        # see distance (type)
                        elif cmd == 61:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                type_ = _gen[obj[5]]
                                radius = 1
                                rot = obj[6]
                                f = False
                                for rr, circle in enumerate(RANGE):
                                    r = rr + 1
                                    for index in range(r * 2 + 1):
                                        p = circle[(index + rot) % 8]
                                        x = p[0] + _x_
                                        y = p[1] + _y_
                                        if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None \
                                                and o[0] == type_:
                                            radius = r + 1
                                            f = True
                                            break
                                    if f:
                                        break
                                obj[5] = (obj[5] + radius) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see distance (angle & type)
                        elif cmd == 62:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                angle = (_gen[obj[5]] + obj[6]) % 3
                                obj[5] = (obj[5] + 1) % _gen_len
                                type_ = _gen[obj[5]]
                                radius = 1
                                for rr, circle in enumerate(RANGE):
                                    r = rr + 1
                                    for index in range(r * 2 + 1):
                                        p = circle[(index + obj[6]) % 8]
                                        x = p[0] + _x_
                                        y = p[1] + _y_
                                        if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None \
                                                and o[0] == type_:
                                            if r ** 2 + index in (ANGLE_1, ANGLE_2, ANGLE_3)[angle]:
                                                radius = r + 1
                                                break
                                obj[5] = (obj[5] + radius) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see type (angle)
                        elif cmd == 63:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                angle = (_gen[obj[5]] + obj[6]) % 3
                                t = 1
                                for rr, circle in enumerate(RANGE):
                                    r = rr + 1
                                    for index in range(r * 2 + 1):
                                        p = circle[(index + obj[6]) % 8]
                                        x = p[0] + _x_
                                        y = p[1] + _y_
                                        if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None:
                                            if r ** 2 + index in (ANGLE_1, ANGLE_2, ANGLE_3)[angle]:
                                                if o[0] == 0 and o[4] == _color:
                                                    t = 7
                                                else:
                                                    t = o[0] + 2
                                                break
                                obj[5] = (obj[5] + t) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see type (dist)
                        elif cmd == 64:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                dist = _gen[obj[5]] % 10
                                rot = obj[6]
                                t = 1
                                circle = RANGE[dist]
                                for index in range(dist * 2 + 1):
                                    p = circle[(index + rot) % 8]
                                    x = p[0] + _x_
                                    y = p[1] + _y_
                                    if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None:
                                        if o[0] == 0 and o[4] == _color:
                                            t = 7
                                        else:
                                            t = o[0] + 2
                                        break
                                obj[5] = (obj[5] + t) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # see type (angle & dist)
                        elif cmd == 65:
                            if _item[0] > 0 and _item[2] > 0:
                                _item[0] -= 1
                                _item[2] -= 1
                                obj[5] = (obj[5] + 1) % _gen_len
                                angle = _gen[obj[5]] % 3
                                obj[5] = (obj[5] + 1) % _gen_len
                                dist = _gen[obj[5]] % 10
                                t = 1
                                p = RANGE[dist][(angle + obj[6]) % 8]
                                x = p[0] + _x_
                                y = p[1] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None:
                                    if o[0] == 0:
                                        t = 7
                                    else:
                                        t = o[0] + 2
                                obj[5] = (obj[5] + t) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # attach -> successful
                        elif cmd == 66:
                            if _item[0] > 4:
                                _item[0] -= 5
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[obj[6]] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[obj[6]] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21 and (o := world[0][y][x]) is not None:
                                    if o[0] in zero_one:
                                        o[1][5] -= 1
                                        obj[5] = (obj[5] + 2) % _gen_len
                                        obj[5] = (obj[5] + _gen[obj[5]])
                                        if o[1][5] < 1:
                                            add_corpse(world, (x, y), o[1])
                                    elif o[0] == 3:
                                        o[1] -= 1
                                        obj[5] = (obj[5] + 2) % _gen_len
                                        obj[5] = (obj[5] + _gen[obj[5]])
                                        if o[1] < 1:
                                            world[0][y][x] = None
                                    else:
                                        obj[5] = (obj[5] + 1) % _gen_len
                                        obj[5] = (obj[5] + _gen[obj[5]])
                                else:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]])
                            else:
                                obj[5] = (obj[5] + 1) % _gen_len
                                obj[5] = (obj[5] + _gen[obj[5]])
                        # build -> successful
                        elif cmd == 67:
                            if _item[0] > 1 and _item[1] > 9 and _item[7] > 0 and _item[8] > 0:
                                _item[0] -= 2
                                x = (0, 1, 1, 1, 0, -1, -1, -1)[obj[6]] + _x_
                                y = (-1, -1, 0, 1, 1, 1, 0, -1)[obj[6]] + _y_
                                if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is None:
                                    _item[1] -= 10
                                    _item[7] -= 1
                                    _item[8] -= 1
                                    obj[5] = (obj[5] + 2) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]])
                                    add_block(world, (x, y))
                                else:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]])
                            else:
                                obj[5] = (obj[5] + 1) % _gen_len
                                obj[5] = (obj[5] + _gen[obj[5]])
                        # synthesis -> successful
                        elif cmd < 80:
                            index = cmd - 68
                            mat = SYNTHESIS_ANIMAL[index][0]
                            prod = SYNTHESIS_ANIMAL[index][1]
                            obj[5] = (obj[5] + 1) % obj[3]
                            for m in range(ITEM_LEN):
                                if obj[1][m] < mat[m]:
                                    break
                            else:
                                obj[5] = (obj[5] + 1) % obj[3]
                                for m in range(ITEM_LEN):
                                    _item[m] -= mat[m]
                                for p in range(ITEM_LEN):
                                    obj[1][p] += prod[p]
                                    if _item[p] > ITEM_MAX[p]:
                                        _item[p] = ITEM_MAX[p]
                            obj[5] = (obj[5] + _gen[obj[5]])

                        obj[5] = (obj[5] + 1) % _gen_len
                    elif _name == 1:
                        _item = obj[1]
                        _item[0] -= 1
                        if _item[0] < 1 or _item[5] < 1 or _item[11] > 19:
                            if _item[0] < 1:
                                _item[0] = 0
                            _item[5] = 0
                            world[0][_y_][_x_] = None
                            add_corpse(world, (_x_, _y_), _item)
                            continue
                        _gen = obj[2]
                        _gen_len = obj[3]
                        _color = obj[4]
                        count_plant += 1
                        cmd = _gen[obj[5]]
                        # wait
                        if cmd == 0:
                            pass
                        # mitosis
                        elif cmd == 1:
                            if _item[0] > 49 and _item[1] > 9 and _item[2] > 2:
                                _item[0] -= 50
                                _item[1] -= 10
                                _item[2] -= 3
                                x = _x_ + randint(-10, 10)
                                y = _y_ + randint(-10, 10)
                                if -1 < x < w_s20 and -1 < y < w_s21:
                                    if world[0][y][x] is None:
                                        items = [it // 4 for it in _item]
                                        items[5] = 3
                                        do_not_update[y][x] = True
                                        add_plant(world, pos=(x, y), gen=_gen.copy(), color=_color,
                                                  item=_item.copy())
                                        items[5] = 0
                                        for index, it in enumerate(items):
                                            _item[index] -= it
                        # inspect
                        elif cmd == 2:
                            obj[5] = (obj[5] + 1) % _gen_len
                            index = _gen[obj[5]]
                            if index <= ITEM_LEN:
                                it = _sun if index == ITEM_LEN else _item[index]
                                obj[5] = (obj[5] + 1) % _gen_len
                                val = _gen[obj[5]]
                                if it < val:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                elif it == val:
                                    obj[5] = (obj[5] + 2) % _gen_len
                                else:
                                    obj[5] = (obj[5] + 3) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # double inspect
                        elif cmd == 3:
                            obj[5] = (obj[5] + 1) % _gen_len
                            index = _gen[obj[5]]
                            if index <= ITEM_LEN:
                                it = _sun if index == ITEM_LEN else _item[index]
                                obj[5] = (obj[5] + 1) % _gen_len
                                val = 256 * _gen[obj[5]]
                                obj[5] = (obj[5] + 1) % _gen_len
                                val += _gen[obj[5]]
                                if it < val:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                elif it == val:
                                    obj[5] = (obj[5] + 2) % _gen_len
                                else:
                                    obj[5] = (obj[5] + 3) % _gen_len
                                obj[5] += _gen[obj[5]]
                        # jump
                        elif cmd == 4:
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] += _gen[obj[5]]
                        # double jump
                        elif cmd == 5:
                            obj[5] = (obj[5] + 1) % _gen_len
                            val = _gen[obj[5]]
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] += 256 * val + _gen[obj[5]]
                        # back jump
                        elif cmd == 6:
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] -= _gen[obj[5]] + 2
                        # double back jump
                        elif cmd == 7:
                            obj[5] = (obj[5] + 1) % _gen_len
                            val = _gen[obj[5]] << 8
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] -= val + _gen[obj[5]] + 2
                        # photosynthesis
                        elif cmd == 8:
                            if _item[6] > 0:
                                count = 0
                                for r in RADIUS_PLANT:
                                    x_ = _x_ + r[0]
                                    y_ = _y_ + r[1]
                                    if -1 < x_ < w_s20 and -1 < y_ < w_s21 and (o := world[0][y_][x_]) is not None:
                                        count += (1, 1, 1, 5, 0)[o[0]]
                                if count < 31:
                                    _item[0] += _sun * (w_s21 - _y_) // w_s21 + _item[6]
                                    if _item[0] > ITEM_MAX[0]:
                                        _item[0] = ITEM_MAX[0]
                        # root
                        elif cmd == 9:
                            if _item[0] > 1:
                                _item[0] -= 2
                                for x, y in RADIUS:
                                    x2 = _x_ + x
                                    y2 = _y_ + y
                                    if -1 < x2 < w_s20 and -1 < y2 < w_s21:
                                        o = world[0][y2][x2]
                                        if o is not None:
                                            if o[0] == 2:
                                                s = 0
                                                for index, im in enumerate(o[1]):
                                                    if index != 5:
                                                        d = im // 4
                                                        _item[index] += d
                                                        if _item[index] > ITEM_MAX[index]:
                                                            _item[index] = ITEM_MAX[index]
                                                            d -= _item[index] - ITEM_MAX[index]
                                                        o[1][index] -= d
                                                        s += im - d
                                                if s < CORPSE_KILL:
                                                    world[0][y2][x2] = None
                                                break
                                            elif o[0] == 4:
                                                if o[1] > 1:
                                                    water = 2
                                                elif o[1] == 1:
                                                    water = 1
                                                else:
                                                    water = 0
                                                _item[7] += water
                                                if _item[7] > ITEM_MAX[7]:
                                                    _item[7] = ITEM_MAX[7]
                                                    water -= _item[7] - ITEM_MAX[7]
                                                o[1] -= water
                                                if o[1] == 0:
                                                    world[0][y2][x2] = None
                                                break
                        # synthesis
                        elif cmd < 20:
                            index = cmd - 10
                            mat = SYNTHESIS_PLANT[index][0]
                            prod = SYNTHESIS_PLANT[index][1]
                            for m in range(ITEM_LEN):
                                if obj[1][m] < mat[m]:
                                    break
                            else:
                                for m in range(ITEM_LEN):
                                    _item[m] -= mat[m]
                                for p in range(ITEM_LEN):
                                    _item[p] += prod[p]
                                    if _item[p] > ITEM_MAX[p]:
                                        _item[p] = ITEM_MAX[p]
                        # mitosis -> successful
                        elif cmd == 20:
                            if _item[0] > 49 and _item[1] > 9 and _item[2] > 2:
                                _item[0] -= 50
                                _item[1] -= 10
                                _item[2] -= 3
                                x = _x_ + randint(-10, 10)
                                y = _y_ + randint(-10, 10)
                                if -1 < x < w_s20 and -1 < y < w_s21 and world[0][y][x] is None:
                                    items = [it // 4 for it in _item]
                                    items[5] = 3
                                    do_not_update[y][x] = True
                                    add_plant(world, pos=(x, y), gen=_gen.copy(), color=_color,
                                              item=_item.copy())
                                    items[5] = 0
                                    for index, it in enumerate(items):
                                        obj[1][index] -= it
                                    obj[5] = (obj[5] + 2) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]]) % _gen_len
                                else:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]]) % _gen_len
                            else:
                                obj[5] = (obj[5] + 1) % _gen_len
                                obj[5] = (obj[5] + _gen[obj[5]]) % _gen_len
                        # root -> successful
                        elif cmd == 21:
                            if _item[0] > 1:
                                _item[0] -= 2
                                for x, y in RADIUS:
                                    x2 = _x_ + x
                                    y2 = _y_ + y
                                    if -1 < x2 < w_s20 and -1 < y2 < w_s21:
                                        o = world[0][y2][x2]
                                        if o is not None:
                                            if o[0] == 2:
                                                s = 0
                                                for index, im in enumerate(o[1]):
                                                    if index != 5:
                                                        d = im // 4
                                                        _item[index] += d
                                                        if _item[index] > ITEM_MAX[index]:
                                                            _item[index] = ITEM_MAX[index]
                                                            d -= _item[index] - ITEM_MAX[index]
                                                        o[1][index] -= d
                                                        s += im - d
                                                if s < CORPSE_KILL:
                                                    world[0][y2][x2] = None
                                                obj[5] = (obj[5] + 2) % _gen_len
                                                obj[5] = (obj[5] + _gen[obj[5]]) % _gen_len
                                                break
                                            elif o[0] == 4:
                                                if o[1] > 1:
                                                    water = 2
                                                elif o[1] == 1:
                                                    water = 1
                                                else:
                                                    water = 0
                                                _item[7] += water
                                                if _item[7] > ITEM_MAX[7]:
                                                    _item[7] = ITEM_MAX[7]
                                                    water -= _item[7] - ITEM_MAX[7]
                                                o[1] -= water
                                                obj[5] = (obj[5] + 2) % _gen_len
                                                obj[5] = (obj[5] + _gen[obj[5]]) % _gen_len
                                                if o[1] == 0:
                                                    world[0][y2][x2] = None
                                                break
                                else:
                                    obj[5] = (obj[5] + 1) % _gen_len
                                    obj[5] = (obj[5] + _gen[obj[5]]) % _gen_len
                            else:
                                obj[5] = (obj[5] + 1) % _gen_len
                                obj[5] = (obj[5] + _gen[obj[5]]) % _gen_len
                        # synthesis -> successful
                        elif cmd < 32:
                            index = cmd - 22
                            mat = SYNTHESIS_PLANT[index][0]
                            prod = SYNTHESIS_PLANT[index][1]
                            for m in range(ITEM_LEN):
                                if _item[m] < mat[m]:
                                    break
                            else:
                                obj[5] = (obj[5] + 1) % _gen_len
                                for m in range(ITEM_LEN):
                                    obj[1][m] -= mat[m]
                                for p in range(ITEM_LEN):
                                    obj[1][p] += prod[p]
                                    if obj[1][p] > ITEM_MAX[p]:
                                        obj[1][p] = ITEM_MAX[p]
                            obj[5] = (obj[5] + 1) % _gen_len
                            obj[5] = (obj[5] + _gen[obj[5]]) % _gen_len
                        obj[5] = (obj[5] + 1) % _gen_len
                    elif _name == 2:
                        count_corpse += 1
                    elif _name == 3:
                        count_block += 1
                    elif _name == 4:
                        count_water += 1
    for i in range(world[3]):
        mutate(world, w_s2)
    return count_animal, count_plant, count_corpse, count_block, count_water


def add_animal(world, pos=(0, 0), gen=None, gen_len=16, item=None, color=None, w_s=None):
    gen = [randint(0, 255) for i in range(gen_len)] if gen is None else gen
    gen_len = gen_len if gen is None else len(gen)
    item = ITEM_L_ANIMAL.copy() if item is None else item
    color = [randint(0, 255), randint(0, 255), randint(0, 255)] if color is None else color
    marker = {
        1: (0, 0),
        2: (w_s[0] * 2 - 1, 0),
        3: (w_s[0] * 2 - 1, w_s[1] * 2 - 1),
        4: (0, w_s[1] * 2 - 1)
    }
    world[0][pos[1]][pos[0]] = [0, item, gen, gen_len, color, 0, 0, marker, [], 0, pos[0], pos[1]]


def add_plant(world, pos=(0, 0), gen=None, gen_len=16, item=None, color=None):
    gen = [randint(0, 40) for i in range(gen_len)] if gen is None else gen
    gen_len = gen_len if gen is None else len(gen)
    item = ITEM_L_PLANT.copy() if item is None else item
    color = [randint(0, 255), randint(0, 255), randint(0, 255)] if color is None else color
    world[0][pos[1]][pos[0]] = [1, item, gen, gen_len, color, 0, 0]


def add_corpse(world, pos=(0, 0), item=None):
    world[0][pos[1]][pos[0]] = [2, ITEM_L_CORPSE.copy() if item is None else item]


def add_block(world, pos=(0, 0)):
    world[0][pos[1]][pos[0]] = [3, 10]
