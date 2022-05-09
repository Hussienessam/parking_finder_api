from flask import Flask
import model.model_app as model

app = Flask(__name__)

@app.route('/find', methods=['POST'])
def find():
    return model.find()
