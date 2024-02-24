import os
from flask import Flask, request, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'file_uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/hello_world")
def hello_world():
    return {
        "response": "Hello, World!"
    }, 200

@app.route("/upload_image", methods=['POST'])
def upload_image():
    # https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
    file = request.files['file']
    if file.filename == '':
        return {
            "error": "No file uploaded"
        }, 500
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        basedir,
        app.config['UPLOAD_FOLDER'],
        secure_filename(file.filename)
    )
    file.save(filename)
    
    # TODO: call functions to run models
    text_response = "Test response"

    os.remove(filename)

    return {
        "response": text_response
    }, 200
    

    