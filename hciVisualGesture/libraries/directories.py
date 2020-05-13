#!/usr/bin/python3
"""
    This module contain function to validate the app directories. If they don't exist, then they are created.
    Also includes a function called closeApp for exit from de application.
"""
import os
import psutil

def checkDirectories():
    if not os.path.exists('./conf'): os.makedirs('./conf')
    if not os.path.exists('./doc'): os.makedirs('./doc')
    if not os.path.exists('./outputs'): os.makedirs('./outputs')
    if not os.path.exists('./resources'): os.makedirs('./resources')

def closeApp():
    try:
        PROCNAME = 'hciVisualGesture.exe'
        for proc in psutil.process_iter():
            # Check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()
    except:
        pass