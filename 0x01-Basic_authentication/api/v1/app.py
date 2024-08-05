#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = os.getenv('AUTH_TYPE')
# Define the list of public paths
public_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

if auth_type:
    from api.v1.auth.auth import Auth
    auth = Auth()

@app.before_request
def before_request():
    """
    Handle authentication before processing the request.
    """
    if auth is None:
        # If auth is None, do nothing
        return
    
    # Check if the path requires authentication
    if not any(request.path.startswith(path) for path in public_paths):
        if auth.require_auth(request.path, public_paths):
            # Check if the Authorization header is present
            if auth.authorization_header(request) is None:
                abort(401)  # Unauthorized
            
            # Check if the current user is present
            if auth.current_user(request) is None:
                abort(403)  # Forbidden

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404
@app.errorhandler(401)
def unauthorized(error) -> str:
    """ UnAuthorized
    """
    return jsonify({"error" : "Unauthorized"}), 401
@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden
    """
    return jsonify({"error" : "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

