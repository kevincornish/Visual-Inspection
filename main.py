import cv2
import pylab
from scipy import ndimage
camera = cv2.VideoCapture(0)

def capture_frames(frames):
    frame = 0
    while frame < frames: # 3 frames to capture
        frame += 1
        result, image = camera.read() # read from camera
        cv2.imwrite(f"images/{frame}.png", image)
    print(f"{frame} frames captured")

def particle_count():
    im = cv2.imread('images/1.png') #load image 1
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #convert to gray
    gray = cv2.GaussianBlur(gray, (5,5), 0) #add slight blur to clean edges
    cv2.imwrite("images/grey_2.jpg", gray) # save the grayscale image
    maxValue = 255
    blockSize = 3 # sensitivity
    C = -3 # constant to be subtracted
    im_thresholded = cv2.adaptiveThreshold(gray, maxValue, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, C)
    labelarray, particle_count = ndimage.label(im_thresholded)
    print (f"Particles found: {particle_count}")
    pylab.figure("Original")
    pylab.imshow(im)
    pylab.figure("Grayscale")
    pylab.imshow(gray)
    pylab.figure("Thresholded")
    pylab.imshow(im_thresholded)
    pylab.show()

capture_frames(3)
particle_count()
