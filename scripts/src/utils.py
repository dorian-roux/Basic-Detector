##################################
# BASIC - DETECTOR | SRC / UTILS # 
##################################

# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import cv2
import json
import os
from moviepy.editor import VideoFileClip
import numpy as np
import random
import string
import time
from tqdm import tqdm
from ultralytics import YOLO



# --------- #
# FUNCTIONS #
# --------- #
        
        
# +-------+ #
# Utilities #
# +-------+ #

# - Output a Pretty Text - #
def print_prettify(text: str, sep: str = '-', pre_space: bool = False, post_space: bool = False):
    """Output a pretty text by adding separators around it.
    Args:
        text (str): the text to make pretty.
        sep (str, optional): the separator to use. Defaults to '-'.
        pre_space (bool, optional): whether to add a space before the text. Defaults to False.
        post_space (bool, optional): whether to add a space after the text. Defaults to False.
    """    
    text = f"{sep} {text} {sep}"
    print(('\n' if pre_space else '' ) + f"{sep*len(text)}\n{text}\n{sep*len(text)}" + ('\n' if post_space else ''))    


# - Find a Folder based on its Name and Depth Level
def find_folder_with_depth(root_dir: str, target_folder_name: str, max_depth: int = 2):
    """Search for a specific folder within the given root directory and its parent directories up to a certain depth.
    Args:
        root_dir (str): The root directory to start searching from.
        target_folder_name (str): The name of the folder to search for.
        max_depth (int): The maximum depth level of parent directories to search.
    """
    # Return if the Maximum Depth is Reached
    if max_depth < 0:
        return 
    # Loop through the Parent Directories up to the Maximum Depth
    if any(entry == target_folder_name and os.path.isdir(os.path.join(root_dir, entry)) for entry in os.listdir(root_dir)):
        return os.path.join(root_dir, target_folder_name)
    # Recursively Update the Root Directory and Depth Level
    return find_folder_with_depth(os.path.dirname(root_dir), target_folder_name, max_depth - 1)


# - Generate a Unique Identifier - #
def generate_unique_id(length: int = 10):
    """Generate an unique identifier.
    Args:
        length (int, optional): the length of the unique identifier. Defaults to 10.
    """    
    return ''.join(np.random.choice(list(string.ascii_letters + string.digits), length))


# - Execute a Input Prompt with Retries and Verification
def input_with_retries(prompt: str, verification_str: str, current_try: int = 0, max_retries: int = 1):
    """
    Prompts the user for input with a specified number of retries.
    Args:
        prompt (str): The input prompt text.
        verification_str (str): A string that will be evaluated to check if the input is valid.
        max_retries (int): The maximum number of retries allowed. Default is 1.
    """
    if current_try >= max_retries:
        print("-> Maximum retries Exceeded.")
        print("-> Exiting the Detector...")
        exit()
    latest_line = f"(Attempt {current_try + 1} of {max_retries}) " + prompt.split('\n')[-1]    
    input_str = latest_line if current_try != 0 else ("\n".join(prompt.split('\n')[:-1]) + "\n" + latest_line if "\n" in prompt else latest_line)
    res = input(input_str)
    try:
        if not verification_str:  # If no verification string is provided, return the input
            return res
        if eval(verification_str):  # Evaluate the verification string
            return res      
    except Exception as e:
        print(e)
        print("-> Error while Verifying the Input.")
        print("-> Exiting the Detector...")
        exit()
    return input_with_retries(prompt, verification_str, current_try + 1, max_retries)




# +------------------+ #
# Model and Categories #
# +------------------+ #

# - Initializes the Model (YOLOv8)
def initialize_model(path_data: str, default_model_name: str = 'yolov8n.pt'):
    """Initializes the Model.
    Args:
        path_data (str): The path to the DATA folder.
        default_model_name (str, optional): The default name of the model file. Defaults to 'yolov8n.pt'.
    """    
    print('-> Finding the YOLOv8 Model...')  # Section Title    
    output_path = os.path.join(path_data, default_model_name)
    if not os.path.exists(output_path):  # Generate a new Model if not found
        print(' > YoloV8 Model not found in the DATA folder | Generating a new one...')
    model = YOLO(output_path, verbose=False)  # Load the Model and Avoid Verbose Output
    print(f"-> Model loaded from {output_path}.\n")
    return model


# - Construct Categories Detection - #
def construct_categories_detection(lsClass: dict):
    """Construct the Categories for the Detection
    Args:
        lsClass (dict): List of Classes.
        savePath (str, optional): Path to save the Categories. Defaults to None.
    """    
    # Initialize the Categories #
    categories = {
        "People": { "LIST": [0], "COLOR": [255, 0, 0] },
        "Vehicle": { "LIST": [1, 2, 3, 4, 5, 6, 7, 8], "COLOR": [0, 255, 0] },
        "Traffic Items": { "LIST": [9, 10, 11, 12], "COLOR": [0, 0, 255] },
        "Animals": { "LIST": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "COLOR": [255, 255, 0] },
        "Accessories": { "LIST": [24, 25, 26, 27, 28], "COLOR": [0, 255, 255] },
        "Sports": { "LIST": [29, 30, 31, 32, 33, 34, 35, 36, 37, 38], "COLOR": [255, 0, 255] },
        "Kitchen Items": { "LIST": [39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55], "COLOR": [128, 0, 0] },
        "Furniture": { "LIST": [56, 57, 58, 59, 60, 61], "COLOR": [0, 128, 0] },
        "Electronics": { "LIST": [62, 63, 64, 65, 66, 67], "COLOR": [0, 0, 128] },
        "Appliances": { "LIST": [68, 69, 70, 71, 72], "COLOR": [128, 128, 0] },
        "Miscellaneous": { "LIST": [13, 73, 74, 75, 76, 77, 78, 79], "COLOR": [128, 0, 128] }
    }
    categories = {k : {"NAME": k, "LIST": p["LIST"], "COLOR": p["COLOR"], "COUNT": len(p["LIST"]), "OBJECTS": {}} for k, p in categories.items()}
    # Loop through each CLASS and assign it to a CATEGORY #
    for idc, val in tqdm(lsClass.items(), desc='Associate Categories and Classes'):  # idc: ID of the Class, val: Name of the Class
        for _, v in categories.items():  # _: Name of the Category, v: Dict of the Category
            if idc in v["LIST"]:
                v["OBJECTS"].update({idc: val})
    # Return the Categories
    return categories


# - Initializes the Categories
def initialize_categories(model: YOLO, path_data: str, default_categories_name: str = 'categories.json'):
    """Initializes the Categories.
    Args:
        model (YOLO): The YOLOv8 Model.
        path_data (str): The path to the DATA folder.
        default_categories_name (str, optional): The default name of the categories file. Defaults to 'categories.json'.
    """    
    default_path_categories = os.path.join(path_data, default_categories_name)
    
    # Load  #
    if os.path.exists(default_path_categories):  # Load the categories if found
        print('-> Finding the categories...')  # Section Title
        userLdCtgs = input_with_retries(">> Do you want to load existing categories? [Y/N]: ", "res.lower() in ['y', 'n']", max_retries=3) 
        if userLdCtgs.lower() == 'y':
            try:
                categories = json.load(open(default_path_categories, 'r'))
                print(f"-> Categories loaded from {default_path_categories}.\n")
                return categories
            except:
                print(" > Error while Loading the categories.")      
    
    # Construct #
    print('-> Constructing the categories...')  # Construct the categories
    user_scategories = input_with_retries(">> Do you want to save the categories? [Y/N]: ", "res.lower() in ['y', 'n']", max_retries=3)
    s_categories_path = ''
    if user_scategories.lower() == 'y':
        s_categories_path = input(f">> Enter the Path where to save the categories [Default Path: \"{default_path_categories}\"]\n>> : ")
        if not s_categories_path:
            s_categories_path = default_path_categories
            print(f"-> No Path provided. Saving the categories in the Default Path: {s_categories_path}")
        if s_categories_path and not os.path.exists(os.path.dirname(s_categories_path)):
            print(f" > Path to the File \"{os.path.dirname(s_categories_path)}\" Invalid | categories will not be saved.")
            s_categories_path = ''
    categories = construct_categories_detection(model.names)
    if s_categories_path:  # Save the Categories (if path is provided)
        json.dump(categories, open(s_categories_path, 'w'), indent=2)
        print(f"-> Categories saved in {s_categories_path}.\n")
        
    # Return #
    return categories


# ---- #
# Save #
# ---- #

# - Save an Image - #
def save_image(path_output: str, image):
    """Save an image to the output folder.
    Args:
        path_output (str): the path to the output folder.
        image: the image to save.
    """    
    os.makedirs(os.path.dirname(path_output), exist_ok=True)  # Create the Directory Folder
    cv2.imwrite(path_output, image)  # Save the Image
    return True