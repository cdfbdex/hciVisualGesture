#!/usr/bin/python3
"""
    This module reads the (control_file.ini) file, to get the values for declared Variables in {face.py} module.
"""

import configparser
from libraries import face

def readControlFile():
    config = configparser.ConfigParser()
    config.read('./conf/control_file.ini')
    config.sections()

    if 'DEBUG' in config:
        face.SHOW_PREVIEW = config.getboolean('DEBUG', 'SHOW_PREVIEW')
        face.SHOW_PLOT = config.getboolean('DEBUG', 'SHOW_PLOT')
        face.PERFORMANCE_METERS = config.getboolean('DEBUG', 'PERFORMANCE_METERS')

    if 'THRESHOLDS' in config:
        face.EYE_AR_THRESH = config.getfloat('THRESHOLDS', 'EYE_AR_THRESH')
        face.MOUTH_AR_THRESH = config.getfloat('THRESHOLDS', 'MOUTH_AR_THRESH')
        face.WINK_AR_DIFF_THRESH = config.getfloat('THRESHOLDS', 'WINK_AR_DIFF_THRESH')

    if 'FRAMES' in config:
        face.EYE_AR_CONSECUTIVE_FRAMES = config.getint('FRAMES', 'EYE_AR_CONSECUTIVE_FRAMES')
        face.WINK_CONSECUTIVE_FRAMES = config.getint('FRAMES', 'WINK_CONSECUTIVE_FRAMES')
        face.MOUTH_AR_CONSECUTIVE_FRAMES = config.getint('FRAMES', 'MOUTH_AR_CONSECUTIVE_FRAMES')

    if 'NAVIGATION' in config:
        face.LEFT_LIMIT_POSITION = config.getfloat('NAVIGATION', 'LEFT_LIMIT_POSITION')
        face.RIGHT_LIMIT_POSITION = config.getfloat('NAVIGATION', 'RIGHT_LIMIT_POSITION')
        face.UP_LIMIT_POSITION = config.getfloat('NAVIGATION', 'UP_LIMIT_POSITION')
        face.DOWN_LIMIT_POSITION = config.getfloat('NAVIGATION', 'DOWN_LIMIT_POSITION')

