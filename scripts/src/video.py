##################################
# BASIC - DETECTOR | SRC / VIDEO # 
##################################

# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import cv2
from moviepy.editor import VideoFileClip
import os
from tqdm import tqdm

# - Custom Libraries - #
from .detection import detect_and_draw_detection
from .utils import save_image



# --------- #
# FUNCTIONS #
# --------- #

# - Perform Detection - #
def perform_video_detection(path_video: str, path_temp_video: str, path_output_video: str, save_frames: bool, model, categories: list, confidence: float, iou: float):
    """Perform detection on an image.
    Args:
        path_video (str): the path to the video.
        path_temp_video (str): the path to the temporary video.
        path_output_video (str): the path to the output video.
        save_frames (bool): whether to save the frames or not.
        model: the YOLO model.
        categories (list): the categories to detect.
        confidence (float): the confidence threshold.
        iou (float): the IoU threshold.
    """    
    cap = cv2.VideoCapture(path_video)  # Open the Video File
    if not cap.isOpened():  # Ensure the Video File is opened
        print("Error: Could not open video file.")
        exit()
        
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 file format
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # VideoWriter Object   
    out_detection = cv2.VideoWriter(path_temp_video, fourcc, fps, (width, height))

    # Process the Video Frames
    ls_output_frames = []
    with tqdm(total=total_frames, desc="Processing Video") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Exit loop when no more frames are available
            
            # Write the annotated frame to the output video
            output_frame = detect_and_draw_detection(model, frame, categories, confidence, iou)
            ls_output_frames.append(output_frame)
            out_detection.write(output_frame)

            # Update progress bar
            pbar.update(1)
            

    # Release resources
    cap.release()
    out_detection.release()  
    
    # Manage Audio
    audioClip = VideoFileClip(path_video).audio
    videoClip = VideoFileClip(path_temp_video)
    outputVideo = videoClip.set_audio(audioClip)
    outputVideo.write_videofile(path_output_video, logger=None)
    
    # Remove the Temporary Video File
    os.remove(path_temp_video)
    
    # Save the Frames (if required)
    if (save_frames):
        for n, frame in tqdm(enumerate(ls_output_frames), desc='Saving Frames', total=len(ls_output_frames)):
            save_image(os.path.join(os.path.dirname(path_output_video), 'frames', os.path.basename(path_output_video.split('.')[0]), f"frame-{n+1}.png"), frame)
    
    # Return True
    return True
   

# - Detection from an File - #
def video_detection_from_file(path_output_folder: str, path_video: str, save_frames: bool, model, categories: list, confidence: float, iou: float):
    """Detect objects from categories within a video.
    Args:
        path_output_folder (str): The path to the output folder.
        path_video (str): The path to the video file.
        save_frames (bool): Whether to save the frames or not.
        model: The YOLO model.
        categories (list): The categories to detect.
        confidence (float): The confidence threshold.
        iou (float): The IoU threshold
    """    
    os.makedirs(path_output_folder, exist_ok=True)
    v_extension = os.path.basename(path_video).split('.')[-1]  # Get the Image Extension
    temp_video, output_video = os.path.join(path_output_folder, f'temp.{v_extension}'), os.path.join(path_output_folder, f"output-conf_{str(confidence).split('.')[-1]}-iou_{str(iou).split('.')[-1]}.{v_extension}"),
    return perform_video_detection(path_video, temp_video, output_video, save_frames, model, categories, confidence, iou)  # Perform Detection
       
    
# - Detection from a Folder - #
def video_detection_from_folder(path_output_folder: str, path_folder: str, save_frames: bool, model, categories: list, confidence: float, iou: float):
    """Detect objects from categories within a folder of videos.
    Args:
        path_output_folder (str): The path to the output folder.
        path_folder (str): The path to the folder.
        save_frames (bool): Whether to save the frames or not.
        model: The YOLO model.
        categories (list): The categories to detect.
        confidence (float): The confidence threshold.
        iou (float): The IoU threshold
    """    
    try:  # Try to Perform Detection
        ls_files = [os.path.join(path_folder, file) for file in os.listdir(path_folder) if file.split('.')[-1] in ['mp4', 'avi', 'mov']]  # Get the List of Video Files
        # - No Video Files Found - #
        if len(ls_files) == 0:  # No Image Files Found
            print("-> No Video Files Found in the Folder.")
            return False
        
        # - Single Image File - #
        if len(ls_files) == 1:  # Single Image File
            return video_detection_from_file(path_output_folder, ls_files[0], save_frames, model, categories, confidence, iou)
        
        # - Multiple Video Files - #
        os.makedirs(path_output_folder, exist_ok=True)
        for n, path_video in tqdm(enumerate(ls_files), desc='Detecting Objects from Videos', total=len(ls_files)):  # Loop through the Image Files
            v_extension = os.path.basename(path_video).split('.')[-1]  # Get the Video Extension
            temp_video, output_video = os.path.join(path_output_folder, f"temp-{n}-conf_{str(confidence).split('.')[-1]}-iou_{str(iou).split('.')[-1]}.{v_extension}"), os.path.join(path_output_folder, f'output-{n}.{v_extension}'),
            perform_video_detection(path_video, temp_video, output_video, save_frames, model, categories, confidence, iou)  # Perform Detection
        return True
    
    except Exception as _:  # Error
        return None