
from itertools import tee
from flask import Flask, render_template, Response

import cv2
import math
import cv2
import numpy as np
from time import time
import speech_recognition
import mediapipe as mp
import matplotlib.pyplot as plt
import nltk
#pip install playsound
from playsound import playsound
import speech_recognition

nltk.download('omw-1.4')
recognizer = speech_recognition.Recognizer()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True,
                    min_detection_confidence=0.3, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils

def AI_speak(com):
    speaker.say(com)
    speaker.runAndWait()
    speaker.stop()


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
<<<<<<< HEAD
                            speaker.say(
                                "You are doing Warrior Pose. Do you want to learn more about this pose?")
                            # speaker.runAndWait()
                            recognizer.adjust_for_ambient_noise(
                                mic, duration=0.2)
=======
                            playsound('C:\\Users\\siddh\\Desktop\\YOGI\\wp.mp3')#directory ka naam daalna and save the audio files in the same folder as your
                            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
>>>>>>> ecccb028d99a26f9be8e2093c5716596ee39ff80
                            audio = recognizer.listen(mic)
                            message = recognizer.recognize_google(audio)
                            if (message == "yes" or message == "sure"):
                                playsound('C:\\Users\\siddh\\Desktop\\YOGI\\wpYes.mp3')
                            else:
                                playsound('C:\\Users\\siddh\\Desktop\\YOGI\\No.mp3')
                

    # ----------------------------------------------------------------------------------------------------------------

    # Check if it is the T pose.
    # ----------------------------------------------------------------------------------------------------------------

            # Check if both legs are straight
            if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:

                # Specify the label of the pose that is tree pose.
                label = 'T Pose'
<<<<<<< HEAD
                AI_speak("T pose")
                
                # speaker.say(
                #                 "You are doing T Pose. Do you want to learn more about this pose?")
                # speaker.runAndWait()
                # with speech_recognition.Microphone() as mic:
                #             speaker.say(
                #                 "You are doing T Pose. Do you want to learn more about this pose?")
                #             speaker.runAndWait()
                #             speaker.stop()
                #             recognizer.adjust_for_ambient_noise(
                #                 mic, duration=0.1)
                #             audio = recognizer.listen(mic)
                #             message = recognizer.recognize_google(audio)
                # if (message == "yes" or message == "sure"):
                #     speaker.say("T pose is a beginner-friendly yoga pose which promotes good posture, improves flexibility and develops good balance. It strengthens your legs and core and also helps to maintain good gut health.")
                #     speaker.runAndWait()
                # else:
                #     speaker.say("Okay, carry on with your pose")
=======
                with speech_recognition.Microphone() as mic:
                            playsound('C:\\Users\\siddh\\Desktop\\YOGI\\TPose.mp3')#directory ka naam daalna and save the audio files in the same folder as your
                            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                            audio = recognizer.listen(mic)
                            message = recognizer.recognize_google(audio)
                            if (message == "yes" or message == "sure"):
                                playsound('C:\\Users\\siddh\\Desktop\\YOGI\\TPYes.mp3')
                            else:
                                playsound('C:\\Users\\siddh\\Desktop\\YOGI\\No.mp3')
                
>>>>>>> ecccb028d99a26f9be8e2093c5716596ee39ff80
 
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
                            playsound('C:\\Users\\siddh\\Desktop\\YOGI\\Tree.mp3')#directory ka naam daalna and save the audio files in the same folder as your
                            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                            audio = recognizer.listen(mic)
                            message = recognizer.recognize_google(audio)
                            if (message == "yes" or message == "sure"):
                                playsound('C:\\Users\\siddh\\Desktop\\YOGI\\TYes.mp3')
                            else:
                                playsound('C:\\Users\\siddh\\Desktop\\YOGI\\No.mp3')
                
                
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

app=Flask(__name__)
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


@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/model')
def model():
    return render_template('app.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
