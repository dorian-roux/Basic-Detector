########################################
## SERVER / SRC | COMMON / UTILS_JOBS ##
########################################

# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import json
import os
import random 
import string
import time

# --------- #
# FUNCTIONS #
# --------- #

# - Generate randomly a Job Identifier - #
def generate_job_id(outer_length: int = 8):
    """Generate randomly a Job Identifier.
    Args:
        outer_length (int, optional): Length of the Outer Key. Defaults to 8.
    """      
    innerKey = str(round(time.time()))
    outerKey = ''.join(random.choices(string.ascii_lowercase + string.digits, k=outer_length))
    return f"{innerKey}-{outerKey}"
   
# - Create a New Job - #
def create_new_job(pathTemp: str):
    """Initialize the Process.
    Args:
        pathTemp (str): Path to the Temporary Folder.
    """    
    jobID = generate_job_id()
    if os.path.exists(os.path.join(pathTemp, f'{jobID}.json')):
        os.remove(os.path.join(pathTemp, f'{jobID}.json'))
    json.dump({}, open(os.path.join(pathTemp, f'{jobID}.json'), 'w'))
    return jobID

# - Get the Process Job Data - #
def get_job_data(pathTemp: str, jobID: str):
    """Get the Process Job Data.
    Args:
        pathTemp (str): Path to the Temporary Folder.
        jobID (str): Job Identifier.
    """    
    if os.path.exists(os.path.join(pathTemp, f'{jobID}.json')):
        return json.load(open(os.path.join(pathTemp, f'{jobID}.json')))
    return {}

# - Save the Process Job Data - #
def save_job_data(pathTemp: str, jobID: str, jobData: dict, keys: list = ['WEIGHTS', 'PROGRESS', 'RESULT']):
    """Save the Process Job Data.
    Args:
        pathTemp (str): Path to the Temporary Folder.
        jobID (str): Job Identifier.
        jobData (dict): Job Data.
    """    
    json.dump({key: jobData[key] for key in keys}, open(os.path.join(pathTemp, f'{jobID}.json'), 'w'), indent=4)
    return True
    
# - Delete the Process Job Data - #
def delete_job_data(pathTemp: str, jobID: str):
    """Delete the Process Job Data.
    Args:
        pathTemp (str): Path to the Temporary Folder.
        jobID (str): Job Identifier.
    """    
    if os.path.exists(os.path.join(pathTemp, f'{jobID}.json')):
        os.remove(os.path.join(pathTemp, f'{jobID}.json'))
        return True
    return False