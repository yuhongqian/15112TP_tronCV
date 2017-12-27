import cv2
import numpy as np
import math
from Constants import *

class cvWebcam(object):
    def __init__(self, numPlayers, game):
        self.cap = cv2.VideoCapture(0)
        self.frame = self.getFrame()
        self.copiedFrame = self.frame.copy()
        # self.maskedFrame = self.getBlueArea()
        # self.rect = self.getRect(self.maskedFrame, self.frame)
        # self.center = self.getCenter(self.rect)
        self.numPlayers = numPlayers
        self.game = game
        self.loadArrows()
        self.ROIs = self.getROI()
        self.drawUI()

    def loadArrows(self):
        self.upArrow = cv2.imread("images/up.jpg")
        self.downArrow = cv2.imread("images/down.jpg")
        self.leftArrow = cv2.imread("images/left.jpg")
        self.rightArrow = cv2.imread("images/right.jpg")
        self.arrows = [self.upArrow, self.downArrow,
                      self.leftArrow, self.rightArrow]


    # divide the frame and get the ROIs (each pertains to a player)
    # and draw on ROIs
    def getROI(self):
        ROIs = [None] * self.numPlayers
        for i in range(self.numPlayers):
           frameHeight = self.frame.shape[0]
           frameWidth = self.frame.shape[1]
           roiHeight =  frameHeight
           roiWidth = frameWidth // self.numPlayers
           startRow = 0
           startCol = 0 + i * roiWidth
           ROIs[i] = self.frame[startRow : startRow + roiHeight,
                               startCol : startCol + roiWidth]
        return ROIs

    def drawUI(self):
        margin = 40
        ROIs = self.ROIs
        for i in range(self.numPlayers):
           frameHeight = self.frame.shape[0]
           frameWidth = self.frame.shape[1]
           roiHeight =  frameHeight
           roiWidth = frameWidth // self.numPlayers
           startRow = 0
           startCol = 0 + i * roiWidth
           x0 =  startCol + margin
           y0 =  frameHeight - 40
           cv2.putText(self.copiedFrame, text = "Player %s" % i, org = (x0, y0),
                       fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 1,
                       color = NUM_COLORS[i], thickness = 2)
           if i != 0:
               cv2.line(self.copiedFrame, pt1 = ( startCol, 0 ),
                       pt2 = (startCol, frameHeight),
                       color = (255,255,255) )
           # print(i, len(self.game.players))
           self.drawArrows(startCol, startRow, roiWidth, roiHeight)

    # from https://www.packtpub.com/mapt/book/application_development/
    # 9781785283932/4/ch04lvl1sec37/fun-with-faces
    # returns a copy of frame with arrows drawn on it
    def drawArrowOnROI(self, x, y, w, h, arrowImg):
        ROI = self.frame[y:y+h, x:x+w]
        # Convert color img to grayscale and threshold it
        grayArrow = cv2.cvtColor(arrowImg, cv2.COLOR_BGR2GRAY)
        # create a mask
        # colored things becomes black (0)
        ret, mask, = cv2.threshold(grayArrow, 200, 255, cv2.THRESH_BINARY_INV)
        # create an inverse mask
        maskInv = cv2.bitwise_not(mask)
        maskedArrow = cv2.bitwise_and(arrowImg, arrowImg, mask = mask)
        maskedROI = cv2.bitwise_and(ROI, ROI, mask = maskInv)
        self.copiedFrame[y:y+h, x:x+w] = cv2.add(maskedArrow, maskedROI)

    # x, y, w, h mark the target ROI
    def drawArrows(self, x, y, w, h):
        arrowShape = self.upArrow.shape[:2]
        arrowH = arrowShape[0]
        arrowW = arrowShape[1]
        arrowSize = max(arrowH, arrowW)
        gap = arrowSize // 2
        cx, cy = x + w // 2, y + h // 2
        # draw up arrow
        xUp = cx - arrowSize // 2
        yUp = cy - gap - arrowSize
        self.drawArrowOnROI(xUp, yUp, arrowW, arrowH, self.upArrow)
        # draw down arrow
        xDown = cx - arrowSize // 2
        yDown = yUp + arrowSize * 2
        self.drawArrowOnROI(xDown, yDown, arrowW, arrowH, self.downArrow)
        # draw left arrow
        xLeft = cx - gap - arrowSize
        yLeft = cy - arrowSize // 2
        self.drawArrowOnROI(xLeft, yLeft, arrowW, arrowH, self.leftArrow)
        # draw right arrow
        xRight = xLeft + arrowSize * 2
        yRight = cy - arrowSize // 2
        self.drawArrowOnROI(xRight, yRight, arrowW, arrowH, self.rightArrow)

    # get the current frame from webcam capture
    def getFrame(self):
        ret, frame = self.cap.read()
        scalingFactor = 0.5
        frame = cv2.resize(frame, None, fx = scalingFactor, fy = scalingFactor,
            interpolation = cv2.INTER_AREA)
        frame = cv2.flip(frame, 1)
        return frame

    def updateWebcam(self):
        # update the webcam
        self.frame = self.getFrame()
        self.copiedFrame = self.frame.copy()
        # self.maskedFrame = self.getBlueArea()
        # self.rect = self.getRect(self.maskedFrame, self.frame)
        self.getROI()

# draw on a (invisible) white canvas
def drawOnCanvas(canvas, points, lineweight):
    if len(points) > 1:
        for i in range(1, len(points)):
            cv2.line(canvas, points[i - 1], points[i], (0, 0, 255), lineweight)





