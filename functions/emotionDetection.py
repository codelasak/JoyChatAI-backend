import mediapipe as mp
import cv2
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

def detect_emotion(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        
        # Extract relevant facial features
        left_eye = np.mean([landmark.y for landmark in face_landmarks.landmark[33:46]])
        right_eye = np.mean([landmark.y for landmark in face_landmarks.landmark[263:276]])
        mouth_open = face_landmarks.landmark[13].y - face_landmarks.landmark[14].y
        
        # Simple emotion classification based on facial features
        if mouth_open > 0.1:
            return "Happy"
        elif left_eye < 0.45 and right_eye < 0.45:
            return "Surprised"
        elif left_eye > 0.55 and right_eye > 0.55:
            return "Sad"
        else:
            return "Neutral"
    
    return "No face detected"

def process_video_emotion(video_path):
    cap = cv2.VideoCapture(video_path)
    emotions = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        emotion = detect_emotion(frame)
        emotions.append(emotion)
    
    cap.release()
    return emotions