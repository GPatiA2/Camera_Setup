import cv2
import numpy as numpy
import os
import numpy as np


class ChessboardCalibrator:

    def __init__(self, inner_row, inner_col):
        self.inner_row = inner_row
        self.inner_col = inner_col

    def calibrate(self, images):

        # Arrays to store object points and image points from all the images.
        objpoints = get_objpoints()
        imgpoints = []

        for frame in images:

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (inner_row, inner_col), None)

            # If found, add object points, image points
            if ret == True:
                imgpoints.append(corners)


        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        return mtx, dist



class CharucoCalibrator:

    def __init__(self, num_corners_th):
        # num_corners_th was set to 7 hardcoded
        self.num_corners_th = num_corners_th
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.board = cv2.aruco.CharucoBoard((11,11),.1,.08,self.dictionary)
    
    def find_charucos(self, images):
        
        corner_coords , id_list = [], []
        for i in images:

            cpy = i.copy()
            gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
            cor, ids, rejected = cv2.aruco.detectMarkers(gray, self.dictionary)

            if len(cor) > self.num_corners_th:
                ret, corners, ids = cv2.aruco.interpolateCornersCharuco(cor, ids, gray, self.board)
                if ret > self.num_corners_th:
                    corner_coords.append(corners)
                    id_list.append(ids)

        return corner_coords, id_list

    def calibrate_charuco(self, images):

        corners, ids = self.find_charucos(images)

        size = images[0].shape[0:2]

        ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(corners, ids, self.board, size, None, None)

        return mtx, dist
    
    def read_chessboard(self, images):
        allCorners = []
        allIds = []
        decimator = 0
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
        
        for im in images:
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.dictionary)

            if len(corners)>0:
                res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,self.board)
                if res2[1] is not None and res2[2] is not None and len(res2[1])>6:
                    allCorners.append(res2[1])
                    allIds.append(res2[2])

                decimator += 1

        imsize = gray.shape
        return allCorners,allIds,imsize

    def calibrate(self, images):

        corners, ids, size = self.read_chessboard(images)

        cameraMatrixInit = np.array([[ 1000.,    0., size[0]/2.],
                                 [    0., 1000., size[1]/2.],
                                 [    0.,    0.,           1.]])

        distCoeffsInit = np.zeros((5,1))
        # flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
        flags = (cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)

        (ret, cam_mtx, dist_coef, rot_vec, trans_vec,
         std_dev_int, std_dev_ext, per_point_err) = cv2.aruco.calibrateCameraCharucoExtended(
                charucoCorners= corners, 
                charucoIds= ids, 
                board= self.board,
                imageSize= size,
                cameraMatrix= cameraMatrixInit,
                distCoeffs= distCoeffsInit,
                flags= flags,
                criteria= (cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9)
            )
       
        return cam_mtx, dist_coef


    def detect_charucos(self, image):
       
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cor, ids, rejected = cv2.aruco.detectMarkers(gray, self.dictionary)

        return cor, ids, rejected


