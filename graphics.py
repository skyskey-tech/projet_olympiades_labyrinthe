import tkinter as tk
from tkinter import ttk  # Pour certains widgets plus modernes si besoin
from PIL import ImageTk
import sys
import ctypes
from copy import deepcopy

# Importations de tes modules locaux
from user import save_game, load_file
from lib_pattern import patterns as all_patterns
from picture import BG, ARROW_FG, ARROW_HOV, pattern_to_image, laby_to_image

# --- OPTIMISATION WINDOWS : DPI AWARENESS ---
# Empêche Windows de rendre la fenêtre floue sur les écrans à haute densité de pixels
try:
    if sys.platform == "win32":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

FONT_MONO = 'Courier New' if sys.platform != 'linux' else 'DejaVu Sans Mono'

# ── Menu de démarrage ──────────────────────────────────────────────────────────
def launch_menu(LabyClass):
    """Affiche un menu pour choisir taille et difficulté, puis lance le jeu."""
    menu = tk.Tk()
    menu.title("Labyrinthe – Nouveau jeu")
    menu.configure(bg=BG)
    
    # Force le focus pour que la molette fonctionne immédiatement
    menu.focus_force()

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
                 troughcolor='#16213e', highlightthickness=0, bd=0,
                 cursor="sb_h_double_arrow"
                 ).grid(row=row, column=1)
        return var

    # ── Scrollable container ─────────────────────────────────────────────
    outer = tk.Frame(menu, bg=BG)
    outer.pack(fill='both', expand=True)

    scrollbar = tk.Scrollbar(outer, orient='vertical')
    scrollbar.pack(side='right', fill='y')

    canvas_scroll = tk.Canvas(outer, bg=BG, highlightthickness=0,
                               yscrollcommand=scrollbar.set)
    canvas_scroll.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=canvas_scroll.yview)

    frame = tk.Frame(canvas_scroll, bg=BG, padx=30, pady=24)
    frame_id = canvas_scroll.create_window((0, 0), window=frame, anchor='nw')

    def on_frame_configure(e):
        canvas_scroll.configure(scrollregion=canvas_scroll.bbox('all'))

    def on_canvas_configure(e):
        canvas_scroll.itemconfig(frame_id, width=e.width)

    frame.bind('<Configure>', on_frame_configure)
    canvas_scroll.bind('<Configure>', on_canvas_configure)

    # Correction du scroll Windows (vitesse et sens)
    def on_mousewheel(e):
        # Sur Windows, e.delta est généralement un multiple de 120
        canvas_scroll.yview_scroll(int(-1 * (e.delta / 120)), 'units')

    canvas_scroll.bind_all('<MouseWheel>', on_mousewheel)

    # ── Contenu du Menu ──
    lbl(frame, "T H E  S H I F T I N G  M A Z E", size=20, bold=True,
        color=ARROW_FG).grid(row=0, column=0, columnspan=3, pady=(0, 24))

    lbl(frame, "Taille", size=12, bold=True,
        color='#a0c4ff').grid(row=1, column=0, columnspan=3, sticky='w', pady=(0, 2))
    size_var = slider_row(frame, 2, "Largeur / Hauteur", 11, 101, 31, 2)

    lbl(frame, "Difficulté", size=12, bold=True,
        color='#a0c4ff').grid(row=3, column=0, columnspan=3, sticky='w', pady=(14, 2))
    diff_var = slider_row(frame, 4, "Nombre de shuffles", 1, 60, 10)

    def start():
        sz = size_var.get()
        if sz % 2 == 0: sz -= 1
        diff = diff_var.get()
        menu.destroy()
        laby = LabyClass(sz, sz, diff)
        launch_game(laby, LabyClass)

    tk.Button(frame, text="  Jouer  →  ", command=start,
              font=(FONT_MONO, 13, 'bold'),
              bg=ARROW_FG, fg='white',
              activebackground=ARROW_HOV, activeforeground='white',
              relief='flat', bd=0, padx=20, pady=10,
              cursor='hand2').grid(row=5, column=0, columnspan=3, pady=(24, 0))

    # Stats et Patterns
    save_data = load_file()
    lbl(frame, "Vos statistiques", size=12, bold=True, color='#a0c4ff').grid(row=7, column=0, columnspan=3, pady=(16, 4))
    lbl(frame, f"Points : {save_data['points']} | Résolus : {save_data['nbLabys']}",
        size=10, color='#a0c4ff').grid(row=8, column=0, columnspan=3)

    lbl(frame, "Votre collection", size=12, bold=True, color='#a0c4ff').grid(row=10, column=0, columnspan=3, pady=(16, 4))

    patterns_frame = tk.Frame(frame, bg=BG)
    patterns_frame.grid(row=11, column=0, columnspan=3, pady=(0, 8))

    COLS = 4
    photos = []
    for idx, p in enumerate(all_patterns):
        col, row = idx % COLS, idx // COLS
        cell_frame = tk.Frame(patterns_frame, bg='#16213e', highlightthickness=1, highlightbackground='#2a2a4a')
        cell_frame.grid(row=row, column=col, padx=4, pady=4, ipadx=4, ipady=2)

        discovered = save_data['patterns'].get(p.name, False)
        if discovered:
            img = pattern_to_image(p)
            photo = ImageTk.PhotoImage(img)
            photos.append(photo)
            tk.Label(cell_frame, image=photo, bg='#16213e').pack(pady=(4, 2))
            tk.Label(cell_frame, text=p.name, font=(FONT_MONO, 7, 'bold'), fg='#80ff80', bg='#16213e').pack()
        else:
            tk.Label(cell_frame, text='???', font=(FONT_MONO, 10), fg='#444466', bg='#16213e').pack(padx=15, pady=15)

    tk.Button(frame, text="  Quitter ✕ ", command=menu.destroy,
              font=(FONT_MONO, 11), bg='#333333', fg='white',
              relief='flat', cursor='hand2').grid(row=12, column=0, columnspan=3, pady=(20, 10))

    menu.update_idletasks()
    screen_h = menu.winfo_screenheight()
    menu.geometry(f"{menu.winfo_reqwidth()}x{min(menu.winfo_reqheight(), int(screen_h * 0.9))}")
    menu.mainloop()

# ── Jeu ────────────────────────────────────────────────────────────────────────
def launch_game(laby, LabyClass):
    won = False
    root = tk.Tk()
    root.title("The Shifting Maze")
    root.configure(bg=BG)

    # Calcul dynamique des dimensions pour Windows
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    UI_H = 250 
    avail_w = screen_w - 100
    avail_h = screen_h - UI_H
    
    CELL = max(4, min(avail_w // laby.width, avail_h // laby.height))
    AZ = max(CELL + 10, 25) 

    maze_pw, maze_ph = laby.width * CELL, laby.height * CELL
    cv_w, cv_h = maze_pw + 2 * AZ, maze_ph + 2 * AZ

    canvas = tk.Canvas(root, width=cv_w, height=cv_h, bg=BG, 
                       highlightthickness=1, highlightbackground=ARROW_FG)
    canvas.pack(pady=10)

    photo_container = [None]

    def draw_maze():
        img = laby_to_image(laby, CELL)
        photo_container[0] = ImageTk.PhotoImage(img)
        canvas.create_image(AZ, AZ, anchor='nw', image=photo_container[0], tags='maze')

    def draw_arrows():
        canvas.delete('arrow')
        s = AZ // 3 
        # Flèches Colonnes
        for col in range(1, laby.width - 1):
            cx = AZ + col * CELL + CELL // 2
            # Haut
            canvas.create_polygon(cx, 10, cx-s, 10+s, cx+s, 10+s, fill=ARROW_FG, tags=('arrow', f'cup{col}'))
            # Bas
            canvas.create_polygon(cx, cv_h-10, cx-s, cv_h-10-s, cx+s, cv_h-10-s, fill=ARROW_FG, tags=('arrow', f'cdn{col}'))
        
        # Flèches Lignes
        for row in range(1, laby.height - 1):
            cy = AZ + row * CELL + CELL // 2
            # Gauche
            canvas.create_polygon(10, cy, 10+s, cy-s, 10+s, cy+s, fill=ARROW_FG, tags=('arrow', f'rlt{row}'))
            # Droite
            canvas.create_polygon(cv_w-10, cy, cv_w-10-s, cy-s, cv_w-10-s, cy+s, fill=ARROW_FG, tags=('arrow', f'rrt{row}'))
        
        # Bindings simplifiés
        setup_bindings()

    def setup_bindings():
        # Utilisation de tags génériques pour Windows pour optimiser la réactivité
        for tag in canvas.find_withtag('arrow'):
            t_name = canvas.gettags(tag)[1]
            if 'cup' in t_name:
                idx = int(t_name[3:])
                canvas.tag_bind(tag, '<Button-1>', lambda e, i=idx: do_move('C', -i))
            elif 'cdn' in t_name:
                idx = int(t_name[3:])
                canvas.tag_bind(tag, '<Button-1>', lambda e, i=idx: do_move('C', i))
            elif 'rlt' in t_name:
                idx = int(t_name[3:])
                canvas.tag_bind(tag, '<Button-1>', lambda e, i=idx: do_move('R', -i))
            elif 'rrt' in t_name:
                idx = int(t_name[3:])
                canvas.tag_bind(tag, '<Button-1>', lambda e, i=idx: do_move('R', i))
            
            canvas.tag_bind(tag, '<Enter>', lambda e, t=tag: canvas.itemconfigure(t, fill=ARROW_HOV))
            canvas.tag_bind(tag, '<Leave>', lambda e, t=tag: canvas.itemconfigure(t, fill=ARROW_FG))

    moves_left = tk.IntVar(value=laby.nbShuffles)
    
    def do_move(direction, index):
        if moves_left.get() > 0:
            laby.movements.append((direction, index))
            laby.move_direction(direction, index)
            moves_left.set(moves_left.get() - 1)
            draw_maze()
            if laby.verificate_path(deepcopy(laby.grille), 0, 0) > 0:
                victory(root, laby, LabyClass, moves_left.get())

    # Barre d'outils en bas
    controls = tk.Frame(root, bg=BG)
    controls.pack(fill='x', padx=20, pady=5)
    
    tk.Label(controls, textvariable=moves_left, font=(FONT_MONO, 14, 'bold'), fg=ARROW_FG, bg=BG).pack(side='left')
    tk.Label(controls, text=" MOVES", font=(FONT_MONO, 10), fg="white", bg=BG).pack(side='left', padx=5)

    def victory(root, laby, LabyClass, m):
        points, pattern_got = save_game(laby, m)
        v_win = tk.Toplevel(root)
        v_win.geometry("400x200")
        v_win.configure(bg="#1a1a2e")
        tk.Label(v_win, text="VICTOIRE !", font=(FONT_MONO, 20, 'bold'), fg="#80ff80", bg="#1a1a2e").pack(pady=20)
        tk.Label(v_win, text=f"+{points} Points", fg="white", bg="#1a1a2e").pack()
        root.after(3000, lambda: [v_win.destroy(), root.destroy(), launch_menu(LabyClass)])

    draw_maze()
    draw_arrows()
    root.mainloop()

def _retour_menu(root, LabyClass):
    # Logique de destruction propre pour Windows
    root.quit()
    root.destroy()
    launch_menu(LabyClass)