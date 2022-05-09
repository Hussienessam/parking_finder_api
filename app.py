from flask import Flask
import model.model_app as model
import owner_user.owner_app as owner
import driver_user.driver_app as driver
import user.user_app as user

app = Flask(__name__)

@app.route('/find', methods=['POST'])
def find():
    return model.find()
