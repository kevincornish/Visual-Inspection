import configparser
import tkinter
from tkinter.messagebox import askyesno
from particle import get_roi, set_roi, merge_images, particle_count, show_images, capture_frames, fill_level
config = configparser.ConfigParser()
config_ini = "config.ini"
config.read(config_ini)

def fill_level_settings():
    threshold = config.get("FILL_LEVEL_SETTING","threshold")
    fill_level_window = tkinter.Toplevel()
    fill_level_window.title("Fill Level Settings")
    threshold_label = tkinter.Label(fill_level_window, text="threshold").pack()
    threshold_entry = tkinter.Entry(fill_level_window)
    threshold_entry.insert(0, threshold)
    threshold_entry.pack()

    def saveConfig():
        config.set("FILL_LEVEL_SETTING", "threshold", threshold_entry.get())
        with open(config_ini, "w") as config_file:
            config.write(config_file)

    save_button = tkinter.Button(fill_level_window, text="Save", command=saveConfig).pack()
    close_button = tkinter.Button(fill_level_window, text="Close", command=fill_level_window.destroy).pack(pady=20)

def particle_settings():
    particle_blur = config.get("PARTICLE_SETTING","blur")
    particle_maxvalue = config.get("PARTICLE_SETTING","maxvalue")
    particle_blocksize = config.get("PARTICLE_SETTING","blocksize")
    particle_constant = config.get("PARTICLE_SETTING","constant")
    particle_fromcenter = config.get("PARTICLE_SETTING","fromcenter")
    particle_window = tkinter.Toplevel()
    particle_window.title("Particle Settings")
    particle_blur_label = tkinter.Label(particle_window, text="Blur").pack()
    particle_blur_entry = tkinter.Entry(particle_window)
    particle_blur_entry.insert(0, particle_blur)
    particle_blur_entry.pack()

    particle_fromcenter_label = tkinter.Label(particle_window, text="fromcenter").pack()
    particle_fromcenter_entry = tkinter.Entry(particle_window)
    particle_fromcenter_entry.insert(0, particle_fromcenter)
    particle_fromcenter_entry.pack()

    particle_maxvalue_label = tkinter.Label(particle_window, text="maxvalue").pack()
    particle_maxvalue_entry = tkinter.Entry(particle_window)
    particle_maxvalue_entry.insert(0, particle_maxvalue)
    particle_maxvalue_entry.pack()

    particle_blocksize_label = tkinter.Label(particle_window, text="blocksize").pack()
    particle_blocksize_entry = tkinter.Entry(particle_window)
    particle_blocksize_entry.insert(0, particle_blocksize)
    particle_blocksize_entry.pack()

    particle_constant_label = tkinter.Label(particle_window, text="Constant").pack()
    particle_constant_entry = tkinter.Entry(particle_window)
    particle_constant_entry.insert(0, particle_constant)
    particle_constant_entry.pack()

    def saveConfig():
        config.set("PARTICLE_SETTING", "blur", particle_blur_entry.get())
        config.set("PARTICLE_SETTING", "fromcenter", particle_fromcenter_entry.get())
        config.set("PARTICLE_SETTING", "maxvalue", particle_maxvalue_entry.get())
        config.set("PARTICLE_SETTING", "blocksize", particle_blocksize_entry.get())
        config.set("PARTICLE_SETTING", "constant", particle_constant_entry.get())
        with open(config_ini, "w") as config_file:
            config.write(config_file)

    save_button = tkinter.Button(particle_window, text="Save", command=saveConfig).pack()
    close_button = tkinter.Button(particle_window, text="Close", command=particle_window.destroy).pack(pady=20)


def detection():
    detection_window = tkinter.Toplevel()
    detection_window.title("Detection")
    detection_capture_button = tkinter.Button(detection_window, text="Capture Image", command=capture_frames).pack(pady=5)
    detection_merge_button = tkinter.Button(detection_window, text="Merge Images", command=merge_images).pack(pady=5)
    detection_get_roi_button = tkinter.Button(detection_window, text="Crop ROI", command=get_roi).pack(pady=5)
    detection_reset_roi_button = tkinter.Button(detection_window, text="Reset ROI", command=set_roi).pack(pady=5)
    detection_fill_level_button = tkinter.Button(detection_window, text="Find Fill Level", command=fill_level).pack(pady=5)
    particle_analysis_button = tkinter.Button(detection_window, text="Find Particle", command=particle_count).pack(pady=5)
    particle_show_button = tkinter.Button(detection_window, text="Show Result", command=show_images).pack(pady=5)
    close_button = tkinter.Button(detection_window, text="Close", command=detection_window.destroy).pack(pady=20)

def general_settings():
    debug = config.get("SETTINGS","debug")
    frames = config.get("SETTINGS","frames")
    general_window = tkinter.Toplevel()
    general_window.title("General Settings")

    frames_label = tkinter.Label(general_window, text="frames").pack()
    frames_entry = tkinter.Entry(general_window)
    frames_entry.insert(0, frames)
    frames_entry.pack()

    debug_label = tkinter.Label(general_window, text="debug").pack()
    debug_entry = tkinter.Entry(general_window)
    debug_entry.insert(0, debug)
    debug_entry.pack()

    def saveConfig():
        config.set("SETTINGS", "debug", debug_entry.get())
        config.set("SETTINGS", "frames", frames_entry.get())
        with open(config_ini, "w") as config_file:
            config.write(config_file)

    save_button = tkinter.Button(general_window, text="Save", command=saveConfig).pack()
    close_button = tkinter.Button(general_window, text="close", command=general_window.destroy).pack(pady=20)


button_window = tkinter.Tk()
button_window.title("Visual Inspection")
detection_button = tkinter.Button(button_window, text="Detection", command=detection).pack(pady=5)
general_settings_button = tkinter.Button(button_window, text="General Settings", command=general_settings).pack(pady=5)
particle_settings_button = tkinter.Button(button_window, text="Particle Settings", command=particle_settings).pack(pady=5)
fill_level_settings_button = tkinter.Button(button_window, text="Fill Level Settings", command=fill_level_settings).pack(pady=5)

def close():
    answer = askyesno(title='confirmation', message='Are you sure that you want to quit?')
    if answer:
        try:
            particle_window.destroy()
        except:
            pass
        try:
            general_window.destroy()
        except:
            pass
        try:
            button_window.destroy()
        except:
            pass
        try:
            detection_window.destroy()
        except:
            pass
        try:
            fill_level_window.destroy()
        except:
            pass

exit_button = tkinter.Button(button_window, text="Exit", command=close).pack(pady=20)

if __name__ == '__main__':
    button_window.mainloop()
