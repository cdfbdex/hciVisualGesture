from hcivisualvesture.videocapture import videocapture
import cv2

valido, image = videocapture(0)
cv2.imshow('Image', image)
cv2.waitKey(0)
