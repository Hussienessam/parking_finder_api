from flask import Flask
import model.model_app as model
import user_operations.user_operations_app as user_operations
import user_operations.user_queries_app as user_queries
import user.user_app as user
import database.connect_database as db_connection
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

db = db_connection.connect()
app = Flask(__name__)
jwt = JWTManager(app)
driver_roles = ['Bookmark', 'Review', 'Camera', 'Owner', 'Snaps', 'GarageSnaps']
owner_roles = ['Garage', 'GarageCamera', 'Owner']

app.config["JWT_SECRET_KEY"] = "this-is-secret-key"


@app.route('/find', methods=['POST'])
@jwt_required()
def find():
    return model.find()


@app.route('/<string:collection>/add', methods=['POST'])
@jwt_required()
def add_document(collection):
    role = get_jwt_identity()
    if collection not in driver_roles and collection not in owner_roles:
        return "collection doesn't exist", 404
    elif collection not in driver_roles and  role == 'driver':
        return 'Not authorized', 401
    elif collection in driver_roles and role == 'owner':
        return 'Not authorized', 401
    return user_operations.create(collection, db)


@app.route('/<string:collection>/get', methods=['GET'])
@jwt_required()
def get_document(collection):
    if collection not in driver_roles and collection not in owner_roles:
        return "collection doesn't exist", 404
    return user_operations.get(collection, db)


@app.route('/<string:collection>/update', methods=['PUT'])
@jwt_required()
def update_document(collection):
    role = get_jwt_identity()
    if collection not in driver_roles and collection not in owner_roles:
        return "collection doesn't exist", 404
    if role == 'driver':
        return 'Not authorized', 401
    return user_operations.update(collection, db)


@app.route('/<string:collection>/delete', methods=['DELETE'])
@jwt_required()
def delete_document(collection):
    role = get_jwt_identity()
    if collection not in driver_roles and collection not in owner_roles:
        return "collection doesn't exist", 404
    elif collection not in driver_roles and  role == 'driver':
        return 'Not authorized', 401
    elif collection in driver_roles and role == 'owner':
        return 'Not authorized', 401
    return user_operations.delete(collection, db)


@app.route('/show_garage_reviews', methods=['GET'])
@jwt_required()
def show_garage_reviews():
    return user_queries.show_garage_reviews(db)


@app.route('/show_street_reviews', methods=['GET'])
@jwt_required()
def show_street_reviews():
    role = get_jwt_identity()
    if role == 'owner':
        return 'Not authorized', 401
    return user_queries.show_street_reviews(db)


@app.route('/get_owner_garages', methods=['GET'])
@jwt_required()
def get_owner_garages():
    return user_queries.get_owner_garages(db)


@app.route('/get_user_bookmark', methods=['GET'])
@jwt_required()
def get_user_bookmark():
    role = get_jwt_identity()
    if role == 'owner':
        return 'Not authorized', 401
    return user_queries.get_user_bookmark(db)


@app.route('/sign_up', methods=['POST'])
def sign_up():
    return user.sign_up(db)


@app.route('/update_name', methods=['POST'])
@jwt_required()
def update_name():
    return user.update_name()


@app.route('/update_email', methods=['POST'])
@jwt_required()
def update_email():
    return user.update_email(db)


@app.route('/update_password', methods=['POST'])
@jwt_required()
def update_password():
    return user.update_password()


@app.route('/update_number', methods=['POST'])
@jwt_required()
def update_number():
    return user.update_number()


@app.route('/get_by_email', methods=['GET'])
@jwt_required()
def get_by_mail():
    return user.get_by_mail()


@app.route('/get_by_id', methods=['GET'])
@jwt_required()
def get_by_id():
    return user.get_by_id()


@app.route('/log_in', methods=['GET'])
def log_in():
    return user.log_in(db)


@app.route('/get_camera_info', methods=['GET'])
@jwt_required()
def get_camera_info():
    return user_queries.get_camera_info(db)
