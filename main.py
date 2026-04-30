from random import randint, sample
import sys
from copy import deepcopy
sys.setrecursionlimit(10000)

class cell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        symbols = {'PATH':'.', 'WALL':'#', 'BLOCK':'%', 'START':'S','FINISH':'F'}
        return symbols[self.type]
    
    def __str__(self):
        return f'({self.x};{self.y}):{self.type}'

class labyrinth:
    def __init__(self, height, width, level):
        self.height = height
        self.width = width
        self.nbShuffles = level
        self.grille = [[cell(x, y, 'WALL') for x in range(width)] for y in range(height)]
        self.generate_laby(0,0)
        self.grille[0][0].type, self.grille[height-1][width-1].type = ('START','FINISH')
        self.shuffle_laby(self.nbShuffles)

    def __str__(self):
        return '\n'.join([''.join([repr(i) for i in j]) for j in self.grille])

    def generate_laby(self, posX, posY):
        self.grille[posY][posX].type = 'PATH'
        if (posX,posY)==(self.width-1, self.height-1):
            return
        deltas = [(2,0),(-2,0),(0,2),(0,-2)]
        unvisited = [delta for delta in deltas if 0<=posY+delta[1]<self.height and 0<=posX+delta[0]<self.width and self.grille[posY+delta[1]][posX+delta[0]].type=='WALL']
        if unvisited:
            unvisited_chosen = sample(unvisited, randint(1,len(unvisited)))
            for delta_chosen in unvisited_chosen:
                if self.grille[posY+delta_chosen[1]][posX+delta_chosen[0]].type == 'WALL':
                    self.grille[posY + delta_chosen[1]//2][posX + delta_chosen[0]//2].type = 'PATH'
                    self.generate_laby(posX+delta_chosen[0], posY+delta_chosen[1])

    def move_row_column(self, row_column, x, y):
        if row_column == 'R':
            if x==self.width-1:
                a = self.grille[y][x]
                b = self.grille[y][:x-1]
            else:
                a = self.grille[y][x]
                b = self.grille[y][x+1:]
        else:
            pass
        return 

    def shuffle_laby(self, nbShuffles):
        movements = ['R','C']
        last_done = None
        for _ in range(nbShuffles):
            self.move_row_column(sample(movements, 1), randint(self.width), randint(self.height))
            last_done = 


    #ne pas oublier de faire un deepcopy avant d'appeler la fonction
    def verificate_path(self, lig, col):
        delta = [(-1,0),(1,0),(0,-1),(0,1)]

        self.grille[lig][col] = 'o'
        nbChemins = 0
        for dx,dy in delta:
            x = lig + dx
            y = col + dy
            case = self.grille[x][y]
            if case.type == 'S':
                nbChemins += 1
            elif case.type == '.':
                nbChemins += self.verificate_path(x,y)
        self.grille[lig][col] = '.'
        return nbChemins

    def verificate_all_connected(self):
        pass

essai = labyrinth(21, 21, 3)
print(essai)