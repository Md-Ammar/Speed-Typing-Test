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

s = ""

def textbox(x, y):
    global font, s

    if event.type == pygame.MOUSEBUTTONDOWN:
        # pygame.draw.rect(win, (200, 0, 0), (c[0], c[1], wid, 30), 2)
        pygame.display.update()

    if event.type == pygame.KEYDOWN:
        l = str(pygame.key.name(event.key))
        print(l)
        if l == "backspace":
            s = s[0:len(s) - 1]
        if l == "space":
            s += " "
        if len(l) == 1:
            s += l
            s = s.upper()
    txt = font.render(s, 1, (0, 0, 0))
    win.blit(txt, (x, y))


def refresh_win():
    win.fill((0, 200, 200))

    pygame.draw.rect(win, (255, 255, 255), (0.2 * w, 0.2 * h, 500, 100))
    pygame.draw.rect(win, (0, 0, 0), (0.2 * w, 0.2 * h, 500, 100), 2)

    if typing:
        textbox(0.2 * w, 0.2 * h)
    pygame.display.update()


while run:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.VIDEORESIZE:
            w = win.get_width()
            h = win.get_height()
            pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)

    refresh_win()

pygame.quit()
