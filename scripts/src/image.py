##################################
# BASIC - DETECTOR | SRC / IMAGE # 
##################################

# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import cv2
import os
from tqdm import tqdm

# - Custom Libraries - #
from .detection import detect_and_draw_detection
from .utils import save_image



# --------- #
# FUNCTIONS #
# --------- #

# - Perform Detection - #
def perform_image_detection(path_im: str, model, categories: list, confidence: float, iou: float):
    """Perform detection on an image.
    Args:
        path_im (str): the path to the image.
        model: the YOLO model.
        categories (list): the categories to detect.
        confidence (float): the confidence threshold.
        iou (float): the IoU threshold.
    """    
    try:
        input_im = cv2.imread(path_im)  # Read the Image
        output_im = detect_and_draw_detection(model, input_im, categories, confidence, iou)  # Detect and Draw the Detection
        return input_im, output_im
    except Exception as _:
        return None, None


# - Detection from an File - #
def image_detection_from_file(path_output_folder: str, path_im: str, model, categories: list, confidence: float, iou: float):
    """Detect objects from categories within an image.
    Args:
        path_output_folder (str): The path to the output folder.
        path_im (str): The path to the image file.
        model: The YOLO model.
        categories (list): The categories to detect.
        confidence (float): The confidence threshold.
        iou (float): The IoU threshold
    """    
    input_im, output_im = perform_image_detection(path_im, model, categories, confidence, iou)  # Perform Detection
    if isinstance(input_im, type(None)) or isinstance(output_im, type(None)):  # No Image Found
        return None, None
    im_extension = os.path.basename(path_im).split('.')[-1]  # Get the Image Extension
    save_image(os.path.join(path_output_folder, f"input.{im_extension}"), input_im)  # Save the Input Image
    save_image(os.path.join(path_output_folder, f"output-conf_{str(confidence).split('.')[-1]}-iou_{str(iou).split('.')[-1]}.{im_extension}"), output_im)  # Save the Output Image
    return True
    

# - Detection from a Folder - #
def image_detection_from_folder(path_output_folder: str, path_folder: str, model, categories: list, confidence: float, iou: float):
    """Detect objects from categories within a folder.
    Args:
        path_output_folder (str): The path to the output folder.
        path_folder (str): The path to the folder.
        model: The YOLO model.
        categories (list): The categories to detect.
        confidence (float): The confidence threshold.
        iou (float): The IoU threshold
    """    
    try:  # Try to Perform Detection
        ls_files = [os.path.join(path_folder, file) for file in os.listdir(path_folder) if file.split('.')[-1] in ['jpg', 'jpeg', 'png']]  # Get the List of Image Files
        # - No Image Files Found - #
        if len(ls_files) == 0:  # No Image Files Found
            print("-> No Image Files Found in the Folder.")
            return False
        
        # - Single Image File - #
        if len(ls_files) == 1:  # Single Image File
            return image_detection_from_file(path_output_folder, ls_files[0], model, categories, confidence, iou)
        
        # - Multiple Image Files - #
        output_input_folder = os.path.join(path_output_folder, 'inputs')  # Create the Raw Folder
        output_output_folder = os.path.join(path_output_folder, 'outputs')  # Create the Result Folder
        for n, path_im in tqdm(enumerate(ls_files), desc='Detecting Objects from Images', total=len(ls_files)):  # Loop through the Image Files
            im_extension = os.path.basename(path_im).split('.')[-1]  # Get the Image Extension
            input_im, output_im = perform_image_detection(path_im, model, categories, confidence, iou)  # Perform Detection
            if isinstance(input_im, type(None)) or isinstance(output_im, type(None)):  # No Image Found
                continue
            save_image(os.path.join(output_input_folder, f"input-{n}.{im_extension}"), input_im)  # Save the Input Image
            save_image(os.path.join(output_output_folder, f"output-{n}-conf_{str(confidence).split('.')[-1]}-iou_{str(iou).split('.')[-1]}.{im_extension}"), output_im)  # Save the Output Image
        return True
    
    except Exception as _:  # Error
        return None