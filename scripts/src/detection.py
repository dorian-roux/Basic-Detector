######################################
# BASIC - DETECTOR | SRC / DETECTION # 
######################################

# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import cv2
import numpy as np


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
def detect_and_draw_detection(model, frame: np.ndarray, categories: list, confidence_thsrld: float, iou_thsrld: float, has_verbose: bool = False):
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