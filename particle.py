import cv2
import pylab
from scipy import ndimage
import time
import configparser
from tkinter.messagebox import askyesno, showerror

## load config
config = configparser.ConfigParser()
config_ini = "config.ini"
config.read(config_ini)
debug = config.getboolean("SETTINGS", "debug")
camera = cv2.VideoCapture(0)
img_path = ("images/particle/")

def edit_config(setting, parameter, value):
    config.set(setting, parameter, value)
    with open(config_ini, "w") as config_file:
        config.write(config_file)

def capture_frames():
    answer = askyesno(title='confirmation', message='Are you sure you want to overwrite images?')
    if answer:
        config.read(config_ini)
        frames = config.getint("SETTINGS", "frames")
        debug = config.getboolean("SETTINGS", "debug")
        if debug:
            st = time.time()
        frame = 0
        while frame < frames: # loop until taken enough frames
            frame += 1
            result, image = camera.read() # read from camera
            cv2.imwrite(f"{img_path}{frame}.png", image) # save images
        if debug:
            print(f"{frame} frames captured")
            et = time.time()
            elapsed_time = et - st
            print('Execution time (capture):', elapsed_time, 'seconds')

def merge_images():
    config.read(config_ini)
    debug = config.getboolean("SETTINGS", "debug")
    if debug:
        st = time.time()
    img1 = cv2.imread(f'{img_path}1.png')
    img2 = cv2.imread(f'{img_path}2.png')
    img3 = cv2.imread(f'{img_path}3.png')
    img4 = cv2.imread(f'{img_path}4.png')
    merge1 = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
    merge2 = cv2.addWeighted(img3, 0.5, img4, 0.5, 0)
    merge3 = cv2.addWeighted(merge1, 0.5, merge2, 0.5, 0)
    try:
        cv2.imwrite(f"{img_path}merged1.jpg", merge1)
        cv2.imwrite(f"{img_path}merged2.jpg", merge2)
        cv2.imwrite(f"{img_path}merged_all.jpg", merge3)
    except:
        showerror(title="Error", message="Capture image first")
    else:
        if debug:
            print (f"4 frames merged")
            et = time.time()
            elapsed_time = et - st
            print('Execution time (merge):', elapsed_time, 'seconds')

def set_roi():
    config.read(config_ini)
    debug = config.getboolean("SETTINGS", "debug")
    merged_all = cv2.imread(f'{img_path}merged_all.jpg')
    try:
        roi = cv2.selectROI(merged_all) # select roi
    except:
        showerror(title="Error", message="Merge images first")
    else:
        roi_cropped = merged_all[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] # crop image
        edit_config("PARTICLE_ROI", "y1", str(roi[1]))
        edit_config("PARTICLE_ROI", "y2", str(roi[1]+roi[3]))
        edit_config("PARTICLE_ROI", "x1", str(roi[0]))
        edit_config("PARTICLE_ROI", "x2", str(roi[0]+roi[2]))
        cv2.imwrite(f"{img_path}roi_cropped.jpg",roi_cropped) # save cropped image
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def get_roi():
    config.read(config_ini)
    debug = config.getboolean("SETTINGS", "debug")
    if debug:
        st = time.time()
    merged_all = cv2.imread(f'{img_path}merged_all.jpg')
    y1 = config.getint("PARTICLE_ROI", "y1")
    y2 = config.getint("PARTICLE_ROI", "y2")
    x1 = config.getint("PARTICLE_ROI", "x1")
    x2 = config.getint("PARTICLE_ROI", "x2")
    roi_cropped = merged_all[y1:y2, x1:x2] # crop image
    cv2.imwrite(f"{img_path}roi_cropped.jpg",roi_cropped) # save cropped image
    if debug:
        et = time.time()
        elapsed_time = et - st
        print('Execution time (get_roi):', elapsed_time, 'seconds')

def particle_count():
    config.read(config_ini)
    debug = config.getboolean("SETTINGS", "debug")
    if debug:
        st = time.time()
    blur = config.getint("PARTICLE_SETTING", "blur")
    maxValue = config.getint("PARTICLE_SETTING", "maxValue")
    blockSize = config.getint("PARTICLE_SETTING", "blockSize")# sensitivity
    constant = config.getint("PARTICLE_SETTING", "constant") # constant to be subtracted
    im = cv2.imread(f'{img_path}roi_cropped.jpg') #load merged frames
    try:
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #convert to gray
        gray = cv2.GaussianBlur(gray, (blur,blur), 0) #add slight blur to clean edges
    except:
        showerror(title="Error", message="Set ROI first")
    else:
        im_thresholded = cv2.adaptiveThreshold(gray, maxValue, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, constant)
        labelarray, particle_count = ndimage.label(im_thresholded) # count particles found in ROI window
        text = f"Particles: {particle_count}"
        text_position = (5,15)
        cv2.putText(im_thresholded, text, text_position, fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.5, color = (250,225,100))
        cv2.imwrite(f"{img_path}grayscale.jpg", gray) # save the grayscale image
        cv2.imwrite(f"{img_path}thresholded.jpg", im_thresholded) # save the thresholded image
        if debug == True:
            et = time.time()
            elapsed_time = et - st
            print('Execution time (analysis):', elapsed_time, 'seconds')

def show_images():
    config.read(config_ini)
    im = cv2.imread(f'{img_path}1.png')
    im_thresholded = cv2.imread(f'{img_path}thresholded.jpg')
    try:
        cv2.imshow("1st Frame", im)
        cv2.imshow("Thresholded", im_thresholded)
    except:
        showerror(title="Error", message="Image not taken / analysed")
    else:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
