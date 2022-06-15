import cv2 # import OpenCV
camera = cv2.VideoCapture(0) # 0 = port

frame = 0
while True:
    frame += 1
    result, image = camera.read() # read from camera
    cv2.imshow("input", image) # create gui showing image
    cv2.imwrite(f"images/{frame}.png", image)
    print(f"image saved {frame}")

    key = cv2.waitKey(10)
    if key == 27 or frame == 30: # if esc is hit or 30 frames taken exit loop
        break

cv2.destroyAllWindows()
cv2.VideoCapture(0).release()
