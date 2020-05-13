#!/usr/bin/python3
"""
    This module contains global variables of the facial landmarks, as well 
    as variables for control in the detection of facial gestures.
"""
from imutils import face_utils

# Indices of facial reference points for the left eye, the right eye and the mouth respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]

# Counters
TOTAL_LEFT = 0      # Counter of times the left eye has been winked
TOTAL_RIGHT = 0     # Counter of times the right eye has been winked
TOTAL_BOTH = 0      # Counter of times that both eyes have been narrowed
TOTAL_MOUTH = 0     # Counter of times that the mouth has been opened
MOUTH_COUNTER = 0   # Mouth opening counter
EYE_COUNTER = 0     # Counter for both eyes when they narrowed
WINK_COUNTER = 0    # Left or right eye counter when closed

# Flags for functions
INPUT_MODE = False          # For future usage
EYE_CLICK = False           # For future usage
LEFT_WINK = False           # For future usage
RIGHT_WINK = False          # For future usage
SCROLL_MODE = False         # For future usage
MOVE_MOUSE = False          # For future usage

# Thresholds and consecutive frame length for triggering the action.
MOUTH_AR_THRESH = 0                 # 0.60
MOUTH_AR_CONSECUTIVE_FRAMES = 0     # 3
EYE_AR_THRESH = 0                   # 0.22
EYE_AR_CONSECUTIVE_FRAMES = 0       # 5
WINK_AR_DIFF_THRESH = 0             # 0.04
WINK_CONSECUTIVE_FRAMES = 0         # 3

# Flags for debbug mode and getting performance info
SHOW_PREVIEW = None         # False
SHOW_PLOT = None            # False
PERFORMANCE_METERS = None   # False

# Limits for adjust positioning of head respect to the webcam
LEFT_LIMIT_POSITION = 0     # -6.00
RIGHT_LIMIT_POSITION = 0    # 15.00
UP_LIMIT_POSITION = 0       # -5.00
DOWN_LIMIT_POSITION = 0     # -11.50
