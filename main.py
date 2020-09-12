from flask import Flask, redirect, request, jsonify, render_template
from flask import Flask, request, redirect, url_for,Response,render_template,send_file,make_response,jsonify,send_from_directory
from werkzeug import secure_filename
from flask_cors import CORS,cross_origin
from google.cloud import vision
from google.cloud.vision import types
import requests
import os
import io
import base64

app = Flask(__name__)

cwd = os.getcwd()

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def identify():
    myfile= request.args.get('myimage').split(',')
    imgdata = base64.b64decode(myfile[1])
    image_name = "photo.jpeg"
    with open(os.path.join(cwd, image_name), "wb") as f:
        f.write(imgdata)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)