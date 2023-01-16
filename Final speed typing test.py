import datetime as dt
import os
import random
import sys
from collections import defaultdict

from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from accessories import *

pygame.init()

w, h = 850, 600
win = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Typing Speed Test")

Font_heading = pygame.font.SysFont('algerian', 60)
Font_text = pygame.font.SysFont('comic sans', 30)
Font_status_bar = pygame.font.SysFont('jetbrains mono', 25)

fps = 20


def init():
    global para, typed_para, line_no, letter_no, capitalize, evaluation, start_time, time_elapsed, speed_list, start, graph_gen_timer, graph_list

    para = defaultdict(str)
    typed_para = defaultdict(str)
    line_no = 0
    letter_no = 0
    capitalize = False
    evaluation = {'correct': 0,
                  'wrong': 0,
                  'word_count': 0}
    speed_list = []
    start_time = dt.datetime.now()
    time_elapsed = dt.datetime
    start = False
    graph_gen_timer = 0
    graph_list = []


init()

clock = pygame.time.Clock()


# datapath = os.path.join('data', 'wordlist.txt')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


with open(resource_path('data/wordlist.txt'), 'r') as wds:
    for wd in wds:
        wdlist = wd.split("|")


def construct_sentences():
    global para, typed_para
    no_of_lines = h // 100
    print(no_of_lines)
    for i in range(no_of_lines):
        typed_para[i] = ''
        rendered_text = Font_text.render(para[i], True, (0, 0, 0))
        while rendered_text.get_width() < 0.8 * w:
            para[i] += random.choice(wdlist) + ' '
            rendered_text = Font_text.render(para[i], True, (0, 0, 0))
        para[i] = para[i][:para[i][:-1].rfind(' ')] + ' '

    typed_para[0] += '_'
    # print(*para.values(), sep='\n')


construct_sentences()


def reset_screen():
    init()
    construct_sentences()


def display_graph():
    global graph_list

    rel_x = 0.5 * w
    rel_y = 0.6 * h

    width = w - rel_x
    height = h - rel_y

    pygame.draw.rect(win, (255, 255, 255), (rel_x, rel_y, width, height))
    pygame.draw.rect(win, (200, 0, 0), (rel_x, rel_y, width, height), 2)

    graphpos = []

    for i in range(len(graph_list)):
        xpos = rel_x + i * 25
        ypos = h - (graph_list[i]/100) * height
        graphpos.append((xpos, ypos))

    if len(graph_list) > 1:
        pygame.draw.lines(win, (200, 0, 0), False, graphpos, 2)

    text = Font_status_bar.render('100WPM', True, (0, 0, 0))
    win.blit(text, (0.5 * w, rel_y))
    text = Font_status_bar.render('50WPM', True, (0, 0, 0))
    win.blit(text, (0.5 * w, rel_y + height//2))

    pygame.draw.line(win, (200, 0, 200), (0.5 * w, rel_y + height//2), (w, rel_y + height//2))

    for i in range(0, 25):
        pygame.draw.line(win, (200, 0, 100), (rel_x + i * width/25, rel_y), (rel_x + i * width/25, h), 1)

    if len(graph_list) * 25 > 0.5 * w + 1:
        graph_list.pop(0)


def display_text():
    global Font_text
    for i in para.keys():
        if i >= 0:
            text = Font_text.render(para[i], True, (0, 0, 0))
            win.blit(text, (0.1 * w, 0.1 * h + i * 30))
            text_typed = Font_text.render(typed_para[i], True, (0, 255, 0))
            win.blit(text_typed, (0.1 * w, 0.1 * h + i * 30))


def generateline():
    txt = ''
    rendered_text = Font_text.render(txt, True, (0, 0, 0))
    while rendered_text.get_width() < 0.8 * w:
        txt += random.choice(wdlist) + ' '
        rendered_text = Font_text.render(txt, True, (0, 0, 0))
    txt = txt[:txt[:-1].rfind(' ')] + ' '
    return txt


def move_lines():
    global para, typed_para
    tempdict = defaultdict(str)
    for i in para.keys():
        tempdict[i - 1] = para[i]
    para = tempdict
    para[i] = generateline()

    tempdict = defaultdict(str)
    for i in typed_para.keys():
        tempdict[i - 1] = typed_para[i]
    typed_para = tempdict


def status_bar():
    # HEADING
    global Font_heading, Font_status_bar, time_elapsed, start_time

    pygame.draw.rect(win, (0, 0, 0), (0, 0, w, 0.1 * h))
    text = Font_heading.render("SPEED TYPER", True, (250, 0, 50))
    win.blit(text, (0.5 * w - text.get_width() // 2, 5))

    # STATUS PANEL

    pygame.draw.rect(win, (0, 0, 0), (0, 0.6 * h, w, 0.4 * h))
    pygame.draw.rect(win, (0, 100, 100), (0, 0.6 * h, w, 0.4 * h), 2)

    if not start:
        # text = Font_status_bar.render("To Begin, start_button Typing", True, (250, 200, 50))
        # win.blit(text, (0.5 * w - text.get_width() // 2, 0.8 * h))
        start_time = dt.datetime.now()

        # return None

    text = Font_status_bar.render(f"Correct: {evaluation['correct']}", True, (0, 255, 0))
    win.blit(text, (0.2 * w, 0.7 * h))
    text = Font_status_bar.render(f"Wrong: {evaluation['wrong']}", True, (255, 0, 0))
    win.blit(text, (0.2 * w, 0.75 * h))

    if evaluation['correct'] + evaluation['wrong'] != 0:
        acc = (evaluation['correct'] / (evaluation['correct'] + evaluation['wrong'])) * 100
    else:
        acc = '_'
    text = Font_status_bar.render(f"Accuracy: {str(acc)[:4]}%", True, (255, 255, 255))
    win.blit(text, (0.2 * w, 0.9 * h))

    time_elapsed = dt.datetime.now() - start_time
    text = Font_status_bar.render(f"Time elapsed: {str(time_elapsed)[:7]}", True, (250, 150, 0))
    win.blit(text, (0.2 * w, 0.95 * h))

    if time_elapsed.seconds > 0:
        speed = evaluation['word_count'] / (time_elapsed.seconds / 60)
    else:
        speed = 0
    text = Font_status_bar.render(f"Speed: {speed}", True, (250, 150, 0))
    win.blit(text, (0.2 * w, 0.6 * h))

    display_graph()


def redraw_window():
    global w, h, letter_no, line_no, para, typed_para, capitalize, key, graph_gen_timer, graph_list, evaluation
    win.fill((0, 200, 200))

    pygame.draw.rect(win, (255, 255, 255), (0.1 * w, 0.1 * h, 0.8 * w, 0.4 * h))
    pygame.draw.rect(win, (0, 0, 0), (0.1 * w, 0.1 * h, 0.8 * w, 0.4 * h), 3)
    display_text()
    status_bar()
    start_button.draw()

    if start:
        if graph_gen_timer == 20 and time_elapsed.seconds != 0:
            graph_list.append(evaluation['word_count'] / (time_elapsed.seconds / 60))
            graph_gen_timer = 0
        else:
            graph_gen_timer += 1
        start_button.update_state(state="OFF")

    if key is not None and len(key) == 1:
        if para[line_no][letter_no] == key or (capitalize and para[line_no][letter_no] == key.upper()):
            evaluation['correct'] += 1
            capitalize = False
            typed_para[line_no] = typed_para[line_no][:-1]
            typed_para[line_no] += para[line_no][letter_no] + "_"
            # print(typed_para[line_no])
            if key == " ":
                evaluation['word_count'] += 1
            if len(para[line_no]) != letter_no + 1:
                letter_no += 1
            else:
                typed_para[line_no] = typed_para[line_no][:-1]
                line_no += 1
                letter_no = 0
                typed_para[line_no] = "_"
                if line_no == 2:
                    move_lines()
                    line_no -= 1
        else:
            pygame.draw.rect(win, (200, 0, 0), (0.1 * w, 0.1 * h, 0.8 * w, 0.4 * h), 3)
            evaluation['wrong'] += 1

    pygame.display.update()


run = True
start_button = Button(win, 0.4 * w, 0.5 * h, "Start", "Reset", 30)
while run:
    clock.tick(fps)
    key = None
    for event in pygame.event.get(pump=True):
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            w = win.get_width()
            h = win.get_height()
            pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
            reset_screen()
        if event.type == pygame.KEYDOWN:
            key = str(pygame.key.name(event.key))
            start = True

            if key == "escape":
                run = False

            if key == "space":
                key = " "

            if bool(key.count("shift")):
                key = "shift"
                capitalize = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if start_button.rect.collidepoint(pos):
                if start:
                    start = False
                    start_button.update_state("ON")
                    reset_screen()
                else:
                    start = True
                    start_button.update_state("OFF")
                # start, start_button.state = False, "OFF" if start else True, "ON"
            # print(key, end=', ')

    redraw_window()
