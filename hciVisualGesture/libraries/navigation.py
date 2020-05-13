#!/usr/bin/python3
"""
    This module contains function to make navigation on WhatsApp application trough the 3D head pose estimation.
"""
import pyautogui as auto
import time
from libraries import face

ACTIVATE_RIGTH_SIDE = False
ACTIVATE_LEFT_SIDE = False

def navigationOnWhatsApp(xHeadPos, yHeadPos, center_w_contacts, center_h_contacts, center_w_messages, center_h_messages):
    flagHeadX = 0 # [0 = None; 1 = Left; 2 = Right]
    flagHeadY = 0 # [0 = None; 1 = Up;   2 = Down]
    global ACTIVATE_RIGTH_SIDE
    global ACTIVATE_LEFT_SIDE

    xHeadPos = xHeadPos * -1
    yHeadPos = yHeadPos * -1
    if xHeadPos >= face.LEFT_LIMIT_POSITION and xHeadPos <= face.RIGHT_LIMIT_POSITION:
        pass
        #print('The position of the head is in the NEUTRAL zone on the X axis')
    elif xHeadPos < face.LEFT_LIMIT_POSITION:
        #print('The position of the head is in the LEFT zone on the X axis')
        flagHeadX = 1
        # Left ROI Cursor Location
        auto.moveTo(center_w_contacts, center_h_contacts)
        ACTIVATE_RIGTH_SIDE = False
        ACTIVATE_LEFT_SIDE = True
    elif xHeadPos > face.RIGHT_LIMIT_POSITION:
        #print('The position of the head is in the RIGHT zone on the X axis')
        flagHeadX = 2
        # Right ROI cursor location
        auto.moveTo(center_w_messages, center_h_messages)
        ACTIVATE_RIGTH_SIDE = True
        ACTIVATE_LEFT_SIDE = False

    if yHeadPos <= face.UP_LIMIT_POSITION and yHeadPos >= face.DOWN_LIMIT_POSITION:
        pass
        #print('The position of the head is in the NEUTRAL zone on the Y axis')
    elif yHeadPos < face.DOWN_LIMIT_POSITION:
        #print('The position of the head is in the LOWER zone on the Y axis')
        flagHeadY = 2
    elif yHeadPos > face.UP_LIMIT_POSITION:
        #print('The position of the head is in the UPPER zone on the Y axis')
        flagHeadY = 1

    if ACTIVATE_LEFT_SIDE == True and ACTIVATE_RIGTH_SIDE == False:
        if flagHeadY == 2:
            # Hot key (Ctrl + Tab) is generated to move to next contact down
            auto.hotkey('ctrl', 'tab')
            time.sleep(0.5)
        elif flagHeadY == 1:
            # Hot key (Ctrl + Shift + Tab) is generated to move to next contact up
            auto.hotkey('ctrl', 'shift', 'tab')
            time.sleep(0.5)
    
    if ACTIVATE_LEFT_SIDE == False and ACTIVATE_RIGTH_SIDE == True:
        if flagHeadY == 1:
            # Send an Scroll up, to move in the conversation
            auto.scroll(clicks = 200)
            time.sleep(0.25)
        elif flagHeadY == 2:
            # Send an Scroll down, to move in the conversation
            auto.scroll(clicks = -150)
            time.sleep(0.25)
