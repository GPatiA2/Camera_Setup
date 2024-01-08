from Params.management import ParamsManager
import cv2
import numpy as np
import argparse

def options():
    parser = argparse.ArgumentParser(description='Rectify images')
    parser.add_argument('--camera_file', type=str, help='File containing parameters of the camera used to take the pictures')
    parser.add_argument('--images', type=str, default='images', help='Path to the images folder')
    parser.add_argument('--output', type=str, default='output', help='Path to the output folder')
    args = parser.parse_args()
    print(args)
    return args


def rectify_image(image, cam_mtx, dist_coeffs):

   h,w = image.shape[:2] 
   optimal_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(cam_mtx, dist_coeffs, (w,h), 1, (w,h)) 
   undistorted_img = cv2.undistort(image, cam_mtx, dist_coeffs, None, optimal_camera_mtx)
   crop_undistorted_img = undistorted_img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
   return crop_undistorted_img

def load_images(images_path):

    images = []
    for i in os.listdir(images_path):
        ipath = os.path.join(images_path,i)
        if ipath.lower().endswith(".jpg") or ipath.lower().endswith(".png:") or ipath.lower().endswith(".jpeg"): 
            images.append(ipath)

    return images

def main():

    args = options()
    params = ParamsManager(args.camera_file)
    cam_mtx = np.array(params.get('cam_mtx'))
    dist_coeffs = np.array(params.get('dist_coeffs'))

    images = load_images(args.images)
    os.makedirs(args.output, exist_ok=True)

    for image_name in images:
        img = cv2.imread(image_name)
        undistorted_img = rectify_image(img, cam_mtx, dist_coeffs)
        output_path = os.path.join(args.output, os.path.basename(image_name))
        cv2.imwrite(output_path, undistorted_img)

if __name__ == '__main__':
    main()
