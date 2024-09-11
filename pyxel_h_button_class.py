import pyxel as px
import globals

def hit_point_box(x1, y1, x2, y2, w2, h2):
    return (x2 <= x1 < x2 + w2) and (y2 <= y1 < y2 + h2)

class Button:
    def __init__(self, x, y, label, callback, col):
        self.x, self.y = x, y
        self.col = col
        self.label = label
        self.callback = callback
        self.pressed = False

    def draw(self):
        x, y, w, h = self.x, self.y, globals.lado, globals.lado  
        px.rect(x, y, w, h, self.col) # background color
        if px.btnp(px.MOUSE_BUTTON_LEFT) and hit_point_box(px.mouse_x, px.mouse_y, x, y, w, h):
            px.rect(x, y, w, h, 10) # highlight (clicked) color
            self.callback()
        




def update():
    pass

def draw():
    pass
