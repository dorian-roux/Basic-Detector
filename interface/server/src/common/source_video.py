##########################################
## SERVER / SRC | COMMON / SOURCE_VIDEO ##
##########################################


################
# - PACKAGES - #
################

# -- General -- #
import json
from flask import Blueprint, send_file, request, jsonify
import os
import shutil
import ultralytics  # YOLO Models

# -- Scripts based Import -- #
from .utils import get_path_to_storage
from .utils_jobs import create_new_job, save_job_data, get_job_data, delete_job_data
from .utils_detections import video_file_feed

############
# - CORE - #
############

# -- Initialize the Blueprint -- #
src_video = Blueprint("basic_detector_source_video", __name__)

# -------------------- #
# - GLOBAL VARIABLES - #
# -------------------- #

# -- Route Name -- #
srcRoute = '/source/video/'

# -- Configuration and Paths -- #
pathStorage = get_path_to_storage()  # Path to the Storage Folder
pathFolderTmp = os.path.join(pathStorage, 'tmp') # Temporary Folder

# -- Create the Temporary Folder if it does not exist -- #
os.makedirs(pathFolderTmp, exist_ok=True)

# -- Initialize the YOLOv8 Model -- #
model = ultralytics.YOLO(os.path.join(pathStorage, 'yolov8n.pt'))


# ---------- #
# - ROUTES - #
# ---------- #

# - Default "/" - #
@src_video.route(srcRoute)
def default():
  	return "Application Programming Interface [API] || Motion Detector Module - Video Source"


# ----------------- #
# - VIDEO SOURCE  - #
# ----------------- #


# - Launch Process by Creating a JOB - #
@src_video.route(f'{srcRoute}/launch-process', methods=['POST'])
def launch_process():
    # Create a Job ID for this Processing Task
    job_id = create_new_job(pathFolderTmp)
   
    # Initialize the Weights
    try:
        weights = request.json.get('weights')
        if isinstance(weights, str):
            weights = json.loads(weights)
        if not isinstance(weights, list):
            weights = list(weights.values())
        confidence = float(request.json.get('confidence'))
        ioU = float(request.json.get('iou'))      
    except:
        return jsonify({"error": "Weights not found"}), 404
        
    # Save the Process Data
    save_job_data(pathFolderTmp, job_id, {"PROGRESS": 0, "WEIGHTS": weights, "CONFIDENCE": confidence, "IOU": ioU, "RESULT": ""})

    # Return the Job ID
    return jsonify({"job_id": job_id}), 200


# - Run the Process of the JOB - #
@src_video.route(f'{srcRoute}/run-process/<job_id>', methods=['POST'])
def run_job_process(job_id):
    try:
        file_bytes = request.files['video'].read()
    except:
        return jsonify({"error": "Video not found"}), 404
    
    job_data = get_job_data(pathFolderTmp, job_id)
    if not job_data:  # Verify the Job ID Exists
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"success": video_file_feed(pathFolderTmp, job_id, job_data, file_bytes, model)}), 200


# - Get the Progress of the JOB - #
@src_video.route(f'{srcRoute}/get-progress/<job_id>', methods=['GET'])
def get_job_progress(job_id):
    try:
        job_data = get_job_data(pathFolderTmp, job_id)
    except:
        return jsonify({'progress': None}), 200
    if not job_data:  # Verify the Job ID Exists
        return jsonify({'progress': None}), 200
    return jsonify({"progress": job_data.get('PROGRESS')}), 200


# - Get the Result of the Process of the JOB - #
@src_video.route(f'{srcRoute}/result-process/<job_id>', methods=['GET'])
def get_job_result(job_id):
    job_data = get_job_data(pathFolderTmp, job_id)
    if not job_data:  # Verify the Job ID Exists
        return jsonify({"error": "Job not found"}), 404
    
    # Save the Final Video as a Response
    response = send_file(job_data['RESULT'], mimetype='video/mp4', as_attachment=True, download_name='processed_video.mp4')
    
    # Clean the Temporary Folder
    if os.path.exists(os.path.dirname(job_data['RESULT'])):
        shutil.rmtree(os.path.dirname(job_data['RESULT']))
    delete_job_data(pathFolderTmp, job_id)
   
    # Return the Response
    return response


# - Delete a JOB - #
@src_video.route(f'{srcRoute}/delete-job/<job_id>', methods=['GET'])
def delete_job(job_id):
    job_data = get_job_data(pathFolderTmp, job_id)
    if job_data:
        delete_job_data(pathFolderTmp, job_id)  # If so, delete it from the Memory Store
        return jsonify({"message": f"the process #{job_id} has been removed successfully"}), 200
    return jsonify({"message": f"the process #{job_id} does not exist"}), 200


# - Display Simple Job - #
@src_video.route(f'{srcRoute}/display-job/<job_id>', methods=['GET'])
def display_job(job_id):
    job_data = get_job_data(pathFolderTmp, job_id)
    if not job_data:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job_data), 200