import cv2
import numpy as numpy

class Rectifier:

    def __init__(self, cam_mtx, dist_params):

        self.cam_mtx = cam_mtx
        self.dist_params = dist_params

    def rectify(self, image : np.ndarray) -> np.ndarray:
        
        image_cpy = image.copy()
        orig_h, orig_w = image_cpy.shape[:2]
        o_cam_mtx, roi = cv2.getOptimalNewCameraMatrix(self.cam_mtx, self.dist_params, (orig_w, orig_h), 1, (orig_w, orig_h))
        rectified_img  = cv2.undistort(image_cpy, self.cam_mtx, self.dist_params, None, o_cam_mtx)
        x, y, w, h = roi
        rectified_img = rectified_img[y:y+h, x:x+w]
        return rectified_img 

    def optimalMatrix(self, h, w):

        return cv2.getOptimalNewCameraMatrix(self.cam_mtx, self.dist_params, (orig_w, orig_h), 1, (orig_w, orig_h))


