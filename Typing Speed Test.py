import pygame, random
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

pygame.init()

global w, h
w, h = 1000, 800
win = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Typing Speed Test")

clock = pygame.time.Clock()
font = pygame.font.SysFont('times new roman', 20, True)
font_heading = pygame.font.SysFont('chiller', 50, True)

run = True

global para, line
para = [""]
line = 0

free_type = False

with open("wordlist.txt", 'r') as wds:
    for w in wds:
        wdlist = w.split("|")


def create_wdlist():
    p = [""]
    color_code = []
    ln = 0
    sent = ""
    for i in range(0, 10):
        color_code.append([])
        while True:
            wd = wdlist[random.randrange(0, len(wdlist))].upper() + " "
            if len(sent + wd) > 40:
                p[ln] = sent
                p.append("")
                sent = ""
                ln += 1
                break
            sent += wd
            color_code[i].append((100, 100, 100))
    return p

paragraph = create_wdlist()
wd = ""
key = ""
wdcount = 0
typed_para = [""]
typed_count = 0


def typed(k):
    global typed_count, typed_para, line
    k = k.upper()
    if typed_count >= len(paragraph[line]):
        typed_para.append("")
        typed_count = 0
        line += 1
    print(typed_count)
    print(k, paragraph[line][typed_count])
    if k == "SPACE":
        k = " "
    if k == paragraph[line][typed_count]:
        typed_para[line] += k
        typed_count += 1


# def check(w):
#     global wdcount, m_sent, line
#     cur_line = paragraph[line]
#
#     w = cur_line.split(" ")[wdcount]
#
#     # if w == wd:
#     #     print("match")
#     # else:
#     #     print(w, wd, "not matched")
#
#     if wdcount == cur_line.count(" "):
#         line += 1
#         wdcount = 0
#     else:
#         wdcount += 1


def ___():
    global wd
    para_win = (0.2 * w, 0.2 * h, 0.8 * w - 0.2 * w, 200)
    text_box = (0.4 * w, 0.5 * h, 200, 100)

    pygame.draw.rect(win, (200, 0, 0), para_win, 2)
    pygame.draw.rect(win, (0, 200, 0), text_box, 2)

    for line in paragraph:
        txt = font.render(line, 1, (255, 255, 255))
        win.blit(txt, (0.2 * w, 0.2 * h + paragraph.index(line) * 20))

    txt = font.render(wd, 1, (0, 255, 0))
    win.blit(txt, (text_box[0], text_box[1]))


def refresh_win():
    win.fill((0, 0, 0))

    txt = font_heading.render("TYPING SPEED TEST", 1, (200, 0, 200))
    win.blit(txt, (0.25 * w, 0.1 * h))
    if free_type:
        pygame.draw.rect(win, (200, 0, 0), (0.2 * w, 0.2 * h, 500, 500), 3)

        for Line in para:
            txt = font.render(Line, 1, (0, 255, 0))
            win.blit(txt, (0.2 * w, 0.2 * h + para.index(Line) * 20))

    if not free_type:
        ___()
        for l in typed_para:
            txt = font.render(l, 1, (0, 0, 200))
            win.blit(txt, (0.2 * w, 0.2 * h + typed_para.index(l ) * 20))

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
            if key == "tab":
                if free_type:free_type = False
                else: free_type = True
            if key == "escape":
                run = False
            if free_type:
                if key == "backspace" and len(para[0]) > 0:
                    para[line] = para[line][0:len(para[line]) - 1]
                    if len(para[line]) == 0 and line > 0:
                        line -= 1
                if key == "space":
                    para[line] += " "
                if len(key) == 1:
                    last_word = para[line].split(" ")[-1]

                    if len(para[line] + last_word) > 40:
                        para[line] = para[line][:-len(last_word)]
                        para.append("")
                        line += 1
                        para[line] += last_word

                    if len(para[line]) + 1 >= 40:
                        para.append("")
                        line += 1

                    para[line] += key
                    para[line] = para[line].upper()
            else:
                typed(key)
                if key == "space":
                    # check(wd)
                    wd = ""
                elif key == "backspace" and len(wd) > 0:
                    wd = wd[:-1]
                elif len(key) == 1:
                    wd += key.upper()

    refresh_win()

pygame.quit()
