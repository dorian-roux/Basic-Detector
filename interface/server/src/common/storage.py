#####################################
## SERVER / SRC | COMMON / STORAGE ##
#####################################

################
# - PACKAGES - #
################

# -- General -- #
from flask import Blueprint
import json
import os

# -- Scripts based Import -- #
from .utils import get_path_to_storage


############
# - CORE - #
############

# -- Initialize the Blueprint -- #
storage = Blueprint("basic_detector_storage", __name__)

# -------------------- #
# - GLOBAL VARIABLES - #
# -------------------- #

# -- Route Name -- #
storageRoute = '/storage/'

# -- Configuration and Paths -- #
pathStorage = get_path_to_storage()  # Path to the Storage Folder

# ---------- #
# - ROUTES - #
# ---------- #

# - Default "/" - #
@storage.route(storageRoute)
def default():
  	return "Application Programming Interface [API] || Motion Detector Module - Storage"


# ----------- #
# | Storage | #
# ----------- #

# # - Upload Guidelines Images - #
# @storage.route(f'{storageRoute}/guidelines/<path:filename>')
# def send_static_folder_projects(filename):
#     return send_from_directory(pathFolderGuidelines, filename)

# - Upload Categories - #
@storage.route(f'{storageRoute}/<locale>/categories', methods=['GET'])
def send_categories(locale):       
    data = json.loads(open(os.path.join(pathStorage, "categories.json"), 'r').read())
    return (data[locale] if locale in data else data), 200 

# - Upload Weight - #
@storage.route(f'{storageRoute}/weights', methods=['GET'])
def send_weights():       
    return json.loads(open(os.path.join(pathStorage, "weights.json"), 'r').read()), 200