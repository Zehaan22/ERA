"""File to find the centre of the object that the system auto-recognises."""

# importing various libraries
import numpy as np
import cv2

# Getting the image capture device
cap = cv2.VideoCapture(0)

# Loading the template images
'''templates = []
for i in range(1, 3):
    tempate = cv2.imread('Assets/img'+str(i)+'.jpg',0)
    templates.append(tempate)'''

template = cv2.imread('Assets/img1.jpeg', 0)
template = cv2.resize(template, (0, 0), fx=0.1, fy=0.1)

h, w = template.shape

# Loop to continuously get the vide0
while True:
    # Getting the frame from the campera
    ret, frame = cap.read()

    # Processing the image
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    location = max_loc

    bottom_right = (location[0] + w, location[1] + h)
    cv2.rectangle(frame, location, bottom_right, 255, 2)

    # Displaying the image
    cv2.imshow('frame', frame)

    # Endkey break
    if cv2.waitKey(1) == ord('q'):
        break


# Quitting all the windows
cap.release()
cv2.destroyAllWindows()
