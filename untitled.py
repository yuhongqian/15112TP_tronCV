# from https://docs.opencv.org/trunk/db/df8/tutorial_py_meanshift.html
def trackRect(frame, trackWindow = None):
    mask = getBlueArea(frame)
    if trackWindow == None and getInitialRoi(mask) != None:
        trackWindow = getInitialRoi(mask)
    if trackWindow != None:
        x, y, w, h = trackWindow
        # set up the ROI for tracking
        roi = frame[y:y+h, x:x+w]
        hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvRoi, lower, upper)
        roiHist = cv2.calcHist([hsvRoi], [0], mask, [180], [0,180])
        cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)

        # set up the termination criteria, either 10 iteration or move by at least
        # 1 pt
        termCrit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)

        # apply camshift to get the new location
        ret, trackWindow = cv2.CamShift(dst, trackWindow, termCrit)

        # draw the outline on the img
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        cv2.polylines(frame, [pts], True, 255, 2)
