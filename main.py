class cell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        symbols = {'PATH':'.', 'WALL':'#', 'BLOCK':'%'}
        return symbols[self.type]
    
    def __str__(self):
        return self.type

class labyrinth:
    def __init__(self, height, width, level):
        self.height = height
        self.width = width
        self.nbShuffle = level
        self.grille = [[cell(x, y) for x in range(width)] for y in range(height)]
        self.base = self.generate_laby()
        self.shuffled = self.shuffle_laby()

    def __str__(self):
        return '\n'.join(self.grille)

    def generate_laby(self):
        pass

    def shuffle_laby(self):

