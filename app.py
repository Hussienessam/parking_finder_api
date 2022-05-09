from flask import Flask
import model.model_app as model
import owner_user.owner_app as owner
import driver_user.driver_app as driver
import user.user_app as user
import database.connect_database as db

db.connect()
app = Flask(__name__)

@app.route('/find', methods=['POST'])
def find():
    return model.find(db)

@app.route('/add_garage', methods=['POST'])
def add_garage():
    return owner.create(db)
