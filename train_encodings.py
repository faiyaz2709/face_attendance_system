# train_encodings.py
import face_recognition
import os
import pickle

DATASET_DIR = "dataset"
ENCODINGS_DIR = "encodings"
ENCODINGS_PATH = os.path.join(ENCODINGS_DIR, "encodings.pkl")

os.makedirs(ENCODINGS_DIR, exist_ok=True)

known_encodings = []
known_names = []

print("Processing dataset and generating encodings...")

for person in os.listdir(DATASET_DIR):
    person_folder = os.path.join(DATASET_DIR, person)
    if not os.path.isdir(person_folder):
        continue

    print(f"Processing: {person}")
    for img_name in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_name)
        try:
            image = face_recognition.load_image_file(img_path)
            boxes = face_recognition.face_locations(image, model="hog")  # "cnn" if GPU and dlib-cnn installed
            if not boxes:
                # no face found in this image
                continue
            encoding = face_recognition.face_encodings(image, boxes)[0]
            known_encodings.append(encoding)
            known_names.append(person)
        except Exception as e:
            print(f"Skipped {img_path}: {e}")

# Save to disk
data = {"encodings": known_encodings, "names": known_names}
with open(ENCODINGS_PATH, "wb") as f:
    pickle.dump(data, f)

print(f"Saved encodings to {ENCODINGS_PATH}")
print(f"Total encodings: {len(known_encodings)}")
