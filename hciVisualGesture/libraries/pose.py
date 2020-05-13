#!/usr/bin/python3
"""
    This module contains the constants to calculate the 3D head pose estimation.
"""
import numpy as np

# Camera parameter (intrinsic)
K = [
    6.5308391993466671e+002, 0.0, 3.1950000000000000e+002, 
    0.0, 6.5308391993466671e+002, 2.3950000000000000e+002, 
    0.0, 0.0, 1.0
]
# Distorition coefficients
D = [
    7.0834633684407095e-002, 6.9140193737175351e-002, 0.0, 
    0.0, -1.3073460323689292e+000
]

# Fill in cam intrinsics and distortion coefficients
cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)

# Fill in 3D references points(world coordinates), model referenced from http://aifi.isr.uc.pt/Downloads/OpenGL/glAnthropometric3DModel.cpp
# 3D points referenced by oher model that corresponds to each face landmarks
object_pts = np.float32([[6.825897, 6.760612, 4.402142],    # Point (33) left brow left corner
                        [1.330353, 7.122144, 6.903745],     # Point (29) left brow right corner
                        [-1.330353, 7.122144, 6.903745],    # Point (34) right brow left corner
                        [-6.825897, 6.760612, 4.402142],    # Point (38) right brow right corner
                        [5.311432, 5.485328, 3.987654],     # Point (13) left eye left corner
                        [1.789930, 5.393625, 4.413414],     # Point (17) left eye right corner
                        [-1.789930, 5.393625, 4.413414],    # Point (25) right eye left corner
                        [-5.311432, 5.485328, 3.987654],    # Point (21) right eye right corner
                        [2.005628, 1.409845, 6.165652],     # Point (55) nose left corner
                        [-2.005628, 1.409845, 6.165652],    # Point (49) nose right corner
                        [2.774015, -2.080775, 5.048531],    # Point (43) mouth left corner
                        [-2.774015, -2.080775, 5.048531],   # Point (39) mouth right corner
                        [0.000000, -3.116408, 6.097667],    # Point (45) mouth central bottom corner
                        [0.000000, -7.415691, 4.070434]])   # Point (6) chin corner

# Reproject 3D points world coordinate axis to verify result pose. (For projecting the box on image plane)
reprojectsrc = np.float32([[10.0, 10.0, 10.0], [10.0, 10.0, -10.0],
                        [10.0, -10.0, -10.0], [10.0, -10.0, 10.0],
                        [-10.0, 10.0, 10.0], [-10.0, 10.0, -10.0],
                        [-10.0, -10.0, -10.0], [-10.0, -10.0, 10.0]])

line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], 
            [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]