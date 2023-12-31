import pygame, random
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE
from datetime import datetime

pygame.init()

global w, h
w, h = 1000, 600
win = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Typing Speed Test")

clock = pygame.time.Clock()
font = pygame.font.SysFont('times new roman', 20, True)
font_heading = pygame.font.SysFont('chiller', 50, True)

run = True
text_mode = True

global para, line
para = {0: ""}
line = 0
wd = ""

with open("data/wordlist.txt", 'r') as wds:
    for w in wds:
        wdlist = w.split("|")


def create_wdlist():
    # p = [""]
    # color_code = []
    # ln = 0
    # sent = ""
    # for i in range(0, 10):
    #     color_code.append([])
    #     while True:
    #         wd = wdlist[random.randrange(0, len(wdlist))].upper() + " "
    #         if len(sent + wd) > 40:
    #             p[ln] = sent
    #             p.append("")
    #             sent = ""
    #             ln += 1
    #             break
    #         sent += wd
    #         color_code[i].append((100, 100, 100))
    # return p
    paragraph = {}
    lines = 10
    for line in range(lines):
        while paragraph[line]["coord"] < 500:
            paragraph[i] = {"word": wdlist[random.randrange(0, len(wdlist))], "color": (255, 255, 255), "coord": 0}
            sent = ' '.join(item for item in (paragraph[j]["word"] for j in range(i)))
            paragraph[i]["coord"] = font.render(sent, 1, (0, 0, 0)).get_width()

    print(paragraph)
    return paragraph


Paragraph = create_wdlist()

def Text_mode(key):
    global line
    if key == "backspace":
        if len(para[line]) > 0:
            para[line] = para[line][:-1]
        elif len(para[line]) == 0 and line > 0:
            line -= 1

    if key == "space":
        para[line] += " "

    if key == "return":
        line += 1
        para[line] = ""

    if len(key) == 1:#valid key
        cur_word = para[line].split(" ")[-1]

        if len(para[line] + cur_word) > 40:
            para[line] = para[line][:-len(cur_word)]
            line += 1
            para[line] = ""
            para[line] += cur_word

        if len(para[line]) + 1 >= 40:
            line += 1
            para[line] = ""

        para[line] += key
        para[line] = para[line].upper()


class Type_Speed():
    def __init__(self):
        pass


def interface():
    global wd
    para_win = (0.2 * w, 0.2 * h, 0.8 * w - 0.2 * w, 200)
    text_box = (0.4 * w, 0.7 * h, 200, 50)

    pygame.draw.rect(win, (200, 0, 0), para_win, 2)
    pygame.draw.rect(win, (0, 200, 0), text_box, 2)

    # for line in paragraph:
    #     txt = font.render(line, 1, (255, 255, 255))
    #     win.blit(txt, (0.2 * w, 0.2 * h + paragraph.index(line) * 20))

    txt = font.render(wd, 1, (0, 255, 0))
    win.blit(txt, text_box[:2])

    for k in Paragraph.keys():
        win.blit(font.render(Paragraph[k]["word"], 1, Paragraph[k]["color"]), (Paragraph[k]["coord"], 0))


def refresh_win():
    win.fill((0, 0, 0))

    txt = font_heading.render("TYPING SPEED TEST", 1, (200, 0, 200))
    win.blit(txt, (0.25 * w, 0.1 * h))

    if text_mode:
        pygame.draw.rect(win, (200, 0, 0), (0.2 * w, 0.2 * h, 500, 500), 3)
        for Line in para.keys():
            txt = font.render(para[Line], 1, (0, 200, 100))
            if Line == line:
                txt = font.render(para[Line] + "|", 1, (0, 200, 100))
            win.blit(txt, (0.2 * w, 0.2 * h + Line * 20))
    if not text_mode:
        interface()

    pygame.display.update()


key = ""

type_speed = Type_Speed()

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

            if key == "tab":
                text_mode = False if text_mode else True
                print(text_mode)

            if key == "escape":
                run = False

            if text_mode:
                Text_mode(key)
            else:
                if key == "space":
                    wd = ""
                elif key == "backspace" and len(wd) > 0:
                    wd = wd[:-1]
                elif len(key) == 1:
                    wd += key.upper()

    refresh_win()

pygame.quit()
