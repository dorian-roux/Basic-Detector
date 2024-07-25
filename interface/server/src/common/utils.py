###################################
## SERVER / SRC | COMMON / UTILS ##
###################################

# --------- #
# LIBRARIES #
# --------- #

# - General Libraries - #
import os

# --------- #
# FUNCTIONS #
# --------- #

# - Get the Path to the Storage Folder - #
def get_path_to_storage(target_name: str = 'storage', target_folder: str = 'server'):
    """Get the Path to the Storage Folder.
    Args:
        target_name (str, optional): Name of the Target Folder. Defaults to 'storage'.
        target_folder (str, optional): Name of the Target Folder. Defaults to 'server'.
    """    
    if target_folder in os.path.abspath(os.getcwd()):
        return os.path.join(os.path.abspath(os.getcwd())[0:os.path.abspath(os.getcwd()).find(target_folder)], target_name)
    if os.path.exists(os.path.join(os.path.abspath(os.getcwd()), target_folder)):
        return os.path.join(os.path.abspath(os.getcwd()), target_folder, target_name)
    return os.path.join(os.path.abspath(os.getcwd()), target_name)