from tkinter import *
from Constants import *
from Scene import  *
from cvControl import *
from Player import *
import pygame
import random, cv2, copy

# A general Game class
# should be compatible with:
# play w/ computer mode / adventure mode / multi-player mode

class Game(object):
    # by default: there will be one human player, controlled using opencv
    mode = "Play With Computer"
    def __init__(self, screen = "init", numHumans = 1, control = "cv"):
        # print(Game.mode)
        Player.board = [ [0] * (COLS + 1) for row in range(ROWS + 1) ]
        self.started = False
        self.players = []
        self.activePlayers = []
        self.deadPlayers = []
        self.control = control
        self.numHumans = numHumans
        # print(numHumans)
        Player.numPlayers = numHumans
        self.winner = None
        self.webcam = cvWebcam(self.numHumans, self)

        for i in range(numHumans):
            print(i)
            player = Player(i, self.webcam)
            self.players.append(player)
            self.activePlayers.append(player)
            print("appended")

        # by default, the map is empty
        self.map = self.emptyMap()
        # start from the "init" screen
        self.screen = screen
        self.playing = False

    def startGame(self):
        self.started = True

    def playMusic(self, musicFile = BG_MUSIC, volume = VOLUME):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play(loops = -1)

    def emptyMap(self):
        map =  [ [0] * (COLS + 1) for row in range(ROWS + 1) ]
        return map

    def movePlayers(self):
        for player in self.activePlayers:
            player.makeMove()
            # print(player.row, player.col)
            if Player.isDead(player, player.row, player.col):
                player.route.append( (player.row, player.col))
                player.dead = True
            else:
                player.route.append( (player.row, player.col) )
                Player.board[player.row][player.col] = 1

    def checkStatus(self):
        # print(data.computerPlayer.dead)
        if len(self.activePlayers) == 1:
            self.winner = self.activePlayers[0].number
            self.screen = "result"
        for player in self.activePlayers:
            if player.dead:
                for (row, col) in player.route:
                    Player.board[row][col] = 0
                self.activePlayers.remove(player)
                self.deadPlayers.append(player)

class GameWithComputer(Game):
     def __init__(self, screen = "init", numHumans = 1, control = "cv"):
         super().__init__(screen, numHumans, control)
         self.computerPlayer = ComputerPlayer(self.numHumans, self.webcam)
         self.players.append(self.computerPlayer)
         self.activePlayers.append(self.computerPlayer)
         # by default, the map is empty
         self.map = self.emptyMap()
         # start from the "init" screen
         self.screen = screen
         self.playing = False


def keyBoardControl(event, game):
    if event.keysym in CONTROL_0 and game.numHumans >= 1:
        game.activePlayers[0].dir = CONTROL_0[event.keysym]
    elif event.keysym in CONTROL_1 and game.numHumans >= 2:
        game.activePlayers[1].dir = CONTROL_1[event.keysym]
    elif event.keysym in CONTROL_2 and game.numHumans >= 3:
        game.activePlayers[2].dir = CONTROL_2[event.keysym]



