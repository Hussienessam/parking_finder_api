from flask import Flask
import model.model_app as model
import owner_user.owner_app as owner
import driver_user.driver_app as driver
import driver_user.driver_app as driver
import user.user_app as user
import database.connect_database as db_connection

db = db_connection.connect()
app = Flask(__name__)

@app.route('/find', methods=['POST'])
def find():
    return model.find()

@app.route('/add_garage', methods=['POST'])
def add_garage():
    return owner.create(db)

@app.route('/get_garage', methods=['GET'])
def get_garage():
    return owner.get(db)

@app.route('/update_garage', methods=['GET'])
def update_garage():
    return owner.update(db)

@app.route('/delete_garage', methods=['GET'])
def delete_garage():
    return owner.delete(db)

@app.route('/add_review', methods=['POST'])
def add_review():
    return driver.create(db)

@app.route('/get_review', methods=['GET'])
def get_review():
    return driver.get(db)

@app.route('/delete_review', methods=['GET'])
def delete_review():
    return driver.delete(db)