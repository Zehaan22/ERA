import numpy as np
import cv2
from cv2 import aruco
import os

current_path = os.getcwd()

aruco_type = "DICT_4X4_1000"
id_ = 1

arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(arucoDict, parameters)

print("Arucco type '{}' with ID_ '{}'".format(aruco_type, id_))
tag_size = 1000
tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
aruco.generateImageMarker(arucoDict, id_, tag_size, tag, 1)

tag_name = "arucoMarkers/" + aruco_type + "_"+str(id_)+".png"
tag_name = os.path.join(current_path, tag_name)
cv2.imwrite("aruco2.png", tag)

cv2.imshow("aruco2.png", tag)

cv2.waitKey(0)

cv2.destroyAllWindows()
