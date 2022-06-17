import cv2
import pylab
from scipy import ndimage
import time
import configparser
import argparse

## load config
config = configparser.ConfigParser()
config_ini = "config.ini"
config.read(config_ini)
debug = config.get("SETTINGS", "debug")
frames = config.get("SETTINGS", "frames")
camera = cv2.VideoCapture(0)

## check for args passed
parser = argparse.ArgumentParser()
parser.add_argument('--roi', required=False)
parser.add_argument('--show', required=False)
args = parser.parse_args()

def edit_config(setting, parameter, value):
    config.set(setting, parameter, value)
    with open(config_ini, "w") as config_file:
        config.write(config_file)

def capture_frames(frames):
    if debug:
        st = time.time()
    frame = 0
    while frame < frames: # loop until taken enough frames
        frame += 1
        result, image = camera.read() # read from camera
        cv2.imwrite(f"images/{frame}.png", image) # save images
    if debug:
        print(f"{frame} frames captured")
        et = time.time()
        elapsed_time = et - st
        print('Execution time (capture):', elapsed_time, 'seconds')

def merge_images():
    if debug:
        st = time.time()
    img1 = cv2.imread('images/1.png')
    img2 = cv2.imread('images/2.png')
    img3 = cv2.imread('images/3.png')
    img4 = cv2.imread('images/4.png')
    merge1 = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
    merge2 = cv2.addWeighted(img3, 0.5, img4, 0.5, 0)
    merge3 = cv2.addWeighted(merge1, 0.5, merge2, 0.5, 0)
    cv2.imwrite("images/merged1.jpg", merge1)
    cv2.imwrite("images/merged2.jpg", merge2)
    cv2.imwrite("images/merged_all.jpg", merge3)
    if debug:
        print (f"4 frames merged")
        et = time.time()
        elapsed_time = et - st
        print('Execution time (merge):', elapsed_time, 'seconds')

def set_roi():
    merged_all = cv2.imread('images/merged_all.jpg')
    roi = cv2.selectROI(merged_all) # select roi
    roi_cropped = merged_all[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] # crop image
    edit_config("ROI", "y1", str(roi[1]))
    edit_config("ROI", "y2", str(roi[1]+roi[3]))
    edit_config("ROI", "x1", str(roi[0]))
    edit_config("ROI", "x2", str(roi[0]+roi[2]))
    cv2.imwrite("images/roi_cropped.jpg",roi_cropped) # save cropped image

def get_roi():
    merged_all = cv2.imread('images/merged_all.jpg')
    y1 = config.getint("ROI", "y1")
    y2 = config.getint("ROI", "y2")
    x1 = config.getint("ROI", "x1")
    x2 = config.getint("ROI", "x2")
    roi_cropped = merged_all[y1:y2, x1:x2] # crop image
    cv2.imwrite("images/roi_cropped.jpg",roi_cropped) # save cropped image

def particle_count():
    if debug:
        st = time.time()
    blur = config.getint("PARTICLE", "blur")
    maxValue = config.getint("PARTICLE", "maxValue")
    blockSize = config.getint("PARTICLE", "blockSize")# sensitivity
    constant = config.getint("PARTICLE", "constant") # constant to be subtracted
    im = cv2.imread('images/roi_cropped.jpg') #load merged frames
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #convert to gray
    gray = cv2.GaussianBlur(gray, (blur,blur), 0) #add slight blur to clean edges
    im_thresholded = cv2.adaptiveThreshold(gray, maxValue, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, constant)
    labelarray, particle_count = ndimage.label(im_thresholded) # count particles found in ROI window
    cv2.imwrite("images/grayscale.jpg", gray) # save the grayscale image
    cv2.imwrite("images/thresholded.jpg", im_thresholded) # save the thresholded image
    print (f"Particles found: {particle_count}")
    if debug:
        et = time.time()
        elapsed_time = et - st
        print('Execution time (analyse):', elapsed_time, 'seconds')

def show_images():
    im = cv2.imread('images/1.png')
    im_merged = cv2.imread('images/merged_all.jpg')
    gray = cv2.imread('images/grayscale.jpg')
    roi = cv2.imread('images/roi_cropped.jpg')
    im_thresholded = cv2.imread('images/thresholded.jpg')
    cv2.imshow("1st Frame", im)
    cv2.imshow("Merged Frames", im_merged)
    cv2.imshow("Grayscale", gray)
    cv2.imshow("ROI", roi)
    cv2.imshow("Thresholded", im_thresholded)
    cv2.waitKey(0)

#capture_frames(frames)
merge_images()
if args.roi:
    set_roi()
else:
    get_roi()
particle_count()
if args.show:
    show_images()
