import pygame, random
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

pygame.init()

global w, h
w, h = 1000, 800
win = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Typing Speed Test")

clock = pygame.time.Clock()
font = pygame.font.SysFont('system', 25, True)

run = True
typing = True

global para, line
para = [""]
line = 0

free_type = True

with open("wordlist.txt", 'r') as wds:
    for w in wds:
        wdlist = w.split("|")


def create_wdlist():
    p = [""]
    color_code = []
    ln = 0
    sent = ""
    for i in range(0, 10):
        while True:
            wd = wdlist[random.randrange(0, len(wdlist))].upper()
            sent += wd + " "
            if len(sent + wd) + 1 > 40:
                p[ln] = sent
                p.append("")
                sent = ""
                ln += 1
                break
    return p


paragraph = create_wdlist()

def refresh_win():
    win.fill((0, 200, 200))

    pygame.draw.rect(win, (255, 255, 255), (0.2 * w, 0.2 * h, 500, 500))
    pygame.draw.rect(win, (0, 0, 0), (0.2 * w, 0.2 * h, 500, 500), 2)

    # for i in range(0, len(wdlist) - 5, 5):
    #     sent = ""
    #     for j in wdlist[i:i + 5]:
    #         sent += j + " "
    #     txt = font.render(sent.upper(), 1, (0, 0, 0))
    #     win.blit(txt, (0.2 * w, 0.2 * h + i * 4))
    for line in paragraph:
        txt = font.render(line + str(len(line)), 1, (0, 0, 0))
        win.blit(txt, (0.2 * w, 0.2 * h + paragraph.index(line) * 20))

    for Line in para:
        txt = font.render(Line, 1, (0, 200, 0))
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
                if len(para[line]) == 0 and line > 0:
                    line -= 1
            if free_type:
                if key == "space":
                    last_word = para[line].split(" ")[-1]
                    if len(para[line] + last_word) + 1 > 40:
                        para[line] = para[line][:-len(last_word)]
                        print(para[line], len())
                        para.append("")
                        line += 1
                        para[line] += last_word
                        print(para[line])
                    para[line] += " "
                if len(key) == 1:
                    if len(para[line]) + 1 > 40:
                        para.append("")
                        line += 1
                    para[line] += key
                    para[line] = para[line].upper()
            # else:
            #     if len(key) == 1:
            #         if len(para[line]) + 1 > 40:
            #             para.append("")
            #             line += 1
            #         para[line] += key
            #         para[line] = para[line].upper()
            #     if key == "space":
            #         para[line] += " "

    refresh_win()

pygame.quit()
