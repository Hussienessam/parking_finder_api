import urllib.request
from io import BytesIO
from PIL import Image
from flask import Flask, request
import os

import main

app = Flask(__name__)
@app.route('/find', methods=['GET', 'POST'])

def find():
    input_path = 'local/image.png'
    dir_path = './local/'

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if request.method == 'POST':
        url = request.form['url']
        capacity = request.form['capacity']

        formats = {
            'image/jpeg': 'JPEG',
            'image/png': 'PNG',
            'image/gif': 'GIF',
            'image/jpg': 'JPG',
        }
        response = urllib.request.urlopen(url)
        image_type = response.info().get('Content-Type')
        try:
            format = formats[image_type]
        except KeyError:
            raise ValueError('Not a supported image format')
        file = BytesIO(response.read())
        img = Image.open(file)
        img.save(input_path, format=format)

        spots = int(capacity) - main.model(input_path)

        return str(spots)