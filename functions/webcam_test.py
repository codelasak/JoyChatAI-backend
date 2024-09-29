import cv2
from deepface import DeepFace
import mediapipe as mp
import time
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Start capturing video
cap = cv2.VideoCapture(0)

# Initialize variables for FPS calculation
prev_frame_time = 0
new_frame_time = 0

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

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and get facial landmarks
    results = face_mesh.process(rgb_frame)

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
                
                # Draw rectangle around face and label with predicted emotion and confidence
                cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 2)
                cv2.putText(frame, f"{emotion} ({confidence:.2f}%)", (int(x), int(y-10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            except Exception as e:
                print(f"Error in emotion detection: {str(e)}")
                cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 0, 255), 2)
                cv2.putText(frame, "Error", (int(x), int(y-10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Get gaze direction
            gaze_direction = get_gaze_direction(face_landmarks, frame.shape)

            # Update gaze times
            update_gaze_times(gaze_direction)

            # Display gaze direction and times
            cv2.putText(frame, f"Gaze: {gaze_direction}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f"Left: {gaze_times['left']:.2f}s", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, f"Center: {gaze_times['center']:.2f}s", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, f"Right: {gaze_times['right']:.2f}s", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Calculate and display FPS
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Real-time Emotion and Gaze Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()