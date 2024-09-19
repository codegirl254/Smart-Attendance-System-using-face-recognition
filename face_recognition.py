import face_recognition
import numpy as np
import os
import cv2


def load_known_faces():
    known_faces = []
    known_names = []
    
    for filename in os.listdir('known_faces'):
        image = face_recognition.load_image_file(f'known_faces/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(filename.split('.')[0])  # Use the filename as the name
    
    return known_faces, known_names

def recognize_faces(known_faces, known_names):
    cam = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cam.read()
        rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
        
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                
            # Draw a rectangle around the face and label it
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        
        cv2.imshow('Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.release()
    cv2.destroyAllWindows()go