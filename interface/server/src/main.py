#########################
## SERVER / SRC | MAIN ##
#########################

################
# - PACKAGES - #
################

# -- General -- #
import os
from flask_cors import CORS

# -- Scripts based Import -- #
from .common.views import views
from .common.source_image import src_image
from .common.source_video import src_video
from .common.storage import storage

#################
# - FUNCTIONS - #
#################

# -- Main Runner for the "Basic Detector" Module -- #
def runBasicDetector(app):
    """Main Runner for the Basic Detector Module
    Args:
        app (flask): the flask app.
    """
    global Base, session
    
    # -- Setup FLASK APP Configuration -- #
    CORS(app)
    
    # -- Register the BLUEPRINTS -- #
    blueprint_url_prefix = '/basic-detector'
    app.register_blueprint(views, url_prefix=blueprint_url_prefix)
    app.register_blueprint(src_image, url_prefix=blueprint_url_prefix)
    app.register_blueprint(src_video, url_prefix=blueprint_url_prefix)
    app.register_blueprint(storage, url_prefix=blueprint_url_prefix)
    
    # -- Return the APP -- #
    return app