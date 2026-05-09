from PIL import Image


# ── Palette ────────────────────────────────────────────────────────────────────
PIL_COLORS = {
    'PATH':    (240, 230, 210),
    'WALL':    ( 40,  40,  40),
    'DRAWING': (56, 84, 126),
    'START':   ( 80, 200, 120),
    'FINISH':  (220,  80,  80),
    'VISITED': (180, 160, 230),
}
BG        = '#1a1a2e'
ARROW_FG  = '#e94560'
ARROW_HOV = '#ff8fa3'

# ── Utilitaires image ──────────────────────────────────────────────────────────
def laby_to_image(laby, cell_size=20):
    img = Image.new('RGB', (laby.width * cell_size, laby.height * cell_size))
    for row in laby.grille:
        for c in row:
            color = PIL_COLORS.get(c.type, (255, 0, 255))
            img.paste(Image.new('RGB', (cell_size, cell_size), color),
                      (c.x * cell_size, c.y * cell_size))
    return img

def save_image(laby, path, cell_size=20):
    laby_to_image(laby, cell_size).save(path)
    print(f'Image sauvegardée : {path}')

CELL_SIZE = 8  # taille d'un pixel du pattern en pixels écran

def pattern_to_image(p):
    rows = len(p.drawing)
    cols = len(p.drawing[0])
    img = Image.new('RGB', (cols * CELL_SIZE, rows * CELL_SIZE), color=(22, 33, 62))
    for j, line in enumerate(p.drawing):
        for i, c in enumerate(line):
            if c == '%':
                color = PIL_COLORS['DRAWING']
            else:
                color = PIL_COLORS['WALL']
            img.paste(Image.new('RGB', (CELL_SIZE, CELL_SIZE), color),
                      (i * CELL_SIZE, j * CELL_SIZE))
    return img