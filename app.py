from flask import Flask
import model.model_app as model
import owner_user.owner_app as owner
import user.user_app as user
import database.connect_database as db_connection
from firebase_admin import auth

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


@app.route('/sign_up', methods=['POST'])
def sign_up():
    return user.sign_up()


@app.route('/update_name', methods=['POST'])
def update_name():
    return user.update_name()


@app.route('/update_email', methods=['POST'])
def update_email():
    return user.update_email()


@app.route('/update_password', methods=['POST'])
def update_password():
    return user.update_password()


@app.route('/update_number', methods=['POST'])
def update_number():
    return user.update_number()


@app.route('/get_by_email', methods=['GET'])
def get_by_mail():
    return user.get_by_mail()


@app.route('/get_by_id', methods=['GET'])
def get_by_id():
    return user.get_by_id()


#@app.route('/log_in', methods=['GET'])
def log_in(n,p):
    return user.log_in(n,p,db)

print(log_in("nada123@gmail.com","nadahossam"))

