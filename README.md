# The Shifting Maze

**The Shifting Maze** est un jeu de puzzle et de réflexion développé en Python dans le cadre des Olympiades de NSI. Contrairement aux jeux de labyrinthe classiques, le joueur ne déplace pas un personnage, mais manipule la structure même du labyrinthe en faisant coulisser ses lignes et ses colonnes.

---

## Règles du Jeu

L'objectif principal est de reconstituer un chemin continu entre le point de départ et le point d'arrivée.

### 1. Mécanique de mouvement
Le labyrinthe est représenté par une grille dont les lignes et les colonnes intérieures sont mobiles :
* **Glissement par paliers :** Chaque mouvement fait glisser la ligne ou la colonne de **2 cases** d'un coup. Cette particularité arithmétique permet de maintenir la structure logique du labyrinthe.
* **Glissement horizontal :** Les flèches latérales permettent de décaler une ligne vers la gauche ou la droite.
* **Glissement vertical :** Les flèches haut/bas permettent de décaler une colonne.
* **Rotation circulaire :** Lorsqu'une cellule sort d'un côté de la grille, elle réapparaît du côté opposé.
* **Fixité des bords :** Le cadre extérieur du labyrinthe est fixe et ne peut pas être déplacé.

### 2. Guide des couleurs
* **Cases Blanches / Beiges :** Représentent le **chemin** praticable.
* **Cases Noires :** Représentent les **murs** infranchissables.
* **Cases Bleues :** Représentent les murs faisant partie d'un **motif secret** (considérées comme des murs pour la navigation).
* **Case Verte (S) :** Point de départ.
* **Case Rouge (F) :** Point d'arrivée.

### 3. Conditions de victoire
* **Le Chemin :** La partie est gagnée dès qu'une suite de cases "chemin" relie le départ à l'arrivée.
* **Limite de coups :** Le joueur dispose d'un nombre de mouvements limité, défini par la difficulté choisie au départ.

### 4. Système de motifs secrets
Le jeu inclut un défi supplémentaire sous forme de motifs cachés :
* **Préservation :** Si le joueur parvient à résoudre le labyrinthe tout en gardant le motif bleu intact, son score est multiplié par 100.
* **Collection :** Il existe 54 motifs différents à découvrir et à débloquer dans la galerie du menu principal.

---

## Architecture du projet

Le projet est découpé en six modules Python :

* **main.py :** Point d'entrée et gestion de la logique coeur (classes cell et labyrinth).
* **graphics.py :** Gestion de l'interface utilisateur avec Tkinter (menus, canvas, événements).
* **user.py :** Gestion des sauvegardes JSON et calcul des scores.
* **lib_pattern.py :** Bibliothèque contenant les 54 motifs en ASCII art.
* **picture.py :** Moteur de rendu Pillow (PIL) pour la génération des images de la grille.
* **symbols_lib.py :** Dictionnaires de correspondance pour les types de cellules.

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

## Téléchargement (Windows)
Pour les utilisateurs Windows qui ne possèdent pas Python, vous pouvez télécharger la version prête à l'emploi dans l'onglet [Releases](lien-vers-tes-releases).

## Illustrations
![Illustration game](https://github.com/skyskey-tech/projet_olympiades_labyrinthe/blob/main/images/illustration_game.png?raw=True)
Illustration du menu

![Illustration game](https://github.com/skyskey-tech/projet_olympiades_labyrinthe/blob/main/images/illustration_menu.png?raw=True)
Illustration du jeu
