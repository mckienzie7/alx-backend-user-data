#!/usr/bin/env python3
""" Flask Application """
from flask import Flask, request, abort, make_response, jsonify
from auth import Auth
from user import User


AUTH = Auth()
app = Flask(__name__)


@app.route('/',methods=['GET'], strict_slashes=False)
def message():
    return jsonify({"message" : "Bievenue"})

@app.route('/users', methods['POST'], strict_slashes=False)
def register():
    """
        Register User
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")





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
