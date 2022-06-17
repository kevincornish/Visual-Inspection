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

You can use the demo images by renaming the demo_img folder to images, if you want to use your own images, uncomment the capture_frames function and run.

To run particle or tip check using the demo settings

```bash
python particle.py
python tip.py
```

To set a new region of interest pass the roi arg

```bash
python particle.py --roi yes
python tip.py --roi yes
```

To show all images processed pass the show arg

```bash
python tip.py --show yes
python particle.py --show yes
```
