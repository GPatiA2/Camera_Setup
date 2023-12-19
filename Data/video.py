import cv2
import numpy as np
import os

def extract_video_frames(video_path, frame_skip):

    frames = []
    video = cv2.VideoCapture(video_path)

    counter = 0
    extracted = True

    while extracted:

        extracted, frame = video.read()

        if counter % frame_skip == 0:
            frames.append(frame)

        counter += 1

    video.release()

    return frames

def load_frames(path):

    frames = []

    for frame_path in os.listdir(path):
        frame = cv2.imread(os.path.join(path, frame_path))
        frames.append(frame)

    return frames
