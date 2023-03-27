
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
import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
import csv
import os
import sys
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import pandas as pd

  
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

array = [0,0,0,0,0]
dataset = pd.read_csv('C:/Nidhi/vscode/yoga/nidhi/yoga.csv')
dataset1=dataset.fillna(0)

print(dataset1)

X = dataset1.drop(columns= 'Label', axis=1)
Y = dataset1['Label']

classifier = svm.SVC(kernel='linear',probability=True)

classifier.fit(X,Y)

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
            landmarks.append((landmark.x))
            landmarks.append((landmark.y))
            landmarks.append((landmark.z))
        
        return output_image, landmarks



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
        # print(landmarks)
        # print(len(landmarks))
        
        input = landmarks
        input_as_np = np.asarray(input)
        input_reshaped = input_as_np.reshape(1,-1)
        a = classifier.predict_proba(input_reshaped)
        print(a)
        avg_percent = sum(array) / len(array)
        color = (0, 255, 0)
        
        cv2.putText(frame, str(classifier.predict(input_reshaped)), (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
        cv2.putText(frame, "Accuracy", (10, 100),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
        
        # Warrior
        # cv2.putText(frame, str(int(a[0][2]*100)), (200, 100),cv2.FONT_HERSHEY_PLAIN, 2, color, 2) 
        
        # Tree
        # cv2.putText(frame, str(int(a[0][1]*100)), (200, 100),cv2.FONT_HERSHEY_PLAIN, 2, color, 2) 
        
        # Goddess
        cv2.putText(frame, str(int(a[0][0]*100)), (200, 100),cv2.FONT_HERSHEY_PLAIN, 2, color, 2) 
        
        
        
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
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
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
    session.pop('email', None)
    return redirect(url_for('login'))

# Register page
#flash for pop up
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
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
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (userName, email, password,))
            mysql.connection.commit()
            flash('You have successfully registered!', 'success')
            return redirect('login')
    elif request.method == 'POST':
        message = 'Please fill out the form!'
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

@app.route('/shoulder')
def shoulders():
     return render_template('shoulders.html')
     
@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
