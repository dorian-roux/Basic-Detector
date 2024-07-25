###################################
## SERVER / SRC | COMMON / VIEWS ##
###################################

################
# - PACKAGES - #
################

# -- General -- #
from flask import Blueprint


############
# - CORE - #
############

# -- Initialize the Blueprint -- #
views = Blueprint("basic_detector_views", __name__)

# ---------- #
# - ROUTES - #
# ---------- #

# - Default "/" - #
@views.route("/")
def default():
  	return "Application Programming Interface [API] || Basic Detector Module"