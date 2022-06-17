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
        if debug == True:
            st = time.time()
        frame = 0
        while frame < frames: # loop until taken enough frames
            frame += 1
            result, image = camera.read() # read from camera
            cv2.imwrite(f"{img_path}{frame}.png", image) # save images
        if debug == True:
            print(f"{frame} frames captured")
            et = time.time()
            elapsed_time = et - st
            print('Execution time (capture):', elapsed_time, 'seconds')

def merge_images():
    config.read(config_ini)
    debug = config.getboolean("SETTINGS", "debug")
    if debug == True:
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
        if debug == True:
            print (f"4 frames merged")
            et = time.time()
            elapsed_time = et - st
            print('Execution time (merge):', elapsed_time, 'seconds')

def set_roi():
    config.read(config_ini)
    debug = config.getboolean("SETTINGS", "debug")
    fromcenter = config.getboolean("PARTICLE_SETTING", "fromcenter")
    merged_all = cv2.imread(f'{img_path}merged_all.jpg')
    roi = cv2.selectROIs("test", merged_all, fromcenter) # select roi
    #showerror(title="Error", message="Merge images first")
    roi_cropped = merged_all[int(roi[0][1]):int(roi[0][1]+roi[0][3]), int(roi[0][0]):int(roi[0][0]+roi[0][2])] # crop image
    roi_cropped2 = merged_all[int(roi[1][1]):int(roi[1][1]+roi[1][3]), int(roi[1][0]):int(roi[1][0]+roi[1][2])] # crop image
    edit_config("PARTICLE_ROI", "y1", str(roi[0][1]))
    edit_config("PARTICLE_ROI", "y2", str(roi[0][1]+roi[0][3]))
    edit_config("PARTICLE_ROI", "x1", str(roi[0][0]))
    edit_config("PARTICLE_ROI", "x2", str(roi[0][0]+roi[0][2]))
    edit_config("FILL_LEVEL_ROI", "y1", str(roi[1][1]))
    edit_config("FILL_LEVEL_ROI", "y2", str(roi[1][1]+roi[1][3]))
    edit_config("FILL_LEVEL_ROI", "x1", str(roi[1][0]))
    edit_config("FILL_LEVEL_ROI", "x2", str(roi[1][0]+roi[1][2]))
    if debug == True:
        print(f"PARTICLE - Y1: {int(roi[0][1])} Y2{int(roi[0][1]+roi[0][3])} X1: {int(roi[0][0])} X2: {int(roi[0][0]+roi[0][2])}")
        print(f"FILL LEVEL - Y1: {int(roi[1][1])} Y2{int(roi[1][1]+roi[1][3])} X1: {int(roi[1][0])} X2: {int(roi[1][0]+roi[1][2])}")
    cv2.imwrite(f"{img_path}roi_cropped.jpg",roi_cropped) # save cropped image
    cv2.imwrite(f"{img_path}roi_cropped_fill.jpg",roi_cropped2) # save cropped image
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_roi():
    config.read(config_ini)
    debug = config.getboolean("SETTINGS", "debug")
    if debug == True:
        st = time.time()
    merged_all = cv2.imread(f'{img_path}merged_all.jpg')
    particle_y1 = config.getint("PARTICLE_ROI", "y1")
    particle_y2 = config.getint("PARTICLE_ROI", "y2")
    particle_x1 = config.getint("PARTICLE_ROI", "x1")
    particle_x2 = config.getint("PARTICLE_ROI", "x2")
    fill_y1 = config.getint("FILL_LEVEL_ROI", "y1")
    fill_y2 = config.getint("FILL_LEVEL_ROI", "y2")
    fill_x1 = config.getint("FILL_LEVEL_ROI", "x1")
    fill_x2 = config.getint("FILL_LEVEL_ROI", "x2")
    roi_cropped = merged_all[particle_y1:particle_y2, particle_x1:particle_x2] # crop image to particle ROI
    roi_cropped_fill = merged_all[fill_y1:fill_y2, fill_x1:fill_x2] # crop image to fill level ROI
    cv2.imwrite(f"{img_path}roi_cropped.jpg",roi_cropped) # save cropped image
    cv2.imwrite(f"{img_path}roi_cropped_fill.jpg",roi_cropped_fill) # save cropped image
    if debug == True:
        et = time.time()
        elapsed_time = et - st
        print('Execution time (get_roi):', elapsed_time, 'seconds')

def fill_level():
    if debug == True:
        st = time.time()
    im = cv2.imread(f'{img_path}roi_cropped_fill.jpg')
    threshold = config.getint("FILL_LEVEL_SETTING", "threshold")
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # convert to gray
    if debug == True:
        print('height, width:', gray.shape) #height and width of image
    ret, thresholded = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    x, y, width, height = cv2.boundingRect(thresholded)
    text = f"Height: {height} Width: {width}"
    text_position = (5,15)
    cv2.putText(thresholded, text, text_position, fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.5, color = (250,225,100))
    cv2.imwrite(f"{img_path}thresholded_fill.jpg",thresholded)
    if debug == True:
        et = time.time()
        elapsed_time = et - st
        print('Execution time (fill_level):', elapsed_time, 'seconds')
        print(f"Height: {height} Width: {width}")

def particle_count():
    config.read(config_ini)
    debug = config.getboolean("SETTINGS", "debug")
    if debug == True:
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
            print(f"Particles: {particle_count}")

def show_images():
    config.read(config_ini)
    im = cv2.imread(f'{img_path}1.png')
    im_thresholded = cv2.imread(f'{img_path}thresholded.jpg')
    fill_level = cv2.imread(f'{img_path}thresholded_fill.jpg')
    try:
        cv2.imshow("Original", im)
        cv2.imshow("Particle", im_thresholded)
        cv2.imshow("Fill Level", fill_level)
    except:
        showerror(title="Error", message="Image not taken / analysed")
    else:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
