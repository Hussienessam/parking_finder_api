from flask import Flask, request
import mock_camera.webcam as camera
import model.model_app as model
from user_operations.HTTP_Exception import HTTP_Exception
import user_operations.user_operations_app as user_operations
import user_operations.user_queries_app as user_queries
import user_operations.user_validations_app as user_validations
import user_operations.user_auth_app as user_auth
import user.user_app as user_app
import database.connect_database as db_connection
import database.login_connect as login_connection
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

db, bucket = db_connection.connect()
auth, storage = login_connection.connect()
app = Flask(__name__)
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = "this-is-secret-key"

@app.route('/find', methods=['POST'])
@jwt_required()
def find():
    return model.find()

@app.route('/mocking_camera', methods=['POST'])
def mock():
    return camera.mock(db, bucket, storage)

@app.route('/<string:collection>/add', methods=['POST'])
@jwt_required()
def add_document(collection):
    try:
        userID = get_jwt_identity()     
        
        return user_operations.create(collection, db, userID)

    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400



@app.route('/<string:collection>/get', methods=['GET'])
@jwt_required()
def get_document(collection):
    try:
        userID = get_jwt_identity()
            
        user_auth.authorize_request(collection, db, request, userID)

        return user_operations.get(collection, db)

    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400


@app.route('/<string:collection>/update', methods=['PUT'])
@jwt_required()
def update_document(collection):
    try:        
        userID = get_jwt_identity()

        return user_operations.update(collection, db, userID)
    
    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400



@app.route('/<string:collection>/delete', methods=['DELETE'])
@jwt_required()
def delete_document(collection):
    try:   
        userID = get_jwt_identity()

        user_auth.authorize_request(collection, db, request, userID)
        
        return user_operations.delete(collection, db)

    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400

@app.route('/show_garage_reviews', methods=['GET'])
@jwt_required()
def show_garage_reviews():
    return user_queries.show_garage_reviews(db)


@app.route('/show_street_reviews', methods=['GET'])
@jwt_required()
def show_street_reviews():
    return user_queries.show_street_reviews(db)


@app.route('/get_owner_garages', methods=['GET'])
@jwt_required()
def get_owner_garages():
    try:   
        userID = get_jwt_identity()

        user_auth.authorize_request('OwnerRequest', db, request, userID)

        return user_queries.get_owner_garages(db)

    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400


@app.route('/get_user_bookmark', methods=['GET'])
@jwt_required()
def get_user_bookmark():
    try:
        userID = get_jwt_identity()

        user_validations.validate_driver(db, {request.args.get('driverID')})

        user_auth.authorize_request('DriverRequests', db, request, userID)

        return user_queries.get_user_bookmark(db, request.args.get('driverID'))
        
    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400 

@app.route('/get_location_bookmark', methods=['POST'])
@jwt_required()
def get_location_bookmark():
    try:
        userID = get_jwt_identity()

        user_validations.validate_driver(db, {request.json['driverID']})

        user_auth.authorize_request('DriverRequests', db, request, userID)

        return user_queries.get_location_bookmark(db)
    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400 

@app.route('/clear_driver_history', methods=['DELETE'])
@jwt_required()
def clear_driver_history():
    try:
        userID = get_jwt_identity()

        user_validations.validate_driver(db, {request.args.get('driverID')})

        user_auth.authorize_request('DriverRequests', db, request, userID)
        
        return user_queries.clear_driver_history(db)

    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400 

@app.route('/clear_driver_bookmark', methods=['DELETE'])
@jwt_required()
def clear_driver_bookmark():
    try:    
        userID = get_jwt_identity()

        user_validations.validate_driver(db, {request.args.get('driverID')})

        user_auth.authorize_request('DriverRequests', db, request, userID)

        return user_queries.clear_driver_bookmark(db)
    
    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400 

@app.route('/get_camera_info', methods=['GET'])
@jwt_required()
def get_camera_info():
    try:    
        userID = get_jwt_identity()

        user_auth.authorize_request('CameraRequest', db, request, userID)
        
        return user_queries.get_camera_info(db)
    
    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400 


@app.route('/log_in', methods=['GET'])
def log_in():
    return user_app.log_in()


@app.route('/sign_up', methods=['POST'])
def sign_up():
    return user_app.sign_up(db)

@app.route('/update_user', methods=['PUT'])
@jwt_required()
def update_user():
    try:
        userID = get_jwt_identity()

        user_auth.authorize_user(request, userID)

        return user_app.update_user()
    
    except HTTP_Exception as e:
        return f"An Error Occurred: {e.message}", e.status_code 
    
    except Exception as e:
        return f"An Error Occurred: {e}", 400 

@app.route('/get_by_email', methods=['GET'])
@jwt_required()
def get_by_mail():
    return user_app.get_by_mail()


@app.route('/get_by_id', methods=['GET'])
@jwt_required()
def get_by_id():
    return user_app.get_by_id()
