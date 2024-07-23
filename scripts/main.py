###########################
# BASIC - DETECTOR | MAIN # 
###########################
# Description: This script purposes is to detect objects from multiple sources (webcam feed, video.s, image.s). 
# Author: Dorian ROUX
# Date: 2024-07-23
# Version: 1.1.0


# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import datetime
import json
import logging
import os

# - Custom Libraries - #
from src import print_prettify, find_folder_with_depth, generate_unique_id, input_with_retries, initialize_model, initialize_categories
from src import image_detection_from_file, image_detection_from_folder, video_detection_from_file, video_detection_from_folder, webcam_feed_detection

# - Logging - #
logging.getLogger('ultralytics').setLevel(logging.WARNING)



# ---- #
# CORE #
# ---- #

if __name__ == '__main__':
    print_prettify('Welcome to the Detector!', sep='#', post_space=True)

    # +------------------+ #
    # | Initialize Paths | #
    # +------------------+ #
    cur_dir = os.path.dirname(os.path.abspath(__file__))  # Get the Current Directory
    ts, id = str(round(datetime.datetime.now().timestamp())), generate_unique_id()  # Generate a Timestamp and an Unique ID
    path_data = find_folder_with_depth(cur_dir, 'data', max_depth=3)  # Find the DATA Folder
    if not path_data:  # Exit if the DATA Folder is not found
        print("\n! > You ENVIRONMENT is missing the folder \"data\" !")
        print('-> Exiting the Detector...')
        exit()
    
    # +------------------------ #
    # | Initialize Parameters | #
    # +------------------------ #
    print_prettify('Initialization of the Parameters', sep='-')  # Section Title
    # Initialize the Model
    model = initialize_model(path_data)
    if not model:  # Model not Found
        print("-> Model not Found.")
        print("-> Exiting the Detector...")
        exit()
       
    # Initialize the Confidence Threshold
    print('-> Setting the Confidence Threshold...')  # Section Title
    print(f'(The Confidence Threshold is a metric used to evaluate the accuracy of an object detection algorithm.)')
    default_confidence_threshold = 0.3
    user_conf_thsld = input_with_retries(f">> Enter the Confidence Threshold for Detection [0 - 100]% (Default: {default_confidence_threshold * 100}): ", "", max_retries=1)
    if not user_conf_thsld or not user_conf_thsld.isdigit() or (float(user_conf_thsld) < 0 and float(user_conf_thsld) > 100):
        confidence_threshold = default_confidence_threshold
        print("-> Invalid Confidence Threshold.")
        print(f"-> The Confidence Threshold is set to default which is {default_confidence_threshold}.\n")
    else:
        confidence_threshold = float(user_conf_thsld) / 100
        print(f"-> The Confidence Threshold is set to {confidence_threshold}.\n")
    
    # Initialize the IoU Threshold
    print('-> Setting the IoU Threshold...')  # Section Title
    print(f'(The IoU, Intersection over Union is a metric used to eliminate the overlapping bounding boxes.)')
    default_iou_threshold = 0.85
    user_iou_thsld = input_with_retries(f">> Enter the IoU Threshold for Detection [0 - 100]% (Default: {default_iou_threshold * 100}): ", "", max_retries=1)
    if not user_iou_thsld or not user_iou_thsld.isdigit() or (float(user_iou_thsld) < 0 and float(user_iou_thsld) > 100):
        iou_threshold = default_iou_threshold
        print("-> Invalid IoU Threshold.")
        print(f"-> The IoU Threshold is set to default which is {default_iou_threshold}.\n")
    else:
        iou_threshold = float(user_iou_thsld) / 100
        print(f"-> The IoU Threshold is set to {iou_threshold}.\n")

        
    # Initialize the Categories
    categories = initialize_categories(model, path_data)
    if not categories:
        print("-> Categories not Found.")
        print("-> Exiting the Detector...")
        exit()    
    
    # +----------------------------- #
    # | Setup Detection Categories | #
    # +----------------------------- #
    print_prettify('Detection Categories', sep='-')  # Section Title
    categories_to_detect = []  # Initialize the Categories to Detect
    print(">> Select the Categories to Detect:")
    ls_available_categories = ["All"] + list(filter(lambda var: var not in categories_to_detect, list(categories.keys()))) 
    user_ctgs = input_with_retries(
        "\n".join([f"[{i+1}] {content} {'(Default)' if i == 0 else ''}" for i, content in enumerate(ls_available_categories)]) + "\n" + ">> Enter the corresponding ID(s) of the Categories to Detect [separate them with a comma ',']: ",
        f"list(map(lambda v : int(v), filter(lambda v : v.isdigit() and int(v) > 0 and int(v) < {len(ls_available_categories)}, res.split(','))))", max_retries=3
    )
    if not user_ctgs:  # Exit if no Categories are selected
        exit()
    for v in user_ctgs.split(','):  # Add the Categories to Detect
        if int(v) == 1 or 1 in list(map(lambda v : int(v), user_ctgs.split(','))):
            categories_to_detect = [categories[ctg] for ctg in categories]
            print(f" + All Categories are added to the Detection.")
            break
        categories_to_detect.append(categories[ls_available_categories[int(v)-1]])
        print(f" + \"{ls_available_categories[int(v)-1]}\" added to the Detection.")
   
  
    # +--------------- #
    # | Source Video | #
    # +--------------- #
    print_prettify('Source of the Video Feed', sep='-', pre_space=True)
    user_source = input_with_retries(">> Select the Source of the Video Feed:\n[1] Image File/Folder\n[2] Video File/Folder\n[3] Live Webcam\n>> Enter the corresponding ID: ", "res in ['1', '2', '3']", max_retries=3)
    if not user_source:
        exit()
    path_output_folder = os.path.join(path_data, ('videos' if user_source != '3' else 'images'), ('webcam' if user_source == '1' else 'records' if user_source == '2' else ''), ts)
    path_output_folder = f"{path_output_folder}-{id}" if os.path.exists(path_output_folder) else path_output_folder
    
    
    # +-------- #
    # | Image | #
    # +-------- #
    if user_source == '1':
        print_prettify('Image File/Folder', sep='-', pre_space=True)
        user_file_path = input_with_retries(">> Enter the PATH to the Image File/Folder (either Absolute or Relative): ", "res != ''", max_retries=1)
        if not os.path.exists(user_file_path) or not (os.path.exists(os.path.join(cur_dir, user_file_path))):
            print("-> File does not Exist!")
            print('-> Exiting the Detector...')
            exit()
        truePath = user_file_path if os.path.exists(user_file_path) else os.path.join(cur_dir, user_file_path)
        if os.path.isdir(truePath):
            print("-> Detection from an Image Folder is starting...")
            if image_detection_from_folder(path_output_folder, truePath, model, categories_to_detect, confidence_threshold, iou_threshold):
                print(f"-> Visit the folder \"{path_output_folder}\" to see the results.")
            else:
                print("-> Detection Failed.")
        else:      
            print("-> Detection from an Image File is starting...")
            if image_detection_from_file(path_output_folder, truePath, model, categories_to_detect, confidence_threshold, iou_threshold):
                print(f"-> Visit the folder \"{path_output_folder}\" to see the results.")
            else:
                print("-> Detection Failed.")
        
        
    # +-------- #
    # | Video | #
    # +-------- #
    if user_source == '2':
        print_prettify('Video File/Folder', sep='-', pre_space=True)
        
        # - Save Frames - #
        user_save_frames = input_with_retries(">> Do you want to save every Frames and their Detections from the Video? [Y/N]: ", "res.lower() in ['y', 'n']", max_retries=3)
        if not user_save_frames:
            print("-> Exiting the Detector...")
            exit()
        user_save_frames = True if user_save_frames.lower() == 'y' else False
        
        # File/Folder Path
        user_file_path = input_with_retries(">> Enter the PATH to the Video File/Folder (either Absolute or Relative): ", "res != ''", max_retries=1)
        if not os.path.exists(user_file_path) or not (os.path.exists(os.path.join(cur_dir, user_file_path))):
            print("-> File does not Exist!")
            print('-> Exiting the Detector...')
            exit()
        truePath = user_file_path if os.path.exists(user_file_path) else os.path.join(cur_dir, user_file_path)
        
        # - Perform Detection - #
        if os.path.isdir(truePath):
            print("-> Detection from a Video Folder is starting...")
            if video_detection_from_folder(path_output_folder, truePath, user_save_frames, model, categories_to_detect, confidence_threshold, iou_threshold):
                print(f"-> Visit the folder \"{path_output_folder}\" to see the results.")
            else:
                print("-> Detection Failed.")
        else:      
            print("-> Detection from a Video File is starting...")
            if video_detection_from_file(path_output_folder, truePath, user_save_frames, model, categories_to_detect, confidence_threshold, iou_threshold):
                print(f"-> Visit the folder \"{path_output_folder}\" to see the results.")
            else:
                print("-> Detection Failed.")
      
                
    # +--------- #
    # | Webcam | #
    # +--------- #
    if user_source == '3':
        print_prettify('Live Webcam', sep='-', pre_space=True)  
        
        # - Detection Mode (Smoothness vs Speed) - #
        user_webcam_mode = input_with_retries(">> Select the Mode of the Detector:\n[1] Live Detection (faster processing but smoothless)\n[2] Detection after Capture (slower processing but smoother)\nPress 1 or 2: ", "res in ['1', '2']", max_retries=3)
        if not user_webcam_mode:
            print("-> Exiting the Detector...")
            exit()
        is_live_detection = True if user_webcam_mode == '1' else False

        # - Save Frames - #
        user_save_frames = input_with_retries(">> Do you want to save every Frames and their Detections from the Video? [Y/N]: ", "res.lower() in ['y', 'n']", max_retries=3)
        if not user_save_frames:
            print("-> Exiting the Detector...")
            exit()
        user_save_frames = True if user_save_frames.lower() == 'y' else False
        
        # - Perform Detection - #
        print("\n->Live Webcam Feed is starting...")
        if webcam_feed_detection(path_output_folder, is_live_detection, user_save_frames, model, categories_to_detect, confidence_threshold, iou_threshold):
            print(f"->Visit the folder \"{path_output_folder}\" to see the results.")


    # +------- #
    # | Exit | #
    # +------- #
    print_prettify('End of the Detector!', sep='#', pre_space=True)