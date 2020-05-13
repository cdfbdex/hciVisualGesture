#!/usr/bin/python3
"""
    This module contains the function to calculate the 3D head pose estimation.
"""
import cv2
import math
import numpy as np
from libraries import pose

def get_head_pose(shape):
    # Dlib shape_predictor can get 68 points of face
    image_pts = np.float32([
        shape[17], shape[21], shape[22], shape[26], shape[36], shape[39],
        shape[42], shape[45], shape[31], shape[35], shape[48], shape[54],
        shape[57], shape[8]
    ])

    _, rotation_vec, translation_vec = cv2.solvePnP(pose.object_pts, image_pts,
                                                    pose.cam_matrix, pose.dist_coeffs)

    # Project 3D points to image plane , output image points
    reprojectdst, _ = cv2.projectPoints(pose.reprojectsrc, rotation_vec,
                                        translation_vec, pose.cam_matrix,
                                        pose.dist_coeffs)
    # Reprojected 2D points
    reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))

    # Calc euler angle
    rotation_mat, _ = cv2.Rodrigues(rotation_vec)
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

    return reprojectdst, euler_angle

