#!/usr/bin/env python3
""" Flask Application """
from flask import Flask, request, abort, make_response, jsonify
from auth import Auth
from user import User
from sqlalchemy.orm.exc import NoResultFound
from db import DB

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def message():
    return jsonify({"message": "Bievenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register():
    """
        Register User
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
        Loging in User
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """ Main Funstion """
    app.run(host="0.0.0.0", port="5000")
