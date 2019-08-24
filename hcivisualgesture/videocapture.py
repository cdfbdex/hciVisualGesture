import cv2
import numpy as np

def videocapture(cameraIndex=0):
  video = cv2.VideoCapture(0)
  valido, imagen = video.read()
  video.release()
  return valido, imagen
