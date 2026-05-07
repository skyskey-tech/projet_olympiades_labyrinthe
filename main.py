import sys
sys.setrecursionlimit(10000)

from random import randint, sample
from copy import deepcopy
import timon
from lib_pattern import pattern, patterns

symbols = {'PATH': '.', 'WALL': '#', 'DRAWING': '%', 'START': 'S', 'FINISH': 'F', 'VISITED': 'o'}


class cell:
    def __init__(self, x: int, y: int, type: str):
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        return symbols[self.type]

    def __str__(self):
        return f'({self.x};{self.y}):{self.type}'


class labyrinth:
    def __init__(self, height: int, width: int, level: int):
        self.height = height
        self.width = width
        self.nbShuffles = level
        self.grille = [[cell(x, y, 'WALL') for x in range(width)] for y in range(height)]
        self.pattern_chosen = None
        if level >= 0 and randint(0, 2) == 0:
            self.pattern_chosen = self.add_pattern()
        self.generate_laby(0, 0)
        self.grille[0][0].type, self.grille[height - 1][width - 1].type = ('START', 'FINISH')
        self.shuffle_laby(self.nbShuffles)
        while level > 0 and deepcopy(self).verificate_path(0, 0) > 0:
            self.shuffle_laby(self.nbShuffles)
        self.model = deepcopy(self.grille)

    def __str__(self):
        return '\n'.join([''.join([repr(i) for i in j]) for j in self.grille])

    def add_pattern(self):
        max_size = min(self.width - 10, self.height - 10)
        usable_patterns = [d for d in patterns if d.size <= max_size]
        if usable_patterns:
            p = sample(usable_patterns, 1)[0]
            x_corner = randint(1, max(2, self.width  - 2 - p.size))
            y_corner = randint(1, max(2, self.height - 2 - p.size))
            sym_inv = {'#': 'WALL', '%': 'DRAWING'}
            for y, row in enumerate(p.drawing):
                for x, ch in enumerate(row):
                    self.grille[y_corner + y][x_corner + x].type = sym_inv[ch]
            return p
        return None

    def generate_laby(self, posX, posY):
        self.grille[posY][posX].type = 'PATH'
        if (posX, posY) == (self.width - 1, self.height - 1):
            return
        deltas = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        unvisited = [
            d for d in deltas
            if 0 <= posY + d[1] < self.height
            and 0 <= posX + d[0] < self.width
            and self.grille[posY + d[1]][posX + d[0]].type == 'WALL'
            and self.grille[posY + d[1] // 2][posX + d[0] // 2].type != 'DRAWING'
        ]
        if unvisited:
            for delta in sample(unvisited, randint(1, len(unvisited))):
                if self.grille[posY + delta[1]][posX + delta[0]].type == 'WALL':
                    self.grille[posY + delta[1] // 2][posX + delta[0] // 2].type = 'PATH'
                    self.generate_laby(posX + delta[0], posY + delta[1])

    def move_direction(self, direction, index):
        for _ in range(2):
            if direction == 'R':
                x = abs(index)
                if index < 0:
                    row = self.grille[x][1:] + [self.grille[x][0]]
                else:
                    row = [self.grille[x][-1]] + self.grille[x][:-1]
                self.grille[x] = row
                for x_new, obj in enumerate(row):
                    obj.x = x_new
            elif direction == 'C':
                y = abs(index)
                column = [row[y] for row in self.grille]
                if index < 0:
                    column = column[1:] + [column[0]]
                else:
                    column = [column[-1]] + column[:-1]
                for i, row in enumerate(self.grille):
                    row[y] = column[i]
                for y_new, obj in enumerate(column):
                    obj.y = y_new

    def shuffle_laby(self, nbShuffles):
        forbidden = None
        for _ in range(nbShuffles):
            direction = sample(['R', 'C'], 1)[0]
            index = randint(1, self.height - 2) if direction == 'R' else randint(1, self.width - 2)
            if index == forbidden:
                index = -index
            self.move_direction(direction, index)
            forbidden = -index

    def verificate_path(self, lig=0, col=0):
        delta = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.grille[lig][col].type = 'VISITED'
        nbChemins = 0
        for dx, dy in delta:
            x, y = lig + dx, col + dy
            if 0 <= x < self.height and 0 <= y < self.width:
                case = self.grille[x][y]
                if case.type == 'FINISH':
                    nbChemins += 1
                elif case.type == 'PATH':
                    nbChemins += self.verificate_path(x, y)
        self.grille[lig][col].type = 'PATH'
        return nbChemins


# Lance le menu → le joueur choisit taille et difficulté
timon.launch_menu(labyrinth)
