import cv2
import numpy as np

# Cargar el video
cap = cv2.VideoCapture('bouncing.mp4')

# Crear un objeto para la sustracciÃ³n de fondo
backSub = cv2.createBackgroundSubtractorMOG2()

# NÃºmero de cuadros a ignorar al principio
num_initial_frames = 30

for _ in range(num_initial_frames):
    ret, frame = cap.read()
    if not ret:
        break

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar la sustracciÃ³n de fondo
    fgMask = backSub.apply(frame)

    # Aplicar un umbral para reducir el ruido
    _, thresh = cv2.threshold(fgMask, 200, 255, cv2.THRESH_BINARY)

    # Aplicar un filtro de desenfoque
    blurred = cv2.GaussianBlur(thresh, (5, 5), 0)

    # Detectar bordes
    edges = cv2.Canny(blurred, 50, 150)

    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos segÃºn el Ã¡rea
    filtered_contours = [c for c in contours if cv2.contourArea(c) > 500]  # Ajusta el Ã¡rea mÃ­nima

    # Dibujar los contornos filtrados en el cuadro original
    cv2.drawContours(frame, filtered_contours, -1, (0, 255, 0), 2)

    # Mostrar el cuadro con contornos
    cv2.imshow("contornos", frame)

    # Esperar un breve periodo para permitir la visualizaciÃ³n
    if cv2.waitKey(30) & 0xFF == 27:  # Salir si se presiona 'Esc'
        break

# Liberar la captura
cap.release()
cv2.destroyAllWindows()