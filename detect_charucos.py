import cv2
import os
import numpy as np
import argparse
from Calibration.calibrator import CharucoCalibrator

def options():

    parser = argparse.ArgumentParser(description='Detect charucos in images')
    parser.add_argument('--images', type=str, default='images', help='Path to the images folder')
    args = parser.parse_args()
    print(args)
    return args

def load_images(images_path):

    images = []
    for i in os.listdir(images_path):
        ipath = os.path.join(images_path,i)
        if ipath.lower().endswith(".jpg") or ipath.lower().endswith(".png:") or ipath.lower().endswith(".jpeg"): 
            images.append(ipath)

    return images

def main():

    args = options()
    images = load_images(args.images)
    calibrator = CharucoCalibrator(7)

    cv2.namedWindow('Charuco detection', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Charuco detection', 800,800)


    for image_name in images:
        img = cv2.imread(image_name)
        corners, ids, rejected = calibrator.detect_charucos(img)
        img_charucos = cv2.aruco.drawDetectedMarkers(img, corners, ids)

        cv2.imshow('Charuco detection', img_charucos)
        cv2.waitKey(0)

if __name__ == '__main__':
    main()
