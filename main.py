import cv2 # import OpenCV
camera = cv2.VideoCapture(0) # 0 = port

while True:
    result, image = camera.read() # read from camera
    cv2.imshow("input", image) # create gui showing image

    key = cv2.waitKey(10)
    if key == 27: # if esc is hit exit loop
        break

cv2.destroyAllWindows()
cv2.VideoCapture(0).release()
