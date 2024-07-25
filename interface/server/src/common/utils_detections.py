##############################################
## SERVER / SRC | COMMON / UTILS_DETECTIONS ##
##############################################

# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import cv2
from moviepy.editor import VideoFileClip
import numpy as np
import os

# -- Scripts based Import -- #
from .utils_jobs import save_job_data

# --------- #
# FUNCTIONS #
# --------- #       
      
# - Get Category Information (Name and Color) based on an Index
def get_category_info(index: int, categories: list):
    """Get the Category Information based on the Index.
    Args:
        index (int): the index of the category
        categories (list): the list of categories
    """    
    cat = list(filter(lambda category: str(index) in list(map(str, category["LIST"])), categories))  # Filter the Category
    if cat: 
        return cat[0]["NAME"], cat[0]["COLOR"]
    return None, None  


# - Detect and Draw the Detection - #
def detect_and_draw_detection(model, frame: np.ndarray, categories: list, confidence_thsrld: float = 0.6, iou_thsrld: float = 0.8, has_verbose: bool = False):
    """Detect and draw the detection on the frame.
    Args:
        model (YOLO): the YOLO model
        frame (np.ndarray): the frame to detect
        categories (list): the categories to detect
        confidence (float): the confidence threshold
        iou (float): the IoU threshold
        hasVerbose (bool, optional): whether to display the verbose. Defaults to False.
    """    
    # Initialize the variables
    output_frame = frame.copy()
    try:
        results = model.predict(source=output_frame, verbose=has_verbose)  # Perform Detection
    except:
        return output_frame
    boxes, scores, class_ids = [], [], []  # Initialize lists for bounding boxes, scores, and class IDs
    
    # Collect bounding boxes and scores
    for result in results:  # Loop through the results
        for box in result.boxes:  # Loop through the boxes
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            confidence = box.conf[0].item()
            class_id = int(box.cls[0].item())
            boxes.append([x1, y1, x2, y2]), scores.append(confidence), class_ids.append(class_id)  # Append to lists
    boxes, scores, class_ids = np.array(boxes), np.array(scores), np.array(class_ids)  # Convert lists to numpy arrays
    indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), score_threshold=float(confidence_thsrld), nms_threshold=float(iou_thsrld))  # Apply Non-Maximum Suppression
    
    # Draw bounding boxes and labels
    if len(indices) > 0:
        indices = indices.flatten()
        for i in indices:  # Loop through the indices
            x1, y1, x2, y2 = boxes[i]        
            categoryName, categoryColor = get_category_info(class_ids[i], categories)  # Get category name and color
            if (not categoryName) or (not categoryColor):  # Skip if category name or color is not found
                continue
            cv2.rectangle(output_frame, (x1, y1), (x2, y2), tuple(categoryColor)[::-1], 4)  # Draw bounding box
            cv2.putText(output_frame, f'{categoryName} {scores[i]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, tuple(categoryColor)[::-1], 2)  # Draw label

    # Return the frame
    return output_frame



# - Video File Feed - #
def video_file_feed(pathFolderTmp: str, jobID: str, jobData: dict, videoBytes, model):
    """Open the Video File Feed.
    Args:
        pathFolderTmp (str): the temporary folder path
        jobID (str): the job ID
        jobData (dict): the job data
        model (YOLO): the YOLO model
    """
    # Initialize the Temporary Folder and Paths
    tmpFolder = os.path.join(pathFolderTmp, jobID)
    os.makedirs(tmpFolder, exist_ok=True)
    temp_alpha, temp_beta, temp_out = os.path.join(tmpFolder, 'output_alpha.mp4'), os.path.join(tmpFolder, 'output_beta.mp4'), os.path.join(tmpFolder, 'output.mp4')
    open(temp_alpha, 'wb').write(videoBytes)
    
    # Read the video stream using OpenCV
    cap = cv2.VideoCapture(temp_alpha)
    
    if not cap.isOpened():  # Ensure the Video File is opened
        print("Error: Could not open video file.")
        exit()

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 file format
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = remaining_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create the Video Writer
    out = cv2.VideoWriter(temp_beta, fourcc, fps, (width, height))
    
    # Loop through the frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit loop when no more frames are available
        
        # Write the annotated frame to the output video
        # try:
        out.write(detect_and_draw_detection(model, frame, jobData['WEIGHTS'], jobData['CONFIDENCE'], jobData['IOU']))
        # except Exception as e:
            # print(e)
            # out.write(frame)
        
        remaining_frames -= 1

        # Update the progress
        jobData['PROGRESS'] = round(((total_frames - remaining_frames)/total_frames)*100) 
        save_job_data(pathFolderTmp, jobID, jobData)
        # yield f"data: {json.dumps({'progress': jobData['PROGRESS']})}\n\n"
            
    # Release resources
    cap.release()
    out.release()

    # Manage Audio
    audioClip = VideoFileClip(temp_alpha).audio
    videoClip = VideoFileClip(temp_beta)
    outputVideo = videoClip.set_audio(audioClip)
    outputVideo.write_videofile(temp_out, logger=None) #, codec='libx264', audio_codec='aac')
            
    # Save
    jobData['PROGRESS'] = 101
    jobData['RESULT'] = temp_out
    save_job_data(pathFolderTmp, jobID, jobData)
      
    # yield f"data: {json.dumps({'progress': jobData['PROGRESS']})}\n\n"
    return True