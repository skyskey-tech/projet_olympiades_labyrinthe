from random import randint, sample
import sys
from copy import deepcopy
sys.setrecursionlimit(10000)
import timon
from lib_pattern import pattern, patterns

symbols = {'PATH':'.', 'WALL':'#', 'DRAWING':'%', 'START':'S','FINISH':'F', 'VISITED':'o'}

class cell:
    def __init__(self, x:int, y:int, type:str):
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        return symbols[self.type]
    
    def __str__(self):
        return f'({self.x};{self.y}):{self.type}'

class labyrinth:
    def __init__(self, height:int, width:int, level:int):
        self.height = height
        self.width = width
        self.nbShuffles = level
        self.grille = [[cell(x, y, 'WALL') for x in range(width)] for y in range(height)]
        if level>=10 and randint(0,2)==0:
            self.add_pattern()  
        self.generate_laby(0,0)
        self.grille[0][0].type, self.grille[height-1][width-1].type = ('START','FINISH')
        self.shuffle_laby(self.nbShuffles)
        while level>0 and deepcopy(self).verificate_path(0,0)>0:
            self.shuffle_laby(self.nbShuffles)
        self.model = deepcopy(self.grille) #ne pas toucher le modele ! Il servira pour la réinitialisation

    def __str__(self):
        return '\n'.join([''.join([repr(i) for i in j]) for j in self.grille])

    def add_pattern(self):
        max_size = min(self.width-10, self.height-10)
        usable_patterns = [drawing for drawing in patterns if drawing.size<=max_size]
        if usable_patterns:
            pattern_chosen = sample(usable_patterns, 1)[0]
            x_corner = randint(1, max(2,self.width-2-pattern_chosen.size))
            y_corner = randint(1, max(2, self.height-2-pattern_chosen.size))
            symbols_inversed = {'#':'WALL', '%':'DRAWING'}
            for y, i in enumerate(pattern_chosen.drawing):
                for x, j in enumerate(i):
                    self.grille[y_corner+y][x_corner+x].type = symbols_inversed[j]
        return


    def generate_laby(self, posX, posY):
        self.grille[posY][posX].type = 'PATH'
        if (posX,posY)==(self.width-1, self.height-1):
            return
        deltas = [(2,0),(-2,0),(0,2),(0,-2)]
        unvisited = [delta for delta in deltas if 0<=posY+delta[1]<self.height and 0<=posX+delta[0]<self.width and self.grille[posY+delta[1]][posX+delta[0]].type=='WALL' and self.grille[posY+delta[1]//2][posX+delta[0]//2].type!='DRAWING']
        if unvisited:
            unvisited_chosen = sample(unvisited, randint(1,len(unvisited)))
            for delta_chosen in unvisited_chosen:
                if self.grille[posY+delta_chosen[1]][posX+delta_chosen[0]].type == 'WALL':
                    self.grille[posY + delta_chosen[1]//2][posX + delta_chosen[0]//2].type = 'PATH'
                    self.generate_laby(posX+delta_chosen[0], posY+delta_chosen[1])

    #index de 1 à width ou height
    def move_direction(self, direction, index):
        for _ in range(2):
            if direction == 'R':
                if index<0:
                    x = -index
                    row = self.grille[x][1:]+[self.grille[x][0]]
                    self.grille[x] = row
                else:
                    x = index
                    row = [self.grille[x][-1]] + self.grille[x][:-1]
                    self.grille[x] = row
                for x_new, obj in enumerate(row):
                    obj.x = x_new
            elif direction=='C':
                column = []
                if index<0:
                    y = -index
                    for row in self.grille:
                        column.append(row[y])
                    column = column[1:]+[column[0]]
                else:
                    y = index
                    for row in self.grille:
                        column.append(row[y])
                    column = [column[-1]] + column[:-1]

                for i, row in enumerate(self.grille):
                    row[y] = column[i]
                    
                for y_new, obj in enumerate(column):
                    obj.y = y_new
        return
        
    def shuffle_laby(self, nbShuffles):
        movements = ['R','C']
        forbidden = None #pour éviter d'annuler un mouvement
        for _ in range(nbShuffles):
            direction = sample(['R', 'C'], 1)[0]
            if direction == 'R':
                index = randint(1, self.height-2)
            else:
                index = randint(1, self.width-2)
            if index == forbidden:
                index = -index
            self.move_direction(direction, index)
            forbidden = -index
        return

    #ne pas oublier de faire un deepcopy avant d'appeler la fonction
    def verificate_path(self, lig=0, col=0):
        delta = [(-1,0),(1,0),(0,-1),(0,1)]

        self.grille[lig][col].type = 'VISITED'
        nbChemins = 0
        for dx,dy in delta:
            x = lig + dx
            y = col + dy
            if 0<=x<self.height and 0<=y<self.width:
                case = self.grille[x][y]
                if case.type == 'FINISH':
                    nbChemins += 1
                elif case.type == 'PATH':
                    nbChemins += self.verificate_path(x,y)
        self.grille[lig][col].type = 'PATH'
        return nbChemins

    def verificate_all_connected(self):
        pass

'''
def lancer_partie(height:int,width:int,level:int):
    essai = labyrinth(height, width, level)
    print(essai)
    nb = 0
    while nb <essai.nbShuffles:
        print(f'il reste : {essai.nbShuffles} essai(s)')
        command = sys.stdin.readline().split()
        if command[0] == 'S':
            print('Vous avez arrêté la partie.')
            return
        if command[0]=='Re':
            nb=-1
            essai.grille = essai.model
        else:
            essai.move_direction(command[0], int(command[1]))
            print(essai)
        
        if essai.verificate_path()>0:
            print('Vous avez réussi !')
        nb+= 1

lancer_partie(9,9,2)
'''
essai = labyrinth(25, 25, 1)
timon.launch_game(essai)