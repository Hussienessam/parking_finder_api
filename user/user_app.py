from flask import request, jsonify
from firebase_admin import auth


def sign_up():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    number = request.json['number']
    try :
        user = auth.create_user(email=email,
                                password=password,
                                phone_number=number,
                                display_name=name,
                                )
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def update_name():
    name = request.json['name']
    id = request.json['id']
    try:
        user=auth.update_user(id,display_name=name)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def update_email():
    email = request.json['email']
    id = request.json['id']
    try:
        user=auth.update_user(id,email=email)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get_by_mail():
    email = request.json['email']

    try:
        user = auth.get_user_by_email(email)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get_by_number():
    number = request.json['number']

    try:
        user = auth.get_user_by_phone_number(number)
        return jsonify(format(user)), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


def get_by_id():
    id = request.json['id']
    try:
        user = auth.get_user(id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
