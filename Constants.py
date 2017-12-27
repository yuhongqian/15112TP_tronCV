WIN_WIDTH = 640
WIN_HEIGHT = 480
LINE_WIDTH = 3
MODES = {"Single Player", "Multiple Players"}
CHOICE_SCREEN = {"init", "Single Player"}
# MOVE_SENSIBILITY = 40
COLORS = ["red", "blue", "green", "yellow"]
NUM_COLORS = [(0,0,255), (255,0,0), (0,255,0), (255,0,255)]
N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)
DIRS = [N, S, W, E]
RADIUS = 8
BG_MUSIC = "music/CountingStars.mp3"
VOLUME = 0.8

# Board settings
CELLSIZE = 10
MARGIN = 20
ROWS = (WIN_HEIGHT - MARGIN * 2) // CELLSIZE
COLS = (WIN_WIDTH - MARGIN * 2) // CELLSIZE


# Player 0:
CONTROL_0 = {"Up": N, "Down": S, "Left": W, "Right": E}

# Player 1:
CONTROL_1 = {"w": N, "s": S, "a": W, "d": E}

# Player 2:
CONTROL_2 = {"i": N, "k": S, "h": W, "l": E}



