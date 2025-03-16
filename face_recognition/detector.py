from facenet_pytorch import MTCNN
import numpy as np

mtcnn = MTCNN(keep_all=True)


def detect_faces(image):
    if image is None or not isinstance(image, np.ndarray):
        print("⚠ Error: La imagen recibida es inválida o None.")
        return None

    faces, _ = mtcnn.detect(image)
    if faces is None:
        print("⚠ No se detectaron rostros en la imagen.")
        return None

    detected_faces = []
    for face in faces:
        x1, y1, x2, y2 = map(int, face)
        detected_faces.append(image[y1:y2, x1:x2])

    return detected_faces
