import Draw
import cv2
import numpy as np
import pygame
from pygame.locals import *
import sys

# init opencv
cap = cv2.VideoCapture(0)
shape = Draw.getFrame(cap).shape

canvas = Draw.makeWhiteCanvas(shape)
# the points that the pen touched
points = []

# init pygame
pygame.init()
pygame.display.set_caption("openCV App")
screen = pygame.display.set_mode( (shape[1], shape[0]) )

try:
    while True:
        frame =Draw.getFrame(cap)
        red = (0, 0, 255)
        lineweight = 3
        #currFrame = frame
        #prevMask = getBlueArea(prevFrame)
       # prevRect = getRect(prevMask)
        mask = Draw.getBlueArea(frame)
        rect = Draw.getRect(mask, frame)
        if len(rect) > 0:
            centerPoint = Draw.getCenter(rect)
            points.append(centerPoint)
            Draw.drawOnCanvas(canvas, points, lineweight)

        # show pygame window
        screen.fill([0,0,0])
        pyframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Rotate and flip the frame to create mirror effect
        pyframe = cv2.flip(pyframe, 1)
        pyframe = np.rot90(pyframe)
        pyframe = pygame.surfarray.make_surface(pyframe)
        screen.blit(pyframe, (0,0))
        pygame.display.update()

        displayFrame = Draw.drawOnFrame(canvas, frame)

        # opencv Display
        cv2.imshow("drawing", canvas )
        cv2.imshow("original", displayFrame)
        cv2.imshow("masked", mask)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                sys.exit(0)

except(KeyboardInterrupt, SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()
    cv2.waitKey(1)




