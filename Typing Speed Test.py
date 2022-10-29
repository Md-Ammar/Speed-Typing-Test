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

global para, line
para = {}
line = 0
wd = ""

text_mode = False

with open("data/wordlist.txt", 'r') as wds:
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


def Text_mode(key):
    global line
    if key == "backspace" and len(para[0]) > 0:
        para[line] = para[line][:-1]
        if len(para[line]) == 0 and line > 0:
            line -= 1
    if key == "space":
        para[line] += " "

    if len(key) == 1:  # valid key
        cur_word = para[line].split(" ")[-1]

        if len(para[line] + cur_word) > 40:
            para[line] = para[line][:-len(cur_word)]
            para.append("")
            line += 1
            para[line] += cur_word

        if len(para[line]) + 1 >= 40:
            para.append("")
            line += 1

        para[line] += key
        para[line] = para[line].upper()


class Type_Speed():
    def __init__(self):
        self.wd_count = 0
        self.wd = ""
        self.List = [[]]
        self.line = 0
        self.prev_line = ""
        self.prop = [[]]
        self.wrong_letter = 0
        self.start = datetime.now().time()
        self.time = ""
        self.analyze = {"correct": 0, "wrong": 0, "estimated speed": 0}

    def form(self, k):
        if self.List[self.line] == paragraph[self.line].split(" ")[:-1]:
            self.List.append([])
            self.prop.append([])
            self.line += 1
            self.wd_count = 0
            self.prev_line = ""
        if k == "space":
            word = paragraph[self.line].split(" ")[self.wd_count]
            self.List[self.line].append(word)

            if len(self.List[self.line]) <= 1:
                self.prev_line = ""
            else:
                self.prev_line += self.List[self.line][self.wd_count - 1] + " "
            # print(self.prev_line, font.render(self.prev_line, 1, (0, 0, 0)).get_width(), self.List)

            x = 0.2 * w + font.render(self.prev_line, 1, (0, 0, 0)).get_width()
            y = 0.2 * h + 20 * self.line
            if self.wd.upper() == word:
                clr = (0, 200, 0)
                self.analyze["correct"] += 1
            else:
                clr = (200, 0, 0)
                self.analyze["wrong"] += 1
            self.prop[self.line].append([clr, (x, y)])

            self.wd = ""
            self.wd_count += 1
        elif k == "backspace":
            self.wd = self.wd[:-1]
        else:
            self.wd += k

    def draw(self):
        for line in range(self.line + 1):
            for wd in self.List[line]:
                i = self.List[line].index(wd)
                txt = font.render(wd, 1, self.prop[line][i][0])
                win.blit(txt, self.prop[line][i][1])

    def calc(self):
        self.time = str(
            datetime.combine(datetime.today(), datetime.now().time()) - datetime.combine(datetime.today(), self.start))[
                    0:7]

        min = int(self.time[2:4])
        sec = int(self.time[5:])

        if sec == 5:
            self.finished()

    def finished(self):
        self.analyze["estimated speed"] = self.analyze["correct"] + self.analyze["wrong"] / 2
        i = 0
        for k, v in self.analyze.items():
            print(k, v)
            i += 1
            txt = font.render(k.upper() + " : " + str(v), 1, (0, 200, 0))
            win.blit(txt, (0, 50 + i * 20))
        win.blit(font.render("PRESS ANY KEY TO CONTINUE", 1, (0, 0, 200)), (0, 150))
        pygame.display.update()

        n = True
        while n:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    n = False
                clock.tick(5)

        pygame.time.delay(3000)
        self.__init__()


def interface():
    global wd
    para_win = (0.2 * w, 0.2 * h, 0.8 * w - 0.2 * w, 200)
    text_box = (0.4 * w, 0.7 * h, 200, 50)

    pygame.draw.rect(win, (200, 0, 0), para_win, 2)
    pygame.draw.rect(win, (0, 200, 0), text_box, 2)

    for line in paragraph:
        txt = font.render(line, 1, (255, 255, 255))
        win.blit(txt, (0.2 * w, 0.2 * h + paragraph.index(line) * 20))

    txt = font.render(wd, 1, (0, 255, 0))
    win.blit(txt, text_box[:2])


def refresh_win():
    win.fill((0, 0, 0))

    txt = font_heading.render("TYPING SPEED TEST", 1, (200, 0, 200))
    win.blit(txt, (0.25 * w, 0.1 * h))

    win.blit(font.render("Time Taken: " + type_speed.time, 1, (200, 200, 20)), (0, 0))

    if text_mode:
        pygame.draw.rect(win, (200, 0, 0), (0.2 * w, 0.2 * h, 500, 500), 3)
        for Line in para:
            if para.index(Line) == line:
                Line += "|"
                txt = font.render(Line, 1, (0, 200, 100))
                win.blit(txt, (0.2 * w, 0.2 * h + para.index(Line[:-1]) * 20))
            else:
                txt = font.render(Line, 1, (0, 200, 100))
                win.blit(txt, (0.2 * w, 0.2 * h + para.index(Line) * 20))

    if not text_mode:
        interface()
        type_speed.calc()
        type_speed.draw()
        # for wd in type_speed.List[type_speed.line]:
        #     i = type_speed.List[type_speed.line].index(wd)
        #     txt = font.render(wd, 1, type_speed.prop[type_speed.line][i][0])
        #     win.blit(txt, type_speed.prop[type_speed.line][i][1])

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
                if text_mode:
                    text_mode = False
                    type_speed.__init__()
                else:
                    text_mode = True

            if key == "escape":
                run = False

            if text_mode:
                Text_mode(key)
            else:
                type_speed.form(key)
                if key == "space":
                    wd = ""
                elif key == "backspace" and len(wd) > 0:
                    wd = wd[:-1]
                elif len(key) == 1:
                    wd += key.upper()

    refresh_win()

pygame.quit()
