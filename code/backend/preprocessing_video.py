import numpy as np
import cv2
import face_recognition
from deepfake_detector import DeepfakeDetector
import math

MAX_NUM_FRAME = 1

def prediction_videoclass(videoPath):
    video_fd = cv2.VideoCapture(videoPath)
    if not video_fd.isOpened():
        print('Skpped: {}'.format(videoPath))
        return 'Error video open'

    frame_width = int(video_fd.get(3))
    frame_height = int(video_fd.get(4))
    frame_size = (frame_width,frame_height)
    video_fps = int(video_fd.get(5))

    frame_index = 0
    success, frame = video_fd.read()
    total_prob = []

    df_detector = DeepfakeDetector()

    while success:
        vframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(vframe) 
        face_probs = []

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = vframe[top:bottom, left:right]
            prob = df_detector.predict(face_image)
            face_probs.append(prob)

        if len(face_probs) > 0:
            total_prob.append(face_probs)

        frame_index += 1
        success, frame = video_fd.read()

        if frame_index == MAX_NUM_FRAME:
            break
    
    if len(total_prob) == 0:
        return 'no_face'

    predictions = []
    for prediction in total_prob:
        prediction_ = np.array(prediction).tolist()
        for p_index in range(len(prediction_)):
            if p_index >= len(predictions):
                predictions.append([]);
            predictions[p_index].extend([prediction_[p_index]])

    flagFake = False
    flagMediumFake = False
    for prediction in predictions:
        p = np.mean(prediction)
        if p < 0.5:
            flagFake = True
            break
        if math.isclose(0.5, p, rel_tol=1e-8):
            flagMediumFake = True

    if flagFake:
        return 'fake'
    
    if flagMediumFake:
        return 'medium-fake'
    
    return 'real'

#print(prediction_videoclass('./static/s.mp4'))