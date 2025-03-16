import uuid

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form, UploadFile
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from face_recognition.detector import detect_faces
from face_recognition.encoder import generate_embedding
from face_recognition.database import find_matching_face, register_face
from utils.image_utils import process_image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

EMBEDDINGS_FILE = "face_embeddings.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get():
    return HTMLResponse(content=open("client.html").read(), status_code=200)


import httpx


@app.websocket("/video-stream")
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            video_blob = await websocket.receive_bytes()
            print("Imagen recibida")

            nparr = process_image(video_blob)
            faces = detect_faces(nparr)

            if faces is not None:
                for face in faces:
                    embedding = generate_embedding(face)
                    match_uuid = find_matching_face(embedding)

                    if match_uuid:
                        print(f"Acceso concedido a: {match_uuid}")

                        policy_url = "http://127.0.0.1:8000/api/policy/evaluate/3331"
                        params = {"face_uuid": match_uuid, "key": "face_recognition"}

                        async with httpx.AsyncClient() as client:
                            response = await client.get(policy_url, params=params)

                            if response.status_code == 200:
                                pdf_bytes = response.content
                                await websocket.send_bytes(pdf_bytes)
                                print("PDF enviado al cliente")
                            else:
                                await websocket.send_text("Acceso denegado según la política")

                    else:
                        await websocket.send_text("Cara no reconocida")
            else:
                await websocket.send_text("No se detectó cara")

    except WebSocketDisconnect:
        print("Cliente desconectado.")


@app.get("/register")
async def register():
    return HTMLResponse(content=open("register_face.html").read(), status_code=200)


@app.post("/register-face/")
async def register_face_endpoint(video_blob: UploadFile = Form(...)):
    try:
        image_bytes = await video_blob.read()

        if not image_bytes:
            return JSONResponse(status_code=400, content={"error": "No se recibió ningún archivo."})

        nparr = process_image(image_bytes)

        if nparr is None:
            return JSONResponse(status_code=400, content={"error": "No se pudo procesar la imagen correctamente."})

        faces = detect_faces(nparr)

        if not faces or len(faces) == 0:
            return JSONResponse(status_code=400, content={"error": "No se detectó una cara en la imagen."})

        embedding = generate_embedding(faces[0])
        face_id  = register_face(embedding)

        return {"message": "Cara registrada con éxito", "face_id": face_id }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
