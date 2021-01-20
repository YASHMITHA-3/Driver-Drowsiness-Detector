
from tkinter import *
import dlib
from imutils import face_utils
import numpy as np
import pygame #For playing sound
import os
from scipy.spatial import distance
import time
import cv2
#Initialize Pygame and load music
pygame.mixer.init()
pygame.mixer.music.load('audio/alert.wav')


#Minimum threshold of eye aspect ratio below which alarm is triggerd
EYE_ASPECT_RATIO_THRESHOLD = 0.3

#Minimum consecutive frames for which eye ratio is below threshold for alarm to be triggered
EYE_ASPECT_RATIO_CONSEC_FRAMES = 10

#COunts no. of consecutuve frames below threshold value

counter= 0

#Load face cascade which will be used to draw a rectangle around detected faces.
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])

    ear = (A+B) / (2*C)
    return ear
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#Extract indexes of facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']


# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global Driver_name
    global password
    global Driver_name_entry
    global password_entry
    Driver_name = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter driver details below", bg="yellow").pack()
    Label(register_screen, text="").pack()
    Driver_name_lable = Label(register_screen, text="driver name ")
    Driver_name_lable.pack()
    Driver_name_entry = Entry(register_screen, textvariable=Driver_name)
    Driver_name_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="brown", command = register_user).pack()


# Designing window for login 

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login",bg="yellow").pack()
    Label(login_screen, text="").pack()

    global Driver_name_verify
    global password_verify

    Driver_name_verify = StringVar()
    password_verify = StringVar()

    global Driver_name_login_entry
    global password_login_entry

    Label(login_screen, text="Driver name * ").pack()
    Driver_name_login_entry = Entry(login_screen, textvariable=Driver_name_verify)
    Driver_name_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify,bg="brown").pack()

# Implementing event on register button

def register_user():

    Driver_name_info = Driver_name.get()
    password_info = password.get()

    file = open(Driver_name_info, "w")
    file.write(Driver_name_info + "\n")
    file.write(password_info)
    file.close()

    Driver_name_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

# Implementing event on login button 

def login_verify():
    Driver_name1 = Driver_name_verify.get()
    password1 = password_verify.get()
    Driver_name_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    
    if Driver_name1 in list_of_files:
        file1 = open(Driver_name1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()

# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success",fg="green").pack()
    Button(login_success_screen, text="OK", command=delete_login_success,bg="brown").pack()
    
    video_capture = cv2.VideoCapture(0)

#Give some time for camera to initialize(not required)
    time.sleep(10)

    while(True):
   
    #Read each frame and flip it, and convert to grayscale
        ret, frame = video_capture.read()
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    #Detect facial points through detector function
        faces = detector(gray, 0)

    #Detect faces through haarcascade_frontalface_default.xml
        face_rectangle = face_cascade.detectMultiScale(gray, 1.3, 5)

    #Draw rectangle around each face detected
        for (x,y,w,h) in face_rectangle:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    #Detect facial points
        for face in faces:

            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)

        #Get array of coordinates of leftEye and rightEye
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]

        #Calculate aspect ratio of both eyes
            leftEyeAspectRatio = eye_aspect_ratio(leftEye)
            rightEyeAspectRatio = eye_aspect_ratio(rightEye)

            eyeAspectRatio = (leftEyeAspectRatio + rightEyeAspectRatio) / 2
            cv2.putText(frame, "EAR: {:.2f}".format(eyeAspectRatio), (500, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        #Use hull to remove convex contour discrepencies and draw eye shape around eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        
        #Detect if eye aspect ratio is less than threshold
        
            if(eyeAspectRatio < EYE_ASPECT_RATIO_THRESHOLD):
                counter+= 1
                print(counter)
            #If no. of frames is greater than threshold frames,
                if counter >= EYE_ASPECT_RATIO_CONSEC_FRAMES:
                
                    pygame.mixer.music.play(-1)
                
                    cv2.putText(frame, "You are Drowsy", (150,200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)
                                    
            else:
                
                pygame.mixer.music.stop()
                counter = 0

    #Show video feed
        cv2.imshow('Video', frame)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    cv2.putText(frame, "alert", (150,200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2)
#Finally when video capture is over, release the video capture and destroyAllWindows
    video_capture.release()
    cv2.destroyAllWindows()
# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("password failed")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ",fg="green").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised,bg="brown").pack()

# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("unuccessful")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found",bg="brown").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Deleting popups

def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("driver drowsy system")
    Label(text="Select Your Choice", bg="yellow", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
    main_screen.mainloop()
main_account_screen()
