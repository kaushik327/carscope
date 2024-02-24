from flask import Flask, request

app = Flask(__name__)

@app.route("/hello_world")
def hello_world():
    return {
        "response": "Hello, World!"
    }