from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from copy import deepcopy
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

def launch_game(laby):
    root = tk.Tk()
    root.title("Labyrinthe")

    # Calcul dynamique de la taille des cellules selon l'écran
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    max_cell_w = (screen_w - 100) // laby.width
    max_cell_h = (screen_h - 350) // laby.height
    CELL_SIZE = max(4, min(max_cell_w, max_cell_h))

    # --- LE CONTENEUR UNIQUE ---
    # On met tout dans main_frame. C'est lui qui dictera sa taille à root.
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10, expand=True, fill="both")

    # Canvas (enfant de main_frame)
    canvas = tk.Canvas(main_frame, width=laby.width * CELL_SIZE, height=laby.height * CELL_SIZE)
    canvas.grid(row=0, column=0, columnspan=4, pady=10)

    photo = None  

    def draw():
        nonlocal photo
        img = laby_to_image(laby, CELL_SIZE)
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor='nw', image=photo)

    # --- CONTRÔLES (enfant de main_frame) ---
    frame_controls = tk.Frame(main_frame)
    frame_controls.grid(row=1, column=0, columnspan=4, pady=(0, 10))

    tk.Label(frame_controls, text="Direction :").grid(row=0, column=0, padx=5)
    direction_var = tk.StringVar(value='R')
    tk.Radiobutton(frame_controls, text="Ligne (R)", variable=direction_var, value='R').grid(row=0, column=1)
    tk.Radiobutton(frame_controls, text="Colonne (C)", variable=direction_var, value='C').grid(row=0, column=2)

    tk.Label(frame_controls, text="Index :").grid(row=0, column=3, padx=5)
    index_var = tk.IntVar(value=1)
    # Note : Correction de la borne du spinbox
    spinbox = tk.Spinbox(frame_controls, from_=1, to=max(laby.width, laby.height)-2, textvariable=index_var, width=5)
    spinbox.grid(row=0, column=4, padx=5)
    
    tk.Label(frame_controls, text="Sens :").grid(row=0, column=5, padx=5)
    sens_var = tk.StringVar(value='positif')
    tk.Radiobutton(frame_controls, text="→ / ↓", variable=sens_var, value='positif').grid(row=0, column=6)
    tk.Radiobutton(frame_controls, text="← / ↑", variable=sens_var, value='negatif').grid(row=0, column=7)

    # --- SCORE ET MESSAGES (enfants de main_frame) ---
    moves_left = tk.IntVar(value=laby.nbShuffles)
    tk.Label(main_frame, textvariable=moves_left, font=('Arial', 14)).grid(row=2, column=0, columnspan=2)
    tk.Label(main_frame, text="mouvements restants", font=('Arial', 14)).grid(row=2, column=2, columnspan=2)

    msg_var = tk.StringVar()
    tk.Label(main_frame, textvariable=msg_var, font=('Arial', 14), fg='green').grid(row=3, column=0, columnspan=4)

    # --- BOUTONS (enfants de main_frame) ---
    btn_frame = tk.Frame(main_frame)
    btn_frame.grid(row=4, column=0, columnspan=4, pady=10)

    def on_move():
        if moves_left.get() <= 0: return
        direction = direction_var.get()
        index = index_var.get()
        if sens_var.get() == 'negatif': index = -index
        laby.move_direction(direction, index)
        moves_left.set(moves_left.get() - 1)
        draw()
        if deepcopy(laby).verificate_path(0, 0) > 0:
            msg_var.set("Bravo, vous avez gagné !")

    def on_reset():
        laby.grille = deepcopy(laby.model)
        moves_left.set(laby.nbShuffles)
        msg_var.set("")
        draw()

    tk.Button(btn_frame, text="Déplacer", command=on_move, width=12).pack(side='left', padx=10)
    tk.Button(btn_frame, text="Réinitialiser", command=on_reset, width=12).pack(side='left', padx=10)

    draw()
    
    # Force le calcul de la taille réelle par Tkinter
    root.update_idletasks()
    # Empêche la fenêtre de devenir plus petite que nécessaire
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
    
    root.mainloop()