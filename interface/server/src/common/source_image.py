##########################################
## SERVER / SRC | COMMON / SOURCE_IMAGE ##
##########################################


################
# - PACKAGES - #
################

# -- General -- #
import cv2
from flask import Blueprint, send_file, request, jsonify
import io
import json
import numpy as np
import os
import ultralytics  # YOLO Models

# -- Scripts based Import -- #
from .utils import get_path_to_storage
from .utils_detections import detect_and_draw_detection

############
# - CORE - #
############

# -- Initialize the Blueprint -- #
src_image = Blueprint("basic_detector_source_image", __name__)

# -------------------- #
# - GLOBAL VARIABLES - #
# -------------------- #

# -- Route Name -- #
srcRoute = '/source/image/'

# -- Paths -- #
pathStorage = get_path_to_storage()  # Path to the Storage Folder

# -- Initialize the YOLOv8 Model -- #
model = ultralytics.YOLO(os.path.join(pathStorage, 'yolov8n.pt'))


# ---------- #
# - ROUTES - #
# ---------- #

# - Default "/" - #
@src_image.route(srcRoute)
def default():
  	return "Application Programming Interface [API] || Motion Detector Module - Video Source"


# ----------------- #
# - VIDEO SOURCE  - #
# ----------------- #

# - Run the Process - #
@src_image.route(f'{srcRoute}/run-process', methods=['POST'])
def run_job_process():
    # Initialize the Variables
    try:
        file_bytes = request.files['image'].read()
        weights = request.form.get('weights')
        if isinstance(weights, str):
            weights = json.loads(weights)
        if not isinstance(weights, list):
            weights = list(weights.values())
        confidence = float(request.form.get('confidence'))
        ioU = float(request.form.get('iou'))        
    except:
        return jsonify({"error": "Invalid Input Variables"}), 400
    
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)    
    file_Im = detect_and_draw_detection(model, img, weights, confidence, ioU)
    
    # Convert the processed image back to a file format (e.g., JPEG)
    _, img_encoded = cv2.imencode('.jpg', file_Im)
    img_bytes = img_encoded.tobytes()

    # Use an in-memory bytes buffer to store the image file
    img_buffer = io.BytesIO(img_bytes)
    img_buffer.seek(0)

    # Send the image file back in the response
    return send_file(img_buffer, mimetype='image/jpeg', as_attachment=True, download_name='processed_image.jpg')
