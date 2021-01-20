# Driver-Drowsiness-Detector
Many existing systems require a camera which is installed in front of driver.It points straight towards the face of the driver and monitors the driver’s eyes in order to identify the drowsiness which is a distraction.If we place a camera on the window of front glass, the camera blocks the frontal view of driver so it is not practical.
*This program is used to detect drowsiness for any given person. In this program checks how long a person's eyes have been closed for.
*If the eyes have been closed for a long period i.e. beyond a certain threshold value, the program will alert the user by playing an alarm sound.
Flow of the project:-

1.Catch live video of the driver and detecting the location of the Face.

2.Detecting the eyes and creating frames.

3.Calculating EAR when there is eye blink.

4.Comparing EAR with threshold value and generating alarm signal when the calculated EAR value < threshold value

Hence could save as many lives as possible!!

pre requirments :
1.WEBCAM
2.PYTHON IDLE (3.X VERSION)
3. PYTHON MODULES: tkinter , os, scipy.spatial , imutils , numpy , pygame ,time,dlib,cv2.
4.FOLDERS:
  a. Audio
   b. Driver drowsiness detector
  c. shape_predictor_68_face_landmarks
5.XML DOCUMENTS
  a. haarcascade_eye  
  b. haarcascade_frontalface_default
  
 How to run: Download the zip file ->extract the files->run the GUI.PY from python ideal.
