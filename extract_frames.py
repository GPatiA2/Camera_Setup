import cv2
import os
import numpy as np
import argparse
from tqdm import tqdm

def options():
    
    parser = argparse.ArgumentParser(description='Calibrate camera using a video file.')
    parser.add_argument('--video_path' , type=str, help='Path to video directory.')
    parser.add_argument('--frame_skip' , type=int, help='Number of frames to skip.')
    parser.add_argument('--output_path' , type=str, help='Path to output directory.')
    args = parser.parse_args()
    print(args)
    return args

def get_video_names(path):
    video_names = []
    for i in os.listdir(path):
        ipath = os.path.join(path,i)
        if ipath.lower().endswith(".mp4") or ipath.lower().endswith(".avi"): 
            video_names.append(ipath)
    return video_names

def extract_video_frames(video_path, frame_skip):
    vidcap = cv2.VideoCapture(video_path)
    success,image = vidcap.read()
    count = 0
    frames = []
    while success:
        if count % frame_skip == 0:
            frames.append(image)
        success,image = vidcap.read()
        count += 1
    return frames

def main():

    args = options()
    video_names = get_video_names(args.video_path)
    os.makedirs(args.output_path, exist_ok=True)
    frames = []
    for video_name in tqdm(video_names):
        frames.extend(extract_video_frames(video_name, args.frame_skip))

    print("Extracted "+str(len(frames))+" frames from "+str(len(video_names))+" videos")

    for i, frame in enumerate(frames):
        cv2.imwrite(os.path.join(args.output_path, 'frame'+str(i)+'.jpg'), frame)

    print("Saved "+str(len(frames))+" frames to "+args.output_path)

if __name__ == '__main__':
    main()
