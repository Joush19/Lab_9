import cv2
import numpy as np

imagen = cv2.imread("figuras.png")
output_image = imagen.copy()

gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def detect_shape(contour):
    shape = "unknown"
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    sides = len(approx)
    if sides == 3:
        shape = "Triangle"
    elif sides == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
    elif sides == 5:
        shape = "Pentagon"
    elif sides == 6:
        shape = "Hexagon"
    elif sides > 6:
        shape = "Circle"
    return shape

def detect_color(contour):
    mask = np.zeros(imagen.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [contour], -1, 255, -1)
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    mean_val = cv2.mean(hsv, mask=mask)[:3]
    color = "unknown"
    if 0 <= mean_val[0] <= 10 or 160 <= mean_val[0] <= 180:
        color = "Red"
    elif 10 <= mean_val[0] <= 35:
        color = "Yellow"
    elif 35 <= mean_val[0] <= 85:
        color = "Green"
    elif 100 <= mean_val[0] <= 130:
        color = "Blue"
    elif 130 <= mean_val[0] <= 170:
        color = "Purple"
    elif 80 <= mean_val[0] <= 100:
        color = "Cyan"
    else:
        print(f"Unknown color with HSV values: {mean_val}")
    return color

for contour in contours:
    shape = detect_shape(contour)
    color = detect_color(contour)
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.drawContours(output_image, [contour], -1, (0, 0, 0), 2)
        cv2.putText(output_image, f"{shape}, {color}", (cX - 50, cY),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

cv2.imshow("Detected Shapes and Colors", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()