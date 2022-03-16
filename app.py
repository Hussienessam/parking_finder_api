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
        static_file = request.files['file']
        static_file.save(input_path)

        capacity = request.form['capacity']
        spots = int(capacity) - main.model(input_path)

        return str(spots)