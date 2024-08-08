#!/usr/bin/env python3
"""Auth class created"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Class to manage api authentications"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth paths"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        slashless_exclude_paths: List[str] = []
        asterik_exclude_paths: List[str] = []

        for new_path in excluded_paths:
            slashless_exclude_paths.append(new_path[:-1])

        for new_path in slashless_exclude_paths:
            if path.startswith(new_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None:
            return None

        auth_header: str = request.headers.get("Authorization")

        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
