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

def merge_images():
    img1 = cv2.imread('images/1.png')
    img2 = cv2.imread('images/2.png')
    merge1 = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
    img3 = cv2.imread('images/3.png')
    img4 = cv2.imread('images/4.png')
    merge2 = cv2.addWeighted(img3, 0.5, img4, 0.5, 0)
    cv2.imwrite("images/merged1.jpg", merge1)
    cv2.imwrite("images/merged2.jpg", merge2)
    merge3 = cv2.addWeighted(merge1, 0.5, merge2, 0.5, 0)
    cv2.imwrite("images/merged_all.jpg", merge3)
    print (f"4 frames merged")


def particle_count():
    im = cv2.imread('images/merged_all.jpg') #load merged frames
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #convert to gray
    gray = cv2.GaussianBlur(gray, (5,5), 0) #add slight blur to clean edges
    cv2.imwrite("images/grey_merged.jpg", gray) # save the grayscale image
    maxValue = 255
    blockSize = 3 # sensitivity
    C = -3 # constant to be subtracted
    im_thresholded = cv2.adaptiveThreshold(gray, maxValue, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, C)
    cv2.imwrite("images/threshold_merged.jpg", im_thresholded) # save the thresholded image
    r_o_i = im_thresholded[131:338, 81:265] # grab the region of interest we want
    labelarray, particle_count = ndimage.label(r_o_i) # count particles found in ROI window
    print (f"Particles found: {particle_count}")
    pylab.figure("Merged")
    pylab.imshow(im)
    pylab.figure("Grayscale")
    pylab.imshow(gray)
    pylab.figure("Thresholded")
    pylab.imshow(im_thresholded)
    pylab.figure("ROI")
    pylab.imshow(r_o_i)
#capture_frames(3)
merge_images()
particle_count()
pylab.show()
