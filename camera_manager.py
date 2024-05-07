import cv2
import numpy as np
import serial


ARDUINO = 'Arduino'
IP = 'IP'


class CameraManager:
    def __init__(self, camera_type, **kwargs):
        self.camera_type = camera_type

        if self.camera_type == ARDUINO:
            self.initialize_arduino_camera(**kwargs)
        elif self.camera_type == IP:
            self.initialize_ip_camera(**kwargs)
        else:
            raise ValueError("Invalid camera type. Please choose either 'Arduino' or 'IP'.")

    def initialize_arduino_camera(self, width=320, height=240, port='COM4', baud=1_000_000):
        self.width = width
        self.height = height
        self.ser = serial.Serial(
            port=port,
            baudrate=baud,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def initialize_ip_camera(self, ip_address):
        self.ip_address = ip_address
        self.cap = cv2.VideoCapture(self.ip_address)
        
        if not self.cap.isOpened():
            raise ValueError("Unable to connect to IP webcam at {}".format(ip_address))

    def capture_frame(self):
        if self.camera_type == ARDUINO:
            return self.capture_arduino_frame()
        elif self.camera_type == IP:
            return self.capture_ip_frame()
        else:
            raise ValueError("Invalid camera type. Please choose either 'Arduino' or 'IP'.")

    def capture_arduino_frame(self):
        # Wait for "rdy" signal from Arduino
        self.wait_for_ready_signal()

        # Read image data
        data = self.ser.read(self.width * self.height)

        # Ensure correct amount of data is received
        if len(data) != self.width * self.height:
            print("Error: Incomplete image data received")
            return None

        # Convert data to numpy array for OpenCV
        image_array = np.frombuffer(data, dtype=np.uint8)

        # Reshape to OpenCV image format
        image = image_array.reshape((self.height, self.width))

        return image 

    def wait_for_ready_signal(self):
        ready_signal = b"*RDY*"
        while True:
            # Read serial data until "*RDY*" signal is received
            data = self.ser.read(len(ready_signal))
            if data == ready_signal:
                print("Ready signal received. Proceeding to read image data.")
                break

    def capture_ip_frame(self):
        ret, frame = self.cap.read()
        return frame

if __name__ == "__main__":
    # Example usage:
    while True:
        camera_type_input = input("Enter camera type (1 for 'Arduino' or 2 for 'IP'): ").strip()

        if camera_type_input in ['1', '2']:
            camera_type = ARDUINO if camera_type_input == '1' else IP
            break
        else:
            print("Invalid camera type. Please enter 1 for 'Arduino' or 2 for 'IP'.")

    if camera_type == ARDUINO:
        port = input("Enter Arduino port (e.g., COM4): ").strip()
        baudrate = input("Enter Arduino baud rate: ").strip()
        # check no value provided just initialize wiht default 

        if port == "":
            print("No port provided, initializing with default value COM4")
            port = 'COM4'
        
        if baudrate == "":
            print("No baudrate provided, initializing with default value 1_000_000")
            baudrate = 1_000_000
        
        arduino_camera = CameraManager(camera_type, port=port, baud=int(baudrate))
    elif camera_type == IP:
        ip_address = input("Enter IP camera address (e.g., http://192.168.1.13:8080/video): ").strip()
        ip_camera = CameraManager(camera_type, ip_address=ip_address)

    while True:
        if camera_type == ARDUINO:
            frame = arduino_camera.capture_frame()
            if frame is None:
                print("Error reading frame from Arduino camera")
                break

            cv2.imshow('Arduino Camera', frame)
        elif camera_type == IP:
            frame = ip_camera.capture_frame()
            if frame is None:
                print("Error reading frame from IP camera")
                break

            cv2.imshow('IP Camera', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
