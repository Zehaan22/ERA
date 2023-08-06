import cv2 as cv
from cv2 import aruco
import numpy as np

list1 = [4, 5]  # upper
list2 = [1, 2, 3, 6, 7, 8, 9, 0]  # left
list3 = []  # right
list4 = []  # lower
id_to_cordinate = {
    1: [1, 2],
    2: [3, 4],
    4: [80, 0],
    5: [160, 0],
    3: [1, 2],
    6: [1, 2],
    7: [1, 2],
    8: [1, 2],
    9: [1, 2],
    0: [1, 2],
}


def locate_bot(ids, distance, theta):
    a = id_to_cordinate[ids]
    x1 = a[0]
    y1 = a[1]
    if ids in list1:
        xf = x1-distance*np.sin(theta)
        yf = y1-distance*np.cos(theta)

    if ids in list2:
        xf = distance*np.cos(theta)
        yf = y1-distance*np.sin(theta)

    if ids in list3:
        xf = x1-distance*np.cos(theta)
        yf = y1-distance*np.sin(theta)

    if ids in list4:
        xf = x1-distance*np.sin(theta)
        yf = distance*np.cos(theta)

    return xf, yf


calib_data_path = "../calib_data/MultiMatrix.npz"

calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 9.5  # centimeters

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(marker_dict, params)

cap = cv.VideoCapture(1)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Processing the image
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(
        gray_frame)

    if markerCorners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            markerCorners, MARKER_SIZE, cam_mat, dist_coef
        )
        total_markers = range(0, markerIds.size)
        for ids, corners, i in zip(markerIds, markerCorners, total_markers):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0,
                                                          255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()

            # Since there was mistake in calculating the distance approach point-outed in the Video Tutorial's comment
            # so I have rectified that mistake, I have test that out it increase the accuracy overall.
            # Calculating the distance
            distance = np.sqrt(
                tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
            )

            sa = abs(top_right[0] - top_left[0]) + \
                abs(bottom_left[0] - bottom_right[0])
            si_right = abs(top_right[1] - bottom_right[1])
            si_left = abs(top_left[1] - bottom_left[1])

            if si_right < si_left:
                theta_z = -1 * np.arccos(sa/si_left)
            else:
                theta_z = 1 * np.arccos(sa/si_right)

            location = locate_bot(ids[0], distance, theta_z)
            # print(location)

            # Draw the pose of the marker
            point = cv.drawFrameAxes(
                frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            cv.putText(
                frame,
                f"id: {ids[0]} Dist: {round(distance, 2)}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            cv.putText(
                frame,
                f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                bottom_right,
                cv.FONT_HERSHEY_PLAIN,
                1.0,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )

    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
