import datetime
from flask import request, jsonify
from firebase_admin import auth
import database.login_connect as db_connection
from flask_jwt_extended import create_access_token
import user_operations.user_handlers_app as user_handlers

login_auth = db_connection.connect()[0]


def sign_up(db):
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    number = request.json['number']
    role = request.json['role']
    try :
        try :
            user = auth.get_user_by_email(email)
            return jsonify({"value": "email already exists"}), 400
        except Exception as e:
            pass
        
        try :
            user = auth.get_user_by_phone_number(number)
            return jsonify({"value": "phone number already exists"}), 400
        except Exception as e:
            pass

        user = auth.create_user(email=email,
                                password=password,
                                phone_number=number,
                                display_name=name,
                                )
        doc_ref = db.collection(u'Owner')
        own = {"email":email, "role":role}
        doc_ref.document(user.uid).set(own)
        return jsonify({"value": "sign up successful"}), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def get_role(id, db):
    try:
        user_ref = db.collection(u'Owner')
        user = user_ref.document(id).get().to_dict()
        return user['role']

    except Exception as e:       
        return f"An Error Occurred: {e}", 400

def log_in():
    password = request.args.get('password')
    email = request.args.get('email')
    try:
        try :
            user = login_auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            return jsonify({"value": f"incorrect email or password {e}"}), 400
        
        access_token = create_access_token(identity=user['localId'], expires_delta=datetime.timedelta(days=7))
        return jsonify(
            {'id': user['localId'], 'idToken': access_token, 'value': "login successful"}), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400


def update_name():
    name = request.json['name']
    email = request.json['email']
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, display_name=name)
        user = auth.get_user(id)
        return jsonify(
            {'id': user.uid, 'name': user.display_name, 'email': user.email, 'number': user.phone_number}), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 400

def update_email(db):
    email = request.json['email']
    new_email = request.json['newemail']
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, email=new_email)
        user_handlers.handle_update_user(db, id, new_email)
        user = auth.get_user(id)
        return jsonify(
            {'id': user.uid, 'name': user.display_name, 
            'email': user.email, 'number': user.phone_number}), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 400


def update_number():
    number = request.json['number']
    email = request.json['email']
    try:
        user = auth.get_user_by_email(email)
        id = user.uid
        auth.update_user(id, phone_number=number)
        user = auth.get_user(id)
        return jsonify(
            {'id': user.uid, 'name': user.display_name, 'email': user.email, 'number': user.phone_number}), 200

    except Exception as e:
        return f"An Error Occurred: {e}", 400


def update_password():
    oldpass = request.json['old_password']
    email = request.json['email']
    newpass = request.json['new_password']
    try:
        try :
            user = login_auth.sign_in_with_email_and_password(email, oldpass)
        except Exception as e:
            return jsonify({"value": "incorrect password"}), 400
        id = user['localId']
        auth.update_user(id, password=newpass)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def parse_error(error):
    return error.split(' (')[0]

def update_user():
    id = request.json['id']
    name = request.json['name']
    number = request.json['number']
    email = request.json['email']
    oldpass = request.json['old_password']
    newpass = request.json['new_password']
    try:
        if newpass != "":
            old_email = auth.get_user(id).email
            try :
                user = login_auth.sign_in_with_email_and_password(old_email, oldpass)
            except Exception as e:
                return jsonify("incorrect password"), 400
            auth.update_user(id, display_name= name, email= email, phone_number=number, password=newpass)
        
        else:
            auth.update_user(id, display_name= name, email= email, phone_number=number)

        return jsonify("The user has been updated successfully"), 200
    except Exception as e:
        return f"{parse_error(str(e))}", 400

def get_by_mail():
    email = request.args.get('email')
    try:
        user = auth.get_user_by_email(email)
        return jsonify({'id': user.uid, 'name': user.display_name, 
        'email': user.email, 'number': user.phone_number}), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400


def get_by_id():
    id = request.args.get('id')
    try:
        user = auth.get_user(id)
        return jsonify({'id': user.uid, 'name': user.display_name,
        'email': user.email, 'number': user.phone_number}), 200
    except Exception as e:
        return f"An Error Occurred: {e}", 400

def get_user_by_id(id):
    try:
        user = auth.get_user(id)
        return {'id': user.uid, 'name': user.display_name, 
        'email': user.email, 'number': user.phone_number}
    except Exception as e:
        return f"An Error Occurred: {e}", 400
