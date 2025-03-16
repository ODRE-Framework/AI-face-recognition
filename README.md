
# Face Recognition API

This project is a real-time face recognition system built using FastAPI, OpenCV, and FaceNet. It provides a **WebSocket**-based service to detect and recognize faces from a video stream and evaluates access policies based on recognized users.

## Features
- **Face Registration**: Users can register their face, and the system generates an embedding for future recognition.
- **Real-Time Recognition**: Captures frames from a video stream, processes them, and matches against stored embeddings.
- **Access Policy Enforcement**: Evaluates if a recognized face has permission to access a document.

## Technologies Used
- **FastAPI** for API development
- **Uvicorn** as ASGI server
- **OpenCV** for image processing
- **FaceNet** for face embedding generation
- **MTCNN** for face detection
- **WebSockets** for real-time communication
- **HTTPX** for making asynchronous API requests
- **JSON storage** for embedding persistence

---

## **Running with Docker**

### **1️⃣ Docker Compose Deployment**

Copy the following **`docker-compose.yml`** file and run:

```bash
docker-compose up

```

```yaml
version: '3.0'
services:
  directory:
    container_name: ia-recognition
    image: acimmino/ia-recognition:latest
    restart: unless-stopped
    ports:
      - "8000:9100"

```

### **2️⃣ Manual Docker Deployment**

1. **Build the Docker Image**:
    
    ```bash
    docker build -t ia-recognition-api .
    
    ```
    
2. **Run the Container**:
    
    ```bash
    docker run -p 8000:9100 ia-recognition-api
    
    ```
    

## Installation & Usage

### 1. Clone the repository
```sh
git clone https://github.com/ODRE-Framework/AI-face-recognition.git
cd AI-face-recognition

```

### 2. Create a virtual environment and install dependencies

```
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

```

### 3. Run the FastAPI server

```
uvicorn app:app --reload --port=8001

```

By default, the API will be available at [**http://127.0.0.1:8001/**](http://127.0.0.1:8001/).

### 4. Open the Web Client

- Open `client.html` or [**http://127.0.0.1:8001/**](http://127.0.0.1:8001/) in a browser to test real-time face recognition.
- Open `register_face.html` or [**http://127.0.0.1:8001/register**](http://127.0.0.1:8001/register) to register new faces.

## API Endpoints

### **1. Register Face**

- **URL**: `POST /register-face/`
- **Request**: Image blob (form-data)
- **Response**: Face ID (UUID) if registration is successful.

