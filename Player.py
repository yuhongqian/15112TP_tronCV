from Constants import *
import random, copy, cv2
import numpy as np
from tkinter import  *

def getX(col):
    return MARGIN + col * CELLSIZE

def getY(row):
    return MARGIN + row * CELLSIZE

class Player(object):
    # the board stores the status of the spots (1 == touched, 0 == untouched)
    board = [ [0] * (COLS + 1) for row in range(ROWS + 1) ]
    numPlayers = 1
    # print(len(board), len(board[0]))
    def __init__(self, number, webcam, speed = 3):
        # the current location
        self.row = random.randint(10, ROWS - 10)
        self.col = random.randint(10, COLS - 10)
        # in the form of (drow, dcol)
        self.dir = random.choice(DIRS)
        self.color = COLORS[number]
        self.dead = False
        self.webcam = webcam
        self.number = number
        self.route = []
        self.loadArrows()
        self.setROI()

        self.maskedROI = self.getBlueArea()
        self.center = self.getRect()

        # self.currCenter = self.center
        # self.prevCenter = self.center

    def makeMove(self):
        # print("direction: ", self.dir)
        drow, dcol = self.dir[0], self.dir[1]
        self.row += drow
        self.col += dcol
        # if move backwards, forced to continue move forward
        if len(self.route) >= 1 and (self.row, self.col) == self.route[-1]:
            # print("backwards")
            self.row -= 2 * drow
            self.col -= 2 * dcol

    def drawDot(self, canvas):
        xc, yc = MARGIN + self.col * CELLSIZE, MARGIN + self.row * CELLSIZE
        canvas.create_oval(xc - RADIUS, yc - RADIUS, xc + RADIUS, yc + RADIUS,
                          fill = self.color, width = 0)

    def drawRoute(self, canvas):
        # self.bombImg = PhotoImage(file = "images/fence.gif")
        for i in range(len(self.route) - 1):
            pos0 = self.route[i]
            pos1 = self.route[i + 1]
            x0, y0 = getX(pos0[1]), getY(pos0[0])
            x1, y1 = getX(pos1[1]), getY(pos1[0])
            # canvas.create_image(x0, y0, image = self.bombImg )
            canvas.create_line( x0, y0, x1, y1,
                            fill = self.color, width = 3)

    def loadArrows(self):
        self.upArrow = cv2.imread("images/up.jpg")
        self.downArrow = cv2.imread("images/down.jpg")
        self.leftArrow = cv2.imread("images/left.jpg")
        self.rightArrow = cv2.imread("images/right.jpg")
        self.arrows = [self.upArrow, self.downArrow,
                      self.leftArrow, self.rightArrow]

    @staticmethod
    def isDead(player, row, col):
        return (Player.board[row][col] == 1
            or row == 0 or row == ROWS or col == 0 or col == COLS )

    # The following functions are related to the openCV scene

    # Get the partial frame areas according to the player's number
    def setROI(self):
        frameHeight = self.webcam.frame.shape[0]
        frameWidth = self.webcam.frame.shape[1]
        self.roiH=  frameHeight
        self.roiW = frameWidth // self.numPlayers
        self.roiY = 0
        self.roiX = 0 + self.number * self.roiW
        self.frameROI = self.webcam.frame[self.roiY:self.roiY+self.roiH,
                                        self.roiX:self.roiX+self.roiW]
    # Return a masked img where only the blue areas are visible
    def getBlueArea(self):
        # convert the bgr img to hsv
        hsvROI = cv2.cvtColor(self.frameROI, cv2.COLOR_BGR2HSV)

        lower = np.array([100, 100, 100])
        upper = np.array([130, 230, 240])
        # create the mask
        mask = cv2.inRange(hsvROI, lower, upper)
        # apply the mask to the img
        maskedROI = cv2.bitwise_and(self.frameROI, self.frameROI, mask = mask)

        return maskedROI

    # return the contour of the blue rectangle
    # and draw the rectangle outline
    def getRect(self):
        # convert to gray img for easier processing
        # takes only the ROI
        # roi = frame[y:y+h, x:x+w]
        # maskedFrame = maskedFrame[y:y+h, x:x+w]
        bgr = cv2.cvtColor(self.maskedROI, cv2.COLOR_HSV2BGR)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        # reduce noise using a Gaussian filtering
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        # remove the blobs
        thresh = cv2.erode(thresh, None, iterations = 2)
        thresh = cv2.dilate(thresh, None, iterations = 2)
        # extract contours
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contour = max(contours, key = cv2.contourArea)
            # peri = cv2.arcLength(contour, True)
            # approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
            # if len(approx) == 4:
            rect = cv2.minAreaRect(contour)
            box  = cv2.boxPoints(rect)
            box = np.int0(box)
            # draw on the frameROI
            # put the frame ROI on to the webcam
            self.frameROI = cv2.polylines(self.frameROI, [box], 0,
                color = NUM_COLORS[self.number], thickness =  2)
            if len(box) > 0:
                circleR = 5
                leftTopPt, rightBottomPt = box[2], box[0]
                xc = (leftTopPt[0] + rightBottomPt[0]) // 2
                yc = (leftTopPt[1] + rightBottomPt[1]) // 2
                cv2.circle(self.frameROI, (xc, yc), radius = circleR,
                        color = NUM_COLORS[self.number], thickness = -1 )
            self.webcam.copiedFrame[self.roiY:self.roiY+self.roiH,
                         self.roiX:self.roiX+self.roiW] = self.frameROI

            # overlay UI on top of it
        self.webcam.drawUI()

        if len(contours) > 0 and len(box) > 0: return (xc, yc)
        else: return None

    def getMove(self):
        cx, cy = self.center
        arrowShape = self.upArrow.shape[:2]
        arrowH = arrowShape[0]
        arrowW = arrowShape[1]
        arrowSize = max(arrowH, arrowW)
        gap = arrowSize // 2
        ROIcx, ROIcy = self.roiW // 2, self.roiH // 2
        # up
        xUp = ROIcx - arrowSize // 2
        yUp = ROIcy - gap - arrowSize
        # down
        xDown = ROIcx - arrowSize // 2
        yDown = yUp + arrowSize * 2
        # left
        xLeft = ROIcx - gap - arrowSize
        yLeft = ROIcy - arrowSize // 2
        # right
        xRight = xLeft + arrowSize * 2
        yRight = ROIcy - arrowSize // 2
        # get move
        if xUp <= cx <= xUp + arrowSize and yUp <= cy <= yUp + arrowSize:
            return (-1, 0)
        elif (xDown <= cx <= xDown + arrowSize and
                yDown <= cy <= yDown + arrowSize):
            return (+1, 0)
        elif (xLeft <= cx <= xLeft + arrowSize and
                yLeft <= cy <= yLeft + arrowSize):
            return (0, -1)
        elif (xRight <= cx <= xRight + arrowSize and
                yRight <= cy <= yRight + arrowSize):
            return (0, +1)

    '''
    # Control methods
    def controlPlayer(self):
        # get the current center
        self.currCenter = self.getCenter(self.rect)

        if self.prevCenter != None and self.currCenter != None:
            prevX, prevY = self.prevCenter[0], self.prevCenter[1]
            currX, currY = self.currCenter[0], self.currCenter[1]
            if ( abs(currX - prevX) >= MOVE_SENSIBILITY or
            abs(currY - prevY) >= MOVE_SENSIBILITY ):
               # print(game.webcam.getMove(game.prevCenter, game.currCenter))
                self.dir = self.getMove(self.prevCenter,
                                        self.currCenter)
        # update the prev center
        self.prevCenter = self.currCenter
    '''

    def controlPlayer(self):
        if self.center != None and self.getMove() != None:
            self.dir = self.getMove()

def controlHumanPlayers(players, numHumans):
    for i in range(numHumans):
        # print(i)
        player = players[i]
        # update the scene
        player.frameROI = player.webcam.frame[player.roiY:player.roiY+player.roiH,
                                        player.roiX:player.roiX+player.roiW]
        player.maskedROI = player.getBlueArea()
        player.center = player.getRect()
        player.controlPlayer()

class ComputerPlayer(Player):
    def __init__(self, number, speed = 3):
         # the current location
        self.row = random.randint(10, ROWS - 10)
        self.col = random.randint(10, COLS - 10)
        # in the form of (drow, dcol)
        self.dir = random.choice(DIRS)
        self.color = COLORS[number]
        self.dead = False
        self.number = number
        # if not given a name, will be named the same as the number
        self.name = self.number
        self.route = []
        # self.currCenter = self.center
        # self.prevCenter = self.center
        self.counter = random.randint(1, self.largestSteps())

    def changeDir(self):
        possibleMoves = []
        for move in DIRS:
            drow, dcol = move[0], move[1]
            nextRow, nextCol = self.row + drow, self.col + dcol
            if not Player.isDead(self, nextRow, nextCol):
                possibleMoves.append(move)
        if len(possibleMoves) == 0:
            temp = copy.copy(DIRS)
            temp.remove(self.dir)
            self.dir = random.choice(temp)
        else:
            self.dir = random.choice(possibleMoves)

    def largestSteps(self):

        nearestRowTouched = None
        nearestColTouched = None
        # largest = 1

        if self.dir == (-1, 0):
            for row in range(self.row - 1, 0, -1):
                # print(Player.board)
                if Player.board[row][self.col] == 1:
                    nearestRowTouched = row
                    break
            if nearestRowTouched != None:
                largest = self.row - nearestRowTouched - 1
            else:
                largest = self.row - 1

        elif self.dir == (+1, 0):
            for row in range(self.row + 1, ROWS):
                if Player.board[row][self.col] == 1:
                    nearestRowTouched = row
                    break
            if nearestRowTouched != None:
                largest = nearestRowTouched - self.row - 1
            else:
                largest = ROWS - self.row - 1

        elif self.dir == (0, -1):
            for col in range(self.col - 1, 0, -1):
                if Player.board[self.row][col] == 1:
                    nearestColTouched = col
                    break
            if nearestColTouched != None:
                largest = self.col - nearestColTouched - 1
            else:
                largest = self.col - 1

        elif self.dir == (0, +1):
            for col in range(self.col + 1, COLS):
                if Player.board[self.row][col] == 1:
                    nearestColTouched = col
                    break
            if nearestColTouched != None:
                largest = nearestColTouched - self.col - 1
            else:
                largest = COLS - self.col - 1

        return largest

def controlComputerPlayer(player):
    if player.counter == 0:
        player.changeDir()
        largest = player.largestSteps()
        if largest == 0:
            player.counter = 1
        else:
            player.counter = random.randint(1, largest)
