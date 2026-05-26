import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

students_folder = "students"

label_id = 0
name_map = {}

for filename in os.listdir(students_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        path = os.path.join(students_folder, filename)

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (200, 200))

        faces.append(img)
        labels.append(label_id)

        name = os.path.splitext(filename)[0]
        name_map[label_id] = name

        label_id += 1

recognizer.train(faces, np.array(labels))
recognizer.save("face_model.yml")

with open("names.txt", "w") as f:
    for label, name in name_map.items():
        f.write(f"{label},{name}\n")

print("Model trained successfully!")