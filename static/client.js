const video = document.getElementById("video");

const socket = new WebSocket('ws://127.0.0.1:8001/video-stream');

socket.onerror = (error) => {
    console.error("Error en la conexión WebSocket:", error);
};

socket.onopen = () => {
    console.log("WebSocket conectado correctamente.");

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;

            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");

            video.addEventListener("loadedmetadata", () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
            });

            setInterval(() => {
                if (socket.readyState === WebSocket.OPEN) {
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    canvas.toBlob(blob => {
                        if (blob) {
                            socket.send(blob);
                            console.log("Imagen capturada y enviada al servidor");
                        }
                    }, "image/png");
                } else {
                    console.warn("WebSocket no está listo para enviar datos.");
                }
            }, 30000); // 30 segundos
        })
        .catch(err => console.error("Error accediendo a la cámara", err));
};


socket.onmessage = (event) => {
    const pdfViewer = document.getElementById("pdfViewer");

    if (event.data instanceof Blob) {
        const pdfBlob = new Blob([event.data], { type: "application/pdf" });
        const pdfUrl = URL.createObjectURL(pdfBlob);
        console.log("hola")
        document.getElementById("pdfViewer").src = pdfUrl;

    } else {
        console.log("Mensaje recibido:", event.data);
        pdfViewer.src = "";
    }
};



