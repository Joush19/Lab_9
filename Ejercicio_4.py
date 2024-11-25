import numpy as np
import cv2

# Cargamos la imagen
original = cv2.imread("monedas_2.jpg")
org = cv2.resize(original, (500,400))
cv2.imshow("original", org)

# Convertimos a escala de grises
gris = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)

# Aplicar suavizado Gaussiano
gauss = cv2.GaussianBlur(gris, (15, 15), 0)
gauss1 = cv2.resize(gauss,(500,400))

cv2.imshow("suavizado", gauss1)

# Detectamos los bordes con Canny
canny = cv2.Canny(gauss, 50, 150)  # Ajusta los umbrales aquí
canny1 = cv2.resize(canny,(500,400))

cv2.imshow("canny", canny1)

# Buscamos los contornos
(contornos, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtramos los contornos por área para ignorar objetos pequeños
contornos_filtrados = [c for c in contornos if cv2.contourArea(c) > 120]  # Ajusta el área mínima

# Mostramos el número de monedas por consola
print("He encontrado {} objetos".format(len(contornos_filtrados)))

# Dibujar los contornos filtrados
cv2.drawContours(original, contornos_filtrados, -1, (0, 0, 255), 2)

original1 = cv2.resize(original,(500,400))
cv2.imshow("contornos", original1)

cv2.waitKey(0)
cv2.destroyAllWindows()