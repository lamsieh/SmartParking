from flask import Flask, jsonify, Blueprint, app
import re
import time  # Pour simuler un délai dans la boucle while
from .camera_manager import  CameraManager
from .plate_detector_old import  detect_license_plate_from_ip
import cv2

ARDUINO = 'Arduino'
IP = 'IP'

bp = Blueprint('models', __name__, url_prefix='/models')






def detect_parking(frame):
    # Simuler la détection d'état de parking
    return {
        "timestamp": time.time(),
        "positions": {
            "a": True,
            "b": False,
            "c": True
        }
    }


@bp.route('/car-detected', methods=['GET'])
def car_detected():
    camera = CameraManager(camera_type=IP, ip_address="http://192.168.19.67:8080/video")
    number_plate = ""

    number_plate = detect_license_plate_from_ip('192.168.19.67')
        

    pattern = r"\b\d(?:\s\d){3}\b"

    
    return jsonify({
        "number_plate": number_plate,
    })

