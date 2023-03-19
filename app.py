 
from itertools import tee
from flask import Flask, render_template, Response, request, redirect, url_for, session, flash
import cv2
import math
import cv2
import numpy as np
from time import time
import speech_recognition
import mediapipe as mp
import matplotlib.pyplot as plt
#pip install nltk
import nltk
#pip install playsound
from playsound import playsound
import speech_recognition
# pip install flask-mysqldb
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import re
  

nltk.download('omw-1.4')
recognizer = speech_recognition.Recognizer()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True,
                    min_detection_confidence=0.3, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils


def detectPose(image, pose, display=True):

    # Create a copy of the input image.
    output_image = image.copy()

    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform the Pose Detection.
    results = pose.process(imageRGB)

    # Retrieve the height and width of the input image.
    height, width, _ = image.shape

    # Initialize a list to store the detected landmarks.
    landmarks = []

    # Check if any landmarks are detected.
    if results.pose_landmarks:

        # Draw Pose landmarks on the output image.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)

        # Iterate over the detected landmarks.
        for landmark in results.pose_landmarks.landmark:

            # Append the landmark into the list.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))

    # Check if the original input image and the resultant image are specified to be displayed.
    if display:

        # Display the original input image and the resultant image.
        plt.figure(figsize=[30, 30])
        plt.subplot(121); plt.imshow(
            image[:, :, ::-1]); plt.title("Original Image"); plt.axis('off');
        plt.subplot(122); plt.imshow(
            output_image[:, :, ::-1]); plt.title("Output Image"); plt.axis('off');

        # Also Plot the Pose landmarks in 3D.
        mp_drawing.plot_landmarks(
            results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    # Otherwise
    else:

        # Return the output image and the found landmarks.
        return output_image, landmarks


def calculateAngle(landmark1, landmark2, landmark3):

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))

    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360

    # Return the calculated angle.
    return angle


def classifyPose(landmarks, output_image, display=False):

    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)

    # Calculate the required angles.
    # ----------------------------------------------------------------------------------------------------------------

    # Get the angle between the left shoulder, elbow and wrist points.
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    # Get the angle between the right shoulder, elbow and wrist points.
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

    # Get the angle between the left elbow, shoulder and hip points.
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points.
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points.
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    # ----------------------------------------------------------------------------------------------------------------

    # Check if it is the warrior II pose or the T pose.
    # As for both of them, both arms should be straight and shoulders should be at the specific angle.
    # ----------------------------------------------------------------------------------------------------------------

    # Check if the both arms are straight.
    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:

        # Check if shoulders are at the required angle.
        if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:

    # Check if it is the warrior II pose.
    # ----------------------------------------------------------------------------------------------------------------

            # Check if one leg is straight.
            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

                # Check if the other leg is bended at the required angle.
                if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:

                    # Specify the label of the pose that is Warrior II pose.
                    # Bot says the name of the pose and asks if user wants more information
                    label = 'Warrior II Pose'
                    with speech_recognition.Microphone() as mic:
                            playsound(r"E:\all_proj\HTML Programming\YOGI\wp.mp3")#directory ka naam daalna and save the audio files in the same folder as your
                            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                            audio = recognizer.listen(mic)
                            message = recognizer.recognize_google(audio)
                            if (message == "yes" or message == "sure"):
                                playsound(r"E:\all_proj\HTML Programming\YOGI\wpYes.mp3")
                            else:
                                playsound(r"E:\all_proj\HTML Programming\YOGI\No.mp3")
                

    # ----------------------------------------------------------------------------------------------------------------

    # Check if it is the T pose.
    # ----------------------------------------------------------------------------------------------------------------

            # Check if both legs are straight
            if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:

                # Specify the label of the pose that is tree pose.
                label = 'T Pose'
                with speech_recognition.Microphone() as mic:
                            playsound(r"E:\all_proj\HTML Programming\YOGI\TPose.mp3")#directory ka naam daalna and save the audio files in the same folder as your
                            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                            audio = recognizer.listen(mic)
                            message = recognizer.recognize_google(audio)
                            if (message == "yes" or message == "sure"):
                                playsound(r"E:\all_proj\HTML Programming\YOGI\TPYes.mp3")
                            else:
                                playsound(r"E:\all_proj\HTML Programming\YOGI\No.mp3")
                
 
    # ----------------------------------------------------------------------------------------------------------------
    
    # Check if it is the tree pose.
    # ----------------------------------------------------------------------------------------------------------------
    
    # Check if one leg is straight
    if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
 
        # Check if the other leg is bended at the required angle.
        if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:
 
            # Specify the label of the pose that is tree pose.
            label = 'Tree Pose'
            with speech_recognition.Microphone() as mic:
                            playsound(r"E:\all_proj\HTML Programming\YOGI\Tree.mp3")#directory ka naam daalna and save the audio files in the same folder as your
                            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                            audio = recognizer.listen(mic)
                            message = recognizer.recognize_google(audio)
                            if (message == "yes" or message == "sure"):
                                playsound(r"E:\all_proj\HTML Programming\YOGI\TYes.mp3")
                            else:
                                playsound(r"E:\all_proj\HTML Programming\YOGI\No.mp3")
                
                
    # ----------------------------------------------------------------------------------------------------------------
    
    # Check if the pose is classified successfully
    if label != 'Unknown Pose':
        
        # Update the color (to green) with which the label will be written on the image.
        color = (0, 255, 0)  
    
    # Write the label on the output image. 
    cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    
    # Check if the resultant image is specified to be displayed.
    if display:
    
        # Display the resultant image.
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
    else:
        # Return the output image and the classified label.
        return output_image, label

app = Flask(__name__)
camera_video = cv2.VideoCapture(0)
cv2.namedWindow('Pose Classification', cv2.WINDOW_NORMAL)
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5,model_complexity=1)

def generate_frames():
    while True:
            
        # read the camera frame
        ok, frame = camera_video.read()
        if not ok:
            
            # Continue to the next iteration to read the next frame and ignore the empty camera frame.
            continue
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ =  frame.shape
        frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
        
        frame, landmarks = detectPose(frame, pose_video, display=False)

        if landmarks:
        
        # Perform the Pose Classification.
            frame, _ = classifyPose(landmarks, frame, display=False)
        # cv2.imshow('Pose Classification', frame)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()

        



        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# ----------------- Authentication code begins------------#
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'yogi'
  
mysql = MySQL(app) #connect flask to mysql

# Login page
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'name' in request.form:
        name=request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE name = %s AND email = % s AND password = % s', (name,email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
# Logout page  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('name',None)
    session.pop('email', None)
    return redirect(url_for('login'))

# Register page
#flash for pop up
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'age' in request.form  and 'gender' in request.form  :
        userName = request.form['name']
        email = request.form['email']
        age=request.form['age']
        gender=request.form['gender']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s,%s,%s,%s)', (userName, email,age,gender, password,))
            mysql.connection.commit()
            flash('You have successfully registered!', 'success')
            return redirect('login')
    elif request.method == 'POST':
        message = 'You are not registered.Please fill out the form!'
    return render_template('register.html', message=message)
# End of Authentication 




@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/SignUp')
def SignUp():
      return render_template('register.html')  
        
@app.route('/model')
def model():
    return render_template('app.html')
    
@app.route('/body')
def body():
    return render_template('bodymap.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shoulder/<name>')
def shoulders(name):
    return render_template('shoulders.html',name=name)
    

# @app.route('/shoulder/<name>')
# def temp(name):
#     print("name is", name)
#     # return render_template('shoulders.html')
#     # return {{'url_for('shoulders')'}} 
#     return {{ url_for('shoulders') }}

if __name__=="__main__":
    app.run(debug=True)
