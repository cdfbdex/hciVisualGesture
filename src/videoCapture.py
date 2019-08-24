import cv2
import numpy as np

def videoCapture(cameraIndex=0):
  video = cv2.VideoCapture(0)
  valido, imagen = video.read()
  return valido, imagen
