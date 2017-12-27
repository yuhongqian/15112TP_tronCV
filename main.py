from tkinter import *
from Constants import *
from Player import *
from Scene import *
import random, cv2
import cvControl
from cvControl import cvWebcam
from Game import *
START_OPTIONS = OptionList([Option("Single Player", selected = True,
                color = "red"),
                Option("Multiple Players")])
SINGLE_OPTIONS = OptionList( [Option("Play With Computer", selected = True,
                color = "red"),
                Option("Adventure Mode")] )

# The Animation Skeleton is from 15-112 course website
# https://www.cs.cmu.edu/~112/syllabus.html

def init(data):
    data.game = Game()
    data.game.playMusic()

def timerFired(data):
    # print(type(data.game))
    if data.game.screen in MODES and data.game.playing: # and data.game.started:
        data.game.webcam.updateWebcam()
        if data.game.control == "cv":
            controlHumanPlayers(data.game.players, data.game.numHumans)
        if Game.mode == "Single Player":
            controlComputerPlayer(data.game.computerPlayer)
            data.game.computerPlayer.counter -= 1
        data.game.movePlayers()
        data.game.checkStatus()

def mousePressed(event,data):
    pass

def keyPressed(event, data):
     # control the human player
    if data.game.screen == "init":
        selectOptions(event, data, START_OPTIONS)
        if Game.mode == "Multiple Players":
            data.game = Game(screen = Game.mode, numHumans = 2)
        elif data.game.screen == "Single Player":
            data.game = GameWithComputer(screen = Game.mode)
            data.game.playing = True
    elif data.game.screen == "Multiple Players" and data.game.playing == False:
        # print("this is the screen," , data.game.numHumans)
        if event.keysym == "Down" and data.game.numHumans ==3:
            data.game.numHumans -= 1
            data.game.__init__(screen = "Multiple Players",
                                numHumans = data.game.numHumans)
        elif event.keysym == "Up" and data.game.numHumans == 2:
            data.game.numHumans += 1
            data.game.__init__(screen = "Multiple Players",
                                numHumans = data.game.numHumans)
        elif event.keysym == "space":
            # print("pressed")
            data.game.playing = True
    elif data.game.screen == "lose" or data.game.screen == "result":
        # print("this screen")
        if event.keysym == "space":
            # print("init here")
            init(data)
    if data.game.playing and data.game.control == "keyboard":
        keyBoardControl(event, data.game)
    pass

def drawGame(canvas, data):
    drawGameScreen(canvas, data)
    for player in data.game.activePlayers:
        player.drawRoute(canvas)
        player.drawDot(canvas)

def redrawAll(canvas, data):
    # print(data.game.screen)
    # print(data.game.playing)
    cv2.imshow("currFrame", data.game.webcam.copiedFrame)
    if data.game.screen == "init":
        drawStartScreen(canvas, START_OPTIONS, data)
    elif data.game.screen == "Multiple Players" and data.game.playing == False:
        drawMultiPlayerChoices(canvas, data)

    elif data.game.screen in MODES and data.game.playing: # and data.game.started:
        drawGame(canvas, data)
    elif data.game.screen == "lose":
        drawGame(canvas, data)
        drawLose(canvas)
    elif data.game.screen == "result":
        drawGame(canvas, data)
        drawWin(canvas, data.game)
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    root = Tk()
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
        redrawAllWrapper(canvas,data)

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
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the appf
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(WIN_WIDTH, WIN_HEIGHT)
