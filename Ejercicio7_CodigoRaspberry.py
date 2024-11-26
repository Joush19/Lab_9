import cv2
import numpy as np
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def send_command(command):
    ser.write(command.encode())

cap = cv2.VideoCapture(0)
cv2.waitKey(1000)

_, background = cap.read()
background = cv2.GaussianBlur(cv2.cvtColor(background, cv2.COLOR_BGR2GRAY), (21, 21), 0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: 
        break

    gray_frame = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    diff = cv2.absdiff(background, gray_frame)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_height, frame_width = frame.shape[:2]
    detected_objects = 0
    detected = False

    # Initialize the positions of the objects
    object_positions = []

    for c in contours:
        area = cv2.contourArea(c)
        if 500 < area < 5000:
            x, y, w, h = cv2.boundingRect(c)
            object_positions.append((x, y, w, h))

            # If one object is in the middle, follow it
            if frame_width // 3 < x + w // 2 < 2 * frame_width // 3:
                detected = True
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                send_command('CENTER')  

            elif x + w // 2 < frame_width // 3:  
                detected = True
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                send_command('LEFT') 

            elif x + w // 2 > 2 * frame_width // 3:  
                detected = True
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                send_command('RIGHT') 

            detected_objects += 1  

    if detected_objects >= 2:
        send_command('TOGGLE_LEDS')  
    elif detected_objects == 0:
        send_command('TURN_SLOWLY')  

    if detected:
        cv2.putText(frame, "Object Detected", (frame_width - 200, frame_height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


    mask = cv2.bitwise_not(thresh)

    background_removed = cv2.bitwise_and(frame, frame, mask=mask)


    cv2.imshow("Object Detection", background_removed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
