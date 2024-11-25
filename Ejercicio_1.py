import cv2

video_path = "/home/GL2/Documents/Lab9/bouncing.mp4"
mog2 = cv2.createBackgroundSubtractorMOG2()
knn = cv2.createBackgroundSubtractorKNN()
bgsegm = cv2.bgsegm.createBackgroundSubtractorMOG()
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: No se pudo abrir el video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar los sustractores
    mog2_mask = mog2.apply(frame)
    knn_mask = knn.apply(frame)
    bgsegm_mask = bgsegm.apply(frame)


    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Original', 320, 240)

    cv2.namedWindow('MOG2', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('MOG2', 320, 240)

    cv2.namedWindow('KNN', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('KNN', 320, 240)  

    cv2.namedWindow('Background Subtractor MOG', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Background Subtractor MOG', 320, 240)  

    cv2.imshow('Original', frame)
    cv2.imshow('MOG2', mog2_mask)
    cv2.imshow('KNN', knn_mask)
    cv2.imshow('Background Subtractor MOG', bgsegm_mask)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()