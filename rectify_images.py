from Params.management import ParamsManager
import cv2
import numpy as np
import argparse
import os
from tqdm import tqdm

def options():
    parser = argparse.ArgumentParser(description='Rectify images')
    parser.add_argument('--camera_file', type=str, help='File containing parameters of the camera used to take the pictures')
    parser.add_argument('--images', type=str, default='images', help='Path to the images folder')
    parser.add_argument('--output', type=str, default='output', help='Path to the output folder')
    parser.add_argument('--resize', type=int, nargs='+', default=[0,0], help='Resize the images to the specified size before undistorting') 
    parser.add_argument('--crop_ratio', type=float, default=0.78, help='Crop the image to the specified ratio after undistorting')
    args = parser.parse_args()
    print(args)
    return args


def rectify_image(image, cam_mtx, dist_coeffs, optimal_camera_mtx, roi):

   h,w = image.shape[:2] 
   print(image.shape)
   
   x,y,w,h = roi
   undistorted_img = cv2.undistort(image, cam_mtx, dist_coeffs, None, optimal_camera_mtx)

   undistorted_img_roi = cv2.rectangle(undistorted_img.copy(), (x,y), (x+w,y+h), (0,0,255), 5)

   undistorted_crop = undistorted_img[y:y+h, x:x+w]

   print(undistorted_crop.shape)
   print(undistorted_img.shape)
   print(roi)

   cv2.namedWindow('undistorted image', cv2.WINDOW_NORMAL)
   cv2.namedWindow('croped image', cv2.WINDOW_NORMAL)

   cv2.resizeWindow('croped image', 800,800)
   cv2.resizeWindow('undistorted image', 800,800)

   cv2.imshow('undistorted image', undistorted_img_roi)
   cv2.imshow('croped image', undistorted_crop) 

   cv2.waitKey(0)


   return undistorted_crop

def load_images(images_path):

    images = []
    for i in os.listdir(images_path):
        ipath = os.path.join(images_path,i)
        if ipath.lower().endswith(".jpg") or ipath.lower().endswith(".png:") or ipath.lower().endswith(".jpeg"): 
            images.append(ipath)

    return images

def center_crop(image, crop_ratio):

    h,w = image.shape[:2]
    new_h = int(h*crop_ratio)
    new_w = int(w*crop_ratio)
    y = int((h-new_h)/2)
    x = int((w-new_w)/2)
    return image[y:y+new_h, x:x+new_w]

def main():

    args = options()
    params = ParamsManager(args.camera_file)
    cam_mtx = np.array(params.get_camera_matrix())
    dist_coeffs = np.array(params.get_distortion_coefs())
    resize = tuple(args.resize) != (0,0)
    new_size = tuple(args.resize)

    images = load_images(args.images)
    os.makedirs(args.output, exist_ok=True)

    h,w = cv2.imread(images[0]).shape[:2]

    optimal_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix= cam_mtx, distCoeffs= dist_coeffs,
                                                            imageSize=(w,h), alpha=1, newImgSize=(w,h), centerPrincipalPoint=0)
    for image_name in tqdm(images):
        img = cv2.imread(image_name)
        if resize:
            img = cv2.resize(img, new_size)
        undistorted_img = rectify_image(img, cam_mtx, dist_coeffs, optimal_camera_mtx, roi)
        undistorted_img_crop = center_crop(undistorted_img, args.crop_ratio)
        output_path = os.path.join(args.output, os.path.basename(image_name))
        cv2.imwrite(output_path, undistorted_img_crop)

if __name__ == '__main__':
    main()
