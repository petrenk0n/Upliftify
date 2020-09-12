import os
import io
import base64
from flask import Flask, redirect, request, jsonify, render_template
from flask import Flask, request, redirect, url_for,Response,render_template,send_file,make_response,jsonify,send_from_directory
from werkzeug import secure_filename
from flask_cors import CORS,cross_origin
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import config

app = Flask(__name__)

cwd = os.getcwd()

image_name = ""
search_term = ""

# Instantiates a client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "visionkeys.json"
client = vision.ImageAnnotatorClient()

# Main route
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

# Uploading image from webcam
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    myfile = request.args.get('myimage').split(',')
    imgdata = base64.b64decode(myfile[1])
    image_name = "photo.jpeg"
    with open(os.path.join(cwd, image_name), "wb") as f:
        f.write(imgdata)
    return render_template('index.html')

# Identify object route
@app.route('/identify', methods=['GET'])
def identify():
    with io.open("photo.jpeg", 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        
        # Handle client's response
        # Neutral case
        if likelihood_name[face.anger_likelihood] == "VERY_UNLIKELY" and likelihood_name[face.joy_likelihood] == "VERY_UNLIKELY" and likelihood_name[face.surprise_likelihood] == "VERY_UNLIKELY":
            search_term = "uplift"
            print(search_term)
        # Angry case
        elif likelihood_name[face.anger_likelihood] == "VERY_LIKELY" and likelihood_name[face.joy_likelihood] == "VERY_UNLIKELY" and likelihood_name[face.surprise_likelihood] == "VERY_UNLIKELY":
            search_term = "chill"
            print(search_term)
        # Joy case
        elif likelihood_name[face.anger_likelihood] == "VERY_UNLIKELY" and likelihood_name[face.joy_likelihood] == "VERY_LIKELY" and likelihood_name[face.surprise_likelihood] == "VERY_UNLIKELY":
            search_term = "joyful"
            print(search_term)

        # Spotify api integration

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        # print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)