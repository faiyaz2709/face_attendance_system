import subprocess

print("Step 1: Capturing photos...")
subprocess.run(["python", "capture_photos.py"])

print("Step 2: Training model...")
subprocess.run(["python", "train_encoding.py"])

print("step 3: excel attendance..:")
subprocess.run(["python","excel_attendance.py"])

print("Step 4: Starting face recognition attendance...")
subprocess.run(["python", "real_time_attendance.py"])
