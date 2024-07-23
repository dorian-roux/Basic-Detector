###################################
# BASIC - DETECTOR | SRC / WEBCAM # 
###################################

# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import cv2
from moviepy.editor import VideoFileClip
import os
import time
from tqdm import tqdm

# - Custom Libraries - #
from .detection import detect_and_draw_detection
from .utils import save_image



# --------- #
# FUNCTIONS #
# --------- #

# # - Perform Detection - #
# def perform_video_detection(path_video: str, path_temp_video: str, path_output_video: str, save_frames: bool, model, categories: list, confidence: float, iou: float):
#     """Perform detection on an image.
#     Args:
#         path_video (str): the path to the video.
#         path_temp_video (str): the path to the temporary video.
#         path_output_video (str): the path to the output video.
#         save_frames (bool): whether to save the frames or not.
#         model: the YOLO model.
#         categories (list): the categories to detect.
#         confidence (float): the confidence threshold.
#         iou (float): the IoU threshold.
#     """    
#     cap = cv2.VideoCapture(path_video)  # Open the Video File
#     if not cap.isOpened():  # Ensure the Video File is opened
#         print("Error: Could not open video file.")
#         exit()
        
#     # Get video properties
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 file format
#     width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
#     # VideoWriter Object   
#     out_detection = cv2.VideoWriter(path_temp_video, fourcc, fps, (width, height))

#     # Process the Video Frames
#     ls_output_frames = []
#     with tqdm(total=total_frames, desc="Processing Video") as pbar:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break  # Exit loop when no more frames are available
            
#             # Write the annotated frame to the output video
#             output_frame = detect_and_draw_detection(model, frame, categories, confidence, iou)
#             ls_output_frames.append(output_frame)
#             out_detection.write(output_frame)

#             # Update progress bar
#             pbar.update(1)
            

#     # Release resources
#     cap.release()
#     out_detection.release()  
    
#     # Manage Audio
#     audioClip = VideoFileClip(path_video).audio
#     videoClip = VideoFileClip(path_temp_video)
#     outputVideo = videoClip.set_audio(audioClip)
#     outputVideo.write_videofile(path_output_video, logger=None)
    
#     # Remove the Temporary Video File
#     os.remove(path_temp_video)
    
#     # Save the Frames (if required)
#     if (save_frames):
#         for n, frame in tqdm(enumerate(ls_output_frames), desc='Saving Frames', total=len(ls_output_frames)):
#             save_image(os.path.join(os.path.dirname(path_output_video), 'frames', os.path.basename(path_output_video.split('.')[0]), f"frame-{n+1}.jpg"), frame)
    
#     # Return True
#     return True
   

# - Detection from an File - #
def webcam_feed_detection(path_output_folder: str, is_live_detection: bool, save_frames: bool, model, categories: list, confidence: float, iou: float):
    """Detect objects from categories within a webcam feed.
    Args:
        path_output_folder (str): The path to the output folder.
        is_live_detection (bool): Whether to perform live detection or not.
        save_frames (bool): Whether to save the frames or not.
        model: The YOLO model.
        categories (list): The categories to detect.
        confidence (float): The confidence threshold.
        iou (float): The IoU threshold
    """    
    cap = cv2.VideoCapture(0)  # Open the Webcam
    if not cap.isOpened():  # Ensure the Webcam is opened
        print("Error: Could not open webcam.")
        exit()

    # Set the Video Size Parameters
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 file format
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Initialize the Frame Lists and Time
    ls_input_frames, ls_output_frames = [], []
    initTime = None

    # Loop until 'ESC' is pressed
    print("Press 'ESC' to Exit the Live Webcam Feed...")
    while True:  
        initTime = time.time() if not initTime else initTime  # Initialize the Time

        ret, frame = cap.read()  # Read the Frame
        if not ret:  # Break the loop if the frame is not read
            print("Error: Failed to capture image.")
            break
        
        ls_input_frames.append(frame)
        if is_live_detection:
            ls_output_frames.append(detect_and_draw_detection(model, frame, categories))
            cv2.imshow('Webcam Feed', ls_output_frames[-1])  # Display the DETECTION feed
        else:
            cv2.imshow('Raw Feed', ls_input_frames[-1])  # Display the RAW feed
        
        # Exit the Loop
        key = cv2.waitKey(1) & 0xFF  # Wait for a key press
        if key == 27:  # Exit loop on 'ESC' key press
            print("Exiting the Live Webcam Feed...")
            cap.release()
            cv2.destroyAllWindows()
            fps = len(ls_input_frames) / (time.time() - initTime)
            break
         
    if not is_live_detection:
        print("Processing...")
        ls_output_frames = list(map(lambda frame: detect_and_draw_detection(model, frame, categories), tqdm(ls_input_frames)))
    
    
    # Output Video Files
    os.makedirs(path_output_folder, exist_ok=True)
    output_video_path = os.path.join(path_output_folder, f"output-conf_{str(confidence).split('.')[-1]}-iou_{str(iou).split('.')[-1]}.mp4")
    
    # Save the Detections Video
    out_detection = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    for frame in ls_output_frames:
        out_detection.write(frame)
    out_detection.release()
    
    # Manage Audio
    videoClip = VideoFileClip(output_video_path)
    outputVideo = videoClip.set_audio(None)
    outputVideo.write_videofile(output_video_path, logger=None)
       
    # Save the Frames (if required)
    if (save_frames):
        for n, frame in tqdm(enumerate(ls_output_frames), desc='Saving Frames', total=len(ls_output_frames)):
            save_image(os.path.join(path_output_folder, 'frames', f"frame-{n+1}.png"), frame)
    
    # Close the Windows
    cv2.destroyAllWindows()

    # Return True
    return True