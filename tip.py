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
frames = config.getint("SETTINGS", "frames")
camera = cv2.VideoCapture(0)
img_path = ("images/tip/")

## check for args passed
parser = argparse.ArgumentParser()
parser.add_argument('--roi',type=str, required=False)
parser.add_argument('--show',type=str, required=False)
parser.add_argument('--capture', type=str, required=False)
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
        cv2.imwrite(f"{img_path}{frame}.jpg", image) # save images
    if debug:
        print(f"{frame} frames captured")
        et = time.time()
        elapsed_time = et - st
        print('Execution time (capture):', elapsed_time, 'seconds')

def set_roi():
    merged_all = cv2.imread(f'{img_path}1.jpeg')
    roi = cv2.selectROI(merged_all) # select roi
    roi_cropped = merged_all[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] # crop image
    edit_config("TIP_ROI", "y1", str(roi[1]))
    edit_config("TIP_ROI", "y2", str(roi[1]+roi[3]))
    edit_config("TIP_ROI", "x1", str(roi[0]))
    edit_config("TIP_ROI", "x2", str(roi[0]+roi[2]))
    cv2.imwrite(f"{img_path}roi_cropped.jpg",roi_cropped) # save cropped image

def get_roi():
    merged_all = cv2.imread(f'{img_path}1.jpeg')
    y1 = config.getint("TIP_ROI", "y1")
    y2 = config.getint("TIP_ROI", "y2")
    x1 = config.getint("TIP_ROI", "x1")
    x2 = config.getint("TIP_ROI", "x2")
    roi_cropped = merged_all[y1:y2, x1:x2] # crop image
    cv2.imwrite(f"{img_path}roi_cropped.jpg",roi_cropped) # save cropped image

def get_height():
    im = cv2.imread(f'{img_path}roi_cropped.jpg')
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # convert to gray
    threshold = config.getint("TIP_SETTING", "threshold")
    #print('height, width:', gray.shape) #height and width of image
    ret, thresholded = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    x, y, width, height = cv2.boundingRect(thresholded)
    cv2.imwrite(f"{img_path}thresholded.jpg",thresholded)
    cv2.imwrite(f"{img_path}grayscale.jpg",gray)
    if debug:
        print('width:', width)
        print('height:', height)

def show_images():
    im = cv2.imread(f'{img_path}1.jpeg')
    roi_cropped = cv2.imread(f'{img_path}roi_cropped.jpg')
    thresholded = cv2.imread(f'{img_path}thresholded.jpg')
    cv2.imshow("1st Frame", im)
    cv2.imshow("ROI cropped", roi_cropped)
    cv2.imshow("thresholded", thresholded)
    cv2.waitKey(0)

if args.capture:
    capture_frames(frames)
if args.roi:
    set_roi()
else:
    get_roi()
get_height()
if args.show:
    show_images()
