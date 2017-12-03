# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *
from Constants import *
import random

class Player(object):
    numOfPlayers = 2

    def __init__(self, number, speed = 3):
        # initial position is random
        self.x = random.randint(10, WIN_WIDTH - 10)
        self.y = random.randint(10, WIN_HEIGHT - 10)
        # assign colors to the player according to the player's number
        self.number = number
        self.color = COLORS[number]

        self.speed = speed
        self.positions = []

    def makeMove(self, dir):
        if dir == "N":
            self.y += self.speed
        elif dir == "S":
            self.y -= self.speed
        elif dir == "W":
            self.x -= self.speed
        elif dir == "E":
            self.x += self.speed
        self.positions.append(self.x, self.y)

    def drawRoute(self, canvas):
        for i in range(len(self.positions) - 1):
            canvas.create_line(self.positions[i], self.positions[i+1],
                                fill = self.color, width = LINE_WIDTH)

def init(data):

    # load data.xyz as appropriate
    pass

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)
