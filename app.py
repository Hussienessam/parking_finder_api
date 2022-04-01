from urllib.error import HTTPError
import urllib.request
from io import BytesIO
from PIL import Image
from flask import Flask, request
import os

import main

app = Flask(__name__)
@app.route('/find', methods=['POST'])

def find():
    input_path = 'local/image.png'
    dir_path = './local/'

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if(request.is_json):
        content = request.get_json()
        url = content['url']
        capacity = content['capacity']
    else:
        url = request.form['url']
        capacity = request.form['capacity']
    
    imageSaved, error = saveImage(input_path, url)
    if(imageSaved):
        spots = int(capacity) - main.model(input_path)
        return str(spots)

    else:
        return error

def saveImage(input_path, url):
    formats = {
        'image/jpeg': 'JPEG',
        'image/png': 'PNG',
        'image/gif': 'GIF',
        'image/jpg': 'JPG',
    }

    imageSaved = True
    error = ''

    try:
        response = urllib.request.urlopen(url)

    except HTTPError as err:
        imageSaved = False
        error = 'File not found'
        return imageSaved, error

    image_type = response.info().get('Content-Type')


    try:
        format = formats[image_type]

    except KeyError:
        imageSaved  = False
        error = 'Not a supported image format'
        return imageSaved, error

    file = BytesIO(response.read())
    img = Image.open(file)
    img.save(input_path, format=format)
    return imageSaved, error