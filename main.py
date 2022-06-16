import cv2
import pylab
from scipy import ndimage
import time
st = time.time()
camera = cv2.VideoCapture(0)
debug = True

def capture_frames(frames):
    frame = 0
    while frame < frames: # loop until taken enough frames
        frame += 1
        result, image = camera.read() # read from camera
        cv2.imwrite(f"images/{frame}.png", image) # save images
    if debug:
        print(f"{frame} frames captured")

def merge_images():
    img1 = cv2.imread('images/1.png')
    img2 = cv2.imread('images/2.png')
    img3 = cv2.imread('images/3.png')
    img4 = cv2.imread('images/4.png')
    merge1 = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
    merge2 = cv2.addWeighted(img3, 0.5, img4, 0.5, 0)
    merge3 = cv2.addWeighted(merge1, 0.5, merge2, 0.5, 0)
    if debug:
        cv2.imwrite("images/merged1.jpg", merge1)
        cv2.imwrite("images/merged2.jpg", merge2)
        cv2.imwrite("images/merged_all.jpg", merge3)
        print (f"4 frames merged")


def particle_count():
    im = cv2.imread('images/merged_all.jpg') #load merged frames
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #convert to gray
    gray = cv2.GaussianBlur(gray, (3,3), 0) #add slight blur to clean edges
    maxValue = 255
    blockSize = 21 # sensitivity
    C = -23 # constant to be subtracted
    im_thresholded = cv2.adaptiveThreshold(gray, maxValue, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
    r_o_i = im_thresholded[131:338, 81:265] # grab the region of interest we want
    labelarray, particle_count = ndimage.label(r_o_i) # count particles found in ROI window
    if debug:
        cv2.imwrite("images/grey_merged.jpg", gray) # save the grayscale image
        cv2.imwrite("images/threshold_merged.jpg", im_thresholded) # save the thresholded image
    print (f"Particles found: {particle_count}")


def show_images():
    im = cv2.imread('images/1.png')
    im_merged = cv2.imread('images/merged_all.jpg')
    gray = cv2.imread('images/grey_merged.jpg')
    im_thresholded = cv2.imread('images/threshold_merged.jpg')
    r_o_i = im_thresholded[131:338, 81:265]
    pylab.figure("1st Frame")
    pylab.imshow(im)
    pylab.figure("Merged Frames")
    pylab.imshow(im_merged)
    pylab.figure("Grayscale")
    pylab.imshow(gray)
    pylab.figure("Thresholded")
    pylab.imshow(im_thresholded)
    pylab.figure("ROI")
    pylab.imshow(r_o_i)
    pylab.show()
#capture_frames(3)
merge_images()
particle_count()
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
show_images()
