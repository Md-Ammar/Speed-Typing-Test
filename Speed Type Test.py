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

para = [""]
line = 0
key_delay = 0

def refresh_win():
    win.fill((0, 200, 200))

    pygame.draw.rect(win, (255, 255, 255), (0.2 * w, 0.2 * h, 500, 100))
    pygame.draw.rect(win, (0, 0, 0), (0.2 * w, 0.2 * h, 500, 100), 2)

    for Line in para:
        txt = font.render(Line, 1, (0, 0, 0))
        win.blit(txt, (0.2 * w, 0.2 * h + para.index(Line) * 20))

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
        if event.type == pygame.KEYDOWN:
            key = str(pygame.key.name(event.key))
            if key == "escape":
                run = False
            if key == "backspace":
                para[line] = para[line][0:len(para[line]) - 1]
            if key == "space":
                para[line] += " "
            if len(key) == 1:  # and key.upper() != s[len(s) - 1]:
                if len(para[line]) > 20:
                    para.append("")
                    line += 1
                para[line] += key
                para[line] = para[line].upper()

    refresh_win()

pygame.quit()
