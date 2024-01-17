
"""

Werkzeug provides a bunch of utilities for developing WSGI-compliant applications. 
These utilities do things like parsing headers, sending and receiving cookies, 
providing access to form data, generating redirects, generating error pages when 
there's an exception, even providing an interactive debugger that runs in the browser. 
Flask then builds upon this foundation to provide a complete web framework.
"""

from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from detect import detect
import os
# =============================================================================
# from uuid import uuid4
# import filetype
# 
# def make_unique(string):
#     ident = uuid4().__str__()
#     return f"{ident}-{string}"
# =============================================================================

#Save images to the 'static' folder as Flask serves images from this directory
UPLOAD_FOLDER = 'static/input/'
RESULT_FOLDER = 'static/output'
# UPLOAD_FOLDER_VIDEO = 'statis/video_input/'

#Create an app object using the Flask class. 
app = Flask(__name__, static_folder="static")

#Add reference fingerprint. 
#Cookies travel with a signature that they claim to be legit. 
#Legitimacy here means that the signature was issued by the owner of the cookie.
#Others cannot change this cookie as it needs the secret key. 
#It's used as the key to encrypt the session - which can be stored in a cookie.
#Cookies should be encrypted if they contain potentially sensitive information.
app.secret_key = "secret key"

#Define the upload folder to save images uploaded by the user. 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, index function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 
@app.route('/')
def index():
    return render_template('index.html')

#Add Post method to the decorator to allow for form submission. 
@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
# =============================================================================
#         if not (filetype.is_image(file.filename) or filetype.is_video(file.filename)):
#             flash('File must be an image or video')
#             return redirect(request.url)
# =============================================================================
        if file:
            print(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
            filename = secure_filename(file.filename)  #Use this werkzeug method to secure filename. 
            # unique_filename = make_unique(filename)
            # if filetype.is_image(filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # else:
                # file.save(os.path.join(app.config['UPLOAD_FOLDER_VIDEO'],filename))
            #getPrediction(filename)
            label = detect(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            flash(label)
            folder=os.listdir(app.config['RESULT_FOLDER'])[-1]
            full_filename = os.path.join(app.config['RESULT_FOLDER'],folder, filename)
            flash(full_filename)
            return redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) #Define port so we can map container port to localhost
    app.run(host='0.0.0.0', port=port)  #Define 0.0.0.0 for Docker
