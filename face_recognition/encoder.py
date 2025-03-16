import cv2
from facenet_pytorch import InceptionResnetV1
import torch

model = InceptionResnetV1(pretrained='vggface2').eval()


def generate_embedding(face_image):
    face_image = cv2.resize(face_image, (160, 160))
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    face_tensor = torch.from_numpy(face_image).permute(2, 0, 1).float().unsqueeze(0) / 255.0
    with torch.no_grad():
        embedding = model(face_tensor)
    return embedding
