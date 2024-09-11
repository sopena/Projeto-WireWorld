import pyxel as px
from bloco import Bloco

class Tela:
    def __init__(self, q_largura, q_altura, lado, cor_grade):
        self.q_largura = q_largura 
        self.q_altura = q_altura 
        self.lado = lado
        self.cor_grade = cor_grade
        self.largura = q_largura*lado
        self.altura =  q_altura*lado

        self.grade = [["0" for i in range(self.q_largura)] for j in range(self.q_altura)]
        self.prox_grade = [["0" for i in range(self.q_largura)] for j in range(self.q_altura)]
        
    def update_grade(self):
        pass
    

    def desenhar_grade(self):

        # Desenha cada bloco na grade da tela
        for i in range(len(self.grade)):
            for j in range(len(self.grade[i])):
                if self.grade[i][j] == "0":
                    px.rect((self.lado*j), self.lado*i, self.lado, self.lado, 0)
                if self.grade[i][j] == "1":
                    px.rect((self.lado*j), self.lado*i, self.lado, self.lado, 5)
                if self.grade[i][j] == "2":
                    px.rect((self.lado*j), self.lado*i, self.lado, self.lado, 7)
                if self.grade[i][j] == "3":
                    px.rect((self.lado*j), self.lado*i, self.lado, self.lado, 9)
        
        # Desenha a Grade da matriz na tela
        for col in range(self.q_largura):
            px.line(col*self.lado, 0, col*self.lado, self.altura, self.cor_grade)
        for lin in range(self.q_altura+1):
            px.line(0, lin*self.lado, self.largura, lin*self.lado, self.cor_grade)