from random import randint, sample
import sys
from copy import deepcopy
sys.setrecursionlimit(10000)
#import timon

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
        self.model = deepcopy(self.grille) #ne pas toucher le modele ! Il servira pour la réinitialisation
        self.shuffle_laby(self.nbShuffles)
        while deepcopy(self).verificate_path(0,0)>0:
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

    #index de 1 à width ou height
    def move_direction(self, direction, index):
        if direction == 'R':
            if index<0:
                x = -index-1
                row = self.grille[x][1:]+[self.grille[x][0]]
                self.grille[x] = row
            else:
                x = index-1
                row = [self.grille[x][-1]] + self.grille[x][:-1]
                self.grille[x] = row
            for x_new, obj in enumerate(row):
                obj.x = x_new
        elif direction=='C':
            column = []
            if index<0:
                y = -index-1
                for row in self.grille:
                    column.append(row[y])
                column = column[1:]+[column[0]]
            else:
                y = index-1
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
                index = randint(1, self.height)
            else:
                index = randint(1, self.width)
            if index == forbidden:
                index = -index
            self.move_direction(direction, index)
            forbidden = -index

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

essai = labyrinth(11, 11, 4)
print(essai)
print('\n'*5)
print(essai.model)
