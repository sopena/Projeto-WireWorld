import pyxel as px
import globals

class Bloco:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo

        if self.tipo == "0":
            self.cor_peca = "0"
        if self.tipo == "1":
            self.cor_peca = "5"
        if self.tipo == "2":
            self.cor_peca = "7"
        if self.tipo == "3":
            self.cor_peca = "9"
    
    