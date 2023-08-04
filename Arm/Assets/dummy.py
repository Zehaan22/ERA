import cv2 as cv


cap = cv.VideoCapture(0)

# Loop to continuously get the vide0
while True:
    # Getting the frame from the campera
    ret, frame = cap.read()

    # Displaying the image
    cv.imshow('frame', frame)

    # Endkey break
    if cv.waitKey(1) == ord('q'):
        break

# Quitting all the windows
cap.release()
cv.destroyAllWindows()
