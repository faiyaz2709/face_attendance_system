# capture_photos.py
import cv2
import os

def main():
    name = input("Enter person name (no spaces): ").strip()
    if not name:
        print("Name required.")
        return

    folder = os.path.join("dataset", name)
    os.makedirs(folder, exist_ok=True)

    cap = cv2.VideoCapture(0)  # use 0 for laptop webcam or change to phone URL
    if not cap.isOpened():
        print("Cannot open camera")
        return

    print("Starting capture. Press 'q' to quit early.")
    count = 0
    target = 100

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("Capture - Press q to stop", frame)

        # Save frames (optionally you may crop and convert to RGB/gray)
        img_path = os.path.join(folder, f"{name}_{count}.jpg")
        cv2.imwrite(img_path, frame)
        count += 1

        if count >= target:
            print(f"Captured {count} images for {name}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Stopped by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
