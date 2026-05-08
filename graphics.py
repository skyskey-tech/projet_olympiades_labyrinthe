from PIL import Image, ImageTk
import tkinter as tk
from copy import deepcopy
import sys
from user import save_game, load_file
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

FONT_MONO = 'Courier New' if sys.platform != 'linux' else 'DejaVu Sans Mono'
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


# ── Menu de démarrage ──────────────────────────────────────────────────────────
def launch_menu(LabyClass):
    """Affiche un menu pour choisir taille et difficulté, puis lance le jeu."""
    menu = tk.Tk()
    menu.title("Labyrinthe – Nouveau jeu")
    menu.configure(bg=BG)
    menu.resizable(False, False)

    def lbl(parent, text, size=11, bold=False, color='#e0e0e0'):
        return tk.Label(parent, text=text,
                        font=(FONT_MONO, size, 'bold' if bold else 'normal'),
                        fg=color, bg=BG)

    def slider_row(parent, row, text, from_, to, init, resolution=1):
        lbl(parent, text).grid(row=row, column=0, sticky='w', padx=(0, 16), pady=6)
        var = tk.IntVar(value=init)
        val_lbl = lbl(parent, str(init), bold=True, color=ARROW_FG)
        val_lbl.grid(row=row, column=2, padx=(8, 0))

        def update(v): val_lbl.config(text=v)

        tk.Scale(parent, from_=from_, resolution=resolution, to=to, orient='horizontal',
                 variable=var, showvalue=False, command=update,
                 length=280, sliderlength=18,
                 bg=BG, fg=ARROW_FG, activebackground=ARROW_HOV,
                 troughcolor='#16213e', highlightthickness=0, bd=0
                 ).grid(row=row, column=1)
        return var

    frame = tk.Frame(menu, bg=BG, padx=30, pady=24)
    frame.pack()

    lbl(frame, "T H E  S H I F T I N G  M A Z E", size=20, bold=True,
        color=ARROW_FG).grid(row=0, column=0, columnspan=3, pady=(0, 24))

    lbl(frame, "Taille", size=12, bold=True,
        color='#a0c4ff').grid(row=1, column=0, columnspan=3, sticky='w', pady=(0, 2))
    size_var = slider_row(frame, 2, "Largeur / Hauteur", 11, 101, 31, 2)

    lbl(frame, "Difficulté", size=12, bold=True,
        color='#a0c4ff').grid(row=3, column=0, columnspan=3, sticky='w', pady=(14, 2))
    diff_var = slider_row(frame, 4, "Nombre de shuffles", 1, 60, 10)

    def get_size():
        v = size_var.get()
        return v if v % 2 == 1 else v - 1   # le générateur a besoin d'un nombre impair

    def start():
        sz   = get_size()
        diff = diff_var.get()
        menu.destroy()
        laby = LabyClass(sz, sz, diff)
        launch_game(laby,LabyClass)

    tk.Button(frame, text="  Jouer  →  ", command=start,
              font=(FONT_MONO, 13, 'bold'),
              bg=ARROW_FG, fg='white',
              activebackground=ARROW_HOV, activeforeground='white',
              relief='flat', bd=0, padx=20, pady=10,
              cursor='hand1').grid(row=5, column=0, columnspan=3, pady=(24, 0))

    tk.Button(frame, text="  Quitter ✕ ", command=menu.destroy,
              font=(FONT_MONO, 13, 'bold'),
              bg=ARROW_FG, fg='white',
              activebackground=ARROW_HOV, activeforeground='white',
              relief='flat', bd=0, padx=20, pady=10,
              cursor='hand1').grid(row=5, column=2, columnspan=3, pady=(24, 0))
    

    # Stats sauvegardées
    save_data = load_file()
    lbl(frame, f"Points totaux : {save_data['points']}",
        size=10, color='#a0c4ff').grid(row=7, column=0, columnspan=3, pady=(16, 0))

    lbl(frame, f"Labyrinthes résolus : {save_data['nbLabys']}",
        size=10, color='#a0c4ff').grid(row=8, column=0, columnspan=3, pady=(16, 0))

    patterns_txt = ', '.join(save_data['patterns']) if save_data['patterns'] else 'Aucun'
    lbl(frame, f"Motifs obtenus : {patterns_txt}",
        size=10, color='#a0c4ff').grid(row=9, column=0, columnspan=3, pady=(4, 0))

    trophees_txt = ', '.join(save_data['trophees']) if save_data['trophees'] else 'Aucun'
    lbl(frame, f"Vos trophées : {trophees_txt}",
        size=10, color='#a0c4ff').grid(row=10, column=0, columnspan=3, pady=(4, 0))
    
    menu.update_idletasks()
    menu.minsize(menu.winfo_reqwidth(), menu.winfo_reqheight())
    menu.mainloop()

def _retour_menu(root, LabyClass):
    popup = tk.Toplevel(root)
    popup.title("Victoire !")
    popup.configure(bg=BG)
    popup.resizable(False, False)

    tk.Label(popup, text="✦  Félicitations !  ✦",
             font=(FONT_MONO, 16, 'bold'), fg='#80ff80', bg=BG).pack(padx=30, pady=(20, 8))

    tk.Label(popup, text="Retour au menu dans 3 secondes…",
             font=(FONT_MONO, 10), fg='#e0e0e0', bg=BG).pack(pady=(0, 20))

    def go():
        popup.destroy()
        root.destroy()
        launch_menu(LabyClass)

    popup.after(3000, go)

# ── Jeu ────────────────────────────────────────────────────────────────────────
def launch_game(laby, LabyClass):
    root = tk.Tk()
    root.title("Labyrinthe")
    root.configure(bg=BG)

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Taille de cellule : on réserve de la place pour les flèches et l'UI
    # UI_H couvre : titre + pattern + compteur + message + boutons + paddings + barre de tâches + chrome fenêtre
    UI_H      = 700
    ARROW_EST = 24
    avail_w   = screen_w - 80  - 2 * ARROW_EST
    avail_h   = screen_h - UI_H - 2 * ARROW_EST
    CELL      = max(4, min(avail_w // laby.width, avail_h // laby.height))
    AZ        = max(CELL + 8, 22)   # Arrow Zone : au moins une cellule + marge

    maze_pw  = laby.width  * CELL
    maze_ph  = laby.height * CELL
    cv_w     = maze_pw + 2 * AZ
    cv_h     = maze_ph + 2 * AZ

    # ── Layout ──────────────────────────────────────────────────────────────
    wrap = tk.Frame(root, bg=BG)
    wrap.pack(padx=12, pady=10)

    tk.Label(wrap, text="T H E  S H I F T I N G  M A Z E",
             font=(FONT_MONO, 14, 'bold'), fg=ARROW_FG, bg=BG).pack(pady=(0, 2))

    if laby.pattern_chosen:
        tk.Label(wrap,
                 text=f"✦  Motif cible : {laby.pattern_chosen.name.upper()}  ✦",
                 font=(FONT_MONO, 9), fg='#a0c4ff', bg=BG).pack(pady=(0, 4))

    # Canvas unique contenant labyrinthe + zones flèches
    canvas = tk.Canvas(wrap, width=cv_w, height=cv_h,
                       bg=BG, highlightthickness=2,
                       highlightbackground=ARROW_FG)
    canvas.pack()

    photo = [None]

    # ── Dessin du labyrinthe ─────────────────────────────────────────────────
    def draw_maze():
        img = laby_to_image(laby, CELL)
        photo[0] = ImageTk.PhotoImage(img)
        canvas.create_image(AZ, AZ, anchor='nw', image=photo[0], tags='maze')

    # ── Flèches (polygones Canvas → alignement pixel parfait) ────────────────
    def draw_arrows():
        canvas.delete('arrow', 'hl')
        s = max(3, AZ * 2 // 5)   # demi-taille du triangle

        for col in range(1, laby.width - 1):
            # Centre X de la colonne col, exprimé en coordonnées canvas
            cx = AZ + col * CELL + CELL // 2

            # Flèche ▲ (haut → déplace vers le haut, index négatif)
            cy = AZ // 2
            tup = f'cup{col}'
            canvas.create_polygon(cx, cy - s, cx - s, cy + s, cx + s, cy + s,
                                  fill=ARROW_FG, outline='', tags=('arrow', tup))
            _bind(tup, 'C', -col, 'col', col)

            # Flèche ▼ (bas → déplace vers le bas, index positif)
            cy = maze_ph + AZ + AZ // 2
            tdn = f'cdn{col}'
            canvas.create_polygon(cx, cy + s, cx - s, cy - s, cx + s, cy - s,
                                  fill=ARROW_FG, outline='', tags=('arrow', tdn))
            _bind(tdn, 'C', col, 'col', col)

        for row in range(1, laby.height - 1):
            # Centre Y de la ligne row
            cy = AZ + row * CELL + CELL // 2

            # Flèche ◀ (gauche → index négatif)
            cx = AZ // 2
            tlt = f'rlt{row}'
            canvas.create_polygon(cx - s, cy, cx + s, cy - s, cx + s, cy + s,
                                  fill=ARROW_FG, outline='', tags=('arrow', tlt))
            _bind(tlt, 'R', -row, 'row', row)

            # Flèche ▶ (droite → index positif)
            cx = maze_pw + AZ + AZ // 2
            trt = f'rrt{row}'
            canvas.create_polygon(cx + s, cy, cx - s, cy - s, cx - s, cy + s,
                                  fill=ARROW_FG, outline='', tags=('arrow', trt))
            _bind(trt, 'R', row, 'row', row)

    def _bind(tag, direction, index, axis, idx):
        canvas.tag_bind(tag, '<Button-1>',
                        lambda e, d=direction, i=index: do_move(d, i))
        canvas.tag_bind(tag, '<Enter>',
                        lambda e, t=tag, ax=axis, ix=idx: _on_enter(t, ax, ix))
        canvas.tag_bind(tag, '<Leave>',
                        lambda e, t=tag: _on_leave(t))

    def _on_enter(tag, axis, idx):
        """Survol : colore la flèche et surligne la ligne/colonne concernée."""
        canvas.itemconfigure(tag, fill=ARROW_HOV)
        canvas.delete('hl')
        if axis == 'col':
            x0, y0 = AZ + idx * CELL, AZ
            x1, y1 = x0 + CELL, y0 + maze_ph
        else:
            x0, y0 = AZ, AZ + idx * CELL
            x1, y1 = x0 + maze_pw, y0 + CELL
        canvas.create_rectangle(x0, y0, x1, y1,
                                fill='#e94560',
                                stipple='gray25',
                                outline='', tags='hl')
        canvas.tag_raise('arrow')

    def _on_leave(tag):
        canvas.itemconfigure(tag, fill=ARROW_FG)
        canvas.delete('hl')

    # ── Logique de jeu ───────────────────────────────────────────────────────
    moves_left = tk.IntVar(value=laby.nbShuffles)
    msg_var    = tk.StringVar()

    def do_move(direction, index):
        if moves_left.get() <= 0:
            return
        laby.move_direction(direction, index)
        moves_left.set(moves_left.get() - 1)
        canvas.delete('maze')
        draw_maze()
        canvas.delete('hl')
        canvas.tag_raise('arrow')
        if deepcopy(laby).verificate_path(0, 0) > 0:
            points, pattern_got = save_game(laby, moves_left.get())
            msg = f"✦  Bravo !  +{points} pts"
            if pattern_got:
                msg += f"  —  Vous avez obtenu un nouveau motif ! : {pattern_got}"
            msg += "  ✦"
            msg_var.set(msg)
            root.after(2000, lambda: _retour_menu(root, laby.__class__))
           

    # ── UI inférieure ────────────────────────────────────────────────────────
    info = tk.Frame(wrap, bg=BG)
    info.pack(pady=6)
    tk.Label(info, textvariable=moves_left,
             font=(FONT_MONO, 11), fg='#e0e0e0', bg=BG).pack(side='left')
    tk.Label(info, text=' mouvements restants',
         font=(FONT_MONO, 11), fg='#e0e0e0', bg=BG).pack(side='left')
    tk.Label(wrap, textvariable=msg_var,
             font=(FONT_MONO, 12, 'bold'), fg='#80ff80', bg=BG).pack()

    btns = tk.Frame(wrap, bg=BG)
    btns.pack(pady=(4, 8))

    def mk_btn(text, cmd):
        b = tk.Button(btns, text=text, command=cmd,
                      font=(FONT_MONO, 10, 'bold'),
                      bg='#16213e', fg='#e0e0e0',
                      activebackground=ARROW_FG, activeforeground='white',
                      relief='flat', bd=0, padx=14, pady=6, cursor='hand1')
        b.pack(side='left', padx=8)
        b.bind('<Enter>', lambda e: b.configure(bg=ARROW_FG, fg='white'))
        b.bind('<Leave>', lambda e: b.configure(bg='#16213e', fg='#e0e0e0'))

    def on_reset():
        laby.grille = deepcopy(laby.model)
        moves_left.set(laby.nbShuffles)
        msg_var.set("")
        canvas.delete('maze')
        draw_maze()
        canvas.delete('hl')
        canvas.tag_raise('arrow')

    mk_btn("↺  Réinitialiser", on_reset)
    mk_btn("✕  Quitter",lambda: [root.destroy(), launch_menu(laby.__class__)])

    draw_maze()
    draw_arrows()

    root.update_idletasks()
    w = min(root.winfo_reqwidth(),  screen_w - 20)
    h = min(root.winfo_reqheight(), screen_h - 60)
    root.minsize(w, h)
    root.maxsize(screen_w - 20, screen_h - 60)
    root.mainloop()
