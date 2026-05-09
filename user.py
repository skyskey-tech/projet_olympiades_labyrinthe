import json
from pathlib import Path
from symbols_lib import symbols_inversed

SAVE_FILE_PATH = Path.home() / '.shifting_maze_save.json'

def check_pattern(laby):
    if laby.pattern_chosen:
        for y_corner in range(1, laby.height - 1 - laby.pattern_chosen.size):
            for x_corner in range(1, laby.width - 1 - laby.pattern_chosen.size):
                i, j = 0, 0
                while laby.grille[y_corner+j][x_corner+i].type == symbols_inversed[laby.pattern_chosen.drawing[j][i]]:
                    if (i, j) == (len(laby.pattern_chosen.drawing[0])-1, len(laby.pattern_chosen.drawing)-1):
                        return laby.pattern_chosen.name
                    if i == len(laby.pattern_chosen.drawing[0]):
                        i=-1
                        j += 1
                    i+=1
    return 

def count_point(laby, pattern, moves_left):
    points = laby.width*0.5 * (laby.nbShuffles-moves_left)**2
    if pattern!=None:
        points *= 100
    return points


def load_file():
    if not SAVE_FILE_PATH.exists():
        data = {
            'points':0,
            'trophees':[],
            'patterns' : [],
            'nbLabys': 0
        }     
        with open(SAVE_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    try:
        with open(SAVE_FILE_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {'points': 0, 'trophees': [], 'patterns': [], 'nbLabys': 0}

    
def save_game(laby, moves_left):
    pattern = check_pattern(laby)
    points = count_point(laby, pattern, moves_left)
    data = load_file()
    data['points']+= points
    if pattern != None and pattern not in data['patterns']:
        data['patterns'].append(pattern)
    data['nbLabys'] += 1
    with open(SAVE_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    return points, pattern