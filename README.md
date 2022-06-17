# Visual Inspection

This python script was created to see how I could detect the presence of a particle within clear liquid solution of a clear glass vial and check the height & width of an clear glass ampoule.

## Particle inspection

We start by capturing an amount of frames from a video source (e.g webcam) i used 4 frames. A standard process for inspection would be somewhere in the region of up to 30 frames for the ability to start detecting trajectory.

The frames are then merged, we can then set a region of interest to reduce the number of false positives / outline of the container or surrounding, crop the image, set to grayscale and thresholded.

## Tip inspection

Capture frames - i used 1 frame
Set image to grayscale, apply threshold
get the bounds of the tip
show height and width

## Installation

Create new python env

```bash
python -m venv env
```

activate env

```bash
source env/bin/activate
```

install requirements

```bash
pip install -r requirements.txt
```

## Running the script

You can use the demo images by renaming the demo_img folder to images.

There is an easy to use GUI to change settings and reprocess images on the fly to test results.

```bash
python main.py
```

## Screenshots

Main GUI - Detection settings are loaded from config.ini and are reloaded on save.

![Main GUI](https://github.com/kevincornish/Visual-Inspection/blob/main/screenshots/main_gui.png?raw=true)

Generate ROI Particle - After clicking reset ROI you click to drag the region of interest for particles and then hit enter.

![Generate ROI Particle](https://github.com/kevincornish/Visual-Inspection/blob/main/screenshots/generating_roi.png?raw=true)

Generate ROI Fill Level - Now you can perform the second ROI for fill level detection, once selected hit enter and then escape to close.

![Generate ROI Fill Level](https://github.com/kevincornish/Visual-Inspection/blob/main/screenshots/generating_roi_level.png?raw=true)

Particle Detection results

![Particle Detection results](https://github.com/kevincornish/Visual-Inspection/blob/main/screenshots/particle_detection.png?raw=true)
