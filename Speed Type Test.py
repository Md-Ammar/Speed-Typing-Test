import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

pygame.init()

global w, h
w, h = 1000, 800
win = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Car Race")

clock = pygame.time.Clock()
font = pygame.font.SysFont('chiller', 25, True)

run = True
typing = True

s = " "
key_delay = 0

def textbox(event, x, y):
    global font, s, key_delay
    if pygame.event.poll().type != 0:
        print(pygame.event.poll())

    if event.type == pygame.KEYDOWN:
        key = str(pygame.key.name(event.key))
        print(key)
        if key == "backspace":
            s = s[0:len(s) - 1]
        if key == "space":
            s += "_"
        if len(key) == 1:# and key.upper() != s[len(s) - 1]:
            print(s[len(s) - 1], key)
            s += key
            s = s.upper()

    txt = font.render(s, 1, (0, 0, 0))
    win.blit(txt, (x, y))


def refresh_win():
    win.fill((0, 200, 200))

    pygame.draw.rect(win, (255, 255, 255), (0.2 * w, 0.2 * h, 500, 100))
    pygame.draw.rect(win, (0, 0, 0), (0.2 * w, 0.2 * h, 500, 100), 2)

    txt = font.render(s, 1, (0, 0, 0))
    win.blit(txt, (0.2 * w, 0.2 * h))

    pygame.display.update()


while run:
    clock.tick(20)
    for event in pygame.event.get(pump=True):
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            w = win.get_width()
            h = win.get_height()
            pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        elif event.type == pygame.KEYDOWN:
            key = str(pygame.key.name(event.key))
            if key == "backspace":
                s = s[0:len(s) - 1]
            if key == "space":
                s += "_"
            if len(key) == 1:  # and key.upper() != s[len(s) - 1]:
                s += key
                s = s.upper()

    refresh_win()

pygame.quit()
