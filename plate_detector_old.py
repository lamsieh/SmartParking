import cv2
from easyocr import Reader
import re
def detect_license_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 10, 200)
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    for contour in contours:
        arc = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * arc, True)
        if len(approx) == 4:
            plate_cnt = approx
            break
    else:
        plate_cnt = None

    return plate_cnt, gray

def detect_license_plate_from_ip(ip_address):
    reader = Reader(['en'], gpu=True, verbose=False)

    # Lecture de la vidéo en continu depuis la caméra
    cap = cv2.VideoCapture(f'http://{ip_address}:8080/video')

    # Définir la résolution et le nombre d'images par seconde
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 10)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Réduire la résolution de l'image
        #frame = cv2.resize(frame, (640, 480))

        # Détection de la plaque d'immatriculation
        plate_cnt, gray = detect_license_plate(frame)

        if plate_cnt is not None:
            # Extraction de la région de la plaque d'immatriculation
            x, y, w, h = cv2.boundingRect(plate_cnt)
            plate = gray[y:y + h, x:x + w]

            # Lecture du texte sur la plaque d'immatriculation
            detection = reader.readtext(plate)
            if len(detection) > 0:
                license_plate_text = detection[0][1]  # Stockage du texte extrait de la plaque

                if re.match(r'\b\d{4}\b', license_plate_text):
                    return license_plate_text

                
                # text = f"{license_plate_text} {detection[0][2] * 100:.2f}%"
                # cv2.drawContours(frame, [plate_cnt], -1, (0, 255, 0), 3)
                # cv2.putText(frame, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)


