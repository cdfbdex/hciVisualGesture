#!/usr/bin/python3
"""
    This module contains the necessary functions to process and locate image sections
    in the snapshot of the WhatsApp application to detect the interaction zones
    necessary to generate navigation..
"""
import collections
import os
import pyautogui as auto
import pygetwindow as gw
import subprocess
from libraries import directories

screenWidth, screenHeight = auto.size()
Box = collections.namedtuple('Box', 'left top width height')
appName = 'WhatsApp'
routeApp = "%s\\..\\Local\\WhatsApp\\WhatsApp.exe" % (os.environ['appdata'])
OPEN_WHATSAPP_FLAG = False

def imagesPathFunction(W, H):
    # To avoid compatibility issues with screen resolutions :
    # an image takes more pixels if it’s displayed in 1920x1080 rather than 1366x768 so the pygetwindow.locateOnScreen()
    # function won’t recognize the images captured on a 1366x768 screen if you search for them on a higher resolution screen.
    # This way, the images are captures in 1366x768 so the search area will be the same in 1366x768.
    if W == 1366 and H == 768:
        imagesPathString = './resources/images/' # Set the correct path of images
    else:
        auto.alert(text='Please, set the screen resolution to {1366 x 768} for optimal interface operation and run again this application. Thank you!', title='hciVisualGesture', button='OK')
        directories.closeApp()
        exit()

    return imagesPathString

def screenCapture(imageName):
    wsp = locateWhatsApp()
    return auto.screenshot(imageName, region=(wsp.left, wsp.top, wsp.width, wsp.height)), wsp.left, wsp.top, wsp.width, wsp.height

def locateDots():
    imagesPath = imagesPathFunction(screenWidth, screenHeight)
    dots = auto.locateOnScreen(imagesPath + 'dots.png', grayscale=True)
    if dots == None:
        return False
    else:
        return dots

def locateEmoticon():
    imagesPath = imagesPathFunction(screenWidth, screenHeight)
    emoticon = auto.locateOnScreen(imagesPath + 'emoticon.png', grayscale=True)
    if emoticon == None:
        return False
    else:
        return emoticon

def locateMicro():
    imagesPath = imagesPathFunction(screenWidth, screenHeight)
    microphone = auto.locateOnScreen(imagesPath + 'micro.png', grayscale=True)
    if microphone == None:
        return False
    else:
        return microphone

def locateInfo():
    imagesPath = imagesPathFunction(screenWidth, screenHeight)
    information = auto.locateOnScreen(imagesPath + 'info.png', grayscale=True)
    if information == None:
        return False
    else:
        return information

def locateWhatsApp():
    wsp = gw.getWindowsWithTitle('WhatsApp')[0]
    wsp.restore()
    return wsp

def locateBoxContactos():
    imagesPath = imagesPathFunction(screenWidth, screenHeight)
    wsp = locateWhatsApp()
    busqueda = auto.locateOnScreen(imagesPath + 'find.png', grayscale=True)
    dots = locateDots()

    if dots == False or busqueda == None:
        return 0,0,0,0,False
    else:
        p2x = dots.left + dots.width + 16
        left = wsp.left if wsp.left > 0 else 0
        top = busqueda.top + busqueda.height
        width = p2x - (wsp.left if wsp.left > 0 else 0)
        height = (wsp.top+wsp.height) - top
        return left, top, width, height, True

def locateBoxBusqueda():
    imagesPath = imagesPathFunction(screenWidth, screenHeight)
    wsp = locateWhatsApp()
    busqueda = auto.locateOnScreen(imagesPath + 'find.png', grayscale=True)
    dots = locateDots()

    if dots == False or busqueda == None:
        return 0,0,0,0,False
    else:
        p2x = dots.left + dots.width + 16
        left = wsp.left if wsp.left > 0 else 0
        top = busqueda.top
        width = p2x - (wsp.left if wsp.left > 0 else 0)
        height = busqueda.height
        return left, top, width, height, True

def locateBoxMensajes():
    imagesPath = imagesPathFunction(screenWidth, screenHeight)
    wsp = locateWhatsApp()
    busqueda = auto.locateOnScreen(imagesPath + 'find.png', grayscale=True)
    dots = locateDots()
    emoticon = locateEmoticon()

    if dots == False or emoticon == False or busqueda == None:
        return 0,0,0,0,False
    else:
        p2x = dots.left + dots.width + 16
        left = p2x + 1
        top = busqueda.top
        width = (wsp.left + wsp.width) - left
        height = ((wsp.top + wsp.height) - top) - emoticon.height
        return left, top, width, height, True

def locateBoxInfo():
    wsp = locateWhatsApp()
    busqueda = locateInfo()
    dots = locateDots()

    if dots == False or busqueda == False:
        return 0,0,0,0,False
    else:
        p2x = dots.left + dots.width + 16
        left = p2x + 1
        top = busqueda.top
        width = p2x - (wsp.left if wsp.left > 0 else 0)
        height = (wsp.top+wsp.height) - top
        return left, top, width, height, True

def locateBoxChat():
    wsp = locateWhatsApp()
    dots = locateDots()
    emoticon = locateEmoticon()

    if dots == False or emoticon == False:
        return 0,0,0,0,False
    else:
        p2x = dots.left + dots.width + 16
        left = p2x + 1
        top = emoticon.top
        width = (wsp.left + wsp.width) - left
        height = emoticon.height
        return left, top, width, height, True

def hasWhatsAppOpen():
    apps = gw.getAllTitles()
    for i in range(len(apps)):
        if str(apps[i]) == appName or len(str(apps[i])) == len(appName):
            return len(gw.getWindowsWithTitle(appName)) > 0

def restoreWhatsApp():
    if hasWhatsAppOpen():
        gw.getWindowsWithTitle(appName)[0].activate()
        gw.getWindowsWithTitle(appName)[0].maximize()
        OPEN_WHATSAPP_FLAG = False
    else:
        OPEN_WHATSAPP_FLAG = True
        if OPEN_WHATSAPP_FLAG == True:
            subprocess.Popen([routeApp])
            OPEN_WHATSAPP_FLAG = False
