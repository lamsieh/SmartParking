import cv2
from easyocr import Reader

# Initialize EasyOCR reader
reader = Reader(['en'], gpu=False, verbose=False)

def detect_and_read_license_plate(frame):
    # Convert the input frame to grayscale if it's not already in grayscale
    if len(frame.shape) == 3:  # If the image has three channels (color image)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:  # If the image is already in grayscale
        gray = frame

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 10, 200)
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    license_plate_text = None  # Initialize license_plate_text

    for contour in contours:
        arc = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * arc, True)
        if len(approx) == 4:
            plate_cnt = approx
            break
    else:
        plate_cnt = None

    # Draw contours on the original frame
    if plate_cnt is not None:
        x, y, w, h = cv2.boundingRect(plate_cnt)
        plate = gray[y:y + h, x:x + w]

        # Reading text on the license plate
        detection = reader.readtext(plate)
        if len(detection) > 0:
            license_plate_text = detection[0][1]  # Storing the extracted text from the plate
            # Check if the detected text contains only numbers
            print("License plate detected:", license_plate_text)
            text = f"{license_plate_text} {detection[0][2] * 100:.2f}%"
            cv2.drawContours(frame, [plate_cnt], -1, (0, 255, 0), 3)
            cv2.putText(frame, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    return frame, license_plate_text
