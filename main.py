from flask import Flask, redirect, request, jsonify, render_template
from google.cloud import vision
from google.cloud.vision import types
import requests
import os
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def identify():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000)