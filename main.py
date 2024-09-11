import pyxel as px
import globals
from tela import Tela
from bloco import Bloco
import pyxel_h_button_class as pb

class App:
    def __init__(self, path):

        self.path = path
        self.t = Tela(globals.q_largura, globals.q_altura, globals.lado, 13)
        self.blocos = []
        self.play = False
        self.generation = 0
        self.selected_block = "3"
        self.popula = 0

        self.b1 = pb.Button(130, self.t.altura+1,  ' ', self.b1_press, 5) 
        self.b2 = pb.Button(140, self.t.altura+1,  ' ', self.b2_press, 7)
        self.b3 = pb.Button(150, self.t.altura+1,  ' ', self.b3_press, 9)
        self.moldura_x = 150
        

        self.limpar_path()
        if not(self.path == ''):
            self.load_file()

        px.init(self.t.largura , self.t.altura + globals.lado, title='WorldWire', fps=30)
        px.run(self.update, self.draw)
    
    def limpar_path(self):
        self.path.replace("\\", "/")                # Troca as barras invertidas pelas barras corretas para leitura do arquivo
        
    
    def load_file(self):
        f = list(open(self.path, "r"))
        print(f)
        print("-"*100)
        f = [s.rstrip() for s in f]                 # Remove qualquer espaço em branco no final da string
        lf = [_str.split(' ') for _str in f]        # Divide uma string em uma lista
        print(lf)
        
        for x in range(len(lf)):
            for y in range(len(lf)):
                self.t.grade[x][y] = lf[x][y] # Carrega os dados da matriz do arquivo na matriz da tela            
        print("-"*100)
        print(self.t.grade)
        self.population()

    # Pega algum valor da matriz
    def get(self, x, y,):
        return self.t.grade[x % globals.q_largura][y % globals.q_altura]
    
    # Coloca um valor na matriz
    def put(self, x, y, b):
        self.t.prox_grade[x][y] = b
    
    # Detecta a quantidade de vizinhos que são Electrons
    def vizinhos(self, x, y):
        neighbors = [self.get(x-1, y-1), self.get(x, y-1), self.get(x+1, y-1), self.get(x-1, y), self.get(x+1, y), self.get(x-1, y+1), self.get(x, y+1), self.get(x+1, y+1)]
        s = 0
        for j in neighbors:
            if j == "1":
                s += 1
        return s

    # Play e Pause
    def playing(self):
        return not(self.play)
    
    def rodando(self):
        for x in range(0, globals.q_largura):
            for y in range(0, globals.q_altura):
                soma_vizinhos = str(self.vizinhos(x, y))
                    
                if self.get(x, y) == "0": #empty -> empty
                    self.put(x, y, "0") 
                if self.get(x, y) == "1": #Electron Head -> Electron Tail
                    self.put(x, y, "2")
                if self.get(x, y) == "2": #Electron Tail -> Connector
                    self.put(x, y, "3")
                if self.get(x, y) == "3": # Connector
                    if soma_vizinhos <= "2" and soma_vizinhos > "0":
                        self.put(x, y, "1")
                    else:
                        self.put(x, y, "3")
        # troca o valor das matrizes                
        self.t.grade, self.t.prox_grade = self.t.prox_grade, self.t.grade
        self.generation += 1
        

    # Add blocos na matriz e incrementa em 1 o numero da população
    def add_bloco(self):
        if px.mouse_x < self.t.altura and px.mouse_y < self.t.largura:
            if self.t.grade[px.mouse_y//globals.lado][px.mouse_x//globals.lado] == "0":
                self.blocos.append(Bloco(px.mouse_x, px.mouse_y, self.selected_block))
                self.t.grade[px.mouse_y//globals.lado][px.mouse_x//globals.lado] = self.selected_block
                if self.t.grade[px.mouse_y//globals.lado][px.mouse_x//globals.lado] != "0":
                    self.popula += 1
            self.blocos.append(Bloco(px.mouse_x, px.mouse_y, self.selected_block))
            self.t.grade[px.mouse_y//globals.lado][px.mouse_x//globals.lado] = self.selected_block
        
    # Remove Blocos da matriz e decrementa em 1 o número da população
    def remove_bloco(self):
        if px.mouse_x < self.t.altura and px.mouse_y < self.t.largura:
            if self.t.grade[px.mouse_y//globals.lado][px.mouse_x//globals.lado] != "0":
                self.popula -= 1
            self.t.grade[px.mouse_y//globals.lado][px.mouse_x//globals.lado] = "0"
        print(self.popula)

    # Funções que detectam qual cor de bloco foi selecionada   
    def b1_press(self):
        self.selected_block = "1"
        self.moldura_x = 130
    def b2_press(self): 
        self.selected_block = "2"
        self.moldura_x = 140
    def b3_press(self): 
        self.selected_block = "3"
        self.moldura_x = 150
    
    # Calcula a população que está no arquivo de estado inicial
    def population(self):
        t = 0
        for x in range(len(self.t.grade)):
            for y in range(len(self.t.grade)):
                if self.t.grade[x][y] != "0":
                    t +=1
        self.popula +=t
    
    def save(self):
        name_file = input("Digite o nome do arquivo para salva-lo: ")
        name_file = name_file+'.txt'
        new_file = open(name_file, "x")        
        matriz = []

        print("-"*100)
        for group in self.t.grade:
            matriz.append((" ".join(group))+'\n')
        print(matriz)

        for x in range(len(matriz)):
            new_file.write(matriz[x])

        
    def update(self):
        px.mouse(True)

        # RESET
        if px.btnp(px.KEY_R): 
            self.load_file()

        if px.btnp(px.KEY_RETURN):
            self.play = self.playing()
        
        # Cria um bloco e adiciona na matriz da tela
        if px.btn(px.MOUSE_BUTTON_LEFT):
            self.add_bloco()
        
        # Apaga um bloco da tela e da matriz
        if px.btn(px.MOUSE_BUTTON_RIGHT):
            self.remove_bloco()

        # PLAY AND PAUSE
        if self.play:
            self.rodando() 

        # STEP BY STEP
        if not(self.play):
            if px.btnp(px.KEY_SPACE): 
                self.rodando()
        
        if px.btnp(px.KEY_S):
            self.save()

    def draw(self):
        px.cls(0)
        self.t.desenhar_grade()
        px.text(0, self.t.altura+3, f'GENERATIONS: {self.generation}', 7)
        px.text(100, self.t.altura+3, f'COLORS: ', 7)
        self.b1.draw()
        self.b2.draw()
        self.b3.draw()
        px.rectb(self.moldura_x, self.t.altura+1, globals.lado, globals.lado, 12)
        px.text(180, self.t.altura+3, f'ERASER: MOUSE RIGHT BUTTON', 7)
        px.text(300, self.t.altura+3, f'POPULATION: {self.popula}', 7)



menu = True
while menu:
    print('-'*40)
    ask_file = input('SEJA BEM-VINDO AO WIREWORLD! \n\n0 - SAIR\n1 - EM BRANCO\n2 - CARREGAR ARQUIVO\n\nESCOLHA UMA OPÇÃO PARA COMEÇAR: ')

    if ask_file == "0":
        print('Fechando...')
        menu = False
    elif ask_file == "1":
        path = ""
        App(path)
    elif ask_file == "2":
        print("\nMARAVILHA!\n")
        print('-'*40)
        path = input("COPIE E COLE O CAMINHO DO ARQUIVO.TXT AQUI: ")
        print('-'*40)
        App(path)
    else:
        print('\n\n')
        print("NENHUMA OPÇÃO ENCONTRADA! TENTE NOVAMENTE.")
