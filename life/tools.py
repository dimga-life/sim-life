from random import randint, random
from time import perf_counter_ns


def mutate_gen(gen, len_gen):
    ch = 0.5 / len_gen
    m = False
    # change gen
    if random() < 0.25:
        for i in range(len_gen):
            if random() < ch:
                m = True
                gen[i] = randint(0, 255)
    # paste
    elif random() < ch:
        m = True
        p = randint(0, len_gen - 1)
        gen[:] = gen[:p] + [randint(0, 255)] + gen[p:]
        len_gen += 1
    # delete
    elif random() < ch + 0.125:
        if len_gen > 1:
            m = True
            p = randint(0, len_gen - 1)
            len_gen -= 1
            gen.pop(p)
    return len_gen, m


def int_to_bin(num) -> (int, bytes):
    if num < 0:
        num = 0
    l_ = len(bin(num)[2:])
    a = l_ // 8 + 1 if l_ % 8 else l_ // 8
    return a, num.to_bytes(a, 'big')


def bin_to_int(bs) -> int:
    s = 0
    for i, b in enumerate(bs[::-1]):
        s += b << (i * 8)
    return s


def testing(func, *args):
    st = perf_counter_ns()
    func(*args)
    end = perf_counter_ns()
    tm = end - st
    return tm


def get_chunks(w, h, s=21):
    s2 = s * 2
    full_w, half_w = divmod(w, s2)
    full_h, half_h = divmod(h, s2)
    ls = []
    ls2 = [[], [], [], []]
    for y in range(full_h):
        for x in range(full_w):
            ls.append((x * s2, y * s2, s2, s2))
    if half_h:
        for x in range(full_w):
            ls.append((x * s2, full_h * s2, s2, half_h))
    if half_w:
        for y in range(full_h):
            ls.append((full_w * s2, y * s2, half_w, s2))
    if half_w and half_h:
        ls.append((full_w * s2, full_h * s2, half_w, half_h))

    for i in ls:
        w1, h1, w2, h2 = i
        for ix, iy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            x = w1 + ix * s
            y = h1 + iy * s
            if w2 == s2:
                sx = s
            else:
                sx = w2 - s * ix
            if h2 == s2:
                sy = s
            else:
                sy = h2 - s * iy
            if sx > 0 and sy > 0:
                chunk = (x, y, x + sx, y + sy)
                ls2[ix + iy * 2].append(chunk)
    return ls2
