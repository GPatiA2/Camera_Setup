import cv2
import numpy as numpy
import os


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
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6x6_250)

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

    def calibrate(self, images):

        corners, ids = find_charucos(images)

        size = images[0].shape

        ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(corners, ids, self.board, size, None, None)

        return mtx, dist


