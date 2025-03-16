import json
import uuid

import numpy as np

EMBEDDINGS_FILE = "face_embeddings.json"

try:
    with open(EMBEDDINGS_FILE, "r") as f:
        face_database = json.load(f)
        face_database = {tuple(map(float, k.split(","))): v for k, v in face_database.items()}
except (FileNotFoundError, json.JSONDecodeError):
    face_database = {}


def save_embeddings():
    with open(EMBEDDINGS_FILE, "w") as f:
        json.dump({",".join(map(str, k)): v for k, v in face_database.items()}, f, indent=4)


def register_face(embedding):
    key = tuple(embedding.cpu().detach().numpy().flatten())
    face_id = str(uuid.uuid4())
    face_database[key] = face_id
    save_embeddings()
    return face_id


def find_matching_face(embedding):
    embedding_np = embedding.cpu().detach().numpy().flatten()
    for stored_embedding, face_id in face_database.items():
        similarity = np.linalg.norm(embedding_np - np.array(stored_embedding))
        if similarity < 0.6:
            return face_id
    return None
