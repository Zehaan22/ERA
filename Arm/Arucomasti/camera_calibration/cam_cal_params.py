import cv2 as cv
import os
import numpy as np

CHECKER_BOARD_SIZE = (9, 6)

SQUARE_SIZE = 30  # mm
criteria = (cv.TERM_CRITERIA_EPS+cv.TermCriteria_MAX_ITER, 30, 0.001)

calib_data_path = "../calib_data"
CHECK_DIR = os.path.isdir(calib_data_path)

if not CHECK_DIR:
    os.makedirs(calib_data_path)
else:
    print("path exits")


object_3D = np.zeros(
    (CHECKER_BOARD_SIZE[0]*CHECKER_BOARD_SIZE[1], 3), np.float32)
object_3D[:, :2] = np.mgrid[0:CHECKER_BOARD_SIZE[0],
                            0:CHECKER_BOARD_SIZE[1]].T.reshape(-1, 2)

object_3D += SQUARE_SIZE

print(object_3D)

obj_points_3D = []
img_points_2D = []

image_dir_path = "images"

files = os.listdir(image_dir_path)
for file in files:
    print(file)
    imagePath = os.path.join(image_dir_path, file)

    image = cv.imread(imagePath)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(image, CHECKER_BOARD_SIZE, None)
    if ret:
        obj_points_3D.append(object_3D)
        corners2 = cv.cornerSubPix(gray, corners, (3, 3), (-1, -1), criteria)
        img_points_2D.append(corners2)

        img = cv.drawChessboardCorners(
            image, CHECKER_BOARD_SIZE, corners2, ret)

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    obj_points_3D, img_points_2D, gray.shape[::-1], None, None
)
print("caliberated")

print('data backchodi kar rha')
np.savez(
    f"{calib_data_path}/MultiMatrix",
    camMatrix=mtx,
    distCoef=dist,
    rvector=rvecs,
    tvector=tvecs
)

print("----------------------------------------")

print("Data loading backchodi")
data = np.load(f"{calib_data_path}/MultiMatrix.npz")

camMatrix = data["camMatrix"]
distCoef = data["distCoef"]
rVector = data["rVector"]
tVector = data["tVector"]

print("loaded !")
