#!/usr/bin/python3
'''
    College: Fundación Universidad Católica Lumen Gentium - UNICATOLICA
    Faculty: Systems Engineering
    Project Name: Virtual assistant for tetraplegic people controlled by voice and facial gestures (First Phase)
    Module: Facial gesture interface

    Description: Facial gesture interface to control the WhatsApp desktop application (Windows)
    based on Facial Detection and 3D head pose estimation
'''
import collections, cv2, dlib
import pandas as pd
import numpy as np
import math, time
import pyautogui as auto
import pygetwindow as gw
from imutils import face_utils
from libraries import face as face_variables
from libraries import face_detection, pose
from libraries import pose_estimation, read_config
from libraries import plotting, whatsapp, navigation, pc_info, directories

(sx,sy) = auto.size()
WindowName = 'FaceDetection_HeadPose'
imageName = './outputs/Screen_WhatsApp.png'
datasetPath = './resources/datasets/'
soundsPath = './resources/sounds/'

def main():
    # Read file (control_file.ini) to get values for gesture detection,
    # head navigation and debbug mode.
    read_config.readControlFile()

    directories.checkDirectories()

    if face_variables.PERFORMANCE_METERS:
        pc_info.getPC_Info()

    # Open the first webcame device
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    auto.FAILSAFE = False

    if not video_capture.isOpened():
        face_detection.notify("Could not connect to the camera")
        #print("Could not connect to the camera")
        return
    else:
        if face_variables.SHOW_PREVIEW:
            face_detection.notify("Starting live capture")

            # Create two opencv named windows
            cv2.namedWindow(WindowName, cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow('App_ROI', cv2.WINDOW_AUTOSIZE)

            # Position the windows next to eachother
            cv2.moveWindow(WindowName,800,20)

            # Start the window thread for the two windows we are using
            cv2.startWindowThread()

        # Initialize Dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(datasetPath + 'shape_predictor_68_face_landmarks.dat')

        if face_variables.PERFORMANCE_METERS:
            execTimes = []

        while True:
            """
                Facial detection and 3D head pose estimation
            """
            if face_variables.PERFORMANCE_METERS:
                start_general = time.time()

            if face_variables.SHOW_PLOT:
                plotting.frame_counter = plotting.frame_counter + 1

            try:
                # Retrieve the latest image from the webcam
                retval, frame = video_capture.read()
                frame = cv2.flip(frame, 1)  # Flip the camera image

                # Resize the image to 320x240
                frame = cv2.resize(frame, (320, 240))

                # For the face detection, we need to make use of a gray
                #colored image so we will convert the baseImage to a
                #gray-based image
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                #Apply histogram equalization to the gray image to standardize the contrast and brightness of the image,
                #this so that different lighting conditions do not affect the detection of the face in the image,
                #in this way the algorithm is more efficient in detecting the faces present in an image.
                cv2.equalizeHist(gray)

                # Now use the Dlib frontal face detector to find all faces in grayscale in the image
                faces = detector(gray, 0)

                # For now, we are only interested in the 'largest' face, and we determine this based on the largest
                #area of the found rectangle. First initialize the required variables to 0
                maxArea = 0
                faceX = 0
                faceY = 0
                faceW = 0
                faceH = 0

                # Loop over all faces and check if the area for this
                #face is the largest so far
                if len(faces) > 0:
                    for face in faces:
                        (_x, _y, _w, _h) = face_utils.rect_to_bb(face)
                        if _w*_h > maxArea:
                            faceX = int(_x)
                            faceY = int(_y)
                            faceW = int(_w)
                            faceH = int(_h)
                            maxArea = faceW * faceH

                        if maxArea > 0 :
                            # Draw rectangle around the face
                            #cv2.rectangle(frame,(faceX,faceY),(faceX+faceW,faceY+faceH),(255,0,0),2)

                            # Determine the facial landmarks for the face region, then
                            #convert the facial landmark (x, y)-coordinates to a NumPy array
                            shape = predictor(gray, face)
                            shape = face_utils.shape_to_np(shape)

                            # Extract the left and right eye coordinates, then use the
                            #coordinates to compute the eye aspect ratio for both eyes
                            left_eye = shape[face_variables.lStart:face_variables.lEnd]
                            right_eye = shape[face_variables.rStart:face_variables.rEnd]
                            mouth = shape[face_variables.mStart:face_variables.mEnd]

                            # Determine the aspect ratios for eyes and mouth
                            ear_left = face_detection.eye_aspect_ratio(left_eye)  
                            ear_right = face_detection.eye_aspect_ratio(right_eye)
                            mar_mouth = face_detection.mouth_aspect_ratio(mouth)

                            # Average the eye aspect ratio together for both eyes
                            ear = (ear_left + ear_right) / 2.0
                            diff_ear = np.abs(ear_left - ear_right)

                            # Drawing the contours for eyes and mouth
                            left_eye_hull = cv2.convexHull(left_eye)
                            right_eye_hull = cv2.convexHull(right_eye)
                            mouth_hull = cv2.convexHull(mouth)
                            cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
                            cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
                            cv2.drawContours(frame, [mouth_hull], -1, (0, 255, 0), 1)

                            # Starting the head positioning estimation processes
                            shape_first_face = predictor(gray, faces[0])
                            shape = face_utils.shape_to_np(shape_first_face)
                            reprojectdst, euler_angle = pose_estimation.get_head_pose(shape)

                            # Detection face gestures for make control on any app
                            face_detection.eye_gestures_detection(ear, diff_ear, ear_left, ear_right)
                            face_detection.mouth_gestures_detection(mar_mouth)

                # Drawing on frame the facial landmarks points
                for (x, y) in shape:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                # Drawing on frame the cube representing the 3D head pose estimation
                for start, end in pose.line_pairs:
                    cv2.line(frame, reprojectdst[start], reprojectdst[end], (255, 0, 0))

                if face_variables.SHOW_PLOT:
                    plotting.graphGestureSigns(ear_left, ear_right, mar_mouth, plotting.frame_counter)

                if face_variables.SHOW_PREVIEW:
                    # Show data info on the screen
                    face_detection.showDetectionInfo(frame, ear_left, ear_right, mar_mouth, euler_angle)

                    # Split the frame in half both width and height, to help the adjust navigation values.
                    cv2.line(frame, (0, int(frame.shape[0]/2)), (frame.shape[1], int(frame.shape[0]/2)), color=(51, 255, 243), lineType=1, thickness=1)
                    cv2.line(frame, (int(frame.shape[1]/2), 0), (int(frame.shape[1]/2), frame.shape[0]), color=(51, 255, 243), lineType=1, thickness=1)

                    cv2.imshow('App_ROI',img)
                    cv2.imshow(WindowName, frame)

            except Exception as e:
                pass 
                #print('Could not processing Face Detection on Python. \nIssue description: ' + str(e)) 

            """
                Detection of WhatsApp ROI interaction zones
            """
            try:
                # Check if the WhatsApp window is open, get the handler and adjust for better interaction (Human-Machine)
                whatsappIsOpen = whatsapp.hasWhatsAppOpen()
                if whatsapp.hasWhatsAppOpen():
                    whatsappWindow = gw.getWindowsWithTitle(whatsapp.appName)[0]
                    if face_variables.SHOW_PREVIEW:
                        whatsappWindow.moveTo(10, 10)
                    else:
                        whatsappWindow.resizeTo(sx-20, sy-55)
                        whatsappWindow.moveTo(10, 10)
                else:
                    whatsapp.restoreWhatsApp()

                # Take a snapshot WhatsApp to process it
                img, wsx, wsy, wswidth, wsheight = whatsapp.screenCapture(imageName=imageName)
                img = cv2.imread(imageName)

                # The <Informative> region is searched in the WhatsApp snapshot
                x1,y1,width1,height1,flag_info = whatsapp.locateBoxInfo()
                if flag_info == True:
                    auto.press('tab', presses=2)
                elif flag_info == False:
                    #print("<Informative> region not found")

                    # The <Messages> region is searched in the WhatsApp snapshot
                    x2,y2,width2,height2,flag_box = whatsapp.locateBoxMensajes()
                    if flag_box == True:
                        coorX = x2 - wsx
                        coorY = y2 - wsy - 16
                        cv2.rectangle(img, (coorX, wsy + 65), (wswidth - 2, coorY + 16), (0, 0, 255), 2)

                        # Right ROI center location
                        center_w_messages = abs(coorX + width2 / 2)
                        center_h_messages = abs(wsheight / 2)
                    elif flag_box == False:
                        pass
                        #print("<Messages> region not found")

                # The <Contacts> region is searched in the WhatsApp snapshot
                x3,y3,width3,height3,flag_contacts = whatsapp.locateBoxContactos()
                if flag_contacts == True:
                    coorX = x3 - wsx
                    coorY = y3 - wsy - 16
                    cv2.rectangle(img, (coorX, wsy + 118), (coorX + width3 - 2, coorY + 16), (255, 0, 0), 2)

                    # Left ROI center location
                    center_w_contacts = abs(coorX + width3 / 2)
                    center_h_contacts = abs(wsheight / 2)
                elif flag_contacts == False:
                    pass
                    #print("<Contacts> region not found")

            except Exception as e:
                pass
                #print('Could not processing WhatsApp on Python. \nIssue description: ' + str(e))

            """
                Navigation control in WhatsApp regarding Facial Detection
            """
            try:
                # Getting 'X' and 'Y' values from 3D head pose estimation
                navigation.xHeadPosition = round(euler_angle[1, 0],2)
                navigation.yHeadPosition = round(euler_angle[0, 0],2)
                navigation.navigationOnWhatsApp(navigation.xHeadPosition, navigation.yHeadPosition, 
                                                center_w_contacts, center_h_contacts, center_w_messages, center_h_messages)
            except Exception as e:
                pass
                #print('Could not generate navigation. \nIssue description: ' + str(e)) 

            if face_variables.PERFORMANCE_METERS:
                end_general = time.time()
                execTimes.append(end_general-start_general)
                df = pd.DataFrame({'Execution Times' : execTimes})
                df.to_csv('./outputs/measures_times.csv', sep=';', index=False)

            if cv2.waitKey(2) & 0xFF == ord('q'):
                video_capture.release()
                cv2.destroyAllWindows()
                break

        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()