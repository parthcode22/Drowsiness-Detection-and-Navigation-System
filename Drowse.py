from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
import cv2
import winsound
import os
import time
import sys
import subprocess
import threading

# Global variable to track rest stop availability
rest_stop_available = False

try:
    from Navigation import ReststopRecommender
    rest_stop_available = True
    print("Rest stop feature available")
except ImportError:
    print("Rest stop feature not available. Make sure Navigation.py is in same directory.")
    rest_stop_available = False

def eyeAspectRatio(eye):
    # Vertical distances
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # Horizontal distance
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def wait_for_start_signal():
    """
    Wait for the start detection signal file
    """
    while not os.path.exists('start_detection.flag'):
        time.sleep(0.5)
    os.remove('start_detection.flag')

def main():
    # Declare global to use the global variable
    global rest_stop_available
    
    # Launch Streamlit frontend
    frontend_process = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'Front.py'])

    # Wait for start signal
    wait_for_start_signal()

    frequency = 2500
    duration = 2000

    count = 0
    earThresh = 0.3
    earFrames = 48

    # Initialize the rest stop recommender if available
    rest_recommender = None
    if rest_stop_available:
        try:
            rest_recommender = ReststopRecommender()
            print("Rest stop recommender initialized")
        except Exception as e:
            print(f"Error initializing rest stop recommender: {e}")
            rest_stop_available = False

    # Track when the last alert was triggered
    last_alert_time = 0
    alert_cooldown = 60  # seconds between alerts

    # Load the sample dataset 
    shapePredictor = "shape_predictor_68_face_landmarks.dat"

    # Initialize the camera access
    cam = cv2.VideoCapture(0)  # Use 0 for default camera

    if not cam.isOpened():
        print("Error: Could not open camera.")
        return

    detector = dlib.get_frontal_face_detector()  # Capture the detected face
    predictor = dlib.shape_predictor(shapePredictor)  # Compare detected data with the dataset 

    # Get the coordinates of left & right eye
    (lstart, lend) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rstart, rend) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    while True:
        ret, frame = cam.read()  # Read frame from camera
        
        if not ret or frame is None:
            print("Error: Could not read frame from camera.")
            continue  # Skip to the next loop iteration

        frame = imutils.resize(frame, width=450)  # Resize frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        if gray.dtype != "uint8":  
            print("Error: Grayscale image not in uint8 format.")  
            continue  

        rects = detector(gray, 0)  # Detect faces

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lstart:lend]
            rightEye = shape[rstart:rend]

            leftEAR = eyeAspectRatio(leftEye)
            rightEAR = eyeAspectRatio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

            if ear < earThresh:
                count += 1
                if count >= earFrames:
                    cv2.putText(frame, "DROWSINESS DETECTED", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    current_time = time.time()
                    if current_time - last_alert_time > alert_cooldown:
                        
                        winsound.Beep(frequency, duration)
                        if rest_stop_available and rest_recommender:
                            try:
                                # Launch navigation script
                                subprocess.Popen([sys.executable, 'Navigation.py'])
                                print("Navigation launched")
                            except Exception as e:
                                print(f"Error launching navigation: {e}")

                        last_alert_time = current_time
            else:
                count = 0  

        cv2.imshow("Drowsiness Detection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break  

    cam.release()
    cv2.destroyAllWindows()
    frontend_process.terminate()

if __name__ == "__main__":
    main()
