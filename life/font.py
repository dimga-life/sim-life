import pygame
import pygame as pg

s1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789абвгдеёжзийклмн'
s2 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_|?+-#/=,()&>:.'


class Font:
    def __init__(self, path):
        pygame.font.init()
        self.font = pygame.font.Font(path, 14)

    def draw_text_l(self, sc: pg.Surface, text='', pos=(0, 0), alpha=255):
        txt = self.font.render(text, True, (0, 0, 0))
        if alpha != 255:
            txt.set_alpha(alpha)
        sc.blit(txt, pos)

    def draw_text_d(self, sc: pg.Surface, text='', pos=(0, 0), alpha=255):
        txt = self.font.render(text, True, (255, 255, 255))
        if alpha != 255:
            txt.set_alpha(alpha)
        sc.blit(txt, pos)
