# visual-inspection

This python script was created to see how I could detect the presence of a particle within liquid solution.

We start by capturing an amount of frames from a video source (e.g webcam) i used 4 frames. A standard process for inspection would be somewhere in the region of up to 30 frames for the ability to start detecting trajectory.

The frames are then merged, we can then set a region of interest to reduce the number of false positives / outline of the container or surrounding, crop the image, set to grayscale and thresholded.

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

You can use the demo images by renaming the demo_img folder to images, if you want to use your own images, uncomment the capture_frames function and run it.

```python
#capture_frames(frames)
merge_images()
particle_count()
```

To run script using the demo settings

```bash
python main.py
```

To set a new region of interest pass the roi arg

```bash
python main.py --roi yes
```

To show all images processed pass the show arg

```bash
python main.py --show yes
```
