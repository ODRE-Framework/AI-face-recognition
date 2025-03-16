import numpy as np
import cv2


def process_image(image_blob, min_width=160, min_height=160):
    if not image_blob or len(image_blob) == 0:
        print("Error: No se recibió una imagen válida o está vacía.")
        return None

    try:
        nparr = np.frombuffer(image_blob, np.uint8)

        image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        if image is None:
            print("OpenCV no pudo decodificar la imagen en modo UNCHANGED. Intentando modo COLOR.")
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            print("OpenCV aún no puede decodificar la imagen.")
            return None

        if len(image.shape) == 3 and image.shape[-1] == 4:
            print("La imagen tiene canal alfa. Convirtiendo de RGBA a BGR.")
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

        height, width = image.shape[:2]
        if width < min_width or height < min_height:
            print(
                f"Error: La imagen es demasiado pequeña (dimensiones: {width}x{height}). Se requiere al menos {min_width}x{min_height}.")
            return None

        return image

    except Exception as e:
        print(f"Error procesando la imagen con OpenCV: {e}")
        return None
