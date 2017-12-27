# This is the temporary start screen
from tkinter import *
from Constants import *
from PIL import Image, ImageTk
import Game

def drawStartScreen(canvas, options, data):
    data.game.startScreen = PhotoImage(file = "images/startScreen.gif")
    canvas.create_image(0, 0, anchor = "nw", image = data.game.startScreen)
    canvas.create_text((WIN_WIDTH / 2, WIN_HEIGHT - 20),
                        text = "press space bar to enter", fill = "white")
    drawOptions(canvas, options, 200)

def drawMultiPlayerChoices(canvas, data):
    vertDist = 30
    data.game.background = PhotoImage(file = "images/background.gif")
    canvas.create_image(0, 0, anchor = "nw", image = data.game.background)
    canvas.create_text(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 40,
        text = """Use up/down arrow keys to choose the number of players,
        \t           press space to start""",
        fill = "white")
    canvas.create_text(WIN_WIDTH / 2, WIN_HEIGHT / 2 + 10,
        text = "Number of players: %s" % data.game.numHumans, fill = "white")

class OptionList(object):
    def __init__(self, list, selection = 0):
        self.list = list
        self.len = len(list)
        self.selection = 0

    def getSeletion(self):
        return self.list(self.selection)

class Option(object):
    def  __init__(self, text, selected = False, color = "white"):
        self.text = text
        self.selected = selected
        self.color = color
    def setColor(self):
        if self.selected:
            self.color = "red"
        else:
            self.color = "white"
    def __repr__(self):
        return self.text

def drawOptions(canvas, optionList, pad):
    vertDist = 30
    for i in range(optionList.len):
        text = optionList.list[i]
        canvas.create_text(WIN_WIDTH / 2, WIN_HEIGHT - pad + i * vertDist,
                            text = text.text, fill = text.color )

def selectOptions(event, data, optionList):
    numOptions = len(optionList.list)
    if event.keysym ==  "Down" and optionList.selection < numOptions - 1:
        optionList.selection += 1
    elif event.keysym == "Up" and optionList.selection > 0:
        optionList.selection -= 1
    elif event.keysym == "space":
        data.game.screen = optionList.list[optionList.selection].text
        if data.game.screen in MODES:
            Game.Game.mode = data.game.screen
    if data.game.screen != "init" and data.game.screen != "Single Player":
        data.game.playing = True
    for i in range(numOptions):
        option = optionList.list[i]
        if i == optionList.selection:
            option.selected = True
        else:
            option.selected = False
        option.setColor()

'''
    def callback():
        print("clicked")
    buttons = []
    for i in range(len(options)):
        vertDist = 10
        text = options[i]
        # https://stackoverflow.com/questions/11980812/
        # how-do-you-create-a-button-on-a-tkinter-canvas
        buttons.append( Button(root, text = text, command = callback))
        buttons[i].configure(width = 10, activebackground = "grey", relief = FLAT)
        canvas.create_window(WIN_WIDTH / 1, WIN_HEIGHT - 50 + i * vertDist,
                             anchor = NW, window = buttons[i])'''

def drawGameScreen(canvas, data):
    data.game.bgGrass = PhotoImage(file = "images/grass.gif")
    canvas.create_image(0, 0, anchor = "nw", image = data.game.bgGrass)

    #for row in range(ROWS):
        #for col in range(COLS):
            #x0, y0 = MARGIN + col * CELLSIZE, MARGIN + row * CELLSIZE
            #canvas.create_rectangle( (x0, y0), (x0 + CELLSIZE, y0 + CELLSIZE))
    canvas.create_rectangle( (MARGIN, MARGIN),
                            (WIN_WIDTH-MARGIN, WIN_HEIGHT-MARGIN),
                            outline = "white",
                            width = 3 )

def drawSingleSetting(canvas, data):
    canvas.create_rectangle( (0, 0), (WIN_WIDTH, WIN_HEIGHT), fill = "beige",
                            width = 0)
    nameBox = Entry(canvas, width = 50)
    canvas.create_window(WIN_WIDTH // 2, WIN_HEIGHT // 2, window = nameBox)
    canvas.create_text(WIN_WIDTH / 2, WIN_HEIGHT / 2,
                        text = "Please enter your name: ")
    canvas.create_text(WIN_WIDTH / 2, WIN_HEIGHT / 2 + 40,
                        text = "Number of computer players: ")
    startButton = Button(canvas, text = "START!",
                        command = data.game.startGame)
    canvas.create_window(WIN_WIDTH // 2,
                        WIN_HEIGHT // 2 + 50, window = startButton )
    # return the name of the user
    return nameBox.get()

def drawLose(canvas):
    canvas.create_text((WIN_WIDTH / 2, WIN_HEIGHT / 2),
                     text = "GAME OVER", font = ("arial", 36, "bold"))
    canvas.create_text((WIN_WIDTH / 2, WIN_HEIGHT - 15),
                        text = "press space to start")

def drawWin(canvas, game):
    winner = game.winner
    canvas.create_text((WIN_WIDTH / 2, WIN_HEIGHT / 2),
                     text = "%s PLAYER WINS!" % COLORS[winner].upper(),
                     font = ("arial", 36, "bold"))
    canvas.create_text((WIN_WIDTH / 2, WIN_HEIGHT - 15),
                        text = "press space to retart")


