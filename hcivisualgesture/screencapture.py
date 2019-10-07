import pyautogui as auto
import pygetwindow as gw
import collections
import time
Box = collections.namedtuple('Box', 'left top width height')


def screencapture(imageName):
    wsp = locateWhatsApp()
    return auto.screenshot(imageName, region=(wsp.left, wsp.top, wsp.width, wsp.height))


def locateDots():
    return auto.locateOnScreen('./resources/images/dots.png')


def locateEmoticon():
    return auto.locateOnScreen('./resources/images/emoticon.png')


def locateMicro():
    return auto.locateOnScreen('./resources/images/micro.png')


def locateWhatsApp():
    wsp = gw.getWindowsWithTitle('WhatsApp')[0]
    wsp.restore()
    time.sleep(0.2)
    return wsp


def locateBoxContactos():
    wsp = locateWhatsApp()
    busqueda = auto.locateOnScreen('./resources/images/busqueda.png')
    dots = locateDots()
    print(dots)
    p2x = dots.left + dots.width + 16
    left = wsp.left if wsp.left > 0 else 0
    top = busqueda.top + busqueda.height
    width = p2x - (wsp.left if wsp.left > 0 else 0)
    height = (wsp.top+wsp.height) - top
    return Box(left, top, width, height)


def locateBoxBusqueda():
    wsp = locateWhatsApp()
    busqueda = auto.locateOnScreen('./resources/images/busqueda.png')
    dots = locateDots()
    p2x = dots.left + dots.width + 16
    left = wsp.left if wsp.left > 0 else 0
    top = busqueda.top
    width = p2x - (wsp.left if wsp.left > 0 else 0)
    height = busqueda.height
    return Box(left, top, width, height)


def locateBoxMensajes():
    wsp = locateWhatsApp()
    busqueda = auto.locateOnScreen('./resources/images/busqueda.png')
    dots = locateDots()
    emoticon = locateEmoticon()
    p2x = dots.left + dots.width + 16
    left = p2x + 1
    top = busqueda.top
    width = (wsp.left + wsp.width) - left
    height = ((wsp.top + wsp.height) - top) - emoticon.height
    return Box(left, top, width, height)


def locateBoxChat():
    wsp = locateWhatsApp()
    busqueda = auto.locateOnScreen('./resources/images/busqueda.png')
    dots = locateDots()
    emoticon = locateEmoticon()
    p2x = dots.left + dots.width + 16
    left = p2x + 1
    top = emoticon.top
    width = (wsp.left + wsp.width) - left
    height = emoticon.height
    return Box(left, top, width, height)
