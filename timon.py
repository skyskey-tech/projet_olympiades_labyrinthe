from PIL import Image

COLORS = {
    'PATH':    (240, 230, 210),
    'WALL':    ( 40,  40,  40),
    'DRAWING': ( 80, 120, 180),
    'START':   ( 80, 200, 120),
    'FINISH':  (220,  80,  80),
    'VISITED': (180, 160, 230),
}

def cell_to_image(cell, cell_size: int = 20) -> Image.Image:
    color = COLORS.get(cell.type, (255, 0, 255))
    return Image.new('RGB', (cell_size, cell_size), color)

def laby_to_image(laby, cell_size: int = 20) -> Image.Image:
    canvas = Image.new('RGB', (laby.width * cell_size, laby.height * cell_size))
    for row in laby.grille:
        for c in row:
            canvas.paste(cell_to_image(c, cell_size), (c.x * cell_size, c.y * cell_size))
    return canvas

def save_image(laby, path: str, cell_size: int = 20):
    laby_to_image(laby, cell_size).save(path)
    print(f'Image sauvegardée : {path}')
