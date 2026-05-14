# The Shifting Maze

**The Shifting Maze** est un jeu de puzzle et de réflexion développé en Python dans le cadre des Olympiades Nationales de NSI. Contrairement aux jeux de labyrinthe classiques, le joueur ne déplace pas un personnage, mais manipule la structure même du labyrinthe en faisant coulisser ses lignes et ses colonnes.

---

## Règles du Jeu

L'objectif principal est de reconstituer un chemin continu entre le point de départ et le point d'arrivée.

### 1. Mécanique de mouvement
Le labyrinthe est représenté par une grille dont les lignes et les colonnes intérieures sont mobiles :
* **Glissement horizontal :** Les flèches latérales permettent de décaler une ligne vers la gauche ou la droite.
* **Glissement vertical :** Les flèches haut/bas permettent de décaler une colonne.
* **Rotation circulaire :** Lorsqu'une cellule sort d'un côté de la grille, elle réapparaît du côté opposé.
* **Fixité des bords :** Le cadre extérieur du labyrinthe est fixe et ne peut pas être déplacé.

### 2. Conditions de victoire
* **Le Chemin :** La partie est gagnée dès qu'une suite de cases de type "chemin" (beige) relie la case de départ (S, verte) à la case d'arrivée (F, rouge).
* **Limite de coups :** Le joueur dispose d'un nombre de mouvements limité, défini par la difficulté choisie au départ.

### 3. Système de motifs secrets
Le jeu inclut un défi supplémentaire sous forme de motifs cachés (dessins en bleu ardoise) :
* **Préservation :** Si le joueur parvient à résoudre le labyrinthe tout en gardant le motif intact dans la grille, son score est multiplié par 100.
* **Collection :** Il existe 54 motifs différents à découvrir. Une fois reconstitués sans être brisés, ils sont débloqués dans la galerie du menu principal.

---

## Architecture du projet

Le projet est découpé en six modules Python pour une meilleure gestion du code :

* **main.py :** Point d'entrée du programme et gestion de la logique coeur (classes cell et labyrinth).
* **graphics.py :** Gestion de l'interface utilisateur avec Tkinter (menus, canvas, événements).
* **user.py :** Gestion des sauvegardes au format JSON et calcul des scores.
* **lib_pattern.py :** Bibliothèque de données contenant les 54 motifs en ASCII art.
* **picture.py :** Moteur de rendu utilisant la bibliothèque Pillow (PIL) pour transformer la grille en image.
* **symbols_lib.py :** Dictionnaires de correspondance pour les différents types de cellules.

---

## Installation et utilisation

### Prérequis
Le projet nécessite Python 3 ainsi que la bibliothèque de traitement d'images Pillow.

### Installation des dépendances
```bash
pip install Pillow
```
### Lancement du jeu
```bash
python3 main.py
```