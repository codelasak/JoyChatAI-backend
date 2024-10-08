import cv2
from deepface import DeepFace
import mediapipe as mp
import time
import numpy as np
import base64
from io import BytesIO
from PIL import Image

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize variables for gaze tracking
gaze_times = {'left': 0, 'center': 0, 'right': 0}
last_gaze = None
last_gaze_time = time.time()

def calculate_ear(eye_landmarks):
    # Calculate the Eye Aspect Ratio (EAR)
    A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
    B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
    C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
    ear = (A + B) / (2.0 * C)
    return ear

def get_gaze_direction(face_landmarks, image_shape):
    # Get relevant landmarks
    left_eye = np.array([(face_landmarks.landmark[p].x * image_shape[1], face_landmarks.landmark[p].y * image_shape[0]) 
                         for p in [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]])
    right_eye = np.array([(face_landmarks.landmark[p].x * image_shape[1], face_landmarks.landmark[p].y * image_shape[0]) 
                          for p in [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]])
    nose_tip = np.array([face_landmarks.landmark[1].x * image_shape[1], face_landmarks.landmark[1].y * image_shape[0]])

    # Calculate eye centers
    left_eye_center = np.mean(left_eye, axis=0)
    right_eye_center = np.mean(right_eye, axis=0)
    eye_center = (left_eye_center + right_eye_center) / 2

    # Calculate EAR for both eyes
    left_ear = calculate_ear(left_eye)
    right_ear = calculate_ear(right_eye)

    # Calculate the direction vector from eye center to nose tip
    gaze_vector = nose_tip - eye_center

    # Normalize the gaze vector
    gaze_vector = gaze_vector / np.linalg.norm(gaze_vector)

    # Calculate the horizontal distance between eye centers
    eye_distance = np.linalg.norm(right_eye_center - left_eye_center)

    # Adjust thresholds based on eye distance to account for different face sizes
    left_threshold = -0.2 * (eye_distance / 100)
    right_threshold = 0.15 * (eye_distance / 100)  # Slightly lower threshold for right gaze

    # Determine gaze direction based on the x-component of the gaze vector and EAR
    if gaze_vector[0] < left_threshold and left_ear > right_ear:
        return "left"
    elif gaze_vector[0] > right_threshold or (gaze_vector[0] > 0 and right_ear > left_ear * 1.1):  # Adjusted condition for right gaze
        return "right"
    else:
        return "center"

def update_gaze_times(gaze):
    global last_gaze, last_gaze_time
    current_time = time.time()
    if last_gaze:
        gaze_times[last_gaze] += current_time - last_gaze_time
    last_gaze = gaze
    last_gaze_time = current_time

def detect_emotion_and_gaze(base64_image):
    # Decode the base64 image
    image_data = base64.b64decode(base64_image.split(',')[1])
    image = Image.open(BytesIO(image_data))
    
    # Convert PIL Image to numpy array
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert the BGR image to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and get facial landmarks
    results = face_mesh.process(rgb_frame)

    emotion = None
    confidence = None
    gaze_direction = None

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get face bounding box
            face_points = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) for lm in face_landmarks.landmark])
            x, y = np.min(face_points, axis=0)
            w, h = np.ptp(face_points, axis=0)
            
            # Extract the face ROI (Region of Interest)
            face_roi = frame[int(y):int(y+h), int(x):int(x+w)]
            
            try:
                # Perform emotion analysis on the face ROI
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                
                # Determine the dominant emotion
                emotion = result[0]['dominant_emotion']
                
                # Get the confidence score
                confidence = result[0]['emotion'][emotion]
            
            except Exception as e:
                print(f"Error in emotion detection: {str(e)}")

            # Get gaze direction
            gaze_direction = get_gaze_direction(face_landmarks, frame.shape)

            # Update gaze times
            update_gaze_times(gaze_direction)

    return {
        "emotion": emotion,
        "confidence": confidence,
        "gaze_direction": gaze_direction,
        "gaze_times": gaze_times
    }

def reset_gaze_times():
    global gaze_times, last_gaze, last_gaze_time
    gaze_times = {'left': 0, 'center': 0, 'right': 0}
    last_gaze = None
    last_gaze_time = time.time()