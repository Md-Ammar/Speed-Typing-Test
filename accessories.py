import pygame

class Button(object):
    def __init__(self, win, x, y, on_text, off_text, font_size):
        self.x = x
        self.y = y
        self.win = win
        self.on_text = on_text
        self.off_text = off_text
        self.text = on_text
        self.state = "ON"
        self.font = pygame.font.SysFont("Comicsans", font_size)
        self.color = (0, 200, 0)
        self.rect = pygame.Rect

    def update_state(self, state):
        self.state = state
        self.color = (0, 200, 0) if self.state == "ON" else (200, 0, 0)
        self.text = self.on_text if self.state == "ON" else self.off_text

    def draw(self):
        text = self.font.render(self.text, True, self.color)
        w, h = text.get_width(), text.get_height()
        self.rect = pygame.Rect(self.x, self.y, w, h)
        pygame.draw.rect(self.win, (0, 0, 0), (self.x, self.y, w, h))
        pygame.draw.rect(self.win, self.color, (self.x, self.y, w, h), 1)
        self.win.blit(text, (self.x, self.y))


