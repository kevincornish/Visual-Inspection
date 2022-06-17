import configparser
import tkinter
from tkinter.messagebox import askyesno
from particle import set_roi, merge_images, particle_count, show_images, capture_frames
config = configparser.ConfigParser()
config_ini = "config.ini"
config.read(config_ini)

def particle_detection():
    particle_blur = config.get("PARTICLE_SETTING","blur")
    particle_maxvalue = config.get("PARTICLE_SETTING","maxvalue")
    particle_blocksize = config.get("PARTICLE_SETTING","blocksize")
    particle_constant = config.get("PARTICLE_SETTING","constant")
    particle_window = tkinter.Toplevel()
    particle_window.title("Particle Settings")
    particle_blur_label = tkinter.Label(particle_window, text="Blur").pack()
    particle_blur_entry = tkinter.Entry(particle_window)
    particle_blur_entry.insert(0, particle_blur)
    particle_blur_entry.pack()

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
        config.set("PARTICLE_SETTING", "maxvalue", particle_maxvalue_entry.get())
        config.set("PARTICLE_SETTING", "blocksize", particle_blocksize_entry.get())
        config.set("PARTICLE_SETTING", "constant", particle_constant_entry.get())
        with open(config_ini, "w") as config_file:
            config.write(config_file)

    save_button = tkinter.Button(particle_window, text="Save", command=saveConfig).pack()

    particle_window_label = tkinter.Label(particle_window, text="Particle Detection").pack()
    particle_capture_button = tkinter.Button(particle_window, text="Capture Image", command=capture_frames).pack()
    particle_merge_button = tkinter.Button(particle_window, text="Merge Images", command=merge_images).pack()
    particle_roi_button = tkinter.Button(particle_window, text="Set ROI", command=set_roi).pack()
    particle_analysis_button = tkinter.Button(particle_window, text="Analyse", command=particle_count).pack()
    particle_show_button = tkinter.Button(particle_window, text="Show Result", command=show_images).pack()
    close_button = tkinter.Button(particle_window, text="Close", command=particle_window.destroy).pack(pady=20)

def general_settings():
    debug = config.get("SETTINGS","debug")
    frames = config.get("SETTINGS","frames")
    general_window = tkinter.Toplevel()
    general_label = tkinter.Label(master=general_window, text="General Settings").pack()

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
particle_detection_button = tkinter.Button(button_window, text="Particle Detection", command=particle_detection).pack()
general_settings_button = tkinter.Button(button_window, text="General Settings", command=general_settings).pack()

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

exit_button = tkinter.Button(button_window, text="Exit", command=close).pack(pady=20)

if __name__ == '__main__':
    button_window.mainloop()
