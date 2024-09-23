# import recognition
import face_recognition  # This is the external library
import numpy as np
import os
import cv2

# Function to load known faces from specific class folders
def load_known_faces(class_type=None):
    known_faces = []
    known_names = []

    # Set folder path based on class type
    folder_path = 'known_faces'
    if class_type == "Cyber Security":
        folder_path = 'known_faces/cyber_security'
    elif class_type == "Data Analytics":
        folder_path = 'known_faces/data_analytics'
    elif class_type == "Instructor":
        folder_path = 'known_faces/instructors'

    # Load images from the respective folder
    for filename in os.listdir(folder_path):
        image = face_recognition.load_image_file(f'{folder_path}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(filename.split('.')[0])  # Use filename as the name

    return known_faces, known_names

# Function to recognize faces from a camera feed
def recognize_faces(known_faces, known_names):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    name = "Unknown"  # Initialize name to "Unknown"

    if ret:
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

        # You may not need to show the video window if integrating into Tkinter
        # cv2.imshow('Face Recognition', frame)

    cam.release()
    cv2.destroyAllWindows()

    return name  # Return the recognized name
