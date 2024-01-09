from Calibration.calibrator import CharucoCalibrator
from Data import video
import argparse
import cv2
import numpy as np
from Params.management import ParamsManager
import json
from pathlib import Path
import os

def options():

    parser = argparse.ArgumentParser(description='Calibrate camera using a video file.')
    parser.add_argument('--args_path', type=str, help='Path to args file.')
    parser.add_argument('--video_path' , type=str, help='Path to video file.')
    parser.add_argument('--frame_skip' , type=int, help='Number of frames to skip.')
    parser.add_argument('--camera_name', type=str, help='Path to output file.')
    parser.add_argument('--min_num_corners', type=int, help='Minimum number of corners to detect.', default = 7)
    parser.add_argument('--extract_frames' , type=bool, help='Extract frames from video.', default = True) 

    opt = parser.parse_args()
    print(opt)
    return opt

def load_args(path):

    with open(path, 'r') as f:
        args = json.load(f)

    opt = Namespace(**args)

    return opt

def main():

    opt = options()

    if opt.args_path is not None:
        opt = load_args(opt.args_path)

    params_file_path = Path('Params/Params_Files/'+opt.camera_name+'.yml')
    params_file_path.touch() 

    p_manager = ParamsManager(params_file_path)
    
    frames = []
    if opt.extract_frames:
        for vp in os.listdir(opt.video_path):
            video_path = os.path.join(opt.video_path, vp)
            extr = video.extract_video_frames(video_path, opt.frame_skip)
            frames.extend(extr[:-1])
    else:
        frames = video.load_frames(opt.video_path)

    if len(frames) == 0:
        print('No frames to calibrate with.')
        return

    calibrator = CharucoCalibrator(opt.min_num_corners)

    matrix, dist_coefs = calibrator.calibrate(frames)

    if matrix is not None:

        params = {
            'cam_name': opt.camera_name,
            'camera_matrix': matrix.tolist(),
            'distortion_coefs': dist_coefs.tolist()
         }

        p_manager.store_camera_params(params)
        p_manager.save_params()

    else:

        print('Calibration failed.')


if __name__ == '__main__':
    main()


