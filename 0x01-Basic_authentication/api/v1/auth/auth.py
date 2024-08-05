#!/usr/bin/env python3
# api/v1/auth/auth.py

from typing import List, TypeVar
from flask import request

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required.
        Currently, always returns False.

        :param path: The path to check
        :param excluded_paths: A list of paths that do not require authentication
        :return: False
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure the path and excluded_paths are slash tolerant
        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path[-1] != '/':
                excluded_path += '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        :param request: The Flask request object
        :return: None
        """
        if request is None:
            return None
        
        request_header = request.headers.get("Authorization")
        if not request_header:
            return None
        else:
            request_header


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.

        :param request: The Flask request object
        :return: None
        """
        return None

