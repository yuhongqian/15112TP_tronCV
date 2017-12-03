import cv2
import numpy as np

# get the current frame from webcam capture
def getFrame(cap):
    ret, frame = cap.read()
    scalingFactor = 0.5
    frame = cv2.resize(frame, None, fx = scalingFactor, fy = scalingFactor,
        interpolation = cv2.INTER_AREA)
    frame = cv2.flip(frame, 1)
    return frame

# Return a masked img where only the blue areas are visible
def getBlueArea(img):
    # convert the bgr img to hsv
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([100, 100, 100])
    upper = np.array([130, 230, 240])
    # create the mask
    mask = cv2.inRange(hsvImg, lower, upper)
    # apply the mask to the img
    res = cv2.bitwise_and(img, img, mask = mask)

    return res

# return the contour of the blue rectangle
# and draw the rectangle outline
def getRect(maskedImg, frame):
    # convert to gray img for easier processing
    bgr = cv2.cvtColor(maskedImg, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # reduce noise using a Gaussian filtering
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    # remove the blobs
    thresh = cv2.erode(thresh, None, iterations = 2)
    thresh = cv2.dilate(thresh, None, iterations = 2)
    # extract contours
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contour = max(contours, key = cv2.contourArea)
        # peri = cv2.arcLength(contour, True)
        # approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        # if len(approx) == 4:
        rect = cv2.minAreaRect(contour)
        box  = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.polylines(frame, [box], 0, 255, 2)
        return box
    return []

# get the center of the detected rectangle
def getCenter(box):
    leftTopPt, rightBottomPt = box[2], box[0]
    xc = (leftTopPt[0] + rightBottomPt[0]) // 2
    yc = (leftTopPt[1] + rightBottomPt[1]) // 2
    return (xc, yc)

# draw on a (invisible) white canvas
def drawOnCanvas(canvas, points, lineweight):
    if len(points) > 1:
        for i in range(1, len(points)):
            cv2.line(canvas, points[i - 1], points[i], (0, 0, 255), lineweight)

# put the drawong on the top of the scene
def drawOnFrame(canvas, frame):
    grayCanvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    cv2.imshow("grayCanvas", grayCanvas)
    _, mask = cv2.threshold(grayCanvas, 254, 255, cv2.THRESH_BINARY)
    cv2.imshow("canvasmask", mask)
    maskInv = cv2.bitwise_not(mask)
    # the drawn part becomes invisible
    scene = cv2.bitwise_and(frame, frame, mask = mask)
    # the background in the drawing becomes invisible
    drawing = cv2.bitwise_and(canvas, canvas, mask = maskInv)
    return cv2.add(scene, drawing)

# make a white canvas
def makeWhiteCanvas(shape):
    canvas = np.zeros(shape, dtype =  "uint8")
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    canvas = cv2.bitwise_not(canvas)
    canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
    return canvas




