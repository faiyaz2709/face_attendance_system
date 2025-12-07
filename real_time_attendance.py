# real_time_attendance.py
import cv2
import face_recognition
import pickle
from excel_attendance import mark_attendance, create_file_if_missing
import os
import numpy as np

# Load known encodings
ENCODINGS_PATH = os.path.join("encodings", "encodings.pkl")
if not os.path.exists(ENCODINGS_PATH):
    raise FileNotFoundError(f"Encodings file not found: {ENCODINGS_PATH}. Run train_encodings.py")

with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)
known_encodings = data["encodings"]
known_names = data["names"]

# Ensure excel exists
create_file_if_missing()

# Choose webcam:
# For laptop webcam use 0:
cap = cv2.VideoCapture("http://192.168.0.100:4747/video")


# If you want to use phone camera via DroidCam, replace above with:
# cap = cv2.VideoCapture("http://<phone-ip>:4747/video")

print("Starting real-time face recognition. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera")
        break

    # Resize frame for speed (optional)
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Locate faces and compute encodings
    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Scale back up face locations because we used small_frame
        top *= 2; right *= 2; bottom *= 2; left *= 2

        # Compare against known encodings
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
        distances = face_recognition.face_distance(known_encodings, face_encoding)
        name = "Unknown"

        if len(distances) > 0:
            best_idx = np.argmin(distances)
            if matches[best_idx]:
                name = known_names[best_idx]
                # mark attendance (excel module prevents duplicates)
                mark_attendance(name, status="Present")

        # Draw green box and put name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Recognition Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
