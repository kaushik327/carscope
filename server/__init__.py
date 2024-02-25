import os
from flask import Flask, request, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from server.vision.vision_base import load_model, predict
from server.llm.summarize import load_qa_pipeline, load_summay_pipeline, get_website_text

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
    prompt = request.values['prompt']
    if file.filename == '':
        return {
            "error": "No file uploaded"
        }, 500
    
    basedir = os.path.abspath(os.path.dirname(__file__))

    folder = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(folder):
        os.mkdir(folder)

    filename = os.path.join(
        basedir,
        app.config['UPLOAD_FOLDER'],
        secure_filename(file.filename)
    )
    file.save(filename)
    
    learner = load_model('server/models/resnet34_tuned_export.pkl')
    car_label = predict(learner, filename)
    
    website_text = get_website_text(car_label)[:100]
    
    if prompt == 'wef':
        summarizer = load_summay_pipeline()
        text_response = summarizer(website_text, min_length=5, max_length=10)[0]['summary_text']
    else:
        answerer = load_qa_pipeline()
        text_response = answerer(question= prompt, context= website_text)['answer']
        
    os.remove(filename)

    return {
        "car_label": car_label,
        "response": text_response
    }, 200
    

    