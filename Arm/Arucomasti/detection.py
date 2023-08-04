import cv2 as cv
from cv2 import aruco
import numpy as np

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(marker_dict, params)

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Processing the image
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(
        gray_frame)
    for corners in markerCorners:
        cv.polylines(frame, [corners.astype(np.int32)],
                     True, (255, 255, 0), 4, cv.LINE_AA)
        if markerIds:
            print(markerIds)

    cv.imshow('frame', frame)

    key = cv.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
