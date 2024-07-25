###################
## SERVER | Main ##
###################

################
# - PACKAGES - #
################

# -- General -- #
from flask import Flask, request, redirect

# -- Scripts based Import -- #
from src.main import runBasicDetector


############
# - CORE - #
############

# -- Initialize the APP -- #
app = Flask(__name__)

# -- Redirect to the PREVIOUS URL -- #
@app.route('/api/', methods=['GET'])
def returnToMain():
    if request.referrer:  # If there's a referrer
        return redirect(request.referrer) # Redirect to the referrer
    return redirect('/')  # Otherwise, redirect to the main page
      
# -- List of Modules -- #
app = runBasicDetector(app)  # Run the Basic Detector Module

# -- Dev - Run the APP -- #
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)